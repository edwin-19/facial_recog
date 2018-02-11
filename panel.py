# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 15:32:29 2017

@author: Edwin
"""

from tkinter import *

class App:
  def __init__(self, master):
    frame = Frame(master,  width=250, height=250)
    frame.pack()
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=quit, height = 10, width = 30)
    self.button.pack(side=BOTTOM)
    self.slogan = Button(frame,
                         text="Hello",
                         command=self.write_slogan, height = 10, width = 30)
    self.slogan.pack(side=LEFT)
  def write_slogan(self):
    print("Tkinter is easy to use!")

root = Tk()
app = App(root)
root.mainloop()
