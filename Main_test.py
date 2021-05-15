import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import load_trial as recog
import 와챠검색 as sear
import database as db

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
UIform = uic.loadUiType("test_GUI.ui")[0]
UIform2 = uic.loadUiType("test_GUI2.ui")[0]

class MainWindow(QWidget, UIform) :   # (모듈 , ui파일 >> ui파일은 같은 폴더 내에 있을 것)
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

# ------
        self.decord_button.clicked.connect(self.button1Function)

#--------

    def button1Function(self) :

        if self.Put_image.toPlainText() == "" :
            QMessageBox.about(self, "error", "이미지를 입력해주세요")

        else :
            print("변경 중..")
            path = (self.Put_image.toPlainText())
            print("파일 경로 : " + path[8 : len(path)])
            recog.save_desce()
            recog.main_recog(path[8 : len(path)])  # << ( )여기에 이미지를 입력

            Window2.show()



class ChoiceWindow(QWidget, UIform2):  # (모듈 , ui파일 >> ui파일은 같은 폴더 내에 있을 것)
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.nathing.clicked.connect(self.button2Function)




    def button2Function(self):

        for i in db.cator_list :
            self.btnList.append(QPushButton(str( i + 1 ) + '.' + db.cator_list[i] , self))
            self.btnList[i].resize(80, 25)
            self.btnList[i].move(10, self.btnTop + (i * 25))


        # db.cator_list <!< 이미지에 있는 사람들의 이름들 >!> 리스트로
        for index, name in enumerate(db.cator_list): print("[ {0} : {1} ]".format(index + 1, name), end='')
        num = int(input("\n 누구를 검색하시겠습니까? : "))
        sear.main_search(db.cator_list[num - 1])


app = QApplication(sys.argv) #QApplication : 프로그램을 실행시켜주는 클래스
Window1 = MainWindow() #MainWindow의 인스턴스 생성(객체 생성)
Window2 = ChoiceWindow() #
Window1.show()  #프로그램 화면을 보여주는 코드
sys.exit(app.exec_()) # 프로그램 종료 (이벤트 정보 ??)  프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드