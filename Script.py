from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidget, QPushButton, QStackedWidget, QCommandLinkButton, QCheckBox, QLineEdit, QSpinBox, QDateEdit
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from datetime import date, datetime
import sys
import json
import os

def is_valid(username, password):
    for char in username:
        if not ('!' <= char <= '~'):
            return False
    for char in password:
        if not ('!' <= char <= '~'):
            return False
    return True

class User():
    def __init__(self, name, password, username):
        self.name = name
        self.password = password
        self.username = username

    def to_dict(self):
        return {
            'name': self.name,
            'password': self.password,
            'username': self.username
        }

class Userlist():
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def JSONreturn(self):
        return [item.to_dict() for item in self.items]

class Task():
    def __init__(self, name, deadline, priority, completed=False):
        self.name = name
        self.deadline = deadline 
        self.priority = priority
        self.completed = completed

    def to_dict(self):
        return {
            'name': self.name,
            'deadline': self.deadline,
            'priority': self.priority,
            'completed': self.completed
        }

class Tasklist():
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def delete_item(self, item):
        self.items.remove(item)

    def is_complete(self):
        complete_s = True
        msg_box = QMessageBox()
        not_completed = []
        for item in self.items:
            if not item.completed:
                complete_s = False
                not_completed.append(item.name)
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                
        if not complete_s:
            msg_box.setWindowTitle("Còn những nhiệm vụ nào chưa làm ?📜")
            msg_box.setText("Bạn có muốn hoàn thành những nhiệm vụ sau không ?\n" + ", ".join(not_completed))
            msg_box.exec()
        else:
            msg_box.setWindowTitle("Chúc Mừng🎇🎉✨")
            msg_box.setText("Tất cả nhiệm vụ đã được hoàn thành")
            msg_box.exec()

    def JSONreturn(self):
        return [item.to_dict() for item in self.items]
class LobbyPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PTI05/UI/main.ui",self)
        self.setWindowTitle("Xin chào!")
        self.tasklist = Tasklist()
        self.nv = self.findChild(QPushButton,"nhiemvu_button")
        self.nv.clicked.connect(self.show_nhiemvu)
        self.tt = self.findChild(QPushButton,"tientrinh_button")
        self.tt.clicked.connect(self.tientrinh)

    def tientrinh(self):
        c = 0
        d = 0
        with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/List.json', 'r') as f:
                    data = json.load(f)
                    for item in data:
                        d=d+1
                        task = Task(item["name"], item["deadline"], item["priority"], item["completed"])
                        if task.completed:
                            c=c+1
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Tiến trình📜")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(f"Bạn đã hoàn thành được {c}/{d} nhiệm vụ!")
        msg_box.exec()
    
        
    def show_nhiemvu(self):
        global showmain
        showmain.show()
        self.close()

class DangkiPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PTI05/UI/dangki.ui", self)
        self.setWindowTitle("Đăng kí tài khoản")
        self.userlist = Userlist()
        self.loadlist()
        self.cotk = self.findChild(QCommandLinkButton, "dacotaikhoan")
        self.cotk.clicked.connect(self.show_dangnhap)
        self.ndangki = self.findChild(QPushButton, "dangki_button")
        self.ndangki.clicked.connect(self.dangkitaikhoan)
    def show_dangnhap(self):
        global showdangnhap
        showdangnhap.show()
        self.close()

    def show_main(self):
        global showlobby
        showlobby.show()
        self.close()

    def loadlist(self):
        try:
            with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/User.json', 'r') as f:
                data = json.load(f)
                for item in data:
                    self.userlist.add_item(User(item["name"], item["password"], item["username"]))
        except (FileNotFoundError, json.JSONDecodeError):
            with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/User.json', 'w') as f:
                json.dump([], f)

    def dangkitaikhoan(self):
        self.dk_tendangnhap = self.tendangki_lineedit.text()
        self.dk_mkdangnhap = self.matkhaudangki_lineedit.text()
        self.dk_tenhienthi = self.tenhienthi_lineedit.text()
        if self.dk_tendangnhap == "" or self.dk_mkdangnhap == "" or self.dk_tenhienthi == "":
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Vui lòng điền đầy đủ thông tin ...✍(◔◡◔)")
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif len(self.dk_mkdangnhap) < 8:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Mật khẩu bắt buộc phải có tối thiểu 8 kí tự (☞ﾟヮﾟ)☞ ********")
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif not is_valid(self.dk_tendangnhap, self.dk_mkdangnhap):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Tên đăng nhập và mật khẩu chỉ được phép dùng kí tự Latin, chữ số '0' '1'...'9' và các kí tự như: '!' '@' '#' '$' '%' '^' '&' '*' '(' ')'")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif self.dk_tendangnhap in [user.username for user in self.userlist.items]:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Tên đăng nhập này đã được đăng kí 📍")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        else:
            name = self.dk_tenhienthi
            password = self.dk_mkdangnhap
            username = self.dk_tendangnhap
            self.person = User(name, password, username)
            self.userlist.add_item(self.person)
            with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/User.json', 'w',encoding='utf8') as f:
                json.dump(self.userlist.JSONreturn(), f, indent=4,ensure_ascii=False)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Đăng kí thành công✨")
            msg_box.setText(f"Chào mừng {name}, bạn đã đăng kí thành công tài khoản {username} ")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            self.show_main()
            self.close()

class DangnhapPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PTI05/UI/dangnhap.ui", self)
        self.setWindowTitle("Đăng nhập tài khoản")
        self.userlist = Userlist()
        self.khongcotk = self.findChild(QCommandLinkButton, "chuacotaikhoan")
        self.khongcotk.clicked.connect(self.show_dangki)
        self.dangnhap = self.findChild(QPushButton, "dangnhap_button")
        self.dangnhap.clicked.connect(self.dangnhaptaikhoan)
        self.loadlist()
        self.k=MainPage()
    def loadlist(self):
        try:
            with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/User.json', 'r') as f:
                data = json.load(f)
                for item in data:
                    self.userlist.add_item(User(item["name"], item["password"], item["username"]))
        except (FileNotFoundError, json.JSONDecodeError):
            with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/User.json', 'w') as f:
                json.dump([], f)

    def show_dangki(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Đăng nhập thành công ✅")
        msg_box.setText("Chào mừng bạn quay trở lại, " + [user.name for user in self.userlist.items if user.username == self.dn_tendangnhap][0] + " 🌟")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        global showdangki
        showdangki.show()
        self.close()

    def show_main(self):
        global showlobby
        showlobby.show()
        self.k.checkdeadline()
        self.close()
    def dangnhaptaikhoan(self):
        self.dn_tendangnhap = self.tendangnhap_lineedit.text()
        self.dn_mkdangnhap = self.matkhaudangnhap_lineedit.text()
        self.check = self.findChild(QCheckBox, "robotcheck")
        if self.dn_tendangnhap == "belphi" and self.dn_mkdangnhap == "belphi":
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Đăng nhập thành công ✅")
            msg_box.setText("Chào mừng thằng Dev béo phì quay trở lại 🤫🧏‍♂️")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            global showlobby
            showlobby.show()
            self.close()
        elif self.dn_tendangnhap == "" or self.dn_mkdangnhap == "":
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Vui lòng nhập đầy đủ thông tin để đăng nhập ...✍(◔◡◔)")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif not self.check.isChecked():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Bạn chưa xác nhận mình không phải là người máy 🤖")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif self.dn_tendangnhap not in [user.username for user in self.userlist.items]:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Tên đăng nhập không đúng ❌")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif self.dn_mkdangnhap not in [user.password for user in self.userlist.items]:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Mật khẩu không đúng ❌")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif self.dn_tendangnhap in [user.username for user in self.userlist.items] and self.dn_mkdangnhap in [user.password for user in self.userlist.items] and self.check.isChecked():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Đăng nhập thành công ✅")
            msg_box.setText("Chào mừng " + [user.name for user in self.userlist.items if user.username == self.dn_tendangnhap][0] + " đã trở lại 🌟")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            self.show_main()
            self.close()

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PTI05/UI/mainlist.ui", self)
        self.setWindowTitle("Danh sách nhiệm vụ của bạn - PTI05 course assignment")
        self.task_listwidget = self.findChild(QListWidget, "todolist")
        self.task_listwidget.clear()
        self.tasklist = Tasklist()
        self.loadlist()
        self.btn_deletetask = self.findChild(QPushButton, "xoa_button")
        self.btn_deletetask.clicked.connect(self.deletetask)
        self.btn_check = self.findChild(QPushButton, "hoanthanh_button")
        self.btn_check.clicked.connect(self.is_complete)
        self.btn_bian = self.findChild(QPushButton, "bian_button")
        self.btn_bian.clicked.connect(self.bian)
        self.btn_danhdau = self.findChild(QPushButton, "danhdau_button")
        self.btn_danhdau.clicked.connect(self.danhdau)
        self.btn_addtask = self.findChild(QPushButton, "them_button")
        self.btn_addtask.clicked.connect(self.addtask)
        '''self.timer = QTimer()
        self.timer.start(5000)
        self.timer.timeout.connect(self.checkdeadline)'''

    def danhdau(self):  
        current_index = self.task_listwidget.currentRow()
        if current_index!= -1:  
            task = self.tasklist.items[current_index]
            task.completed = not task.completed
            self.update_task(current_index, task)
    def update_task(self, index, task):
        item_text = f"{task.name} | Deadline: {task.deadline} | Priority: {task.priority} | Completed: {task.completed}"
        self.task_listwidget.takeItem(index)
        self.task_listwidget.insertItem(index, item_text)
    def loadlist(self): 
        if hasattr(self, 'task_listwidget'): 
            try:
                with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/List.json', 'r') as f:
                    data = json.load(f)
                    for item in data:
                        task = Task(item["name"], item["deadline"], item["priority"], item["completed"])
                        self.tasklist.add_item(task)
                        self.task_listwidget.addItem(f"{task.name} | Deadline: {task.deadline} | Priority: {task.priority} | Completed: {task.completed}")
            except FileNotFoundError:
                print("The file 'List.json' was not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON data.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
    def addtask(self):
        task_name = self.findChild(QLineEdit, "tennv_lineedit").text()
        task_deadline = self.findChild(QDateEdit, "deadline").date().toString("dd/MM/yyyy")
        task_priority = self.findChild(QSpinBox, "uutien").value()
        task_completed = False
        new_task = Task(task_name, task_deadline, task_priority, task_completed)
        self.tasklist.add_item(new_task)
        self.task_listwidget.addItem(f"{task_name} | Deadline: {task_deadline} | Priority: {task_priority} | Completed: {task_completed}")
        with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/List.json', 'w',encoding='utf8') as f:
            json.dump(self.tasklist.JSONreturn(), f, indent=4,ensure_ascii=False)
    def deletetask(self):
        selected_task = self.task_listwidget.currentItem()
        if selected_task:
            task_info = selected_task.text().split(" | ")
            task_name = task_info[0]
            for task in self.tasklist.items:
                if task.name == task_name:
                    self.tasklist.delete_item(task)
                    break
            self.task_listwidget.takeItem(self.task_listwidget.row(selected_task))
            with open('D:/Programming Languages/Python/EndCourseProject-PTI05/Data/List.json', 'w') as f:
                json.dump(self.tasklist.JSONreturn(), f, indent=4)
    
    def is_complete(self):
        self.tasklist.is_complete()
    def bian(self):
        msg_box = QMessageBox()
        msg_box.setText("Cập nhật tính năng sắp xếp danh sách🔀📜, tìm kiếm nhiệm vụ🔍📜, chức năng chỉnh sửa nhiệm vụ ⚙🛠📜, giao diện chính, menu✨📚")
        msg_box.setWindowTitle("Cập nhật sắp tới🎯")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def checkdeadline(self): 
        today = date.today()
        for task in self.tasklist.items:
            deadline_date = datetime.strptime(task.deadline, "%d/%m/%Y").date()
            if deadline_date == today and not task.completed:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Anh nhắc em😠")
                msg_box.setText(f"Nhiệm vụ {task.name} đã đến hạn⏰!")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.exec()
            elif deadline_date < today and not task.completed:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Anh nhắc em😠")
                msg_box.setText(f"Nhiệm vụ {task.name} đã đến hạn⏰!")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.exec()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    showdangnhap = DangnhapPage()
    showdangki = DangkiPage()
    showmain = MainPage()
    showlobby = LobbyPage()
    showdangnhap.show()
    app.exec()