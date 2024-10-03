import multiprocessing
from collections import defaultdict
from pathlib import Path
import timeit
import os


def search_in_file(file_path, keywords, results_queue):
    # Додаємо обробку можливих помилок з читанням файлів
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results_queue.put((keyword, file_path))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


def process_task(files, keywords, results_queue):
    for file in files:
        search_in_file(file, keywords, results_queue)


def main_multiprocessing(file_paths, keywords):
    # Додаємо вимір часу виконання
    start_time = timeit.default_timer()  # Початок вимірювання часу
    num_processes = 4
    
    processes = []
    results_queue = multiprocessing.Queue()
    results = defaultdict(list)

    # Описуємо логіку ефективного розділення файлів між процесами
    file_chunks = [file_paths[i::num_processes] for i in range(num_processes)]  # Розділяємо файли між процесами

    # Створюємо процеси
    for i in range(num_processes):
        process = multiprocessing.Process(target=process_task, args=(file_chunks[i], keywords, results_queue))
        processes.append(process)
        process.start()

    # Очікуємо завершення всіх процесів
    for process in processes:
        process.join()

    # Збираємо результати з черги
    while not results_queue.empty():
        keyword, file_path = results_queue.get()
        results[keyword].append(file_path)

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
    
    # Виклик основної функції для багатопроцесорного пошуку
    results = main_multiprocessing(file_paths, keywords)  
    
    # Виведення результатів
    print(results)
