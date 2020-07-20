# import all the modules
from tkinter import *
import mysql.connector
import tkinter.messagebox
import datetime
import os
import random

conn = mysql.connector.connect(host='localhost', user='root', passwd='7729', database='store',use_pure=True )
con = conn.cursor()

# creating transactions table
s = "create table if not exists transactions(id int not null auto_increment, product_name varchar(50) not null, quantity int not null," \
    "amount int, tdate date, primary key(id))"

con.execute(s)
conn.commit()

# date
date = datetime.datetime.now().date()

# temporary lists like sessions
products_list = []
product_price = []
product_quantity = []
product_id =[]

# labels list
lables_list = []

class Application:
    def __init__(self, main, *args, **kwargs):

        self.main = main
        # frames
        self.left = Frame(main, width=700, height=768, bg='white')
        self.left.pack(side=LEFT)

        self.right = Frame(main, width=666, height=768, bg='lightblue')
        self.right.pack(side=RIGHT)

        # components
        self.heading = Label(self.left, text="2k Market", font=('arial 40 bold'), bg='white')
        self.heading.place(x=0,y=0)

        self.date_l = Label(self.right, text="Today's Date: " + str(date), font=('arial 18 bold'), bg='lightblue', fg='white')
        self.date_l.place(x=0, y=0)

        # table invoice ==================================================================
        self.tproduct = Label(self.right, text="Products", font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tproduct.place(x=0,y=60)

        self.tquantity = Label(self.right, text="Quantity", font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tquantity.place(x=300, y=60)

        self.tamount = Label(self.right, text="Amount", font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tamount.place(x=500, y=60)

        # enter stuff
        self.enterid = Label(self.left, text="Enter Product's ID", font=('arial 18 bold'), bg='white')
        self.enterid.place(x=0, y=80)

        self.enteride = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.enteride.place(x=230, y=80)
        self.enteride.focus()

        self.search_btn = Button(self.left, text="Search", width=22, height=2, bg='orange', command=self.ajax)
        self.search_btn.place(x=350, y=120)

        # fill it by the function ajax
        self.productname = Label(self.left, text="", font=('arial 27 bold'), bg='white', fg='steelblue')
        self.productname.place(x=0, y=250)

        self.pprice = Label(self.left, text="", font=('arial 27 bold'), bg='white', fg='steelblue')
        self.pprice.place(x=0, y=290)

        # total label
        self.total_l= Label(self.right, text="", font=('arial 40 bold'), bg='lightblue', fg='white')
        self.total_l.place(x=0, y=600)

        self.main.bind("<Return>", self.ajax)
        self.main.bind("<Up>", self.add_to_cart)
        self.main.bind("<space>", self.generate_bill)

    def ajax(self, *args, **kwargs):
        self.get_id=self.enteride.get()
        # get the productsinfo with there id and fill in the labels above
        query="SELECT * FROM inventory WHERE id=%s"
        con.execute(query,(self.get_id, ))
        result=con.fetchall()
        for self.r in result:
            self.get_id= self.r[0]
            self.get_name= self.r[1]
            self.get_price= self.r[4]
            self.get_stock= self.r[2]
        self.productname.configure(text="Product's Name: " + str(self.get_name))
        self.pprice.configure(text="Price: Rs. " + str(self.get_price))

        # create the quatity and discount label
        self.quantity_l=Label(self.left, text="Enter Quantity", font=('arial 18 bold'), bg='white')
        self.quantity_l.place(x=0, y=370)

        self.quantity_e= Entry(self.left, width=25,font=('arial 18 bold'), bg='light blue')
        self.quantity_e.place(x=190, y=370)
        self.quantity_e.focus()

        self.discount_l = Label(self.left, text="Enter Discount", font=('arial 18 bold'), bg='white')
        self.discount_l.place(x=0, y=410)

        self.discount_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='light blue')
        self.discount_e.place(x=190, y=410)
        self.discount_e.insert(END, 0)

        # add to cart button

        self.add_to_cart_btn = Button(self.left, text="Add To Cart", width=22, height=2, bg='orange', command=self.add_to_cart)
        self.add_to_cart_btn.place(x=350, y=450)

        #generate bills and change
        self.change_l=Label(self.left,text="Given Amount", font=('arial 18 bold'), bg='white')
        self.change_l.place(x=0, y=550)

        self.change_e= Entry(self.left, width =25, font=('arial 18 bold'), bg='lightblue')
        self.change_e.place(x=190, y=550)

        #button change
        self.change_btn = Button(self.left, text="Calculate Change", width=22, height=2, bg='orange', command=self.change_fun)
        self.change_btn.place(x=350, y=590)

        #generate bill button
        self.generate_bill_btn = Button(self.left, text="Generate Bill", width=80, height=2, bg='red', command=self.generate_bill)
        self.generate_bill_btn.place(x=60, y=640)

    def add_to_cart(self, *args, **kwargs):
        #get the quantity value from the database
        self.quantity_value= int(self.quantity_e.get())
        if self.quantity_value > int(self.get_stock):
            tkinter.messagebox.showinfo("Error","Not that many Products in our Inventory.")
        else:
            #calculate the price
            self.final_price= float(self.quantity_value)*float(self.get_price)-(float(self.discount_e.get()))

            products_list.append(self.get_name)
            product_price.append(self.final_price)
            product_quantity.append(self.quantity_value)
            product_id.append(self.get_id)

            self.x_index=0
            self.y_index=100
            self.counter=0
            for self.p in products_list:
                self.tempname= Label(self.right, text=str(products_list[self.counter]), font =('arial 18 bold') , bg='lightblue', fg='white')
                self.tempname.place(x=0, y=self.y_index)
                lables_list.append(self.tempname)

                self.tempqt = Label(self.right, text=str(product_quantity[self.counter]), font=('arial 18 bold'), bg='lightblue',fg='white')
                self.tempqt.place(x=300, y=self.y_index)
                lables_list.append(self.tempqt)

                self.tempprice = Label(self.right, text=str(product_price[self.counter]), font=('arial 18 bold'), bg='lightblue',fg='white')
                self.tempprice.place(x=500, y=self.y_index)
                lables_list.append(self.tempprice)

                self.y_index+=40
                self.counter+=1

                # total configure
                self.total_l.configure(text="Total Rs. " + str(sum(product_price)))

                # delete
                self.productname.configure(text="")
                self.pprice.configure(text="")
                self.quantity_l.place_forget()
                self.quantity_e.place_forget()
                self.discount_l.place_forget()
                self.discount_e.place_forget()
                self.add_to_cart_btn.destroy()

                # autofocus to the enter id
                self.enteride.focus()
                self.enteride.delete(0, END)


    def change_fun(self):
        # get the amount given by the customer and the amount generated by the computer
        self.amount_given = float(self.change_e.get())
        self.our_total = float(sum(product_price))

        self.to_give = self.amount_given - self.our_total

        #label change
        self.c_amount = Label(self.left, text="Change: Rs. "+str(self.to_give), font=('arial 18 bold'), fg='red', bg='white')
        self.c_amount.place(x=0, y=600)

    def generate_bill(self, *args, **kwargs):
        # create the bill before updating the database
        directory = "C:/New folder/StoreManagement/Invoice/" + str(date) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # templates for the bill
        company = "\t\t\t\t\t2K Market\n"
        address = "\t\tNational Institute of Technology, Tiruchirappalli\n"
        phone = "\t\t\t\t\t9876543210\n"
        sample = "\t\t\t\t\tInvoice\n"
        dt = "\t\t\t\t\t" + str(date)

        table_header = "\n\n\t-----------------------------------------------------------\n\t\tSNo.\t\tProducts\t\tQty\t\tAmount\n\t-----------------------------------------------------------"
        final = company + address + phone + sample + dt + "\n" + table_header

        # open a file to write it to
        file_name = str(directory) + str(random.randrange(5000,10000)) + ".rtf"
        f = open(file_name, 'w')
        f.write(final)
        # fill dynamics
        r = 1
        i = 0
        for t in products_list:
            f.write("\n\t\t" + str(r) + "\t\t" + str(products_list[i] + "     ")[:10] + "\t\t" + str(product_quantity[i]) +"\t\t" + str(product_price[i]))
            r += 1
            i += 1
        f.write("\n\n\t\t\t\tTotal Amount Rs. " + str(sum(product_price)))
        f.write("\n\t\t\t\tThanks for Visiting.")
        os.startfile(file_name, "print")
        f.close()

        # decrease the stock
        self.x = 0

        for i in products_list:
            initial = "SELECT * FROM inventory WHERE id=%s"
            con.execute(initial, (product_id[self.x],))
            result = con.fetchall()

            for r in result:
                self.old_stock = r[2]

            self.new_stock = int(self.old_stock)-int(product_quantity[self.x])

            # updating the stock
            sql="UPDATE inventory SET stock=%s WHERE id=%s"
            con.execute(sql, (self.new_stock, product_id[self.x]))
            conn.commit()

            # insert into the transaction
            sql2 = "INSERT INTO transactions(product_name, quantity, amount, tdate) VALUES (%s,%s,%s,%s)"
            con.execute(sql2,(products_list[self.x], product_quantity[self.x], product_price[self.x], date))
            conn.commit()

            self.x += 1

        for a in lables_list:
            a.destroy()

        del(product_id[:])
        del(products_list[:])
        del(product_quantity[:])
        del(product_price[:])

        self.total_l.configure(text="")
        self.c_amount.configure(text="")
        self.change_e.delete(0, END)
        self.enteride.focus()

        tkinter.messagebox.showinfo("Success", "Done Everything Smoothly.")

root = Tk()
b = Application(root)

root.geometry("1366x768+0+0")
root.mainloop()