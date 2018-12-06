import sys
import numpy as np
import cv2 as cv

# параметры цветового фильтра
hsv_min = np.array((0, 20, 0), np.uint8)
hsv_max = np.array((170, 255, 255), np.uint8)

if __name__ == '__main__':
    print(__doc__)

    fn = 'th.jpg' # путь к файлу с картинкой
    img = cv.imread(fn)

    hsv = cv.cvtColor( img, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV
    thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
    # ищем контуры и складируем их в переменную contours
    _, contours, hierarchy = cv.findContours( thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # отображаем контуры поверх изображения
    cv.drawContours( img, contours, -1, (0,255,0), 3, cv.LINE_AA, hierarchy, 1 )
    cv.imshow('contours', img) # выводим итоговое изображение в окно

    cv.waitKey()
    cv.destroyAllWindows()