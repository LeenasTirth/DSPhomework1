# -*- coding: utf-8 -*-

import numpy as np
from gate import get_new_lists


class Frame_Window:
    def __init__(self):
        pass

    def TimeAnalyze(self, frame_list):
        '''
        短时时域特性分析
        :param frame_list: 传入的是帧序列，也就是devide_frame函数得到的结果
        :return:依次返还短时能量、平均幅度和短时过零率，都是一个列表
        '''
        energy_list = []
        zerorate_list = []
        magnitude_list = []
        for f in frame_list:
            e, m, z = self.frame_energy_find(f)
            energy_list.append(e)
            zerorate_list.append(z)
            magnitude_list.append(m)
        return energy_list, magnitude_list, zerorate_list

    def sgn(self, a):
        if a < 0:
            return -1
        else:
            return 1

    def frame_energy_find(self, frame):
        energy = 0
        zerorate = 0
        M = 0
        for i in range(len(frame)):
            energy += frame[i] * frame[i]
            M += abs(frame[i])
            if i == 1:
                tmp = self.sgn(frame[i]) - self.sgn(frame[i - 1])
            else:
                tmp = 0
            zerorate += abs(tmp)
        zerorate = zerorate / 2
        return energy, M, zerorate

    def devide_frame(self, data_list, frame_long, method=2):
        '''
        分帧加窗接口
        :param data_list:传入一个一维numpy数组，是没有分帧之前的信号序列
        :param frame_long:帧的长度
        :param method:选择使用哪一种窗函数
        :return:返回一个分帧加窗后的列表，是一个二维列表，每一个元素是一个列表，是一帧。即：[[....],[....],....]
        '''
        frame_list = []
        frame_move = int(frame_long * 0.75)
        sum = len(data_list)
        start = 0
        while start < sum - frame_long:
            end = start + frame_long
            tmp = np.array(data_list[start:end])
            tmp = self.Compute(tmp, method)
            tmp = tmp.tolist()
            frame_list.append(tmp)
            start = start + frame_move

        return frame_list

    def Compute(self, seq, method=1):
        '''

        :param seq: 传入一帧
        :param method: 选择使用哪种窗函数
        :return: 返还窗函数作用后的一帧
        '''
        if method == 1:
            processed_seq = self.RectWindow(seq)
        elif method == 2:
            processed_seq = self.HanminWindow(seq)
        else:
            processed_seq = self.HailingWindow(seq)
        return processed_seq

    def RectWindow(self, seq):
        return seq

    def HanminWindow(self, seq):
        hanmin_window = np.arange(len(seq))
        # hanmin_window = np.expand_dims(hanmin_window, axis=0).repeat(seq.shape[0], axis=0)
        # print(hanmin_window)
        hanmin_window = 0.54 - 0.46 * np.cos(2 * np.pi * hanmin_window / (len(seq) - 1))
        # print(hanmin_window)
        return seq * hanmin_window

    def HailingWindow(self, seq):
        hailing_window = np.arange(len(seq))
        # hailing_window = np.expand_dims(hailing_window, axis=0).repeat(seq.shape[0], axis=0)
        hailing_window = 0.5 * (1 - np.cos(2 * np.pi * hailing_window / (len(seq) - 1)))
        return seq * hailing_window

    def GetFeature(self, energy_list, magnitude_list, zerorate_list, length=100,weight = None):
        '''

        :param energy_list: 能量序列
        :param magnitude_list: 幅度序列
        :param zerorate_list: 过零率序列
        :param length: 取序列起始的 length 个
        :param weight: 每个序列的加权系数
        :return: 3*length维度的特征
        '''
        delta = 1e-15#防止除以0
        if weight is None:
            weight=[0.3, 0.3, 0.3]
        weight = np.array(weight)
        weight = weight/(weight.sum())

        energy = np.array(energy_list)
        energy = (energy-energy.mean())/(energy.std()+delta)*weight[0]
        #energy = energy.tolist()
        magnitude = np.array(magnitude_list)
        magnitude = (magnitude-magnitude.mean())/(magnitude.std()+delta)*weight[1]
        #magnitude = magnitude.tolist()
        zerorate = np.array(zerorate_list)
        zerorate = (zerorate-zerorate.mean())/(zerorate.std()+delta)*weight[2]
        #zerorate = zerorate.tolist()
        ans = np.hstack((energy[:length],magnitude[:length],zerorate[:length])).tolist()

        return ans


if __name__ == '__main__':
    # Step1:实例化Frame_Window对象
    w = Frame_Window()
    seq = np.ones((1000,))
    # Step2:调用devide_frame，传入序列，进行分帧加窗,frame_long是帧长度，method是选择哪种窗函数
    s = w.devide_frame(seq, frame_long=200, method=2)
    # Step3:调用TimeAnalyze函数，传入Step2中返回的变量（帧的列表），返回三个列表，分别是每一帧的：能量，幅度和过零率
    energy_list, magnitude_list, zerorate_list = w.TimeAnalyze(s)
    # Step4:实例化对象，其中的3和2是可选参数，3就是过零率阈值的缩放值scale_pass_zero，也就是该阈值等于过零率的均值除以3，需要传入前面得到的三个列表
    Gate = get_new_lists(energy_list, magnitude_list, zerorate_list, 3, 2)
    # Step5:此处即为所需的切分后的能量序列以及过零率序列
    new_energy, new_aver_amplitude_list,new_pass_zero = Gate.get_lists()
    # Step6:传入三个序列列表，返回一个3*length维度的特征。length指的是从这三个列表的起始位置开始，取多少个元素作为定长特征；weight是给三个序列的加权。
    feature = w.GetFeature(new_energy, new_aver_amplitude_list,new_pass_zero,length=100,weight=[0.3,0.3,0.3])

    print(feature)
    # print(energy_list)
    # print(magnitude_list)
    # print(zerorate_list)
