import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import webbrowser
import project1_console_app as core


class App(tk.Tk): #main window class
    tag_id = 0 #a variable for generating tags when binding them for events

    def __init__(self): #initializes GUI and needed variables
        super().__init__()
        self.title("Project1")
        # self.geometry()
        self.minsize(535 ,600)

        self.text = ""
        self.dfa_email ,self.dfa_web ,self.re_email ,self.re_web = core.initial()

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff="false")
        file_menu.add_command(label="Save Results" ,command=self.save)
        file_menu.add_command(label="Clear all" ,command=self.clear)
        file_menu.add_separator()
        file_menu.add_command(label="Exit" ,command=self.destroy)
        help_menu = tk.Menu(menubar, tearoff="false")
        help_menu.add_command(label="About" ,command=lambda: tk.messagebox.showinfo("About" ,"Hello from Hosein Fanai !"))
        menubar.add_cascade(label="File" ,menu=file_menu)
        menubar.add_cascade(label="Help" ,menu=help_menu)

        tk.Label(self ,text="Web address or Text file path").place(x=5 ,y=5)
        self.inp_path = tk.StringVar()
        tk.Entry(self ,textvariable=self.inp_path).place(x=170 ,y=7 ,relwidth=0.35)
        self.search_btn = ttk.Button(self ,text="Search" ,command=self.search ,state="disable")
        ttk.Button(self ,text="Open" ,command=self.open).place(relx=0.35 ,y=5 ,x=180)
        self.def_lib = tk.IntVar()
        self.def_lib.set(0)
        ttk.Checkbutton(self ,text="Use default librarys" ,takefocus=0 ,variable=self.def_lib).place(relx=0.35 ,y=35 ,x=205)
        self.sec_dep = tk.IntVar()
        self.sec_dep.set(0)
        ttk.Checkbutton(self ,text="Search emails in found urls(not recommended!)" ,takefocus=0 ,variable=self.sec_dep).place(relx=0.35 ,y=35 ,x=-75)

        pan_win = tk.PanedWindow(self ,showhandle=True ,handlesize=12 ,relief="ridge")

        lf_email = tk.LabelFrame(pan_win ,text="Emails")
        self.out_email = tk.Text(lf_email ,state="disable" ,width=20)
        scrl_email = ttk.Scrollbar(lf_email ,command=self.out_email.yview)
        self.out_email.config(yscrollcommand=scrl_email.set)
        self.out_email.pack(side=tk.LEFT ,fill=tk.BOTH ,expand=True)
        scrl_email.pack(side=tk.RIGHT ,fill=tk.Y)

        lf_web = tk.LabelFrame(pan_win ,text="Web addresses")
        self.out_web = tk.Text(lf_web ,state="disable" ,width=20)
        scrl_web = ttk.Scrollbar(lf_web ,command=self.out_web.yview)
        self.out_web.config(yscrollcommand=scrl_web.set)
        self.out_web.pack(side=tk.LEFT ,fill=tk.BOTH ,expand=True)
        scrl_web.pack(side=tk.RIGHT ,fill=tk.Y)

        pan_win.add(lf_email)
        pan_win.add(lf_web)

        self.msg = tk.Label(self ,text="Welcome!" ,fg="blue")

        self.search_btn.place(relx=0.35 ,y=5 ,x=265)
        pan_win.place(x=10 ,y=55 ,relwidth=0.8 ,relheight=0.9)
        self.msg.place(rely=1 ,relx=0.9 ,x=-35 ,y=-25)

        self.inp_path.trace("w", lambda name, index, mode, sv=self.inp_path: self.entry_search_event(self.inp_path))

    def search(self): #binded to search button to start searching with given options
        file_path = self.inp_path.get()
        if not self.check_path(file_path) and not self.check_url(file_path):
            self.msg.config(text="Wrong path." ,fg="red")
            return

        if self.def_lib.get() == 0:
            # s_time = time.time()
            self.insert_text(self.out_email ,core.search(self.dfa_email ,self.text))
            # print(time.time() - s_time)

            self.insert_text(self.out_web ,core.search(self.dfa_web ,self.text))

            if self.sec_dep.get():
                self.insert_text(self.out_email
                                 ,core.search_sec_dep(self.dfa_email 
                                                    ,core.search(self.dfa_web ,self.text) ,
                                                    "dfa") 
                                 ,False)

        else:
            self.insert_text(self.out_email ,[email[0] for email in self.re_email.findall(self.text)])

            urls = [web[0] for web in self.re_web.findall(self.text)]
            self.insert_text(self.out_web ,urls)

            if self.sec_dep.get():
                self.insert_text(self.out_email 
                                ,core.search_sec_dep(self.re_email 
                                                    ,urls 
                                                    ,"re") 
                                ,False)

    def open(self): #opens filedialog for getting inpu file path
        file_path = filedialog.askopenfilename(title="Select file" ,filetypes=(("text files","*.txt") ,("html files","*.html") ,("all files","*.*")))
        self.inp_path.set(file_path)
        # self.check_path(file_path)
        if file_path:
            self.msg.config(text="File found." ,fg="green")

    def save(self): #binded to save menu bar for saving results in a file
        out_path = filedialog.asksaveasfilename(title="Save as" ,filetypes=(("text files" ,"*.txt") ,("all files" ,"*.*")))
        out_str = "Found Emails :\n" + self.out_email.get("1.0" ,tk.END) + "\r\nFound Web Addresses :\n" + self.out_web.get("1.0" ,tk.END)

        with open(out_path + ".txt" ,'w') as my_file:
            my_file.write(out_str)
        
    def check_path(self ,file_path): #checks given file path is valid or not
        self.text = ""
        try:
            with open(file_path ,'r' ,encoding='latin1') as my_file:
                self.text = my_file.read()
        except:
            return False

        if self.text:
            self.search_btn["state"] = "normal"
            self.msg.config(text="Text loaded." ,fg="green")
            return True
        else:
            self.msg.config(text="Wrong input." ,fg="red")
            return False

    def check_url(self ,url): #checks wether given url is valid or not
        try:
            res = core.get_response(url)
            if res:
                self.text = res.text
                self.msg.config(text="Text loaded." ,fg="green")
                return True
            else:
                self.msg.config(text="Error!" ,fg="red")
                return False
        except:
            return False

    def entry_search_event(self ,file_path): #an event trrigers when we have a charchter in input path and vice versa
        path = file_path.get()
        if path or self.text:
            self.search_btn["state"] = "normal"
        else:
            self.search_btn["state"] = "disable"

    def insert_text(self ,text_box ,text_list ,clear=True): #writes text from a given list to a text box on gui
        text_box["state"] = "normal"

        if clear:
            text_box.delete("0.1" ,tk.END)
            # for item in text_box.tag_names():
            #     text_box.tag_delete(item)

        for text in text_list:
            text_box.insert(tk.END ,text ,str(self.tag_id))
            text_box.insert(tk.END ,'\n')

            text_box.tag_bind(str(self.tag_id) ,"<Button-1>" ,lambda event ,i=self.tag_id ,text_b=text_box: self.on_click_event(text_b ,str(i)))
            text_box.tag_bind(str(self.tag_id) ,"<Enter>" ,lambda event ,i=self.tag_id ,text_b=text_box: self.enter_event(text_b ,i))
            text_box.tag_bind(str(self.tag_id) ,"<Leave>" ,lambda event ,i=self.tag_id ,text_b=text_box: self.leave_event(text_b ,i))

            self.tag_id += 1

        text_box["state"] = "disable"

    def clear(self): #clears all input and output stats
        self.def_lib.set(0)
        self.sec_dep.set(0)
        self.inp_path.set("")
        self.insert_text(self.out_email ,[] ,True)
        self.insert_text(self.out_web ,[] ,True)

    def enter_event(self ,text_box ,tag): #mouse enters on one of the results
        text_box.config(cursor="hand2")

        text_box.tag_config(str(tag) ,foreground="blue")
        fnt = font.Font(text_box ,text_box.cget("font"))
        fnt.configure(underline=True)
        text_box.tag_config(str(tag) ,font=fnt)

    def leave_event(self ,text_box ,tag): #mouse leaves the result
        text_box.config(cursor="arrow")

        text_box.tag_config(str(tag) ,foreground="black")
        fnt = font.Font(text_box, text_box.cget("font"))
        fnt.configure(underline=False)
        text_box.tag_config(str(tag) ,font=fnt)

    def on_click_event(self ,text_box ,tag): #clicking on one of the results
        text_box.tag_config(tag ,foreground="red")
        clicked_item = text_box.get(f"{tag}.first", f"{tag}.last")

        if text_box == self.out_web:
            webbrowser.open_new(clicked_item)
        elif text_box == self.out_email:
            webbrowser.open(f"mailto:?to={clicked_item}")
        else:
            self.msg.config(text="Error" ,fg="red")



if __name__=="__main__":
    App().mainloop() #main window of GUI(Parrent) waiting for events

