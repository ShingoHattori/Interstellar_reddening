import csv
import sys
sys.path.append("..")
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import cv2



def open_csv(filepath):
    #csvファイルを開いてリストにする関数
    all_data = []
    with open(filepath, newline='') as CsvFile:
        reader = csv.reader(CsvFile, delimiter=' ', quotechar = '|')
        for row in reader:
            all_data.append(', '.join(row))
    return all_data



def separete_csv(all_data):
    #open_csvで作成されたリストをもとに，データの集合とキーの集合を作る関数
    sep_datas = []
    for var in range(1, len(all_data)):
        data = all_data[var]
        sep_data = data.split(",")
        sep_datas.append(sep_data)

    keys_data = all_data[0].split(",")

    keys = {}

    for var in range(0, len(keys_data)):
        keys[str(keys_data[var])] = var

    return sep_datas, keys

def getsigma(data):
    # 引数dataのsigmaを求める関数
    sigma = ((np.sum((data - np.mean(data)) ** 2)) / len(data)) ** (1/2)
    return sigma

def sigma_clipping_index(data, n = 1):
    # dataのうち,n sigma以内に入っているデータのみを返す関数
    mean_value = np.mean(data)
    sigma = getsigma(data)
    value_index = np.where((mean_value - n * sigma < data) &  (data < mean_value + n * sigma))
    return value_index

def both_array_sigma(array1, array2, n = 1):
    # 2つのデータについて，その両方でn sigma以内に入っているデータのみを返す関数
    array1_index = sigma_clipping_index(array1, n)
    array2_index = sigma_clipping_index(array2, n)
    sameindex = np.intersect1d(array1_index[0],array2_index[0])
    return_array1 = array1[sameindex]
    return_array2 = array2[sameindex]
    return return_array1, return_array2
