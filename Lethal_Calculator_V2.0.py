import csv
import os

# -----------------------------------------------------------------------------
# Globals and Defaults
# -----------------------------------------------------------------------------
loadedMS = ""
defaultQuotaSheet = [[130, '-', '-', '-', '-', '-']]

# -----------------------------------------------------------------------------
# Print Utilities
# -----------------------------------------------------------------------------
# Print a double separator line
def breakLineDbl():
    print("=" * 134)

# Print a single separator line
def breakline():
    print("-" * 134)

# -----------------------------------------------------------------------------
# ASCII Art Logos
# -----------------------------------------------------------------------------
# Main ASCII art logo
def logo():
    print(r"""
        ____        _____      __  _         __    _       __    __        _            
       / __ )____ _/ / (_)____/ /_(_)____   / /   (_)___ _/ /_  / /_____  (_)___  ____ _
      / __  / __ `/ / / / ___/ __/ / ___/  / /   / / __ `/ __ \/ __/ __ \/ / __ \/ __ `/
     / /_/ / /_/ / / / (__  ) /_/ / /__   / /___/ / /_/ / / / / /_/ / / / / / / / /_/ / 
    /_____/\__,_/_/_/_/____/\__/_/\___/  /_____/_/\__, /_/ /_/\__/_/ /_/_/_/_/\__, /   
                                                 /____/                        /____/   
    """)

# Calculation logo and patch notes
def calcLogo():
    print(r"""
        __         __  __          __   ______      __           __      __                _    _______  ______
       / /   ___  / /_/ /_  ____ _/ /  / ____/___ _/ /______  __/ /___ _/ /_____  _____   | |  / /__  / / __  /
      / /   / _ \/ __/ __ \/ __ `/ /  / /   / __ `/ / ___/ / / / / __ `/ __/ __ \/ ___/   | | / /__/ / / / / /
     / /___/  __/ /_/ / / / /_/ / /  / /___/ /_/ / / /__/ /_/ / / /_/ / /_/ /_/ / /       | |/ // __/_/ /_/ / 
    /_____/\___/\__/_/ /_/\__,_/_/   \____/\__,_/_/\___/\__,_/_/\__,_/\__/\____/_/        |___//____(_)____/  
                                                                                                          
    """)
    print("""
        Patch notes for v2.0: 
        + File I/O added! Import and save your csv files.
        
    """)

# Quota sheet header logo
def quotaLogo():
    print(r"""
       ____              __           __  ___           __            _____ __              __ 
      / __ \__  ______  / /_____ _   /  |/  /___ ______/ /____  _____/ ___// /_  ___  ___  / /_
     / / / / / / / __ \/ __/ __ `/  / /|_/ / __ `/ ___/ __/ _ \/ ___/\__ \/ __ \/ _ \/ _ \/ __/
    / /_/ / /_/ / /_/ / /_/ /_/ /  / /  / / /_/ (__  ) /_/  __/ /   ___/ / / / /  __/  __/ /_  
    \___\_\\__,_/\____/\__/\__,_/  /_/  /_/\__,_/____/\__/\___/_/   /____/_/ /_/\___/\___/\__/  
    """)

# -----------------------------------------------------------------------------
# Error Handling
# -----------------------------------------------------------------------------
def errThrow(Throw):
    # Print error message based on code
    error_messages = {
        "invCom": "Invalid Command",
        "subZ": "Value can not be below zero",
        "subQ": "Value can not be less than provided Quota",
        "impErrCat": "Catastrophic import error, corrupted file!!!",
        "impErrFmt": "Significant import error, reformat attempt...",
        "impErrCsv": "File provided is not a .csv file!"
    }
    print(error_messages.get(Throw, "Unknown error"))

# -----------------------------------------------------------------------------
# File I/O Functions
# -----------------------------------------------------------------------------
def readMS():
    global loadedMS
    # Prompt for filename and validate
    while True:
        loadedMS = input("Enter file name: ")
        if not loadedMS.endswith(".csv"):
            errThrow("impErrCsv")
        else:
            break
    # If file doesn't exist, offer to create default
    if not os.path.exists(loadedMS):
        while True:
            opt = input(f"{loadedMS} does not exist, create file? (y/n) ").lower()
            if opt == "y":
                with open(loadedMS, "w", newline="") as file:
                    csv.writer(file).writerows(defaultQuotaSheet)
                return defaultQuotaSheet.copy()
            elif opt == "n":
                return defaultQuotaSheet.copy()
            else:
                errThrow("invCom")
    # Read existing CSV into list of rows
    quotaMasterSheet = []
    with open(loadedMS, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                row[1] = float(row[1]) if row[1] != '-' else 0
                row[2] = float(row[2]) if row[2] != '-' else 0
                row[3] = float(row[3]) if row[3] != '-' else 0
                row[4] = float(row[4]) if row[4] != '-' else 0
            except (ValueError, IndexError):
                errThrow("impErrFmt")
                raise
            row[5] = row[5] if len(row) > 5 else '-'
            quotaMasterSheet.append(row)
    return quotaMasterSheet

def writeMS(quotaMasterSheet):
    # Save current sheet to loadedMS
    with open(loadedMS, "w", newline="") as file:
        csv.writer(file).writerows(quotaMasterSheet)

# -----------------------------------------------------------------------------
# Sheet Management
# -----------------------------------------------------------------------------
def sheetDelete(quotaMasterSheet):
    # Completely clear all rows
    quotaMasterSheet.clear()

def sheetImport(quotaMasterSheet):
    # Delete and reload sheet, then pad to 21 rows
    sheetDelete(quotaMasterSheet)
    newData = readMS()
    for row in newData:
        quotaMasterSheet.append(row)
    while len(quotaMasterSheet) < 21:
        quotaMasterSheet.append(['-'] * 6)
    sheetPredict(quotaMasterSheet)

def sheetClean(quotaMasterSheet):
    # Clear prediction columns for rows without valid quota
    for i in range(1, len(quotaMasterSheet)):
        if not isinstance(quotaMasterSheet[i][0], int):
            for j in range(1, 6):
                quotaMasterSheet[i][j] = '-'

# -----------------------------------------------------------------------------
# Prediction and Display
# -----------------------------------------------------------------------------
def sheetPredict(quotaMasterSheet):
    # Recalculate Min, Avg, Max, Roll, Description
    for i in range(1, len(quotaMasterSheet)):
        # Reset old values
        for j in range(1, 6):
            quotaMasterSheet[i][j] = '-'
        prevData = quotaMasterSheet[i - 1]
        prevQuotaAmount = prevData[0] if isinstance(prevData[0], (int, float)) else prevData[2]
        quotaMasterSheet[i][1] = randMath(i + 1, 0, prevQuotaAmount)
        quotaMasterSheet[i][2] = randMath(i + 1, 0.5, prevQuotaAmount)
        quotaMasterSheet[i][3] = randMath(i + 1, 1, prevQuotaAmount)
        currentQuota = quotaMasterSheet[i][0] if isinstance(quotaMasterSheet[i][0], (int, float)) else quotaMasterSheet[i][2]
        quotaMasterSheet[i][4] = rollMath(i + 1, currentQuota, prevQuotaAmount)
        # Determine description
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

def displaySheet(quotaMasterSheet):
    print(f"Quota\t|\tCurrent\t\tMin\t\tAvg\t\tMax\t\tRoll\t\tDescription")
    breakline()
    for q in range(1, 22):
        if q <= len(quotaMasterSheet):
            data = quotaMasterSheet[q - 1]
        else:
            data = ["-"] * 6 
        current = data[0] if data[0] else "-"
        min = data[1] if data[1] else "-"
        avg = data[2] if data[2] else "-"
        max = data[3] if data[3] else "-"
        roll = data[4] if data[4] else "-"
        description = data[5] if data[5] else "-"
        print(f"{q}\t|\t{int(current) if current != '-' else '-'}\t\t"
            f"{int(min) if min != '-' else '-'}\t\t"
            f"{int(avg) if avg != '-' else '-'}\t\t"
            f"{int(max) if max != '-' else '-'}\t\t"
            f"{roll}\t\t{description}")

# -----------------------------------------------------------------------------
# Menus and Commands
# -----------------------------------------------------------------------------
def menu():
    # Main menu display
    breakline()
    print("Lethal Company Calc")
    print(f"COMMANDS\n  Overtime Calc\n  To Sell Calc\n  Quota Mastersheet")
    breakline()

def sheetAdd(quotaMasterSheet):
    # Add a new quota entry
    for i in range(1, len(quotaMasterSheet)):
        if quotaMasterSheet[i][0] == '-':
            name = f"Quota {i + 1}"
            inputOpt = input(f"Would you like to add {name} data? (y/n) ").lower()
            if inputOpt == 'y':
                sheetClean(quotaMasterSheet)
                addedQuota = int(input("Enter Quota Amount: "))
                quotaMasterSheet[i][0] = addedQuota
                sheetPredict(quotaMasterSheet)
                displaySheet(quotaMasterSheet)
                print(f"Data for {name} has been added.")
            return

def sheetMenu(quotaMasterSheet):
    # Quota sheet submenu
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
            writeMS(quotaMasterSheet)
            print(f"{loadedMS} saved!")
        elif command == 'save as':
            while True:
                saveAsMS = input("Enter new file name (must end in .csv): ")
                if not saveAsMS.endswith('.csv'):
                    errThrow('impErrCsv')
                else:
                    break
            with open(saveAsMS, 'w', newline='') as f:
                csv.writer(f).writerows(quotaMasterSheet)
            loadedMS = saveAsMS
            print(f"Saved as {saveAsMS}!")
        elif command.startswith('im'):
            while True:
                opt = input(f"Would you like to save {loadedMS} first? (y/n) ").lower()
                if opt == 'y':
                    writeMS(quotaMasterSheet)
                    print(f"{loadedMS} has been saved!")
                    break
                elif opt == 'n':
                    break
                else:
                    errThrow('invCom')
            sheetImport(quotaMasterSheet)
            displaySheet(quotaMasterSheet)
        elif command.startswith('ret'):
            return
        else:
            errThrow('invCom')

# -----------------------------------------------------------------------------
# Calculations
# -----------------------------------------------------------------------------
def randMath(timesFufil, randValue, quotaAmount):
    # Compute min/avg/max
    quotaAmount = float(quotaAmount) if isinstance(quotaAmount, str) else quotaAmount
    return float((100 * (1 + (((timesFufil - 1) ** 2) / 16)) * (randValue + 0.5)) + quotaAmount)

def rollMath(timesFufil, currentQuota, previousQuota):
    # Compute roll value
    currentQuota = float(currentQuota) if isinstance(currentQuota, str) else currentQuota
    previousQuota = float(previousQuota) if isinstance(previousQuota, str) else previousQuota
    return round(float((currentQuota - previousQuota) // (100 * (1 + (((timesFufil - 1) ** 2) / 16))) - 0.5), 2)

# -----------------------------------------------------------------------------
# User Flows
# -----------------------------------------------------------------------------
def overCalc():
    # Overtime calculation
    while True:
        quota = int(input("Quota Amount: "))
        sold = int(input("Sold Amount: "))
        if quota <= 0 or sold <= 0:
            errThrow('subZ')
        elif quota > sold:
            errThrow('subQ')
        else:
            overtime = int((((sold - quota) // 5) + 15) - 1)
            if overtime < 0:
                overtime = 0
            breakline()
            print(f"Overtime Amount: |{overtime}|")
            return overtime

def sellCalc():
    # To sell calculation
    while True:
        quota = int(input("Quota Amount: "))
        target = int(input("Target Amount: "))
        if quota <= 0 or target <= 0:
            errThrow('subZ')
        elif quota > target:
            errThrow('subQ')
        else:
            toSell = int((((5 * target) + 75 + quota) // 6) + 1)
            breakline()
            print(f"Sell Amount: |{toSell}|")
            return toSell

# -----------------------------------------------------------------------------
# Main Program Flow
# -----------------------------------------------------------------------------
def quotaMast():
    # Entry to quota master sheet view
    if loadedMS == "":
        quotaMasterSheet = readMS()
    for _ in range(len(quotaMasterSheet), 21):
        quotaMasterSheet.append(['-'] * 6)
    breakLineDbl()
    quotaLogo()
    breakLineDbl()
    sheetPredict(quotaMasterSheet)
    displaySheet(quotaMasterSheet)
    sheetMenu(quotaMasterSheet)

def cmdLoop():
    # Main command loop
    calcLogo()
    while True:
        menu()
        command = input(": ").lower()
        try:
            if command.startswith('ov'):
                overCalc()
            elif command.startswith('to'):
                sellCalc()
            elif command.startswith('qu'):
                quotaMast()
            else:
                errThrow('invCom')
        except ValueError:
            errThrow('invCom')

def main():
    # Program start
    breakLineDbl()
    logo()
    breakLineDbl()
    cmdLoop()

if __name__ == '__main__':
    main()
