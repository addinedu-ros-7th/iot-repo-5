import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import mysql.connector
import json
import socket
    

from_class = uic.loadUiType("driver.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # mysql 접속
        self.remote = mysql.connector.connect(
            host = "msdb.cvyy46quatrs.ap-northeast-2.rds.amazonaws.com",
            port = 3306,
            user = "root",
            password = "Dbsalstjq128!",
            database = "iot"
        )
        self.cur = self.remote.cursor()

        self.inputName
        self.inputPhone
        self.btnExit.clicked.connect(self.exit)

        self.btnSearch.clicked.connect(self.Search)



    def Search(self):
        name = self.inputName.text()
        phone = self.inputPhone.text()
        
        self.connect_to_server(name, phone)
        
        self.inputName.setText("")
        self.inputPhone.setText("")
        

    def exit(self):
        if self.remote.is_connected():
            self.remote.close()
            print("데이터베이스 연결종료")
            self.close()


    def Add(self, result):
        row = self.dbRecordWidget.rowCount()
        self.dbRecordWidget.insertRow(row)
        self.dbRecordWidget.setItem(row, 0, QTableWidgetItem(str(result[0])))
        self.dbRecordWidget.setItem(row, 1, QTableWidgetItem(str(result[1])))
        self.dbRecordWidget.setItem(row, 2, QTableWidgetItem(str(result[2])))
        self.dbRecordWidget.setItem(row, 3, QTableWidgetItem(str(result[3])))
        self.dbRecordWidget.setItem(row, 4, QTableWidgetItem(str(result[4])))
        self.dbRecordWidget.setItem(row, 5, QTableWidgetItem(str(result[5])))
        self.dbRecordWidget.setItem(row, 6, QTableWidgetItem(str(result[6])))
        self.dbRecordWidget.setItem(row, 7, QTableWidgetItem(str(result[7])))
        
    

    def connect_to_server(self, name, phone):
        host = '192.168.2.117'  # 서버 IP 주소
        port = 65433        # 서버 포트 번호

        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        
        message = name+','+phone
        client_socket.send(message.encode('utf-8'))

        
        response_data = client_socket.recv(1024)

        decoded_data = response_data.decode('utf-8')

        responses = json.loads(decoded_data)
        num = len(responses)
        
        for i in range(num):
            self.Add(responses[f'{i}'])

        client_socket.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())
