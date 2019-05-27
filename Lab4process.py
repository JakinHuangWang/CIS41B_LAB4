import requests
from bs4 import BeautifulSoup 
import sys
import os
def gui2fg():
    """Brings tkinter GUI to foreground on MacCall gui2fg() after creating main window and before mainloop() start"""
    if sys.platform == 'darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))
from multiprocessing import Pool

#with open('states_hash.json', 'r') as infile:
    #State_dict = json.load(infile)
    
#codeLst = list(State_dict.keys())
#nameLst = list(State_dict.values())
#API_key = "11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg"
#data = []

#class mainWin(tk.Tk):
    #def __init__(self):
        #super().__init__()
        #tk.Label(self, text="Select up to 3 States").grid(row = 0, column = 0)
        #self.LB = tk.Listbox(self, height = 10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        #self.LB.grid(row = 1, column = 0)
        #for v in State_dict.values():
            #self.LB.insert(tk.END, v)
        #tk.Button(self, text='OK', command=lambda:tkmb.showerror("Input Error", "Has to be between 1 to 3 options selected", parent=self)
                  #if len(self.LB.curselection()) > 3 or len(self.LB.curselection()) < 1 
                  #else disWin(self).display(self, [codeLst[i] for i in self.LB.curselection()],
                                      #[nameLst[i] for i in self.LB.curselection()])).grid(row=2, column=0)
        
#class disWin(tk.Toplevel):
    #def __init__(self, master):
        #super().__init__(master)
        #self.LB = tk.Listbox(self, width=50, height=10, selectmode = 'multiple', yscrollcommand = tk.Scrollbar(self).set)
        #self.LB.grid(row = 0, column = 0)
        #tk.Button(self, text='OK', command=self.browseFile).grid(row=1, column=0)
        #self.label = tk.Label(master, text='')
        #self.label.grid(row = 3, column = 0)         
        #self.protocol("WM_DELETE_WINDOW", self.eraseLabel)
        
    #def eraseLabel(self):
        #self.label['text'] = ''
        #self.destroy()
        
    #def display(self, master, codeLst, nameLst):
        #processLst = []       
        #for i in range(len(codeLst)):
            #print(codeLst[i], nameLst[i])
            #p = mp.Process(target=loadFromWeb, args=(codeLst[i],), name=nameLst[i])
            #p.start()
            #p.join()
        ##for i in range(len(processLst)):
            ##processLst[i].join()
            ##self.label['text'] = 'Fetching data for ' + str(len(codeLst)) + ' States(s)'
            ##self.label.update() 
            ##for d in data[i]['data']:
                ##self.LB.insert(tk.END, nameLst[i] + ': ' + d['name'] + ' ' + d['designation'])            
            
    #def browseFile(self):
        #filename = filedialog.askdirectory()
        #if filename == '':
            #return
        #if os.path.isfile(filename + '/parks.txt'):
            #tkmb.showinfo("Browse File Notification", "parks.txt already existed and will be overwritten", parent = self)
            #filename += '/parks.txt'
        #if  filename == os.getcwd():
            #filename = 'parks.txt'
        #try:
            #with open(filename, 'w', encoding="utf-8") as outfile:
                #for dic in data:
                    #for d in dic['data']:
                        #outfile.write(d['fullName'] + '; ' + 
                                      #', '.join([(State_dict[state] if state in State_dict else state) for state in d['states'].split(',')]) 
                                      #+ '\n' + d['description'] + '\n\n')
        #except FileNotFoundError:
            #raise SystemExit
        #self.destroy()

base_url = 'https://developer.nps.gov/api/v1/parks?stateCode=DE&api_key=11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg'

all_urls = list()

def generate_urls():
    for i in range(3):
        all_urls.append(base_url)
        
def loadFromWeb(StateCode):
    page = requests.get('https://developer.nps.gov/api/v1/parks?stateCode=DE&api_key=11hZnAoJ398zWsTjp6HhqCIhlblofgLwSUsB1EJg')
    print(page.status_code, page.url)
    
generate_urls()
pool = Pool(3)
pool.map(loadFromWeb, all_urls)
pool.terminate()
pool.join()
    
#mWin = mainWin()
#mWin.mainloop()