import csv
import db
from objects import Quota
import os

# -----------------------------------------------------------------------------
# Global Inits
# -----------------------------------------------------------------------------

loadedMS = ""
defaultQuotaSheet = [[130, '0', '0', '0', '0', '0']]

# -----------------------------------------------------------------------------
# Line Prints
# -----------------------------------------------------------------------------

def breakLineDbl():
    print("=" * 134)

def breakline():
    print("-" * 134)

# -----------------------------------------------------------------------------
# ASCII Art Logos and Patch notes
# -----------------------------------------------------------------------------

def logo():
    print(r"""
        ____        _____      __  _         __    _       __    __        _            
       / __ )____ _/ / (_)____/ /_(_)____   / /   (_)___ _/ /_  / /_____  (_)___  ____ _
      / __  / __ `/ / / / ___/ __/ / ___/  / /   / / __ `/ __ \/ __/ __ \/ / __ \/ __ `/
     / /_/ / /_/ / / / (__  ) /_/ / /__   / /___/ / /_/ / / / / /_/ / / / / / / / /_/ / 
    /_____/\__,_/_/_/_/____/\__/_/\___/  /_____/_/\__, /_/ /_/\__/_/ /_/_/_/_/\__, /   
                                                 /____/                        /____/   
    """)

def calcLogo():
    print(r"""
        __         __  __          __   ______      __           __      __                _    _______  ______
       / /   ___  / /_/ /_  ____ _/ /  / ____/___ _/ /______  __/ /___ _/ /_____  _____   | |  / /__  / / ____/
      / /   / _ \/ __/ __ \/ __ `/ /  / /   / __ `/ / ___/ / / / / __ `/ __/ __ \/ ___/   | | / /__/ / / /___ 
     / /___/  __/ /_/ / / / /_/ / /  / /___/ /_/ / / /__/ /_/ / / /_/ / /_/ /_/ / /       | |/ // __/ /___  / 
    /_____/\___/\__/_/ /_/\__,_/_/   \____/\__,_/_/\___/\__,_/_/\__,_/\__/\____/_/        |___//____(_)____/  
                                                                                                          
    """)
    print("""
        Patch notes for v2.5: 
        + SQLite Database integration added!
        x Added Quotas in the QMS may not be less than or equal to zero.
        
    """)

def quotaLogo():
    print(r"""
       ____              __           __  ___           __            _____ __              __ 
      / __ \__  ______  / /_____ _   /  |/  /___ ______/ /____  _____/ ___// /_  ___  ___  / /_
     / / / / / / / __ \/ __/ __ `/  / /|_/ / __ `/ ___/ __/ _ \/ ___/\__ \/ __ \/ _ \/ _ \/ __/
    / /_/ / /_/ / /_/ / /_/ /_/ /  / /  / / /_/ (__  ) /_/  __/ /   ___/ / / / /  __/  __/ /_  
    \___\_\\__,_/\____/\__/\__,_/ /_/  /_/\__,_/____/\__/\___/_/   /____/_/ /_/\___/\___/\__/  
    """)

# -----------------------------------------------------------------------------
# Error Handling
# -----------------------------------------------------------------------------

def errThrow(Throw):
    error_messages = {
        "invCom": "Invalid Command",
        "subZ": "Value can not be below zero",
        "atZ": "Value can not be zero",
        "subQ": "Value can not be less than provided Quota",
        "impErrCat": "Catastrophic import error, corrupted file!!!",
        "impErrFmt": "Significant import error, reformat attempt...",
        "impErrCsv": "File provided is not a .csv file!",
        "invDB" : "You are unable to perform this action after selecting sqlite!"
    }
    print(error_messages.get(Throw, "Unknown error"))

# -----------------------------------------------------------------------------
# Prediction
# -----------------------------------------------------------------------------

def sheetPredict(quotaMasterSheet):
    # Recalculate Min, Avg, Max, Roll, Description
    for i in range(1, len(quotaMasterSheet)):
        # Reset old values
        for j in range(1, 6):
            quotaMasterSheet[i][j] = '0'
        prevData = quotaMasterSheet[i - 1]
        prevQuotaAmount = prevData[0] if isinstance(prevData[0], (int, float)) else prevData[2]
        quotaMasterSheet[i][1] = Quota.randMath(i + 1, 0, prevQuotaAmount)
        quotaMasterSheet[i][2] = Quota.randMath(i + 1, 0.5, prevQuotaAmount)
        quotaMasterSheet[i][3] = Quota.randMath(i + 1, 1, prevQuotaAmount)
        currentQuota = quotaMasterSheet[i][0] if isinstance(quotaMasterSheet[i][0], (int, float)) else quotaMasterSheet[i][2]
        quotaMasterSheet[i][4] = Quota.rollMath(i + 1, currentQuota, prevQuotaAmount)
        if quotaMasterSheet[i][4] <= 0.05:
            quotaMasterSheet[i][5] = 'Never play again, zeekers has cursed you'
        elif quotaMasterSheet[i][4] <= 0.20:
            quotaMasterSheet[i][5] = 'Just give up honestly'
        elif quotaMasterSheet[i][4] <= 0.35:
            quotaMasterSheet[i][5] = 'You better High roll the rest of the run'
        elif quotaMasterSheet[i][4] <= 0.45:
            quotaMasterSheet[i][5] = 'Low roll'
        elif quotaMasterSheet[i][4] <= 0.55:
            quotaMasterSheet[i][5] = 'Mid roll'
        elif quotaMasterSheet[i][4] <= 0.65:
            quotaMasterSheet[i][5] = 'High roll'
        elif quotaMasterSheet[i][4] <= 0.80:
            quotaMasterSheet[i][5] = 'Hey man, nice roll!'
        elif quotaMasterSheet[i][4] <= 0.95:
            quotaMasterSheet[i][5] = 'Chat, is this gonna be the WR run?'
        elif quotaMasterSheet[i][4] <= 1.00:
            quotaMasterSheet[i][5] = 'Bro is just hacking at this point'
        else:
            quotaMasterSheet[i][5] = 'Your run has been sent to zeekers for review'

# -----------------------------------------------------------------------------
# Display
# -----------------------------------------------------------------------------

def displaySheet(quotaMasterSheet):
    print(f"Quota\t|\tCurrent\t\tMin\t\tAvg\t\tMax\t\tRoll\t\tDescription")
    breakline()
    for q in range(1, 22):
        if q <= len(quotaMasterSheet):
            data = quotaMasterSheet[q - 1]
        else:
            data = ["0"] * 6 
        current = data[0] if data[0] else "0"
        min = data[1] if data[1] else "0"
        avg = data[2] if data[2] else "0"
        max = data[3] if data[3] else "0"
        roll = data[4] if data[4] else "0"
        description = data[5] if data[5] else "-"
        print(f"{q}\t|\t{int(current) if current != '0' else '0'}\t\t"
            f"{int(min) if min != '0' else '0'}\t\t"
            f"{int(avg) if avg != '0' else '0'}\t\t"
            f"{int(max) if max != '0' else '0'}\t\t"
            f"{roll}\t\t{description}")

# -----------------------------------------------------------------------------
# Menus
# -----------------------------------------------------------------------------

def menu():
    breakline()
    print("Lethal Company Calc")
    print(f"COMMANDS\n  Overtime Calc\n  To Sell Calc\n  Quota Mastersheet")
    breakline()

def sheetMenu(quotaMasterSheet):
    global loadedMS
    breakline()
    print("Quota Master Sheet")
    print(f"COMMANDS\n Import\n Add\n Refresh\n Save\n Save As\n Return")
    breakline()
    while True:
        command = input(": ").lower()
        if command.startswith('ad'):
            sheetAdd(quotaMasterSheet)
        elif command.startswith('ref'):
            sheetPredict(quotaMasterSheet)
            displaySheet(quotaMasterSheet)
        elif command == 'save':
            db.writeMS(quotaMasterSheet)
            print(f"{loadedMS} saved!")
        elif command == 'save as':
            db.writeToMS(quotaMasterSheet)
        elif command.startswith('im'):
            if db.DB == True:
                errThrow("invDB")
            else:
                while True:
                    opt = input(f"Would you like to save {loadedMS} first? (y/n) ").lower()
                    if opt == 'y':
                        db.writeMS(quotaMasterSheet)
                        print(f"{loadedMS} has been saved!")
                        break
                    elif opt == 'n':
                        break
                    else:
                        errThrow('invCom')
                db.sheetImport(quotaMasterSheet)
                displaySheet(quotaMasterSheet)
        elif command.startswith('ret'):
            return
        else:
            errThrow('invCom')

# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

def sheetAdd(quotaMasterSheet):
    for i in range(1, len(quotaMasterSheet)):
        if quotaMasterSheet[i][0] == '0':
            name = f"Quota {i + 1}"
            inputOpt = input(f"Would you like to add {name} data? (y/n) ").lower()
            if inputOpt == 'y':
                db.sheetClean(quotaMasterSheet)
                while True:
                    addedQuota = int(input("Enter Quota Amount: "))
                    if addedQuota <= 0:
                        errThrow("atZ")
                    else:
                        quotaMasterSheet[i][0] = addedQuota
                        sheetPredict(quotaMasterSheet)
                        displaySheet(quotaMasterSheet)
                        print(f"Data for {name} has been added.")
                        break
            return

# -----------------------------------------------------------------------------
# Main Program Flow
# -----------------------------------------------------------------------------

def main():
    breakLineDbl()
    logo()
    breakLineDbl()
    cmdLoop()

def cmdLoop():
    calcLogo()
    while True:
        menu()
        command = input(": ").lower()
        try:
            if command.startswith('ov'):
                Quota.overCalc()
            elif command.startswith('to'):
                Quota.sellCalc()
            elif command.startswith('qu'):
                quotaMast()
            else:
                errThrow('invCom')
        except ValueError:
            errThrow('invCom')

def quotaMast():
    if loadedMS == "":
        quotaMasterSheet = db.readMS()
    for _ in range(len(quotaMasterSheet), 21):
        quotaMasterSheet.append(['0'] * 6)
    breakLineDbl()
    quotaLogo()
    breakLineDbl()
    sheetPredict(quotaMasterSheet)
    displaySheet(quotaMasterSheet)
    sheetMenu(quotaMasterSheet)

if __name__ == '__main__':
    main()
