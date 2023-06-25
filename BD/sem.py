from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import psycopg2
import json
import re

from pymongo import MongoClient
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QCalendarWidget
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QTextBrowser
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QInputDialog, QLineEdit, QDialogButtonBox, QGridLayout
from PyQt5 import QtCore
import sys
import csv
from datetime import date


# функция для подключения к PostgreSQL
def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="1234"
        )
    except psycopg2.DatabaseError as e:
        print(f"Error while connecting to PostgreSQL: {e}")
    return conn

def connect():
    uri = "mongodb://localhost:27017"
    client = MongoClient(uri)
    return client


def get_collection(client, collection_name):
    db = client['diagnosis_db']
    collection = db['diagnosis']
    return collection


def insert_record(collection, record):
    result = collection.insert_one(record)


def find_all_records(collection):
    cursor = collection.find()
    result = ''
    for record in cursor:
        result += str(record) + '\n'
    QMessageBox.information(None, 'Query Result', result)



def delete_record(collection, query):
    result = collection.delete_one(query)



def update_record(collection, query, update):
    result = collection.update_one(query, update)



# функция для выполнения SELECT запроса
def select_from_table(conn, results):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT * FROM client.results;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

# функция для выполнения SELECT запроса
def select_from_table2(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT * FROM client.client;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

# функция для выполнения SELECT запроса
def select_from_table2_2(conn, therapist):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT * FROM therapists.therapist;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

# функция для выполнения SELECT запроса
def select_from_table2_3(conn, hospital):
    res = []
    with conn.cursor() as cur:
        query = f"select * from therapists.hospital;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

def select_from_table_tests(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT nameTest FROM client.tests;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

def select_from_table_dateC(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT Client.nameClient, Client.idContract, Contract.dateFinish FROM client.Client JOIN client.Contract ON Client.idContract = Contract.idContract;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

def select_from_table_results(conn, results):
    res = []
    with conn.cursor() as cur:
        query = f"SELECT tests.nametest, results.dateresult, results.description FROM client.tests JOIN client.results ON tests.idresults = results.idresults WHERE results.dateresult BETWEEN '2021-01-01' AND '2021-12-31';"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res


def select_from_table_hosp(conn, client):
    res = []
    with conn.cursor() as cur:
        query = f"select therapist.nametherapist, hospital.namehospital, hospital.address from therapists.therapist join therapists.hospital on therapist.hospitalId=hospital.idhospital;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

def select_from_table_price(conn, results):
    res = []
    with conn.cursor() as cur:
        query = f"select therapist.nametherapist, costs.price from therapists.therapist join therapists.costs on therapist.costId=costs.idCost where costs.price < 2000;"
        cur.execute(query)
        res = cur.fetchall()
    conn.commit()
    return res

class GroupDialog(QDialog):
    def __init__(self):
        super().__init__()

        # здесь размещаем виджеты для групповой терапии, например, таблицу записей

        self.register_button = QPushButton("Записаться", self)
        self.register_button.clicked.connect(self.insert_for_group)

        self.cancel_button = QPushButton("Отменить", self)
        self.cancel_button.clicked.connect(self.delete_for_group)

        self.reschedule_button = QPushButton("Перенести", self)
        self.reschedule_button.clicked.connect(self.update_for_group)

        hbox = QHBoxLayout()
        hbox.addWidget(self.register_button)
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.reschedule_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    # функция для выполнения INSERT запроса
    def insert_for_group(self):
        conn = create_conn()
        if conn:
            visitDate, ok1 = QInputDialog.getText(None, "Enter Data", "visitDate:", QLineEdit.Normal, "")
            nameGroup, ok2 = QInputDialog.getText(None, "Enter Data", "nameGroup:", QLineEdit.Normal, "")
            idClient, ok3 = QInputDialog.getText(None, "Enter Data", "idClient:", QLineEdit.Normal, "")
            if ok1 and ok2 and ok3:
                with conn.cursor() as cur:
                    query = f"INSERT INTO client.groupClient (visitDate, nameGroup, idClient) VALUES ('{visitDate}', '{nameGroup}', '{idClient}');"
                    cur.execute(query)
                conn.commit()
            conn.close()

    # функция для выполнения UPDATE запроса
    def update_for_group(self):
        conn = create_conn()
        if conn:
            idClient, ok1 = QInputDialog.getText(None, "Enter Data", "idClient:", QLineEdit.Normal, "")
            new_visitDate, ok2 = QInputDialog.getText(None, "Enter Data", "new visitDate:", QLineEdit.Normal, "")
            if ok1 and ok2:
                with conn.cursor() as cur:
                    query = f"UPDATE client.groupClient SET visitDate = '{new_visitDate}' WHERE idClient = '{idClient}';"
                    cur.execute(query)
                conn.commit()
            conn.close()

    # функция для выполнения DELETE запроса
    def delete_for_group(self):
        conn = create_conn()
        if conn:
            idClient, ok = QInputDialog.getText(None, "Enter Data", "idClient:", QLineEdit.Normal, "")
            if ok:
                with conn.cursor() as cur:
                    query = f"DELETE FROM client.groupClient WHERE idClient = '{idClient}';"
                    cur.execute(query)
                conn.commit()
            conn.close()


class ReviewDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оставить отзыв")
        self.setFixedSize(300, 200)

        self.review_label = QLabel("Введите отзыв:")
        self.review_text_edit = QTextEdit(self)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.add_review_to_db)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.review_label)
        vbox.addWidget(self.review_text_edit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def add_review_to_db(self):
        conn = create_conn()
        if conn:
            description = self.review_text_edit.toPlainText()
            dateReview = str(date.today())
            idClient = 5
            if description and dateReview and idClient:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO client.review (dateReview, description, idClient) VALUES (%s, %s, %s)",
                                   (dateReview, description, idClient))
                    conn.commit()
                    cursor.close()
                    QMessageBox.information(self, "Успех", "Отзыв успешно добавлен!")
                except Exception as e:
                    print(e)
                    conn.rollback()
                conn.close()

class LoginRegisterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.login_form_therapist = LoginFormTherapist()  # создаем экземпляр LoginFormTherapist
        self.login_form_client = LoginFormClient()
        self.register_form_client = RegistrationFormClient()
        self.register_form_therapist = RegistrationFormTherapist()

    def initUI(self):
        self.login_button = QtWidgets.QPushButton("Войти")
        self.register_button = QtWidgets.QPushButton("Зарегистрироваться")
        self.role_label = QtWidgets.QLabel("Выберите роль:")
        self.role_combobox = QtWidgets.QComboBox()
        self.role_combobox.addItems(["therapist", "client"])

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.role_label)
        button_layout.addWidget(self.role_combobox)
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        self.setLayout(button_layout)

        self.login_button.clicked.connect(self.show_login_form)
        self.register_button.clicked.connect(self.show_register_form)

    def show_login_form(self):
        try:
            if self.role_combobox.currentText() == "therapist":
                self.login_form_therapist.show()
                self.hide()
            elif self.role_combobox.currentText() == "client":
                self.login_form_client.show()
                self.hide()
        except Exception as e:
            print(f"Ошибка при открытии формы авторизации: {e}")

    def show_register_form(self):
        try:
            if self.role_combobox.currentText() == "therapist":
                self.register_form_therapist.show()
                self.hide()
            elif self.role_combobox.currentText() == "client":
                self.register_form_client.show()
                self.hide()
        except Exception as e:
            print(f"Ошибка при открытии формы регистрации: {e}")


class RegistrationFormClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.username_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.confirm_password_edit = QtWidgets.QLineEdit()
        self.id_edit = QtWidgets.QLineEdit()
        self.submit_button = QtWidgets.QPushButton("Зарегистрироваться", self)
        self.submit_button.clicked.connect(self.insert_reg)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Имя пользователя", self.username_edit)
        form_layout.addRow("Пароль", self.password_edit)
        form_layout.addRow("Подтверждение пароля", self.confirm_password_edit)
        form_layout.addRow("ID", self.id_edit)
        form_layout.addRow("", self.submit_button)

        self.setLayout(form_layout)

    # функция для выполнения INSERT запроса
    def insert_reg(self):
        conn = create_conn()
        if conn:
            user = self.username_edit.text()
            password = self.password_edit.text()
            confirm_password = self.confirm_password_edit.text()
            idClient = self.id_edit.text()
            if user and password and idClient:
                with conn.cursor() as cur:
                    query = f"INSERT INTO client.login (loginst, passwd, idclient) VALUES ('{user}', '{password}', '{idClient}');"
                    cur.execute(query)
                conn.commit()
            elif not (user and password and idClient):  # проверяем, чтобы все поля были заполнены
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Заполните все поля")
            elif password != confirm_password:  # проверяем совпадение паролей
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Пароли не совпадают")
            conn.close()
            self.open_client_window()
    def open_client_window(self):
        self.window = ClientWindow()
        self.window.show()
        self.close()

class LoginFormClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.username_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.submit_button = QtWidgets.QPushButton("Войти")
        self.submit_button.clicked.connect(self.check_login)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Имя пользователя", self.username_edit)
        form_layout.addRow("Пароль", self.password_edit)
        form_layout.addRow("", self.submit_button)

        self.setLayout(form_layout)

    # функция для проверки данных при авторизации
    def check_login(self):
        conn = create_conn()
        if conn:
            user = self.username_edit.text()
            password = self.password_edit.text()
            with conn.cursor() as cur:
                query = f"SELECT * FROM client.login WHERE loginst = '{user}' AND passwd = '{password}';"
                cur.execute(query)
                record = cur.fetchone()
            conn.close()
            if record:
                # выполняем действия для успешной авторизации
                print("Успешная авторизация!")
                self.open_client_window()
            else:
                # выполняем действия для неуспешной авторизации
                print("Ошибка авторизации!")
    def open_client_window(self):
        self.window = ClientWindow()
        self.window.show()
        self.close()

class RegistrationFormTherapist(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.username_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.confirm_password_edit = QtWidgets.QLineEdit()
        self.id_edit = QtWidgets.QLineEdit()
        self.submit_button = QtWidgets.QPushButton("Зарегистрироваться", self)
        self.submit_button.clicked.connect(self.insert_reg)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Имя пользователя", self.username_edit)
        form_layout.addRow("Пароль", self.password_edit)
        form_layout.addRow("Подтверждение пароля", self.confirm_password_edit)
        form_layout.addRow("ID", self.id_edit)
        form_layout.addRow("", self.submit_button)

        self.setLayout(form_layout)

    # функция для выполнения INSERT запроса
    def insert_reg(self):
        conn = create_conn()
        if conn:
            user = self.username_edit.text()
            password = self.password_edit.text()
            confirm_password = self.confirm_password_edit.text()
            idTherapist = self.id_edit.text()
            if user and password and idTherapist:
                with conn.cursor() as cur:
                    query = f"insert into therapists.login (loginst, passwd, therapistId) values ('{user}', '{password}', '{idTherapist}');"
                    cur.execute(query)
                conn.commit()
            elif not (user and password and idTherapist):  # проверяем, чтобы все поля были заполнены
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Заполните все поля")
            elif password != confirm_password:  # проверяем совпадение паролей
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Пароли не совпадают")
            conn.close()
            self.open_therapist_window()

    def open_therapist_window(self):
        self.window = TherapistWindow()
        self.window.show()
        self.close()

class LoginFormTherapist(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.username_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.submit_button = QtWidgets.QPushButton("Войти")
        self.submit_button.clicked.connect(self.check_login)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Имя пользователя", self.username_edit)
        form_layout.addRow("Пароль", self.password_edit)
        form_layout.addRow("", self.submit_button)

        self.setLayout(form_layout)
    # функция для проверки данных при авторизации
    def check_login(self):
        try:
            conn = create_conn()
            if conn:
                user = self.username_edit.text()
                password = self.password_edit.text()
                with conn.cursor() as cur:
                    query = f"SELECT * FROM therapists.login WHERE loginst = '{user}' AND passwd = '{password}';"
                    cur.execute(query)
                    record = cur.fetchone()
                conn.close()
                if record:
                    # выполняем действия для успешной авторизации
                    print("Успешная авторизация!")
                    self.open_therapist_window()  # открываем окно терапевта
                else:
                    # выполняем действия для неуспешной авторизации
                    print("Ошибка авторизации!")
        except Exception as e:
            print(f"Ошибка при проверке логина и пароля: {e}")

    def open_therapist_window(self):
        self.window = TherapistWindow()
        self.window.show()
        self.close()

class ClientWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    # def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #    painter = QPainter(self)
    #    painter.setBrush(Qt.lightGray)
    #    painter.drawRect(self.rect())

    def setupUi(self):
        # Основное окно
        self.setWindowTitle("Психологическая помощь (Клиент)")
        # self.setGeometry(300, 300, 300, 300)

        self.resize(1900, 1000)
        self.setMinimumSize(QtCore.QSize(1000, 800))
        self.setMaximumSize(QtCore.QSize(1800, 1300))

        self.chat_button = QPushButton("Оставить отзыв", self)
        self.chat_button.clicked.connect(self.show_review)
        self.chat_button.setGeometry(QtCore.QRect(1250, 20, 500, 50))

        # Календарь
        self.calendar_label = QLabel("Ближайший сеанс:", self)
        self.calendar_label.setGeometry(QtCore.QRect(1250, 75, 500, 50))
        self.calendar = QCalendarWidget(self)
        self.calendar.setGeometry(QtCore.QRect(1250, 140, 500, 500))
        self.calendar.selectionChanged.connect(self.calendar_selection_changed)
        self.calendar_selected_date_label = QLabel(self)
        self.calendar_selected_date_label.setGeometry(QtCore.QRect(1250, 650, 500, 50))

        self.back_button = QPushButton("Выход", self)
        self.back_button.clicked.connect(self.show_exit)
        self.back_button.setGeometry(QtCore.QRect(50, 20, 200, 50))

        self.group_button = QPushButton("Групповая терапия", self)
        self.group_button.setGeometry(QtCore.QRect(1250, 710, 500, 50))
        self.group_button.clicked.connect(self.show_group)
        # Психологические тесты
        self.tests_button = QPushButton("Психологические тесты", self)
        self.tests_button.setGeometry(QtCore.QRect(1250, 780, 500, 50))
        self.tests_button.clicked.connect(self.show_tests)
        # Результаты
        self.results_button = QPushButton("Результаты", self)
        self.results_button.clicked.connect(self.show_result)
        self.results_button.setGeometry(QtCore.QRect(1250, 850, 500, 50))
        # --------------------------------------------------------------------------------------------------------------
        # Для моей базы данных
        self.client_label = QLabel("Запросы для таблицы Client:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 80, 200, 50))

        update_btn2 = QPushButton('Update for Client', self)
        update_btn2.setToolTip('Execute UPDATE query')
        update_btn2.setGeometry(QtCore.QRect(50, 290, 200, 50))
        update_btn2.clicked.connect(self.update_client)

        delete_btn2 = QPushButton('Delete for Client', self)
        delete_btn2.setToolTip('Execute Delete query')
        delete_btn2.setGeometry(QtCore.QRect(50, 360, 200, 50))
        delete_btn2.clicked.connect(self.delete_client)

        self.client_label = QLabel("Запросы для таблицы Results:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 430, 200, 50))

        select_btn = QPushButton('Select for Results', self)
        select_btn.setToolTip('Execute SELECT query')
        select_btn.setGeometry(QtCore.QRect(50, 500, 200, 50))
        select_btn.clicked.connect(self.select_button_clicked)

        insert_btn = QPushButton('Insert for Results', self)
        insert_btn.setToolTip('Execute INSERT query')
        insert_btn.setGeometry(QtCore.QRect(50, 570, 200, 50))
        insert_btn.clicked.connect(self.insert_into_results)

        update_btn = QPushButton('Update for Results', self)
        update_btn.setToolTip('Execute UPDATE query')
        update_btn.setGeometry(QtCore.QRect(50, 640, 200, 50))
        update_btn.clicked.connect(self.update_results)

        delete_btn = QPushButton('Delete for Results', self)
        delete_btn.setToolTip('Execute Delete query')
        delete_btn.setGeometry(QtCore.QRect(50, 710, 200, 50))
        delete_btn.clicked.connect(self.delete_from_results)

        self.client_label = QLabel("Запросы с join:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 770, 200, 50))

        select_btn_j1 = QPushButton('Select for DateFinish', self)
        select_btn_j1.setToolTip('Execute SELECT query')
        select_btn_j1.setGeometry(QtCore.QRect(50, 840, 200, 50))
        select_btn_j1.clicked.connect(self.select_button_clickedj1)

        select_btn_j2 = QPushButton('Select for DateResult', self)
        select_btn_j2.setToolTip('Execute SELECT query')
        select_btn_j2.setGeometry(QtCore.QRect(50, 910, 200, 50))
        select_btn_j2.clicked.connect(self.select_button_clickedj2)

        # --------------------------------------------------------------------------------------------------------------
        # Для базы данных Кати
        self.client_label = QLabel("Запросы для таблицы Diagnosis:", self)
        self.client_label.setGeometry(QtCore.QRect(305, 80, 200, 50))

        select_btn2_2k = QPushButton('Select for Diagnosis', self)
        select_btn2_2k.setToolTip('Execute SELECT query')
        select_btn2_2k.setGeometry(QtCore.QRect(300, 150, 200, 50))
        select_btn2_2k.clicked.connect(self.select_button_clicked2_4)

        self.client_label = QLabel("Сложные запросы:", self)
        self.client_label.setGeometry(QtCore.QRect(305, 770, 200, 50))

        select_btn_j12 = QPushButton('Select for PublicationDate', self)
        select_btn_j12.setToolTip('Execute SELECT query')
        select_btn_j12.setGeometry(QtCore.QRect(300, 840, 200, 50))
        select_btn_j12.clicked.connect(self.select_button_clicked2_5)

        select_btn_j22 = QPushButton('Select for Therapy', self)
        select_btn_j22.setToolTip('Execute SELECT query')
        select_btn_j22.setGeometry(QtCore.QRect(300, 910, 200, 50))
        select_btn_j22.clicked.connect(self.select_button_clicked2_6)

    def calendar_selection_changed(self):
        date = self.calendar.selectedDate()
        self.calendar_selected_date_label.setText(f"Выбранная дата: {date.toString('yyyy-MM-dd')}")

    def select_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        cursor = collection.find({})
        data = [json.loads(json.dumps(disease, default=str)) for disease in cursor]
        result_str = '\n'.join(
            [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
             data])

        msg = QMessageBox(self)
        msg.setWindowTitle('Diagnosis')
        msg.setText('SELECT query result:')
        msg.setDetailedText(result_str)
        msg.setFixedSize(900, 600)
        msg.exec_()
        client.close()

    def insert_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        # Получение данных для выполнения INSERT запроса
        disease_id, ok_pressed1 = QInputDialog.getText(self, "Введите данные", "ID заболевания:", QLineEdit.Normal, "")
        author, ok_pressed2 = QInputDialog.getText(self, "Введите данные", "Автор статьи:", QLineEdit.Normal, "")
        heading, ok_pressed3 = QInputDialog.getText(self, "Введите данные", "Заголовок статьи:", QLineEdit.Normal, "")
        link, ok_pressed4 = QInputDialog.getText(self, "Введите данные", "Ссылка на статью:", QLineEdit.Normal, "")
        pub_date, ok_pressed5 = QInputDialog.getText(self, "Введите данные", "Дата публикации статьи (YYYY-MM-DD):",
                                                     QLineEdit.Normal, "")
        medicine, ok_pressed6 = QInputDialog.getText(self, "Введите данные", "Название лекарства:", QLineEdit.Normal,
                                                     "")
        med_type, ok_pressed7 = QInputDialog.getText(self, "Введите данные", "Тип лекарства:", QLineEdit.Normal, "")
        name_method, ok_pressed8 = QInputDialog.getText(self, "Введите данные", "Название метода лечения:",
                                                        QLineEdit.Normal, "")
        therapy, ok_pressed9 = QInputDialog.getText(self, "Введите данные", "Описание метода лечения:",
                                                    QLineEdit.Normal, "")
        disease_name, ok_pressed10 = QInputDialog.getText(self, "Введите данные", "Название заболевания:",
                                                          QLineEdit.Normal, "")
        if ok_pressed1 and ok_pressed2 and ok_pressed3 and ok_pressed4 and ok_pressed5 and ok_pressed6 and ok_pressed7 and ok_pressed8 and ok_pressed9 and ok_pressed10:
            # Вызов функции для выполнения INSERT запроса
            record = {
                '_id': disease_id,
                'articles': [
                    {'author': author, 'heading': heading, 'link': link, 'publicationDate': pub_date}
                ],
                'medication': {'medicine': medicine, 'type': med_type},
                'method': {'nameMethod': name_method, 'therapy': therapy},
                'name': disease_name,
            }
            insert_record(collection, record)
        client.close()

    def update_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        # Получение id записи и полей для выполнения UPDATE запроса
        record_id, ok_pressed1 = QInputDialog.getText(self, "Введите данные", "ID записи:", QLineEdit.Normal, "")
        field, ok_pressed2 = QInputDialog.getText(self, "Введите данные", "Поле для обновления:", QLineEdit.Normal, "")
        new_value, ok_pressed3 = QInputDialog.getText(self, "Введите данные", "Новое значение:", QLineEdit.Normal, "")
        if ok_pressed1 and ok_pressed2 and ok_pressed3:
            # Вызов функции для выполнения UPDATE запроса
            query = {'_id': record_id}
            update_query = {'$set': {field: new_value}}
            update_record(collection, query, update_query)
        client.close()

    def delete_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        # Получение id записи для выполнения DELETE запроса
        record_id, ok_pressed = QInputDialog.getText(self, "Удаление записи", "ID записи для удаления:",
                                                     QLineEdit.Normal, "")
        if ok_pressed:
            # Вызов функции для выполнения DELETE запроса
            query = {'_id': record_id}
            delete_record(collection, query)
        client.close()

    def select_button_clicked2_5(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        query = {'articles.publicationDate': {'$gt': '2022-01-01'}}
        cursor = collection.find(query)

        data = [json.loads(json.dumps(doc, default=str)) for doc in cursor]
        result_str = '\n'.join(
            [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
             data])

        msg = QMessageBox(self)
        msg.setWindowTitle('Query Result')
        msg.setText('SELECT query result:')
        msg.setDetailedText(result_str)
        msg.setFixedSize(700, 500)
        msg.exec_()

        client.close()

    def select_button_clicked2_6(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        query = {'articles.publicationDate': {'$gt': '2022-01-01'}}
        projection = {'method.therapy': 1, 'name': 1, '_id': 0}
        cursor = collection.find(query, projection)

        result = []
        for record in cursor:
            result.append({'method.therapy': record['method']['therapy'], 'name': record['name']})

        result_str = '\n'.join(
            [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
             result])

        msg = QMessageBox(self)
        msg.setWindowTitle('Query Result')
        msg.setText('SELECT query result:')
        msg.setDetailedText(result_str)
        msg.setFixedSize(700, 500)
        msg.exec_()

        client.close()

    def select_button_clicked(self):
        conn = create_conn()
        if conn:
            res = select_from_table(conn, 'results')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Query Result')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def insert_into_results(conn):
        idresults, ok1 = QInputDialog.getText(None, "Enter Data", "idresults:", QLineEdit.Normal, "")
        dateresult, ok2 = QInputDialog.getText(None, "Enter Data", "dateresult:", QLineEdit.Normal, "")
        description, ok3 = QInputDialog.getText(None, "Enter Data", "description:", QLineEdit.Normal, "")

        if ok1 and ok2 and ok3:
            conn = create_conn()
            if conn:
                cursor = conn.cursor()
                idresults = int(idresults)
                try:
                    cursor.execute(
                        "INSERT INTO client.Results (idresults, dateresult, description) VALUES (%s, %s, %s)",
                        (idresults, dateresult, description))
                    conn.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    conn.rollback()
                conn.close()

    def update_results(conn):
        conn = create_conn()
        if conn:
            idresults, ok1 = QInputDialog.getText(None, "Enter Data", "idresults:", QLineEdit.Normal, "")
            new_dateresult, ok2 = QInputDialog.getText(None, "Enter Data", "new dateresult:", QLineEdit.Normal, "")
            new_description, ok3 = QInputDialog.getText(None, "Enter Data", "new description:", QLineEdit.Normal, "")
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE client.Results SET dateresult = %s, description = %s WHERE idresults = %s",
                    (new_dateresult, new_description, idresults))
                conn.commit()
            except Exception as e:
                print('Ошибка в запросе: ', e)
            finally:
                cursor.close()
                conn.close()

    def delete_from_results(conn):
        conn = create_conn()
        if conn:
            idresults, ok = QInputDialog.getText(None, "Enter Data", "idresults:", QLineEdit.Normal, "")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM client.Results WHERE idresults = %s", (idresults,))
            conn.commit()
            cursor.close()
            conn.close()

    def select_button_clicked2(self):
        conn = create_conn()
        if conn:
            res = select_from_table2(conn, 'client')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Query Result')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def insert_into_client(conn):
        idclient, ok1 = QInputDialog.getText(None, "Enter Data", "idclient:", QLineEdit.Normal, "")
        nameclient, ok2 = QInputDialog.getText(None, "Enter Data", "nameclient:", QLineEdit.Normal, "")
        phone, ok3 = QInputDialog.getText(None, "Enter Data", "phone:", QLineEdit.Normal, "")
        email, ok4 = QInputDialog.getText(None, "Enter Data", "email:", QLineEdit.Normal, "")

        if ok1 and ok2 and ok3 and ok4:
            conn = create_conn()
            if conn:
                cursor = conn.cursor()
                idclient = int(idclient)
                try:
                    cursor.execute(
                        "INSERT INTO client.Client (idclient, nameclient, phone, email) VALUES (%s, %s, %s, %s)",
                        (idclient, nameclient, phone, email))
                    conn.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    conn.rollback()
                conn.close()

    def update_client(conn):
        conn = create_conn()
        if conn:
            idclient, ok1 = QInputDialog.getText(None, "Enter Data", "idclient:", QLineEdit.Normal, "")
            new_phone, ok3 = QInputDialog.getText(None, "Enter Data", "new phone:", QLineEdit.Normal, "")
            new_email, ok4 = QInputDialog.getText(None, "Enter Data", "new email:", QLineEdit.Normal, "")

            cursor = conn.cursor()
            cursor.execute("UPDATE client.Client SET phone = %s, email = %s WHERE idclient = %s",
                           (new_phone, new_email, idclient))
            conn.commit()
            cursor.close()
            conn.close()

    def delete_client(self):
        conn = create_conn()
        if not conn:
            QMessageBox.critical(None, "Error", "Failed to connect to database.")
            return

        idclient, ok = QInputDialog.getText(None, "Enter Data", "idclient:", QLineEdit.Normal, "")
        if not ok:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT idclient FROM client.Client WHERE idclient = %s", (idclient,))
        row = cursor.fetchone()
        if not row:
            QMessageBox.critical(None, "Error", "Client not found.")
            cursor.close()
            conn.close()
            return

        cursor.execute("DELETE FROM client.Client WHERE idclient = %s", (idclient,))
        conn.commit()
        cursor.close()
        conn.close()

        # QMessageBox.information(None, "Success", "Client deleted successfully.")

    def show_review(self):
        dialog = ReviewDialog()
        dialog.exec_()

    def show_group(self):
        dialog = GroupDialog()
        dialog.exec_()

    def show_tests(self):
        conn = create_conn()
        if conn:
            res = select_from_table_tests(conn, 'tests')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Tests')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def show_result(self):
        conn = create_conn()
        if conn:
            res = select_from_table_results(conn, 'results')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Results')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def show_exit(self):
        reply = QMessageBox.question(self, "Подтверждение выхода", "Вы уверены, что хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def select_button_clickedj1(self):
        conn = create_conn()
        if conn:
            res = select_from_table_dateC(conn, 'contract')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Contracts')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def select_button_clickedj2(self):
        conn = create_conn()
        if conn:
            res = select_from_table_results(conn, 'results')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Results')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

class TherapistWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    # def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #    painter = QPainter(self)
    #    painter.setBrush(Qt.lightGray)
    #    painter.drawRect(self.rect())

    def setupUi(self):
        # Основное окно
        self.setWindowTitle("Психологическая помощь")
        # self.setGeometry(300, 300, 300, 300)
        self.resize(1900, 1000)
        self.setMinimumSize(QtCore.QSize(1000, 800))
        self.setMaximumSize(QtCore.QSize(1800, 1300))

        self.chat_button = QPushButton("Оставить отзыв", self)
        self.chat_button.clicked.connect(self.show_review)
        self.chat_button.setGeometry(QtCore.QRect(1250, 20, 500, 50))

        # Календарь
        self.calendar_label = QLabel("Ближайший сеанс:", self)
        self.calendar_label.setGeometry(QtCore.QRect(1250, 75, 500, 50))
        self.calendar = QCalendarWidget(self)
        self.calendar.setGeometry(QtCore.QRect(1250, 140, 500, 500))
        self.calendar.selectionChanged.connect(self.calendar_selection_changed)
        self.calendar_selected_date_label = QLabel(self)
        self.calendar_selected_date_label.setGeometry(QtCore.QRect(1250, 650, 500, 50))

        self.back_button = QPushButton("Выход", self)
        self.back_button.clicked.connect(self.show_exit)
        self.back_button.setGeometry(QtCore.QRect(50, 20, 200, 50))

        self.group_button = QPushButton("Групповая терапия", self)
        self.group_button.setGeometry(QtCore.QRect(1250, 710, 500, 50))
        self.group_button.clicked.connect(self.show_group)
        # Психологические тесты
        self.tests_button = QPushButton("Психологические тесты", self)
        self.tests_button.setGeometry(QtCore.QRect(1250, 780, 500, 50))
        self.tests_button.clicked.connect(self.show_tests)
        # Результаты
        self.results_button = QPushButton("Результаты", self)
        self.results_button.clicked.connect(self.show_result)
        self.results_button.setGeometry(QtCore.QRect(1250, 850, 500, 50))
        # --------------------------------------------------------------------------------------------------------------
        # Для базы данных Тани
        self.client_label = QLabel("Запросы для таблицы Therapist:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 80, 200, 50))

        select_btn2_2 = QPushButton('Select for Therapist', self)
        select_btn2_2.setToolTip('Execute SELECT query')
        select_btn2_2.setGeometry(QtCore.QRect(50, 150, 200, 50))
        select_btn2_2.clicked.connect(self.select_button_clicked2_2)

        insert_btn2_2 = QPushButton('Insert for Therapist', self)
        insert_btn2_2.setToolTip('Execute INSERT query')
        insert_btn2_2.setGeometry(QtCore.QRect(50, 220, 200, 50))
        insert_btn2_2.clicked.connect(self.insert_into_therapist)

        update_btn2_2 = QPushButton('Update for Therapist', self)
        update_btn2_2.setToolTip('Execute UPDATE query')
        update_btn2_2.setGeometry(QtCore.QRect(50, 290, 200, 50))
        update_btn2_2.clicked.connect(self.update_therapist)

        delete_btn2_2 = QPushButton('Delete for Therapist', self)
        delete_btn2_2.setToolTip('Execute Delete query')
        delete_btn2_2.setGeometry(QtCore.QRect(50, 360, 200, 50))
        delete_btn2_2.clicked.connect(self.delete_from_therapist)

        self.client_label = QLabel("Запросы для таблицы Hospital:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 430, 200, 50))

        select_btn = QPushButton('Select for Hospital', self)
        select_btn.setToolTip('Execute SELECT query')
        select_btn.setGeometry(QtCore.QRect(50, 500, 200, 50))
        select_btn.clicked.connect(self.select_button_clicked2_3)

        insert_btn = QPushButton('Insert for Hospital', self)
        insert_btn.setToolTip('Execute INSERT query')
        insert_btn.setGeometry(QtCore.QRect(50, 570, 200, 50))
        insert_btn.clicked.connect(self.insert_into_hospital)

        update_btn = QPushButton('Update for Hospital', self)
        update_btn.setToolTip('Execute UPDATE query')
        update_btn.setGeometry(QtCore.QRect(50, 640, 200, 50))
        update_btn.clicked.connect(self.update_hospital)

        delete_btn = QPushButton('Delete for Hospital', self)
        delete_btn.setToolTip('Execute Delete query')
        delete_btn.setGeometry(QtCore.QRect(50, 710, 200, 50))
        delete_btn.clicked.connect(self.delete_from_hospital)

        self.client_label = QLabel("Запросы с join:", self)
        self.client_label.setGeometry(QtCore.QRect(55, 770, 200, 50))

        select_btn_j1 = QPushButton('Select for Address', self)
        select_btn_j1.setToolTip('Execute SELECT query')
        select_btn_j1.setGeometry(QtCore.QRect(50, 840, 200, 50))
        select_btn_j1.clicked.connect(self.select_button_clickedj1_2)

        select_btn_j2 = QPushButton('Select for Price', self)
        select_btn_j2.setToolTip('Execute SELECT query')
        select_btn_j2.setGeometry(QtCore.QRect(50, 910, 200, 50))
        select_btn_j2.clicked.connect(self.select_button_clickedj2_2)
        # --------------------------------------------------------------------------------------------------------------
        # Для базы данных Кати
        self.client_label = QLabel("Запросы для таблицы Diagnosis:", self)
        self.client_label.setGeometry(QtCore.QRect(305, 80, 200, 50))

        select_btn2_2k = QPushButton('Select for Diagnosis', self)
        select_btn2_2k.setToolTip('Execute SELECT query')
        select_btn2_2k.setGeometry(QtCore.QRect(300, 150, 200, 50))
        select_btn2_2k.clicked.connect(self.select_button_clicked2_4)

        insert_btn2_2k = QPushButton('Insert for Diagnosis', self)
        insert_btn2_2k.setToolTip('Execute INSERT query')
        insert_btn2_2k.setGeometry(QtCore.QRect(300, 220, 200, 50))
        insert_btn2_2k.clicked.connect(self.insert_button_clicked2_4)

        update_btn2_2k = QPushButton('Update for Diagnosis', self)
        update_btn2_2k.setToolTip('Execute UPDATE query')
        update_btn2_2k.setGeometry(QtCore.QRect(300, 290, 200, 50))
        update_btn2_2k.clicked.connect(self.update_button_clicked2_4)

        delete_btn2_2k = QPushButton('Delete for Diagnosis', self)
        delete_btn2_2k.setToolTip('Execute Delete query')
        delete_btn2_2k.setGeometry(QtCore.QRect(300, 360, 200, 50))
        delete_btn2_2k.clicked.connect(self.delete_button_clicked2_4)

        self.client_label = QLabel("Сложные запросы:", self)
        self.client_label.setGeometry(QtCore.QRect(305, 770, 200, 50))

        select_btn_j12 = QPushButton('Select for PublicationDate', self)
        select_btn_j12.setToolTip('Execute SELECT query')
        select_btn_j12.setGeometry(QtCore.QRect(300, 840, 200, 50))
        select_btn_j12.clicked.connect(self.select_button_clicked2_5)

        select_btn_j22 = QPushButton('Select for Therapy', self)
        select_btn_j22.setToolTip('Execute SELECT query')
        select_btn_j22.setGeometry(QtCore.QRect(300, 910, 200, 50))
        select_btn_j22.clicked.connect(self.select_button_clicked2_6)

    def calendar_selection_changed(self):
        date = self.calendar.selectedDate()
        self.calendar_selected_date_label.setText(f"Выбранная дата: {date.toString('yyyy-MM-dd')}")

    def select_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        cursor = collection.find({})
        data = [json.loads(json.dumps(disease, default=str)) for disease in cursor]
        result_str = '\n'.join(
            [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
             data])

        msg = QMessageBox(self)
        msg.setWindowTitle('Diagnosis')
        msg.setText('SELECT query result:')
        msg.setDetailedText(result_str)
        msg.setFixedSize(900, 600)
        msg.exec_()
        client.close()

    def insert_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        # Получение данных для выполнения INSERT запроса
        disease_id, ok_pressed1 = QInputDialog.getText(self, "Введите данные", "ID заболевания:", QLineEdit.Normal, "")
        author, ok_pressed2 = QInputDialog.getText(self, "Введите данные", "Автор статьи:", QLineEdit.Normal, "")
        heading, ok_pressed3 = QInputDialog.getText(self, "Введите данные", "Заголовок статьи:", QLineEdit.Normal, "")
        link, ok_pressed4 = QInputDialog.getText(self, "Введите данные", "Ссылка на статью:", QLineEdit.Normal, "")
        pub_date, ok_pressed5 = QInputDialog.getText(self, "Введите данные", "Дата публикации статьи (YYYY-MM-DD):",
                                                     QLineEdit.Normal, "")
        medicine, ok_pressed6 = QInputDialog.getText(self, "Введите данные", "Название лекарства:", QLineEdit.Normal,
                                                     "")
        med_type, ok_pressed7 = QInputDialog.getText(self, "Введите данные", "Тип лекарства:", QLineEdit.Normal, "")
        name_method, ok_pressed8 = QInputDialog.getText(self, "Введите данные", "Название метода лечения:",
                                                        QLineEdit.Normal, "")
        therapy, ok_pressed9 = QInputDialog.getText(self, "Введите данные", "Описание метода лечения:",
                                                    QLineEdit.Normal, "")
        disease_name, ok_pressed10 = QInputDialog.getText(self, "Введите данные", "Название заболевания:",
                                                          QLineEdit.Normal, "")
        if ok_pressed1 and ok_pressed2 and ok_pressed3 and ok_pressed4 and ok_pressed5 and ok_pressed6 and ok_pressed7 and ok_pressed8 and ok_pressed9 and ok_pressed10:
            # Вызов функции для выполнения INSERT запроса
            record = {
                '_id': disease_id,
                'articles': [
                    {'author': author, 'heading': heading, 'link': link, 'publicationDate': pub_date}
                ],
                'medication': {'medicine': medicine, 'type': med_type},
                'method': {'nameMethod': name_method, 'therapy': therapy},
                'name': disease_name,
            }
            insert_record(collection, record)
        client.close()

    def update_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        # Получение id записи и полей для выполнения UPDATE запроса
        record_id, ok_pressed1 = QInputDialog.getText(self, "Введите данные", "ID записи:", QLineEdit.Normal, "")
        field, ok_pressed2 = QInputDialog.getText(self, "Введите данные", "Поле для обновления:", QLineEdit.Normal, "")
        new_value, ok_pressed3 = QInputDialog.getText(self, "Введите данные", "Новое значение:", QLineEdit.Normal, "")
        if ok_pressed1 and ok_pressed2 and ok_pressed3:
            # Вызов функции для выполнения UPDATE запроса
            query = {'_id': record_id}
            update_query = {'$set': {field: new_value}}
            update_record(collection, query, update_query)
        client.close()

    def delete_button_clicked2_4(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        # Получение id записи для выполнения DELETE запроса
        record_id, ok_pressed = QInputDialog.getText(self, "Удаление записи", "ID записи для удаления:",
                                                     QLineEdit.Normal, "")
        if ok_pressed:
            # Вызов функции для выполнения DELETE запроса
            query = {'_id': record_id}
            delete_record(collection, query)
        client.close()

    def select_button_clicked2_5(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        query = {'articles.publicationDate': {'$gt': '2022-01-01'}}
        cursor = collection.find(query)

        data = [json.loads(json.dumps(doc, default=str)) for doc in cursor]
        result_str = '\n'.join(
            [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
             data])

        msg = QMessageBox(self)
        msg.setWindowTitle('Query Result')
        msg.setText('SELECT query result:')
        msg.setDetailedText(result_str)
        msg.setFixedSize(700, 500)
        msg.exec_()

        client.close()

    def select_button_clicked2_6(self):
        client = connect()
        collection = get_collection(client, 'diagnosis')
        query = {'articles.publicationDate': {'$gt': '2022-01-01'}}
        projection = {'method.therapy': 1, 'name': 1, '_id': 0}
        cursor = collection.find(query, projection)

        result = []
        for record in cursor:
            result.append({'method.therapy': record['method']['therapy'], 'name': record['name']})

        result_str = '\n'.join(
            [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
             result])

        msg = QMessageBox(self)
        msg.setWindowTitle('Query Result')
        msg.setText('SELECT query result:')
        msg.setDetailedText(result_str)
        msg.setFixedSize(700, 500)
        msg.exec_()

        client.close()

    def select_button_clicked2_2(self):
        conn = create_conn()
        if conn:
            res = select_from_table2_2(conn, 'therapist')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Query Result')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def insert_into_therapist(conn):
        idTherapist, ok1 = QInputDialog.getText(None, "Enter Data", "idTherapist:", QLineEdit.Normal, "")
        nameTherapist, ok2 = QInputDialog.getText(None, "Enter Data", "nameTherapist:", QLineEdit.Normal, "")
        email, ok3 = QInputDialog.getText(None, "Enter Data", "email:", QLineEdit.Normal, "")
        phone, ok4 = QInputDialog.getText(None, "Enter Data", "phone:", QLineEdit.Normal, "")
        hospitalId, ok5 = QInputDialog.getText(None, "Enter Data", "hospitalId:", QLineEdit.Normal, "")
        educationId, ok6 = QInputDialog.getText(None, "Enter Data", "educationId:", QLineEdit.Normal, "")
        coursesId, ok7 = QInputDialog.getText(None, "Enter Data", "coursesId:", QLineEdit.Normal, "")
        experienceId, ok8 = QInputDialog.getText(None, "Enter Data", "experienceId:", QLineEdit.Normal, "")
        questionsId, ok9 = QInputDialog.getText(None, "Enter Data", "questionsId:", QLineEdit.Normal, "")
        costId, ok10 = QInputDialog.getText(None, "Enter Data", "costId:", QLineEdit.Normal, "")

        if ok1 and ok2 and ok3 and ok4 and ok5 and ok6 and ok7 and ok8 and ok9 and ok10:
            conn = create_conn()
            if conn:
                cursor = conn.cursor()
                idTherapist = int(idTherapist)
                hospitalId = int(hospitalId)
                educationId = int(educationId)
                coursesId = int(coursesId)
                experienceId = int(experienceId)
                questionsId = int(questionsId)
                costId = int(costId)

                try:
                    cursor.execute(
                        "INSERT INTO therapists.Therapist (idTherapist, nameTherapist, email, phone, hospitalId, educationId, coursesId, experienceId, questionsId, costId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (idTherapist, nameTherapist, email, phone, hospitalId, educationId, coursesId, experienceId,
                         questionsId, costId))
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()
                finally:
                    cursor.close()
                    conn.close()

    def update_therapist(conn):
        conn = create_conn()
        if conn:
            idTherapist, ok1 = QInputDialog.getText(None, "Enter Data", "idTherapist:", QLineEdit.Normal, "")
            new_nameTherapist, ok2 = QInputDialog.getText(None, "Enter Data", "new nameTherapist:", QLineEdit.Normal,
                                                          "")
            new_email, ok3 = QInputDialog.getText(None, "Enter Data", "new email:", QLineEdit.Normal, "")
            new_phone, ok4 = QInputDialog.getText(None, "Enter Data", "new phone:", QLineEdit.Normal, "")
            new_hospitalId, ok5 = QInputDialog.getText(None, "Enter Data", "new hospitalId:", QLineEdit.Normal, "")
            new_educationId, ok6 = QInputDialog.getText(None, "Enter Data", "new educationId:", QLineEdit.Normal, "")
            new_coursesId, ok7 = QInputDialog.getText(None, "Enter Data", "new coursesId:", QLineEdit.Normal, "")
            new_experienceId, ok8 = QInputDialog.getText(None, "Enter Data", "new experienceId:", QLineEdit.Normal, "")
            new_questionsId, ok9 = QInputDialog.getText(None, "Enter Data", "new questionsId:", QLineEdit.Normal, "")
            new_costId, ok10 = QInputDialog.getText(None, "Enter Data", "new costId:", QLineEdit.Normal, "")

            if ok1 and ok2 and ok3 and ok4 and ok5 and ok6 and ok7 and ok8 and ok9 and ok10:
                cursor = conn.cursor()
                idTherapist = int(idTherapist)
                new_hospitalId = int(new_hospitalId)
                new_educationId = int(new_educationId)
                new_coursesId = int(new_coursesId)
                new_experienceId = int(new_experienceId)
                new_questionsId = int(new_questionsId)
                new_costId = int(new_costId)

                try:
                    cursor.execute(
                        "UPDATE therapists.Therapist SET nameTherapist = %s, email = %s, phone = %s, hospitalId = %s, educationId = %s, coursesId = %s, experienceId = %s, questionsId = %s, costId = %s WHERE idTherapist = %s",
                        (new_nameTherapist, new_email, new_phone, new_hospitalId, new_educationId, new_coursesId,
                         new_experienceId, new_questionsId, new_costId, idTherapist))
                    conn.commit()
                except Exception as e:
                    print('Ошибка в запросе: ', e)
                    conn.rollback()
                finally:
                    cursor.close()
                    conn.close()

    def delete_from_therapist(conn):
        conn = create_conn()
        if conn:
            idTherapist, ok = QInputDialog.getText(None, "Enter Data", "idTherapist:", QLineEdit.Normal, "")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM therapists.Therapist WHERE idTherapist = %s", (idTherapist,))
            conn.commit()
            cursor.close()
            conn.close()

    def select_button_clicked2_3(self):
        conn = create_conn()
        if conn:
            res = select_from_table2_3(conn, 'hospital')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Query Result')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def insert_into_hospital(conn):
        id_hospital, ok1 = QInputDialog.getText(None, "Enter Data", "idHospital:", QLineEdit.Normal, "")
        name_hospital, ok2 = QInputDialog.getText(None, "Enter Data", "nameHospital:", QLineEdit.Normal, "")
        address, ok3 = QInputDialog.getText(None, "Enter Data", "address:", QLineEdit.Normal, "")

        if ok1 and ok2 and ok3:
            conn = create_conn()
            if conn:
                cursor = conn.cursor()
                id_hospital = int(id_hospital)
                try:
                    cursor.execute(
                        "INSERT INTO therapists.hospital (idHospital, nameHospital, address) VALUES (%s, %s, %s)",
                        (id_hospital, name_hospital, address))
                    conn.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    conn.rollback()
                conn.close()

    def update_hospital(conn):
        conn = create_conn()
        if conn:
            id_hospital, ok1 = QInputDialog.getText(None, "Enter Data", "idHospital:", QLineEdit.Normal, "")
            new_name_hospital, ok2 = QInputDialog.getText(None, "Enter Data", "new nameHospital:", QLineEdit.Normal, "")
            new_address, ok3 = QInputDialog.getText(None, "Enter Data", "new address:", QLineEdit.Normal, "")
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE therapists.hospital SET nameHospital = %s, address = %s WHERE idHospital = %s",
                    (new_name_hospital, new_address, id_hospital))
                conn.commit()
            except Exception as e:
                print('Ошибка в запросе: ', e)
            finally:
                cursor.close()
                conn.close()

    def delete_from_hospital(conn):
        conn = create_conn()
        if conn:
            id_hospital, ok = QInputDialog.getText(None, "Enter Data", "idHospital:", QLineEdit.Normal, "")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM therapists.hospital WHERE idHospital = %s", (id_hospital,))
            conn.commit()
            cursor.close()
            conn.close()

    def show_review(self):
        dialog = ReviewDialog()
        dialog.exec_()

    def show_group(self):
        dialog = GroupDialog()
        dialog.exec_()

    def show_tests(self):
        conn = create_conn()
        if conn:
            res = select_from_table_tests(conn, 'tests')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Tests')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def show_result(self):
        conn = create_conn()
        if conn:
            res = select_from_table_results(conn, 'results')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Results')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def show_exit(self):
        reply = QMessageBox.question(self, "Подтверждение выхода", "Вы уверены, что хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()


    def select_button_clickedj1_2(self):
        conn = create_conn()
        if conn:
            res = select_from_table_hosp(conn, 'hospital')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Hospitals')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()

    def select_button_clickedj2_2(self):
        conn = create_conn()
        if conn:
            res = select_from_table_price(conn, 'price')
            result_str = '\n'.join(
                [str(record).replace('{', '').replace('}', '').replace("'", '').replace(':', ' ') + '\n' for record in
                 res])

            msg = QMessageBox(self)
            msg.setWindowTitle('Prices')
            msg.setText('SELECT query result:')
            msg.setDetailedText(result_str)
            msg.setFixedSize(700, 500)
            msg.exec_()

            conn.close()


if __name__ == "__main__":
    app = QApplication([])
    login_register_window = LoginRegisterWindow()

    login_form_client = LoginFormClient()
    login_form_therapist = LoginFormTherapist()
    register_form_client = RegistrationFormClient()
    register_form_therapist = RegistrationFormTherapist()

    login_register_window.show()
    app.exec_()