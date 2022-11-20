from tkinter import *
from tkinter import ttk
import random

class Minesweeper:
    def __init__(self, tk, ttk, size, difficulty):
        self.sizeMap = { "small": 10, "medium": 20, "large": 30 }
        self.difficultyMap = { "easy": [0,4], "medium": [0,3], "hard": [0,2] }
        self.difficulty = self.difficultyMap[difficulty]
        self.size = self.sizeMap[size]
        self.tk = tk
        self.ttk = ttk
        self.tk.geometry(f"{int(self.size * 28.75)}x{int(self.size * 25.75)}")
        self.tk.title("MineSweeper")
        self.frame = ttk.Frame(self.tk, padding="5")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.firstClick = True
        self.tiles = {}
        self.totalBombs = 0

        for row in range(self.size):
            for col in range(self.size):
                id = str(row) + '_' + str(col)

                tile = {
                    "id": id,
                    "coords": {
                        "row": row,
                        "col": col
                    },
                    "button": ttk.Button(self.frame, width=3),
                    "isMine": None,
                    "value": None,
                    "clicked": False,
                    "flagged": False
                }
                tile["button"].bind("<Button-1>", self.clickMine(row,col))
                tile["button"].bind("<Button-3>", self.rightClick(row,col))
                tile["button"].grid(row=row,column=col)

                self.tiles[id] = tile

    def clickMine(self,row,col):
        return lambda Button : self.onClick(self.tiles[f"{row}_{col}"])

    def rightClick(self,row,col):
        return lambda Button : self.onRightClick(self.tiles[f"{row}_{col}"])

    def onRightClick(self, tile):
        if tile["clicked"] == False and tile["flagged"] == False:
            tile["button"].config(text="?")
            tile["flagged"] = True
        elif tile["flagged"] == True and tile["clicked"] == False:
            tile["flagged"] = False
            tile["button"].config(text="")

    def onClick(self, tile):
        if self.firstClick == True:
            self.firstClick = False
            self.randomizeMines(tile)
            self.assignAllTileValues()
            tile["isMine"] = False
            tile["value"] = 0
            tile["button"].config(state = DISABLED)
            tile["clicked"] = True 
            self.chainReveal(tile)
        elif tile["clicked"] == True:
            print(tile)
        elif tile["isMine"] == True and tile["flagged"] == False:
            tile["button"].bell()
            gameover=GameOver(self.tk,self.ttk, self.size)
        elif tile["value"] == 0:
            tile["button"].config(state = DISABLED)
            tile["clicked"] = True 
            self.chainReveal(tile)
        elif tile["flagged"] == True:
            pass
        else:
            tile["button"].config(state = DISABLED)
            tile["clicked"] = True 
            tile["button"].config(text = tile["value"])

    def randomizeMines(self, tile): #take tile arg to asure that the first tile clicked hash a value of 0 meaning no bombs surrond it
        nonMineSpot = []
        nonMineSpot.append(tile)
        for i in self.getTouching(tile):
            row = i["row"]
            col = i["col"]
            nonMineSpot.append(self.tiles[f"{row}_{col}"])
        for i in self.tiles:
            rand = random.randint(self.difficulty[0],self.difficulty[1]) #difficulty
            if rand == 0 and self.tiles[i] not in nonMineSpot:
                self.tiles[i]["isMine"] = True
                self.totalBombs += 1
            else:
                self.tiles[i]["isMine"] = False

    def assignAllTileValues(self):
        for i in self.tiles:
            if self.tiles[i]["isMine"] == True:
                tileValue = 99
                self.tiles[i]["value"] = tileValue
                #self.tiles[i]["button"].config(text=f"{tileValue}")   #*cheats*
            else:
                touching = self.getTouching(self.tiles[i])
                tileValue = self.getValue(touching)
                self.tiles[i]["value"] = tileValue
                #self.tiles[i]["button"].config(text=f"{tileValue}")   #*cheats*
                

    def getTouching(self, tile):
        touching = []
        cordMap = [
            { "row": tile["coords"]["row"], "col": tile["coords"]["col"] + 1 }, #RIGHT
            { "row": tile["coords"]["row"] + 1, "col": tile["coords"]["col"] + 1 }, #BOTTOM-RIGHT
            { "row": tile["coords"]["row"] + 1, "col": tile["coords"]["col"] }, #BOTTOM
            { "row": tile["coords"]["row"] + 1, "col": tile["coords"]["col"] - 1 }, #BOTTOM-LEFT
            { "row": tile["coords"]["row"], "col": tile["coords"]["col"] - 1 }, #LEFT
            { "row": tile["coords"]["row"] - 1, "col": tile["coords"]["col"] - 1 }, #TOPLEFT
            { "row": tile["coords"]["row"] - 1, "col": tile["coords"]["col"] }, #TOP
            { "row": tile["coords"]["row"] - 1, "col": tile["coords"]["col"] + 1 } #TOP-RIGHT
        ]
        for i in cordMap:
            if (i["row"] >= 0 and i["row"] <= self.size - 1 and i["col"] >= 0 and i["col"] <= self.size - 1):
                touching.append(i)
        return touching

    def getValue(self, touching):
        bombCount = 0
        for i in touching:
            row = i["row"]
            col = i["col"]
            if (self.tiles[f"{row}_{col}"]["isMine"] == True):
                bombCount += 1
        return bombCount
    
    def chainReveal(self, tile):
        touching = self.getTouching(tile)
        chain = []
        for i in touching:
            row = i["row"]
            col = i["col"]
            converterdTile = self.tiles[f"{row}_{col}"]
            
            if converterdTile["value"] == 0 and converterdTile["clicked"] == False and converterdTile["flagged"] == False:
                chain.append(converterdTile)
                converterdTile["button"].config(state = DISABLED)
                converterdTile["clicked"] = True
            elif converterdTile["value"] != 0 and converterdTile["flagged"] == False:
                converterdTile["button"].config(state = DISABLED, text=str(converterdTile["value"]))
                converterdTile["clicked"] = True

        for i in chain:
            self.chainReveal(i)
        
        chain = []


class StartMenu:
    def __init__(self, tk, ttk):
        self.tk = tk
        self.tk.geometry("300x300")
        self.tk.eval('tk::PlaceWindow . center')
        self.ttk = ttk
        self.tk.title("Minesweeper")
        self.frame = ttk.Frame(self.tk, width=300, height= 300)
        #self.frame.pack()
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        #self.frame.grid_rowconfigure(0, weight=1)
        #self.frame.grid_columnconfigure(0, weight=1)

        self.size = StringVar()
        self.difficulty = StringVar()
        self.difficulty.set("Difficulty")
        self.size.set("Size")
        self.sizeSelector = self.selectSize = self.ttk.Combobox(self.tk, textvariable=self.size, values=("small","medium","large"), state="readonly")
        self.sizeSelector.place(x=75,y=50)
        #self.size_label = Label(self.frame, text = "select size:").pack(side=BOTTOM)
        #self.difficulty_label = Label(self.frame, text = "select difficutly:").pack(side=BOTTOM, anchor=SW)
        self.difficultySelector = self.selectDifficulty = self.ttk.Combobox(self.tk, textvariable=self.difficulty, values=("easy","medium","hard"), state="readonly")
        self.difficultySelector.place(x=75,y=90)
        self.startBtn = self.ttk.Button(self.frame, width=5, text="Start", command=self.start)
        self.startBtn.place(x=125,y=250)

    def start(self):
        if self.size.get() != "Size" and self.difficulty.get() != "Difficulty":
            self.size = self.size.get()
            self.difficulty = self.difficulty.get()
            self.startBtn.forget()
            self.sizeSelector.forget()
            self.difficultySelector.forget()
            minesweeper = Minesweeper(self.tk, self.ttk, self.size, self.difficulty)
        else:
            self.startBtn.bell()
            print("error")

class GameOver:
    def __init__(self, tk, ttk, size):
        self.tk = tk
        self.size = size
        self.tk.title("Minesweeper")
        self.tk.geometry(f"{int(self.size * 28.75)}x{int(self.size * 25.75)}")
        self.ttk = ttk
        self.frame = ttk.Frame(self.tk, width=300, height= 300)
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.gameOver = Label(self.frame, text = "GAME OVER").place(relx=.45,rely=.45)
        self.restart = Button(self.frame, text="restart").pack(side=BOTTOM, anchor=N)

def main():
    window = Tk()
    startmenu = StartMenu(window, ttk)
    window.mainloop()

if __name__ == "__main__":
    main()
