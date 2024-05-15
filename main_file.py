
import pymysql
import sys
from pymysql import Error
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

config = {
    'user': 'root',
    'passwd': 'M@nchester7',  #Change this line to enter your MySQL password
    'host': 'localhost',
    'database': 'contact_book'
}

def connect_to_database():
    try:    
        conn = pymysql.connect(**config)   
        if conn:
            print('Connected to MySQL database')
            
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY last_name ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()        
        
    except Error as e:
        print(f"Error: {e}")
        return None


def submit_data():
    if FIRST_NAME.get() == "" or LAST_NAME.get() == "" or AGE.get() == "" or CONTACT_NUMBER.get() == "":
        result = tkMessageBox.showwarning('', 'Please complete the required field', icon = 'warning')
    else:
        tree.delete(*tree.get_children())
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts(first_name, last_name, age, phone_number) values(\'%s\',\'%s\',%d,\'%s\')' % (str(FIRST_NAME.get()),str(LAST_NAME.get()),int(AGE.get()),str(CONTACT_NUMBER.get())))
        conn.commit()

        cursor.execute('SELECT * FROM contacts ORDER BY last_name ASC')
        fetch = cursor.fetchall()
        for row in fetch:
            tree.insert('', 'end', values=(row))
        cursor.close()
        conn.close()
        FIRST_NAME.set('')
        LAST_NAME.set('')
        AGE.set('')
        CONTACT_NUMBER.set('')
        result = tkMessageBox.showinfo('', message='New contact added successfully!', icon='info')

def update_data():
    if FIRST_NAME.get() == "" or LAST_NAME.get() == "" or AGE.get() == "" or CONTACT_NUMBER.get() == "":
        result = tkMessageBox.showwarning('', 'Please complete the required field', icon = 'warning')
    else:
        tree.delete(*tree.get_children())
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute('UPDATE contacts set first_name=\'%s\', last_name=\'%s\', age=%d, phone_number=\'%s\' where contact_id=%d' %(str(FIRST_NAME.get()),str(LAST_NAME.get()),int(AGE.get()),str(CONTACT_NUMBER.get()), int(mem_id)))
        conn.commit()

        cursor.execute('SELECT * FROM contacts ORDER BY last_name ASC')
        fetch = cursor.fetchall()
        for row in fetch:
            tree.insert('', 'end', values=(row))
        cursor.close()
        conn.close()
        FIRST_NAME.set('')
        LAST_NAME.set('')
        AGE.set('')
        CONTACT_NUMBER.set('')    
        result = tkMessageBox.showinfo('', message='Updated successfully!', icon='info')

def AddNewWindow():
    global NewWindow
    FIRST_NAME.set("")
    LAST_NAME.set("")
    AGE.set("")
    CONTACT_NUMBER.set("")

    NewWindow = Toplevel()
    NewWindow.title("CONTACT LIST")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2 - 455) - (width/2))
    y = ((screen_height/2 + 20) - (height/2))
    NewWindow.resizable(True, True)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()    

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)

    title_label = Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="#66ff66", width=300)
    title_label.pack(fill=X)
    firstname_label = Label(ContactForm, text="First Name", font=('arial', 14), bd=5)
    firstname_label.grid(row=0, sticky=W)
    lastname_label = Label(ContactForm, text="Last Name", font=('arial', 14), bd=5)
    lastname_label.grid(row=1, sticky=W)
    age_label = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    age_label.grid(row=2, sticky=W)
    contactno_label = Label(ContactForm, text="Contact Number", font=('arial', 14), bd=5)
    contactno_label.grid(row=3, sticky=W)

    firstname_entry = Entry(ContactForm, textvariable=FIRST_NAME, font=('arial',14))
    firstname_entry.grid(row=0,column=1)
    lastname_entry = Entry(ContactForm, textvariable=LAST_NAME, font=('arial',14))
    lastname_entry.grid(row=1,column=1)
    firstname_entry = Entry(ContactForm, textvariable=AGE, font=('arial',14))
    firstname_entry.grid(row=2,column=1)
    firstname_entry = Entry(ContactForm, textvariable=CONTACT_NUMBER, font=('arial',14))
    firstname_entry.grid(row=3,column=1)     

    save_btn = Button(ContactForm,text="Save", width=50, command=submit_data)
    save_btn.grid(row=4, columnspan=2, pady=10)
    


def DeleteContact():
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Select a contact First!', icon='warning')
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == "yes":
            cur_item = tree.focus()
            contents = (tree.item(cur_item))
            selected_item = contents['values']
            tree.delete(cur_item)
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts where contact_id = %d' % selected_item[0])
            conn.commit()
            cursor.close()
            conn.close()
            result = tkMessageBox.showinfo('', message='Deleted successfully!', icon='info')
            


def OnSelected(event):
    global mem_id, UpdateWindow
    cur_item = tree.focus()
    contents = (tree.item(cur_item))
    selected_item = contents['values']
    mem_id = selected_item[0]
    FIRST_NAME.set("")
    LAST_NAME.set("")
    AGE.set("")
    CONTACT_NUMBER.set("")
    
    FIRST_NAME.set(selected_item[1])
    LAST_NAME.set(selected_item[2])
    AGE.set(selected_item[3])
    CONTACT_NUMBER.set(selected_item[4])

    UpdateWindow = Toplevel()
    UpdateWindow.title("CONTACT LIST")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2 + 450) - (width/2))
    y = ((screen_height/2 + 450) - (height/2))
    UpdateWindow.resizable(True, True)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)

    title_label = Label(FormTitle, text="Updating Existing Contact", font=('arial', 16), bg="#66ff66", width=300)
    title_label.pack(fill=X)
    firstname_label = Label(ContactForm, text="First Name", font=('arial', 14), bd=5)
    firstname_label.grid(row=0, sticky=W)
    lastname_label = Label(ContactForm, text="Last Name", font=('arial', 14), bd=5)
    lastname_label.grid(row=1, sticky=W)
    age_label = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    age_label.grid(row=2, sticky=W)
    contactno_label = Label(ContactForm, text="Contact Number", font=('arial', 14), bd=5)
    contactno_label.grid(row=3, sticky=W)

    firstname_entry = Entry(ContactForm, textvariable=FIRST_NAME, font=('arial',14))
    firstname_entry.grid(row=0,column=1)
    lastname_entry = Entry(ContactForm, textvariable=LAST_NAME, font=('arial',14))
    lastname_entry.grid(row=1,column=1)
    firstname_entry = Entry(ContactForm, textvariable=AGE, font=('arial',14))
    firstname_entry.grid(row=2,column=1)
    firstname_entry = Entry(ContactForm, textvariable=CONTACT_NUMBER, font=('arial',14))
    firstname_entry.grid(row=3,column=1)     

    save_btn = Button(ContactForm,text="Update", width=50, command=update_data)
    save_btn.grid(row=4, columnspan=2, pady=10)





root = Tk()
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(True, True)
root.config(bg="#6666ff")

FIRST_NAME = StringVar()
LAST_NAME = StringVar()
AGE = IntVar()
CONTACT_NUMBER = StringVar()

Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg='#6666ff')
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg='#6666ff')
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT,  pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

title_label = Label(Top, text="Contact Management System", font=('arial', 16), width=500)
title_label.pack(fill=X)

add_button = Button(MidLeft, text="+ ADD NEW CONTACT", bg='#66ff66', command=AddNewWindow)
add_button.pack()
delete_button = Button(MidRight, text="DELETE CONTACT", bg='red', command=DeleteContact)
delete_button.pack()

scrollbary = Scrollbar(TableMargin, orient=VERTICAL)

tree = ttk.Treeview(TableMargin, columns = ('MemberID', 'First_Name', 'Last_Name', 'Age', 'Contact_Number'), height=400, selectmode='extended', yscrollcommand=scrollbary.set)

scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)

tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('First_Name', text="First Name", anchor=W)
tree.heading('Last_Name', text="Last Name", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Contact_Number', text="Contact Number", anchor=W)


tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>',OnSelected)

connect_to_database()

root.mainloop()







        



#CHANGE AGE TO STRING TO MAKE IT EASIER