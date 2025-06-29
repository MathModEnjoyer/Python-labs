import sys
import math
import json
import numpy as np
def calculate_function(n0: float, nk: float, h: float, a: float, b: float, c: float) -> dict:
    """
    Функция, которая на основе значений x вычисляет значения y
    Аргументы:
    n0 – левая граница диапазона x 
    nk – правая граница диапазона x
    h – шаг диапазона x
    a, b, с - параметры, используемые при вычислении функции y
    Возвращает:
    dict(...), где ключи представляют собой элементы диапазона x, и значения – соответствующие им значения функции y
    """
    myDict = {}
    xCount = int((nk - n0) / h)
    xRange = np.linspace(n0, nk, xCount)
    for i in range(xCount):
        myDict["x = " + str(xRange[i])] = "y = " + str(a* math.sin(b * xRange[i]) - math.cos(c * xRange[i]) ** 2)
    return myDict

dictR = {}

if len(sys.argv) > 1:
    try:
        dictR = {}
        dictR['n0'] = float(sys.argv[1])
        dictR['nk'] = float(sys.argv[2])
        dictR['h'] = float(sys.argv[3])
        dictR['a'] = float(sys.argv[4])
        dictR['b'] = float(sys.argv[5])
        dictR['c'] = float(sys.argv[6])
    except IndexError:
        print("Некорректное количество аргументов")
else:
    try: 
        with open('config.json', 'r') as fr:
            dictR = json.load(fr)
    except FileNotFoundError:
        print("Файл config.json не найден")

if len(dictR) >= 6: 
    with open("results.json", 'w') as fw:
        temp = calculate_function(dictR['n0'], dictR['nk'], dictR['h'], dictR['a'], dictR['b'], dictR['c'])
        fw.write(json.dumps(temp))
