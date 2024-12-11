import cv2
image_paths=['images/karmel/carmel-00.png','images/karmel/carmel-01.png','images/karmel/carmel-02.png','images/karmel/carmel-03.png','images/karmel/carmel-04.png']
#image_paths=['images/diamondhead/diamondhead-10.png','images/diamondhead/diamondhead-11.png','images/diamondhead/diamondhead-12.png','images/diamondhead/diamondhead-13.png']
#image_paths=['images/hotel/hotel-02.png','images/hotel/hotel-03.png','images/hotel/hotel-04.png']
#image_paths=['images/rio/rio-47.png','images/rio/rio-48.png','images/rio/rio-49.png']

imgs = []

for i in range(len(image_paths)):
	imgs.append(cv2.imread(image_paths[i]))
#   imgs[i]=cv2.resize(imgs[i],(0,0),fx=0.4,fy=0.4)
#Ewentualne skalowanie obrazków gdy jest ich za dużo
#obrazki pojedyncze
for i in range(len(imgs)):
    cv2.imshow(f'{i}',imgs[i])

stitchy = cv2.Stitcher.create()
(status,output) = stitchy.stitch(imgs)

if status != cv2.STITCHER_OK:
#stitcher zwraca 0 jeśli się nie powiedzie
	print("Tworzenie panoramy nie powiodło się")
else:
	print('Panorama gotowa!!!')

#Pokaz panoramy
cv2.imshow('final result',output)

cv2.waitKey(0)
