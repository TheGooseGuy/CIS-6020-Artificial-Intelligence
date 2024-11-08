import cv2
from itertools import groupby
import os

def image_to_nonogram_opencv(image_path, threshold=128, resize=None):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if resize:
        image = cv2.resize(image, resize, interpolation=cv2.INTER_AREA)

    _, binary_image = cv2.threshold(image, threshold, 1, cv2.THRESH_BINARY_INV)

    row_clues = []
    for row in binary_image:
        row_clues.append([sum(1 for _ in group) for value, group in groupby(row) if value == 1])

    col_clues = []
    for col in binary_image.T:
        col_clues.append([sum(1 for _ in group) for value, group in groupby(col) if value == 1])

    return binary_image, row_clues, col_clues


def print_nonogram_clues(row_clues, col_clues):
    max_row_clues = max(len(clue) for clue in row_clues)

    for i in range(max(len(clue) for clue in col_clues)):
        line = ' ' * (max_row_clues * 2)
        for col_clue in col_clues:
            if i < len(col_clue):
                line += f"{col_clue[i]:>2} "
            else:
                line += "   "
        print(line)
    
    for row_clue in row_clues:
        row_line = " ".join(f"{num}" for num in row_clue).rjust(max_row_clues * 2)
        print(row_line)

# Convert picture to nonogram
image_path = "/Users/Desktop/A2-F2024/original image 1.jpg"
binary_image, row_clues, col_clues = image_to_nonogram_opencv(image_path, threshold=180, resize=(33, 33))
print_nonogram_clues(row_clues, col_clues)
print("Row Clues:", row_clues)
print("Column Clues:", col_clues)