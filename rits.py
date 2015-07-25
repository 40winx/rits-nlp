"""
The RITS Question-Answering System
Created by Winx (Rachelle Goll), Ian McGowan, Trieu Vo, and Suman Phuyal

Updated to run in Python3 by Winx Goll 07/2015

This program answers questions about Truman State University's
2009 MTCS faculty members using regular expressions.
"""

import re
import string
import os
import tkinter


#______________________________________________________________________________

## reads in a document and formats it into
## a dictionary.
def readFile(fileHandle, dictName): 
     line = fileHandle.readline()
     dictName = {} 
     keycounter = 1 
     while line: 
         key = str(keycounter) 
         dictName[key] = line 
         keycounter = keycounter + 1 
         line = fileHandle.readline() 
     return dictName

#______________________________________________________________________________

## Takes in the user's question and
## analyzes the information in it.
def takeInput(question):
    question = question.lower()
    ## Looks for words starting with "w,"
    ## specifically we're interested in question words
    ## like "where," "what," or "when".
    professor_name = ""
    p2 = re.compile(r'(^[w])([a-z]*)')
    sol2 = p2.search(question)
    if sol2:
        whq = sol2.group()
    else:
        whq = ""

    ## Uses regular expressions again to search for
    ## a title; then we can figure out the subject professor.
    p3 = re.compile('dr|prof|professor|proff')
    sol3 = p3.search(question)
    p4 = re.compile(r'\W+')
    if sol3:
        sol4 = question[sol3.end():]
        sol4 = p4.split(sol4)
        professor_name =  sol4[1]

        ## Looking for key words to help decipher the question's meaning.
        keyword = ""
        for word in p4.split(question):
             if word == "office" or word == "schedule" or word == "website" or word == "contact":
                  keyword = word
             if word == "e" or word == "email":
                  keyword = "e-mail address"
             if word == "telephone" or word == "phone":
                  keyword = "phone number"
             if word == "head" or word == "dean":
                  keyword = "department head"
    ## A special case: if the user asks for the department head.              
    else :
         for word in p4.split(question):
             if word == "head" or word == "dean" or word == "chair":
                  keyword = "department head"
                  professor_name = "dean"

    ## Error message: We can't look up information if we don't know the professor's name
         if (professor_name != "dean"):
             root = tkinter.Tk();
             root.title('Oops!')
             root.geometry('+500+350')
             tkinter.Label(root, text="\nI'm sorry, I don't quite understand your question.\n" +
                    "   Remember to include a professor's name (i.e., 'Dr. Beck').   \n" +
                    "For further assistance you can contact the MTCS office at: \n660-785-4547. \n" +
                              "For hints on how to use the RITS Q&A program, \nclick the 'I'm Feelin' Ritsy' button. \n",
                              font=(16), fg = "white", bg = "purple").pack(pady=20)
             tkinter.Button(root, text="Retry", font=(16), command= root.destroy).pack(side= tkinter.RIGHT)
             root.mainloop()

     ## Before we can answer, we need to
     ## make sure the professor's name is valid or if there
     ## are more than one prof with that last name.
    checkName(whq,professor_name,keyword)

#______________________________________________________________________________
    
def checkName(qword, pname, keyword):
     ## First we check if the name given is a file
     ## in our database.
     try:
          filename = pname + ".txt"
          fpointer = open(filename)
          displayResult(qword, pname, keyword)
     except IOError:
          ## If not, we must check to see if two professors
          ## share that last name.
          try:
               filename1 = pname + "1.txt"
               fpointer1 = open(filename1)
               d1 = readFile(fpointer1,pname + "1")
               filename2 = pname + "2.txt"
               fpointer2 = open(filename2)
               d2 = readFile(fpointer2,pname + "2")
               root = tkinter.Tk();
               root.title('Double Trouble!')
               root.geometry('+500+350')
               tkinter.Label(root, text="\n There are two professors \nwith that last name. \n" +
                             " Please indicate which \nyou're asking about. \n",
                      font=(16), fg = "white", bg = "purple").pack(side= tkinter.LEFT)

               tkinter.Button(root, text=(d1['1'][:-1]), font=(16),
                              command= lambda x = qword, y= pname + "1", z=keyword: displayResult(x,y,z)).pack(side= tkinter.RIGHT)
               tkinter.Button(root, text=(d2['1'][:-1]), font=(16),
                              command= lambda x = qword, y= pname + "2", z=keyword: displayResult(x,y,z)).pack(side= tkinter.RIGHT)               

          ## If that is also not the case, we know that
          ## the name isn't in our database. 
          except IOError:
               root = tkinter.Tk();
               root.title("Who's that?")
               root.geometry('+500+350')
               tkinter.Label(root, text="\n I'm sorry but I don't know that person. " +
                             "\n Please make sure to check your spelling. \n" +
                             "For hints on how to use the RITS Q&A program, \nclick the 'I'm Feelin' Ritsy' button. \n",
                           font=(16), fg = "white", bg = "purple").pack(side= tkinter.LEFT)
               tkinter.Button(root, text="Retry", font=(16), command= root.destroy).pack(side= tkinter.RIGHT)
               root.mainloop()

#______________________________________________________________________________
              
## Now we can formulate the answer.
def displayResult(qtype,pname,keyword):
     ## First we read in the document.
     filename = pname + ".txt"
     fpointer = open(filename)
     d = readFile(fpointer,pname)
     root = tkinter.Tk();
     root.title('Double Trouble!')
     root.geometry('+500+350')
     tkinter.Button(root, text="Retry", font=(16), command= root.destroy).pack(side= tkinter.RIGHT)
     
     ## Then we use patterns and the keywords
     ## to answer the question to the best of our ability.
     if keyword == "office" and (qtype == "where" or qtype == "where" or qtype == "what"):
        tkinter.Label(root, text=("\n " + d['1'][:-1] +  "\'s office is in " + d['4'][:-1] + ". \n"),
                      font=(16), fg= "white", bg = "purple").pack(side= tkinter.LEFT)
     elif qtype == "what" and keyword == "schedule" or qtype == "when":
        tkinter.Label(root,text=("\n " + d['1'][:-1] +  "\'s schedule is  \n" + d['7'][:-1] + ". \n"),
                      font=(16), fg= "white", bg = "purple", anchor="w").pack(side= tkinter.LEFT)
     elif qtype == "what" and (keyword == "phone number" or keyword == "e-mail address" or keyword == "website"):
          num = changeNumber(keyword)
          for i in d.keys():
               if ( i == str(num) ):
                    tkinter.Label(root, text=("\n " + d['1'][:-1] + "\'s " + keyword + " is " + d[i][:-1] + ". \n"),
                      font=(16), fg= "white", bg = "purple").pack(side= tkinter.LEFT)
     elif keyword == "department head":
          tkinter.Label(root,text=("\n Department head of Math and Computer Information is as Follows\n"
                                   + "Name: " + d['1'][:-1] + "\nOffice: " + d['4'][:-1] + "," +
                                   "\nEmail: " + d['6'][:-1] + ",\nPhone: " + d['5'][:-1] + ". \n"),
                      font=(16), fg= "white", bg = "purple", anchor="w").pack(side= tkinter.LEFT)
     else:
          if keyword != "contact":
               tkinter.Label(root,text=("\n ""I'm sorry, but I don't know the answer to your question. \n" +
                                        " Please try asking your question in a different way, or for further assistance, \n" +
                                        d['1'][:-1] + "\'s contact information is as follows: \nOffice: " + d['4'][:-1] + "," +
                                        "\nEmail: " + d['6'][:-1] + ",\nPhone: " + d['5'][:-1] + ". \n"),
                      font=(16), fg= "white", bg = "purple", anchor="w").pack(side= tkinter.LEFT)
          else:
               tkinter.Label(root,text=("\n " + d['1'][:-1] + "\'s contact information is as follows: \nOffice: " + d['4'][:-1] + "," +
                                   "\nEmail: " + d['6'][:-1] + ",\nPhone: " + d['5'][:-1] + ". \n"),
                      font=(16), fg= "white", bg = "purple", anchor="w").pack(side= tkinter.LEFT)

#______________________________________________________________________________

## Allows for easy access to dictionary information
## by way of the keyword
def changeNumber(keyword):
     if keyword == "office":
          return 4
     if keyword == "e-mail address":
          return 6
     if keyword == "phone number":
          return 5
     if keyword == "schedule":
          return 7
     if keyword == "website":
          return 8

#______________________________________________________________________________
##
## GRAPHICS
##
#______________________________________________________________________________


## modified version of GUI code from http://sebsauvage.net/python/gui/

class start_screen(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.geometry('+500+350')
        self.grid()
        tkinter.Frame(bg="purple")

        self.entryVariable = tkinter.StringVar()
        self.entry = tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='NESW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Ask RITS your question.")

        button = tkinter.Button(self,text=u" ASK ",
                                command=self.OnButtonClick, bg= "white", fg= "purple")
        button.grid(column=1,row=0)
        button2 = tkinter.Button(self,text=u"QUIT",
                                command=self.destroy, bg= "white", fg= "purple")
        button2.grid(column=1,row=1)

        button2 = tkinter.Button(self,text=u"     I'm Feelin' Ritsy!       ",
                                command=rules, bg= "white", fg= "purple")
        button2.grid(column=0,row=2, columnspan=2)

        self.labelVariable = tkinter.StringVar()
        label = tkinter.Label(self,textvariable=self.labelVariable,font=(16),
                              anchor="w",fg="white",bg="purple")
        label.grid(column=0,row=1,sticky='NESW')
        self.labelVariable.set(u"Answering all your TSU MTCS faculty questions since 2009")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)
        
    def OnButtonClick(self):
        takeInput( self.entryVariable.get())

    def OnPressEnter(self,event):
        takeInput( self.entryVariable.get())

def rules():
     root = tkinter.Tk();
     root.title('Rules of RITS')
     root.geometry('+500+350')
     ritsRules = open("rits_rules.txt").read()
     label = tkinter.Label(root, justify= tkinter.LEFT, text= ritsRules, font=(16), fg= "white", bg = "purple").pack(side= tkinter.LEFT)


if __name__ == "__main__":
    app = start_screen(None)
    app.title('RITS Q&A')
    app.mainloop()

