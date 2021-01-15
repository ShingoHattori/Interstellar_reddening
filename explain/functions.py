import csv
import sys
sys.path.append("..")
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import cv2



def open_csv(filepath):# CSVを開いてリストにする
    all_data = []
    with open(filepath, newline='') as CsvFile:
        reader = csv.reader(CsvFile, delimiter=' ', quotechar = '|')
        for row in reader:
            all_data.append(', '.join(row))
    return all_data



def separete_csv(all_data):# リストを辞書にする
    #返り値は，各天体のデータのリストと，キーとインデックスを変換するための辞書
    sep_datas = []

    #とりあえずリストに突っ込む
    #0行目はindexデータであって不要である．よって除去する．
    for var in range(1, len(all_data)):
        data = all_data[var]
        sep_data = data.split(",")
        sep_datas.append(sep_data)

    #キーのみのリストを作成する
    keys_data = all_data[0].split(",")

    keys = {}

    #キーとインデックスの紐付けを行う
    for var in range(0, len(keys_data)):
        keys[str(keys_data[var])] = var

    return sep_datas, keys

def getsigma(data):
    sigma = ((np.sum((data - np.mean(data)) ** 2)) / len(data)) ** (1/2)
    return sigma

def sigma_clipping_index(data, n = 1):
    #nsigma に入るデータのインデックスを返す
    #共有のインデックスはこのようにして取得する
    mean_value = np.mean(data)
    sigma = getsigma(data)
    value_index = np.where((mean_value - n * sigma < data) &  (data < mean_value + n * sigma))
    return value_index

def both_array_sigma(array1, array2, n = 1):
    #gets np.array and calocurete sigma. returns n sigma values
    array1_index = sigma_clipping_index(array1, n)
    array2_index = sigma_clipping_index(array2, n)
    #片方の指標で値が外れていなくても，もう片方で外れ値となっていたら解析の邪魔になるので，両方の指標で値が外れ値でないデータのインデックスを返す．
    #2つのデータで，それぞれのデータで n sigmaに収まるデータのインデックスをまとめた配列を作成し，
    #二つの配列に共通するインデックスのみを返す．
    #何故か返り値が値を一つだけ持つリストになってたんですよね
    sameindex = np.intersect1d(array1_index[0],array2_index[0])
    return_array1 = array1[sameindex]
    return_array2 = array2[sameindex]
    return return_array1, return_array2
