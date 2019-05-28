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


with open('states_hash.json', 'r') as infile:
    State_dict = json.load(infile)
    
codeLst = list(State_dict.keys())
nameLst = list(State_dict.values())
API_key = "11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg"
data = []

def loadFromWeb(StateCode):
    print(StateCode)
    page = requests.get('https://developer.nps.gov/api/v1/parks?stateCode=DE&api_key=11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg')
    print(page.json())    

class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        tk.Label(self, text="Select up to 3 States").grid(row = 0, column = 0)
        self.title('Main Window')
        self.LB = tk.Listbox(self, height = 10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        self.LB.grid(row = 1, column = 0)
        for v in State_dict.values():
            self.LB.insert(tk.END, v)
        tk.Button(self, text='OK', command=lambda:tkmb.showerror("Input Error", "Has to be between 1 to 3 options selected", parent=self)
                  if len(self.LB.curselection()) > 3 or len(self.LB.curselection()) < 1 
                  else disWin(self).display(self, [codeLst[i] for i in self.LB.curselection()],
                                      [nameLst[i] for i in self.LB.curselection()])).grid(row=2, column=0)
        
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
        
    def display(self, master, codeLst, nameLst):
        proc = []
        for i in range(len(codeLst)):
            p = mp.Process(target=loadFromWeb, args=(codeLst[i], ))
            proc.append(p)
            p.start()
        #pool = mp.Pool(len(codeLst))
        #pool.map(loadFromWeb, codeLst)
        #for i in range(len(processLst)):
            #processLst[i].join()
            #self.label['text'] = 'Fetching data for ' + str(len(codeLst)) + ' States(s)'
            #self.label.update() 
            #for d in data[i]['data']:
                #self.LB.insert(tk.END, nameLst[i] + ': ' + d['name'] + ' ' + d['designation'])            
            
    def browseFile(self):
        filename = filedialog.askdirectory()
        if filename == '':
            return
        if os.path.isfile(filename + '/parks.txt'):
            tkmb.showinfo("Browse File Notification", "parks.txt already existed and will be overwritten", parent = self)
            filename += '/parks.txt'
        if  filename == os.getcwd():
            filename = 'parks.txt'
        try:
            with open(filename, 'w', encoding="utf-8") as outfile:
                for dic in data:
                    for d in dic['data']:
                        outfile.write(d['fullName'] + '; ' + 
                                      ', '.join([(State_dict[state] if state in State_dict else state) for state in d['states'].split(',')]) 
                                      + '\n' + d['description'] + '\n\n')
        except FileNotFoundError:
            raise SystemExit
        self.destroy()

    
if __name__ == '__main__':
    mWin = mainWin()
    mWin.mainloop()