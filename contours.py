''' Для определения контуров'''
''' На основе иерархии можно найти две страницы паспорта, и выровнять изображение для дальнейшей работы с ним'''
import cv2

def resize(im):
    dsize = (1060, 1500)
    im = cv2.resize(im, dsize)
    return im

image2 = cv2.imread('0.PNG')
#image2 = resize(image2)
img_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) 
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
ret, thresh2 = cv2.threshold(img_blur, 150, 255, cv2.THRESH_BINARY)
contours6, hierarchy6 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

ids = []
print(hierarchy6[0])
for i in range(len(hierarchy6[0])):
    if hierarchy6[0][i][2] != -1: # 2 - чехол паспорта при [0][i][2]
        ids.append(i)
contours = []
for i in ids:
    contours.append(contours6[i])

image_copy7 = image2.copy()
cv2.drawContours(image_copy7, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)
# смотрим резльтат
cv2.imshow('TREE', image_copy7)
print(f"TREE: {hierarchy6}")
cv2.waitKey(0)
#cv2.imwrite('contours_retr_tree.jpg', image_copy7)
cv2.destroyAllWindows()