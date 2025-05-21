def breakLineDbl():
    print("==============================================================================================================================================")
def breakline():
    print("----------------------------------------------------------------------------------------------------------------------------------------------")

def logo():
    print("""
        ____        _____      __  _         __    _       __    __        _            
       / __ )____ _/ / (_)____/ /_(_)____   / /   (_)___ _/ /_  / /_____  (_)___  ____ _
      / __  / __ `/ / / / ___/ __/ / ___/  / /   / / __ `/ __ \/ __/ __ \/ / __ \/ __ `/
     / /_/ / /_/ / / / (__  ) /_/ / /__   / /___/ / /_/ / / / / /_/ / / / / / / / /_/ / 
    /_____/\__,_/_/_/_/____/\__/_/\___/  /_____/_/\__, /_/ /_/\__/_/ /_/_/_/ /_/\__, /  
                                                 /____/                        /____/   
    """)

def calcLogo():
    print("""
        __         __  __          __   ______      __           __      __                _    __ ___ __
       / /   ___  / /_/ /_  ____ _/ /  / ____/___ _/ /______  __/ /___ _/ /_____  _____   | |  / /<  /< /  
      / /   / _ \/ __/ __ \/ __ `/ /  / /   / __ `/ / ___/ / / / / __ `/ __/ __ \/ ___/   | | / / / // / 
     / /___/  __/ /_/ / / / /_/ / /  / /___/ /_/ / / /__/ /_/ / / /_/ / /_/ /_/ / /       | |/ / / // / 
    /_____/\___/\__/_/ /_/\__,_/_/   \____/\__,_/_/\___/\__,_/_/\__,_/\__/\____/_/        |___(_)_(_)/ 
    """)
    print("""
        Patch notes for v1.1: 
        x Fixed bug where Quota Prediction was slightly higher than what it actually should have been. 
        + Quota Master Sheet now auto refreshes upon Add Command.
        - Negative values are no longer accepted.
        - Sold and Target amounts less than the provided quota are no longer accepted.
          """)

def quotaLogo():
    print("""
       ____              __           __  ___           __            _____ __              __ 
      / __ \__  ______  / /_____ _   /  |/  /___ ______/ /____  _____/ ___// /_  ___  ___  / /_
     / / / / / / / __ \/ __/ __ `/  / /|_/ / __ `/ ___/ __/ _ \/ ___/\__ \/ __ \/ _ \/ _ \/ __/
    / /_/ / /_/ / /_/ / /_/ /_/ /  / /  / / /_/ (__  ) /_/  __/ /   ___/ / / / /  __/  __/ /_  
    \___\_\__,_/\____/\__/\__,_/  /_/  /_/\__,_/____/\__/\___/_/   /____/_/ /_/\___/\___/\__/                                                                                                                                                    
    """)

def menu():
    breakline()
    print("Lethal Company Calc")
    print(f"COMMANDS\n  Overtime Calc\n  To Sell Calc\n  Quota Mastersheet")
    breakline()

def errThrow(Throw):
    if Throw == "inv":
        print("Invalid Command")
    if Throw == "SubZ":
        print("Value can not be below zero")
    if Throw == "<0":
        print("Value can not be less than provided Quota")

def overCalc():
    while True:
        quota = int(input("Quota Amount: "))
        sold = int(input("Sold Amount: "))
        if quota <= 0 or sold <=0:
            errThrow("SubZ")
        elif quota > sold:
            errThrow("<0")
        else:
            overtime = int((((sold - quota) // 5) + 15) - 1)
            if overtime < 0:
                overtime = 0
            breakline()
            print(f"Overtime Amount: |{overtime}|")
            return overtime
            break

def sellCalc():
    while True:
        quota = int(input("Quota Amount: "))
        target = int(input("Target Amount: "))
        if quota <= 0 or target <=0:
            errThrow("SubZ")
        elif quota > target:
            errThrow("<0")
        else:
            toSell = int((((5 * target) + 75 + quota) // 6) + 1)
            breakline()
            print(f"Sell Amount: |{toSell}|")
            return toSell
            break

quotaMasterSheet = [[130, '-', '-', '-', '-', '-']]

def quotaMast():
    for _ in range(len(quotaMasterSheet), 21):
        quotaMasterSheet.append(['-'] * 6)
    breakLineDbl()
    quotaLogo()
    breakLineDbl()
    sheetPredict(quotaMasterSheet)
    displaySheet(quotaMasterSheet)
    sheetMenu(quotaMasterSheet)

def sheetAdd(quotaMasterSheet):
    for i in range(1, len(quotaMasterSheet)):
        if quotaMasterSheet[i][0] == '-':
            while True:
                inputOpt = str(input(f"Would you like to add Quota {i + 1} data? (y/n)")).lower()
                if inputOpt == "y":
                    sheetClean(quotaMasterSheet)
                    while True:
                        try:
                            addedQuota = int(input("Enter Quota Amount:"))
                            if addedQuota >= 0:
                                quotaMasterSheet[i][0] = addedQuota
                                sheetPredict(quotaMasterSheet)
                                displaySheet(quotaMasterSheet)
                                break
                            else:
                                errThrow("SubZ")
                        except ValueError:
                            errThrow("inv")
                elif inputOpt == "n":
                    break
                break
            break

def sheetMenu(quotaMasterSheet):
    breakline()
    print("Quota Master Sheet")
    print(f"COMMANDS\n  Add\n  Refresh\n  Return")
    breakline()
    while True:
        command = input(": ").lower()
        try:
            if "ad" in command:
                sheetAdd(quotaMasterSheet)
            elif "ref" in command:
                sheetPredict(quotaMasterSheet)
                displaySheet(quotaMasterSheet)
            elif "ret" in command:
                cmdLoop()
            else:
                errThrow("inv")
        except ValueError:
            errThrow("inv")


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

def sheetPredict(quotaMasterSheet):
    for i in range(1, len(quotaMasterSheet)):
        if all(quotaMasterSheet[i][j] != '-' for j in range(1, 4)):
            continue
        
        prevData = quotaMasterSheet[i - 1]
        prevQuotaAmount = prevData[0] if prevData[0] != '-' else prevData[2]
        if quotaMasterSheet[i][1] == '-':
            quotaMasterSheet[i][1] = randMath(i + 1, 0, prevQuotaAmount)
        if quotaMasterSheet[i][2] == '-':
            quotaMasterSheet[i][2] = randMath(i + 1, 0.5, prevQuotaAmount)
        if quotaMasterSheet[i][3] == '-':
            quotaMasterSheet[i][3] = randMath(i + 1, 1, prevQuotaAmount)

        currentQuota = quotaMasterSheet[i][0] if quotaMasterSheet[i][0] != '-' else quotaMasterSheet[i][2]
        if currentQuota != '-' and prevQuotaAmount != '-':
            quotaMasterSheet[i][4] = rollMath(i + 1, currentQuota, prevQuotaAmount)
        if quotaMasterSheet[i][4] > 0 and quotaMasterSheet[i][4] <= 0.05:
            quotaMasterSheet[i][5] = 'Never play again, zeekers has cursed you'
        elif quotaMasterSheet[i][4] > 0.05 and quotaMasterSheet[i][4] <= 0.20:
            quotaMasterSheet[i][5] = 'Just give up honestly'
        elif quotaMasterSheet[i][4] > 0.20 and quotaMasterSheet[i][4] <= 0.35:
            quotaMasterSheet[i][5] = 'You better High roll the rest of the run'
        elif quotaMasterSheet[i][4] > 0.35 and quotaMasterSheet[i][4] <= 0.45:
            quotaMasterSheet[i][5] = 'Low roll'
        elif quotaMasterSheet[i][4] > 0.45 and quotaMasterSheet[i][4] <= 0.55:
            quotaMasterSheet[i][5] = 'Mid roll'
        elif quotaMasterSheet[i][4] > 0.55 and quotaMasterSheet[i][4] <= 0.65:
            quotaMasterSheet[i][5] = 'High roll'
        elif quotaMasterSheet[i][4] > 0.65 and quotaMasterSheet[i][4] <= 0.80:
            quotaMasterSheet[i][5] = 'Hey man, nice roll!'
        elif quotaMasterSheet[i][4] > 0.80 and quotaMasterSheet[i][4] <= 0.95:
            quotaMasterSheet[i][5] = 'Chat, is this gonna be the WR run?'
        elif quotaMasterSheet[i][4] > 0.95 and quotaMasterSheet[i][4] <= 1:
            quotaMasterSheet[i][5] = 'Bro is just hacking at this point'
        else:
            quotaMasterSheet[i][5] = 'Your run has been sent to zeekers for review'
            
def sheetClean(quotaMasterSheet):
    for i in range(1, len(quotaMasterSheet)):
        if not isinstance(quotaMasterSheet[i][0], int):
            quotaMasterSheet[i][1] = '-'
            quotaMasterSheet[i][2] = '-'
            quotaMasterSheet[i][3] = '-'
            quotaMasterSheet[i][4] = '-'
            quotaMasterSheet[i][5] = '-'

def randMath(timesFufil, randValue, quotaAmount):
    return float((100 * (1 + (((timesFufil - 1) ** 2) / 16)) * (randValue + 0.5)) + quotaAmount)

def rollMath(timesFufil, currentQuota, previousQuota):
    return round(float((currentQuota - previousQuota) / (100 * (1 + (((timesFufil - 1) ** 2) / 16))) - 0.5), 2)
    

def cmdLoop(): 
    calcLogo() 
    while True:
        menu()
        command = input(": ").lower()
        try:
            if "ov" in command:
                overCalc()
            elif "to" in command:
                sellCalc()
            elif "qu" in command:
                quotaMast()
            else:
                errThrow("inv")
        except ValueError:
            errThrow("inv")

def main():
    breakLineDbl()
    logo()
    breakLineDbl()
    cmdLoop()

if __name__ == "__main__":
    main()
