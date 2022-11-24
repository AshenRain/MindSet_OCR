import cv2
import numpy as np
import pytesseract

def resize(im):
    dsize = (1060, 1500)
    im = cv2.resize(im, dsize)
    return im

def sharpness(im):
	kernel = np.array([[0,1,0], [1,-4,1], [0,1,0]])
	im = cv2.filter2D(im, -1, kernel)
	return im

def eroding(im):
	kernel = np.ones((2, 2), 'uint8')
	im = cv2.erode(im, kernel, cv2.BORDER_REFLECT, iterations=1)
	return im

def del_noise(im):
	im = resize(im)
	im = cv2.fastNlMeansDenoisingColored(im, None,10,10,7,21) # удаление шумов
	im = eroding(im)					  # уменьшение размеров контуров
	im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im = cv2.GaussianBlur(im, (3, 3), 0)
	#im = sharpness(im) #сомнительный фильтр
	return im

# Путь для подключения tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR-05\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR-05\\tessdata"'
# Подключение фото
img = cv2.imread('0.PNG')

#Блок обработки изображения
img = del_noise(img)

# Будет выведен весь текст с изображения
config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(img, lang='rus', config=tessdata_dir_config) #'rus+eng' -> 'rus'
print(text.split('\n'))


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
cv2.imwrite('test.jpg', img)
cv2.waitKey(0)




#['МО УФМС РОССИИ', 'ПО МУРМАНСКОЙ ОБЛАСТИ', '', 'В ГОРОДЕ МОНЧЕГОРСК', '', 'ХАЛАБУДИНА.', '', 'юлия', 'АЛЕКСЕЕВНА', 'ж п', '', 'МОНЧЕГОРСК', '', '']
#['ПАСПОРТНО-ВИЗОВЫМ ОТДЕЛЕНИЕМ', 'ОВД ПРЕСНЕНСКОГО РАЙОНА.', 'УВД ЦАО ГОРОДА МОСКВЫ', '', '09.11.2016. 772-112', '', 'ТРАМП', '', 'ДОНАЛЬД', 'джон', '14.06.1946', 'ГОР, куИНС', 'ШТАТ НЬЮ-ЙОРК', 'сил', '', '']
#['РОССИЙСКАЯ ФЕЛАЕРАЦИЯ', 'ОТДЕЛОМ ВНУТРЕННИХ ДЕЛ', 'ГОР. КРАСНОЗНАМЕНСК', '', '16.10.2016 _ 100-128', '', '= === = Г В |', '', 'фев: = ШАПОШНИКОВА', '', '"_— >в. НИКОЛАЕВНА', '. „. ЖЕН. 5. 14.09.1985', 'ь =>. ГОР. КРАСНОЗНАМЕНСК', '', '<<<Пробная страничка Паспорт РФ 2017>>>', '', 'Е', 'Е', '', '<<<Стоимость программы 10 $>>>', '<<<Ета11: ПВаскег1аБпеи@дта11.сом>>>>', '', '']
