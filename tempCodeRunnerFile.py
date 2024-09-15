from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidget, QPushButton,QCommandLinkButton, QCheckBox
from PyQt6 import uic
from datetime import *
import sys
import json
import os

def is_valid(username, password): #bộ lọc tiếng việt và kí tự lạ
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
    def to_dict(self):  # biến đổi dữ liệu qua JSON
        return {
            'name': self.name,
            'password': self.password,
            'username': self.username
        }

class Userlist():
    def __init__(self):
        self.items = [] # danh sách người dùng
    def add_item(self, item):
        self.items.append(item) # thêm người dùng vào danh sách
    def JSONreturn(self):
        return [item.to_dict() for item in self.items]
class task():
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
class tasklist():
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
    def delete_item(self, item):
        self.items.remove(item)
    def is_complete(self):
        complete_s = True
        msg_box = QMessageBox
        not_completed = []
        for item in self.items:
            if not item.completed:
                complete_s = False
                not_completed.append(item.name)
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle("Còn những nhiệm vụ nào chưa làm ?📜")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                
        if complete_s == False:
            msg_box.setText("Bạn có muốn hoàn thành những nhiệm vụ sau không ?\n" + ", ".join(not_completed))
            msg_box.exec()
        elif complete_s:
            msg_box.setText("Tất cả nhiệm vụ đã được hoàn thành")
            msg_box.exec()
    def JSONreturn(self):
        return [item.to_dict() for item in self.items]
    
class dangki_page(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PYI/UI/dangki.ui",self)
        self.userlist = Userlist() # danh sách người dùng
        self.loadlist()#tải dữ liệu người dùng
        #sự kiện có tài khoản
        self.cotk=self.findChild(QCommandLinkButton,"dacotaikhoan")
        self.cotk.clicked.connect(self.show_dangnhap)
        #sự kiện ấn nút đăng kí
        self.ndangki=self.findChild(QPushButton,"dangki_button")
        self.ndangki.clicked.connect(self.dangkitaikhoan)
    #định nghĩa sự kiện có tài khoản
    def show_dangnhap(self):
        global showdangnhap
        showdangnhap.show()
        self.close()
    def show_main(self):
        global showmain
        showmain.show()
        self.close()
    #tải dữ liệu
    def loadlist(self):
        with open('D:/Programming Languages/Python/EndCourseProject-PYI/Data/User.json','r') as f:
            data = json.load(f)
            for item in data:
                self.userlist.add_item(User(item["name"],item["password"],item["username"]))
    #đăng kí tài khoản
    def dangkitaikhoan(self):
        self.dk_tendangnhap = self.tendangki_lineedit.text()
        self.dk_mkdangnhap = self.matkhaudangki_lineedit.text()
        self.dk_tenhienthi = self.tenhienthi_lineedit.text()
        #cảnh báo lỗi thông tin
        if self.dk_tendangnhap == "" or self.dk_mkdangnhap == "" or self.dk_tenhienthi == "":
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Vui lòng điền đầy đủ thông tin ...✍(◔◡◔)")
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setWindowIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif len(self.dk_mkdangnhap) < 8:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Mật khẩu bắt buộc phải có tối thiểu 8 kí tự (☞ﾟヮﾟ)☞ ********")
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setWindowIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif not is_valid(self.dk_tendangnhap,self.dk_mkdangnhap):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setWindowIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Tên đăng nhập và mật khẩu chỉ được phép dùng kí tự Latin , chữ số '0' '1'...'9' và các kí tự như: '!' '@' '#' '$' '%' '^' '&' '*' '(' ')'")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif self.dk_tendangnhap in [user.username for user in self.userlist.items]:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setWindowIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Tên đăng nhập này đã được đăng kí 📍")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        else:
            name = self.dk_tenhienthi
            password = self.dk_mkdangnhap
            username = self.dk_tendangnhap
            self.person=User(name,password,username)
            self.userlist.add_item(self.person)
            with open('User.json','w') as f: 
                json.dump(self.userlist.JSONreturn(),f,indent=4)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowIcon(QMessageBox.Icon.NoIcon)
            msg_box.setWindowTitle("Đăng kí thành công✨")
            msg_box.setText(f"Chào mừng {name}, bạn đã đăng kí thành công tài khoản {username} ")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            self.close()
            self.show_main()


class dangnhap_page(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PYI/UI/dangnhap.ui",self)
        self.userlist = Userlist()
        #sự kiện không có tài khoản
        self.khongcotk=self.findChild(QCommandLinkButton,"chuacotaikhoan")
        self.khongcotk.clicked.connect(self.show_dangki)
        self.dangnhap=self.findChild(QPushButton,"dangnhap_button")
        self.dangnhap.clicked.connect(self.dangnhaptaikhoan)

        self.loadlist()
    def loadlist(self): #tài dữ liệu người dùng
        with open('D:/Programming Languages/Python/EndCourseProject-PYI/Data/User.json','r') as f:
            data = json.load(f)
            for item in data:
                self.userlist.add_item(User(item["name"],item["password"],item["username"]))
    #định nghĩa sự kiện không có tài khoản
    def show_dangki(self):
        global showdangki
        showdangki.show()
        self.close()
    def show_main(self):
        global showmain
        showmain.show()
        self.close()
    def dangnhaptaikhoan(self):
        self.dn_tendangnhap = self.tendangnhap_lineedit.text()
        self.dn_mkdangnhap = self.matkhaudangnhap_lineedit.text()
        self.check = self.findChild(QCheckBox,"robotcheck")
        # Kiểm tra định dạng
        if self.dn_tendangnhap == "" or self.dn_mkdangnhap == "":
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Vui lòng điền đầy đủ thông tin ...✍(◔◡◔)")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif not is_valid(self.dn_tendangnhap,self.dn_mkdangnhap):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Tên đăng nhập và mật khẩu chỉ được phép dùng kí tự Latin , chữ số '0' '1'...'9' và các kí tự như: '!' '@' '#' '$' '%' '^' '&' '*' '(' ')'")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif not(self.dn_tendangnhap in [user.username for user in self.userlist.items]):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText(f"Không tìm thấy tài khoản {self.dn_tendangnhap}🔍❌")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif not self.check.isChecked():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Robot ư?🤨🤔 chúng tôi không cho robot vào🤖🚫")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif not (self.dn_mkdangnhap in [user.password for user in self.userlist.items]):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText(f"Sai mật khẩu❌")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        else:
            for i in range(len(self.userlist.items)):
                if self.dn_tendangnhap == self.userlist.items[i].username and self.dn_mkdangnhap == self.userlist.items[i].password:
                    name = self.userlist.items[i].name
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Đăng nhập thành công✨")
            msg_box.setText(f"Chào mừng {name}!")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            self.show_main()
            self.close()

class main_page(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PYI/UI/main.ui",self)
        #thiết lập các nút trong giao diện chính   
        self.nhiemvu=self.findChild(QPushButton,"nhiemvu_button")
        self.nhiemvu.clicked.connect(self.show_nhiemvu)
        #self.tientrinh=self.findChild(QPushButton,"tientrinh_button")
        #self.tientrinh.clicked.connect(self.show_tientrinh)
        self.comingsoon=self.findChild(QPushButton,"comingsoon_button")
        self.comingsoon.clicked.connect(self.show_comingsoon)

    #định nghĩa chức năng của các nut trong giao diện chính
    def show_nhiemvu(self):
        global shownhiemvu
        shownhiemvu.show()
        self.close()
    #def show_tientrinh(self):
    def show_comingsoon(self):
            msg_box=QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Cập nhật sắp tới🎯")
            msg_box.setText("Cập nhật chức năng Ghi chú 📝, nhắc nhở thường xuyên ⏰ và cập nhật thêm chỉnh thời gian trong ngày cho deadline🕒 ")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
class nhiemvu_page(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/Programming Languages/Python/EndCourseProject-PYI/UI/mainlist.ui",self)

        self.list=self.findChild(QListWidget,"todolist")
        self.loadlist()
        self.tennhiemvu=self.tennv.text()
        self.thembutton=self.findChild(QPushButton,"them_button")
        self.thembutton.clicked.connect(self.them)
        self.xoabutton=self.findChild(QPushButton,"xoa_button")
        self.xoabutton.clicked.connect(self.xoa)
        self.chinhsuabutton=self.findChild(QPushButton,"chinhsua_button")
        self.chinhsuabutton.clicked.connect(self.chinhsua)
        self.sapxepbutton=self.findChild(QPushButton,"sapxep_button")
        self.sapxepbutton.clicked.connect(self.sapxep)
        self.hoanthanhbutton=self.findChild(QPushButton,"hoanthanh_button")
        self.hoanthanhbutton.clicked.connect(self.hoanthanh)
        self.lenbutton=self.findChild(QPushButton,"len_button")
        self.lenbutton.clicked.connect(self.len)
        self.xuongbutton=self.findChild(QPushButton,"xuong_button")
        self.xuongbutton.clicked.connect(self.xuong)
        self.bianbutton=self.findChild(QPushButton,"bian_button")
        self.bianbutton.clicked.connect(self.sukienbian)
        self.uutien.value()
        self.deadline.date()
        self.tasklist=tasklist()
    def len(self):
        pass
    def xuong(self):
        pass
    def them(self):
        if(self.uutien =="" or self.deadline =="" or self.tennhiemvu ==""):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Cảnh báo ❌")
            msg_box.setText("Vui lòng điền đầy đủ thông tin ...✍(◔◡◔) ")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        else:
            self.list.addItem(self.tennhiemvu)
            self.tennhiemvu.setText("")
            self.tasklist.add_item(self.tennhiemvu,self.deadline,self.uutien)
            with open('D:\Programming Languages\Python\EndCourseProject-PYI\Data\List.json','w') as f:
                json.dump(self.tasklist.JSONreturn(),f,indent=4)

    def loadlist(self):
        with open('D:\Programming Languages\Python\EndCourseProject-PYI\Data\List.json','r') as f:
            self.data=tasklist(json.load(f))
        for i in self.data.tasks:
            self.list.addItem(i)
    def xoa(self):
        clicked=self.list.currentRow()
        self.list.takeItem(clicked)
        self.tasklist.delete_item(clicked)
    def chinhsua(self):
        pass
    def sapxep(self):
        pass
    def hoanthanh(self):
        pass
    def sukienbian(self):
        pass

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    showdangki = dangki_page()
    showdangnhap = dangnhap_page()
    showmain = main_page()
    shownhiemvu = nhiemvu_page()

    showdangnhap.show()
    sys.exit(app.exec())