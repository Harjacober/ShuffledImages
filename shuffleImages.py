import cv2
import random
from os import listdir
from os.path import join

#each image provided is divided into various fragments. This class use an an array
#of fragments to hold each pixels fragment in the image
class ImageClass:
    def __init__(self, fragments, name):
        self.fragments = fragments
        self.name = name

#this class is used to hold the properties of each fragments. we can later allow it
#to capture other properties of the fragments like the RGB values sha 
class fragment:
    def __init__(self,oldindex,newindex,start_row,end_row,start_col,end_col):
        self.oldindex = oldindex
        self.newindex = newindex
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col

#@function to get all the fragments and its properties from each image
def getFragments(path): 
    p = 64
    m = 512//p
    index = 0
    arr = []
    for i in range(m):
        start_row, end_row = p*i, p*(i+1)
        for j in range(m):
            start_col, end_col = p*j, p*(j+1)
            arr.append(fragment(index,index,start_row,end_row,start_col,end_col))
            index += 1 
    return arr        
#this is the main function that does the shuffling.
#for now, I'm just shuffling it randomlys
def shuffle(fragments): 
    arr = [i for i in range(len(fragments))]
    random.shuffle(arr) 
    for i in range(len(fragments)):
        frag = fragments[i]
        frag.newindex = arr[i]
        arr.append(frag)
    return fragments 

if __name__ == '__main__':
    ImageClasses = [] #stores all instance of each Image
    mypath = "C:/Users/Harjacober/Desktop/HuaweiHornoCup/data_train/64"
    #list all the image files in tne data folder
    for file in listdir(mypath): 
        img_file = join(mypath, file)  
        fragments = getFragments(img_file) #get all fragments of this image file 
        ImageClasses.append(ImageClass(fragments, file))   
    f = open("data_train_64_answer.txt", "w")
    for each in ImageClasses: #loop through each image one by one
        ans = [i.newindex for i in shuffle(each.fragments)]  #shuffle the fragments
        output = ' '.join(list(map(str,ans))) 
        f.write(each.name+"\n"+output+"\n") 
    f.close()
    print("Done")
