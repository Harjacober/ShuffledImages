import cv2
import random
from os import listdir
from os.path import join
from collections import deque
import pixel_comparison as pc
import numpy as np

#each image provided is divided into various fragments. This class use an an array
#of fragments to hold each pixels fragment in the image
class ImageClass:
    def __init__(self, fragments, name):
        self.fragments = fragments
        self.name = name

#this class is used to hold the properties of each fragments. we can later allow it
#to capture other properties of the fragments like the RGB values sha 
class fragment:
    def __init__(self,index,edges):
        self.index = index 
        self.edges = edges 
        
class Pixel:
    def __init__(self, right, left, top, bottom):
        self.right = right #Edge (treated as a normal image)
        self.left = left #Edge (treated as a normal image)
        self.top = top #Edge (treated as a normal image)
        self.bottom = bottom #Edge(treated as a normal image) 
        

#@function to get all the fragments and its properties from each image
def getFragments(path):
    #image = cv2.imread(path)
    image = pc.get_img(path) #read image
    p = 64 #size of pixel of each frsgment. change to 32 or 16 for other datasets
    m = 512//p
    index = 0
    arr = set() #to enable fast remove operations
    #cv2.imshow("",image)
    for i in range(m):
        start_row, end_row = p*i, p*(i+1)
        start_row_top, end_row_top = p*i, p*i+1
        start_row_bottom, end_row_bottom = p*(i+1)-1, p*(i+1)
        for j in range(m):
            start_col, end_col = p*j, p*(j+1)
            start_col_left, end_col_left = p*j, p*j+1
            start_col_right, end_col_right = p*(j+1)-1, p*(j+1)
            left = image[start_row:end_row,start_col_left:end_col_left] #left edge
            right = image[start_row:end_row,start_col_right:end_col_right] #right edge
            top = image[start_row_top:end_row_top, start_col:end_col] #top edge
            bottom = image[start_row_bottom:end_row_bottom,start_col:end_col] #bottom edge
            edges = Pixel(right, left, top, bottom)
            arr.add(fragment(index, edges))
            index += 1 
    return arr


#generator function to arrange the imaages and generate the correct index position 
def shuffle(fragments):
    row_holder = compareedges(fragments)
    for each in row_holder:
        for i in each:
            yield i.index
            
def compareedges(fragments): 
    p = 512//64  #denominator is the size of pixel of each frsgment. change to 32 or 16 for other datasets
    row_holder = deque()
    #compare left and right edges
    for i in range(int(p)):
        start = fragments.pop() 
        each_row = deque([start]) 
        for i in range(int(p)-1):
            right = each_row[-1].edges.right
            left = each_row[0].edges.left
            best= (float('inf'),None,"") 
            for each in fragments:
                rsim = pixel_sim(right, each.edges.left)
                lsim = pixel_sim(left, each.edges.right)
                best = min(best,(rsim, each,"aright"),(lsim, each,"aleft"),key=lambda x:x[0])
            each_row.append(best[1]) if best[2] == "aright" else each_row.appendleft(best[1])
            fragments.remove(best[1])
        row_holder.append(each_row)
    #compare top and bottom edges
    start = row_holder.pop() 
    ans = deque([start])
    for i in range(int(p)-1): 
        top = ans[0][0].edges.top
        bottom = ans[0][-1].edges.bottom
        bestHere= (float('inf'),None,"") 
        for ro in row_holder: 
            for each in ro:
                tsim = pixel_sim(top, each.edges.bottom)
                bsim = pixel_sim(bottom, each.edges.top)
                bestHere = min(bestHere,(tsim, ro,"atop"),(bsim, ro,"abottom"),key=lambda x:x[0])
                
        ans.append(bestHere[1]) if bestHere[2] == "atop" else ans.appendleft(bestHere[1]) 
        row_holder.remove(bestHere[1]) 
        
    return ans         
    
def sift_sim(img_a, img_b): 
  # initialize the sift feature detector
  orb = cv2.ORB_create() 
 
  # find the keypoints and descriptors with SIFT
  kp_a, desc_a = orb.detectAndCompute(img_a, None)
  kp_b, desc_b = orb.detectAndCompute(img_b, None)

  # initialize the bruteforce matcher
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

  # match.distance is a float between {0:100} - lower means more similar
  matches = bf.match(desc_a, desc_b)
  similar_regions = [i for i in matches if i.distance < 70]
  if len(matches) == 0:
    return 0
  return len(similar_regions) / len(matches)

def pixel_sim(img_a, img_b):  
  return np.sum(np.absolute(img_a - img_b)) / (pc.height*pc.width) / 255 



if __name__ == '__main__':
    ImageClasses = [] #stores all instance of each Image
    mypath = "C:/Users/Harjacober/Desktop/data/data_test1_blank/64"
    #list all the image files in tne data folder
    for file in listdir(mypath): 
        img_file = join(mypath, file)  
        fragments = getFragments(img_file) #get all fragments of this image file 
        ImageClasses.append(ImageClass(fragments, file))   
    f = open("my_test_answer3.txt", "w")
    i=1
    for each in ImageClasses: #loop through each image one by one
        print(i)
        i+=1
        ans = shuffle(each.fragments)  #shuffle the fragments
        output = ' '.join(list(map(str,ans))) 
        f.write(each.name+"\n"+output+"\n") 
    f.close()
    print("Done")
