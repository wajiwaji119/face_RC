import os.path
import datetime
import pickle
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, '入室する', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, '退出する', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, '新しく登録する', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.add_webcam(self.webcam_label)
        self.db_dir = 'face-attendance-system-master\db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log_path = 'face-attendance-system-master\log.txt'
        
        
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()
        
        
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)
        
        
    def login(self):
        name = util.recognize(self.most_recent_capture_arr, self.db_dir)
        if name in ['登録されていないユーザーです。', 'あなたの情報は見つかりません']:
            util.msg_box('ログインに失敗しました', 'あなたの情報は登録されていません。もう一度やり直すか、顔写真の登録をお願いします。')
        else:
            dt6= datetime.datetime.now()
            strdt6 = dt6.strftime('%Y-%m-%d %H:%M:%S')

            util.msg_box('入室', 'ようこそ, {}.'.format(name)+'さん！\n{}.'.format(strdt6)+'に入室しました!')
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                f.close()
                

    def logout(self):

        name = util.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['登録されていないユーザーです。', 'あなたの情報は見つかりません']:
            util.msg_box('ログアウトに失敗しました', 'あなたの情報は登録されていません。もう一度やり直すか、顔写真の登録をお願いします。')
        else:
            dt6= datetime.datetime.now()
            strdt6 = dt6.strftime('%Y-%m-%d %H:%M:%S')
            util.msg_box('退室', 'またね！, {}.'.format(name)+'さん！\n{}.'.format(strdt6)+'に退室を確認しました!')
            with open(self.log_path, 'a') as f:
                f.write('{},{},out\n'.format(name, datetime.datetime.now()))
                f.close()


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, '登録する', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'もう一度やり直す', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        self.add_img_to_label(self.capture_label)
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, '初めまして！, \nお名前を入力してください！:')
        self.text_label_register_new_user.place(x=750, y=70)
        
        
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
        
        

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
    def start(self):
        self.main_window.mainloop()
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]
        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        pickle.dump(embeddings, file)
        util.msg_box('登録しました!', 'これからよろしくお願いします!')
        
        self.register_new_user_window.destroy()
if __name__ == "__main__":
    app = App()
    app.start()