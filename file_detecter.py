from os import listdir
from os.path import isfile, join
from yolo import image_checker
#function to return files in a directory
def fileInDirectory(my_dir: str):
    onlyfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return(onlyfiles)
#function comparing two lists


def listComparison(OriginalList: list, NewList: list):
    differencesList = [x for x in NewList if x not in OriginalList] #Note if files get deleted, this will not highlight them
    return(differencesList)


import time


def fileWatcher(watchDirectory: str, pollTime: int):
    while True:
        if 'watching' not in locals():  # Check if this is the first time the function has run
            previousFileList = fileInDirectory(watchDirectory)
            watching = 1
            print(previousFileList)

        time.sleep(pollTime)

        newFileList = fileInDirectory(watchDirectory)

        fileDiff = listComparison(previousFileList, newFileList)

        previousFileList = newFileList
        if len(fileDiff) == 0: continue
        for images in fileDiff:
            images=str(images)
            if images.endswith(".jpg") or images.endswith(".jpeg") or images.endswith(".png"):
                image_checker(images)

fileWatcher("graphs/", 1)