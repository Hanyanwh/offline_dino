from PyQt5 import QtGui, QtCore, QtWidgets, Qt
import sys
import qtawesome


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化折叠参数
        self.getFold = False
        self.setWindowTitle("offline-dino")
        self.__init_ui()

    def __init_ui(self):
        self.setFixedSize(960, 270)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网络布局层
        self.main_widget.setLayout(self.main_layout)  # 将布局设置为网格布局

        self.top_widget = QtWidgets.QWidget()
        self.top_widget.setObjectName("top_widget")

        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName("right_widget")

        self.left_widget = QtWidgets.QWidget()
        self.left_widget.setObjectName("left_widget")

        # 顶部布局设计
        self.top_little = QtWidgets.QLabel(self.top_widget)
        self.top_little.setText("offline-dino")
        self.top_little.setGeometry(QtCore.QRect(10, 0, 70, 30))
        self.top_mini_button = QtWidgets.QPushButton(self.top_widget)
        self.top_mini_button.setIcon(QtGui.QIcon('./resource/img/mini.png'))
        self.top_mini_button.setObjectName("top_mini")
        self.top_mini_button.setGeometry(QtCore.QRect(820, 0, 40, 30))
        self.top_mini_button.setIconSize(QtCore.QSize(30, 30))
        self.top_max_button = QtWidgets.QPushButton(self.top_widget)
        self.top_max_button.setIcon(QtGui.QIcon('./resource/img/max.png'))
        self.top_max_button.setObjectName("top_max")
        self.top_max_button.setGeometry(QtCore.QRect(860, 0, 40, 30))
        self.top_max_button.setIconSize(QtCore.QSize(30, 30))
        self.top_close_button = QtWidgets.QPushButton(self.top_widget)
        self.top_close_button.setIcon(QtGui.QIcon('./resource/img/close.png'))
        self.top_close_button.setObjectName("top_close")
        self.top_close_button.setGeometry(QtCore.QRect(900, 0, 40, 30))
        self.top_close_button.setIconSize(QtCore.QSize(40, 40))

        # 右侧布局设计
        self.logo_label = QtWidgets.QLabel(self.right_widget)
        self.logo_label.setPixmap(QtGui.QPixmap("./resource/img/logo.png"))
        self.logo_label.setScaledContents(True)

        self.right_button_1 = QtWidgets.QPushButton(self.right_widget)
        self.right_button_1.setObjectName("right_button")
        self.right_button_1.setIcon(qtawesome.icon('fa.television', color='gray'))
        self.right_button_1.setIconSize(QtCore.QSize(25, 25))
        self.right_button_1.setText("开始学习")

        self.right_button_2 = QtWidgets.QPushButton(self.right_widget)
        self.right_button_2.setObjectName("right_button")
        self.right_button_2.setIcon(qtawesome.icon('fa.clipboard', color='gray'))
        self.right_button_2.setIconSize(QtCore.QSize(25, 25))
        self.right_button_2.setText("训练模型")

        self.right_button_3 = QtWidgets.QPushButton(self.right_widget)
        self.right_button_3.setObjectName("right_button")
        self.right_button_3.setIcon(qtawesome.icon('fa.gamepad', color='gray'))
        self.right_button_3.setIconSize(QtCore.QSize(25, 25))
        self.right_button_3.setText("模型通关")

        self.logo_label.setGeometry(QtCore.QRect(20, 15, 80, 80))
        self.right_button_1.setGeometry(QtCore.QRect(0, 100, 115, 40))
        self.right_button_2.setGeometry(QtCore.QRect(0, 140, 115, 40))
        self.right_button_3.setGeometry(QtCore.QRect(0, 180, 115, 40))

        self.main_layout.addWidget(self.top_widget, 0, 0, 1, 40)
        self.main_layout.addWidget(self.left_widget, 1, 0, 9, 35)
        self.main_layout.addWidget(self.right_widget, 1, 35, 9, 5)

        self.top_widget.setStyleSheet(
            '''
             QWidget#top_widget{
                background:white;
                border-top:1px solid back;
                border-bottom:lpx solid  rgba(255, 255, 255, 40);
                border-left:1px solid  back;
                border-right:1px solid back;
            }
            QPushButton{
                border:none;
                color:white;
            }
            QPushButton#top_mini::hover{
                background: #CCCCCC;
            }
            QPushButton#top_max::hover{
                background: #CCCCCC;
            }
            QPushButton#top_close::hover{
                background: #EE3B3B;
            }
            QLabel{
                font-size: 12px;
                font-weight:50;
                font-family:'微软雅黑'
            }
            '''
        )
        self.right_widget.setStyleSheet(
            '''
            QPushButton{
                border:none;
                color:white;
                text-align: center;
                font-size:16px;
                font-weight:100;
                font-family:"楷体";
                }
            QWidget#right_widget{
                background:rgb(50, 50, 50);
                border-bottom:lpx solid  back;
                border-left:1px solid  rgba(255, 255, 255, 40);
                border-right:1px solid back;
            }
            QPushButton#right_button::hover{
                background: rgba(255, 255, 255, 40);
                border-left:2px solid #CD0000;
                font-weight:700;
            }
            '''
        )

        self.left_widget.setStyleSheet(
            '''
            QWidget#left_widget{
                border-left: 1px solid back;
                border-top: 1px solid #BFBFBF;
                border-bottom: 1px solid back;               
            }
            
            '''
        )

        # 设置窗口主部件
        self.setCentralWidget(self.main_widget)

        # 边框隐藏，透明
        self.setWindowOpacity(0.95)  # 设置窗口透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

        # 触发事件
        self.top_close_button.clicked.connect(QtCore.QCoreApplication.quit)
        self.right_button_1.clicked.connect(self.status_learn)
        self.right_button_2.clicked.connect(self.train)
        self.right_button_3.clicked.connect(self.game)

    # 鼠标拖动方法重写
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QtWidgets.QApplication.postEvent(self, Qt.QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def status_learn(self):
        pass

    def train(self):
        pass

    def game(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
