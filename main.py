# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import glob
import multiprocessing
import time
import random
from multiprocessing import Process


def create_file(n_proc, fileNumber):
    for j in range(50):
        randfile = open("RandomFile{}.{}.txt".format(n_proc, str(fileNumber)), "w")
        numofstring = random.randint(20, 100)
        for i in range(numofstring):
            line = str(random.randint(0, 9))
            for g in range(random.randint(5, 40)):
                line += " " + str(random.randint(0, 9))
            line += "\n"
            randfile.write(line)
        randfile.close()


def create_files(n_proc, calc):
    for i in range(calc):
        create_file(n_proc, i)


def calculate_file(result_sum, lock, file):
    row_file = open(file, "r")
    row_file = row_file.read()
    nums = row_file.replace("\n", " ")
    array_nums = nums.split(" ")
    sum_in_file = 0
    for num in array_nums:
        if num != "":
            sum_in_file = sum_in_file + int(num)
    lock.acquire()
    result_sum.value = result_sum.value + sum_in_file
    lock.release()


def create_file_process(n_proc, calc):
    processes = []
    for i in range(n_proc):
        p = Process(target=create_files, args=(i, calc))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()


def get_sum_of_all_files():
    manager = multiprocessing.Manager()
    files = glob.glob('*.txt')
    lock = multiprocessing.Lock()
    result_sum = manager.Value('sum', 0)
    processes = []

    for file in files:
        p = Process(target=calculate_file, args=(result_sum, lock, file))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print(result_sum.value)


if __name__ == "__main__":
    n_proc = multiprocessing.cpu_count()
    calc = 1000 // n_proc
    start_time = time.time()
    create_file_process(n_proc, calc)
    print(time.time() - start_time, "seconds")
    start_time_of_sum = time.time()
    get_sum_of_all_files()
    print(time.time() - start_time_of_sum, "seconds")
