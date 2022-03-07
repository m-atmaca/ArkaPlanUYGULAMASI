import cv2
import numpy as np
# import sys

def boyutlandir(arka, kamera):
        genislik = kamera.shape[1]
        yukseklik = kamera.shape[0]
        dim = (genislik, yukseklik)
        resized = cv2.resize(arka, dim, interpolation=cv2.INTER_AREA)
        return resized
# bu fonksiyonla kameradan gelen görüntüyle arkaplanda kullanılan görüntüyü aynı boyuta getiriyoruz
# arka değişkeni arkaplan videosu
# kamera değişkeni kameradan gelen görüntü

video = cv2.VideoCapture(0)
# kameradan gelen görüntü
arkaplan = cv2.VideoCapture("video.mp4")
# arkaplan videosu

success, ref_img = video.read()
flag = 0

while (True):
        success, kamera = video.read()
        success2, ap = arkaplan.read()
        ap = boyutlandir(ap, ref_img)

        if flag == 0:
                ref_img = kamera

        diff1 = cv2.subtract(kamera, ref_img)
        diff2 = cv2.subtract(ref_img, kamera)

        diff = diff1 + diff2
        diff[abs(diff) < 13.0] = 0
        #değerlerin farklarının mutlak değeri alınır

        gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        gray[np.abs(gray) < 10] = 0

        fgmask = gray.astype(np.uint8)
        fgmask[fgmask > 0] = 255

        # invert the mask
        fgmask_inv = cv2.bitwise_not(fgmask)
        # use the masks to extract the relevant parts from FG and BG
        kameragoruntusu = cv2.bitwise_and(kamera, kamera, mask=fgmask)
        arkagoruntu = cv2.bitwise_and(ap, ap, mask=fgmask_inv)
        # arkaplanla kamera görüntülerini birleştirir

        dst = cv2.add(arkagoruntu, kameragoruntusu)
        cv2.imshow('Background Removal', dst)
        key = cv2.waitKey(5) & 0xFF

        if ord('q') == key:
                break
        # çıkış yapmak için q 'ya basılır
        elif ord('w') == key:
                flag = 1
                print("Background Captured")
        # arkaplanla kameradan gelen göüntüyü eşleştirmek için w'ye basılır
        elif ord('e') == key:
                flag = 0
                print("Ready to Capture new Background")
# kameradan gelen görüntüyü almaz sadece arkaplan videosunu ekrana verdirir


cv2.destroyAllWindows()
video.release()
