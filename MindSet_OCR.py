import cv2
import numpy as np
import pytesseract

def sharpness(im):
	kernel = np.array([[0,1,0], [1,-4,1], [0,1,0]])
	im = cv2.filter2D(im, -1, kernel)
	return im

def contur(im):
	img_grey = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	#зададим порог
	thresh = 100
	#получим картинку, обрезанную порогом
	ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
	#надем контуры
	contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#создадим пустую картинку
	img_contours = np.zeros(im.shape)
	#отобразим контуры
	cv2.drawContours(img_contours, contours, -1, (255,255,255), 1)
	return im


#import os; os.environ['TESSDATA_PREFIX']='C:\Program Files (x86)\Tesseract-OCR'

# Путь для подключения tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

# Подключение фото
#img = cv2.imread('4-esEJgh_kI.jpg')
#img = cv2.imread('ffff.PNG')
img = cv2.imread('1.PNG')

img = sharpness(img)
img = contur(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Будет выведен весь текст с картинки
config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(img, lang='rus', config=tessdata_dir_config) #'rus+eng' -> 'rus'
print(text.split('\n'))

# Делаем нечто более крутое!!!

data = pytesseract.image_to_data(img, lang='rus', config=tessdata_dir_config) #'rus+eng' -> 'rus'

# Перебираем данные про текстовые надписи
for i, el in enumerate(data.splitlines()):
	if i == 0:
		continue

	el = el.split()
	try:
		# Создаем подписи на картинке
		x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
		#print(x,y,w,h, el[10]) #11 -> 10
		cv2.rectangle(img, (x - 5, y - 5), (w + x + 10, h + y + 10), (0, 0, 255), 1)
		cv2.putText(img, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
	except IndexError:
		print("Операция была пропущена")

# Отображаем фото
cv2.imshow('Result', img)
cv2.waitKey(0)