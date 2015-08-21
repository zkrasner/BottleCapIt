from scipy import misc
import os
import math


class BottleCap(object):
    ''' A BottleCap object. Satisfies the custon class
    requirement of the project'''

    ''' Initialize the object with the given image'''
    def __init__(self, image_name):
        self.img_dir = "bottlecaps"
        self.image = misc.imread(os.path.join(self.img_dir, image_name))
        self.average = find_average_color_centered(self.image)

    ''' magic method for the custom class. Satisfies the magic method
    requirement of the project'''
    def __str__(self):
        return str(self.average)

    ''' Just a getter for the average color of the bottle cap '''
    def average(self):
        return self.average

    ''' when displaying the bottle cap image, the original images must be
    scaled down so the bottle cap image can fit on the user's monitor '''
    def resize(self, height, width):
        if (height < 10):
            height = 10
        if (width < 10):
            width = 10
        return misc.imresize(self.image, (height, width))

    ''' Played around with weighing the colors differently based on how the
    human eye picks up subtleties in the color change of various colors. The
    results from using this method are not very great though. '''
    def getWeightedDistance(self, r, g, b):
        return math.sqrt(((r-self.average[0])*.3)**2 +
                         ((g-self.average[1])*.59)**2 +
                         ((b-self.average[2])*.11)**2)

    ''' Standard three dimensional distance evaluation '''
    def getDistance(self, r, g, b):
        return math.sqrt(((r-self.average[0]))**2 +
                         ((g-self.average[1]))**2 +
                         ((b-self.average[2]))**2)


def find_average_color_all(img):
    ''' Find the average rgb color of a given square image '''
    shape = img.shape
    total_size = shape[0] * shape[1]
    if (total_size == 0):
            return (0, 0, 0)
    sum_red = sum_green = sum_blue = 0
    for row in range(shape[0]):
        for col in range(shape[1]):
            sum_red += img[row, col, 0]
            sum_green += img[row, col, 1]
            sum_blue += img[row, col, 2]
    return (int(sum_red/total_size) % 256,
            int(sum_green/total_size) % 256,
            int(sum_blue/total_size) % 256)


def find_average_color_centered(img):
    ''' find the average color of the centermost pixels of a square image. Used
    to account for the different backgrounds of the bottle cap images. Using
    this method gets a better representation of the bottle cap's true color.'''
    shape = img.shape
    total_size = shape[0] * shape[1]
    if (total_size == 0):
            return (0, 0, 0)
    center = (shape[0]/2, shape[1]/2)
    sum_red = sum_green = sum_blue = 0
    for row in range(shape[0]):
        for col in range(shape[1]):
            dist = math.sqrt((row - center[0])**2 + (col - center[1])**2)
            if (dist < 3 / 8*shape[0]):
                sum_red += img[row, col, 0]
                sum_green += img[row, col, 1]
                sum_blue += img[row, col, 2]
    return (int(sum_red/total_size) % 256,
            int(sum_green/total_size) % 256,
            int(sum_blue/total_size) % 256)
