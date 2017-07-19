import urllib2
import re
import datetime
import sqlite3
import os
from bs4 import BeautifulSoup


def get_list(url = 'https://www.laserdiodesource.com'):
    '''
    giving a source file that returns all subcategory files.
    :param url: str
    :return: list[str]
    '''
    print 'start getting the sublist'
    try:
        page = urllib2.urlopen(url)
    except (urllib2.URLError, ValueError):
        print 'Page no longer available'
        return None

    html = page.read()
    potential_list = []
    for m in re.finditer('View ALL Wavelengths', html):
       potential_list.append(html[m.start()- 100:m.start()])

    outcome_list = []
    for each in potential_list:
        l = 0
        while each[0] != '"':
            each = each[1:]
        each = each[1:]

        end = 0
        while each[end] != '"':
            end += 1
        each = 'https://www.laserdiodesource.com' + each[:end]
        print 'subpage found: ' + each
        outcome_list.append(each)
    return outcome_list

def save_data_to_text(data):
    text_file = open("data_" + str(datetime.date.today()) +".txt", "w")
    text_file.write(data)
    text_file.close()


class get_data(object):
    def __init__(self):
        self.Wavelength = []
        self.Power = []
        self.Manufactor = []
        self.all_data = []
    def fetch_data(self):
        print 'start fetching the data'
        all_sub_list = get_list()
        for each_sub in all_sub_list:
            self.get_attributes(each_sub)

        self.all_data = zip(self.Wavelength, self.Power, self.Manufactor)
        save_data_to_text(str(self.all_data))

        print 'Extraction completed. Data extracted: ' + str(len(self.all_data))

    def get_attributes(self, url):
        '''
        Import an url and extract the attributes of each aspect
        :param url: str
        :return: list[list[str]]
        '''
        try:
            page = urllib2.urlopen(url)
        except (urllib2.URLError, ValueError):
            print str(url) + 'This Page no longer available'
            return None
        html = page.read()
        soup = BeautifulSoup(html)

        # col1: wavelength, col2:Power, col5:Manufactorer
        self.Wavelength.extend([str(i.text) for i in soup.find_all('span', {"class": "col1"})])
        self.Power.extend([str(i.text) for i in soup.find_all('span', {"class": "col2"})])
        self.Manufactor.extend([str(i.text) for i in soup.find_all('span', {"class": "col5"})])



    def get_manufactors(self):
        print 'There are total :', len(list(set(self.Manufactor))), 'manufactors.'
        return list(set(self.Manufactor))

    def get_Power(self):
        print 'There are total :', len(list(set(self.Power))), 'type of powers.'
        return list(set(self.Power))

    def get_Wavelength(self):
        print 'There are total :', len(list(set(self.Wavelength))), 'type of wavelengths.'
        return list(set(self.Wavelength))

    def convert_sql(self):
        connection = sqlite3.connect(str(datetime.date.today()) + "_data.db")
        cursor = connection.cursor()

        sql_command = """
                CREATE TABLE Wave_Power_Laser (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Wavelength VARCHAR(30),
                Power VARCHAR(30),
                Manufactor_brand VARCHAR(250),
                Ranged BOOLEAN DEFAULT FALSE);"""
        cursor.execute(sql_command)

        while self.all_data:
            each = self.all_data.pop()
            wavelen = each[0]
            power = each[1]
            manu = each[2]
            range = 'TRUE' if '-' in wavelen else 'FALSE'
            if ',' in wavelen:
                for wave in wavelen.split(','):
                    self.all_data.append((wave, power, manu))
            else:
                cursor.execute("INSERT INTO Wave_Power_Laser (Wavelength,Power,Manufactor_brand,Ranged) \
                    VALUES (?,?,?,?);",(wavelen.strip(), power.strip(), manu.strip(), range.strip()))

        connection.commit()
        connection.close()

if __name__ == "__main__":
    if os.path.isfile("data_" + str(datetime.date.today()) +".txt"):
        print 'File already exist, process to database \n'
    else:
        A = get_data()
        A.fetch_data()
        A.convert_sql()
        print 'Data Fetching Complete'


'''
connection = sqlite3.connect(str(datetime.date.today()) + "_test_data.db")
cursor = connection.cursor()


cursor.execute("SELECT * FROM Wave_Power_Laser")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3]
   print "range", row[4], "\n"

connection.commit()
connection.close()



cursor.execute("""INSERT INTO Wave_Power_Laser (Wavelength,Power,Manufactor_brand) \
                    VALUES (?,?,?);""",('100nm','200nm','300nm'))
                    
                    
cursor.execute("SELECT * FROM Wave_Power_Laser LIMIT 10")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"
'''