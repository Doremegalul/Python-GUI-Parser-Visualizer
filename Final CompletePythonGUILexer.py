# Python Library
import re
from tkinter import *
from tkinter import ttk  

# -= class definition =-
class MyFirstGUI: 

  # -= Function Description: =-
  # This is the main GUI interface with titles, entry, buttons, and global variables
    def __init__(self, root):

      #  --------------------Titles--------------------
      # GUI: Delta Version 12.13
      self.master = root
      self.master.title("GUI: Delta Version 12.13")                                    

      # Source Code Input: 
      self.inputlabel = Label(self.master, text = "Source Code Input: ") 
      self.inputlabel.grid(row = 0, column = 0 , sticky = W)

      # Token Output: 
      self.outputlabel = Label(self.master, text = "Token Output: ")            
      self.outputlabel.grid(row = 0, column = 2, sticky = W)

      # Parse Tree:  
      self.parselabel = Label(self.master, text = "Parse Tree: ")            
      self.parselabel.grid(row = 0, column = 4, sticky = W)

      # Visualization Tree:
      self.visualizationtreelabel = Label(self.master, text=" Treeview(hierarchical)")
      self.visualizationtreelabel.grid(row=2, column=2, sticky=W)
      
      # Current Processing Line:
      self.currentlabel = Label(self.master, text = "Current Processing Line: ")         
      self.currentlabel.grid(row = 4, column = 0, sticky = W)

      #  --------------------Entry--------------------
      # Source Code Input Box
      self.copyinput = Text(self.master, width = 55, height = 30)                
      self.copyinput.grid(row = 1, column = 0, columnspan = 2, sticky = E)

      # Token Output Box
      self.pasteoutput = Text(self.master, width = 40, height = 30)                     
      self.pasteoutput.grid(row=1, column = 2, columnspan = 2, sticky=E)    

      # Current Processing Line Box
      self.currentoutput = Entry(self.master)                                             
      self.currentoutput.grid(row=4, column = 1, sticky=E)               

      # Parse Tree Box
      self.parseoutput = Text(self.master, width = 55, height = 30)             
      self.parseoutput.grid(row=1, column=4, columnspan = 2, sticky=E)

      # Visualization Tree Box
      self.visualizationtreeoutput = ttk.Treeview(self.master)
      self.visualizationtreeoutput.grid(row=3, column=2, sticky=E)

      #  --------------------Buttons--------------------
      # Next Line Button
      self.nextline = Button (self.master, text = "Next Line", command=self.NextLine)
      self.nextline.grid(row=5,column=0, sticky=W)    

      # Quit Button
      self.nextline = Button (self.master, text = "Quit", command=self.QuitProgram)   
      self.nextline.grid(row=5,column=3, columnspan = 3, sticky=E)     

      #  --------------------Global Variables--------------------
      self.counter = 0
      self.Mytokens = []
      self.inToken = ("empty", "empty")

    # -= Function Description: =-
    # This is to read the user inputs and run it to other function to insert it in other boxes
    def NextLine(self):
        self.clear_treeview()
        #Copy the user inputs
        getuserinput = self.copyinput.get("1.0", "end-1c")
        #Get the user input lines
        lines = getuserinput.split('\n')

        #If there is still a user input to check
        if self.counter < len(lines): 

            #The current lines input
            currentlines = lines[self.counter]

            #Insert into the [Token Output Box]
            self.pasteoutput.insert("end", f"--------------------Below is case--------------------\n{currentlines}\n\n")

            #Get the list using [CutOneLineTokens] functions
            gettokenlist = self.CutOneLineTokens(currentlines)  

            #If there is anything left in the list
            if gettokenlist: 
                #Insert the lists into the [Token Output Box]
                self.pasteoutput.insert("end", "\n\n".join(gettokenlist) + "\n\n")

                #Update the counter in the [Current Processing Line Box]
                self.currentoutput.delete(0, "end")
                self.counter += 1
                self.currentoutput.insert(0, self.counter)

                #Go to the [parser] functions
                self.parser()
              
            #Else there isn't anything left in the list
            else: 
                print ("The list is empty")
        #Else, there is no more input 
        else:
            print ("Working Progress on the error")

    #Function Description: 
    #The behind button to quit out the GUI
    def QuitProgram(self):                                                                 
        self.master.destroy()   #Termintated the program
        self.master.quit()  #Quit the program 

    #Function Descrition: To find the Tinypie definition token in the string and add it to the list to return later
    def CutOneLineTokens(self, testStr):
        tokenList = []

        tokenPatterns = [   #The list of token patterns for the loop
            (r'"(.*?)"', 'lit_string'),
            (r'\b(if)?(else)?(float)?(int)?(while)?\b', 'key'),
            (r'(\=)?(\+)?(\>)?(\*)?', 'op'), 
            (r'(\(|\)|:|"|;|<|>)', 'sep'),
            (r'\d+\.\d+', 'lit_float'),
            (r'\b\d+\b', 'lit_int'),
            (r'[a-zA-Z]+[a-zA-Z0-9]', 'id')
        ]

        while testStr:  #While there is a string
            for num, (pattern, token_type) in enumerate(tokenPatterns): #Go through the list of token patterns
                testStr = testStr.strip()   #Remove any whitespaces
                matchToken = re.match(pattern, testStr) #Check if match the current token patterns
                if matchToken:  #If it is matched, group them to remove the full description of match
                    resultMatchToken = matchToken.group()
                    if resultMatchToken:    #If there is something after group, then check if it a string with quote or something else
                        if token_type == 'lit_string': #If it a string, remove the quote and the whitespace and add the quote manually while the string with the token type into the list
                            quote = resultMatchToken[1:-1]
                            quote = quote.strip()
                            tokenList.extend(['<sep,">', f'<{token_type},{quote}>', '<sep,">']) #Extend is append with adding mutiple stuff into the list instead one by one
                        else: #Else, add the string with the token type into the list
                            tokenList.append(f'<{token_type},{resultMatchToken}>')
                    testStr = testStr.replace(matchToken.group(), "", 1)    #Remove the whitespace in the string

            if testStr == "":   #If the string is empty, then break out
                break

        temp_Mytokens = []        
        for token_string in tokenList:
            # Remove the angle brackets and split the string at the comma
                type_value = token_string.strip('<>').split(',')
                if len(type_value) == 2:
                    temp_Mytokens.append((type_value[0], type_value[1]))

        self.Mytokens = temp_Mytokens

        print("Printing the list of Mytokens: ", self.Mytokens)

        print("Printing the list of tokenList: ", tokenList)

        return tokenList   #Return the list

    def accept_token(self):
        #global inToken
        if self.Mytokens:
            print("     accept token from the list:" + self.inToken[1])
            self.parseoutput.insert("end", "     accept token from the list:" + self.inToken[1] + "\n")
            self.inToken = self.Mytokens.pop(0)
        else:
            #print("No more tokens to accept.")
            self.parseoutput.insert("end", "\n")
            return

    def multi(self, token_node_id): 
        print("----parent node multi, finding children nodes: " + "\n")
        self.parseoutput.insert("end", "\n" + "----parent node multi, finding children nodes: " + "\n")
        #global inToken
      
        if (self.inToken[0] == "lit_int"):
            print("child node (internal): int")
            self.parseoutput.insert("end", "child node (internal): int" + "\n")
            print("   int has child node (token):" + self.inToken[1])
            self.parseoutput.insert("end","   int has child node (token):" + self.inToken[1] + "\n")

            sub_token_node_id = token_node_id + 'levelA-4-1' # int | levelB-4-1 int
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text='int') 

            under_sub_token_node_id = sub_token_node_id + 'levelA-5-1' # 5 | levelB-5-2 2
            self.visualizationtreeoutput.insert(sub_token_node_id, 'end', under_sub_token_node_id, text = self.inToken[1]) 
        
            self.accept_token()
          
        elif (self.inToken[0] == "lit_float"): 
            print("child node (internal): float")
            self.parseoutput.insert("end","child node (internal): float" + "\n")
            print("   float has child node (token):" + self.inToken[1])
            self.parseoutput.insert("end","   float has child node (token):" + self.inToken[1] + "\n")
          
            sub_token_node_id = token_node_id + 'levelA-4-5' # float | levelB-4-1 float
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text='float') 

            under_sub_token_node_id = sub_token_node_id + 'levelA-5-4' # 2.1 | levelB-5-1 4.1
            self.visualizationtreeoutput.insert(sub_token_node_id, 'end', under_sub_token_node_id, text = self.inToken[1]) 
          
            self.accept_token()
            
        if (self.inToken[1] == "*"):
            print("child node (token):" + self.inToken[1])
            self.parseoutput.insert("end","child node (token):" + self.inToken[1] + "\n")
            sub_token_node_id = token_node_id + 'levelA-4-2' # op | levelB-4-4  op
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text='op') 

            under_sub_token_node_id = sub_token_node_id + 'levelA-5-2' # * | levelB-5-3 *
            self.visualizationtreeoutput.insert(sub_token_node_id, 'end', under_sub_token_node_id, text = self.inToken[1]) 
          
            self.accept_token()
            if (self.inToken[0] == "lit_float"):
                print("child node (internal): float")
                self.parseoutput.insert("end","child node (internal): float" + "\n")
                print("   float has child node (token):" + self.inToken[1])
                self.parseoutput.insert("end","   float has child node (token):" + self.inToken[1] + "\n")
              
                sub_token_node_id = token_node_id + 'levelA-4-3' # float | levelB-4-5 float 
                self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text='float') 

                under_sub_token_node_id = sub_token_node_id + 'levelA-5-3' # 4.3 | levelB-5-4 5.5
                self.visualizationtreeoutput.insert(sub_token_node_id, 'end', under_sub_token_node_id, text = self.inToken[1]) 
                self.accept_token()

    def math(self):
        print("\n----parent node math, finding children nodes:")
        self.parseoutput.insert("end","\n" + "----parent node math, finding children nodes:" + "\n")
 
        key_node_id = 'levelA-2-4' # math | levelB-2-4 math 
        self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text = 'math')
      
        if (self.inToken[0] == "lit_int" or self.inToken[0] == "lit_float"):
            print("child node (internal): multi")
            self.parseoutput.insert("end","child node (internal): multi" + "\n")

            token_node_id = key_node_id + '_' + 'levelA-3-1' # multi | levelB-3-4 multi
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='multi')
 
            self.multi(token_node_id) 
            if(self.inToken[0] == "lit_int"):
                print("child node (internal): int")
                self.parseoutput.insert("end","child node (internal): int" + "\n")
                print("   int has child node (token):" + self.inToken[1])
                self.parseoutput.insert("end","   int has child node (token):" + self.inToken[1] + "\n")

              
                self.accept_token()
              
            if(self.inToken[0] == "lit_float"):
                print("child node (internal): float")
                self.parseoutput.insert("end","child node (internal): float" + "\n")
                print("   float has child node (token):" + self.inToken[1])
                self.parseoutput.insert("end","   float has child node (token):" + self.inToken[1] + "\n")

              
                self.accept_token()    
              
            if (self.inToken[1] == "+"):
                print("\n----parent node math, finding children nodes:")
                self.parseoutput.insert("end","\n" + "----parent node math, finding children nodes:" + "\n")
                print("   op has child node (token):" + self.inToken[1])
                self.parseoutput.insert("end","   op has child node (token):" + self.inToken[1] + "\n")
              
                token_node_id = key_node_id + '_' + 'levelB-3-2' # op
                self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='op')
                sub_token_node_id = token_node_id + 'levelB-4-2' # +
                self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text=self.inToken[1]) 
              
                self.accept_token()
              
                print("\n----parent node math, finding children nodes:")
                self.parseoutput.insert("end","\n" + "----parent node math, finding children nodes:" + "\n")
                print("child node (internal): multi")
                self.parseoutput.insert("end","child node (internal): multi" + "\n")

                token_node_id = key_node_id + '_' + 'levelB-3-3' # multi
                self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='multi')
              
                self.multi(token_node_id)
            else:
                print("error, you need + after the int in the math")
                self.parseoutput.insert("end","error, you need + after the int in the math" + "\n")
        else:
            print("error, math expects float or int")
            self.parseoutput.insert("end","error, math expects float or int" + "\n")

    def exp(self):

        print("\n----parent node exp, finding children nodes:")
        self.parseoutput.insert("end","----parent node exp, finding children nodes: " + "\n")

        typeT, token = self.inToken
        if_token = token
        print_token = token

        # First level, exp
        self.visualizationtreeoutput.insert('', 'end', 'level1', text = "exp") 
       
        if (token == "if"):  # Third Input, the if
            print("child node (internal): key")
            self.parseoutput.insert("end","child node (internal): key" + "\n")
            print("   key has child node (token):" + token)
            self.parseoutput.insert("end","   key has child node (token): " + token + "\n")

            key_node_id = 'levelC-2-1' # key
            self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text='key') 

            token_node_id = key_node_id + '_' + 'levelC-3-1' # if
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text=token) 
          
            self.accept_token()

            print("child node (internal): if_exp")
            self.parseoutput.insert("end","child node (internal): if_exp" + "\n")

            print("child node (internal): comparision_exp")
            self.parseoutput.insert("end","child node (internal): comparision_exp" + "\n")

            print("child node (internal): if_exp")
            self.parseoutput.insert("end","child node (internal): if_exp" + "\n")
          
            self.if_exp() 
        elif (token == "print"):  # Fourth Input, the print
            print("child node (internal): id")
            self.parseoutput.insert("end","child node (internal): id" + "\n")
            print("   key has child node (token):" + token)
            self.parseoutput.insert("end","   key has child node (token): " + token + "\n\n")
          
            key_node_id = 'levelD-2-1' # id
            self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text='id') 

            token_node_id = key_node_id + '_' + 'levelD-3-1' # 
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text=token) 
          
            self.accept_token()

            print("child node (internal): print_exp")
            self.parseoutput.insert("end","child node (internal): print_exp" + "\n")
            self.print_exp()
          
        elif (typeT == "key"):  # First and Second Input, the float
            print("child node (internal): key")
            self.parseoutput.insert("end","child node (internal): key" + "\n")
            print("   key has child node (token):" + token)
            self.parseoutput.insert("end","   key has child node (token): " + token + "\n")
            
            key_node_id = 'levelA-2-1' # key
            self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text='key') 
   
            token_node_id = key_node_id + '_' + token # float
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text=token) 
          
            self.accept_token()
          
        elif (typeT == "id"):  # First and Second Input, the id like myVar and mynum
            print("child node (internal): identifier")
            self.parseoutput.insert("end","\nchild node (internal): identifier" + "\n")
            print("   identifier has child node (token):" + token)
            self.parseoutput.insert("end","   identifier has child node (token): " + token + "\n")
            self.accept_token()  
        else:
            print("expect identifier as the first element of the expression!\n")
            self.parseoutput.insert("end","expect identifier as the first element of the expression!" + "\n")
            return

        typeT, token = self.inToken
        if (typeT == "id"):  # First and Second Input, the id like myVar and mynum
            print("child node (internal): identifier")
            self.parseoutput.insert("end","child node (internal): identifier" + "\n")
            print("   identifier has child node (token):" + token)
            self.parseoutput.insert("end","   identifier has child node (token): " + token + "\n")
          
            key_node_id = 'levelA-2-2' # id
            self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text = 'id') 
            
            token_node_id = key_node_id + '_' + "levelA-2-2"  # mathresult1 
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text=token)

            self.accept_token()  

        if (self.inToken[1] == "="):  # First and Second Input, the =
            print("child node (token):" + self.inToken[1])
            self.parseoutput.insert("end","child node (token):" + self.inToken[1] + "\n")

            key_node_id = 'levelA-2-3' # op
            self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text = 'op') 
            
            token_node_id = key_node_id + '_' + "levelA-3-2"  # =
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text = self.inToken[1])
          
            self.accept_token()
          
            print("Child node (internal): math")
            self.parseoutput.insert("end","Child node (internal): math" + "\n")
            self.math()
          
        elif(if_token == "if"):
            return
          
        elif(print_token == "print"):
            return
          
        else:
            print("expect = as the second element of the expression!")
            self.parseoutput.insert("end","expect = as the second element of the expression!" + "\n")
            return

    def if_exp(self):
        # if(mathresult1 > mathresult2)
        print("\n----parent node if_exp, finding children nodes:")
        self.parseoutput.insert("end", "\n" + "----parent node if_exp, finding children nodes: " + "\n")
        #global inToken
        typeT, token = self.inToken

        key_node_id = 'levelC-2-2' # if_exp
        self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text='if_exp')
      
        if (typeT == "key"):
            print("child node (internal): key")
            self.parseoutput.insert("end","child node (internal): key" + "\n")
            print("   key has child node (token):" + token)
            self.parseoutput.insert("end","   key has child node (token): " + token + "\n")
            self.accept_token()

        typeT, token = self.inToken
        if (typeT == "sep"):
            print("child node (internal): separator")
            self.parseoutput.insert("end","child node (internal): separator")
            print("   separator has child node (token):" + token + "\n")
            self.parseoutput.insert("end","   separator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelC-3-2' # sep
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='sep') 
          
            sub_token_node_id = token_node_id + 'levelC-4-1' # (
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = self.inToken[1]) 
          
            self.accept_token()

        self.comparison_exp() 

        print("\n----parent node if_exp, finding children nodes:")
        self.parseoutput.insert("end", "\n" + "----parent node if_exp, finding children nodes: " + "\n")
        
        key_node_id = 'levelC-4-4' # if_exp
        self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text='if_exp')
      
        typeT, token = self.inToken
        if (typeT == "sep"):
            print("child node (internal): separator")
            self.parseoutput.insert("end","child node (internal): separator" + "\n")
            print("   separator has child node (token):" + token)
            self.parseoutput.insert("end","   separator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelC-3-6' # sep
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='sep') 

            sub_token_node_id = token_node_id + 'levelC-4-5' # )
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = self.inToken[1]) 
          
            self.accept_token()

        typeT, token = self.inToken
        if (typeT == "sep"):
            print("child node (internal): separator")
            self.parseoutput.insert("end","child node (internal): separator" + "\n")
            print("   separator has child node (token):" + token)
            self.parseoutput.insert("end","   separator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelC-3-7' # sep
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='sep') 

            sub_token_node_id = token_node_id + 'levelC-4-6' # :
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = self.inToken[1]) 
          
            self.accept_token()

    def comparison_exp(self):
    #(mathresult1 > mathresult2)
        print("\n----parent node comparison_exp, finding children nodes:")
        self.parseoutput.insert("end", "\n" + "----parent node comparison_exp, finding children nodes: " + "\n")
        #global inToken
        typeT, token = self.inToken

        key_node_id = 'levelB-3-3' # comparison_exp
        self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text = 'comparison_exp')
      
        if (typeT == "id"):
            print("child node (internal): identifier")
            self.parseoutput.insert("end","child node (internal): identifier" + "\n")
            print("   identifier has child node (token):" + token)
            self.parseoutput.insert("end","   identifier has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelC-3-3' # id
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text="id") 

            sub_token_node_id = token_node_id + 'levelC-4-2' # mathresult1
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = token) 
          
            self.accept_token()

        typeT, token = self.inToken
        if (typeT == "op"):
            print("child node (internal): operator")
            self.parseoutput.insert("end","child node (internal): operator" + "\n")
            print("   operator has child node (token):" + token)
            self.parseoutput.insert("end","   operator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelC-3-4' # op
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text="op") 

            sub_token_node_id = token_node_id + 'levelC-4-3' # >
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = ">") 
          
            self.accept_token()

        typeT, token = self.inToken
        if (typeT == "id"):
            print("child node (internal): identifier")
            self.parseoutput.insert("end","child node (internal): identifier" + "\n")
            print("   identifier has child node (token):" + token)
            self.parseoutput.insert("end","   identifier has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelC-3-5' # id
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text="id") 

            sub_token_node_id = token_node_id + 'levelC-4-4' # mathresult2
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = token) 
          
            self.accept_token()

    def print_exp(self):
        print("\n----parent node print_exp, finding children nodes:")
        self.parseoutput.insert("end","----parent node print_exp, finding children nodes: " + "\n")
        #global inToken

        key_node_id = 'levelD-2-2' # print_exp
        self.visualizationtreeoutput.insert('level1', 'end', key_node_id, text='print_exp')
      
        typeT, token = self.inToken    
        if (typeT == "sep"):    # (
            print("child node (internal): separator")
            self.parseoutput.insert("end","child node (internal): separator" + "\n")
            print("   separator has child node (token):" + token)
            self.parseoutput.insert("end","   separator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelD-3-2' # sep
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='sep') 

            sub_token_node_id = token_node_id + 'levelD-4-1' # (
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = token) 
          
            self.accept_token()

        typeT, token = self.inToken
        if (typeT == "sep"): # "
            print("child node (internal): separator")
            self.parseoutput.insert("end","child node (internal): separator")
            print("   separator has child node (token):" + token)
            self.parseoutput.insert("end","   separator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelD-3-3' # sep
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='sep') 

            sub_token_node_id = token_node_id + 'levelD-4-2' # "
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = token) 
          
            self.accept_token()

        typeT, token = self.inToken    #Quote
        if (typeT == "lit_string"):
            print("child node (internal): string_literal")
            self.parseoutput.insert("end","child node (internal): string_literal" + "\n")
            print("   string_literal has child node (token):" + token)
            self.parseoutput.insert("end","   string_literal has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelD-3-4' # string_literal
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='string_literal') 

            sub_token_node_id = token_node_id + 'levelD-4-3' # quote
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = token) 
          
            self.accept_token()

        typeT, token = self.inToken
        if (typeT == "sep"):    # " 
            print("child node (internal): separator")
            self.parseoutput.insert("end","child node (internal): separator" + "\n")
            print("   separator has child node (token):" + token)
            self.parseoutput.insert("end","   separator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelD-3-5' # sep
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='sep') 

            sub_token_node_id = token_node_id + 'levelD-4-4' # "
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = token) 
          
            self.accept_token()

        typeT, token = self.inToken    
        if (typeT == "sep"):    # )
            print("child node (internal): separator")
            self.parseoutput.insert("end","child node (internal): separator" + "\n")
            print("   separator has child node (token):" + token)
            self.parseoutput.insert("end","   separator has child node (token): " + token + "\n")

            token_node_id = key_node_id + '_' + 'levelD-3-6' # sep
            self.visualizationtreeoutput.insert(key_node_id, 'end', token_node_id, text='sep') 

            sub_token_node_id = token_node_id + 'levelD-4-5' # )
            self.visualizationtreeoutput.insert(token_node_id, 'end', sub_token_node_id, text = token) 
          
            self.accept_token()

    def clear_treeview(self):
      # Clear existing items in the treeview
      for item in self.visualizationtreeoutput.get_children():
        self.visualizationtreeoutput.delete(item)

    def parser(self):
        #global inToken
        self.parseoutput.insert("end", f"--------------------Below is case--------------------\n{self.Mytokens}\n\n")

        self.inToken = self.Mytokens.pop(0)
        self.exp()
        if (self.inToken[1] == ";"):
            print("\nparse tree building success!")
            self.parseoutput.insert("end", "\n" + "parse tree building success!" + "\n\n")
        
if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()
