import datetime
import sqlite3
from Tkinter import Tk, Label, Button, Entry, StringVar, N, S, W, E, Scale
import ttk
import main
import os


class GuessingGame:
    def __init__(self, master):
        self.master = master
        master.title("Laser Data Fetcher")


        # text
        self.title = ttk.Label(text="Guiyang Laser-Device's Data Fetching System")
        self.company = Label(master, text = "Search by Company's Name: ")
        self.frequency = Label(master, text = "Search by Frequencies: ")
        self.start = Label(master, text = "Start Range (nm): ")
        self.end = Label(master, text = "End Range (nm): ")

        self.companies = StringVar()
        self.companies.set("Total Companies Found: ")
        self.company_found = Label(master, textvariable=self.companies)
        self.entries = StringVar()
        self.entries.set("Total Entries Found: ")
        self.entry_found = Label(master, textvariable=self.entries)

        # search block
        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master)

        #define all widgets
        self.find_name_button = Button(master, text="Get", command=self.find_name)
        self.start_freq = Scale(master, from_=369, to=2961, orient="horizontal", length= 180)
        self.end_freq = Scale(master, from_=369, to=2961, orient="horizontal", length= 180)
        self.get_it = Button(master, text='Get Data', command=self.get_between)

        self.tree_scroll = ttk.Scrollbar(orient="vertical")
        self.output = ttk.Treeview()
        self.output.configure(columns=('Frequencies', 'Powers', 'Manufactor'), show='headings')
        self.output.heading('Frequencies', text='Wavelength')
        self.output.heading('Powers', text='Power')
        self.output.heading('Manufactor', text='Manufactor')
        self.output.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.configure(command=self.output.yview)



        self.title.grid(row=0, column=0, columnspan=4)
        self.company.grid(row=1, column=0,sticky = W)
        self.entry.grid(row=1, column=1, columnspan=1, sticky = W + E)
        self.find_name_button.grid(row=1, column=2, sticky = W)
        self.frequency.grid(row=4, column=0,sticky = W)
        self.start.grid(row=5, column=0)
        self.end.grid(row=6, column=0)
        self.start_freq.grid(row=5, column=1)
        self.end_freq.grid(row=6, column=1)
        self.get_it.grid(row=6, column=2)
        self.output.grid(row=9, column=0, columnspan=4, sticky=W+E)
        self.tree_scroll.grid(row=9, rowspan=4, column=5, sticky=N+S)
        self.company_found.grid(row =10, column=0, sticky = W)
        self.entry_found.grid(row=10, column=2, sticky = W)

    def validate(self, new_text):
            return False

    def get_between(self):
        start = self.start_freq.get()
        end = self.end_freq.get()

        # get data add in the list.
        self.output.delete(*self.output.get_children())
        connection = sqlite3.connect(str(datetime.date.today()) + "_data.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM Wave_Power_Laser WHERE CAST(Wavelength AS INT) > (?) AND CAST(Wavelength AS INT) < (?) ORDER BY CAST(Wavelength AS INT);""", (start, end))
        connection.commit()
        for row in cursor:
            self.output.insert('', 'end', text='item 2', values=(row[1],row[2],row[3]))
        connection.close()


        # find total companies + entries:
        connection = sqlite3.connect(str(datetime.date.today()) + "_data.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT COUNT (DISTINCT Manufactor_brand) FROM Wave_Power_Laser WHERE CAST(Wavelength AS INT) > (?) AND CAST(Wavelength AS INT) < (?) ORDER BY CAST(Wavelength AS INT);""", (start, end))
        connection.commit()
        total_company = cursor.fetchone()

        cursor.execute("""SELECT COUNT (*) FROM Wave_Power_Laser WHERE CAST(Wavelength AS INT) > (?) AND CAST(Wavelength AS INT) < (?) ORDER BY CAST(Wavelength AS INT);""", (start, end))
        connection.commit()
        total_entry = cursor.fetchone()
        connection.close()

        self.companies.set("Total Companies Found: " + str(total_company[0]))
        self.entries.set("Total Entries Found: " + str(total_entry[0]))

        print start, end


    def find_name(self):
        self.output.delete(*self.output.get_children())
        connection = sqlite3.connect(str(datetime.date.today()) + "_data.db")
        cursor = connection.cursor()
        manufactor_name = self.entry.get()
        print manufactor_name
        cursor.execute("""SELECT * FROM Wave_Power_Laser WHERE Manufactor_brand = (?) ORDER BY CAST(Wavelength AS INT);""", (manufactor_name,))
        connection.commit()
        for row in cursor:
            self.output.insert('', 'end', text='item 2', values=(row[1],row[2],row[3]))

        cursor.execute("""SELECT COUNT (*) FROM Wave_Power_Laser WHERE Manufactor_brand = (?) ORDER BY CAST(Wavelength AS INT);""", (manufactor_name,))
        connection.commit()
        total_entry = cursor.fetchone()
        connection.close()

        self.companies.set("Total Companies Found: ")
        self.entries.set("Total Entries Found: " + str(total_entry[0]))



if __name__ == "__main__":
    if not os.path.isfile("data_" + str(datetime.date.today()) +".txt"):
        A = main.get_data()
        A.fetch_data()
        A.convert_sql()
    root = Tk()
    my_gui = GuessingGame(root)
    root.mainloop()







