import glob
import os
from clicpic import Clicpic
import sys
import getopt


def renameJPGs():
    # Command line arguments... ignore this
    inputFile = Clicpic.camera_path + 'headings.txt'
    imageCounter = 0
    
    fileExtension = 'JPG'

    # Where the actual work is done
    newFileNames = openAndStore(inputFile)
    files = sorted(glob.glob(Clicpic.camera_path + '*.' + fileExtension))
    
    if not files or len(files) != len(newFileNames):
        print("Different sizes!")
        sys.exit(2)
    
    for index in range(0, len(newFileNames)):
        os.rename(files[index], Clicpic.unprocessed_path + newFileNames[index] + '.' + str(imageCounter) + ('.' + fileExtension))
        imageCounter += 1

# input: input text file name
# output: list of new file names
def openAndStore(inputFile):
    listNames = []
    with open(inputFile) as file:
        listNames = file.readline().split()
        
    file.close()
    return listNames

myClicpic = Clicpic()

# Point to directory of Images
# Must have or create a directory for processed images 
# and for unprocessed images
os.chdir(Clicpic.unprocessed_path)

answer = "NO"

renameJPGs()

imageFilenameList = glob.glob("*")

if len(imageFilenameList) > 0:
    for filename in imageFilenameList:
        print("\n", Clicpic.unprocessed_path + filename)
        myClicpic.clic2picXY(filename)
      

            
