import urllib.request as ur
import requests
from bs4 import BeautifulSoup 
import re
import time
import collections
import json
import threading
import tkinter as tk
import tkinter.messagebox as tkmb

with open('states_hash.json', 'r') as infile:
    State_dict = json.load(infile)
codeLst = list(State_dict.keys())
nameLst = list(State_dict.values())
API_key = "11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg"

class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        tk.Label(self, text="Select up to 3 States").grid(row = 0, column = 0)
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
        self.data = {}
        self.LB = tk.Listbox(self, width=50, height=10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        self.LB.grid(row = 0, column = 0)
        tk.Button(self, text='OK', command=self.destroy).grid(row=1, column=0)
    def display(self, master, codeLst, nameLst):
        threadLst = []
        for i in range(len(codeLst)):
            print(codeLst[i], nameLst[i])
            t = threading.Thread(target=self.loadFromWeb, args=(codeLst[i],), name=nameLst[i])
            threadLst.append(t)
        i = 3
        for t in threadLst: 
            t.start()
            t.join()
            tk.Label(master, text='').grid(row=i, column=0)                        
            tk.Label(master, text=t.getName() + ": " + self.data['total']).grid(row=i, column=0)            
            for d in self.data['data']:
                self.LB.insert(tk.END, d['name'] + ' ' + d['designation'])            
            i += 1
    def loadFromWeb(self, StateCode):
        lock = threading.Lock()
        with lock:
            page = requests.get("https://developer.nps.gov/api/v1/parks?stateCode=" + 
                                StateCode + "&api_key=" + API_key)
            self.data = page.json()
mWin = mainWin()
mWin.mainloop()