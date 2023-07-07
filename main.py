# -*- coding: utf-8 -*-
"""
卫东廷
基于DPCM的语音编码方案
"""
import wave
import os
import numpy as np

# 压缩文件
def compressWaveFile(wave_data):
    quantized_num = 0.05  # 量化因子
    diff_value = []  # 存储差分值
    compressed_data = []  # 存储压缩后的数据
    diff_value = [wave_data[0]]
    compressed_data = [wave_data[0]]
    for index in range(len(wave_data)):
        if index == 0:
            continue
        # 计算差分值
        diff_value.append(wave_data[index] - compressed_data[index - 1])
        # 压缩差分值
        compressed_data.append(calCompressedData(diff_value[index], quantized_num))
    return compressed_data

# 计算映射——量化具体步骤
def calCompressedData(diff_value, quantized_num):
    if diff_value > 4 * quantized_num:
        return 4
    elif diff_value < -5 * quantized_num:
        return -5
    for i in range(10):
        j = i - 5
        if (j - 1) * quantized_num < diff_value <= j * quantized_num:
            return j

for i in range(10):
    original_file_path = "./原始文件/" + str(i + 1) + ".wav"
    f = wave.open(original_file_path, "rb")
    params = f.getparams()
    # nframes 采样点数目
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = f.readframes(nframes)  # str_data 是二进制字符串
    # 转成二字节数组形式（每个采样点占两个字节）
    wave_data = np.fromstring(str_data, dtype=np.short)
    print(str(i + 1) + ".wav的" + "采样点数目：" + str(len(wave_data)))  # 输出应为采样点数目
    f.close()
    compressed_data = compressWaveFile(wave_data)
    # 写压缩文件
    with open("./压缩文件/" + str(i + 1) + ".dpc", "wb") as f:
        for num in compressed_data:
            f.write(np.int16(num))
    # 原始文件大小
    original_file_size = os.path.getsize(original_file_path)
    print("\t" + "原始字节大小：" + str(original_file_size))
    # 压缩后文件大小
    compressed_file_path = "./压缩文件/" + str(i + 1) + ".dpc"
    compressed_file_size = os.path.getsize(compressed_file_path)
    print("\t" + "压缩后字节大小：" + str(os.path.getsize(compressed_file_path)))
    # 压缩比
    compression_ratio = original_file_size / compressed_file_size
    print("\t" + "压缩比为：" + str(compression_ratio))

