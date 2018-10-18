# Jane's tp project!

import tkinter 
import math
from tkinter import *
from finalhuffman import *

# Basic animation framework taken from timer based animation notes

def init(data):
	data.startScreen = True
	data.getFileScreen = False
	data.fileName = ""
	data.getCodeScreen = False
	data.saveOptionScreen = False
	data.finishedEncoding = False
	data.saveName = ""
	data.freqScreen = False
	data.treeScreen = False
	data.whatHuffmanScreen = False
	data.explanationPart = 0
	data.usertyped = ""
	data.fileBoxClicked = False
	data.saveBoxClicked = False
	data.margin = 15
	data.pageTitleMargin = data.height/4
	data.huffmanCode = dict()
	data.typed = False
	data.typedG,data.typedO = False,False
	data.startTree = False
	data.timerDelay = 1000
	data.leaves = []
	data.leafInfo = []
	data.freqDict = dict()
	data.leafSize = 20
	data.currOrigSize = 0
	data.currNewSize = 0

def mousePressed(event, data): #information needed when user pressed back or next buttons
	titleX,titleY = 3,4
	buttonSizeX,buttonSizeY = data.width/titleX,data.height/10
	textboxIndex = data.width/10
	if not data.startScreen and not data.whatHuffmanScreen:
		if (20<=event.x<=80 and data.height-20>=event.y>=data.height-50):
			if data.freqScreen: data.freqScreen,data.startScreen=False,True
			elif data.treeScreen: 
				data.treeScreen,data.freqScreen= False,True
				data.startTree,data.typedG,data.typedO=False,False,False
				data.leafInfo.clear()
				addLeafInfo(event,data)
				setLeafLocation(data)
			elif data.getFileScreen: data.getFileScreen,data.startScreen=False,True
			elif data.getCodeScreen: data.getCodeScreen,data.getFileScreen=False,True
			elif data.saveOptionScreen: data.saveOptionScreen,data.getCodeScreen=False,True
	if data.startScreen:
		leftOverIndex = data.pageTitleMargin+80
		buttonAllowedHeight = data.height-leftOverIndex-30
		buttonHeight = buttonAllowedHeight/5
		buttonIndex = buttonAllowedHeight/10
		if (data.width/(titleY+1)<=event.x<=data.width/2+buttonSizeX and
			leftOverIndex+buttonIndex<=event.y<=leftOverIndex+buttonIndex+buttonHeight): 
			#learn more option
			data.startScreen = False
			data.whatHuffmanScreen = True
			data.explanationPart += 1
		elif (data.width/(titleY)<=event.x<=data.width/2+buttonSizeX and 
			leftOverIndex+2*buttonHeight<=event.y<=leftOverIndex+3*buttonHeight): 
			#get encoding info option
			data.startScreen = False
			data.getFileScreen = True
		elif (data.width/(titleY)<=event.x<=data.width/2+buttonSizeX and 
			leftOverIndex+7*buttonIndex<=event.y<=leftOverIndex+9*buttonIndex):
			#visualize option
			data.startScreen = False
			data.freqScreen = True
	elif data.freqScreen: #if user clicks "next" button, go to tree screen
		if (data.width-data.width/8*1.5<=event.x<=data.width-data.width/24 and
			data.pageTitleMargin/4<=event.y<=data.width-data.pageTitleMargin*7/12):
			data.freqScreen,data.treeScreen = False,True
	elif data.treeScreen and data.startTree:
		if (data.width-130<=event.x<=data.width-20 and 
			data.height-50<=event.y<=data.height-20):
			data.treeScreen,data.startScreen,data.typed=False,True,False
			data.usertyped = ""
			data.leaves.clear()
			data.leafInfo.clear()
	elif data.getFileScreen:
		if (textboxIndex<=event.x<=data.width-textboxIndex and 
			data.pageTitleMargin*2+buttonSizeY<=event.y
			<=data.pageTitleMargin*2+buttonSizeY*2):
			data.fileBoxClicked = True
		else: data.fileBoxClicked = False
		if (data.width-textboxIndex*3<=event.x<=data.width-textboxIndex-10 and
			data.pageTitleMargin*3<=event.y<=data.pageTitleMargin*3+buttonSizeY/2):
			data.fileSubmitted = True
			data.getFileScreen = False
			data.getCodeScreen = True
	elif data.getCodeScreen:
		if (data.width-80<=event.x<=data.width-20 and data.height-20>=event.y>=
			data.height-50):
			data.getCodeScreen = False
			data.saveOptionScreen = True
	elif data.saveOptionScreen:
		if (data.width/10<=event.x<=data.width-data.width/10 and 
			data.pageTitleMargin*2-data.height/10<=event.y<=data.pageTitleMargin*2):
			data.saveBoxClicked = True
		else: data.saveBoxClicked = False
		if (data.width/10+15<=event.x<=data.width/3+5 and 
			data.height/2+20<=event.y<=data.height/2+50):
			exportCode(data.fileName,data.saveName)
			data.saveOptionScreen = False
			data.finishedEncoding = True
		elif (data.width*3/5-35<=event.x<=data.width-55 and 
			data.height/2+20<=event.y<=data.height/2+50):
			exportCompressed(data.fileName,data.saveName)
			data.saveOptionScreen = False
			data.finishedEncoding = True
	elif data.finishedEncoding: #back to menu
		if (data.width/2-65<=event.x<=data.width/2+65 and
			data.height*4/5+25<=event.y<=data.height*4/5+65):
			data.finishedEncoding = False
			data.startScreen = True
	elif data.whatHuffmanScreen and data.explanationPart>=4:
		if (data.width/2-60<=event.x<=data.width/2+60 and
			data.height/2-20<=event.y<=data.height/2+20):
			data.whatHuffmanScreen=False
			data.explanationPart = 0
			data.startScreen=True

def keyPressed(event, data): #information for collecting typed text and arrow navigation
	if data.whatHuffmanScreen:
		if event.keysym == "Right" or event.keysym == "Up":
			data.explanationPart += 1
		elif event.keysym == "Left" or event.keysym == "Down":
			data.explanationPart -= 1
			if data.explanationPart == 0:
				data.startScreen = True
				data.whatHuffmanScreen = False
	elif data.getFileScreen:
		if data.fileBoxClicked:
			if event.keysym != "BackSpace":
				data.fileName = data.fileName[:]+event.char
			else: data.fileName = data.fileName[:-1]
	elif data.saveOptionScreen:
		if data.saveBoxClicked:
			if event.keysym != "BackSpace":
				data.saveName = data.saveName[:]+event.char
			else: data.saveName = data.saveName[:-1]
	elif data.freqScreen:
		if event.keysym == "Right" or event.keysym == "Up":
			data.freqScreen,data.treeScreen= False,True
		if event.keysym == "Left" or event.keysym == "Down":
			data.explanationPart -= 1
			data.freqScreen = False
			data.whatHuffmanScreen = True
		addLeafInfo(event,data)
	elif data.treeScreen: #type in GO and enter to start animation
		if event.keysym == "Left" or event.keysym == "Down":
			data.treeScreen = False
			data.freqScreen = True
		elif event.char == "g": data.typedG = True
		elif event.char == "o": data.typedO = True
		if data.typedG and data.typedO:
			if event.keysym == "Return":
				data.startTree = True

def addLeafInfo(event,data): #for the visualization - adds characters from the frequency screen
	if not event.char == "\x08": #as long as it's not a backspace
		data.usertyped = data.usertyped[:] + event.char
		if event.keysym == "Space":
			if "[s]" not in data.leaves:
				data.leaves.append("[s]")
		elif event.keysym == "Tab":
			if "[t]" not in data.leaves:
				data.leaves.append("[t]")
		elif event.keysym == "Return":
			if "[r]" not in data.leaves:
				data.leaves.append("[r]")
		else: 
			if event.char not in data.leaves:
				data.leaves += event.char
		data.typed = True
	if event.keysym == "BackSpace": 
		data.usertyped = data.usertyped[:-1]
		if data.leaves[-1] not in data.usertyped:
			data.leaves.pop()
	setLeafLocation(data)

def setLeafLocation(data): #sets the location of each leaf
	leafIndex = data.width/(len(data.leaves)+1)
	newLeafLocations = []
	for leaf in range(len(data.leaves)):
		leafX = leafIndex*(leaf+1)
		leafY = data.pageTitleMargin
		newLeafLocations.append([leafX,leafY])
	data.leafInfo = newLeafLocations

def timerFired(data): #start counting once animation has been cued
	if data.startTree and data.usertyped != 0:
		moveLeaves(data)
		
def drawStartScreen(canvas,data): # basic start screen info
	titleX,titleY = 3,4
	buttonSizeX,buttonSizeY = data.width/titleX,data.height/10
	canvas.create_rectangle(0,0,data.width,data.height,fill="snow"
		,outline="dodgerblue3",width=10)
	canvas.create_text(data.width/2,data.pageTitleMargin/2+40, fill="gray12",
				text="Data Compression",font="palatino 32 bold")
	canvas.create_text(data.width*titleX/10,data.pageTitleMargin+25,
		fill="dodger blue",anchor=W,text="with Huffman Trees", font="palatino 20 bold")
	#buttons user can click on
	leftOverIndex = data.pageTitleMargin+80
	buttonAllowedHeight = data.height-leftOverIndex-30
	buttonHeight = buttonAllowedHeight/5
	buttonIndex = buttonAllowedHeight/10
	canvas.create_rectangle(data.width/(titleY+1),leftOverIndex+buttonIndex,
		data.width/2+buttonSizeX,leftOverIndex+buttonIndex+buttonHeight,
		fill="honeydew",width=3,outline = "springgreen4")
	canvas.create_text(data.width/2+10,leftOverIndex+buttonHeight,text="Learn More!",
		font="palatino 15",fill="springgreen4",justify= "center")
	canvas.create_rectangle(data.width/(titleY+1),leftOverIndex+2*buttonHeight, 
		data.width/2+buttonSizeX,leftOverIndex+3*buttonHeight,
		fill="lavender blush",width=3,outline="deep pink")
	canvas.create_text(data.width/2+10,leftOverIndex+5*buttonIndex,text="Get Encoding Data",
		font="palatino 15",fill="deep pink",justify="center")
	canvas.create_rectangle(data.width/(titleY+1),leftOverIndex+7*buttonIndex,
		data.width/2+buttonSizeX,leftOverIndex+9*buttonIndex,
		fill="lavender",width=3,outline="blue violet")
	canvas.create_text(data.width/2+10,leftOverIndex+4*buttonHeight,text="Visualize Tree",
		font="palatino 15",fill="blue violet",justify="center")

def drawGetFileScreen(canvas,data): #"textbox" where user enters name of desired text info
	textboxIndex,writeIndex = data.width/10,1.5
	buttonSizeX,buttonSizeY = data.width/3,data.height/10
	canvas.create_rectangle(0,0,data.width,data.height,fill="lavender blush",
		outline="deep pink",width=10)
	#back button
	canvas.create_rectangle(20,data.height-20,80,data.height-50,fill="lemon chiffon",
		outline="gold",width=3)
	canvas.create_text(50,data.height-35,text="Back",font="arial 10",fill="grey11")
	canvas.create_text(data.width/2,data.pageTitleMargin,text="Obtain Huffman Code",
		fill="deep pink",font="palatino 20 bold")
	borderTriggered,bordercolor = 0, None
	if data.fileBoxClicked: 
		borderTriggered,bordercolor = 2,"grey20"
	canvas.create_rectangle(textboxIndex,data.pageTitleMargin*2+buttonSizeY,
		data.width-textboxIndex,data.pageTitleMargin*2+buttonSizeY*2,
		fill="gainsboro",width=borderTriggered,outline=bordercolor)
	canvas.create_text(data.width/2,data.pageTitleMargin*2,
		text="Type in the name of your file below:", font="arial 15", fill="grey11")
	canvas.create_text(data.width/2,data.pageTitleMargin*2+buttonSizeY*writeIndex,
		text="%s"%data.fileName,font="arial 15",justify="left")
	canvas.create_rectangle(data.width-textboxIndex*3,data.pageTitleMargin*3,
		data.width-textboxIndex-10,data.pageTitleMargin*3+buttonSizeY/2,
		fill="lemon chiffon",outline="gold",width=3)
	canvas.create_text(data.width-textboxIndex*2-5,data.pageTitleMargin*3+buttonSizeY/4,
		text="Done",fill="grey8")

def drawGetCodeScreen(canvas,data): #screen displaying huffman code generated from user's file
	try:
		usersFile = open("%s.txt"%data.fileName,"r")
		usersFileContent = ""
		for entry in usersFile:
			usersFileContent = usersFileContent[:]+entry
		usersCode = getTree(usersFileContent)
	except:
		usersCode = "No such text file named %s"%data.fileName
	canvas.create_rectangle(0,0,data.width,data.height,fill="lavender blush",
		outline="deep pink",width=10)
	#back button
	canvas.create_rectangle(20,data.height-20,80,data.height-50,fill="lemon chiffon",
		outline="gold",width=3)
	canvas.create_text(50,data.height-35,text="Back",font="arial 10",fill="grey11")
	canvas.create_text(data.width/2,10,justify="center",anchor=N,
		text="Huffman Code for file:\n'%s.txt'"%data.fileName,fill="deep pink",
		font="palatino 20 bold")
	if isinstance(usersCode,dict):
		numLines,linesIndex = len(usersCode),90
		linesHeight,lineNumber = data.height-linesIndex,0
		lineSize = linesHeight/(numLines/2)
		newCol = False
		maxCol = False
		xStart = 35
		for key in usersCode:
			if (lineNumber+1)*lineSize+linesIndex+40>=data.height and newCol == False:
				xStart = 155
				lineNumber = 0
				newCol = True
			elif (lineNumber+1)*lineSize+linesIndex+40>=data.height and maxCol == False:
				xStart = data.width/2+85
				lineNumber = 0
				maxCol = True
			canvas.create_text(xStart+60,lineNumber*lineSize+linesIndex,
				text=usersCode[key],font="courier 10")
			if key == "\t": key = "tab"
			elif key == "\n": key = "return"
			elif key == " ": key = "space"
			canvas.create_text(xStart,lineNumber*lineSize+linesIndex,text=key,font="courier 10")
			lineNumber += 1
	else:
		canvas.create_text(data.width/2,data.height/2,text=usersCode,
			fill="black",font="arial",width=data.width-20)
	if not usersCode == "No such text file named %s"%data.fileName:
		canvas.create_rectangle(data.width-20,data.height-20,data.width-80,data.height-50,
			fill="lemon chiffon",outline="deep pink",width=3)
		canvas.create_text(data.width-50,data.height-35,text="Save?",
			fill="grey11",font="arial 10")

def drawSaveOptionScreen(canvas,data): #option where user can save the encoding information
	canvas.create_rectangle(0,0,data.width,data.height,fill="lavender blush",
		outline="deep pink",width=10)
	#back button
	canvas.create_rectangle(20,data.height-20,80,data.height-50,
		fill="lemon chiffon",outline="gold",width=3)
	canvas.create_text(50,data.height-35,text="Back",font="arial 10",fill="grey11")
	canvas.create_text(data.width/2,data.pageTitleMargin,anchor=S,
		text="Save Options:",fill="deep pink",font="palatino 20 bold")
	#two save options:
	borderTriggered,bordercolor = 0,None
	if data.saveBoxClicked: 
		borderTriggered,bordercolor = 2,"grey20"
	canvas.create_rectangle(data.width/10,data.pageTitleMargin*2-data.height/10,
		data.width-data.width/10,data.pageTitleMargin*2,
		fill="gainsboro",width=borderTriggered,outline=bordercolor)
	canvas.create_text(data.width/2,data.pageTitleMargin*2-data.height/20,justify="left",
		text="%s"%data.saveName, fill="grey11",font="arial 15")
	canvas.create_rectangle(data.width/10+15,data.height/2+20,data.width/3+5,data.height/2+50,
		fill="lemon chiffon",outline="gold",width=3)
	canvas.create_text((data.width/10+15+data.width/3+5)/2,data.height/2+35,text="Export Code")
	canvas.create_rectangle(data.width*3/5-35,data.height/2+20,data.width-55,data.height/2+50,
		fill="lemon chiffon",outline="gold",width=3)
	canvas.create_text((data.width*3/5-35+data.width-55)/2,data.height/2+35,
		text="Export Compressed File")

def drawFinishedEncodingScreen(canvas,data): #shows user animation of how much data space they saved
	canvas.create_rectangle(0,0,data.width,data.height,fill="lavender blush",
		outline="deep pink",width=10)
	canvas.create_text(data.width/2,data.height*4/5,text="Saved.",fill="deep pink",
		font="palatino 20")
	canvas.create_rectangle(data.width/2-65,data.height*4/5+25,
		data.width/2+65,data.height*4/5+65,	fill="lemon chiffon", outline="deep pink",width=3)
	canvas.create_text(data.width/2,data.height*4/5+45,fill="grey11",font="palatino 12",
		text="Back To Menu")
	canvas.create_text(data.width/2,data.pageTitleMargin/3,text="You Saved:",
		font="palatino",fill="grey11")
	sizeInfo = getSize(data.fileName)
	origSize = (sizeInfo[0])/40
	newSize = (sizeInfo[1])/40
	origCenterX,newCenterX = data.width/3,data.width*2/3
	centerY = data.pageTitleMargin*3/2
	if data.currNewSize < newSize:
		canvas.create_oval(newCenterX-data.currNewSize,centerY-data.currNewSize,
			newCenterX+data.currNewSize,centerY+data.currNewSize,fill="red",width=0)
	elif data.currNewSize >= newSize:
		canvas.create_oval(newCenterX-newSize,centerY-newSize,newCenterX+newSize,
			centerY+newSize,fill="red",width=0)
		canvas.create_text(newCenterX,centerY,text="original\nfile\nsize",
			font="arial 12 ",fill="lavender blush",justify="center")
	if data.currOrigSize < origSize:
		canvas.create_oval(origCenterX-data.currOrigSize,centerY-data.currOrigSize,
			origCenterX+data.currOrigSize,centerY+data.currOrigSize,
			fill="medium spring green",width=0)
	elif data.currOrigSize >= origSize:
		canvas.create_oval(origCenterX-origSize,centerY-origSize,origCenterX+origSize,
			centerY+origSize,fill="medium spring green",width=0)
		canvas.create_text(origCenterX,centerY,text="compressed\nfile\nsize",
			font="arial 12 ",fill="deep pink",justify="center")
	if data.currOrigSize <= origSize or data.currNewSize <= newSize:
		data.timerDelay = 10
	else: data.timerDelay = 1000
	data.currNewSize += 0.5
	data.currOrigSize += 1

def drawHuffExplain(canvas,data):
	canvas.create_rectangle(0,0,data.width,data.height,fill="honeydew",
		outline="springgreen4",width=10)
	canvas.create_text(data.width/2,data.pageTitleMargin,anchor=S,
		text="What is Huffman Encoding?",fill="springgreen4",font="palatino 20 bold")
	if data.explanationPart < 4:
		canvas.create_text(data.width/2,data.pageTitleMargin+20,
			text="[Use Arrow Keys to Navigate]",font="palatino 10")
	if data.explanationPart == 1:
		with open("explanation part 1.txt","r") as file:
			partOne = file.read()
		canvas.create_text(data.width/2,data.height*3/4+90,anchor=S,text=partOne,
			justify="center",width=data.width-20,font="arial 13")
	elif data.explanationPart == 2:
		with open("explanation part 2.txt","r") as file:
			partTwo = file.read()
		canvas.create_text(data.width/2,data.height*3/4-30,anchor=S,text=partTwo,
			justify="center",width=data.width-20,font="arial 13")
	elif data.explanationPart == 3:
		with open("explanation part 3.txt","r") as file:
			partThree = file.read()
		canvas.create_text(data.width/2,data.height*3/4-50,text=partThree,
			justify="center",
			width=data.width-20,font="arial 13")
	elif data.explanationPart >=4:
		canvas.create_rectangle(data.width/2-60,data.height/2-20,data.width/2+60,
			data.height/2+20,fill="lemon chiffon",outline="springgreen4",width=3)
		canvas.create_text(data.width/2,data.height/2,text="Back to Menu",
			font="palatino 13",fill="springgreen4")

def drawFreqScreen(canvas,data):
	titleYNumer,titleYDenom = 6.5,16
	rectX,rectY,textX,textY = 6,7,10,11
	third,fourth=3,4
	freqList = masterList(data.usertyped) #get the letters that the user is typing w/their freqs
	#background and title
	canvas.create_rectangle(0,0,data.width,data.height,fill="lavender",
		outline="blue violet",width=10)
	canvas.create_text(data.width/2,data.pageTitleMargin*3/4, anchor=S,
		text="Character Frequencies",font="palatino 30",fill="blue violet")
	#"next" button that takes user to tree screen
	canvas.create_rectangle(data.width-20,20,data.width-80,50,
		fill="lemon chiffon",outline="gold",width=3)
	canvas.create_text(data.width-50,35,text="Next",font="arial 10",fill="grey11")
	#back button
	canvas.create_rectangle(20,data.height-20,80,data.height-50,fill="lemon chiffon",
		outline="gold",width=3)
	canvas.create_text(50,data.height-35,text="Back",font="arial 10",fill="grey11")
	if not data.typed or len(freqList)==0: #directions disappear once they are followed
		canvas.create_text(data.width/2,data.height/2,text="Start typing!",
			fill="grey50",font="arial 30")
	freqList = masterList(data.usertyped) #get the letters that the user is typing w/their freqs
	freqsHeight = data.height-data.pageTitleMargin*3/4-50
	boxSizeY = freqsHeight/rectY
	boxSizeX = (data.width-2*data.margin)/rectY
	maxCol = 7
	colCount = 0
	rowCount = 0
	for char in range(len(freqList)):
		if colCount >= maxCol:
			colCount = 0
			rowCount += 1
		x = colCount*boxSizeX + data.margin
		y = data.pageTitleMargin*3/4 + rowCount*boxSizeY
		canvas.create_rectangle(x,y,x+boxSizeX,y+boxSizeY,outline="blue violet",
			fill="floral white")
		canvas.create_line(x,y+boxSizeY/2,x+boxSizeX,y+boxSizeY/2,fill="blue violet")
		letter,frequency = freqList[char][0],freqList[char][1]
		if letter == " ": letter = "Space"
		elif letter == "\r": letter = "Return"
		elif letter == "\t": letter = "Tab"
		canvas.create_text(x+boxSizeX/2,y+boxSizeY/fourth,text=letter,fill="midnight blue")
		canvas.create_text(x+boxSizeX/2,y+boxSizeY*third/fourth,
			text=frequency,fill="dark violet")
		colCount += 1

def drawTreeScreen(canvas,data):
	#prior to animation
	canvas.create_rectangle(0,0,data.width,data.height,fill="lavender",
		outline="blue violet",width=10) 
	canvas.create_text(data.width/2,data.pageTitleMargin/2, anchor=S,
		text="Huffman Tree",font="palatino 30",fill="blue violet")
	#back button
	canvas.create_rectangle(20,data.height-20,80,data.height-50,
		fill="lemon chiffon",outline="gold",width=3)
	canvas.create_text(50,data.height-35,text="Back",font="arial 10",fill="grey11")
	if not data.startTree: #show directions to start animation
		canvas.create_text(data.width/2,data.height/2,
			text="Type in 'go' \nand press enter to see tree!",
			fill="grey50",font="arial 20")
		canvas.create_text(data.width*2/5,data.height*2/3,text="G",
			fill="grey80",font="courier 50")
		canvas.create_text(data.width*3/5,data.height*2/3,text="O",
			fill="grey80",font="courier 50")
		if data.typedG:
			canvas.create_text(data.width*2/5,data.height*2/3,text="G",
				fill="Spring Green",font="courier 50")
		if data.typedO:
			canvas.create_text(data.width*3/5,data.height*2/3,text="O",
				fill="Spring Green",font="courier 50")
	if data.startTree: 
		treeAnimation(canvas,data)
		canvas.create_rectangle(data.width-20,data.height-20,data.width-130,
			data.height-50,fill="lemon chiffon", outline="blue violet",width=3)
		canvas.create_text(data.width-75,data.height-35,fill="grey11",font="palatino 12",
			text="Back To Menu")

def treeAnimation(canvas,data):
	#draw leaves
	if len(data.leafInfo) == 0:
		canvas.create_text(data.width/2,data.height/2,
			text="No text was entered! Go back!",font="arial 20")
	for leaf in range(len(data.leafInfo)):
		leafX,leafY=data.leafInfo[leaf][0],data.leafInfo[leaf][1]
		leafName=data.leaves[leaf]
		canvas.create_oval(leafX,leafY,leafX+data.leafSize,leafY+data.leafSize,
			fill="lavender",outline="blue violet",width=2)
		canvas.create_text(leafX+data.leafSize/2,leafY+data.leafSize/2,text="%s"%leafName,
			font="courier 10",fill="midnight blue")
	if len(data.huffmanCode)==0:
		data.huffmanCode = getTree(data.usertyped)

def moveLeaves(data):
	moveVert = 30
	moveHoriz = 10
	for leaf in range(len(data.leafInfo)):
		leafName = data.leaves[leaf]
		leafCode = str(data.huffmanCode[leafName])
		if len(leafCode) != 0:
			first = leafCode[0]
			data.leafInfo[leaf][1] += moveVert
			if first == '0':
				data.leafInfo[leaf][0] -= moveHoriz
			elif first == '1':
				data.leafInfo[leaf][0] += moveHoriz
		data.huffmanCode[leafName] = leafCode[1:]

def redrawAll(canvas, data):
	if data.startScreen:
		drawStartScreen(canvas,data)
	elif data.getFileScreen:
		drawGetFileScreen(canvas,data)
	elif data.getCodeScreen:
		drawGetCodeScreen(canvas,data)
	elif data.saveOptionScreen:
		drawSaveOptionScreen(canvas,data)
	elif data.finishedEncoding:
		drawFinishedEncodingScreen(canvas,data)
	elif data.whatHuffmanScreen:
		drawHuffExplain(canvas,data)
	elif data.freqScreen:
		drawFreqScreen(canvas,data)
	elif data.treeScreen:
		drawTreeScreen(canvas,data)


####################################
# run function
####################################

def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas,data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 #milliseconds
	root = Tk()
	init(data)
	# create the root and the canvas
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas,data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(400, 500)