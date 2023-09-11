import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, \
    QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem,QDialog , QToolBar,QStatusBar
from PyQt6.QtGui import QAction,QIcon
import mysql.connector
import sqlite3



class DatabaseConnect:
    def __init__(self ,host="localhost" , user="root" , password="Dang.khoi1" , database="school"):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
    def connect(self):
        connection=mysql.connector.connect(host=self.host , user= self.user , password=self.password , database=self.database)
        return connection
class Mainwindow(QMainWindow):
    def __init__(self):
        """ khởi tạo class"""
        super().__init__()
        self.setWindowTitle("Student Management System")
        # set dài rông
        self.setMinimumSize(500,400)

        """khởi tạo menu"""
        file_menu_item=self.menuBar().addMenu("&file")
        help_menu_item=self.menuBar().addMenu("&Help")
        Edit_menu_item=self.menuBar().addMenu("&Edit")

        add_student_action=QAction(QIcon("icons/add.png"),"Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)


        # search
        search_action=QAction(QIcon("icons/search.png"),"Search Student",self)
        search_action.triggered.connect(self.seach)
        Edit_menu_item.addAction(search_action)


        about_action=QAction("About" ,self)
        help_menu_item.addAction(about_action)

        about_action.setMenuRole(QAction.MenuRole.NoRole)
         # set table
        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)


        # tạo thanh toolbar
        toolbar=QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create status bar and add status bar elements
        self.statusbar=QStatusBar()
        self.setStatusBar(self.statusbar)


        self.table.cellClicked.connect(self.cell_clicked)
    def cell_clicked(self):
        self.edit_button = QPushButton("Edit record")
        self.edit_button.clicked.connect(self.editINF)

        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.deleteINF)
        # tìm đối tượng và trả ra màn hình
        children=self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)



        self.statusbar.addWidget(self.edit_button)
        self.statusbar.addWidget(self.delete_button)



        """ hàm connect data đên"""
    def load_data(self):

            connection=DatabaseConnect().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students")
            result=cursor.fetchall()
            # tạo bảng cho các đối tượng

            self.table.setRowCount(0)
            for row_number ,row_data in enumerate(result):
                self.table.insertRow(row_number)
                for column_number,data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
    def seach(self):
        dialog=search_student()
        dialog.exec()
    def editINF(self):
        dialog=EditDialog()
        dialog.exec()
    def deleteINF(self):
        dialog=DeleteDialog()
        dialog.exec()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        #get student name from slected row
        index=age_calculator.table.currentRow()
        # chọn phần tử thông tin hiển thị trong bảng ra ngoài
        self.student_id=age_calculator.table.item(index,0).text()
        student_name=age_calculator.table.item(index,1).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        # chọn phần tử thông tin hiển thị trong bảng ra ngoài
        course_name=age_calculator.table.item(index,2).text()
        self.course_name = QComboBox()
        course = ["Biology", "MAth", "Astronomy", "Physics"]
        self.course_name.addItems(course)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)


        # Add mobile widget
        mobile=age_calculator.table.item(index,3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("MOBIle")
        layout.addWidget(self.mobile)
        # close window
        self.close_button = QPushButton("Close window", self)

        layout.addWidget(self.close_button)
        # add button submit

        button = QPushButton("Update")
        button.clicked.connect(self.update)
        layout.addWidget(button)
        self.setLayout(layout)

    def update(self):

        connection=DatabaseConnect().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name=? , course=%s , mobile=%s WHERE id =%s",
                       (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text() ,
                        self.student_id))


        connection.commit()
        cursor.close()
        connection.close()
        age_calculator.load_data()
        self.close()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student data")

        layout=QGridLayout()
        confirmation=QLabel("Are you sue you want to delete")
        yes=QPushButton("Yes")
        no=QPushButton("NO")
        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)
        yes.clicked.connect(self.delete_student)
        self.setLayout(layout)

    def delete_student(self):
        index = age_calculator.table.currentRow()
        student_id=age_calculator.table.item(index,0).text()
        connection = DatabaseConnect().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id=%s", (student_id,))

        connection.commit()
        cursor.close()
        connection.close()
        age_calculator.load_data()
        self.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout=QVBoxLayout()

        self.student_name=QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        self.course_name=QComboBox()
        course=["Biology" ,"MAth","Astronomy" ,"Physics"]
        self.course_name.addItems(course)
        layout.addWidget(self.course_name)



        # Add mobile widget
        self.mobile=QLineEdit()
        self.mobile.setPlaceholderText("MOBIle")
        layout.addWidget(self.mobile)

        #add button submit
        button=QPushButton("Register")
        button.clicked.connect(self.addstudent)
        layout.addWidget(button)

        self.setLayout(layout)

    def addstudent(self):
        name=self.student_name.text()
        course=self.course_name.itemText(self.course_name.currentIndex())
        mobile=self.mobile.text()
        connection=DatabaseConnect().connect()
        cursor=connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES (%s,%s,%s)",
                       (name,course,mobile))

        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        age_calculator.load_data()

class search_student(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        self.student_name=QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)



        button=QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)
    def search(self):
        name=self.student_name.text()
        connection=DatabaseConnect().connect()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name=%s",(name,))
        result=cursor.fetchall()
        rows=list(result)
        print(rows)
        # Cú pháp hiển thị dòng chứa cần tìm
        items=age_calculator.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        # hiển thị các đối tượng cần tìm
        for item in items:
            print(item)
            age_calculator.table.item(item.row(),1).setSelected(True)


        cursor.close()
        connection.close()



app=QApplication(sys.argv)
age_calculator=Mainwindow()
age_calculator.show()
age_calculator.load_data()

sys.exit((app.exec()))