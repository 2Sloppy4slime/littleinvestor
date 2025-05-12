import pyxel
import random

pyxel.init(160, 120, title = "INVESTCLICKR",fps = 30)
pyxel.mouse(True)

oneSecTimer_val = 30
def oneSecTimer():
    global oneSecTimer_val
    global time_m
    global time_s
    if oneSecTimer_val == 0: 
        oneSecTimer_val = 30
        time_s += 1
        if time_s == 60 :
            time_s = 0
            time_m += 1
        return True
    else : 
        oneSecTimer_val -=1
        return False

def pricetoheight(price):
    if price > 1:
        return (5 + (80 - price * 16 ))
    else : return (80 - 11*price)

def sensdemouvement(a,b):
    pass
    if a > b:
        return 8
    else :
        return 11


stocks = 10
stock_price = 1
money = 20
moneyPerTick = 1
bought = 0
sold = 0
stock_history = []
goal = random.randrange(500,1000)
time_s = 0
time_m = 0
gamestate = 0
mousex = 0
mousey = 0 
maxrollpricechange = 300
minrollpricechange = 0
score = 0
trades = 0
def drawprogress():
    global money
    global goal
    col = 10
    bars = (((int(money)*100)/goal)*65)/100
    for i in range(1,int(bars)+1) :
        if col == 10:
            col = 9
        else :
            col = 10
        pyxel.line(116,80 - i,153,80-i,col)

def buy() :
    global money
    global stock_price
    global stocks
    global bought
    global trades
    if money > stock_price :
            stocks += 1
            money -= stock_price
            bought += 1
            trades += 1
def sell() :
    global stocks
    global money
    global stock_price
    global sold
    global trades
    if stocks > 0:
            money += stock_price
            stocks -= 1 
            sold += 1
            trades += 1 
#-------------------------------------------------------
#                    GameFuncs
#---------------------------------------------------------
def update():
    global money
    global stock_price
    global stocks
    global bought
    global sold
    global stock_history
    global maxrollpricechange
    global minrollpricechange
    global mousex
    global mousey
    global gamestate
    global goal
    global score
    global trades
    match gamestate:
        case 0:
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()
            
            if money > goal:
                print("you win")
                gamestate = 1
                score = goal *6000 - (60*time_m + time_s)*30 - 50*trades

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mousey = pyxel.mouse_x
                mousex = pyxel.mouse_y
                if mousey > 116 and mousey < 158 and mousex > 104 and mousex < 114:
                    sell()
                if mousey > 116 and mousey < 158 and mousex > 93 and mousex < 103:
                    buy()

            if oneSecTimer()  :
                deflation = 0
                inflation = 0
                if bought >0:
                    inflation = (random.randrange(0 , 0 +  bought*40) * 0.01)
                if sold >0:
                    deflation = (random.randrange(0 - sold*40, 100) * 0.01)
                    

                stock_price = round(stock_price + (float(random.randrange( minrollpricechange , maxrollpricechange)-150) * 0.01) + deflation + inflation , 2)
                #eviter la merde où ça se bloque ds les coins
                if stock_price >= 5 :
                    stock_price = 5
                    minrollpricechange = -300
                    maxrollpricechange = 50
                elif stock_price <= 0 :
                    stock_price = 0
                    maxrollpricechange = 450
                    minrollpricechange = 50

                else: 
                    maxrollpricechange = 300
                    minrollpricechange = 0

                

                bought = 0
                sold = 0
                stock_history.append(stock_price)
                if len(stock_history) > 11 :
                    stock_history.pop(0)


            if pyxel.btnp(pyxel.KEY_C): #acheter
                buy()

            if pyxel.btnp(pyxel.KEY_N): #vendre
                sell()
        
        case 1:
            if pyxel.btnp(pyxel.KEY_SPACE):
                goal = random.randrange(500,1500)
                money = 20
                stocks = 10
                stock_history = []
                stock_price = 1
                gamestate = 0 
                score = 0
                trades = 0

def draw():
    global stock_history
    global goal
    global money
    global time_s
    global time_m
    global score
    pyxel.cls(4)
    match gamestate:
        case 0 :
                    
            pyxel.rect(9, 5, 103, 76, 0)
            pyxel.rect(115, 5, 40, 110, 5)
            pyxel.rect(10, 85, 100, 30, 5)
            pyxel.rect(116,15,38,65,13)
            drawprogress()
            #5 : stock = 5 ; 80 : stock = 0

            if len(stock_history) >= 2:
                for i in range(1,len(stock_history)):
                    pyxel.line(i*10, pricetoheight(stock_history[i-1]),10+i*10,pricetoheight(stock_history[i]), sensdemouvement(stock_history[i-1],stock_history[i]))
            # 5 + (80 - stock_price * 16 ) si 1<stock_price<5
            # (80 - 11*stock_price) si 0<stock_price<1

            # boutons
            pyxel.rect(116,104,38,10,3) #(116,104) -> (154,114)
            pyxel.rect(116,93,38,10,3) #(116,93) -> (154,103)
            pyxel.text(116,106,"   sell",7)
            pyxel.text(115,95,"    buy",7)


            pyxel.text(10,85,"money: " + str(money),7)
            pyxel.text(10,95,"stocks: " + str(stocks),7)
            pyxel.text(10,105,"price: " + str(stock_price),7)
            pyxel.text(114,7," make " + str(goal) ,7)
            
            pyxel.text(125,85,str(time_m) + " : " + str(time_s),7)
        case 1 :
            pyxel.text(70,60,"YOU WIN",7)
            pyxel.text(30,80,"(press spacebar to play again)",7)
            pyxel.text(30,90,"your score: " + str(score),7)


pyxel.run(update, draw)