from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
from mysql.connector.errors import DatabaseError

class Criminal:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x800+0+0")
        self.root.title("CRIMINAL gaurav SYSTEM")

        # Variables

        self.var_case_id = StringVar()
        self.var_criminal_no = StringVar()
        self.var_name = StringVar()
        self.var_nickname = StringVar()
        self.var_father_name = StringVar()
        self.var_arrest_date = StringVar()
        self.var_date_of_crime = StringVar()
        self.var_address = StringVar()
        self.var_age = StringVar()
        self.var_occupation = StringVar()
        self.var_birthMark = StringVar()
        self.var_crime_type = StringVar()
        self.var_gender = StringVar()
        self.var_wanted = StringVar()
        self.var_adhar_no = StringVar()

        lbltitle = Label(self.root, text="CRIMINAL MANAGEMENT SYSTEM", bd=8, relief=RIDGE,
                         bg="black", fg="white", font=("times new roman", 50, "bold"), padx=2, pady=-2)
        lbltitle.pack(side=TOP, fill=X)

        # police logo Image

        img_logo = Image.open("E:\Project Files\Project👍\Final Project\images\maharashtra.png")
        img_logo = img_logo.resize((60, 60), Image.ANTIALIAS)
        self.photo_logo = ImageTk.PhotoImage(img_logo)
        self.logo = Label(self.root, image=self.photo_logo)
        self.logo.place(x=100, y=15, width=60, height=60)

        # Main Frame
        Main_frame = Frame(self.root,  relief=RIDGE, bg="white")
        Main_frame.place(x=0, y=100, width=1515, height=675)
            
        #Down frame
        down_frame = LabelFrame(Main_frame, bd=2, relief=RIDGE, text="Criminal Information Table", 
        font=("times new roman", 12, "bold"), fg="darkgreen", bg="white")
        down_frame.place(x=8, y=17, width=1490, height=655)

        search_frame = LabelFrame(down_frame, bd=2, relief=RIDGE, text="Search Criminal Record", 
        font=("times new roman", 12, "bold"), fg="darkgreen", bg="white")
        search_frame.place(x=10, y=0, width=1465, height=62)
        #Search By
        search_by=Label(search_frame,font=("arial",11,"bold"),text="Search By:",bg="red",fg="white")
        search_by.grid(row=0,column=0,sticky=W,padx=5)

        self.var_com_search=StringVar()
        combo_search_box=ttk.Combobox(search_frame,textvariable=self.var_com_search ,
        font=("arial",11,"bold"),width=18,state='readonly')
        combo_search_box['value']=('Select Option','Case ID','Criminal Name','Status')
        combo_search_box.current(0)
        combo_search_box.grid(row=0,column=1,sticky=W,padx=5)

        self.var_search=StringVar()
        search_txt=ttk.Entry(search_frame,textvariable=self.var_search ,width=18,font=("arial",11,"bold"))
        search_txt.grid(row=0,column=2,sticky=W,padx=5)

        #search button
        btn_search=Button(search_frame,bd=4,command=self.search_data, text='Search',
        font=("arial",13,"bold"),width=14,bg='#32a885')
        btn_search.grid(row=0,column=3,padx=1,pady=0)

        #all button
        btn_all=Button(search_frame,bd=4,command=self.fetch_data, text='Show All',
        font=("arial",13,"bold"),width=14,bg='#3275a8')
        btn_all.grid(row=0,column=4,padx=3,pady=5)

        crimeagency=Label(search_frame,font=("arial",15,"bold"),text="मुंबई पुलिस",bg='white',fg='crimson')
        crimeagency.grid(row=0,column=5,sticky=W,padx=300,pady=0)

        # Table Frame
        table_frame = Frame(down_frame, bd=5, relief=RIDGE)
        table_frame.place(x=8, y=65, width=1467, height=555)

        # Scroll bar
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.criminal_table=ttk.Treeview(table_frame,column=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.criminal_table.xview)
        scroll_y.config(command=self.criminal_table.yview)

        self.criminal_table.heading("1",text="Case Id")
        self.criminal_table.heading("2",text="Act")
        self.criminal_table.heading("3",text="Criminal Name")
        self.criminal_table.heading("4",text="Officer Name")
        self.criminal_table.heading("5",text="Arrest Date")
        self.criminal_table.heading("6",text="Date of crime")
        self.criminal_table.heading("7",text="Address")
        self.criminal_table.heading("8",text="Age")
        self.criminal_table.heading("9",text="Occupation")
        self.criminal_table.heading("10",text="Status")
        self.criminal_table.heading("11",text="Crime Type")
        self.criminal_table.heading("12",text="Father Name")
        self.criminal_table.heading("13",text="Gender")
        self.criminal_table.heading("14",text="Wanted")
        self.criminal_table.heading("15",text="Adhar")

        self.criminal_table['show']='headings'

        self.criminal_table.column("1",width=50)
        self.criminal_table.column("2",width=70)
        self.criminal_table.column("3",width=140)
        self.criminal_table.column("4",width=100)
        self.criminal_table.column("5",width=100)
        self.criminal_table.column("6",width=100)
        self.criminal_table.column("7",width=100)
        self.criminal_table.column("8",width=50)
        self.criminal_table.column("9",width=130)
        self.criminal_table.column("10",width=140)
        self.criminal_table.column("11",width=100)
        self.criminal_table.column("12",width=100)
        self.criminal_table.column("13",width=100)
        self.criminal_table.column("14",width=100)
        self.criminal_table.column("15",width=100)

        self.criminal_table.pack(fill=BOTH,expand=1)

        self.criminal_table.bind("<ButtonRelease>",self.get_cursor )
        self.fetch_data()

    # Add function

    def add_data(self):
        if self.var_case_id.get()=="":
            messagebox.showerror('Error','All fields are required')
        else:
            try:
                conn=mysql.connector.connect(host='localhost', username='root',password='Gaurav', database='sys')
                my_cursor=conn.cursor()
                my_cursor.execute('insert into criminal values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(self.var_case_id.get(),
                                                                                                            self.var_criminal_no.get(),
                                                                                                            self.var_name.get(),
                                                                                                            self.var_nickname.get(),
                                                                                                            self.var_arrest_date.get(),
                                                                                                            self.var_date_of_crime.get(),
                                                                                                            self.var_address.get(),
                                                                                                            self.var_age.get(),
                                                                                                            self.var_occupation.get(),
                                                                                                            self.var_birthMark.get(),
                                                                                                            self.var_crime_type.get(),
                                                                                                            self.var_father_name.get(),
                                                                                                            self.var_gender.get(),
                                                                                                            self.var_wanted.get(),
                                                                                                            self.var_adhar.get() ))
                conn.commit()
                self.fetch_data()
                self.clear_data()
                conn.close()
                messagebox.showinfo('successful', 'Criminal record has been added')
            except Exception as es:
                messagebox.showerror('error',f'Due to{str(es)}')

    # fetch data

    def fetch_data(self):
        conn=mysql.connector.connect(host='localhost', username='root',password='Gaurav', database='sys')
        my_cursor=conn.cursor()
        my_cursor.execute('select * from criminal')
        data=my_cursor.fetchall()
        if len(data)!=0:
            self.criminal_table.delete(*self.criminal_table.get_children())
            for i in data:
                self.criminal_table.insert('',END,values=i)
            conn.commit()
        conn.close()

    # get cursor

    def get_cursor(self,event=""):
        cursor_row=self.criminal_table.focus()
        content=self.criminal_table.item(cursor_row)
        data=content['values']

        self.var_case_id.set(data[0])
        self.var_criminal_no.set(data[1])
        self.var_name.set(data[2])
        self.var_nickname.set(data[3])
        self.var_arrest_date.set(data[4])
        self.var_date_of_crime.set(data[5])
        self.var_address.set(data[6])
        self.var_age.set(data[7])
        self.var_occupation.set(data[8])
        self.var_birthMark.set(data[9])
        self.var_crime_type.set(data[10])
        self.var_father_name.set(data[11])
        self.var_gender.set(data[12])
        self.var_wanted.set(data[13])
        self.var_adhar.set(data[14])

    # update

    def update_data(self):
        if self.var_case_id.get()=="":
            messagebox.showerror('Error','All fields are required')
        else:
            try:
                update=messagebox.askyesno('update', "Are you sure you want to update this record?")
                if update>0:
                    conn=mysql.connector.connect(host='localhost', username='root',password='Gaurav', database='sys')
                    my_cursor=conn.cursor() 
                    my_cursor.execute('update criminal set  Criminal_no=%s, Criminal_name=%s, Nick_name=%s, arrest_date=%s, dateOfcrime=%s, address=%s, age=%s,  occupation=%s, BirthMark=%s, crimeType=%s, fatherName=%s, gender=%s, wanted=%s, adhar=%s where Case_id=%s',(
                                                                                                                self.var_criminal_no.get(),
                                                                                                                self.var_name.get(),
                                                                                                                self.var_nickname.get(),
                                                                                                                self.var_arrest_date.get(),
                                                                                                                self.var_date_of_crime.get(),
                                                                                                                self.var_address.get(),
                                                                                                                self.var_age.get(),
                                                                                                                self.var_occupation.get(),
                                                                                                                self.var_birthMark.get(),
                                                                                                                self.var_crime_type.get(),
                                                                                                                self.var_father_name.get(),
                                                                                                                self.var_gender.get(),
                                                                                                                self.var_wanted.get(), 
                                                                                                                self.var_adhar.get(), 
                                                                                                                self.var_case_id.get()))    
                else:
                    if not update:
                        return
                conn.commit()
                self.fetch_data()
                self.clear_data()
                conn.close()
                messagebox.showinfo('successful', 'Criminal record has been updated')
            except Exception as es:
                messagebox.showerror('error',f'Due to{str(es)}')   
    
    #delete

    def delete_data(self):
        if self.var_case_id.get()=="":
            messagebox.showerror('Error','All fields are required')
        else:
            try:
                delete=messagebox.askyesno('Delete', "Are you sure you want to Delete this record?")
                if delete>0:
                    conn=mysql.connector.connect(host='localhost', username='root',password='Gaurav', database='sys')
                    my_cursor=conn.cursor() 
                    sql="DELETE FROM criminal WHERE Case_id= %s "
                    value=(self.var_case_id.get(),)
                    my_cursor.execute(sql,value)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.clear_data()
                conn.close()
                messagebox.showinfo('successful', 'Criminal record has been deleted')
            except Exception as es:
                messagebox.showerror('error',f'Due to {str(es)}')   

    # clear

    def clear_data(self):
        self.var_case_id.set("")
        self.var_criminal_no.set("")
        self.var_name.set("")
        self.var_nickname.set("")
        self.var_arrest_date.set("")
        self.var_date_of_crime.set("")
        self.var_address.set("")
        self.var_age.set("")
        self.var_occupation.set("")
        self.var_birthMark.set("")
        self.var_crime_type.set("")
        self.var_father_name.set("")
        self.var_gender.set("")
        self.var_wanted.set("")
        self.var_adhar.set("")

    # search

    def search_data(self): 
        if self.var_com_search.get()=="":
            messagebox.showerror('Error','All fields are required') 
        else:
            try:
                conn=mysql.connector.connect(host='localhost', username='root',password='Gaurav', database='sys')
                my_cursor=conn.cursor()
                my_cursor.execute('select * from criminal where '+str(self.var_com_search.get())+" LIKE'%"+str(self.var_search.get()+"%'"))
                rows=my_cursor.fetchall()
                if len(rows)!=0:
                    self.criminal_table.delete(*self.criminal_table.get_children())
                    for i in rows:
                        self.criminal_table.insert('',END,values=i)
                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror('error',f'Due to{str(es)}') 

if __name__=="__main__":
    root=Tk()
    obj=Criminal(root)
    root.mainloop()
