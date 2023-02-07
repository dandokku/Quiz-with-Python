import re
import random
import sqlite3
import sys
import time
# gets current date and time
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen

# create a connection to the database
db = sqlite3.connect('C:\\Users\\USER\\PycharmProjects\\Quiz\\quizdatabase.db')

# creating our cursor object
cur = db.cursor()

# getting the current date and storing in a variable
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

# method for getting random values
random_val = (random.randint(1000000, 99999999))

# converting values to hex decimal
val = format(random_val, 'x')

score = 0
user_n = " "


# --------------------------------------------------------------Splash Screen----------------------------------------------------------------
class Screen(QSplashScreen, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\splashscreen.ui', self)
        self.setWindowFlag(
            Qt.FramelessWindowHint)  # this removes the frame from the window, making it a frameless window
        pixmap = QPixmap("welp.jpg")  # this is the background of the pixmap
        self.setPixmap(pixmap)
        self.hide()

    def progress(self):
        for i in range(100):
            time.sleep(0.01)
            self.progressBar.setValue(i)


# ------------------------------------------------------Home Window------------------------------------------------------------
class Home(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\home_page.ui', self)
        self.show()
        self.log_btn.clicked.connect(self.open_login_win)
        self.reg_btn.clicked.connect(self.open_reg_win)
        self.exit.clicked.connect(self.close_app)

    def open_login_win(self):
        Login(self)
        self.hide()

    def open_reg_win(self):
        Register(self)
        self.hide()

    def close_app(self):
        self.close()


# -----------------------------------------------------Register Window------------------------------------------------
class Register(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Register, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\Register_Page.ui', self)
        self.show()  # displaying the current window
        self.reg_btn.clicked.connect(self.home)
        self.cancel_btn.clicked.connect(self.go_back)

    def go_back(self):
        Home(self)
        self.hide()

    def home(self):
        special_symbols = ["@", "#", "&", "$", "%"]
        vals = True
        username = self.username_box.text()
        email = self.email_box.text()
        password = self.password_box.text()
        confirm = self.confirm_box.text()

        if username == " ":
            window = Messagebox1(self)
            vals = False

        if username == [" ", "@", "%", "^", "*", "(", ")"]:
            window = Messagebox1(self)
            vals = False

        elif len(username) > 10:
            window = Messagebox1(self)
            vals = False

        if email == " ":
            window = Messagebox1(self)
            vals = False

        if password == " ":
            window = Messagebox1(self)
            vals = False

        elif len(password) < 6:
            window = Messagebox1(self)
            vals = False

        elif len(password) > 8:
            window = Messagebox1(self)
            vals = False

        if confirm != password:
            window = Messagebox1(self)
            vals = False

        elif not any(char.isdigit() for char in password):
            window = Messagebox1(self)
            vals = False

        elif not any(char in special_symbols for char in password):
            window = Messagebox1(self)
            vals = False

        else:
            if password == confirm:
                cur.execute(
                    "INSERT into Userdetails(Username, Emailaddress, Password) values(?,?,?)",
                    (username, email, password))
                db.commit()

                window = Success(self)
                global email_var
                email_var = email

                self.hide()
            else:
                window = Messagebox1(self)
                vals = False


# ------------------------------------------------Login Window---------------------------------------------------------
class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\Login_Page.ui', self)
        self.show()
        self.log_btn.clicked.connect(self.dashboard)
        self.cancel_btn.clicked.connect(self.go_back)

    def go_back(self):
        Home(self)
        self.hide()

    def dashboard(self):
        Dashboard(self)
        self.hide()

        user_name = self.username_box.text()
        pass_word = self.password_box.text()

        statement = cur.execute(
            f"Select * from Userdetails where Username  = '{user_name}' AND Password = '{pass_word}'")
        result = cur.fetchall()
        print(result)

        for state in statement:
            if user_name == state and pass_word == state:
                print(state)
                Dashboard(self)
                self.hide()
            else:
                Messagebox2(self)
                self.hide()


# -------------------------------------------------------------------------------Dashboard Windows---------------------------------------------------
class Dashboard(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dashboard, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\dashboard.ui', self)
        self.show()
        self.play.clicked.connect(self.level)
        self.highscores.clicked.connect(self.highscore)
        self.setting.clicked.connect(self.settings)
        self.exit_btn.clicked.connect(self.exit)
        global user_n
        query = "SELECT Username from Userdetails where Username  like '" + user_n + "'"
        cur.execute(query)
        self.uname = cur.fetchone()
        print(self.uname)
        if self.uname:
            self.name.setText(self.uname[0])
            db.commit()
        else:
            print("not working")

    def level(self):
        Level(self)
        self.hide()

    def highscore(self):
        Highscore(self)
        self.hide()

    def settings(self):
        Settings(self)
        self.hide()

    def exit(self):
        self.close()

        # username_box = cur.execute("Select Username from Userdetails")
        # username_box.fetchone()
        # self.name.setText(username_box)


# -------------------------------------------------------------Highscore Windows----------------------------------------------------
class Highscore(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Highscore, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\highscore.ui', self)
        self.show()


# --------------------------------------------------------------Setting / Logout Windows-------------------------------------------------------------
class Settings(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\settings.ui', self)
        self.show()
        self.log_out_2.clicked.connect(self.logout)
        self.back.clicked.connect(self.dashboard)

    def logout(self):
        Logout(self)
        self.show()

    def dashboard(self):
        Dashboard(self)
        self.hide()


class Logout(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Logout, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\logout.ui', self)
        self.show()
        self.yes.clicked.connect(self.home)
        self.no.clicked.connect(self.settings)

    def home(self):
        Home(self)
        self.hide()

    def settings(self):
        Settings(self)
        self.hide()


# ------------------------------------------------------LEVEL WINDOW--------------------------------------------------------
class Level(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Level, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\level.ui', self)
        self.show()
        self.back_btn.clicked.connect(self.go_back)
        self.lvl_one.clicked.connect(self.begin)
        self.lvl_two.clicked.connect(self.messagebox3)
        self.lvl_three.clicked.connect(self.messagebox3)
        self.lvl_four.clicked.connect(self.messagebox3)
        self.lvl_five.clicked.connect(self.messagebox3)

    def go_back(self):
        Dashboard(self)
        self.hide()

    def begin(self):
        Begin(self)
        self.show()

    def messagebox3(self):
        Messagebox3(self)
        self.show()


class Begin(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Begin, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\begin.ui', self)
        self.show()
        self.yes_btn.clicked.connect(self.lvl_one_q1)
        self.no_btn.clicked.connect(self.level)

    def lvl_one_q1(self):
        Lvl_One_Q1(self)
        self.hide()

    def level(self):
        Level(self)
        self.hide()


# -------------------------------------------------------------------Level 1----------------------------------------------------
class Lvl_One_Q1(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Lvl_One_Q1, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\lvl_one_q1.ui', self)
        self.show()
        self.exit_btn.clicked.connect(self.close_app)
        self.d.clicked.connect(self.lvl_one_q2)
        self.c.clicked.connect(self.messagebox4)
        self.b.clicked.connect(self.messagebox4)
        self.a.clicked.connect(self.messagebox4)

    def close_app(self):
        self.close()

    def lvl_one_q2(self):
        Lvl_One_Q2(self)
        self.show()

    def messagebox4(self):
        Messagebox4(self)
        self.show()


class Lvl_One_Q2(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Lvl_One_Q2, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\lvl_one_q2.ui', self)
        self.show()
        self.exit_btn.clicked.connect(self.close_app)
        self.b.clicked.connect(self.lvl_one_q3)
        self.c.clicked.connect(self.messagebox4)
        self.d.clicked.connect(self.messagebox4)
        self.a.clicked.connect(self.messagebox4)

    def close_app(self):
        self.close()

    def lvl_one_q3(self):
        Lvl_One_Q3(self)
        self.show()

    def messagebox4(self):
        Messagebox4(self)
        self.show()


class Lvl_One_Q3(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Lvl_One_Q3, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\lvl_one_q3.ui', self)
        self.show()
        self.exit_btn.clicked.connect(self.close_app)
        self.d.clicked.connect(self.lvl_one_q4)
        self.a.clicked.connect(self.messagebox4)
        self.b.clicked.connect(self.messagebox4)
        self.c.clicked.connect(self.messagebox4)

    def close_app(self):
        self.close()

    def lvl_one_q4(self):
        Lvl_One_Q4(self)
        self.show()

    def messagebox4(self):
        Messagebox4(self)
        self.show()


class Lvl_One_Q4(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Lvl_One_Q4, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\lvl_one_q4.ui', self)
        self.show()
        self.exit_btn.clicked.connect(self.close_app)
        self.b.clicked.connect(self.lvl_one_q5)
        self.c.clicked.connect(self.messagebox4)
        self.d.clicked.connect(self.messagebox4)
        self.a.clicked.connect(self.messagebox4)

    def close_app(self):
        self.close()

    def lvl_one_q5(self):
        Lvl_One_Q5(self)
        self.show()

    def messagebox4(self):
        Messagebox4(self)
        self.show()


class Lvl_One_Q5(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Lvl_One_Q5, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\lvl_one_q5.ui', self)
        self.show()
        self.exit_btn.clicked.connect(self.close_app)
        self.a.clicked.connect(self.messagebox5)
        self.c.clicked.connect(self.messagebox4)
        self.d.clicked.connect(self.messagebox4)
        self.b.clicked.connect(self.messagebox4)

    def close_app(self):
        self.close()

    def messagebox5(self):
        Messagebox5(self)
        self.show()

    def messagebox4(self):
        Messagebox4(self)
        self.show()


# ----------------------------------------------------------Message Box Windows--------------------------------------------------------------
class Messagebox1(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Messagebox1, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\messagebox1.ui', self)
        self.show()


class Messagebox2(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Messagebox2, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\messagebox2.ui', self)
        self.show()
        self.reg_btn.clicked.connect(self.open_reg_win)
        self.cancel_btn.clicked.connect(self.go_back)

    def open_reg_win(self):
        Register(self)
        self.hide()

    def go_back(self):
        Login(self)
        self.hide()


class Messagebox3(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Messagebox3, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\messagebox3.ui', self)
        self.show()
        self.ok.clicked.connect(self.level)

    def level(self):
        Level(self)
        self.hide


class Messagebox4(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Messagebox4, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\messagebox4.ui', self)
        self.show()
        self.restart.clicked.connect(self.begin)
        self.main_menu.clicked.connect(self.level)

    def begin(self):
        Begin(self)
        self.hide()

    def level(self):
        Level(self)
        self.hide()


class Messagebox5(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Messagebox5, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\messagebox5.ui', self)
        self.show()
        self.restart.clicked.connect(self.begin)
        self.main_menu.clicked.connect(self.level)

    def begin(self):
        Begin(self)
        self.hide()

    def level(self):
        Level(self)
        self.hide()


class Success(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Success, self).__init__(parent)
        uic.loadUi('C:\\Users\\USER\\PycharmProjects\\Quiz\\successful.ui', self)
        self.show()
        self.ok_btn.clicked.connect(self.home)

    def home(self):
        Home(self)
        self.hide()


app = QtWidgets.QApplication(sys.argv)

# creating a main window
main = Home()

# SplashScreen
splash = Screen()
splash.show()
splash.progress()

window = Home()
window.show()

splash.finish(window)

widget = QtWidgets.QStackedWidget()
# widget.addWidget(main)

# Setting a definite size, so the user won't be able to change the size
widget.setFixedWidth(480)
widget.setFixedHeight(620)

app.setQuitOnLastWindowClosed(True)

# executing the app
app.exec_()
