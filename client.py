# if message == "NICK":
#               self.sock.send(self.nickname.encode('utf-8'))


import socket 
import threading
import tkinter 
import tkinter.scrolledtext
from tkinter import *
import sqlite3 
import os

HOST = "127.0.0.1"
# HOST = "0.0.0.0"
PORT = 9000

# We create a client which has a socket , The socket connects to Host and port 
# The client takes nickname fro the dialog box 
# We say gui is still not done and the connection is running 
# The we run two threads on eto build gui and other to deal with the server

path=os.getcwd()

def handle_email(client_email,rand):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    from random import randint
    from time import sleep

    def send_mail(fromaddr, frompasswd, toaddr, msg_subject, msg_body):
        try:
            msg = MIMEMultipart()
            print("[+] Message Object Created")
        except:
            print("[-] Error in Creating Message Object")
            return

        msg['From'] = fromaddr

        msg['To'] = toaddr

        msg['Subject'] = msg_subject

        body = msg_body

        msg.attach(MIMEText(body, 'plain'))
        
        # p = MIMEBase('application', 'octet-stream')

        # encoders.encode_base64(p)

        # try:
        #     msg.attach(p)
        #     print("[+] File Attached")
        # except:
        #     print("[-] Error in Attaching file")
        #     return

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # s = smtplib.SMTP('mail.iitp.ac.in', 587)
            print("[+] SMTP Session Created")
        except:
            print("[-] Error in creating SMTP session")
            return

        s.starttls()

        try:
            s.login(fromaddr, frompasswd)
            print("[+] Login Successful")
        except:
            print("[-] Login Failed")
        text = msg.as_string()

        # try:
        s.sendmail(fromaddr, toaddr, text)
        print("[+] Mail Sent successfully")
        # except:
        #     print('[-] Mail not sent')

        s.quit()

    def isEmail(x):
        # if ('@' in x) and ('.' in x):
            return True
        # else:
        #     return False

    FROM_ADDR = "adityaramdaspatil@gmail.com" #email address can be changed
    FROM_PASSWD = "zbht hbqb ztwm zxex"

    

    Subject = "password reset"
    Body ='''
    enter this activation code
    '''+str(rand)
    from datetime import datetime

    start_time = datetime.now()

    #what a ever is the limit of your sending mails, like gmail has 500.
    max_count = 9999999
    count=0
    # try:
    if isEmail(client_email) and count <=max_count:
        count+=1
        send_mail(FROM_ADDR, FROM_PASSWD, client_email, Subject, Body)
    print("Count Value: ", count)
    print("Sleeping . .. . ")
    sleep(randint(1,3))
    # except:
    #     print("Lets see ")

    print("Count Max is reached: " ,count)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

class Client:
    
    # self.gui_done, self.running ,  self.win ,  self.sock
    
    
    def __init__(self , host , port):
        
        # msg = tkinter.Tk()
        # msg.withdraw()
        # self.nickname = simpledialog.askstring("Nickname" , "Please Choose a nickname", parent = msg)
        
        # The entire SignUp Login GUI 
        import time
        self.last_presstime  = 0
        
        self.nickname  = " "
        #create an object to create a window
        window = Tk()
        
        #Actions on Pressing Login Button
        def login():
            window.destroy()  #closes the previous window
            login_window = Tk() #creates a new window for loging in
            login_window.title("LogIn")  #set title to the window
            login_window.geometry("800x500")  #set dimensions to the window
            
            from PIL import Image, ImageTk
            # Read the Image and resize using PIL
            home_image= Image.open(path+"\\home.png")
            resize_home_image = home_image.resize((2000, 1000))
            
            # #Convert image into button 
            # login_image= PhotoImage("G:\\Chat Software Using python\\login.png")
            # # resize_login_image = login_image.resize((2000, 1000))
            # signup_image= PhotoImage("G:\\Chat Software Using python\\signup.png")
            # # resize_signup_image = signup_image.resize((2000, 1000))
            
            img = ImageTk.PhotoImage(resize_home_image)
            
            # create label and add resize image
            label = Label(image=img)
            label.image = img
            label.pack()
        
            def login_database():
                conn = sqlite3.connect("1.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM test WHERE email=? AND password=?",(e1.get(),e2.get()))
                row=cur.fetchall()
                conn.commit()
                cur.close()
                print(row)
                if row!=[]:
                    login_window.destroy()
                    user_name=row[0][1]
                    # l3.config(text="user name found with name: "+user_name)
                    # This is the place from where the user will get logged in and will see the signup window further
                    self.nickname  = user_name
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((host, port))
                    self.afterLogInActivity()
                    
                else:
                    l3.config(text="user not found")

            #add 2 Labels to the window
            l1 = Label(login_window,text="email: ",font="times 23")
            l1.place(x = 340,y = 200) 
            l2 = Label(login_window,text="Password: ",font="times 23")
            l2.place(x = 340,y = 260) 
            l3 = Label(login_window,font="times 23") 
            l3.place(x = 390,y = 389)

            #creating 2 adjacent text entries
            email_text = StringVar() #stores string
            e1 = Entry(login_window,textvariable=email_text, font= "times20")
            e1.place(x = 500,y = 209)

            password_text = StringVar()
            e2 = Entry(login_window,textvariable=password_text,show='*', font= "times20")
            e2.place(x = 500,y = 269)

            #create 1 button to login
            b = Button(login_window,text="login",width=13,command=login_database, font= "times20")
            b.place(x = 420,y = 329)

            #create 1 button to reset
            # b2 = Button(login_window,text="reset",width=13,command=lambda:pass_reset(e1.get()))
            # b2.place(x = 620,y = 329)

            login_window.mainloop()

        #Actions on Pressing Signup button
        def signup():
            #Database action on pressing signup button
            def signup_database():
                conn = sqlite3.connect("1.db") #create an object to call sqlite3 module & connect to a database 1.db
                #once you have a connection, you can create a cursor object and call its execute() method to perform SQL commands
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS test([id] INTEGER PRIMARY KEY,[name] text,[email] text,[password] text)")
                cur.execute("INSERT INTO test Values(Null,?,?,?)",(e1.get(),e2.get(),e3.get()))
                
                #execute message after account successfully created
                l4 = Label(signup_window,text="account created",font="times 15")
                l4.place(x = 420,y = 449)
                
                conn.commit()  #save the changes 
                cur.close() #close the connection

            window.destroy()  #closes the previous window
            signup_window = Tk() #creates a new window for signup process
            signup_window.geometry("800x500") #dimensions for new window
            signup_window.title("Sign Up") #title for the window
            
            from PIL import Image, ImageTk
            # Read the Image and resize using PIL
            home_image= Image.open(path+"\\home.png")
            resize_home_image = home_image.resize((2000, 1000))
            
            # #Convert image into button 
            # login_image= PhotoImage("G:\\Chat Software Using python\\login.png")
            # # resize_login_image = login_image.resize((2000, 1000))
            # signup_image= PhotoImage("G:\\Chat Software Using python\\signup.png")
            # # resize_signup_image = signup_image.resize((2000, 1000))
            
            img = ImageTk.PhotoImage(resize_home_image)
            
            # create label and add resize image
            label = Label(image=img)
            label.image = img
            label.pack()
            
            #create 3 Labels
            l1 = Label(signup_window,text="User Name: ",font="times 20")
            l1.place(x = 340,y = 209)

            l2 = Label(signup_window,text="User email: ",font="times 20")
            l2.place(x = 340,y = 269)

            l3 = Label(signup_window,text="Password: ",font="times 20")
            l3.place(x = 340,y = 329)
            #create 3 adjacent text entries
            name_text = StringVar() #declaring string variable for storing name and password
            e1 = Entry(signup_window,textvariable=name_text,font="times 20")
            e1.place(x = 500,y = 209)

            email_text = StringVar()
            e2 = Entry(signup_window,textvariable=email_text,font="times 20")
            e2.place(x = 500,y = 269)

            password_text = StringVar()
            e3 = Entry(signup_window,textvariable=password_text,show='*',font="times 20")
            e3.place(x = 500,y = 329)

            #create 1 button to signup
            b1 = Button(signup_window,text="signup",width=20,command=signup_database, font="times 15")
            b1.place(x = 420,y = 389)

            signup_window.mainloop()
  
        #Actions on Pressing Reset button
        def reset():

                window.destroy()  #closes the previous window
                reset_window = Tk() #creates a new window for loging in
                reset_window.title("Reset Password")  #set title to the window
                reset_window.geometry("800x500")  #set dimensions to the window
                from PIL import Image, ImageTk
                # Read the Image and resize using PIL
                home_image= Image.open(path+"\\home.png")
                resize_home_image = home_image.resize((2000, 1000))
                
                # #Convert image into button 
                # login_image= PhotoImage("G:\\Chat Software Using python\\login.png")
                # # resize_login_image = login_image.resize((2000, 1000))
                # signup_image= PhotoImage("G:\\Chat Software Using python\\signup.png")
                # # resize_signup_image = signup_image.resize((2000, 1000))
                
                img = ImageTk.PhotoImage(resize_home_image)
            
                # create label and add resize image
                label = Label(image=img)
                label.image = img
                label.pack()
                
                
                def pass_reset(new_pass,cnf_pass,client_email,code_text,rand,reset_window):
                    
                    if(code_text != rand):
                        l1 = Label(reset_window,text="         Wrong OTP             ",font="times 25")
                        l1.place(x = 420,y = 435) 
                    elif (code_text==rand):
                        if(new_pass == cnf_pass):
                            conn = sqlite3.connect("1.db") #create an object to call sqlite3 module & connect to a database 1.db
                            #once you have a connection, you can create a cursor object and call its execute() method to perform SQL commands
                            cur = conn.cursor()
                            # cur.execute("UPDATE test set password_text ="+new_pass+" where email_text ="+str(client_email))
                            sql_update_query = """Update test set password = ? where email = ?"""
                            data = (new_pass, client_email)
                            cur.execute(sql_update_query, data)
                            # save the changes
                            conn.commit()
                            cur.close()
                            l1 = Label(reset_window,text="Password reset successfull",font="times 25")
                            l1.place(x = 420,y = 435) 
                        else:
                            l4 = Label(reset_window,text="Password did not Match",font="times 25")
                            l4.place(x = 420,y = 435) 
                        
                        
                def reset_through_email(client_email):
                    conn = sqlite3.connect("1.db")
                    cur = conn.cursor()
                    print(client_email)
                    cur.execute("SELECT * FROM test WHERE email=?",(client_email,))
                    row=cur.fetchall()
                    conn.commit()
                    cur.close()
                    print(row)
                    
                    
                    #checks if email is present in db
                    if row != []:
                        from random import randint
                        rand=randint(1000,9999)
                        reset_window.destroy()
                        handle_email(client_email,rand)
                        # if email is sent open a new reset window 
                        reset_window2 = Tk() #creates a new window for loging in
                        reset_window2.title("Reset Password")  #set title to the window
                        reset_window2.geometry("800x500")  #set dimensions to the window
                        from PIL import Image, ImageTk
                        # Read the Image and resize using PIL
                        home_image= Image.open(path+"\\home.png")
                        resize_home_image = home_image.resize((2000, 1000))
                        
                        # #Convert image into button 
                        # login_image= PhotoImage("G:\\Chat Software Using python\\login.png")
                        # # resize_login_image = login_image.resize((2000, 1000))
                        # signup_image= PhotoImage("G:\\Chat Software Using python\\signup.png")
                        # # resize_signup_image = signup_image.resize((2000, 1000))
                        
                        img = ImageTk.PhotoImage(resize_home_image)
                    
                        # create label and add resize image
                        label = Label(image=img)
                        label.image = img
                        label.pack()
                        #add Label to the window
                        l1 = Label(reset_window2,text="OTP ",font="times 20",bg="#CCCCCC")
                        l1.place(x =50,y = 260) 
                        #creating adjacent text entries
                        code_text = StringVar() #stores string
                        e1 = Entry(reset_window2,textvariable=code_text,width=20,font="times 20",bg="#CCCCCC")
                        e1.place(x = 450,y = 260)
                        l2 = Label(reset_window2,text="New Password: ",font="times 20",bg="#CCCCCC")
                        l2.place(x = 50,y = 320) 
                        #creating adjacent text entries
                        new_pass = StringVar() #stores string
                        e2 = Entry(reset_window2,textvariable=new_pass,width=20,font="times 20",bg="#CCCCCC")
                        e2.place(x = 450,y = 320)

                        l3 = Label(reset_window2,text="Confirm Password: ",font="times 20",bg="#CCCCCC")
                        l3.place(x = 50,y = 380) 
                        #creating adjacent text entries
                        cnf_pass = StringVar() #stores string
                        e3 = Entry(reset_window2,textvariable=cnf_pass,width=20,font="times 20",bg="#CCCCCC")
                        e3.place(x = 450,y = 380)
                        # create 1 button to reset pass
                        b = Button(reset_window2,text="Reset Password",bg="#CCCCCC",font="times 15",width=13,command=lambda:pass_reset(e2.get(),e3.get(),client_email,e1.get(),str(rand),reset_window2))
                        b.place(x = 250,y = 440)
                    else:
                        reset_window.destroy()
                        reset_window2 = Tk() #creates a new window for loging in
                        reset_window2.title("Reset Password")  #set title to the window
                        reset_window2.geometry("800x500")  #
                        reset_window2.configure(bg="#FF0000")
                        l1 = Label(reset_window2,text="Your Email is not registered",font="times 20")
                        l1.place(x = 250,y = 260) 

                
                #add Label to the window
                l1 = Label(reset_window,text="email: ",font="times 23",bg="#CCCCCC")
                l1.place(x = 340,y = 300) 
                #creating adjacent text entries
                email_text = StringVar() #stores string
                e1 = Entry(reset_window,textvariable=email_text,width=20,font="times 20",bg="#CCCCCC")
                e1.place(x = 500,y = 300)

                # create 1 button to reset pass
                b = Button(reset_window,text="get email",bg="#CCCCCC",width=13,font="times15",command=lambda:reset_through_email(e1.get()))
                b.place(x = 500,y = 400)
                
                reset_window.mainloop()     
                
        #main window code and driver code
        #give dimensions to the window
        window.geometry("800x500")
        #add title to the window
        window.title("Login and Signup system")
        
        from PIL import Image, ImageTk
        # Read the Image and resize using PIL
        home_image= Image.open(path+"\\home.png")
        resize_home_image = home_image.resize((2000, 1000))
        
        img = ImageTk.PhotoImage(resize_home_image)
        
        # create label and add resize image
        label = Label(image=img)
        label.image = img
        label.pack()
        # ,bg="#04aa6d"
        label1 = Label(window, text="Register Here!",font="times 30",bg="#04aa6d").place(x = 540,y = 150) 
        
        #adding 3 buttons - login and signup and reset
        button1 = Button(window,text="Login",width=10,font="times15",command=login,bg="#04aa6d", borderwidth = 2).place(x = 300,y = 360)

        button2 = Button(window,text="Signup",width=10,font="times15",command=signup,bg="#04aa6d", borderwidth = 2).place(x = 440,y = 360)

        button3 = Button(window,text="Reset Password",width=20,font="times15",command=reset,bg="#04aa6d", borderwidth = 2).place(x = 580,y = 360)
        
        
        
        window.mainloop()
     
    def afterLogInActivity(self):
        
        # The below two threads will run simultaneously
        self.gui_done = False
        self.running  = True 

        self.sock.send(self.nickname.encode('utf-8'))
        
        gui_thread = threading.Thread(target = self.gui_loop )
        receive_thread = threading.Thread(target = self.receive )
        
        gui_thread.start()
        receive_thread.start()
        
        gui_thread.join()
        receive_thread.join()
        
    def gui_loop(self):
        def browseFiles():
            from tkinter import filedialog as fd
            
            root = Tk()
            root.withdraw()
            filepath = fd.askopenfilename(parent=root)
            
            print(filepath)
            file_size = os.path.getsize(filepath)
            with open(filepath, "rb") as file:
                c = 0
                filedata=''
                # Running loop while c != file_size.
                while c <= file_size:
                    data = file.read(1024)
                    if not (data):
                        break
                    try:
                        # self.sock.sendall(data)
                        print(data)                        
                        c += len(data)
                        filedata=filedata+data.decode('utf-8')
                        # message = f"{self.nickname} : {data.decode('utf-8')}"
                        # self.sock.send(message.encode('utf-8'))
                        # message = str(self.sock.recv(1024).decode('utf-8'))
                    except:
                        print("some error in sending file")
                        break
                message = '#'+f"{self.nickname} : {filedata}"
                self.sock.send(message.encode('utf-8'))       
                
            # file = open(filepath , "rb")
            # data = file.read()
            
            # self.sock.sendall(data)
            

         # The entire gui of the chat window is written here 
        self.win = tkinter.Tk()  #  `defined a tkinter window for self here 
        self.win.configure(bg ="#171717")
        
        self.chat_label = tkinter.Label(self.win, text = "Chat: " ,bg = "lightgray")
        self.chat_label.config(font= ("Arial", 12))
        self.chat_label.pack(padx = 20, pady = 5)
        
        
        self.who_typing = tkinter.scrolledtext.ScrolledText(self.win , bg = "#90EE90",width= 80, height = 2)
        self.who_typing.pack(padx = 20, pady = 5)
        # self.who_typing.configure(state ='disabled')
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win , bg = "lightgray")
        self.text_area.pack(padx = 20, pady = 5)
        self.text_area.configure(state ='disabled')
        
        self.msg_label = tkinter.Label(self.win, text = "Message: " ,bg = "lightgray")
        self.msg_label.config(font= ("Arial", 12))
        self.msg_label.pack(padx = 20, pady = 5)
        
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.typing_indicator_callback(sv))
        self.input_area = tkinter.Entry(width=100, textvariable=sv,font="times 20",bg="#CCCCCC")
        self.input_area.pack(side=tkinter.LEFT, padx=10)
        self.input_area.pack()
        
        # self.input_area = tkinter.Text(self.win , height = 3, bg = "#CD950C")  
        # self.input_area.pack(padx = 20, pady = 5)
            
        # Send Message operation
        self.send_button = tkinter.Button(self.win, text ="Send" , command = self.write, bg = "#00FF00")
        self.send_button.config(font= ("Arial", 12))
        self.send_button.pack(padx = 20, pady = 5)
        
        # Attach File Operation
        self.attach_button = tkinter.Button(self.win, text ="Attach" , command = browseFiles, bg ="#CD3278")
        self.attach_button.config(font= ("Arial", 12))
        self.attach_button.pack(padx = 20, pady = 5)
        
        # Typing Operation when self.win window is open
        # t1 = threading.Thread(target=self.typing,args=(Event,))
        # t2 = threading.Thread(target=self.nottyping,args=(Event,))
        
        # import time
        
        # self.win.bind("<KeyPress>",self.typing)
        # if(time.time() - self.last_presstime >= 20):
        #     print('executing')
        #     self.nottyping()
            
        # self.win.bind("<KeyRelease>",t2.start())
        
        # self.win.bind("<KeyPress>",self.typing)
        # self.win.bind("<KeyRelease>",self.nottyping)

        self.gui_done = True
        
        # what happens if we close the window 
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.win.mainloop()  
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)  
        
    def write(self):
        message = f"{self.nickname} : {self.input_area.get()}\n"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete(0, len(message))
        # self.input_area.delete('1.0', 'end')
        
    def typing(self):
        import time
        self.last_presstime = time.time()
        message = f"${self.nickname}"
        self.sock.send(message.encode('utf-8'))
    
    def nottyping(self):
        import time
        time.sleep(0.01)
        message = f"~{self.nickname}"
        self.sock.send(message.encode('utf-8'))
        
    # Callback to handle typing events
    def typing_indicator_callback(self,sv):
        # nonlocal current_typing_state
        # nonlocal prev_typing_state

        content = sv.get()
        print(content)
        if content != '':
            self.typing()
        else:
            self.nottyping()
        # else:
        #     current_typing_state = True

        # if current_typing_state != prev_typing_state:
        #     print('Changed')
        #     # \! : Typing indicator command
        #     client.sendall(f"\!{SEPARATOR}{username}{SEPARATOR}{person}".encode('utf-8'))
        #     # pass # Send typing info to person
        # prev_typing_state = current_typing_state


    def receive(self):
            # Token ->
            # '@' -> new user joined and server broadcasted the list of active users
            # '#' -> a user has sent a file in the group 
            # '$' -> a user is typing
            while self.running:
                # try:
                message = str(self.sock.recv(1024).decode('utf-8'))
                
                l=message.split('#')
                
                if(len(message)>0 and message[0] == '@'): # New User Joined
                    print("user list received")
                    print(message)
                    active_users = message.split('@')
                    print(active_users)
                    
                    self.active_label = tkinter.Label(self.win, text = "Active Users " ,bg = "lightgray")
                    self.active_label.config(font= ("Arial", 12))
                    self.active_label.place(x = 1250 , y = 20)
                    
                    self.active_area = tkinter.scrolledtext.ScrolledText(self.win, width= 40, height = 20, bg= "#3C99DC" )
                    # self.active_area.pack(padx = 20, pady = 5)
                    self.active_area.place(x = 1150, y = 50)
                    self.active_area.configure(state ='disabled')
                    for user_name in active_users:
                        self.active_area.config(state = "normal")
                        actual_user_name=user_name[2:len(user_name)-1]
                        self.active_area.insert('end', str(actual_user_name+'\n'))
                        self.active_area.yview('end')
                        self.active_area.config(state ='disabled')
                elif len(l)==2: 
                    l2=l[1].split(' : ')   
                    self.text_area.config(state = "normal")
                    self.text_area.insert('end', l2[0]+' : file sent\n')
                    self.text_area.yview('end')
                    self.text_area.config(state ='disabled')
                    l3=l2[1].split('\r')
                    filedata=''
                    for data in l3:
                        filedata=filedata+data
                    with open(l2[0]+'s file','w') as file:
                        file.write(filedata)
                        
                elif(len(message)>0 and message[0] == '$'):
                    typing_users = message.split('$')
                    self.who_typing.delete("1.0", "end")
                    cnt = 0
                    for user_name in typing_users:
                        if(user_name == ""):
                            continue
                        else:
                            cnt += 1
                            self.who_typing.config(state = "normal")
                            self.who_typing.insert('end', str(user_name)+",")
                            self.who_typing.yview('end')
                        # self.who_typing.config(state ='disabled')
                    if(cnt == 1):
                        self.who_typing.insert('end', "is typing")
                    elif(cnt >1 ):
                        self.who_typing.insert('end', "are typing")
                else:
                    # if self.gui_done:
                        self.text_area.config(state = "normal")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state ='disabled')
                # except ConnectionAbortedError:
                #     break
                # except:
                #     print("Error")
                #     self.sock.close()
                #     break


client = Client(HOST , PORT)

