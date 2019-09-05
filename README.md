# DataClassifier
Quick and dirty script to enable manual classification of images. Requires PyQt5

# Requirements
This code requires PyQt5 to work, which should be part of ANACONDA

# How to use it

1. Define classes in predefinedClasses.txt. They ust be comma separated
2. start the program giving the path to the predefined classes, a path to images and an output filename. Output will be CSV
3. The program will load the first image in the folder and display it. Classes are selected using the buttons down the left side. To proceed to the next image, click next; this will write the image name and class to the csv and store it internally. You can go back, but it might screw up your CSV file.
4. When finished, click finished. The program will close and re-write the CSV file from a stored dictionary.


# Notes
This is a very rough and ready program and may do strange things or crash. It is also quite likely to get upset if the window is resized (it shouldn't, but it does)
If you find problems, please make an issue with details so I can try to fix it, or fix it yourself and submit a pull request.
