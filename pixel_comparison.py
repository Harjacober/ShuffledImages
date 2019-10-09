import cv2
from os import listdir
from os.path import join
from skimage.measure import compare_ssim
from skimage.transform import resize
from scipy.stats import wasserstein_distance
from scipy.misc import imsave
from scipy.ndimage import imread
import numpy as np 

height = 512 #this can be adjustEd
width = 512   #and this. they are called in the shuffled image class inside the @pixel_simh fuction 
def get_img(path, norm_size=True, norm_exposure=False):
  '''   Prepare an image for image processing tasks
  '''
  # flatten returns a 2d grayscale array if True
  img = imread(path, flatten=False).astype(int) 
  return img
  
#not in use. already redefined in the shuffledImageClass
def pixel_sim(path_a, path_b): 
  img_a = get_img(path_a, norm_exposure=True)[0:64,0:1] 
  img_b = get_img(path_b, norm_exposure=True)[0:64,2:3]  
  return np.sum(np.absolute(img_a - img_b)) / (height*width) / 255

#another similarity algorithm, it doesn't give good result like the pixel_sim am using
def difference(imga, imgb):
  # convert the images to grayscale
  grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
  grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
  (score, diff) = compare_ssim(grayA, grayB, full=True)
  return score

"""
mypath = "C:/Users/Harjacober/Desktop/HuaweiHornoCup/my_test_data/64"
mypath2 = "C:/Users/Harjacober/Desktop/HuaweiHornoCup/my_test_data/64"
img_file = []
for file in listdir(mypath): 
    img_file.append(join(mypath, file) )    
print(pixel_sim(img_file[0], img_file[1]))
imageA = cv2.imread(img_file[0])[0:64,56:64] 
imageB = cv2.imread(img_file[0])[0:64,56:64]
print(compare_ssim(imageA, imageB, multichannel=True)) 
print(difference(imageA, imageB))"""
