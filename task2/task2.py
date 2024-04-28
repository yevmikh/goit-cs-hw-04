from multiprocessing import Process, Queue, Manager, current_process
import multiprocessing
import time

def process_files(file_queue, keywords, result_dict, lock):
    while True:
        file_path = file_queue.get()
        if file_path is None:
            break
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        with lock:
                            result_dict[keyword].append(file_path)
        except Exception as e:
            print(f"Error in {current_process().name} while processing file {file_path}: {e}")

def main_multiprocessing(files, keywords):
    start_time = time.time()
    num_processes = multiprocessing.cpu_count()
    file_queue = Queue()
    manager = Manager()
    result_dict = manager.dict()
    lock = manager.Lock()

    for keyword in keywords:
        result_dict[keyword] = manager.list()

    for file in files:
        file_queue.put(file)

    processes = []
    for _ in range(num_processes):
        process = Process(target=process_files, args=(file_queue, keywords, result_dict, lock))
        processes.append(process)
        process.start()

    for _ in range(num_processes):
        file_queue.put(None)

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Multiprocess execution time: {end_time - start_time} seconds")
    return dict((key, list(val)) for key, val in result_dict.items())

if __name__ == "__main__":
    num_files = int(input("Enter the number of files: "))
    files = [input(f"Enter path for file {i+1}: ") for i in range(num_files)]
    num_keywords = int(input("Enter the number of keywords: "))
    keywords = [input(f"Enter keyword {i+1}: ") for i in range(num_keywords)]
    results = main_multiprocessing(files, keywords)
    for keyword, file_paths in results.items():
        print(f"{keyword}: {file_paths}")
