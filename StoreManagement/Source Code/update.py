# import all the modules
import tkinter
from tkinter import *
import mysql.connector
import tkinter.messagebox

conn = mysql.connector.connect(host='localhost', user='root', passwd='7729', database='store', use_pure=True)
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
    def __init__(self, main, *args, **kwargs):
        self.main = main
        self.heading = Label(main, text="Update To The Database", font=('arial 40 bold'), fg='steelblue')
        self.heading.place(x=400, y=0)

        # label and entry for id
        self.id_le = Label(main, text="Enter ID", font=("arial 18 bold"))
        self.id_le.place(x=0, y=70)

        self.id_leb = Entry(main, width=10, font=('arial 20 bold'))
        self.id_leb.place(x=400, y=70)

        self.btn_search = Button(main, text="Search", width=15, height=2, bg='orange', command=self.search)
        self.btn_search.place(x=580, y=70)

        # labels for the window
        self.name_l = Label(main, text="Enter Product Name", font=('arial 18 bold'))
        self.name_l.place(x=0, y=120)

        self.stock_l = Label(main, text="Enter Stocks", font=("arial 18 bold"))
        self.stock_l.place(x=0, y=170)

        self.cp_l = Label(main, text="Enter Cost Price", font=("arial 18 bold"))
        self.cp_l.place(x=0, y=220)

        self.sp_l = Label(main, text="Enter Selling Price", font=("arial 18 bold"))
        self.sp_l.place(x=0, y=270)

        self.totalcp_l = Label(main, text="Enter Total Cost Price", font=("arial 18 bold"))
        self.totalcp_l.place(x=0, y=320)

        self.totalsp_l = Label(main, text="Enter Total Selling Price", font=("arial 18 bold"))
        self.totalsp_l.place(x=0, y=370)

        self.vendor_l = Label(main, text="Enter Vendor Name", font=("arial 18 bold"))
        self.vendor_l.place(x=0, y=420)

        self.vendor_phone_l = Label(main, text="Enter Vendor Phone Number", font=("arial 18 bold"))
        self.vendor_phone_l.place(x=0, y=470)

        # entries for lables
        self.name_e = Entry(main, width=25, font=('arial 18 bold'))
        self.name_e.place(x=400, y=120)

        self.stock_e = Entry(main, width=25, font=('arial 18 bold'))
        self.stock_e.place(x=400, y=170)

        self.cp_e = Entry(main, width=25, font=('arial 18 bold'))
        self.cp_e.place(x=400, y=220)

        self.sp_e = Entry(main, width=25, font=('arial 18 bold'))
        self.sp_e.place(x=400, y=270)

        self.totalcp_e = Entry(main, width=25, font=('arial 18 bold'))
        self.totalcp_e.place(x=400, y=320)

        self.totalsp_e = Entry(main, width=25, font=('arial 18 bold'))
        self.totalsp_e.place(x=400, y=370)

        self.vendor_e = Entry(main, width=25, font=('arial 18 bold'))
        self.vendor_e.place(x=400, y=420)

        self.vendor_phone_e = Entry(main, width=25, font=('arial 18 bold'))
        self.vendor_phone_e.place(x=400, y=470)

        # button to add to the database
        self.btn_clear = Button(main, text="Clear All Fields", width=25, height=2, bg='red', fg='white')
        self.btn_clear.place(x=320, y=520)

        self.btn_update = Button(main, text="Update Database", width=25, height=2, bg='steelblue', fg='white', command=self.update)
        self.btn_update.place(x=520, y=520)

        # text box for the logs
        self.tBox = Text(main, width=60, height=20)
        self.tBox.place(x=800, y=70)
        self.tBox.insert(END, "")

    def search(self, *args, **kwargs):
        sql = "SELECT * FROM inventory WHERE id=%s"
        con.execute(sql, (self.id_leb.get(), ))
        result = con.fetchall()

        for r in result:
            self.n1 = r[1]  # name
            self.n2 = r[2]  # stock
            self.n3 = r[3]  # cp
            self.n4 = r[4]  # sp
            self.n5 = r[5]  # totalcp
            self.n6 = r[6]  # tatalsp
            self.n7 = r[7]  # assumed_profit
            self.n8 = r[8]  # vendor
            self.n9 = r[9]  # vendor_phoneno
        conn.commit()

        # insert into the entries to update
        self.name_e.delete(0, END)
        self.name_e.insert(0, str(self.n1))

        self.stock_e.delete(0, END)
        self.stock_e.insert(0, str(self.n2))

        self.cp_e.delete(0, END)
        self.cp_e.insert(0, str(self.n3))

        self.sp_e.delete(0, END)
        self.sp_e.insert(0, str(self.n4))

        self.totalcp_e.delete(0, END)
        self.totalcp_e.insert(0, str(self.n5))

        self.totalsp_e.delete(0, END)
        self.totalsp_e.insert(0, str(self.n6))

        self.vendor_e.delete(0, END)
        self.vendor_e.insert(0, str(self.n8))

        self.vendor_phone_e.delete(0, END)
        self.vendor_phone_e.insert(0, str(self.n9))

    def update(self, *args, **kwargs):
        con = conn.cursor()
        # get all updated values
        self.u1 = self.name_e.get()
        self.u2 = self.stock_e.get()
        self.u3 = self.cp_e.get()
        self.u4 = self.sp_e.get()
        self.u5 = self.totalcp_e.get()
        self.u6 = self.totalsp_e.get()
        self.u7 = self.vendor_e.get()
        self.u8 = self.vendor_phone_e.get()

        query = "UPDATE inventory SET name=%s, stock=%s, cp=%s, sp=%s, totalcp=%s, tatalsp=%s, vendor=%s, vendor_phoneno=%s WHERE id=%s"
        con.execute(query, (self.u1, self.u2, self.u3, self.u4, self.u5, self.u6, self.u7, self.u8, self.id_leb.get()))
        conn.commit()
        tkinter.messagebox.showinfo("Success","Database Updated!!!")



root = Tk()
b = Database(root)

root.geometry("1366x768+0+0")
root.title("Update To Database")
root.mainloop()