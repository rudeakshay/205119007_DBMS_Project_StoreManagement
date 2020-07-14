# import all the modules
import tkinter
from tkinter import *
import mysql.connector
import tkinter.messagebox

conn = mysql.connector.connect(host='localhost', user='root', passwd='7729', database='store',use_pure=True )
con = conn.cursor()

s = "create table if not exists inventory(id int not null auto_increment, name varchar(50) not null, stock int not null," \
    "cp int, sp int, totalcp int, tatalsp int, assumed_profit int, vendor varchar(50), vendor_phoneno bigint, primary key(id))"

con.execute(s)
conn.commit()

con.execute("SELECT Max(id) FROM inventory")
result = con.fetchall()
if result:
    for r in result:
        id = r[0]

class Database:
    def __init__(self, master, *args, **kwargs):

        self.master = master
        self.heading = Label(master, text="Add To The Database", font=('arial 40 bold'), fg='steelblue')
        self.heading.place(x=450, y=0)

        # labels for the window
        self.name_l = Label(master, text="Enter Product Name", font=('arial 18 bold'))
        self.name_l.place(x=0, y=70)

        self.stock_l = Label(master, text="Enter Stocks", font=("arial 18 bold"))
        self.stock_l.place(x=0, y=120)
        
        self.cp_l = Label(master, text="Enter Cost Price", font=("arial 18 bold"))
        self.cp_l.place(x=0, y=170)
        
        self.sp_l = Label(master, text="Enter Selling Price", font=("arial 18 bold"))
        self.sp_l.place(x=0, y=220)
        
        self.vendor_l = Label(master, text="Enter Vendor Name", font=("arial 18 bold"))
        self.vendor_l.place(x=0, y=270)
        
        self.vendor_phone_l = Label(master, text="Enter Vendor Phone Number", font=("arial 18 bold"))
        self.vendor_phone_l.place(x=0, y=320)

        self.id_l = Label(master, text="Enter ID", font=("arial 18 bold"))
        self.id_l.place(x=0, y=370)

        # entries for lables
        self.name_e = Entry(master, width=25, font=('arial 18 bold'))
        self.name_e.place(x=400, y=70)
        
        self.stock_e = Entry(master, width=25, font=('arial 18 bold'))
        self.stock_e.place(x=400, y=120)
        
        self.cp_e = Entry(master, width=25, font=('arial 18 bold'))
        self.cp_e.place(x=400, y=170)
        
        self.sp_e = Entry(master, width=25, font=('arial 18 bold'))
        self.sp_e.place(x=400, y=220)
        
        self.vendor_e = Entry(master, width=25, font=('arial 18 bold'))
        self.vendor_e.place(x=400, y=270)
        
        self.vendor_phone_e = Entry(master, width=25, font=('arial 18 bold'))
        self.vendor_phone_e.place(x=400, y=320)

        self.id_e = Entry(master, width=25, font=('arial 18 bold'))
        self.id_e.place(x=400,y=370)

        # button to add to the database
        self.btn_clear = Button(master, text="Clear All Fields", width=25, height=2, bg='red', fg='white', command=self.clear_all)
        self.btn_clear.place(x=320, y=420)

        self.btn_add = Button(master, text="Add To Database", width=25, height=2, bg='steelblue', fg='white', command = self.get_items)
        self.btn_add.place(x=520, y=420)

        # text box for the logs
        self.tBox = Text(master, width=60, height=20)
        self.tBox.place(x=800, y=70)
        self.tBox.insert(END, "ID has reached upto: " + str(id))

    def get_items(self, *args, **kwaargs):
        conn = mysql.connector.connect(host='localhost', user='root', passwd='7729', database='store',use_pure=True )
        con = conn.cursor()
        # get data from entries
        self.name = self.name_e.get()
        self.stock = self.stock_e.get()
        self.cp = self.cp_e.get()
        self.sp = self.sp_e.get()
        self.vendor = self.vendor_e.get()
        self.vendor_phone = self.vendor_phone_e.get()

        # dynamic entries
        self.totalcp = float(self.cp) * float(self.stock)
        self.totalsp = float(self.sp) * float(self.stock)
        self.assumed_profit = float(self.totalsp - self.totalcp)

        if self.name == '' or self.stock == '' or self.cp == '' or self.sp == '':
            tkinter.messagebox.showinfo("Error", "Please Fill All Entries.")
        else:
            sql = "INSERT INTO inventory (name, stock, cp, sp, totalcp, tatalsp, assumed_profit, vendor, vendor_phoneno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            con.execute(sql, (self.name, self.stock, self.cp, self.sp, self.totalcp, self.totalsp, self.assumed_profit, self.vendor, self.vendor_phone))
            conn.commit()
            self.tBox.insert(END, "\n\nInserted " + str(self.name) + " into the database with code " + str(self.id_e.get()))
            tkinter.messagebox.showinfo("Success", "Successfully added to the Database.")
        conn.close()

    def clear_all(self, *args, **kwargs):
        # num=id+1
        self.name_e.delete(0, END)
        self.stock_e.delete(0, END)
        self.cp_e.delete(0, END)
        self.sp_e.delete(0, END)
        self.vendor_e.delete(0, END)
        self.vendor_phone_e.delete(0, END)
        self.id_e.delete(0, END)

root = Tk()
b = Database(root)

root.geometry("1366x768+0+0")
root.title("Add To Database")
root.mainloop()