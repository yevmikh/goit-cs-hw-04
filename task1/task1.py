import threading
from collections import defaultdict
import time

def search_keywords(file_list, keywords, result_dict, lock):
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        with lock:
                            result_dict[keyword].append(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def main_threading(files, keywords):
    start_time = time.time()
    num_threads = 4
    file_chunks = [files[i::num_threads] for i in range(num_threads)]
    threads = []
    result_dict = defaultdict(list)
    lock = threading.Lock()

    for i in range(num_threads):
        thread = threading.Thread(target=search_keywords, args=(file_chunks[i], keywords, result_dict, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threaded execution time: {end_time - start_time} seconds")
    return dict(result_dict)

if __name__ == "__main__":
    num_files = int(input("Enter the number of files: "))
    files = [input(f"Enter path for file {i+1}: ") for i in range(num_files)]
    num_keywords = int(input("Enter the number of keywords: "))
    keywords = [input(f"Enter keyword {i+1}: ") for i in range(num_keywords)]
    results = main_threading(files, keywords)
    for keyword, file_paths in results.items():
        print(f"{keyword}: {file_paths}")


