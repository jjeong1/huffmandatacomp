# algorithm code
import math

def masterList(s): #obtains frequencies 
	#-> one list of letters and their frequencies in tuples
	master = []
	considered = []
	for char in s:
		if char not in considered:
			master.append((char,1))
			considered += char
		else: #if the character was already considered
			freqs = considered.count(char)
			master.remove((char,freqs))
			master.append((char,freqs+1))
			considered += char
	return master

def createTree(lst): #nests the tuples based on increasing freq
	if len(lst) == 0: return ("",0) #default "no input" value
	first = ("",math.inf) #set infinitely big default values
	second = ("",math.inf)
	if len(lst)==1: return lst[0] #if finished, return tree and max freq
	freqs = [] 
	for leaf in lst: freqs.append(leaf[1]) 
	#get a list of the possible frequencies, in order
	firstMin = min(freqs)
	firstIndex = freqs.index(firstMin)
	first = lst[firstIndex]
	lst.remove(first) 
	freqs.remove(firstMin) #remove char with lowest freq
	secondMin = min(freqs)
	secondIndex = freqs.index(secondMin)
	second = lst[secondIndex]
	lst.remove(second) 
	freqs.remove(secondMin) 
	#remove char with second lowest freq
	node = (first[0],second[0]) 
	#create a node enlisting chars and calculate joint freq
	nodeValue = first[1]+second[1]
	lst.append((node,nodeValue))
	return createTree(lst)

print(createTree(masterList("hello my name is jane")))

def assignValues(tup): #wrapper function for creating code dictionary
	#we can ignore the maximum frequency number for this f(x)
	#now take the tree and begin accessing from the outsidemost values
	return assignWrapper(tup[0],assigned = dict(),coded ='')

def assignWrapper(tree,assigned,coded): 
	#generates code according to its nested level
	if isinstance(tree,str): #if you are at a leaf
		assigned[tree] = coded
		return assigned
	else: #if you are at a node
		leftTree,rightTree = tree[0],tree[1]
		assignWrapper(leftTree,assigned,coded=coded[:]+"0")
		assignWrapper(rightTree,assigned,coded=coded[:]+"1")
		return assigned

def getTree(s):
	return assignValues(createTree(masterList(s)))

def exportCode(fileName,desiredName): #makes a file containing the huffman code
	with open("%s.txt"%fileName,"r") as file:
		redFile = file.read()
	toCode = ""
	for entry in redFile:
		toCode=toCode[:]+entry
	gotCode = getTree(toCode)
	filedCode = open("%s"%desiredName,"w+")
	filedCode.write("%s"%gotCode)
	filedCode.close()

def exportCompressed(fileName,desiredName): 
	#makes new text file of ascii using compression code; uses bits
	with open("%s.txt"%fileName,"r") as file:
		redFile = file.read()
	toCode = ""
	for entry in redFile:
		toCode=toCode[:]+entry
	gotCode = getTree(toCode)
	toCompr = "" #a longg string of binary
	for char in toCode:
		charCode = gotCode[char]
		toCompr = toCompr[:]+charCode
	comprCode = bytes(toCompr,"ascii")
	filedCode = open("%s"%desiredName,"wb")
	filedCode.write(comprCode)
	filedCode.close()

def getSize(fileName):
	#gets the size information of the original file and compressed file
	with open("%s.txt"%fileName,"r") as file:
		redFile = file.read()
	toCode = ""
	for entry in redFile:
		toCode=toCode[:]+entry
	gotCode = getTree(toCode)
	comprData = ""
	for char in toCode:
		charCode = gotCode[char]
		comprData = comprData[:]+charCode
	comprFileSize = len(comprData)
	origFileSize = len(toCode)*8
	return (comprFileSize,origFileSize)


print(-9%7)


