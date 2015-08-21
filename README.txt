Name: Zach Krasner
PennKey: zkrasner
Date: May 4, 2015

CIS 192 Final Project

——— Instructions for use ——
Put your desired image file into the ‘imgs’ directory within the final_project folder and ensure that the ‘bottle caps’ folder is populated with images of the bottle caps you want to use for this image. Bottle cap images can easily be found on http://www.bottlecaps.de/index/.
%> cd final_project
%> python3 BottleCapIt.py -t “image_file”

To begin the program, run the above lines in terminal where “image_file” is the name of the image in the “imgs” directory that you wish to turn into a bottle capped image. 

Assuming that the image file you provided was valid. A tinter GUI should appear. On the left hand side of the GUI there is a column of sliders and buttons for user input. To the right is the image that you selected for this process. 

Begin by moving the height and width sliders to reflect the number of bottle caps that you want in each dimension of the output image. The height-to-width ratio of the input image is displayed below the sliders as a guide for the user. To avoid distorting the image, the user should aim to have a bottle cap height and width that roughly matches the input ratio. The cap ratio is displayed below the input ratio to make this selection process easy. Below that cap ratio is a label letting the user know just how many caps are necessary to make this output image given the position of the sliders. 

When the user is happy with his or her height and width selection, they can press the grid button to preview how the input image will be divided. When the button is hit, a grid of black lines should appear over the input image. Each section of the grid is a section that will be represented by a bottle cap once the process is continued. 

If the user is happy with the grid (or if they chose not to see the grid and jumped right to this step), they can hit the ‘Cap It!’ button. This begins the process of Cappifying the input image. The program looks at each grid section and assigns it the cap that most closely matches the average color of the section. Once each section has been assigned a cap, the program stitches together all of the caps and updates the GUI image to the Cappified version of the input image. 

If the user is unhappy with the output, they can change the height and width sliders to slightly alter the output image. 

—— Requirements Met —— 
  Custom class:
	BottleCap.py

  Three Modules:
    1 -> tkinter
    2 -> scipy
    3 -> numpy
    4 -> functools
    5 -> PIL
    6 -> os

   Custom Decorator or Generator function:
	_findCapDecorator in BottleCapIt.py

—— Python Files ——

BottleCapIt.py

This is the main class. It creates the tkinter GUI and responds to user input to generate the bottle cap image from the input user image file.

BottleCap.py

This is the custom class that represents a physical bottle cap. It takes in the bottle cap image file and produces information about the average color of the cap for use in the Cappifying process.

—— Interesting Parts ——-
In BottleCap.py, finding the average colors of an image was interesting as different averages were desired for different parts of the program. Since the bottle caps are round, the corners of their square images should not be included in the color averaging process. To try to ensure this, I examine the distance of each pixel from the center of the image and only count those within a certain radius. This greatly reduces the number of non-cap pixels being added to the average color and thus give a better representation of the cap. The section of the gridded image however want all of the pixels for a better representation, so that is a more straightforward average. 

Also in this file there is a getDistance function. This takes in the rgb values of another image and finds that color’s distance in a three dimensional space with red, green and blue as axes. 

The BottleCapIt.py file has many interesting parts. Since the input image should not be altered in any way, it is necessary to copy it to a junk file and manipulate that. In order to do this, a lot of PIL, scipy, os and numpy functions were used. The original image is copied to a new file where the grid can be added and displayed. 

Another interesting part is how the resulting bottle cap image is made. Once the section averages are calculated. Each section loops through the database of bottle caps to find the most suitable match. This cap is placed in an array. Once the whole array has been populated, the cap images are resized and stitched together into one image that can then be displayed. 

—— Resources Used——
Images for bottle caps: http://www.bottlecaps.de/index/
Image manipulation (scipy and numpy): http://docs.scipy.org/doc/scipy/reference/misc.html
Also a lot of help from the class code and slides
