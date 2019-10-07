import cv2
from os import listdir
from os.path import join
from skimage.measure import compare_ssim
from skimage.transform import resize
from scipy.stats import wasserstein_distance
from scipy.misc import imsave
from scipy.ndimage import imread
import numpy as np 

height = 2**10
width = 2**10
def get_img(path, norm_size=True, norm_exposure=False):
  '''
  Prepare an image for image processing tasks
  '''
  # flatten returns a 2d grayscale array
  img = imread(path, flatten=True).astype(int)
  # resizing returns float vals 0:255; convert to ints for downstream tasks
  if norm_size:
    img = resize(img, (height, width), anti_aliasing=True, preserve_range=True)
  if norm_exposure:
    img = normalize_exposure(img)
  return img

def get_histogram(img): 
  h, w = img.shape
  hist = [0.0] * 256
  for i in range(h):
    for j in range(w):
      hist[img[i, j]] += 1
  return np.array(hist) / (h * w) 


def normalize_exposure(img):
  '''
  Normalize the exposure of an image.
  '''
  img = img.astype(int)
  hist = get_histogram(img)
  # get the sum of vals accumulated by each position in hist
  cdf = np.array([sum(hist[:i+1]) for i in range(len(hist))])
  # determine the normalization values for each unit of the cdf
  sk = np.uint8(255 * cdf)
  # normalize each position in the output image
  height, width = img.shape
  normalized = np.zeros_like(img)
  for i in range(0, height):
    for j in range(0, width):
      normalized[i, j] = sk[img[i, j]]
  return normalized.astype(int)
def pixel_sim(path_a, path_b): 
  img_a = get_img(path_a, norm_exposure=True)
  img_b = get_img(path_b, norm_exposure=True)
  return np.sum(np.absolute(img_a - img_b)) / (height*width) / 255

"""
mypath = "C:/Users/Harjacober/Desktop/HuaweiHornoCup/my_test_data/64"
mypath2 = "C:/Users/Harjacober/Desktop/HuaweiHornoCup/my_test_data/64"
img_file = []
for file in listdir(mypath): 
    img_file.append(join(mypath, file) )  
    #image = cv2.imread(img_file)
    #cv2.imshow("",image[0:64,0:64] )
    #
print(sift_sim(img_file[0], img_file[1]))    
print(pixel_sim(img_file[0], img_file[1]))
"""
