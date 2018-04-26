# Lens Smear Detection

An application that will detect any smear on camera lens given a set of images taken by the camera.

### Setup
In order to run this project, you must have `Python 2.7` installed. Additionally, you will need to have Open CV and Numpy installed as well. 

We recommend creating a `conda` environment and installing these two required packages.

###Running the project
In order to run our project, a directory must be specified that locates the image sets. Open smear-detection.py. At the top of the script, there is a variable called `path`. Enter the path to your directory here. The directory should specify the folder that contains all the subfolders with the images from each camera.

Example:

sample_drive contains 4 folders. Ensure that the `path` variable contains the path to the sample drive directory. The function 'start-detection' will then be able to automatically identify all the sub-directories in the path (i.e. cam_0, cam_1 etc) and create final images for each sub-directory.

_sample_drive
___cam_0
___cam_1
___cam_2
___cam_3
___cam_5


Once 'path' has been updated in smear-detection.py, you can run the script by calling the following command:

python smear-detection.py

### Final Results:
After running smear-detection.py, you will receive 3 results for each camera:

1.cam_number_mean_image.jpg
2.cam_number_intermediate_mask.jpg
3.cam_number_final_mask.jpg

where cam_number is the name of the sub-directory
