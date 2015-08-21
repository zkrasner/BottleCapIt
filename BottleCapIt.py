import tkinter as tk
import argparse
from functools import partial, wraps
from scipy import misc
from PIL import Image, ImageTk
import numpy as np
import os
from BottleCap import *


# Main frame for the entire GUI
class TkinterGui(tk.Frame):

    STICKY = tk.N + tk.S + tk.E + tk.W
    # Directory for the bottle cap images
    BCDir = 'bottlecaps'

    # Initializing the GUI
    def __init__(self, image_name, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=self.STICKY)
        self.root = master if master is not None else self

        # Grab the image from the filename given by the user
        self.original = get_temp_image(image_name)
        # Tranfer the image to the junk file so it can be manipulated
        self.currentPhoto = make_img(image_name)

        # Build a frame for all of the buttons and labels on the left side
        self.LabelFrame = tk.Frame(self)
        self.LabelFrame.grid(sticky=self.STICKY)

        # Sliders to select the number of caps for each dimension
        self.heightLabel = tk.Label(self.LabelFrame,
                                    text="Height in bottle caps")
        self.heightLabel.grid(row=0, column=0)
        self.heightScale = tk.Scale(self.LabelFrame, from_=8,
                                    orient=tk.HORIZONTAL,
                                    command=self.updateCapInfo)
        self.heightScale.grid(row=1, column=0)
        self.widthLabel = tk.Label(self.LabelFrame,
                                   text="Width in bottle caps")
        self.widthLabel.grid(row=2, column=0)
        self.widthScale = tk.Scale(self.LabelFrame, from_=8,
                                   orient=tk.HORIZONTAL,
                                   command=self.updateCapInfo)
        self.widthScale.grid(row=3, column=0)
        ratio = "Image Ratio: {0:.2f} h/w".format(self.currentPhoto.height() /
                                                  self.currentPhoto.width())
        self.ratioLabel = tk.Label(self.LabelFrame, text=ratio)
        self.ratioLabel.grid(row=4, column=0)

        # Labels to give the user information for making a reasonable grid
        ratio2 = "Cap Ratio: {0:.2f} h/w".format(self.heightScale.get() /
                                                 self.widthScale.get())
        self.capRatioLabel = tk.Label(self.LabelFrame, text=ratio2)
        self.capRatioLabel.grid(row=5, column=0)

        # Interesting info on the size of the output
        numcaps = "Total Caps: {}".format(self.heightScale.get() *
                                          self.widthScale.get())
        self.numCapsLabel = tk.Label(self.LabelFrame, text=numcaps)
        self.numCapsLabel.grid(row=6, column=0)

        # Buttons to interact with the image
        # Show the grid on the image
        self.gridLabel = tk.Label(self.LabelFrame, text="Preview grid?")
        self.gridLabel.grid(row=7, column=0)
        self.showGridButton = tk.Button(self.LabelFrame, text="Grid",
                                        command=partial(self.addGrid,
                                                        image_name))
        self.showGridButton.grid(row=8, column=0)
        # convert the image into caps
        self.readyLabel = tk.Label(self.LabelFrame, text="Ready?")
        self.readyLabel.grid(row=9, column=0)
        self.capItButton = tk.Button(self.LabelFrame, text="Cap It!",
                                     command=partial(self.capIt, image_name))
        self.capItButton.grid(row=10, column=0)
        # display the image
        self.imageLabel = tk.Label(self, image=self.currentPhoto)
        self.imageLabel.grid(row=0, column=1)
        # Generate the list of bottle caps for the image
        self.createBottleImages()

    ''' Update the text for the label of the ratio for the grid being placed
    over the image as well as the number of caps that are required for it'''
    def updateCapInfo(self, newval):
        ratio2 = "Cap Ratio: {0:.2f} h/w".format(self.heightScale.get() /
                                                 self.widthScale.get())
        self.capRatioLabel['text'] = ratio2
        numcaps = "Total Caps: {}".format(self.heightScale.get() *
                                          self.widthScale.get())
        self.numCapsLabel['text'] = numcaps

    ''' Grab the image and place a grid over it so that the user can get a
    preview of how the bottle caps will be generated'''
    def addGrid(self, image_name):
        img = get_temp_image(image_name)
        imageHeight = img.shape[0]
        imageWidth = img.shape[1]
        for row in range(imageHeight):
            if (row % (int(imageHeight/self.heightScale.get())) == 0):
                for col in range(imageWidth):
                    img[row, col, :] = 0
            else:
                for col in range(0, imageWidth,
                                 int(imageWidth/self.widthScale.get())):
                    img[row, col, :] = 0
        save_grid_image(img)
        # Update the image in the GUI with the new grid
        self.updateImage()

    ''' Main function that kicks off the process of creating a bottle cap image
    from the input image'''
    def capIt(self, image_name):
        self.populateAverageColors(image_name)
        self.convertedCaps = np.empty((self.heightScale.get(),
                                       self.widthScale.get()), dtype=np.object)
        for row in range(self.heightScale.get()):
            for col in range(self.widthScale.get()):
                rgb = self.averageColors[row, col, :]
                cap = self.findClosestCap(rgb[0], rgb[1], rgb[2])
                self.convertedCaps[row, col] = cap
        save_grid_image(self.combineCaps())
        self.updateImage()

    ''' Once the grid of bottle caps has been generated, combine each of the
    smaller images into one large one in order to display it more easily'''
    def combineCaps(self):
        rows = []
        plotHeight = math.ceil(self.currentPhoto.height() /
                               self.heightScale.get())
        plotWidth = math.ceil(self.currentPhoto.width() /
                              self.widthScale.get())
        for row in range(self.heightScale.get()):
            start = self.convertedCaps[row, 0].resize(plotHeight, plotWidth)
            for cap in self.convertedCaps[row, 1:]:
                resized = cap.resize(plotHeight, plotWidth)
                start = np.hstack((start, resized))
            rows.append(start)
        ret = rows[0]
        for r in rows[1:]:
            ret = np.vstack((ret, r))
        return ret

    ''' Section the image by the rows and columns selected by the user and
    populate the matrix of the average rgb colors of each of these sections'''
    def populateAverageColors(self, image_name):
        self.averageColors = np.zeros((self.heightScale.get(),
                                       self.widthScale.get(),
                                       3), dtype=np.int)
        boxHeight = self.original.shape[0]/self.heightScale.get()
        boxWidth = self.original.shape[1]/self.widthScale.get()
        img = get_temp_image(image_name)
        for row in range(self.heightScale.get()):
            for col in range(self.widthScale.get()):
                ave = find_average_color_all(img[int(row*boxHeight):
                                                 int((row+1)*boxHeight),
                                                 int(col*boxWidth):
                                                 int((col+1)*boxWidth),
                                                 :])
                self.averageColors[row, col, :] = ave

    ''' Dive into the directory of bottle cap images and create a bottle cap
    object for each of the image files there. The images must be .jpg files'''
    def createBottleImages(self):
        self.cap_list = []
        for b in os.listdir(self.BCDir):
            if os.path.isfile(os.path.join(self.BCDir, b)) and '.jpg' in b:
                self.cap_list.append(BottleCap(b))

    ''' Decorator for the findClosestCap function debugging. Initially had some
    issues getting what seemed like correct caps to show up. Seeing the input
    average color along side the rgb value of the bottle cap selected helped
    with the debugging process. This decorator also takes advantage of the
    BottleCap's __str__ magic method and satisfies the both the magic method
    and decorator project requirements'''
    def _findCapDecorator(func):
        def inner(self, r, g, b):
            closest = func(self, r, g, b)
            print("input: {} --> closest: {}".format((r, g, b), closest))
            return closest
        return inner

    ''' Takes in the rgb values of the grid section in question and iterates
    through the list of bottle caps to find the cap that is closest to this
    section in color '''
    @_findCapDecorator
    def findClosestCap(self, r, g, b):
        closest = self.cap_list[0]
        closeDist = self.cap_list[0].getDistance(r, g, b)
        for cap in self.cap_list:
            this_dist = cap.getDistance(r, g, b)
            if this_dist < closeDist:
                closest = cap
                closeDist = this_dist
        return closest

    ''' After the image has been altered, either adding the grid or the image
    of all of the bottle caps, the GUI display must be updated to reflect these
    changes.'''
    def updateImage(self):
        im = Image.open(os.path.join('junk_file_for_write_and_read.png'))
        self.currentPhoto = ImageTk.PhotoImage(im)
        self.imageLabel['image'] = self.currentPhoto

###############################################################################
# Image Helpers#


def make_img(im_var):
    ''' Takes in the file name of the image and save the original image to a
    junk file that can be writen over. This preserves the original so it can
    still be accessed'''
    IMG_DIR = "imgs"
    original = misc.imread(os.path.join(IMG_DIR, im_var))
    save_grid_image(original)
    im = Image.open(os.path.join('junk_file_for_write_and_read.png'))
    return ImageTk.PhotoImage(im)


def get_temp_image(im_var):
    '''Grabs the input image. Usually used to grab the original input image.'''
    IMG_DIR = "imgs"
    return misc.imread(os.path.join(IMG_DIR, im_var))


def save_grid_image(im):
    ''' save the input image to the junk file.'''
    name = os.path.join('junk_file_for_write_and_read.png')
    misc.imsave(name, im)

###############################################################################


def tkinter_main(image_loc):
    ''' Main call to start the GUI up '''
    root = tk.Tk()
    app = TkinterGui(image_name=image_loc, master=root)
    app.mainloop()

''' Handles the input arguments from the terminal '''
if __name__ == '__main__':
    desc = 'A GUI writen in tkinter for the BottleCapIt application'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-t', '--tkinter', metavar='tkinter',
                        default=False, action='store_const', const=True,
                        dest='tkinter',
                        help='Runs the tkinter version of the app')
    parser.add_argument("image_file",
                        help="""name of the image in the imgs directory that
                             you wish to cappify""")
    args = parser.parse_args()
    if args.tkinter:
        tkinter_main(args.image_file)
    else:
        parser.print_help()
