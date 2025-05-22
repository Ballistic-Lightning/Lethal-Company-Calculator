from dataclasses import dataclass
import ui
import db

# -----------------------------------------------------------------------------
# Quota Class
# -----------------------------------------------------------------------------

@dataclass
class Quota:
    currentQuota:float = 0
    min:float = 0
    avg:float = 0
    max:float = 0
    roll:float = 0
    description:str = ""

# -----------------------------------------------------------------------------
# Calculations
# -----------------------------------------------------------------------------

    def randMath(timesFufil, randValue, quotaAmount):
        quotaAmount = float(quotaAmount) if isinstance(quotaAmount, str) else quotaAmount
        return float((100 * (1 + (((timesFufil - 1) ** 2) / 16)) * (randValue + 0.5)) + quotaAmount)

    def rollMath(timesFufil, currentQuota, previousQuota):
        currentQuota = float(currentQuota) if isinstance(currentQuota, str) else currentQuota
        previousQuota = float(previousQuota) if isinstance(previousQuota, str) else previousQuota
        return round(float((currentQuota - previousQuota) // (100 * (1 + (((timesFufil - 1) ** 2) / 16))) - 0.5), 2)
    
    def overCalc():
        while True:
            quota = int(input("Quota Amount: "))
            sold = int(input("Sold Amount: "))
            if quota <= 0 or sold <= 0:
                ui.errThrow('subZ')
            elif quota > sold:
                ui.errThrow('subQ')
            else:
                overtime = int((((sold - quota) // 5) + 15) - 1)
                if overtime < 0:
                    overtime = 0
                ui.breakline()
                print(f"Overtime Amount: |{overtime}|")
                return overtime
            
    def sellCalc():
        while True:
            quota = int(input("Quota Amount: "))
            target = int(input("Target Amount: "))
            if quota <= 0 or target <= 0:
                ui.errThrow('subZ')
            elif quota > target:
                ui.errThrow('subQ')
            else:
                toSell = int((((5 * target) + 75 + quota) // 6) + 1)
                ui.breakline()
                print(f"Sell Amount: |{toSell}|")
                return toSell