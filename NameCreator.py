import tkinter as tk
import random
from tkinter.constants import NORMAL, TOP

createdNameList = []
alpha = '_abcdefghijklmnopqrstuvwxyz'
association_dict = {}

class NameCreator(tk.Frame):
    """
    A class used to create a TKinter window and render
    the options for the names to be generated

    Attributes
    -----------
    None


    Methods
    ----------
    submitAction(self, gender)
        Will submit the options entered in the TKinter window to the mainLoop function
        Also will print the created Names to the text area at the bottom of the window
    """
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        #self.create_Widgets()

        def number_Validator(char):
            return char.isdigit()
        validation = self.register(number_Validator)

        #Markov Level
        self.markovLvLabel = tk.Label(self, text="Markov Level(default is 2)")
        self.markovLvLabel.grid()
        self.markovLvEntry = tk.Entry(self, validate="key", validatecommand=(validation, '%S'))
        self.markovLvEntry.grid()

        #Minimum Value
        self.minLenLabel = tk.Label(self, text="Minimum Name Length")
        self.minLenLabel.grid()
        self.minLenEntry = tk.Entry(self, validate="key", validatecommand=(validation, '%S'))
        self.minLenEntry.grid()

        #Maximum Value
        self.maxLenLabel = tk.Label(self, text="Maximum Name Length")
        self.maxLenLabel.grid()
        self.maxLenEntry = tk.Entry(self, validate="key", validatecommand=(validation, '%S'))
        self.maxLenEntry.grid()

        #Number of Names to Generate
        self.numNamesLabel = tk.Label(self, text="How Many Names Would you like to generate?")
        self.numNamesLabel.grid()
        self.numNamesEntry = tk.Entry(self, validate="key", validatecommand=(validation, '%S'))
        self.numNamesEntry.grid()
        
        #Male or Female Name (Will use namesBoys.txt or namesGirls.txt to populate )
        self.maleButton = tk.Button(self, text="Generate Male Names", command=lambda: self.submitAction("male"))
        self.maleButton.grid()
        self.femaleButton = tk.Button(self, text="Generate Female Name", command=lambda: self.submitAction("female"))
        self.femaleButton.grid()

        self.text = tk.Text(self, height=10, width=30)
        self.text.grid();

        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()


    def submitAction(self, gender):
        createdNameList.clear()
        if (self.markovLvEntry.get() == None):
            mkvLv = 2;
        else:
            mkvLv = int(self.markovLvEntry.get())
        print(mkvLv)
        mnl = self.minLenEntry.get()
        mxl = self.maxLenEntry.get()
        numNames = self.numNamesEntry.get()
        self.text.delete(1.0, tk.END)
        self.text.update()
        if mnl == '':
            mnl = 5
        else:
            mnl = int(mnl)
        if mxl == '':
            mxl = 10
        else:
            mxl = int(mxl)
        if numNames == '':
            numNames = 10
        else:
            numNames = int(numNames)
        mainLoop(mkvLv, gender, mnl, mxl, numNames)
        for i in range(len(createdNameList)):
            self.text.insert("end", str(i+1)+": "+createdNameList[i]+"\n")



########################AI CODE##########################

"""
Main loop of the MarkovChain code:
    Takes params:
        markovLv   -> int
          how deep the letter associations go in the dict
          eg.
              markovLv = 2 : key = __-a val=(amt of names that start with a)
        gender     -> string
            which name list to pull the not-created names from
        minLn      -> int
            Set mininum length of created names
        maxLn      -> int
            Set maximum length of created names
        amtOfNames -> int
            Set the amount of names to be created
"""
def mainLoop(markovLv, gender, minLn, maxLn, amtOfNames):
    """
    Main loop of the MarkovChain code that will create the names:
    Params:
        markovLv   -> int
          how deep the letter associations go in the dict
          eg.
              markovLv = 2 : key = __-a val=(amt of names that start with a)
        gender     -> string
            which name list to pull the not-created names from
        minLn      -> int
            Set mininum length of created names
        maxLn      -> int
            Set maximum length of created names
        amtOfNames -> int
            Set the amount of names to be created
    """
    markov_level = markovLv
    gender = gender
    minLen = minLn
    maxLen = maxLn
    numNames = amtOfNames
    if gender.lower() == 'male':
        patternCheck('namesBoys.txt', markov_level)
    else:
        patternCheck('namesGirls.txt', markov_level)
    counter = 0
    print("Creating Names...")
    while counter < numNames:
        potentialName = createName(minLen, maxLen, markov_level)
        if (potentialName not in createdNameList and len(potentialName.strip('_')) <= maxLen):
            createdNameList.append(potentialName.strip("_"))
            counter += 1


def patternCheck(inptTxt, mkv_lv):
    """
    Creates the association dictionary using a list of names and a chosen markov level
    Params:
        inptTxt -> str
            the address of the txt file to be used for making the associations
        mkv_lv  -> int
            the level of association between letters
    """
    print("Creating Association Table...")
    with open(inptTxt) as file:
        for line in file:
            tempName = "_"*(mkv_lv-1) + line.lower().rstrip()+"_"
            while(len(tempName) >= mkv_lv):
                if tempName[:mkv_lv-1]+"-"+tempName[mkv_lv-1] in association_dict.keys():
                    association_dict[tempName[:mkv_lv-1]+"-"+tempName[mkv_lv-1]] +=  1
                else:
                    association_dict[tempName[:mkv_lv-1]+"-"+tempName[mkv_lv-1]] = 1
                tempName = tempName[1:]
    normalize(mkv_lv)
    print("Finished Normalizing...")


def normalize(mk_lv):
    """
    Normalizes the dictionary and averages the values
    Params:
        mk_lv -> int
            Uses this to find the correct keys in the dictionary
    """
    print("Normalizing Table...")
    total = 0
    key_string = "_"*(mk_lv-1)
    while ((key_string != ("z"*(mk_lv-1)))):
        for key in association_dict.keys():
            if key_string in key:
                total += association_dict[key]
        for key in association_dict.keys():
            if key_string in key:
                if total != 0:
                    association_dict[key] = (association_dict[key]/total)
        total = 0
        key_string = nextString(key_string)
        

def nextString(strn):
    """
    Find the next string to be used for keys
    Params:
        strn -> str
            The current string used
    """
    temp_str = strn
    if strn[-1] == "_":
        temp_str = temp_str[:-1] + alpha[1]
    elif strn[-1] != "_" and strn[-1] != "z":
        temp_str = temp_str[:-1] + chr((ord(strn[-1])+1))
    else:
        if len(strn) > 1:
             temp_str = nextString(strn[:-1])
             temp_str = temp_str + "_"
        else:
            temp_str = "a"
    return temp_str


def createName(mnLen, mxLen,mkv_lv):
    """
    function used to create names with a given minLength and maxLength
    uses random number generated and subtracts the percentage of
    a given letter association until a letter is chosen
    Params:
        mnLen -> int
            minLength for a name
        mxLen -> int
            maxLength for a name
        mkv_lv -> int
            the markov level(used to get the proper key)
    """
    name = '_'*(mkv_lv-1)
    nextLetter = ''
    while nextLetter != '_':
        cur_key = name[-(mkv_lv-1):]
        nxt_letter_prob = random.random()
        for item in association_dict.keys():
            if cur_key in item:
                if nxt_letter_prob - association_dict[item] <= 0:
                    nextLetter = item[-1]
                    name += nextLetter
                    break
                else:
                    nxt_letter_prob -= association_dict[item]
    if len(name.strip("_")) < mnLen or len(name.strip("_")) > mxLen:
        name = createName(mnLen, mxLen, mkv_lv)
    return name



###Create and run the app###
app = NameCreator()
app.master.title("Name Generator")
app.mainloop()
