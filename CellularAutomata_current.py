from tkinter import *
from time import sleep
import sys
sys.setrecursionlimit(10**9)
from random import choice

class Automata:

	def __init__(self, root):
		self.height = 700
		self.width = 1200
		self.cellSize = 4
		self.color = 'black'
		self.root = root
		self.canvas = Canvas(self.root, height = self.height, width = self.width)
		frame = Frame(self.root)
		frame.grid(row = 0, column = 0)
		self.canvas.grid(row = 1, column = 0)
		self.cells = ['sentinelRow']
		for row in range(self.height):
			cellRow = ['sentinelColumn']
			if row % self.cellSize == 0:
				for column in range(self.width):
					if column % self.cellSize == 0:
						cellRow.append(self.canvas.create_rectangle(column, row, column + self.cellSize, row + self.cellSize, fill = 'white'))
			if cellRow != ['sentinelColumn']:
				cellRow.append('sentinelColumn')
				self.cells.append(cellRow)
		self.cells.append('sentinelRow')
		self.array = []
		self.emptyArray = []
		subArray = []
		subArray1 = []
		for row in range(int((self.height / self.cellSize) + 2)):
			for column in range(int((self.width / self.cellSize) + 2)):
				subArray.append(0)
				subArray1.append(0)
				if column == (self.width / self.cellSize) + 1:
					self.array.append(subArray)
					self.emptyArray.append(subArray1)
					subArray = []
					subArray1 = []
		self.ruleByte = [0, 0, 0, 1, 1, 1, 1, 0]
		frame1 = Frame(self.root)
		frame1.grid(row = 2, column = 0)
		self.runButton = Button(frame1, text = 'Run', bg = '#CCCCCC', command = self.run)
		self.runButton.pack(side = LEFT)
		spacer = Label(frame1, text = ' ') # spacer
		spacer.pack(side = LEFT)
		self.clearButton = Button(frame1, text = 'Clear', bg = '#CCCCCC', command = self.clear)
		self.clearButton.pack(side = LEFT)
		spacer1 = Label(frame1, text = ' ') # spacer
		spacer1.pack(side = LEFT)
		quitButton = Button(frame1, text = 'Quit', bg = '#CCCCCC', command = self.quit)
		quitButton.pack(side = LEFT)
		self.canvas.bind('<Button-1>', self.populate)
		self.pens = ['Populate', 'Depopulate']
		self.currentPen = StringVar()
		self.currentPen.set(self.pens[0])
		penMenu = OptionMenu(frame, self.currentPen, *self.pens)
		penMenu.config(bg = '#CCCCCC')
		penMenu.pack(side = LEFT)
		spacer2 = Label(frame, text = ' ') # spacer
		spacer2.pack(side = LEFT)
		self.ruleSets = ["Elementary cellular automata", "John Conway's Game of Life", "Chaos automaton"]
		self.currentRuleSet = StringVar()
		self.currentRuleSet.set(self.ruleSets[0])
		ruleSetMenu = OptionMenu(frame, self.currentRuleSet, *self.ruleSets)
		ruleSetMenu.config(bg = '#CCCCCC')
		ruleSetMenu.pack(side = LEFT)
		spacer3 = Label(frame, text = ' ') # spacer
		spacer3.pack(side = LEFT)
		self.base10Rule = StringVar()
		ruleEntry = Entry(frame, textvariable = self.base10Rule, width = 3)
		ruleEntry.pack(side = LEFT)
		spacer4 = Label(frame, text = ' ') # spacer
		spacer4.pack(side = LEFT)
		setRuleButton = Button(frame, text = 'Set elementary rule', bg = '#CCCCCC', command = self.setElementaryRule)
		setRuleButton.pack(side = LEFT)
		spacer5 = Label(frame, text = ' ') # spacer
		spacer5.pack(side = LEFT)
		ruleLabel = Label(frame, text = 'Valid rules: 0-255 (inclusive)  |  Current rule: ', font = ('bold'))
		ruleLabel.pack(side = LEFT)
		self.ruleLabel1 = Label(frame, text = '30', font = ('bold'))
		self.ruleLabel1.pack(side = LEFT)
		
	def setElementaryRule(self):
		if self.base10Rule.get().isnumeric() and int(self.base10Rule.get()) > -1 and int(self.base10Rule.get()) < 256:
			self.ruleLabel1.config(text = self.base10Rule.get())
			for i in range(8):
				self.ruleByte[i] = 0
			index = 8
			for i in reversed(str(bin(int(self.base10Rule.get())))):
				index -= 1
				if i == '1':
					self.ruleByte[index] = 1

	def populate(self, event): # deals with populating and depopulating cells
		row = int(event.y / self.cellSize)
		column = int(event.x / self.cellSize)
		if self.currentPen.get() == self.pens[0]:
			self.array[row+1][column+1] = 1
			self.canvas.itemconfig(self.cells[row+1][column+1], fill = self.color)
		if self.currentPen.get() == self.pens[1]:
			self.array[row+1][column+1] = 0
			self.canvas.itemconfig(self.cells[row+1][column+1], fill = 'white')

	def disablePopulate(self, event):
		pass

	def run(self):
		self.canvas.bind('<Button-1>', self.disablePopulate)
		self.runButton.config(text = 'Running...', state = DISABLED)
		if self.currentRuleSet.get() == self.ruleSets[0]: # elementary cellular automata
			for row in range(1, int(self.height / self.cellSize)):
				for column in range(1, int((self.width / self.cellSize) + 1)):				
					if self.array[row][column-1] == 1 and self.array[row][column] == 1 and self.array[row][column+1] == 1:
						self.array[row+1][column] = self.ruleByte[0]
					if self.array[row][column-1] == 1 and self.array[row][column] == 1 and self.array[row][column+1] == 0:
						self.array[row+1][column] = self.ruleByte[1]
					if self.array[row][column-1] == 1 and self.array[row][column] == 0 and self.array[row][column+1] == 1:
						self.array[row+1][column] = self.ruleByte[2]
					if self.array[row][column-1] == 1 and self.array[row][column] == 0 and self.array[row][column+1] == 0:
						self.array[row+1][column] = self.ruleByte[3]
					if self.array[row][column-1] == 0 and self.array[row][column] == 1 and self.array[row][column+1] == 1:
						self.array[row+1][column] = self.ruleByte[4]
					if self.array[row][column-1] == 0 and self.array[row][column] == 1 and self.array[row][column+1] == 0:
						self.array[row+1][column] = self.ruleByte[5]
					if self.array[row][column-1] == 0 and self.array[row][column] == 0 and self.array[row][column+1] == 1:
						self.array[row+1][column] = self.ruleByte[6]
					if self.array[row][column-1] == 0 and self.array[row][column] == 0 and self.array[row][column+1] == 0:
						self.array[row+1][column] = self.ruleByte[7]
					if self.array[row+1][column] == 1:
						self.canvas.itemconfig(self.cells[row+1][column], fill = self.color)
					if self.array[row+1][column] == 0:
						self.canvas.itemconfig(self.cells[row+1][column], fill = 'white')						
				self.canvas.update()
		if self.currentRuleSet.get() == self.ruleSets[1] or self.currentRuleSet.get() == self.ruleSets[2]: # John Conway's Game of Life or a random 2D automaton
			successorArray = []
			subArray = []
			for row in range(int((self.height / self.cellSize) + 2)):
				for column in range(int((self.width / self.cellSize) + 2)):
					subArray.append(0)
					if column == (self.width / self.cellSize) + 1:
						successorArray.append(subArray)
						subArray = []
			for row in range(1, int((self.height / self.cellSize) + 1)):
				for column in range(1, int((self.width / self.cellSize) + 1)):
					neighborCounter = 0
					if self.array[row-1][column+1] == 1:
						neighborCounter += 1
					if self.array[row-1][column] == 1:
						neighborCounter += 1
					if self.array[row-1][column-1] == 1:
						neighborCounter += 1
					if self.array[row][column-1] == 1:
						neighborCounter += 1
					if self.array[row+1][column-1] == 1:
						neighborCounter += 1
					if self.array[row+1][column] == 1:
						neighborCounter += 1
					if self.array[row+1][column+1] == 1:
						neighborCounter += 1
					if self.array[row][column+1] == 1:
						neighborCounter += 1						
					if self.currentRuleSet.get() == self.ruleSets[1]:						
						if neighborCounter < 2 and self.array[row][column] == 1:
							successorArray[row][column] = 0
						elif (neighborCounter == 2 or neighborCounter == 3) and self.array[row][column] == 1:
							successorArray[row][column] = 1
						elif neighborCounter > 3 and self.array[row][column] == 1:
							successorArray[row][column] = 0
						elif neighborCounter == 3 and self.array[row][column] == 0:
							successorArray[row][column] = 1							
					if self.currentRuleSet.get() == self.ruleSets[2]:
						if neighborCounter < choice(range(9)) and self.array[row][column] == choice(range(2)):
							successorArray[row][column] = choice(range(2))
						elif (neighborCounter == choice(range(9)) or neighborCounter == choice(range(9))) and self.array[row][column] == choice(range(2)):
							successorArray[row][column] = choice(range(2))
						elif neighborCounter > choice(range(9)) and self.array[row][column] == choice(range(2)):
							successorArray[row][column] = choice(range(2))
						elif neighborCounter == choice(range(9)) and self.array[row][column] == choice(range(2)):
							successorArray[row][column] = choice(range(2))						
					if successorArray[row][column] == 0:
						self.canvas.itemconfig(self.cells[row][column], fill = 'white')
					elif successorArray[row][column] == 1:
						self.canvas.itemconfig(self.cells[row][column], fill = self.color)							
			self.array = successorArray
			self.canvas.update()
			if self.array != self.emptyArray:
				self.run()
		self.runButton.config(text = 'Run', state = NORMAL)
		self.canvas.bind('<Button-1>', self.populate)

	def clear(self):
		self.canvas.bind('<Button-1>', self.disablePopulate)
		self.runButton.config(state = DISABLED)
		self.clearButton.config(text = 'Clearing...', state = DISABLED)
		for row in range(int(self.height / self.cellSize), 0, -1):
			for column in range(int(self.width / self.cellSize), 0, -1):
				self.array[row][column] = 0
				self.canvas.itemconfig(self.cells[row][column], fill = 'white')
			self.canvas.update()
		self.clearButton.config(text = 'Clear', state = NORMAL)
		self.runButton.config(state = NORMAL)
		self.canvas.bind('<Button-1>', self.populate)

	def quit(self):
		self.root.destroy()


def main():
	root = Tk()
	root.title("Cellular Automata")
	start = Automata(root)
	root.mainloop()

if __name__ == '__main__':
	main()