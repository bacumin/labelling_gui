#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 15:31:25 2017

@author: e84605

Function:  
    This program is a GUI created in tkinter to quickly label image data, and 
    output a python dict.
    
    To use it, run this file with the path to the directory containing all your 
    images as a command line argument (if no path is given the
    default images directory is "<current working directory>/images"). 

Features:
    - User can create custom labels, and assign a corresponding shortcut
    - Use the right and left key to flip through the photos, delete to clear an 
        image's labels
    - If checkbox "only 1 label" is on, the program will automatically navigate to
        the next image after 1 label is assigned.
    - Progress bar at the bottom tells you how many of the total files you have
        gone through.
    - Once the labelling is complete, use the "Save dictionary file" button to 
        save the dict file as a json in your current working directory.
        The key to the dict is the full path of the images, the values are
        lists of labels.

Credit:    Jeremy Lowery's code to create a slide show in tkinter was very helpful.
            Link: https://github.com/jeremylowery/slideshow/blob/master/slide.py
"""

import tkinter as tk
from tkinter import ttk
import os, sys
from PIL import ImageTk, Image

""" 
Checks if a command line argument was passed, or if it should use the default
file path to find images. Returns a list of file paths to the images.
"""
def get_images():
    if (len(sys.argv) > 1):
        dir_path=sys.argv[1]
        if(dir_path[-1]!="/"):
            dir_path+='/'
    else:
        dir_path=os.getcwd()+"/images/"
        
    im=os.listdir(dir_path)
    im_path=[(dir_path+k) for k in im]
    return(im_path)



class MainPage():
    
    """
    Set up initial GUI. Notice many of the page elements assigned as attributes,
    since they are updated or their elements are updated as the program runs.
    """
    def __init__(self):    
        #******* CREATE PANELS ******
        
            #Container for other frames, contains save dict button
        self.root=tk.Tk()
        self.root.pack_propagate(False)
        self.root.config(bg="#F0B67F", width=800, height=600)
        self.root.wm_title("Image Labeller")
        
            #Image frame contains image, nothing else
        s=tk.ttk.Style()
        s.configure('imgstyle.TFrame', background='#E0EDFC')
        self.imgframe = ttk.Frame(self.root, width=700, height=700, style='imgstyle.TFrame')
        self.imgframe.grid(row=0, column=0)
        self.imgframe.columnconfigure(0, weight=1)
        self.imgframe.rowconfigure(0, weight=1)
        
            #Contains next, prev, progress bar
        s2=tk.ttk.Style()
        s2.configure('bf.TFrame', background='#F0B67F')
        self.bottomframe = ttk.Frame(self.root, width=700, height=100, style='bf.TFrame')
        self.bottomframe.grid(column=0, row=1, sticky="nsew") # side=tk.BOTTOM, anchor='sw', fill=tk.BOTH)
        self.bottomframe.columnconfigure(10, weight=1)
        self.bottomframe.rowconfigure(10, weight=1)
        
            #Contains all the label settings
        s1=tk.ttk.Style()
        s1.configure('rf.TFrame', background='#ACCBE1', relief="solid")
        self.rightframe = ttk.Frame(self.root, width=300, height=500, style='rf.TFrame')
        self.rightframe.grid(row=0, column=1, sticky='nsew') #(side=tk.LEFT, fill=tk.BOTH)
        self.rightframe.columnconfigure(0, weight=1)
        self.rightframe.rowconfigure(0, weight=1)
        
        
        #******* IMAGE SETUP ****
        self._images = get_images()
        self._image_pos = -1
        self.image_dict = {}
        
        self.label = tk.Label(self.root, image=None)
        self.label.configure(borderwidth=0)
        self.label.pack()

        # ***** BOTTOM UI ******
        
            #shortcuts
        self.root.bind("<Right>", self.show_next_image)
        self.root.bind("<Left>", self.show_previous_image)
        self.root.bind("<Delete>", self.clear_label)

            #clear label, next and prev buttons
        but = tk.Button(self.bottomframe, text="Clear Labels", bg="#FAA916",
                             command=self.clear_label)
        but.pack(side="right", anchor="e")
        
        but = tk.Button(self.bottomframe, text="Next", bg="#FAA916",
                             command=self.show_next_image)
        but.pack(side="right", anchor="e")
        
        but = tk.Button(self.bottomframe, text="Prev", bg="#FAA916",
                             command=self.show_previous_image)
        but.pack(side="left", anchor="w")
        
            #progress bar
        prg_style=ttk.Style()
        prg_style.configure("red.Horizontal.TProgressbar", foreground="#FAA916", 
                            background="#FCA311")
        
        self.prgbar=ttk.Progressbar(self.bottomframe, orient=tk.HORIZONTAL,
                            length=100,maximum=len(self._images)+1, 
                                variable=self._image_pos, mode='determinate',
                                style="red.Horizontal.TProgressbar")
        self.prgbar.pack(side="top", anchor='s')
        
        #*******RIGHT LABEL UI *********
        
        labels=tk.Label(self.rightframe, background="#81b1d3", text="Label Settings",
                             borderwidth=2, relief="solid", font=("Helvetica", 16, "bold"))
        labels.pack(pady=(0,10), fill="x")
        
            # 1 label checkbox
        global one_lab
        one_lab=tk.IntVar() # variable is 1 if button selected, 0 otherwise
        self.check=tk.Checkbutton(self.rightframe, text="One Label Only", 
                                  bg="#ACCBE1",relief="solid", anchor="w",
                                  variable=one_lab)
        self.check.pack(fill="x", pady=10)
        
            #label entry
        new_lab=tk.Label(self.rightframe, text="New Label:", anchor='w',
                              bg="#ACCBE1")
        new_lab.pack(fill="x", padx=5, pady=(10,0))
        
        new_label=tk.StringVar()
        self.label_entry = ttk.Entry(self.rightframe, textvariable=new_label)
        self.label_entry.pack()
        
            #shortcut entry
        scut=tk.Label(self.rightframe, text="Shortcut:", anchor='w', 
                           bg="#ACCBE1"
                           )
        scut.pack(fill="x", padx=5)
        
        shortcut=tk.StringVar()
        self.shortcut_entry = ttk.Entry(self.rightframe, textvariable=shortcut)
        self.shortcut_entry.pack()
        
            #create label button
        but = tk.Button(self.rightframe, background="#ACCBE1", text="Create Label", 
                             command=lambda: self.create_label_but(new_label, shortcut))
        but.pack(fill="x", padx=5)
        
            #labels title (labels are automatically packed with button above)
        labels=tk.Label(self.rightframe, background="#ACCBE1", text="Labels",
                             borderwidth=1, relief="solid")
        labels.pack(pady=(35,0), fill="x")
        
        #*****Bottom right save file*****
        save_but=tk.Button(self.root, text="Save dictionary file", bg="#FAA916",
                           command=lambda: self.save_file())
        save_but.grid(column=1, row=1, sticky="e")
        
        
        #*****Loop*******
        self.root.mainloop()
          
""" 
Main page functions - these are all self explanatory unless specified. 
"""

    def clear_label(self, _):
        if(self._images[self._image_pos] in self.image_dict):
            del self.image_dict[self._images[self._image_pos]]
    
    def create_label_but(self, label, shortcut,  e=None):
        lab=custom_label(label.get())
        #past
        textt="Lab: "+label.get()+" | SC: " + shortcut.get()
        b = tk.Button(self.rightframe, text=textt, background="#ACCBE1", 
                      borderwidth=1, relief="ridge", 
                      command=lambda: self.label_custom(lab.get_label()) )
        b.pack(anchor="n")
        
        self.root.bind(shortcut.get(),lambda x: self.label_custom(lab.get_label()) )
        
    def save_file(self):
        import json
        with open('labelling.json', 'w') as fp:
            json.dump(self.image_dict, fp)
    
    # Add one of the user defined labels to an image.
    def label_custom(self, label):
        #case 1: there's only one label allowed, just replace it go to next
        if(one_lab.get() == 1):
            self.image_dict[self._images[self._image_pos]]=[label]
            self.show_next_image()
            
        else:
            #case 2: more than one label allowed, one label already added
            if(self._images[self._image_pos] in self.image_dict):
                self.image_dict[self._images[self._image_pos]]+=[label]
            
            #case 3: more than one label allowed, no label added yet
            else:
                self.image_dict[self._images[self._image_pos]]=[label]
 
                
    def show_next_image(self, e=None):
        fname=self.next_image()
        self.show_image(fname)
        self.prgbar.step()
    
    def show_previous_image(self, e=None):
        fname=self.previous_image()
        self.show_image(fname)
        self.prgbar.step(-1)
    
    #Show next image calls this to increment variables, and get file path. 
    # The two methods could easily be combined    
    def next_image(self):
        self._image_pos += 1
        self._image_pos %= len(self._images)
        return self._images[self._image_pos]
    
    def previous_image(self):
        self._image_pos -=1
        return self._images[self._image_pos]
    
    # Once methods have found file path and changed variable values, this renders
    # the next image in the right size, using fit to box and scaled size.
    def show_image(self, fname):
        self.original_image=Image.open(fname)
        self.image=None
        self.fit_to_box()

        if(self._image_pos == (len(self._images))):
            for widget in self.root.winfo_children():
                widget.destroy()
            
            dict_lab=tk.Label(self.root, text=self.image_dict)
            dict_lab.grid(row=1, column=3)
            
            finish_label=tk.Label(self.root, text="Finished with labelling")
            finish_label.grid(row=3, column=3)
            
    def fit_to_box(self):
        if self.image:
            if self.image.size[0] == self.box_width: return
            if self.image.size[1] == self.box_height: return
        width, height = self.original_image.size
        new_size = scaled_size(width, height, (self.box_width), (self.box_height))
        self.image = self.original_image.resize(new_size, Image.ANTIALIAS)
        self.label.place(x=self.box_width/2, y=self.box_height/2, anchor=tk.CENTER)
        tkimage = ImageTk.PhotoImage(self.image)
        self.label.configure(image=tkimage)
        self.label.image=tkimage
    
    @property
    def box_width(self):
        return self.imgframe.winfo_width()
    
    @property
    def box_height(self):
        return self.imgframe.winfo_height()


"""
Custom label object - these are created as the user creates custom labels. Created
as a separate object to keep track of all the different labels.
"""
class custom_label:
    def __init__(self, assigned_lab):
        self.assigned_label=assigned_lab
    
    def get_label(self):
        return self.assigned_label

# Helper method to render image and fit to box
def scaled_size(width, height, box_width, box_height):
    source_ratio = width / float(height)
    box_ratio = box_width / float(box_height)
    if source_ratio < box_ratio:
        return int(box_height/float(height) * width), box_height
    else:
        return box_width, int(box_width/float(width) * height)
    
    
#Initial startup
if __name__== '__main__': app=MainPage()