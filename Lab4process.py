'''
Lab4process.py
Author: Jakin Wang
Description: Lab4 uses the NPS to create a GUI and utilizing processes
that allows the users to view all the parks in a certain state
'''
import requests
from bs4 import BeautifulSoup 
import sys
import os
import json
import tkinter as tk, multiprocessing as mp
import tkinter.messagebox as tkmb
from tkinter import filedialog

API_key = "11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg"

def loadFromWeb(StateCode):
    page = requests.get('https://developer.nps.gov/api/v1/parks?stateCode='+StateCode+'&api_key='+API_key)
    return page.json()['data']
    
class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        with open('states_hash.json', 'r') as infile:
            State_dict = json.load(infile)
            self.codeLst = list(State_dict.keys())
            self.nameLst = list(State_dict.values())
        tk.Label(self, text="Select up to 3 States").grid(row = 0, column = 0)
        self.title('Main Window')
        self.LB = tk.Listbox(self, height = 10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        self.LB.grid(row = 1, column = 0)
        self.LB.insert(tk.END, *self.nameLst)
        tk.Button(self, text='OK', command=lambda:disWin(self).display(self, [self.codeLst[i] for i in self.LB.curselection()],
                [self.nameLst[i] for i in self.LB.curselection()]) if  1 <= len(self.LB.curselection()) <= 3
                else  tkmb.showerror("Input Error", "Has to be between 1 to 3 options selected", parent=self)).grid(row=2, column=0)
        
class disWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.LB = tk.Listbox(self, width=50, height=10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        self.LB.grid(row = 0, column = 0)
        tk.Button(self, text='OK', command=self.browseFile).grid(row=1, column=0)
        self.title('Display Window')
        self.label = tk.Label(master, text='')
        self.label.grid(row = 3, column = 0)         
        self.protocol("WM_DELETE_WINDOW", self.eraseLabel)
        self.focus_set()
        self.grab_set()
        
    def eraseLabel(self):
        self.label['text'] = ''
        self.destroy()
        
    def display(self, master, codeSelect, nameSelect):
        self.codeSelect = codeSelect
        self.nameSelect = nameSelect
        pool = mp.Pool(len(codeSelect))
        self.data = pool.map(loadFromWeb, codeSelect)
        self.label['text'] = 'Fetching data for ' + str(len(codeSelect)) + ' States(s)'
        self.label.update()
        print(self.data)
        for i in range(len(codeSelect)):
            self.LB.insert(tk.END, *[nameSelect[i] + ': ' + d['fullName'] for d  in self.data[i]])
            
    def browseFile(self):
        filename = filedialog.askdirectory()
        if filename == '':
            return
        if os.path.isfile(filename + 'parks.txt'):
            tkmb.showinfo("Browse File Notification", "parks.txt already existed and will be overwritten", parent = self)
        if  filename == os.getcwd():
            filename = 'parks.txt'
        else:
            filename += 'parks.txt'
        try:
            with open(filename, 'w', encoding="utf-8") as outfile:
                for i in range(len(self.data)):
                    outfile.writelines([dic['fullName'] + '; ' + self.nameSelect[i] 
                                      + '\n' + dic['description'] + '\n\n' for dic in self.data[i]] )
        except FileNotFoundError:
            raise SystemExit
        self.destroy()

    
if __name__ == '__main__':
    mWin = mainWin()
    mWin.mainloop()