from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json,glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('view.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def forget(self):
        self.manager.current = 'forget_screen'
    def login(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def back_signin(self):
        self.manager.transition.direction='right'
        self.manager.current = "login_screen"
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users:
            self.ids.sign_up_sign.text= "This Username Already Been Used!"
        else:
            users[uname] = {'username': uname, 'password': pword,
                'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            with open("users.json",'w') as f:
                json.dump(users,f)
            self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def login_in(self):
        self.manager.transition.direction='right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current = "login_screen"
    def get_text(self,feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            with open("quotes/{}.txt".format(feel),encoding='UTF-8') as file:
                quotes = file.readlines()
            self.ids.lb_output.text = random.choice(quotes)
        else:
            self.ids.lb_output.text = "Try another feeling"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class ForgetScreen(Screen):
    def get_password(self,uname,year):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['created'][0:4] == year:
            self.ids.lb_psw.text = "Your password is : " +users[uname]['password']
        else:
            self.ids.lb_psw.text = "Wrong"
    def back_signin(self):
        self.manager.transition.direction='left'
        self.manager.current = "login_screen"

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
