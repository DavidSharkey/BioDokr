from Tkinter import *
from subprocess import call
from datetime import datetime
import json
import subprocess
import tkFileDialog
import fileinput
import os,stat

# Create new shell script with timestamp
new_s = str(datetime.today()) + ".sh"
new_sh = new_s.replace(' ', '')
subprocess.call(["touch", new_sh])

# Copy contents of process.sh to new shell script
with open("process.sh") as t:
	l = t.readlines()
	l = [x for x in l]
	with open(new_sh, "w") as t2:
		t2.writelines(l)

# Change permissions of new shell script	
os.chmod(new_sh,stat.S_IRWXU)


# Load parameters from JSON files:

with open("parameters/augustus.json", "r") as aparams:
    p = json.load(aparams)

with open("parameters/interproscan.json", "r") as iparams:
    i = json.load(iparams)



root = Tk()
root.title("BioDokr")


# Species Dropbox
l1 = StringVar()
la1 = Label(root, textvariable=l1)
l1.set("Choose Species")
la1.grid(row = 0, column = 0) 


ex1 = StringVar(root)
ex1.set("human")

# Load paramters from JSON into GUI
option = OptionMenu(root, ex1, *p["organism"])
option.grid(row = 1, column = 0, pady = 10)

# Strand Dropbox
l2 = StringVar()
la2 = Label(root, textvariable=l2)
l2.set("Choose Strand")
la2.grid(row = 2, column =0)


ex2 = StringVar(root)
ex2.set("both")
option1 = OptionMenu(root, ex2, *p["strand"])
option1.grid(row = 3, column = 0, pady = 10)

# Genemodel Dropbox
l3 = StringVar()
la3 = Label(root,textvariable=l3)
l3.set("Choose Gene Model")
la3.grid(row = 4, column = 0)


ex3 = StringVar(root)
ex3.set("partial")
option2 = OptionMenu(root, ex3, *p["genemodel"])
option2.grid(row = 5, column = 0)


# Checkbox for including InterProScan
var = IntVar()
inte = Checkbutton(root, text="Include InterProScan", variable=var).grid(row = 6, column = 0, padx = 10, pady = 10)


l4 = StringVar()
la4 = Label(root, textvariable=l4)
l4.set("Choose Interproscan Output Type")
la4.grid(row = 7, column = 0)


# File extention for InterProScan
ex5 = StringVar(root)
ex5.set("tsv")
option5 = OptionMenu(root, ex5, *i["file"])
option5.grid(row = 8, column = 0)


l5 = StringVar()
la5 = Label(root, textvariable=l5)
l5.set("Choose Organism Type")
la5.grid(row = 10, column = 0)


ex4 = StringVar(root)
ex4.set("euk")
option4 = OptionMenu(root, ex4, *s["type"])
option4.grid(row = 11, column = 0)



# This function creates a "master" string out of all the selected tools and paramters. 
# The string will always start with augustus parameters and a mixture of the other three tools
# The string is subsequently sent to process.sh for processing.
def choice():
    param1 = ex1.get()
    param2 = ex2.get()
    param3 = ex3.get()
	
    # Augustus parameters
    augp = param1 + " " + param2 + " " + param3


    if var.get() == 1:
        inter = "interproscan" + " " + ex5.get()

    else:
        inter = ""
    
    fi = "./" + new_sh
    masterp = augp + " " + inter + " " + sign + " " + tmh
    subprocess.call([fi, masterp])
    root.quit()

# This function asks the user for the input file
def choose():

	root.input=tkFileDialog.askopenfilename(initialdir="/home/me/", title="Please choose an input", filetypes=(("fa", "*.fa"),("all", "*.*")))
	file_dir = root.input
	new_input = 'input=' + file_dir
	
	# Path of input file is added to new shell script (shell script with timestamp)
	for i in fileinput.input(new_sh, inplace=True):
		print i.replace('input=""', new_input),
	
# This function asks the user for the directory for the Output folder to be saved
def chooseDir():

	root.save = tkFileDialog.askdirectory()
	directory = root.save
	new_dir = 'save_dir=' + directory

	# Path of Output folder is added to the new shell script
	for i in fileinput.input(new_sh, inplace=True):
		print i.replace('save_dir=""', new_dir),


button1 = Button(root, text="Choose File", command=choose).grid(row = 13, column = 0, padx = 10, pady = 10) 
button2 = Button(root, text="Choose Save Location", command=chooseDir).grid(row = 14, column = 0)
button3 = Button(root, text="Start", command=choice).grid(row = 15, column = 0, padx = 10, pady = 10)

mainloop()








