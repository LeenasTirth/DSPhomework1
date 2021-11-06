class get_new_lists:
    def __init__(self, energy_list, aver_amplitude_list, pass_zero_list, scale_pass_zero=3,
                 scale_energy_threshold=2) -> None:
        self.scale_pass_zero = scale_pass_zero
        self.scale_energy_threshold = scale_energy_threshold
        self.energy_list = energy_list
        self.aver_amplitude_list = aver_amplitude_list
        self.pass_zero_list = pass_zero_list
        self.calculate_thresh()
        self.N3, self.N4 = self.get_n3_n4(energy_list)
        self.N2, self.N5 = self.get_n2_n5(energy_list, self.N3, self.N4)
        self.N1, self.N6 = self.get_n1_n6(pass_zero_list, self.N2, self.N5)

    def get_lists(self):
        return self.energy_list[self.N1:self.N6 + 1], self.aver_amplitude_list[
                                                      self.N1:self.N6 + 1], self.pass_zero_list[self.N1:self.N6 + 1]

    def calculate_thresh(self):
        tmplist = self.energy_list.copy()
        for i in range(len(tmplist) - 1):
            for i in range(len(tmplist) - 1):
                if tmplist[i] > tmplist[i + 1]:
                    tmp = tmplist[i + 1]
                    tmplist[i + 1] = tmplist[i]
                    tmplist[i] = tmp
        sum = 0
        for i in self.pass_zero_list:
            sum += i
        self.t_pass_zero = sum / len(self.pass_zero_list) / self.scale_pass_zero
        self.t_energy_high = tmplist[int(len(tmplist) / 2)] * 1.0  # 返回排序后的中位数
        self.t_energy_low = self.t_energy_high / self.scale_energy_threshold

    def get_n3_n4(self, energy_list):
        n3 = 0
        for i in range(len(energy_list)):
            if energy_list[i] >= self.t_energy_high:
                n3 = i
                # print(n3,energy_list[n3])
                break
        n4 = len(energy_list) - 1
        for i in range(len(energy_list) - 1, -1, -1):
            if energy_list[i] >= self.t_energy_high:
                n4 = i
                # print(n4,energy_list[n4])
                break
        return (n3, n4)

    def get_n2_n5(self, energy_list, n3, n4):
        i = n3
        n2 = n3
        while (i >= 0):
            if energy_list[i] <= self.t_energy_low:
                n2 = i
                break
            else:
                i -= 1
        i = n4
        n5 = n4
        while (i <= len(energy_list) - 1):
            if energy_list[i] <= self.t_energy_low:
                n5 = i
                break
            else:
                i += 1
        return (n2, n5)

    def get_n1_n6(self, pass_zero_list, n2, n5):
        i = n2
        n1 = 0
        while (i >= 0):
            if pass_zero_list[i] <= self.t_pass_zero:
                n1 = i
                break
            else:
                i -= 1
        i = n5
        n6 = len(self.pass_zero_list) - 1
        while (i < len(pass_zero_list)):
            if pass_zero_list[i] <= self.t_pass_zero:
                n6 = i
                break
            else:
                i += 1
        return (n1, n6)

    def get_N1_N6(self):
        return (self.N1, self.N6)


if __name__ == "__main__":
    energy = [0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4,
              5, 6, 6, 6, 8, 5, 4, 3, 2, 2, 1, 1, 1, 0, 0, 0]
    aver_amplitude_list = [0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4,
                           5, 6, 6, 6, 8, 5, 4, 3, 2, 2, 1, 1, 1, 0, 0, 0]
    pass_zero = [0, 1, 2, 2, 2, 1, 3, 4, 5, 8, 5, 4, 8,
                 9, 7, 6, 5, 4, 4, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0]
    # 上述为示例列表
    a = get_new_lists(energy, aver_amplitude_list, pass_zero, 3, 2)
    # 实例化对象，其中的3和2是可选参数，3就是过零率阈值的缩放值scale_pass_zero，也就是该阈值等于过零率的均值除以3
    # 2 同理,是scale_energy，计算时，较高的能量的阈值t_energy_high为其能量均值，较低的那个阈值是较高的那个阈值除以scale_energy，也就是此处的二。
    # 如果切分效果不好，可以尝试调节这个参数
    new_energy,  new_aver_amplitude_list,new_pass_zero = a.get_lists()  # 此处即为所需的切分后的能量序列以及过零率序列
    N1, N6 = a.get_N1_N6()  # 此处返回切分处在原序列的索引，可能会用到
    print(new_energy)
    print(new_pass_zero)
    print(new_aver_amplitude_list)
    print(a.t_energy_high, a.t_energy_low, a.t_pass_zero, N1, N6)
