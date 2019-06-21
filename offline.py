from offline_ui import MainUi
import PyHook3
import pythoncom
from PyQt5 import QtWidgets
import sys
import cv2
import numpy as np
from PIL import ImageGrab
import win32gui
import threading
import time
import scipy.io as so

"""
    样本：【D_前， D_后，D_1_前，D_1_后，上端，下端】
    输出_1：【无操作，上按住，上松开，下按住，下松开】
    输出_2：【无操作，上，下】    
    sample：时序采样样本
    sample_key_1：输出_1的按键采样样本
    sample_key_2：输出_2的按键采样样本
    
"""
learn_flag = False


class Offline(MainUi):
    def __init__(self):
        super().__init__()
        self.learn_flag = False
        self.key_down = False
        self.time_sample_delete = 2

        self.sample = np.array([0, 0, 0, 0, 0, 0])
        self.input_1 = np.array([0, 0, 0, 0, 0])
        self.input_2 = np.array([0, 0, 0])
        self.sample_key_1 = np.array([0, 0, 0, 0, 0, 0])
        self.key_input_1 = np.array([0, 0, 0, 0, 0])
        self.sample_key_2 = np.array([0, 0, 0, 0, 0, 0])
        self.key_input_2 = np.array([0, 0, 0])

        self.data = {}

    def status_learn(self):

        def learn_tread():
            rect = self.get_rect()
            input_1 = [1, 0, 0, 0, 0]
            input_2 = [1, 0, 0]

            thread_key = threading.Thread(target=learn_keyboard)
            thread_key.setDaemon(True)
            thread_key.start()

            while self.learn_flag:
                time.sleep(np.random.random())
                try:
                    sample_temp = self.get_sample(rect)
                    self.push_sample(sample_temp, input_1, input_2)
                except IndexError as e:
                    print(e)
                    if self.sample[0, 0] == 0 and self.sample.shape[0] > self.time_sample_delete \
                            and self.sample_key_2.shape[0] > 1:

                        self.save_sample(self.sample[1: -self.time_sample_delete, :],
                                         self.input_1[1:-self.time_sample_delete, :],
                                         self.input_2[1:-self.time_sample_delete, :],
                                         self.sample_key_1[1:-1, :], self.key_input_1[1:-1, :],
                                         self.sample_key_2[1:-1, :], self.key_input_2[1:-1, :]
                                         )
                    elif self.sample[0, 0] != 0 and self.sample.shape[0] > self.time_sample_delete \
                            and self.sample_key_2.shape[0] > 1:

                        self.save_sample(self.sample[0: -self.time_sample_delete, :],
                                         self.input_1[0:-self.time_sample_delete, :],
                                         self.input_2[0:-self.time_sample_delete, :],
                                         self.sample_key_1[0:-1, :], self.key_input_1[0:-1, :],
                                         self.sample_key_2[0:-1, :], self.key_input_2[0:-1, :]
                                         )
                    else:
                        break

                    self.right_button_1.setText("开始学习")
                    self.learn_flag = False

        def learn_keyboard():
            # 监听键盘操作事件
            hook_manager = PyHook3.HookManager()
            hook_manager.KeyDown = self.key_down_sample
            hook_manager.KeyUp = self.key_up_sample
            hook_manager.HookKeyboard()
            pythoncom.PumpMessages()

        try:
            self.data = so.loadmat("Data.mat")
        except TypeError:
            self.data = {'sample': np.array([0, 0, 0, 0, 0, 0]),
                         'input_1': np.array([0, 0, 0, 0, 0]),
                         'input_2': np.array([0, 0, 0]),
                         'sample_key_1': np.array([0, 0, 0, 0, 0, 0]),
                         'key_input_1': np.array([0, 0, 0, 0, 0]),
                         'sample_key_2': np.array([0, 0, 0, 0, 0, 0]),
                         'key_input_2': np.array([0, 0, 0])
                         }
        finally:
            self.sample = self.data['sample']
            self.input_1 = self.data['input_1']
            self.input_2 = self.data['input_2']
            self.sample_key_1 = self.data['sample_key_1']
            self.key_input_1 = self.data['key_input_1']
            self.sample_key_2 = self.data['sample_key_2']
            self.key_input_2 = self.data['key_input_2']

        if not self.learn_flag:
            self.right_button_1.setText("停止学习")
            self.learn_flag = True

            thread_time = threading.Thread(target=learn_tread)

            thread_time.setDaemon(True)
            thread_time.start()

        else:
            self.right_button_1.setText("开始学习")
            self.learn_flag = False

    def train(self):
        self.picture()

    def game(self):
        def video_thread():
            rect = self.get_rect()
            while True:
                img = self.get_img(rect)
                try:
                    stats, _, __ = self.get_stats(img)
                except IndexError as e:
                    print(e)
                    break
                for rect in range(stats.shape[0]):
                    x, y, w, h, a = stats[rect, :]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 225, 0), 1)
                    cv2.imshow("", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        link = threading.Thread(target=video_thread)
        link.setDaemon(True)
        link.start()

    def get_sample(self, rect):
        img = self.get_img(rect)
        infinity = rect[2] - rect[0]

        stats, dino, barrier = self.get_stats(img)
        if barrier.shape[0] == 0:
            sample_temp = [infinity, infinity, infinity, infinity, infinity, infinity]
        elif barrier.shape[0] == 1:
            sample_temp = [(barrier[0, 0] - dino[0] + dino[2])/dino[0],
                           (barrier[0, 0] + barrier[0, 2] - dino[0])/dino[0],
                           infinity,
                           infinity,
                           (barrier[0, 1])/dino[0],
                           (barrier[0, 1] + barrier[0, 3])/dino[0]]
        else:
            sample_temp = [(barrier[0, 0] - dino[0] + dino[2])/dino[0],
                           (barrier[0, 0] + barrier[0, 2] - dino[0])/dino[0],
                           (barrier[1, 0] - dino[0] + dino[2])/dino[0],
                           (barrier[1, 0] + barrier[1, 2] - dino[0])/dino[0],
                           (barrier[0, 1])/dino[0],
                           (barrier[0, 1] + barrier[0, 3])/dino[0]]

        return sample_temp

    def push_sample(self, sample, input_1, input_2):
        self.sample = np.row_stack((self.sample, sample))
        self.input_1 = np.row_stack((self.input_1, input_1))
        self.input_2 = np.row_stack((self.input_2, input_2))

    def push_sample_key(self, sample_key, key_input_1, key_input_2):
        if key_input_2.size == 0:
            self.sample_key_1 = np.row_stack((self.sample_key_1, sample_key))
            self.key_input_1 = np.row_stack((self.key_input_1, key_input_1))
        else:
            self.sample_key_2 = np.row_stack((self.sample_key_2, sample_key))
            self.key_input_1 = np.row_stack((self.key_input_1, key_input_1))
            self.key_input_2 = np.row_stack((self.key_input_2, key_input_2))

    def save_sample(self, sample, input_1, input_2, sample_key_1, key_input_1, sample_key_2, key_input_2):
        self.data['sample'] = sample
        self.data['input_1'] = input_1
        self.data['input_2'] = input_2
        self.data['sample_key_1'] = sample_key_1
        self.data['key_input_1'] = key_input_1
        self.data['sample_key_2'] = sample_key_2
        self.data['key_input_2'] = key_input_2
        so.savemat("Data.mat", self.data)

    def key_down_sample(self, event):
        if self.learn_flag and not self.key_down and event.Key == "Down":
            rect = self.get_rect()
            self.key_down = True
            try:
                sample_key = self.get_sample(rect)
            except IndexError:
                return True
            key_input_1 = np.array([0, 0, 0, 1, 0])
            key_input_2 = np.array([0, 0, 1])
            self.push_sample_key(sample_key, key_input_1, key_input_2)
        elif self.learn_flag and not self.key_down and event.Key == "Up":
            rect = self.get_rect()
            self.key_down = True
            try:
                sample_key = self.get_sample(rect)
            except IndexError:
                return True
            key_input_1 = np.array([0, 1, 0, 0, 0])
            key_input_2 = np.array([0, 1, 0])
            self.push_sample_key(sample_key, key_input_1, key_input_2)
        else:
            pass
        return True

    def key_up_sample(self, event):
        if self.learn_flag and event.Key == "Down":
            rect = self.get_rect()
            self.key_down = False
            try:
                sample_key = self.get_sample(rect)
            except IndexError:
                return True
            key_input_1 = np.array([0, 0, 0, 0, 1])
            self.push_sample_key(sample_key, key_input_1, np.array([]))
        elif self.learn_flag and event.Key == "Up":
            rect = self.get_rect()
            self.key_down = False
            try:
                sample_key = self.get_sample(rect)
            except IndexError:
                return True
            key_input_1 = np.array([0, 0, 1, 0, 0])
            self.push_sample_key(sample_key, key_input_1,  np.array([]))
        else:
            pass
        return True

    def get_img(self, rect):
        pic = ImageGrab.grab(rect)
        img = cv2.cvtColor(np.asarray(pic), cv2.COLOR_RGB2GRAY)
        return img

    def get_stats(self, img):

        # 背景色与龙色的映射函数
        f = lambda x: 168.3-0.32 * x
        background = img[0, 0]
        dino = f(background)
        if dino < 127:
            circles_state, img_ = cv2.threshold(img, dino, 225, 1)
        else:
            circles_state, img_ = cv2.threshold(img, dino, 225, 0)

        _, labels, stats, centroids = cv2.connectedComponentsWithStats(img_, 8, cv2.CV_32S)
        sort = centroids[:, 0].argsort()
        stats = stats[sort]
        centroids = centroids[sort]

        # 筛选龙和障碍物
        centroids = centroids[stats[:, 4] > 100]
        stats = stats[stats[:, 4] > 100]
        centroids = centroids[stats[:, 4] < 10000]
        stats = stats[stats[:, 4] < 10000]
        ratio = stats[:, 2] / stats[:, 3]

        # 分离龙和障碍物
        bool_dino = []
        bool_barriers = []
        for i in range(len(ratio)):
            bool_dino.append(1 > ratio[i] > 0.85 or ratio[i] > 2)
            bool_barriers.append(ratio[i] < 0.85 or 1 < ratio[i] < 2)

        dino = stats[bool_dino][0]
        barrier = stats[bool_barriers]
        centroid = centroids[bool_barriers][:, 0]

        # 剔除已经通过的障碍物
        bool_barrier = np.where(barrier[:, 0]+barrier[:, 2] < dino[0], False, True)
        barrier = barrier[bool_barrier]
        centroid = centroid[bool_barrier]

        centroid_diff = np.diff(centroid)
        for i in range(len(centroid_diff)):
            if centroid_diff[i] < dino[2]:
                x = min(barrier[i][0], barrier[i + 1][0])
                y = min(barrier[i][1], barrier[i + 1][1])
                w = barrier[i + 1][0] - barrier[i][0] + barrier[i + 1][2]
                h = barrier[i][1] + barrier[i][3] - y
                a = barrier[i][4] + barrier[i + 1][4]
                new_box = np.array([x, y, w, h, a])
                barrier[i][4] = 0
                barrier[i + 1, :] = new_box

        barrier = barrier[barrier[:, 4] != 0]
        stats = np.row_stack((dino, barrier))

        return stats, dino, barrier

    def video(self, flag):
        """

        :param flag:0： 播放视频，1： 录制视频
        :return:
        """

        if flag == 0:
            def video_thread():
                i = 0
                while True:
                    img = self.get_img()
                    cv2.imwrite("./resource/img_" + str(i) + ".bmp", img)
                    i = i + 1
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            link = threading.Thread(target=video_thread)
            link.setDaemon(True)
            link.start()
        else:

            i = 0
            while True:
                time.sleep(0.08)
                img = cv2.imread("./resource/video/img_" + str(i) + ".bmp", cv2.CV_8U)
                try:
                    stats, _, __ = self.get_stats(img)
                except IndexError as e:
                    print(e)
                    break
                if stats.shape[1]:
                    for rect in range(stats.shape[0]):
                        x, y, w, h, a = stats[rect, :]
                        cv2.rectangle(img, (x, y), (x + w, y + h), 83, 1)
                cv2.imshow("", img)
                i = i + 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def picture(self):
        img = cv2.imread("./resource/video/img_" + str(1) + ".bmp", cv2.CV_8U)
        try:
            stats, _, __ = self.get_stats(img)
        except IndexError as e:
            print(e)
            return
        if stats.shape[1]:
            for rect in range(stats.shape[0]):
                x, y, w, h, a = stats[rect, :]
                cv2.rectangle(img, (x, y), (x + w, y + h), 83, 1)
        cv2.imshow("", img)
        cv2.waitKey()

    def get_rect(self):
        hwnd = win32gui.FindWindow(None, "offline-dino")
        rect = win32gui.GetWindowRect(hwnd)
        rect = [rect[0] + 10, rect[1] + 40, rect[2] - 130, rect[3] - 10]

        return rect


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = Offline()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
