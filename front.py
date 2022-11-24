from tkinter import *
import tkinter.font
from back import *


bot_name = "AI 약사"
BG_GRAY = "#F6F8FA"
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"
TI_COLOR = "#669933"
BT_COLOR = "#CCFF99"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
FONT_TEXT = "맑은고딕"


class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        # 제목 라벨
        head_label = Label(self.window, bg=TI_COLOR, fg="#FFFFFF",
                           text="AI약사", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # 채팅창
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT_TEXT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # 스크롤바
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.98)
        scrollbar.configure(command=self.text_widget.yview)
        
        # 하단 라벨
        bottom_label = Label(self.window, bg=TI_COLOR, height=60) #  80
        bottom_label.place(relwidth=1, rely=0.865) # 0.825
        
        # 메세지 박스
        self.msg_entry = Entry(bottom_label, bg="#FFFFFF", fg="#000000", font="FONT_TEXT 12")
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # Ask버튼
        send_button = Button(bottom_label, text="ASK", font=FONT_BOLD, width=20, bg=BT_COLOR, activebackground="#669933",
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
        # 최초 실행 메세지
        self.msg_entry.delete(0, END)
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, "안녕하세요 고객님, 무엇을 도와드릴까요?\n\n")
        self.text_widget.see(END)
        #

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "고객님")


    # 메세지 출력 함수    
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        
        self.text_widget.configure(state=DISABLED)                 
        msg2 = f"{bot_name}: {respond(msg)}\n\n"  
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED) 
        
        self.text_widget.see(END)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()