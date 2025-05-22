import csv
import ui
import sqlite3
import os
from objects import Quota
from contextlib import closing

# -----------------------------------------------------------------------------
# Global Inits
# -----------------------------------------------------------------------------
conn = None
DB = None

# -----------------------------------------------------------------------------
# Main Sheet Functions
# -----------------------------------------------------------------------------

def sheetDelete(quotaMasterSheet):
    quotaMasterSheet.clear()

def sheetImport(quotaMasterSheet):
    sheetDelete(quotaMasterSheet)
    if DB == False:
        newData = readMS()
    elif DB == True:
        newData = getQuotas()
        if newData is None:
            newData = ui.defaultQuotaSheet.copy()
        converted = []
        for row in newData:
            converted.append([
                row["currentQuota"],
                row["min"],
                row["avg"],
                row["max"],
                row["roll"],
                row["description"]
            ])
        newData = converted
    for row in newData:
        quotaMasterSheet.append(row)
    while len(quotaMasterSheet) < 21:
        quotaMasterSheet.append(['0'] * 6)
    ui.sheetPredict(quotaMasterSheet)

def sheetClean(quotaMasterSheet):
    for i in range(1, len(quotaMasterSheet)):
        if not isinstance(quotaMasterSheet[i][0], int):
            for j in range(1, 6):
                quotaMasterSheet[i][j] = '0'

# -----------------------------------------------------------------------------
# Read Functions
# -----------------------------------------------------------------------------

def readMS():
    global loadedMS
    global DB
    while True:
        sheetChoice = input("What filetype would you like to import? (csv / sqlite)")
        if sheetChoice.startswith("c"):
            DB = False
            break
        elif sheetChoice.startswith("s"):
            DB = True
            connect()
            rows = getQuotas()
            if rows is None:
                return ui.defaultQuotaSheet.copy()
            converted = []
            for row in rows:
                converted.append([
                    row["currentQuota"],
                    row["min"],
                    row["avg"],
                    row["max"],
                    row["roll"],
                    row["description"]
                ])
            return converted
        else:
            ui.errThrow("invCom")
    if DB == False:
        while True:
            loadedMS = input("Enter file name: ")
            if not loadedMS.endswith(".csv"):
                ui.errThrow("impErrCsv")
            else:
                break
        if not os.path.exists(loadedMS):
            while True:
                opt = input(f"{loadedMS} does not exist, create file? (y/n) ").lower()
                if opt == "y":
                    with open(loadedMS, "w", newline="") as file:
                        csv.writer(file).writerows(ui.defaultQuotaSheet)
                    return ui.defaultQuotaSheet.copy()
                elif opt == "n":
                    return ui.defaultQuotaSheet.copy()
                else:
                    ui.errThrow("invCom")
        quotaMasterSheet = []
        with open(loadedMS, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    row[1] = float(row[1]) if row[1] != '0' else 0
                    row[2] = float(row[2]) if row[2] != '0' else 0
                    row[3] = float(row[3]) if row[3] != '0' else 0
                    row[4] = float(row[4]) if row[4] != '0' else 0
                except (ValueError, IndexError):
                    ui.errThrow("impErrFmt")
                    raise
                row[5] = row[5] if len(row) > 5 else '0'
                quotaMasterSheet.append(row)
        return quotaMasterSheet

# -----------------------------------------------------------------------------
# Write Functions
# -----------------------------------------------------------------------------

def writeMS(quotaMasterSheet):
    if DB == True:
        with closing(conn.cursor()) as c:
            c.execute("DELETE FROM MasterSheet")
            for i, row in enumerate(quotaMasterSheet):
                if isinstance(row[0], (int, float)) and row[0] != 0:
                    c.execute(
                        '''INSERT INTO MasterSheet (quotaID, currentQuota, min, avg, max, roll, description)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (i + 1, row[0], row[1], row[2], row[3], row[4], row[5])
                    )
            conn.commit()
    elif DB == False:
        with open(loadedMS, "w", newline="") as file:
            csv.writer(file).writerows(quotaMasterSheet)

def writeToMS(quotaMasterSheet):
    global loadedMS
    if DB == True:
        ui.errThrow("invDB")
    elif DB == False:
        while True:
            saveAsMS = input("Enter new file name (must end in .csv): ")
            if not saveAsMS.endswith('.csv'):
                ui.errThrow('impErrCsv')
            else:
                break
        with open(saveAsMS, 'w', newline='') as f:
            csv.writer(f).writerows(quotaMasterSheet)
        loadedMS = saveAsMS
        print(f"Saved as {saveAsMS}!")


# -----------------------------------------------------------------------------
# SQLite Functions
# -----------------------------------------------------------------------------

def connect():
    global conn
    if not conn:
        DB_FILE = "QuotaMasterSheet.sqlite" 
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def getQuotas():
    try: 
        query = '''SELECT quotaID, currentQuota, min, avg, max, roll, description
                   FROM MasterSheet
                   ORDER BY quotaID'''
        with closing(conn.cursor()) as c:
            c.execute(query)
            results = c.fetchall()
        return results
    except sqlite3.OperationalError:
        return None

# -----------------------------------------------------------------------------
# Main Program Flow
# -----------------------------------------------------------------------------

def main():
    connect()
    quotas = getQuotas()
    for quota in quotas or []:
        print(quota["currentQuota"], quota["min"], quota["avg"], quota["max"], quota["roll"], quota["description"])

if __name__ == "__main__":
    main()
