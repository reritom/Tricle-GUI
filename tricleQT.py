'''Tested on: Python 3.5.2 |Anaconda 4.2.0 (64-bit)|'''

from __future__ import division
import os, time, random, sys

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

qtCreatorFile = "NewUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):		
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.setStyleSheet("background-color:#eef1ef;")
		
		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		
		self.Outer.setObjectName("OuterFrame");
		self.Outer.setStyleSheet('#OuterFrame {border:none;}')
		
		self.Left.setStyleSheet("background-color:#283039;")
		self.Mid.setStyleSheet("background-color:#bdd5ea;")
		self.Right.setStyleSheet("background-color:#f7f7ff;")
		
		self.radioButtonS.setStyleSheet("background-color: #687580; color: white;")
		self.radioButtonU.setStyleSheet("background-color: #687580; color: white;")
		self.radioButtonFile.setStyleSheet("background-color: #687580; color: white;")
		self.radioButtonFolder.setStyleSheet("background-color: #687580; color: white;")
		self.radioButtonFolders.setStyleSheet("background-color: #687580; color: white;")
		
		self.Heading.setStyleSheet("background-color:#687580; color: white;")
		
		self.FileButton.setStyleSheet("background-color: #687580; color: white;")
		self.StartButton.setStyleSheet("background-color: #66ccff; color: white;")
		self.CloseButton.setStyleSheet("background-color: #687580; color: white;")
		
		self.HFrame.setObjectName("MidFrame")
		self.Mid.setObjectName("MidFrame")
		self.Mid.setStyleSheet('''	#MidFrame {color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255)); 
									background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 black, stop:0.02 #687580 stop:1 #687580);}''')
		self.Right.setObjectName("RightFrame")
		self.BGshape.setObjectName("RightFrame")
		self.fList.setObjectName("RightFrame")
		self.pList.setObjectName("RightFrame")
		
		self.Right.setStyleSheet('''#RightFrame {color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255)); 
									background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 black, stop:0.01 #f7f7ff stop:1 #f7f7ff);}''')							
		self.BGshape.setStyleSheet("color: #e6e6e6;")
		
		self.fList.setStyleSheet("color: #e6e6e6;")
		self.pList.setStyleSheet("color: #e6e6e6;")
		
		self.StartButton.clicked.connect(self.run)
		self.FileButton.clicked.connect(self.Browse)
		self.CloseButton.clicked.connect(app.exit)
		
		self.keys = list()
		self.seeds = list()
		self.errorStat = ""
		self.mode = ""			#scramble (1) or unscramble (-1)
		self.ver = ""			#file(-1) or folder (1)
		self.adr = ""			#location of file or folder
		self.address = ""		#location of file
		self.saveDir = ""
		self.imName = ""
		
		self.totalBytes = 0
		self.sumBytes = 0
		self.totalImages = 0
		self.curImage = 0
		
		self.gridSize = 5
		self.xNum = ""
		self.yNum = ""
		
		self.orig = ""
		self.proc = ""
		self.ret = ""
		self.final = ""
		
		self.colx = ""
		self.rowy = ""
		
		self.encodeArray = ["","",""]
		
	def verSelect(self):		
		'''Determines which checkbox is ticked, and stores the result in self.ver'''
		
		if self.radioButtonFile.isChecked():
			self.ver = 1				#File Version
		elif self.radioButtonFolder.isChecked():
			self.ver = -1				#Folder Version
		else:
			self.ver = -2				#Folders Version
			
	def Browse(self):
		'''Depending in the value of self.ver, either a file or folder is selected using a dialog box,
		with the address stored in self.adr'''
	
		self.verSelect()
		self.BGshape.setText("</>")
		
		if self.ver == 1:
			self.adr = QtWidgets.QFileDialog.getOpenFileName(self,"Pick a file")[0]		
		else:
			self.adr = QtWidgets.QFileDialog.getExistingDirectory(self,"Pick a folder")
		
	def appOut(self):
		'''When called, this function displays whatever string is stored in self.errorStat, and displays it in the GUI'''
		
		self.textOut.setText(self.errorStat)
    
	def run(self):
		self.BGshape.setText("</>")
	
		self.modeSelect()
		self.readKeys()
		
		self.totalBytes = 0
		self.sumBytes = 0
		self.totalImages = 0
		self.curImage = 0

		if self.ver == 1:
			self.BGshape.setText("0/1")
			self.address = self.adr
			
			try:
				self.loadImage()
			except:
				self.textOut.setText("No Image Selected")
				return
				
			self.textOut.setText("This could take a while")
			self.progressBar.setValue(5)	
				
			self.encode()
			
			if self.mode == 1:
				self.scramble()
				
			elif self.mode == -1:
				self.unscramble()
			
			self.imName = self.adr.replace(os.path.split(self.adr)[0], "") 	#extracts filename from the address
			self.imName = self.imName[1:]									#removes the '/' from the beginning of the string
			self.adr = self.adr.replace(self.imName, "")					#removes the file name from the address
			self.adr = self.adr[:len(self.adr)]								#removes the remaining '/' from the address

			if self.mode == 1:
				self.imName = os.path.splitext(self.imName)[0] + ".bmp"
			else:
				self.imName = os.path.splitext(self.imName)[0] + ".jpeg"
			self.outputDir()
			
			self.final.save(os.path.join(self.saveDir, self.imName), format="BMP", subsampling=0, quality=100)
			self.progressBar.setValue(100)
			self.textOut.setText("Completed")
			self.final.close()
			self.BGshape.setText("1/1")
			
		elif self.ver == -1:
		
			self.fileCount()
			self.progressBar.setValue(5)
			self.BGshape.setText("0/" + str(self.totalImages))
					
			if len(os.listdir(self.adr)) > 0:
				self.outputDir()
				i = 1
				for image in os.listdir(self.adr):
					
					QtCore.QCoreApplication.processEvents()
					
					if image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
						self.address = os.path.join(self.adr, image)
						
						self.loadImage()
						self.encode()
						
						self.BGshape.setText(str(i) + "/" + str(self.totalImages))
						
						self.curImage = self.curImage + 1
						self.sumBytes = self.sumBytes + os.path.getsize(os.path.join(self.adr, image))
			
						if self.mode == 1:
							self.scramble()
							self.imName = os.path.splitext(image)[0] + ".bmp"
							self.final.save(os.path.join(self.saveDir, self.imName), format="BMP", subsampling=0, quality=100)
							
						elif self.mode == -1:
							self.unscramble()
							self.imName = os.path.splitext(image)[0] + ".jpeg"
							self.final.save(os.path.join(self.saveDir, self.imName), format="JPEG", subsampling=0, quality=100)
							
						self.final.close()
						
						self.progressBar.setValue((self.sumBytes/self.totalBytes) * 100)
						
						i = i + 1
						
				self.textOut.setText("Completed")
						
		else:
			self.textOut.setText("Incomplete Module")
			
	def modeSelect(self):
		'''Checks which mode is selected in the GUI and stores it in self.mode'''
		
		if self.radioButtonS.isChecked():
			self.mode = 1				#SCRAMBLE MODE
		elif self.radioButtonU.isChecked():
			self.mode = -1				#UNSCRAMBLE MODE
			
	def readKeys(self):
		'''Clears info from any previous seeds and keys. Then reads the new keys from the GUI'''
		
		self.keys = list()
		self.seeds = list()
		self.keys.append(self.KeyOne.toPlainText())
		self.keys.append(self.KeyTwo.toPlainText())
		self.keys.append(self.KeyThree.toPlainText())
		
		for i in range(3):
			if len(self.keys[i]) < 1:
				self.errorStat = "KeyError"
				self.appOut()
			else:
				self.seedGen()
		
	def seedGen(self):
		'''Takes the three keys and creates three seed values which are stored in the list self.seeds'''
		
		onekey = self.keys[len(self.seeds)]
		uniKey = list()
		uniVal = len(onekey)
		count = 0
		for i in range(len(onekey)):
			uniKey.append(ord(onekey[i]))
			
			if count%2 == 0:
				uniVal = uniVal * uniKey[i]
			else:
				uniVal = uniVal / uniKey[i]
		
		seed = str((uniKey[0] + uniKey[len(uniKey) - 1]))
		seed = seed + str(uniVal) + str(len(onekey))
		
		self.seeds.append(seed)
		
	def loadImage(self):
		'''Loads the image from self.address using PIL, then converts it to a numpy array, which is copied and 
		has the x and y dimensions stored'''
		
		original = Image.open(self.address)

		self.orig = np.array(original)
		self.proc = np.copy(self.orig)
		self.ret = np.copy(self.orig)
		
		original.close()
		
		self.colx = self.orig.shape[0]
		self.rowy = self.orig.shape[1]
		
	def scramble(self):
		'''Uses the keys to scramble the image using two index manipulation methods'''
		
		for x in range(self.colx):
			for y in range(self.rowy):
				self.proc[x][y] = self.orig[self.encodeArray[0][x]][self.encodeArray[1][y]]
				
		proc2 = np.copy(self.proc)
		
		ind = 0
		for x in range(self.xNum):
			for y in range(self.yNum):
				blue = self.encodeArray[2][ind]
				xEn = blue%self.xNum
				yEn = int((blue - xEn)/self.xNum)
				
				proc2[x*self.gridSize:x*self.gridSize+self.gridSize,y*self.gridSize:y*self.gridSize+self.gridSize,:] = self.proc[xEn*self.gridSize:xEn*self.gridSize+self.gridSize,yEn*self.gridSize:yEn*self.gridSize+self.gridSize,:]
				
				ind = ind + 1
		
		self.final = Image.fromarray(proc2)
		
	def unscramble(self):	
		'''Uses the keys to unscramble the image'''
		
		ind = 0
		for x in range(self.xNum):
			for y in range(self.yNum):
				blue = self.encodeArray[2][ind]
				xEn = blue%self.xNum
				yEn = int((blue - xEn)/self.xNum)
				
				self.ret[xEn*self.gridSize:xEn*self.gridSize+self.gridSize,yEn*self.gridSize:yEn*self.gridSize+self.gridSize,:] = self.proc[x*self.gridSize:x*self.gridSize+self.gridSize,y*self.gridSize:y*self.gridSize+self.gridSize,:]

				ind = ind + 1
		
		ret2 = np.copy(self.ret)

		for x in range(self.colx):
			for y in range(self.rowy):
				ret2[self.encodeArray[0][x]][self.encodeArray[1][y]] = self.ret[x][y]
				
		self.final = Image.fromarray(ret2)
		
	def outputDir(self):
		'''Creates an output directory within the image location directory'''
		
		if self.mode == 1:
			ext = "TricleS"
		elif self.mode == -1:
			ext = "TricleU"
	
		os.makedirs(os.path.join(self.adr, ext))
		self.saveDir = os.path.join(self.adr, ext)
		
	def encode(self):
		'''Creates arrays for the scrambling methods, the arrays are shuffled randomly using the seeds'''
		
		self.encodeArray[0] = list(range(0,self.colx))
		self.encodeArray[1] = list(range(0,self.rowy))
		
		self.xNum = int((self.colx - self.colx%self.gridSize)/self.gridSize)
		self.yNum = int((self.rowy - self.rowy%self.gridSize)/self.gridSize)
		
		self.encodeArray[2] = list(range(0,self.xNum*self.yNum))

		random.Random(self.seeds[0]).shuffle(self.encodeArray[0])
		random.Random(self.seeds[1]).shuffle(self.encodeArray[1])
		random.Random(self.seeds[2]).shuffle(self.encodeArray[2])	
		
	def fileCount(self):
		'''Counts how many images are going to be converted and determines the total size'''
		
		if len(os.listdir(self.adr)) > 0:
			self.totalImages = len(os.listdir(self.adr))
			for image in os.listdir(self.adr):
				if image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
					self.totalBytes = self.totalBytes + os.path.getsize(os.path.join(self.adr, image))
	
					
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())