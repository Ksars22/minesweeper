from tkinter import *
from tkinter import ttk
import sympy as sp
import numpy as np
import random
import time

class Minesweeper:
    def __init__(self, tk, ttk, size, difficulty, botStatus):
        self.sizeMap = { "small": 10, "medium": 20, "large": 30 }
        self.difficultyMap = { "easy": [0,4], "medium": [0,3], "hard": [0,2] }
        self.difficulty = self.difficultyMap[difficulty]
        self.difficultyName = difficulty
        self.size = self.sizeMap[size]
        self.botStatus = botStatus
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
                    "button": ttk.Button(self.frame, width=3, takefocus=False),
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
        if tile["clicked"] == False and tile["flagged"] == False and self.botStatus == False:
            tile["button"].config(text="?")
            tile["flagged"] = True
        elif tile["flagged"] == True and tile["clicked"] == False and self.botStatus == False:
            tile["flagged"] = False
            tile["button"].config(text="")

    def onClick(self, tile):
        if self.firstClick == True:
            if self.botStatus:
                self.botSolve(tile)
            else:
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
        elif tile["isMine"] == True and tile["flagged"] == False and self.botStatus == False:
            tile["button"].bell()
            gameover=GameOver(self.tk,self.ttk, self.size, self.difficultyName)
        elif tile["value"] == 0 and self.botStatus == False:
            tile["button"].config(state = DISABLED)
            tile["clicked"] = True 
            self.chainReveal(tile)
        elif tile["flagged"] == True:
            pass
        elif self.firstClick == True and self.botStatus == True:
            print("bot")
        elif self.botStatus == False:
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

    def botSolve(self,tile):
        self.solved = False
        self.firstClick = False
        self.randomizeMines(tile)
        self.assignAllTileValues()
        tile["isMine"] = False
        tile["value"] = 0
        tile["button"].config(state = DISABLED)
        tile["clicked"] = True
        self.chainReveal(tile)
        infoTiles = []
        self.borderTiles = []
        self.knownBombs = []
        self.safeTiles = []
        #while not self.solved:
        for i in range(20):
            for i in self.tiles:
                checkTouching = self.getTouching(self.tiles[i])
                allClicked = True
                for tile in checkTouching:
                    row = tile["row"]
                    col = tile["col"]
                    convTile = self.tiles[f"{row}_{col}"]
                    if convTile["clicked"] == False:
                        allClicked = False
                if self.tiles[i]["clicked"] and self.tiles[i]["value"] != 0 and allClicked == False:
                    infoTiles.append(self.tiles[i])
            
            for tile in infoTiles:
                touching = self.getTouching(tile)
                nonRevealedTouching = []
                for i in touching:
                    row = i["row"]
                    col = i["col"]
                    if self.tiles[f"{row}_{col}"]["clicked"] == False:
                        nonRevealedTouching.append(self.tiles[f"{row}_{col}"])
                for tile in nonRevealedTouching:
                    if tile["coords"] not in self.borderTiles:
                        self.borderTiles.append(tile["coords"])

            self.matrix = []
            self.singleMatrix = []
            print(len(self.borderTiles))
            print(len(infoTiles))
            #print(self.matrix)
            #print(self.singleMatrix)
            self.new_borders = []
            for tile in infoTiles:
                row = tile["coords"]["row"]
                col = tile["coords"]["col"]
                self.singleMatrix.append(tile["value"])
                borders = self.getTouching(tile)
                #print(borders)
                curr_borders = []
                for i in borders:
                    row = i["row"]
                    col = i["col"]
                    if self.tiles[f"{row}_{col}"]["clicked"] == False and self.tiles[f"{row}_{col}"]["coords"] not in self.new_borders:
                        curr_borders.append(self.tiles[f"{row}_{col}"]["coords"])
                self.new_borders.append(curr_borders)
            print(self.borderTiles)
            for i in range(len(self.new_borders)):
                matrixRow = sp.Matrix(len(infoTiles),len(self.borderTiles), self.f)
            #print(matrixRow,self.singleMatrix)
            secondMatrix = sp.Matrix(len(self.singleMatrix), 1, self.singleMatrix)
            print(secondMatrix)
            final = matrixRow.row_join(secondMatrix)
            final = final.rref()
            final_rref_matrix = final[0]
            print(final_rref_matrix)
            for row in range(len(infoTiles)):
                rowEq = []
                for i in range(len(self.borderTiles) + 1):
                    if i == len(self.borderTiles):
                        rowEq.append(final_rref_matrix[row,i])
                    elif final_rref_matrix[row,i] == 1:
                        tile = {
                            "row": self.borderTiles[i]["row"],
                            "col": self.borderTiles[i]["col"],
                            "positive": True
                        }
                        rowEq.append(tile)
                    elif final_rref_matrix[row,i] == -1:
                        tile = {
                            "row": self.borderTiles[i]["row"],
                            "col": self.borderTiles[i]["col"],
                            "positive": False
                        }
                        rowEq.append(tile)
                self.matrixSolutions = self.possibleRowEqSolutions(rowEq)
                for i in self.matrixSolutions["knownBombs"]:
                    row = i["row"]
                    col = i["col"]
                    self.knownBombs.append(self.tiles[f"{row}_{col}"])
                for j in self.matrixSolutions["safeTiles"]:
                    row = j["row"]
                    col = j["col"]
                    self.safeTiles.append(self.tiles[f"{row}_{col}"])
            self.botMove(self.safeTiles, self.knownBombs)
            moveStatus = self.checkMove()
            if moveStatus == "GAME_OVER":
                gameover = GameOver(self.tk, self.ttk, self.size, self.difficulty)
                self.solved = True
            elif moveStatus == "GAME_WIN":
                self.solved = True
            infoTiles.clear()
            self.borderTiles.clear()
            self.knownBombs.clear()
            self.safeTiles.clear()

    def checkMove(self):
        allClicked = True
        for tile in self.tiles.values():
                if tile["clicked"] == True and tile["isMine"] == True:
                    return "GAME_OVER"
                elif tile["clicked"] == False:
                    allClicked = False
                else:
                    return "VALID"
        if allClicked == True:
            return "GAME_WIN"
    
    def possibleRowEqSolutions(self, row):
        knownBombs = []
        safeTiles = []
        if (len(row) - 1) == row[-1]:
            for i in range(len(row) -1):
                knownBombs.append(row[i])
        elif len(row) == 2:
            if row[-1] == 0:
                safeTiles.append(row[0])
            if row[-1] == 1:
                knownBombs.append(row[0])
        else:
            allPos = True
            for i in range(len(row) - 1):
                if row[i]["positive"] == False:
                    allPos = False
            if allPos == True and row[-1] == 0:
                for i in range(len(row)-1):
                    safeTiles.append(row[i])
            elif allPos != True and row[-1] in [-1,1] and len(row) == 3:
                if row[-1] == 1:
                    knownBombs.append(row[0])
                    if row[1] not in safeTiles:
                        safeTiles.append(row[1])
                elif row[-1] == -1:
                    safeTiles.append(row[0])
                    if row[1] not in safeTiles:
                        knownBombs.append(row[1])

        return { "knownBombs": knownBombs, "safeTiles": safeTiles, }

    def f(self, i,j):
        #print(self.new_borders[i],self.borderTiles[j])
        if self.borderTiles[j] in self.new_borders[i]:
            return 1
        else:
            return 0

    def botMove(self,safeTiles,knownBombs):
        print(safeTiles,knownBombs)
        if len(safeTiles) == 0:
            randRow = random.randint(0, self.size -1)
            randCol = random.randint(0, self.size -1)
            print(randRow,randCol)
            randTile = self.tiles[f"{randRow}_{randCol}"]
            if randTile["isMine"] == True:
                gameover = GameOver(self.tk,self.ttk,self.size,self.difficulty)
                self.solved = True
            if randTile["value"] == 0:
                self.chainReveal(randTile)
            else:
                randTile["button"].config(state=DISABLED, text=randTile["value"])
                randTile["clicked"] = True
        else:
            for bomb in knownBombs:
                bomb["button"].config(text="?")
                bomb["flagged"] = True
            for tile in safeTiles:
                if tile["value"] == 0:
                    self.chainReveal(tile)
                else:
                    tile["button"].config(state=DISABLED, text=str(tile["value"]))
                    tile["clicked"] = True

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
        self.botStatus = IntVar()
        self.botBtn = self.ttk.Checkbutton(self.frame, variable=self.botStatus, offvalue=False, onvalue=True, takefocus=False, text="Enable bot")
        self.botBtn.place(x=110,y=225)
        self.startBtn = self.ttk.Button(self.frame, width=5, text="Start", command=self.start)
        self.startBtn.place(x=125,y=250)

    def start(self):
        if self.size.get() != "Size" and self.difficulty.get() != "Difficulty":
            self.size = self.size.get()
            self.difficulty = self.difficulty.get()
            self.botStatus = self.botStatus.get()
            self.botBtn.forget()
            self.startBtn.forget()
            self.sizeSelector.forget()
            self.difficultySelector.forget()
            minesweeper = Minesweeper(self.tk, self.ttk, self.size, self.difficulty, self.botStatus)
        else:
            self.startBtn.bell()
            print("error")

class GameOver:
    def __init__(self, tk, ttk, size, difficulty):
        self.tk = tk
        self.difficulty = difficulty
        self.size = size
        self.tk.title("Minesweeper")
        self.tk.geometry(f"{int(self.size * 28.75)}x{int(self.size * 25.75)}")
        self.ttk = ttk
        self.frame = ttk.Frame(self.tk, width=300, height= 300)
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.gameOver = Label(self.frame, text = "GAME OVER")
        self.gameOver.place(relx=.45,rely=.45)
        self.restartBtn = Button(self.frame, text="restart")
        self.restartBtn.pack(side=BOTTOM, anchor=N)
        self.restartBtn.bind("<Button-1>", self.clickWrapper())

    def clickWrapper(self):
        return lambda Button : self.restart()

    def restart(self):
        self.gameOver.forget()
        self.restartBtn.forget()
        startmenu = StartMenu(self.tk, self.ttk)




def main():
    window = Tk()
    startmenu = StartMenu(window, ttk)
    window.mainloop()

if __name__ == "__main__":
    main()


#go through infotiles for each tile create an array length of boderTiles with a 1 at each tile index?
#
#
#