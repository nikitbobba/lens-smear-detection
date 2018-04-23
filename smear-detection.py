
import cv2
import numpy as np
import os




#Change path according to where your data is
path = 'sample_drive'

def start_detection(dir_path):
    '''
    Identifies subdirectories from input folder and performs smear detection
    on the images in each subdirectory. Creates mean, intermediate and final images
	for each directory
	Input: path for data set
	'''
    print ('Starting...')
    directories = os.listdir(dir_path)
    dir_list = []
    for d in directories:
        if os.path.isdir(dir_path + '/' + d):
            dir_list.append(d)
    
    for directory in dir_list:
        temp_path = path + '/' + directory
        data_set = process_image(temp_path)
        final_data_set = split_data(data_set)

        print ('Creating Mean Image for', directory)
        mean_img = create_mean_image(final_data_set)
        cv2.imwrite(directory + '_mean_image.jpg',mean_img)
        
        print ('Creating Intermediate Mask for', directory)
        prelim_mask = create_prelim_mask(mean_img)
        cv2.imwrite(directory + '_intermediate_mask.jpg',prelim_mask)
        
        print ('Creating Mask for', directory)
        final_image = create_binary_mask(prelim_mask)
        cv2.imwrite(directory + '_final_mask.jpg',final_image)
        

def process_image(dir_path):
    '''
	Pre-processes every image by converting to grayscale, applying histogram equalization,
	blurring and binary threshold. Returns list of processed images
	Input: directory path for images
	'''
    images = []
    for image in os.listdir(dir_path):
        img = cv2.imread(os.path.join(dir_path,image))
        if img is not None:
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eq_img = cv2.equalizeHist(gray_image)
            blur_img = cv2.blur(eq_img, (3,3))
            ret,thresh_img = cv2.threshold(blur_img,127,255,cv2.THRESH_BINARY)
            images.append(thresh_img)
    return images
        

def split_data(image_set):
    '''
	Splits set of images into subsets of approximately 200 images for batch processing
	Input: list of images
	'''
    total = []
    count = 0
    number_of_splits = len(image_set)/200
    for i in range(number_of_splits):
        maxcount = count + 200
        if maxcount < len(image_set)-1:
            temp_arr = image_set[count:maxcount]
        else:
            temp_arr = image_set[count:]
        total.append(temp_arr)
        count += 200
    return total


def calc_mean_image(arr, length):
    '''
	Returns an averaged image of the given list of images
	Input: list of images
	'''
    i = 1
    sum_image = arr[0] * 1/length
    while (i < len(arr)):
        sum_image = cv2.add(sum_image,arr[i]* 1/length)
        i += 1
    return sum_image


def create_mean_image(total_data):
    '''
	Batch processes the average of each image subset and returns one averaged image
	Input: List of lists of images
	'''
    avg_images = []
    for data in total_data:
        temp_img = calc_mean_image(data,len(data))
        avg_images.append(temp_img)
    
    return calc_mean_image(avg_images,len(avg_images))
    

def create_prelim_mask(img):
    '''
	Applies an adaptive threshold on the input and performs a bitwise not operation
	Input: image
	'''
    adapt = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,105,10)
    return cv2.bitwise_not(adapt)
    

def create_binary_mask(img):
    '''
	Applies erosion and dilation to reduce noise and returns a final binary mask
	Input: image
	'''
    kernel = np.ones((10,10),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 5)
    dilation = cv2.dilate(erosion,kernel,iterations = 5)
    return dilation

start_detection(path)

