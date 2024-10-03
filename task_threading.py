import threading
import timeit
from collections import defaultdict
from pathlib import Path

def search_in_file(file_path, keywords, results, lock):
    # Обробка можливих помилок при читанні файлів
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    with lock:  # Використовуємо блокування для безпечного доступу до спільного ресурсу
                        results[keyword].append(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def thread_task(files, keywords, results, lock):
    for file in files:
        search_in_file(file, keywords, results, lock)

def main_threading(file_paths, keywords):
    # Додаємо вимір часу виконання
    start_time = timeit.default_timer()  # Початок вимірювання часу

    num_threads = 4  # Визначення кількості потоків
    threads = []
    results = defaultdict(list)
    lock = threading.Lock()  # Блокування для синхронізації доступу до словника результатів

    # Описуємо логіку ефективного розділення файлів між потоками
    # Розподіляємо файли рівномірно між потоками
    file_chunks = [file_paths[i::num_threads] for i in range(num_threads)]

    # Створення та запуск потоків
    for i in range(num_threads):
        thread = threading.Thread(target=thread_task, args=(file_chunks[i], keywords, results, lock))
        threads.append(thread)
        thread.start()

    # Очікування завершення всіх потоків
    for thread in threads:
        thread.join()

    end_time = timeit.default_timer()  # Кінець вимірювання часу
    print(f"Execution time: {end_time - start_time:.2f} seconds")  # Виведення часу виконання

    return results


if __name__ == '__main__':
    # Приклад виклику
    # Отримання всіх файлів з розширенням .txt з папки "input"
    file_paths = list(Path("input").glob("*.txt"))  
    print(f"File paths: {file_paths}\n")
    
    # Список ключових слів для пошуку
    keywords = ["pulvinar", "potenti", "dictum"]  
    
    # Виклик основної функції для багатопотокового пошуку
    results = main_threading(file_paths, keywords)  
    
    # Виведення результатів
    print(results)
