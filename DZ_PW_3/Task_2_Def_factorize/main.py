from multiprocessing import Pool, cpu_count
from time import perf_counter_ns


def measure_time(func):
    """ Вимірює час виконання декорованої функції """

    def wrapper(*args, **kwargs):
        # фіксуємо старт
        start = perf_counter_ns()
        result = func(*args, **kwargs)
        # фіксуємо кінець
        end = perf_counter_ns()
        print(
            f"function `{func.__name__}({args},{kwargs})` took {(end-start)/1000000000} s")
        return result

    return wrapper


def factorization(num: int) -> list[int]:
    """ Функція повертає список дільників заданого числа num """
    # частка від ділення
    fractions = [1, num]
    # дільники
    dividers = []
    # перший дільник
    divider = 2

    n = num
    # поки дільник менший від поточного діленого
    while divider < n:
        # випадок : якщо поточне ділене ділиться на дільник націло
        if n % divider == 0:
            # ділимо ділене
            n = n // divider
            # додаємо в список ділене
            fractions.append(n)
            # додаємо в список дільник
            dividers.append(divider)
        # випадок : не ділиться націло
        else:
            # оновлюємо ділене на початкове значення
            n = num
            # збільшуємо дільник
            divider += 1
    # повертаємо відсортований список
    return sorted(list(set(fractions + dividers)))


@measure_time
def factorize(*args: tuple[int]) -> list[list[int]]:
    """ 
    Функція приймає змінну кількість аргументів - цілих додатніх чисел.\n
    Для кожного числа знаходить всі дільники.\n
    Результатом буде список списків.\n
    Обрахунки відбуваються послідовно в одному процесі. 
    """
    results = []
    for num in args:
        # перевіряємо чи коректні дані передані
        if not isinstance(num, int) or num < 0:
            raise ValueError(
                "This function only works with integer positive arguments !")
        # запускаємо для кожного елемента та додаємо в список
        results.append(factorization(num))

    return results


@measure_time
def factorize_multi_process(*args: tuple[int]) -> list[list[int]]:
    """ 
    Функція приймає змінну кількість аргументів - цілих додатніх чисел.\n
    Для кожного числа знаходить всі дільники.\n
    Результатом буде список списків.\n
    Обрахунки відбуваються одночасно паралельно в різних процесах.
    """
    # перевіряємо чи коректні дані передані
    for num in args:
        if not isinstance(num, int) or num < 0:
            raise ValueError(
                "This function only works with integer positive arguments !")
    
    # Запускаємо пул процесів 
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(factorization, args)

    return results


def main():

    # тестуємо функцію
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("Single-process function testing is OK")

    # тестуємо функцію
    a, b, c, d = factorize_multi_process(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("Multi-process function testing is OK")
    print("\n\n\n")

    # кортеж завдань для функції
    tasks = (35463257, 23423452, 123213213, 23432432,
             4234234, 312312315, 43534534, 34123123,
             4354534, 23123, 324324, 23123,
             432423, 234435, 74645, 1236543,
             123213, 4323545, 21312, 54634,
             213123, 565464, 234234555, 563653,
             32132, 5345345,345345,234234,
             234324,53435435,123123,123123,
             232344,6546346534,321312,5465465,
             21312,43534,123123,645645,123123,
             123123,54353,123123,453453,12312,
             43242,545,23423,64562, 12321,564324,
             )

    # запускаємо два варіанти функції
    
    print("Single-process function is working.....")
    factorize(*tasks)

    print("Multi-process function is working.....")
    factorize_multi_process(*tasks)

    # можна зробити висновок що на відносно невеликих вхідних даних однопроцесна версія працює швидше,
    # але вже на більших за об'ємом вхідних даних багатопроцесна версія працює швидше

if __name__ == "__main__":
    main()
