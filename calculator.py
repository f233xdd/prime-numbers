import time
import threading
import math
import json


exit_flag = False # unchangeable variable
alive = True # unchangeable variable
time_out = 60
time1 = time.perf_counter() # get start time
mode = 'json'


def core_function(max_number=500):
    """计算素数的核心函数"""
    # print("Core function start!")
    print(f"Target: {max_number}")

    for current_number in range(1, max_number):
        # 遍历所有需要计算的数字
        result = True

        for divisor in range(0, int(math.sqrt(max_number))):
            # 把单个需要计算的数字除以所有可能的数

            if not alive:
                exit(0)

            if divisor == 0 or divisor == 1:
                # 进一步缩小范围，去除0和1
                continue

            if divisor + 1 == current_number:
                # 判断当前除数是否与当前数只差1, 是则立刻停止循环
                break

            if (current_number % divisor) != 0:
                # 判断是否能整除, 不能则继续, 能则到else语句
                continue

            else:
                # 停止循环并把结果设定为False
                result = False
                break

        if result:
            # 若所有除法做完都为小数, 则不触发else语句, result为默认True, 迭代器传出当前数字
            yield current_number


def stopwatch():
    """简单的计数器"""
    global alive
    # print("Stopwatch start!")

    while True:

        time2 = time.perf_counter()
        time_in_total = round(time2 - time1, 2)
        if exit_flag:
            # 检查run_core_function是否运行完毕，是则打印出运行的时间
            print('\n')
            print(f"Run for {time_in_total}s in total to work out the numbers")
            exit(0)
        if time_in_total > time_out:
            # 超时判断, 若超时则把alive设定为False并引发TimeoutError
            print(f"_____________Run over {time_out}s_____________")
            alive = False
            raise TimeoutError


def run_core_function(var=500000):
    """运行并打印出结果"""
    global exit_flag
    number_list = []

    for num in core_function(var):
        # run core function
        number_list.append(num)

    exit_flag = True

    if mode == 'txt':
        with open('result.txt', 'w') as text:
            text.write(str(number_list))
            
    elif mode == 'json':
        with open('result.json', 'w') as json_file:
            json_file.write(json.dumps(number_list))
            
    else:
        print("Do you want to print the result?")
        
        decision = input('> ')
        if decision == 'yes', or decision == 'Yes':
              print(number_list)
        else:
              print('Ok...')
    print("Finished successfully.")


def main():
    """开始多线程的函数(主函数)"""
    thread1 = threading.Thread(target=run_core_function)
    thread2 = threading.Thread(target=stopwatch)

    for thread in [thread1, thread2]:
        # start threads
        thread.start()
    for thread in [thread1, thread2]:
        # synchronize threads
        thread.join()

    # print("Main thread is over!")


if __name__ == '__main__':
    # run main function
    main()
