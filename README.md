# rits-nlp
## Python Question Answering Program

This program was written quite a while ago (2009) as a group project for an undergrad Artificial Intelligence course. 

It was originally made in Python 2.7, but I tweaked it to run in 3.4 before posting it here. The GUI is the original, so it's pretty outdated looking but still functional.

rits.py is the main file and the various txt files are the knowledge base. 

--------------------------------


#### Below is the paper that was sumbitted with this project:
##### _(with a few edits to make sense in this context)_

The RITS Question-Answering System is designed to answer questions about Truman’s 2009 MTCS faculty. Our system’s knowledge is a set of separate text files containing basic information on individual professors (i.e. office number, e-mail address, schedule). Regular expressions and pattern matching were the main tools used in creating RITS. 

By way of a graphical interface, users will enter their inquiry in a provided text box. For instance, the user might ask, “Where is Dr. Beck’s office?” The takeInput() function parses the query and uses regular expressions to decide what information to provide.  By seeing “dr” (or a related title such as “professor” or “prof”), RITS would know the following word, “beck,” indicated the text file that is needed. In the case that no title is provided, however, there is an error message as the system cannot provide information about an unknown professor. Another implementation of pattern matching then occurs as RITS searches through the query for certain question words and keywords. In the example question, “where” would be identified as the question word and “office” as the keyword. Now we must check to make sure the professor’s name matches one in our data. 

The output from takeInput() is then handed off as parameters in the checkName() function. This function only checks to see if the professor’s name is in the knowledge base. The question word and the keyword derived from takeInput() are only given to checkName() so they can be passed on to the next function, displayResult(). First RITS looks for a text file exactly matching the given professor’s name. If it is found, we move on to displayResult(). If it does not exist, it checks to see if perhaps there is more than one professor with that name, in which case a “1” would be attached at the end of the filename. If this is the case, RITS allows the user to select which professor he or she wants, and then the system sends that professor’s name as a parameter in displayResult(). However, should this return no match, an error message is displayed that the professor’s name could not be found in the database. 

Now for displayResult(). It first calls the readFile() function which opens the appropriate file and turns its information into a dictionary file type. RITS then uses patterns of question words and keywords in a series of if and else-if statements to answer the questions to the best of its ability. Again going with our example, since the question word is “where” and the keyword is “office,” RITS knows to retrieve the information stored in the dictionary beck[4]. Also if the question type (what, where, when) and keyword are unclear, the professor’s office, email address, and phone number are returned so the user can contact the professor to specifically ask his or her question. 

In order to create the graphical user interface for our system, we imported and used the Tkinter **(now called tkinter and updated in code)** package. The main code was based off of an example GUI written by Sébastien SAUVAGE, webmaster of http://sebsauvage.net, and modified to fit our program. Other smaller bits of code were written using Tkinter throughout the program to display information and ask for clarification. 

We also added an “I’m feelin’ Ritsy” button (an obvious spoof of Google’s “I’m feeling lucky” button). This brings up text that describes some helpful hints for using the RITS system. For example, it gives the details on what information is required as input, and therefore encourages the use of keywords. 
