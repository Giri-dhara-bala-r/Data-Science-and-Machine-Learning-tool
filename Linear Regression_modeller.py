#!/usr/bin/env python
# coding: utf-8

# In[1]:



from tkinter import *
import ttkbootstrap as tb
from tkinter import messagebox
from ttkbootstrap.tableview import Tableview
from tkinter.filedialog import askopenfilename
from ttkbootstrap.constants import *
import pymysql as sql
import pandas as pd
import numpy as np
import time
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error,accuracy_score,r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


App= tb.Window(themename='darkly')
App.title('Linear regression Application')
#App.iconbitmap('Icon.ico')
App.state('zoomed')
App.resizable(False,False)

user_name = StringVar()
pass_word = StringVar()
cnf_pass_word= StringVar()
sp_pass_word= StringVar()
sp_user_name = StringVar()
sp_name= StringVar()
directory = StringVar()

def login_layout():
    global login_frame,user_name,pass_word,name,pword
    cl_window()
    login_frame = tb.LabelFrame(App,text="Login",borderwidth=20,relief='solid',bootstyle='info')
    login_frame.place(relx=0.35,rely=0.28)
    login_frame.columnconfigure((0,1),weight=1,uniform='a')
    login_frame.rowconfigure((0,1,2,3,4),weight=1,uniform='a')
    user_label = tb.Label(login_frame, text="USERNAME",font=("Times New Roman", 12,"bold"),bootstyle='info')
    user_label.grid(column=0, row=1,sticky='e',padx=20,pady=5)
    name = tb.Entry(login_frame, textvariable=user_name,width=20, font=('TimesNewRoman 11'),bootstyle="info")
    name.grid(column=1, row=1,sticky='w',padx=20,pady=5)
    pass_label = tb.Label(login_frame, text="PASSWORD",font=("Times New Roman", 12,"bold"),bootstyle='info')
    pass_label.grid(column=0, row=2,sticky='e',padx=20,pady=5)
    pword = tb.Entry(login_frame, textvariable=pass_word,show="*",width=20, font=('TimesNewRoman 11 bold'),bootstyle="info")
    pword.grid(column=1, row=2,sticky='w',padx=20,pady=5)
    
    if name.get()!='abc@gmail.com':
        name.insert(0,"abc@gmail.com")
        pword.insert(0,"********")
        pword.bind("<FocusIn>",lambda d:pword.delete('0','end')) if name.get()=='abc@gmail.com' else None
        name.bind("<FocusIn>",lambda d:name.delete('0','end')) if pword.get()=="********" else None
    success_style = tb.Style()
    success_style.configure('success.TButton',font=("Times New Roman", 12,"bold"),width=20)
    successO_style=tb.Style()
    successO_style.configure('success.Outline.TButton',font=("Times New Roman", 12,"bold"),width=20)
    sign_in = tb.Button(login_frame, text='SIGN IN', width=10,command=signin,bootstyle="success",style='success_style')
    sign_in.grid(column=1, row=3,sticky='sw',padx=20,pady=10)
    sign_up = tb.Button(login_frame, text='SIGN UP', width=10,command=signup,bootstyle="success-outline",style="success.Outline.TButton")
    sign_up.grid(column=0, row=3,sticky='se',padx=20,pady=10)
    quit =tb.Button(App, text=' Quit ', width=10,command=App.destroy,bootstyle='danger')
    quit.place(relx=0.92,rely=0)
    
def connect_db():
    global connection,db,table_name,db_name
    table_name = 'login_credentials'
    db_name = 'User_details'
    connection = sql.connect(host='localhost', user='root', port=3306, password='Giri@021103')
    db = connection.cursor()
    db.execute("create database if not exists %s" % (db_name))
    db.execute("use %s" % (db_name))
    db.execute("create table if not exists %s (update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, Name varchar(500), UserName varchar(500), PassWord varchar(20),constraint user_primary primary key(UserName))" % (table_name))
    connection.commit()
    
def disconnect_db():
    global connection,db,table_name,db_name
    connection.commit()
    db.close()
    connection.close()

def signin():
    global user_name,pass_word,name,pword,good_name
    user_name,pass_word=name.get(),pword.get()
    user_name=user_name.lower()
    pass_word=pass_word.lower()
    b=''
    connect_db()
    if user_name != 'abc@gmail.com' and pass_word != "********" :
        if '@gmail.com' in user_name:
            db.execute("select * from %s where UserName = '%s'"%(table_name,user_name.lower()))
            a=db.fetchall()
            try:
                if user_name == a[0][2] and pass_word == a[0][3]:
                    good_name=a[0][1]
                    sucess= messagebox.showinfo(title='Login Sucessful', message="You are good to go!!")
                    if sucess =='ok':
                        auth_window()
                else:
                    b=messagebox.showwarning(title='Username Error', message='Kindly Check your User Name and Password')
            except:
                b=messagebox.showwarning(title='Username Error', message='User Name Does not exists !!')
        else:
            b=messagebox.showwarning(title='Username Error', message='User Name should be your mail id')  
    else:
        b=messagebox.showwarning(title='Error', message='Kindly Check your Credentials')
    if b=='ok':
        login_layout()
    disconnect_db()
    
def signup():
    global user_name,cnf_pass_word,sp_pass_word,sp_user_name,sp_name,cp_word,p_word,u_name,f_name,success_style
    cl_window()
    
    signup_frame= tb.LabelFrame(App,text='Sign Up',borderwidth=20,relief='solid',bootstyle='info')
    signup_frame.place(relx=0.35,rely=0.25)
    signup_frame.columnconfigure((0,1),weight=1,uniform='a')
    signup_frame.rowconfigure((0,1,2,3,4,5,6),weight=1,uniform='a')
    back = tb.Button(App, text='<< Go Back', width=10,command=login_layout,bootstyle='warning')
    back.place(relx=0,rely=0)
    quit = tb.Button(App, text=' Quit ', width=10,command=App.destroy,bootstyle='danger')
    quit.place(relx=0.92,rely=0)
    
    name_label =tb.Label(signup_frame, text="NAME", font=("Times New Roman", 12,"bold"),bootstyle='info')
    name_label.grid(column=0, row=1,sticky='e',padx=20,pady=5) 
    f_name = tb.Entry(signup_frame, textvariable=sp_name, font=('TimesNewRoman 11'),bootstyle="info")
    f_name.grid(column=1, row=1,sticky='w',padx=20,pady=5)
    user_label = tb.Label(signup_frame, text="USERNAME", font=("Times New Roman", 12,"bold"),bootstyle='info')
    user_label.grid(column=0, row=2,sticky='e',padx=20,pady=5)
    u_name = tb.Entry(signup_frame, textvariable=sp_user_name, font=('TimesNewRoman 11'),bootstyle="info")
    u_name.grid(column=1, row=2,sticky='w',padx=20,pady=5)
    pass_label = tb.Label(signup_frame, text="PASSWORD",font=("Times New Roman", 12,"bold"),bootstyle='info')
    pass_label.grid(column=0, row=3,sticky='e',padx=20,pady=5)
    p_word = tb.Entry(signup_frame, textvariable=sp_pass_word, font=('TimesNewRoman 11'),bootstyle="info")
    p_word.grid(column=1, row=3,sticky='w',padx=20,pady=5)
    cp_label = tb.Label(signup_frame, text="RE-ENTER PASSWORD",font=("Times New Roman", 12,"bold"),bootstyle='info')
    cp_label.grid(column=0, row=4,sticky='e',padx=20,pady=5)
    cp_word = tb.Entry(signup_frame, textvariable=cnf_pass_word, font=('TimesNewRoman 11'),bootstyle="info")
    cp_word.grid(column=1, row=4,sticky='w',padx=20,pady=5)
    success_style = tb.Style()
    success_style.configure('success.TButton',font=("Times New Roman", 12,"bold"),width=20)    
    done = tb.Button(signup_frame, text='SIGN UP',width=10,command=gettodb,bootstyle="success",style='success_style')
    done.grid(column=0, row=5,columnspan=2,padx=20,pady=5)
    
    if f_name.get()!= 'Your Name':
        f_name.insert(0,'Your Name')
        f_name.bind("<FocusIn>",lambda d:f_name.delete('0','end'))
    if u_name.get()!='abc@gmail.com':
        u_name.insert(0,'abc@gmail.com')
        u_name.bind("<FocusIn>",lambda d:u_name.delete('0','end'))
    if p_word.get!='Create password':
        p_word.insert(0,'Create password')
        p_word.bind("<FocusIn>",lambda d:p_word.delete('0','end'))
    if cp_word.get()!='Confirm Password':
        cp_word.insert(0,'Confirm Password')
        cp_word.bind("<FocusIn>",lambda d:cp_word.delete('0','end'))

def gettodb():
    global connection,db,table_name,db_name,user_name,cnf_pass_word,sp_pass_word,sp_user_name,sp_name,cp_word,p_word,u_name,f_name
    connect_db()
    
    cnf_pass_word=cp_word.get().lower()
    sp_pass_word=p_word.get().lower()
    sp_user_name= u_name.get().lower()
    sp_name= f_name.get().lower()
    b=''
    if sp_name != 'Your Name' and sp_user_name !='abc@gmail.com' and cnf_pass_word != '********':
        if cnf_pass_word == sp_pass_word:
            if '@gmail.com'in sp_user_name:
                if len(sp_name) >0:
                    try:
                        db.execute('insert into %s (Name,UserName,PassWord) values ("%s","%s","%s")'%(table_name,sp_name,sp_user_name,cnf_pass_word))
                        a = messagebox.showinfo(title='Sucess!!', message='Your Details Recorded Sucessfully !!')
                        if a =='ok':
                            login_layout()
                    except:
                        b=messagebox.showwarning(title='Error', message='Username already exists!!')
                else:
                    b= messagebox.showwarning(title='Name Error', message='Name field cannot be empty')
            else:
                b=messagebox.showwarning(title='Username Error', message='Give valid username')
        else:
            b=messagebox.showwarning(title='Password Error', message="Re-enter Password and Password doesn't match")
    else:
        b=messagebox.showwarning(title='Error', message='Kindly Provide valid info')
    disconnect_db()   
    if b=='ok':
        cl_window()
        signup()

def cl_window():
    for widget in App.winfo_children():
        widget.destroy()

def auth_topbar():
    global good_name
    top_bar= tb.LabelFrame(App,relief='flat',bootstyle="default")
    top_bar.columnconfigure((0,1,2,3),weight=1,uniform='a')
    top_bar.rowconfigure((0),weight=1,uniform='a')
    
    #top_bar.grid(row=0,column=0,padx=10,sticky='nw')
    top_bar.place(relx=0,rely=0)
    welcome_label = tb.Label(top_bar, text='Welcome, %s!' % (good_name.capitalize().split()[0]), font=("arial", 15, "bold", "underline"),bootstyle='info')
    welcome_label.pack(side='left',padx=20)
    #welcome_label.grid(row=0,column=1,padx=20)
    log_out_button = tb.Button(top_bar, text='Log Out',width=10, command=logout,bootstyle='warning-outline')
    log_out_button.pack(side='left',padx=20)
    #log_out_button.grid(row=0,column=1,padx=20)
    quit =tb.Button(App, text=' Quit ', width=10,command=App.destroy,bootstyle='danger')
    quit.place(relx=0.954,rely=0)
    #quit.grid(row=0,column=3,sticky='ne')
    
'''    
def auth_window():
    cl_window()
    file_frame = tb.LabelFrame(App, text='File',borderwidth=5,bootstyle="info")
    file_frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1,uniform='a')
    file_frame.rowconfigure((0),weight=1,uniform='a')
    #file_frame.grid(column=0, row=1, columnspan=4, padx=10, pady=10,sticky='sw')
    file_frame.place(relx=0.01,rely=0.07)
    file_en = tb.Entry(file_frame, textvariable=directory, width=150,bootstyle='info')
    file_en.grid(column=0, row=0, padx=10, pady=10, columnspan=9, sticky="w")
    file_button = tb.Button(file_frame, text='Browse',bootstyle='info-outline',command=on_browse)
    file_button.grid(column=9, row=0,sticky='w')
    done_button =tb.Button(file_frame, text='Confirm Selection',width=15,bootstyle='success-outline',command=confirm_selection())
    done_button.grid(column=10, row=0)
    auth_topbar()
'''    
    
def auth_window():
    cl_window()
    auth_topbar()
    file_frame = tb.LabelFrame(App, text='File', borderwidth=5, bootstyle="info")
    file_frame.place(relx=0.01, rely=0.07)

    file_en = tb.Entry(file_frame, textvariable=directory, width=150, bootstyle='info')
    file_en.grid(column=0, row=0, padx=10, pady=10, columnspan=8, sticky="w")

    file_button = tb.Button(file_frame, text='Browse', bootstyle='info-outline', command=on_browse)
    file_button.grid(column=9, row=0, sticky='w')

    cnf_sel = tb.Button(file_frame, text='Confirm Selection', width=15, bootstyle='success-outline', command=confirm_selection)
    cnf_sel.grid(column=10, row=0)


def on_browse():
    file_path = askopenfilename(title="Select a file")
    if file_path:
        directory.set(file_path)
def get_data():
    global tx_dir,load,col_name,df
    #load=tb.Progressbar(bootstyle="danger-striped")
    if tx_dir.split('.')[1] == "csv":
        df=pd.read_csv(directory.get(),encoding = "utf-8")
    else:
        df=pd.read_excel(directory.get())
        
    col_name= []
    #val_lst=[]
    for i in range(len(df.columns)):
        col_name.append(df.columns[i])
    row_dt=[]
    for i in df.values:
        row_dt.append(i)
    colors = App.style.colors
    table= Tableview(App,coldata=col_name,rowdata=row_dt,searchable=True,paginated=True,bootstyle='info',stripecolor=(colors.secondary, None),pagesize=35,height=35)
    #table.place(relx=0.1,rely=0.2)
    #table.grid(column=1,row=3)
    table.place(relx=0.01,rely=0.15,relwidth=0.5)
    #for i in df.values:
    #    table.insert_row('end', i)
    load.destroy()
    
def confirm_selection():
    global directory,df,tx_dir,load,col_name,success_style,sel_alg,sel_x,sel_y,sel_pane
    cl_window()
    load=tb.Progressbar(App,maximum=100,length=300,value=0, bootstyle="danger-striped")
    load.place(relx=0.0,rely=0.95)
    load.start()
    auth_topbar()
    tx_dir = directory.get().split('/')[-1]
    data_label = tb.Label(App, text='You have selected %s Dataset..!'%(tx_dir.split('.')[0].capitalize()),font=("arial", 12, "bold"), bootstyle='info')
    data_label.place(relx=0,rely=0.1)
    sep_h= tb.Separator(orient='horizontal',bootstyle="info")
    sep_h.place(relx=0,rely=0.128,relwidth=1)
    get_data()
    sep_v= tb.Separator(orient='vertical',bootstyle="info")
    sep_v.place(relx=0.53,rely=0.128,relheight=0.872)
    sel_pane=tb.LabelFrame(App, text='Selection Pane', borderwidth=5, bootstyle="info")
    sel_pane.place(relx=0.55, rely=0.15)
    sel_pane.columnconfigure((0,1),weight=1,uniform='a')
    sel_pane.rowconfigure((0,1,2,3),weight=1,uniform='a')
    
    lab_alg=tb.Label(sel_pane, text="ALGORITHM", font=("Times New Roman", 12,"bold"),bootstyle='info')
    lab_alg.grid(column=0, row=0,sticky='e',padx=20,pady=5)
    lab_x=tb.Label(sel_pane, text="Select X", font=("Times New Roman", 12,"bold"),bootstyle='info')
    lab_x.grid(column=0, row=1,sticky='e',padx=20,pady=5)
    lab_y=tb.Label(sel_pane, text="Select Y", font=("Times New Roman", 12,"bold"),bootstyle='info')
    lab_y.grid(column=0, row=2,sticky='e',padx=20,pady=5)
    sel_alg= tb.Combobox(sel_pane,bootstyle="Success")
    sel_alg.insert('end', 'Linear Regression')
    sel_alg.grid(column=1, row=0,sticky='e',padx=20,pady=5)
    sel_x=tb.Combobox(sel_pane,bootstyle="info",values=col_name)
    sel_x.grid(column=1, row=1,sticky='e',padx=20,pady=5)
    sel_y=tb.Combobox(sel_pane,bootstyle="info",values=col_name)
    sel_y.grid(column=1, row=2,sticky='e',padx=20,pady=5)
    
    cnf_sel=tb.Button(sel_pane, text='GET METRICS',width=15,command=get_metrics,bootstyle="success",style='success_style')
    cnf_sel.grid(column=0, row=3,columnspan=2,padx=20,pady=5)
    
def get_metrics():
    global sel_alg,sel_x,sel_y,df,sel_pane
    alg=sel_alg.get()
    x_val=sel_x.get()
    y_val=sel_y.get()
    sel_pane.destroy()
    y = df[x_val]
    X = df[[y_val]]
    
    X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.7, random_state=2529)
    
    model = LinearRegression()
    model.fit(X_train,y_train)
    
    inp = model.intercept_
    cof = model.coef_
    y_pred = model.predict(X_test)
    mape= mean_absolute_percentage_error(y_test,y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    accuracy = model.score(X_test, y_test)
    
    print(f'{inp}\n{cof}\n{mape}\n{mae}\n{mse}\n{accuracy}')
    metrics_pane=tb.LabelFrame(App, text='METRICS', borderwidth=5, bootstyle="info")
    metrics_pane.place(relx=0.55, rely=0.75)
    
    lab_inp=tb.Label(metrics_pane, text=f"Intercept : {inp}", font=("Times New Roman", 12,"bold"),bootstyle='info')
    lab_inp.grid(column=0, row=0,sticky='w',padx=20,pady=5)
    lab_cof=tb.Label(metrics_pane, text=f"Coeffcient : {cof}", font=("Times New Roman", 12,"bold"),bootstyle='info')
    lab_cof.grid(column=0, row=1,sticky='w',padx=20,pady=5)
    lab_acc=tb.Label(metrics_pane, text=f"Accuracy : {accuracy}", font=("Times New Roman", 12,"bold"),bootstyle='info')
    lab_acc.grid(column=0, row=2,sticky='w',padx=20,pady=5)
    #sel_alg= tb.Combobox(sel_pane,bootstyle="Success")
    #sel_alg.insert('end', 'Linear Regression')
    #sel_alg.grid(column=1, row=0,sticky='e',padx=20,pady=5)
    #sel_x=tb.Combobox(sel_pane,bootstyle="info",values=col_name)
    #sel_x.grid(column=1, row=1,sticky='e',padx=20,pady=5)
    #sel_y=tb.Combobox(sel_pane,bootstyle="info",values=col_name)
    #sel_y.grid(column=1, row=2,sticky='e',padx=20,pady=5)
    
    
    
    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue', label='Actual')
    ax.plot(X_test, y_pred, color='red', label='Predicted')
    ax.set_xlabel(x_val)
    ax.set_ylabel(y_val)
    ax.set_title('Prediction')
    ax.legend()

    # Embedding plot into tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=App)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.55, rely=0.15)
    
def logout():
    global user_name,pass_word
    qm = messagebox.askquestion(title='Log Out', message='Do you want to Log Out')
    if qm == 'yes':
        user_name=''
        pass_word=''
        login_layout()
#directory=r'D:/Academics/BESANT/Datasets/diabetes.csv'
#good_name='Giri'
#auth_window()        
login_layout()
#confirm_selection()
App.mainloop()

