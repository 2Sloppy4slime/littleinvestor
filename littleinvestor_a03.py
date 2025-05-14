import pyxel
import random

pyxel.init(160, 120, title = "MAEKMONEH",fps = 30)
pyxel.mouse(True)

#-------------------------VARIABLES-----------------------#
stocks = 10
stock_price = 1
money = 20
bought, sold, score, trades, gamestate, time_s, time_m, mousey, mousex, sellbox, buybox = 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 , [0,0,0,0,0,0] , [0,0,0,0,0,0] #I need to use them through multiple functions sooooo
#gamestate : 0 = normal ; 1 = win ; 2 = faq ; 3 = main menu??
stock_history = []
goal = random.randrange(500,1000)
maxrollpricechange = 300
minrollpricechange = 0
mobilemode = False
#--------------------SECONDARY FUNCTIONS----------------------
oneSecTimer_val = 30
def oneSecTimer():
    global oneSecTimer_val, time_m, time_s
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

def buy() :
    global money, stock_price, stocks, bought, trades
    if money > stock_price :
            stocks += 1
            money -= stock_price
            bought += 1
            trades += 1
def sell() :
    global stocks, money, stock_price, sold, trades
    if stocks > 0:
            money += stock_price
            stocks -= 1 
            sold += 1
            trades += 1 
#-------------------UI_DRAWING_FUNCTIONS------------------
def pricetoheight(price):
    if price > 1:
        return (5 + (80 - price * 16 ))
    else : return (80 - 11*price)


def sensdemouvement(a,b): #green if going up, red if going down
    if a > b: return 8
    else : return 11


def draw_progress():
    global money, goal
    if gamestate == 0 :
        col = 10
        bars = (((int(money)*100)/goal)*65)/100
        for i in range(1,int(bars)+1) :
            if col == 10:
                col = 9
            else :
                col = 10
            pyxel.line(116,80 - i,135,80-i,col)

def draw_stock_history():
    if gamestate == 0 :
        if mobilemode :
            if len(stock_history) >= 2:
                for i in range(len(stock_history)):
                    pyxel.line(i*10, pricetoheight(stock_history[i-1]),10+i*10,pricetoheight(stock_history[i]), sensdemouvement(stock_history[i-1],stock_history[i]))
        else : 
            if len(stock_history) >= 2:
                        for i in range(1,len(stock_history)):
                            pyxel.line(i*10, pricetoheight(stock_history[i-1]),10+i*10,pricetoheight(stock_history[i]), sensdemouvement(stock_history[i-1],stock_history[i]))

def draw_buttons():
    global sellbox,buybox
    match gamestate :
        case 0 :
            if mobilemode :
                sellbox, buybox =  [56,87,45,30,70,100], [3,87,50,30,22,100] 
            else:
                sellbox, buybox = [116,104,38,10,128,106] , [116,93,38,10,128,95]
            pyxel.rect(buybox[0],buybox[1],buybox[2],buybox[3],3) #(116,93) -> (154,103) on pc
            pyxel.text(buybox[4],buybox[5],"buy",7)

            pyxel.rect(sellbox[0],sellbox[1],sellbox[2],sellbox[3],3) #(116,104) -> (154,114) on pc
            pyxel.text(sellbox[4],sellbox[5],"sell",7)

            pyxel.rect(137,15,17,17,7)
            pyxel.text(139,21,"tel",10)
            
                        
def drawbg_ui():
    match gamestate :
        case 0 :
            pos = []
            if mobilemode :
                pos = [(112,0,50,120),(0,81,120,60),(0, 0, 112, 81)]
            else :
                pos = [(115,5,40,110),(10,85,100,30),(9,5,103,79)]
            pyxel.rect(pos[2][0], pos[2][1], pos[2][2], pos[2][3], 0) #stock
            pyxel.rect(pos[0][0], pos[0][1], pos[0][2], pos[0][3], 5) #section droite
            pyxel.rect(pos[1][0], pos[1][1], pos[1][2], pos[1][3], 5)
            pyxel.rect(116,15,20,65,13) # score bar

def draw_stats(): # draws text too lmao
    match gamestate :
        case 0 :
            pos = []
            if mobilemode:
                pos = [(105,86),(105,96),(105,106),(45,81)]
            else:
                pos = [(10,85),(10,95),(10,105),(125,85)]
            pyxel.text(pos[0][0],pos[0][1],"money: " + str(money),7)
            pyxel.text(pos[1][0],pos[1][1],"stocks: " + str(stocks),7)
            pyxel.text(pos[2][0],pos[2][1],"price: " + str(stock_price),7)
            pyxel.text(114,7," make " + str(goal) ,7)
            pyxel.text(pos[3][0],pos[3][1],str(time_m) + " : " + str(time_s),7)
        case 1 :
            pyxel.text(70,60,"YOU WIN",7)
            pyxel.text(30,90,"your score: " + str(score),7)
#-------------------------------------------------------
#                    GameFuncs
#---------------------------------------------------------
def update():
    global money, stock_price, stocks, bought, sold, stock_history, maxrollpricechange, minrollpricechange, mousex, mousey, gamestate, goal, score, trades, mobilemode, sellbox, buybox
    match gamestate:
        case 0: #Main Game
            #-----state changing-----
            if money > goal:
                print("you win")
                gamestate = 1
                score = goal *300 - (60*time_m + time_s)*30 - 10*trades
            #-----Input checking-----
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mousey = pyxel.mouse_x
                mousex = pyxel.mouse_y
                if mousey > sellbox[0] and mousey < sellbox[0] + sellbox[2] and mousex > sellbox[1] and mousex < sellbox[1] + sellbox[3]:
                    sell()
                if mousey > buybox[0] and mousey < buybox[0] + buybox[2] and mousex > buybox[1] and mousex < buybox[1] + buybox[3]:
                    buy()
                if mousey > 137 and mousey < 154 and mousex > 15 and mousex < 23 :
                    mobilemode = not mobilemode

            if pyxel.btnp(pyxel.KEY_B): #acheter
                buy()
            if pyxel.btnp(pyxel.KEY_S): #vendre
                sell()
            if pyxel.btnp(pyxel.KEY_M): #vendre
                mobilemode = not mobilemode
            #-----processing-----
            if oneSecTimer()  :

                deflation = 0
                inflation = 0
                if bought >0:
                    inflation = (random.randrange(0 , 0 +  bought*40) * 0.01)
                if sold >0:
                    deflation = (random.randrange(0 - sold*40, 50-sold*10) * 0.01)
                stock_price = round(stock_price + (float(random.randrange( minrollpricechange , maxrollpricechange)-150) * 0.01) + deflation + inflation , 2)
                #eviter la merde où ça se bloque ds les coins
                if stock_price >= 5 :
                    stock_price = 5
                    minrollpricechange = -150
                    maxrollpricechange = 50
                elif stock_price <= 0 :
                    stock_price = 0.1
                    maxrollpricechange = 350
                    minrollpricechange = 100
                else: 
                    maxrollpricechange = 300
                    minrollpricechange = 0

                bought = 0
                sold = 0

                stock_history.append(stock_price)
                if len(stock_history) > 11 :
                    stock_history.pop(0)

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
    global stock_history, goal, money, time_s, time_m, score
    pyxel.cls(4)
         
    drawbg_ui()   
    draw_progress()
    draw_stock_history()
    draw_buttons()
    draw_stats()
    pyxel.text(95,115,"@SloppySlime2025",7)
    
            
pyxel.run(update, draw)