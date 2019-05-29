'''
Lab4thread.py
Author: Jakin Wang
Description: Lab4 uses the NPS to create a GUI and utilizing threading 
that allows the users to view all the parks in a certain state
'''
import requests
import json
import os
import threading
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as tkmb

#This is my Key for the NPS API
API_key = "11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg"

#The Main Window creates a listbox which allows the users to choose 1 - 3 states to view the parks.
class mainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        with open('states_hash.json', 'r') as infile:
            State_dict = json.load(infile)
            self.codeLst = list(State_dict.keys())
            self.nameLst = list(State_dict.values())
        self.data = []
        self.title("US National Parks")
        tk.Label(self, text="Select up to 3 States").grid(row = 0, column = 0)
        self.LB = tk.Listbox(self, height = 10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        self.LB.grid(row = 1, column = 0)
        self.LB.insert(tk.END, *self.nameLst)
        self.label = tk.Label(self, text='')
        self.label.grid(row = 3, column = 0) 
        tk.Button(self, text='OK', command=lambda:self.fetch([self.codeLst[i] for i in self.LB.curselection()],
                                      [self.nameLst[i] for i in self.LB.curselection()]) if 1 <= len(self.LB.curselection()) <= 3
                                    else tkmb.showerror("Input Error", "Has to be between 1 to 3 options selected", parent=self)).grid(row=2, column=0)

    def fetch(self, codeSelect, nameSelect):
        self.data.clear()
        threadLst = []
        self.label['text'] = ''
        self.label.update()        
        for i in range(len(codeSelect)):
            t = threading.Thread(target=self.loadFromWeb, args=(codeSelect[i], nameSelect[i]), name=nameSelect[i])
            threadLst.append(t)
        output = 'Result: '
        for i in range(len(threadLst)): 
            t = threadLst[i]
            t.start()
            t.join()
            output += t.getName() + ": " + self.data[i][1]['total'] + '\t'
            self.label['text'] = output
            self.label.update()
        disWin(self).display(self.data)
        
    #Loab data from the web using NPS API           
    def loadFromWeb(self, StateCode, StateName):
        lock = threading.Lock()
        with lock:
            page = requests.get("https://developer.nps.gov/api/v1/parks?stateCode=" + 
                                StateCode + "&api_key=" + API_key)
            self.data.append((StateName, page.json()))
            
#The Display Window displays all the state parks chosen by the user     
class disWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.data = []
        self.title('Display Window')
        self.LB = tk.Listbox(self, width=50, height=10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        self.LB.grid(row = 0, column = 0)
        tk.Button(self, text='OK', command=lambda: self.browseAndWriteFile() if len(self.LB.curselection()) >= 1
                    else tkmb.showerror("Error Message", "Please select at least 1 choice")).grid(row=1, column=0)     
        self.protocol("WM_DELETE_WINDOW", lambda:self.eraseLabel(master))
        self.grab_set()
        self.focus_set()
    
    #clear the label and destroy the display window    
    def eraseLabel(self, master):
        master.label['text'] = ''
        master.label.update()
        self.destroy()
        
    #Display all the state parks by using threads to scrap the web    
    def display(self, data):
        self.data = data
        for tup in self.data:
            self.LB.insert(tk.END, *[tup[0] + ': ' + d['fullName'] for d in tup[1]['data']])            
    
    #Loab data from the web using NPS API           
    def loadFromWeb(self, StateCode):
        lock = threading.Lock()
        with lock:
            page = requests.get("https://developer.nps.gov/api/v1/parks?stateCode=" + 
                                StateCode + "&api_key=" + API_key)
            self.data.append(page.json())
            
    #Allows the users to choose a directory to write the parks.txt        
    def browseAndWriteFile(self):
        choices = [(self.data[i][0], d) for i in range(len(self.data)) for d in self.data[i][1]['data'] ]
        filename = filedialog.askdirectory()
        if filename == '':
            return
        if os.path.isfile(filename + '/parks.txt'):
            tkmb.showinfo("Browse File Notification", "parks.txt already existed and will be overwritten", parent = self)
        filename += '/parks.txt'
        if  filename == os.getcwd():
            filename = '/parks.txt'
        try:
            with open(filename, 'w', encoding="utf-8") as outfile:
                outfile.writelines([choices[num][1]['fullName'] + '; ' + choices[num][0]
                                      + '\n' + choices[num][1]['description'] + '\n\n' 
                                      for num in self.LB.curselection()])
        except FileNotFoundError:
            raise SystemExit
        self.destroy()

if __name__ == '__main__':            
    mWin = mainWin()
    mWin.mainloop()