import wx
import matplotlib
import numpy as np
import xlrd
import re

matplotlib.use("WXAgg")

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter

import pylab
from matplotlib import pyplot as plt

class Solution():
    thredhold = 5
    li = []

    def lcs(self, a, b):
        lena = len(a)
        lenb = len(b)
        c = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
        flag = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
        for i in range(lena):
            for j in range(lenb):
                if abs(a[i] - b[j]) < self.thredhold:
                    c[i + 1][j + 1] = c[i][j] + 1
                    flag[i + 1][j + 1] = 'ok'
                elif c[i + 1][j] > c[i][j + 1]:
                    c[i + 1][j + 1] = c[i + 1][j]
                    flag[i + 1][j + 1] = 'left'
                else:
                    c[i + 1][j + 1] = c[i][j + 1]
                    flag[i + 1][j + 1] = 'up'
        return c, flag

    def printLcs(self, flag, a, i, j):
        if i == 0 or j == 0:
            return
        if flag[i][j] == 'ok':
            self.printLcs(flag, a, i - 1, j - 1)
            # print a[i - 1]
            self.li.append(a[i - 1])
        elif flag[i][j] == 'left':
            self.printLcs(flag, a, i, j - 1)
        else:
            self.printLcs(flag, a, i - 1, j)



    def DTW_puls(self, data1, data2):
        x = np.array(data1, dtype=float)
        y = np.array(data2, dtype=float)

        m = x.size
        n = y.size

        # plt.plot(x)
        # plt.plot(y)
        # plt.show()

        # euclidean distance matrix
        d = np.zeros((m, n), dtype=int)
        # DTW distance matrix
        D = np.zeros((m, n), dtype=int)

        # calculate values in matrix d including table head
        for i in range(m):
            for j in range(n):
                d[i, j] = abs(x[i] - y[j])


        # calculate values in matrix D including table head
        D[0, 0] = d[0, 0]
        for i in range(1, m):
            D[i, 0] = D[i - 1, 0] + d[i, 0]
        for j in range(1, n):
            D[0, j] = D[0, j - 1] + d[0, j]
        for i in range(1, m):
            for j in range(1, n):
                D[i, j] = self.getMin(D[i, j - 1], D[i - 1, j], D[i - 1, j - 1]) + d[i, j]

        # print('Matrix D: \n', D)
        # print('DTW distance: \n', D[m - 1, n - 1])
        return D[m-1, n-1]

    def getMin(self, a, b, c):
        v = a
        if b < v:
            v = b
        if c < v:
            v = c
        return v

    def pr(self):
        print("ok")

    def Head(self, A):
        return A[0]

    def Rest(self, A):
        B = A.copy()
        B.pop(0)
        return B

    def d(self, a, b):
        return abs(a - b)

    def max_1(self, a, b):
        if (a > b):
            return a
        else:
            return b

    def Lcss(self, A, B):
        if (len(A) == 0 or len(B) == 0):
            return 0
        elif (d(Head(A), Head(B)) <= 1 and abs(len(A) - len(B)) < 2):
            return 1 + Lcss(Rest(A), Rest(B))
        else:
            return max_1(Lcss(Rest(A), B), Lcss(A, Rest(B)))

    def min_1(self, a, b, c):
        if (a > b):
            if (b >= c):
                return c
            else:
                return b
        else:
            if (a >= c):
                return c
            else:
                return a

    def DTW(self, A, B):
        if (len(A) == 0 and len(B) == 0):
            return 0
        elif (len(A) == 0 or len(B) == 0):
            return 99999
        else:
            return (self.d(self.Head(A), self.Head(B)) + self.min_1(self.DTW(A, self.Rest(B)), self.DTW(self.Rest(A), B), self.DTW(self.Rest(A), self.Rest(B))))

    def min_2(self, a, b, c, d):
        if (a > b):
            if (b > c):
                if (c > d):
                    return d
                else:
                    return c
            else:
                if (b > d):
                    return d
                else:
                    return b
        else:
            if (a > c):
                if (c > d):
                    return d
                else:
                    return c
            else:
                if (a > d):
                    return d
                else:
                    return a

    def EDR(self, A, B):

        if (d(Head(A), Head(B)) <= 1):
            subcost = 0
        else:
            subcost = 1

        if (len(A) == 0):
            return len(B)
        elif (len(B) == 0):
            return len(A)
        else:
            a1 = EDR(Rest(A), Rest(B)) + subcost
            a2 = EDR(Rest(A), B) + 1
            a3 = EDR(A, Rest(B)) + 1
            return min_1(a1, a2, a3)

class ButtonFrame(wx.Frame,object):

    def __init__(self, object):
        wx.Frame.__init__(self, None, -1, 'Button Example', size=(700, 560))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('gray')

        #set bcakground

        image_file = 'image.jpg'
        to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(panel, -1, to_bmp_image, (0, 0))
        image_width = to_bmp_image.GetWidth()
        image_height = to_bmp_image.GetHeight()
        set_title = '%s %d x %d' % (image_file, to_bmp_image.GetWidth(), to_bmp_image.GetHeight())
        self.SetTitle(set_title)

        #set button
        self.introduce = wx.Button(panel, -1, "introduce", pos=(350, 180))
        self.input_data = wx.Button(panel, -1, "input_data", pos=(450, 180))
        self.start = wx.Button(panel, -1, "start", pos=(550, 180))
        self.introduce.SetBackgroundColour('#DDDEE0')
        #set choice
        self.scores = ['DTW', 'LCSS', '3', '4', '5']
        self.choice_1 = wx.Choice(panel, -1, choices=self.scores, pos=(352, 130), size=(80, 30))

        #set label
        self.input_filename = wx.TextCtrl(panel, -1, pos=(520, 135), size=(120, 19))

        self.information = wx.StaticText(panel, -1, '输入文件名:', pos=(435, 135), size=(80, 10), style=wx.ALIGN_CENTER)
        self.information = wx.StaticText(panel, -1, '信息栏', pos=(120, 130), size=(100, 20), style=wx.ALIGN_CENTER)
        self.information.SetForegroundColour('black')
        self.information.SetBackgroundColour('#DDDEE0')
        font_information = wx.Font(22, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.information.SetFont(font_information)

        self.information_1 = wx.TextCtrl(panel, -1, "\n1. 请选择想使用的匹配算法!!!\n\n2. 通过点击introduce了解相应算法!!!\n\n3. 写入输入数据的文件!!!\n\n4. 成功写入数据后,点击start开始匹配!!!", pos=(50, 180), size=(250, 300), style=wx.TE_READONLY)
        self.information_1.SetBackgroundColour("#DDDEE0")
        self.information_1.SetForegroundColour('black')

        self.title = wx.StaticText(panel, -1, '时序数据相似性匹配', pos=(220, 30), size=(100, 50), style=wx.ALIGN_CENTER)
        font_title = wx.Font(28, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.title.SetFont(font_title)
        self.title.SetForegroundColour('')

        #set Bind_function
        self.Bind(wx.EVT_BUTTON, self.OnClick_introduce, self.introduce)
        self.Bind(wx.EVT_BUTTON, self.OnClick_input, self.input_data)
        self.Bind(wx.EVT_BUTTON, self.OnClick_start, self.start)
        # self.introduce.SetDefault()
        # self.input_data.SetDefault()

        #set and buffer of data
        self.li = []
        self.thredhold1 = 0.5

        self.figure_num = 1
        self.text_DTW = '\n    动态时间规整DTW是一个典型的优化\n\n问题,它用满足一定条件的的时间规整函数W(n)\n\n描述测试模板和参考模板的时间对应关系，\n\n求解DTW通过把时间序列进行延伸和缩短，\n\n来计算两个时间序列性之间的相似性。'
        self.text_LCSS = 'this is LCSS'
        self.filename = 'data.txt'
        self.dataset_array = []
        labelMat = []
        file = xlrd.open_workbook('data.xlsx')
        table = file.sheets()[0]
        ncols = table.ncols
        nrows = table.nrows
        for cols in range(ncols):
            self.dataset_array.append(table.col_values(cols))
        for item in self.dataset_array:
            print(item)

        # fr = open(self.filename)
        # key = 0
        # for line in fr.readlines():
        #     lineArr = line.strip().split()
        #     data_num = len(lineArr)-1
        #
        #
        #     if(key==0):
        #         for i in range(data_num):
        #             self.dataset_array.append([])
        #         key = 1
        #     print('data_array:', self.dataset_array)
        #     n = 0
        #     for item in range((data_num+1)):
        #
        #         self.dataset_array[n].append(float(lineArr[n]))
        #         print('lineArrp[n]', n, lineArr[n])
        #         n = n+1
            # dataMat.append(
            #     [1.0, float(lineArr[0]), float(lineArr[1])])  # 前面的1，表示方程的常量。比如两个特征X1,X2，共需要三个参数，W1+W2*X1+W3*X2
            # labelMat.append(int(lineArr[2]))




        #set algrithm
        self.solution = object


    #判断chice的方法
    def get_choice_str(self):
        return self.choice_1.GetStringSelection()


    def OnClick_introduce(self, event):
        self.information_1.Remove(0, 200)
        if ("DTW" == self.choice_1.GetStringSelection()):
            self.information_1.WriteText(self.text_DTW)
        if ("LCSS" == self.choice_1.GetStringSelection()):
            self.information_1.WriteText(self.text_LCSS)
        # self.introduce.SetLabel("ok")
        # plt.figure(3)
        # plt.scatter([1, 2, 3], [1, 2, 3], s=10, alpha=0.5)
        # plt.scatter([2, 3, 4], [2, 3, 4], s=10, alpha=0.5)
        # plt.legend(labels=['perch', 'salmon'])
        # plt.xlabel('length')
        # plt.ylabel('color')
        # plt.show()

    def OnClick_input(self, event):
        try:
            input_filename = self.input_filename.GetValue()
            if(bool(re.match('.*txt',input_filename))):
                fr = open(input_filename)
                self.aimdata = []
                for line in fr.readlines():
                    lineArr = line.strip().split()
                    self.aimdata.append(float(lineArr[0]))

                self.information_1.Remove(0, 200)
                self.information_1.WriteText("\n数据读入成功!!!\n\n请点击匹配按钮进行匹配工作！！！")
                print('aimdata :', self.aimdata)
                # str1 = [0, 1, 2, 3]
                # str2 = [1, 2, 3]
                # data = self.solution.DTW(str1, str2)
                # self.information.SetLabelText(self.text)
                # aa = self.choice_1.GetStringSelection()
                # self.information_1.WriteText(str(data)+'\n')
            if (bool(re.match('.*xlsx', input_filename))):
                file = xlrd.open_workbook(input_filename)
                self.aimdata = file.sheets()[0].col_values(0)
                self.information_1.Remove(0, 200)
                self.information_1.WriteText("\n数据读入成功!!!\n\n请点击匹配按钮进行匹配工作！！！")
                print(self.aimdata)
        except FileNotFoundError:
            self.information_1.Remove(0, 200)
            self.information_1.WriteText("\n输入的数据文件不存在!!!\n\n请确认文件的正确性！！！")



    def OnClick_start(self, event):
        plt.figure(self.figure_num)
        self.figure_num = self.figure_num+1
        aim = self.aimdata

        ##判断那种方法
        choice_str = self.get_choice_str()
        if(choice_str=='DTW'):
            e_value = solution.DTW_puls(aim, self.dataset_array[0])
            whichone = 0
            for item in self.dataset_array:
                whichone = whichone + 1
                print(whichone)
                key = self.solution.DTW_puls(item, aim)
                print("the key is :", key)
                if(key <= e_value):
                    print('the e_value is :', key)
                    e_value = key
                    e_str = item
                    num_w = whichone

            plt.plot(e_str, color='red', label='e_str', alpha=0.7, linestyle='-.')
            plt.legend('Curve_found')
            plt.plot(aim, color='blue', label='input_str', alpha=0.7, linestyle='--')
            plt.legend('Curves_matched')
            plt.xlabel('time')
            plt.ylabel('value')
            plt.show()
            #修改信息栏
            self.information_1.Remove(0, 200)
            text = "\nDTW算法匹配结束！！！\n\n被匹配的是第"+str(num_w)+'条曲线，结果已经画出!!!\n\n红色为匹配到的曲线,蓝色为输入的曲线!!!\n\n两者之间的距离为'+str(e_value)+'\n\n匹配到的曲线已经写入result.txt文件!!!'
            self.information_1.WriteText(text)
            #写入result文件
            result = np.array(e_str)
            result = result.transpose()
            np.savetxt('result.txt', result, fmt='%0.f')

        if(choice_str=='LCSS'):
            e_value = 0
            whichone = 0
            for item in self.dataset_array:
                whichone = whichone + 1
                print(whichone)
                c,flag = solution.lcs(item, aim)
                solution.li = []
                solution.printLcs(flag, item, len(item), len(aim))
                key = len(solution.li)
                print("the key is :", key)
                if (key > e_value):
                    print('the e_value is :', key)
                    e_value = key
                    e_str = item
                    num_w = whichone
            print('final evalue:',e_value)
            plt.plot(e_str, color='red', label='e_str', alpha=0.7, linestyle='-.')
            plt.legend('Curve_found')
            plt.plot(aim, color='blue', label='input_str', alpha=0.7, linestyle='--')
            plt.legend('Curves_matched')
            plt.xlabel('time')
            plt.ylabel('value')
            plt.show()
            # 修改信息栏
            self.information_1.Remove(0, 200)
            text = "\nLCSS算法匹配结束！！！\n\n被匹配的是第" + str(num_w) + '条曲线，结果已经画出!!!\n\n红色为匹配到的曲线,蓝色为输入的曲线!!!\n\n两者之间的距离为' + str(e_value) + '\n\n匹配到的曲线已经写入result.txt文件!!!'
            self.information_1.WriteText(text)
            # 写入result文件
            result = np.array(e_str)
            result = result.transpose()
            np.savetxt('result.txt', result, fmt='%0.f')
            # print("LCSS result")
            # c, flag = solution.lcs([1, 2, 3], [1, 2.5, 3.1])
            # solution.printLcs(flag, [1, 2, 3], len([1, 2, 3]), len([1, 2.5, 3.1]))
            # print(solution.li)
            # plt.legend(labels=['perch', 'salmon'])
            # plt.plot(self.aimdata)
            # plt.xlabel('time')
            # plt.ylabel('value')
            # plt.show()
        self.aimdata = []






if __name__ == '__main__':
    app = wx.PySimpleApp()
    solution = Solution()
    frame = ButtonFrame(solution)
    frame.Show()
    app.MainLoop()
