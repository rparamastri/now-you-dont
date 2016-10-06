# overlay.py
# author: Renata Paramastri
# Steganography by encoding a picture in two pictures such that overlaying
# the two pictures creates the original.

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import argparse
import random

SLASH = True
BACKSLASH = False
ENCODED_1 = "encoded_1.png"
ENCODED_2 = "encoded_2.png"
OVERLAY = "overlay.png"
COLORMAP = "gray"  # for a black and white image

def getArgs():
    parser = argparse.ArgumentParser(description="Encodes a black and white " + 
                                                 "image in two images.")
    parser.add_argument("filename")
    return parser.parse_args().filename

def randomSlash():
    """ Randomly decides if the black cells of a pixel 
    are arranged as a slash or backslash.
    Returns this decision.
    """
    return random.choice((SLASH, BACKSLASH))

def drawSlash(topRow, leftCol, imageData):
    """
    topRow    -- the top row of the 2x2 cell
    leftCol   -- the left row of the 2x2 cell
    imageData -- the array we are modifying
    Draws a black slash in the given 2x2 cell of imageData.
    """
    # determine pixel indices
    topLeft     = (topRow*2    , leftCol*2    )
    topRight    = (topRow*2    , leftCol*2 + 1)
    bottomLeft  = (topRow*2 + 1, leftCol*2    )
    bottomRight = (topRow*2 + 1, leftCol*2 + 1)

    imageData[topLeft]     = 1.0
    imageData[topRight]    = 0.0
    imageData[bottomLeft]  = 0.0
    imageData[bottomRight] = 1.0

def drawBackslash(topRow, leftCol, imageData):
    """
    topRow    -- the top row of the 2x2 cell
    leftCol   -- the left row of the 2x2 cell
    imageData -- the array we are modifying
    Draws a black backslash in the given 2x2 cell of imageData.
    """
    # determine pixel indices
    topLeft     = (topRow*2    , leftCol*2    )
    topRight    = (topRow*2    , leftCol*2 + 1)
    bottomLeft  = (topRow*2 + 1, leftCol*2    )
    bottomRight = (topRow*2 + 1, leftCol*2 + 1)

    imageData[topLeft]     = 0.0
    imageData[topRight]    = 1.0
    imageData[bottomLeft]  = 1.0
    imageData[bottomRight] = 0.0

    
def encode(originalData):
    """ Given a 2D numpy array representing an image, create two 2D numpy array
    with double the width and double the height of the original,
    where the original image is encoded.
    Saves the two arrays to images.
    Returns the two arrays in a tuple (first, second).
    """
    height, width = originalData.shape
    firstData = np.empty((height*2, width*2), dtype="float32")
    secondData = np.empty((height*2, width*2), dtype="float32")

    # iterate through the original data
    for row in range(height):
        for col in range(width):
            direction = randomSlash()

            # randomly populate the first image
            # and populate the second image based
            # on the original and first image
            if direction == SLASH:
                drawSlash(row, col, firstData)
                if originalData[row, col] == 0:  # pixel is black
                    drawBackslash(row, col, secondData)
                else:                            # pixel is white
                    drawSlash(row, col, secondData)
            else:
                drawBackslash(row, col, firstData)
                if originalData[row, col] == 0:  # pixel is black
                    drawSlash(row, col, secondData)
                else:                            # pixel is white
                    drawBackslash(row, col, secondData)

    mpimg.imsave(ENCODED_1, firstData, cmap = COLORMAP)
    mpimg.imsave(ENCODED_2, secondData, cmap = COLORMAP)

    return (firstData, secondData)

def overlay(firstData, secondData):
    """
    firstData and secondData are 2D numpy arrays of the same dimensions.
    Overlays the images.
    Saves the new image as OVERLAY.
    Returns the resulting array.
    """
    height, width = firstData.shape
    overlayData = np.empty((height, width), dtype="float32")

    # iterate through each pixel
    for row in range(height):
        for col in range(width):
            # if either cell is black, the resulting overlay is black
            if firstData[row,col] == 0.0 or secondData[row,col] == 0.0:
                overlayData[row, col] = 0.0
            else:  # both have white pixels
                overlayData[row, col] = 1.0  # resulting overlay is white

    mpimg.imsave(OVERLAY, overlayData, cmap = COLORMAP)

    return overlayData


def oneChannel(imageData):
    """ Given a 3D numpy array representing an image with multiple channels,
    pick the first channel to make a 2D numpy array of the image.
    """
    return imageData[:,:,0]

def main():
    filename = getArgs()

    originalData = mpimg.imread(filename)
    oneChannelData = oneChannel(originalData)

    firstData, secondData = encode(oneChannelData)
    overlayData = overlay(firstData, secondData)

    # plotting
    fig = plt.gcf()

    # arrange layout of axes
    axOriginal = plt.subplot2grid((3,2), (0,0), colspan=2)
    ax1 = plt.subplot2grid((3,2), (1,0))
    ax2 = plt.subplot2grid((3,2), (1,1))
    axOverlay = plt.subplot2grid((3,2), (2,0), colspan=2)

    # hide axes labels and ticks
    axOriginal.get_xaxis().set_visible(False)
    axOriginal.get_yaxis().set_visible(False)
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    axOverlay.get_xaxis().set_visible(False)
    axOverlay.get_yaxis().set_visible(False)

    # plot images
    axOriginal.imshow(originalData, cmap = COLORMAP)
    ax1.imshow(firstData, cmap = COLORMAP)
    ax2.imshow(secondData, cmap = COLORMAP)
    axOverlay.imshow(overlayData, cmap = COLORMAP)

    axOriginal.set_title("Original image")
    axOverlay.set_title("Overlay result")

    plt.show()

if __name__ == "__main__":
    main()


