# -*- coding: utf-8 -*-

import numpy as np
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
        :return:返回一个分帧加窗后的列表，是一个二维列表，每一个元素是一个列表，是一帧。
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


if __name__ == '__main__':
    w = Frame_Window()
    seq = np.ones((1000,))
    s = w.devide_frame(seq, frame_long=200, method=2)
    energy_list, magnitude_list, zerorate_list = w.TimeAnalyze(s)
    print(energy_list)
    print(magnitude_list)
    print(zerorate_list)
