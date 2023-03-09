import requests
import cv2
import numpy as np
def lambda_handler(event, context):  
    print("testtttt")
    # val = userSkinTone.test()
    val = userSkinTone()
    print('vvvvvvvvvvvv',val)
    return val
    # response = requests.get("https://www.example.com/")
    # print(response.text)
    # return response.text

def avgHSVCalc(imgHSV):
    imgHue = 0
    imgSat = 0
    imgVib = 0

    pixelCount = len(imgHSV[0]) * len(imgHSV) # col * row


    for i in imgHSV: # i is a particular row
        for n in i: # n is a partcular column
            # if black, disregard pixel for averaging
            if n[0] == 0 and n[1] == 0 and n[2] == 0 : 
                pixelCount = pixelCount - 1

            else :
                imgHue = imgHue + n[0]
                imgSat = imgSat + n[1]
                imgVib = imgVib + n[2]
            # print(f"{n[0]} {n[1]} {n[2]}")


    avgImgHue = imgHue / pixelCount
    avgImgSat = imgSat / pixelCount
    avgImgVib = imgVib / pixelCount


    # HSV in CV2 is [179,255,255]. Conversions:
    # avgImgHue = (avgImgHue / 179) * 360
    # avgImgSat = (avgImgSat / 255) * 100
    # avgImgVib = (avgImgVib / 255) * 100
    # /\ If commented out, we are using 0-255 range for S&V.

    return [avgImgHue, avgImgSat, avgImgVib]


def userSkinTone():
    # # Load the image
    # userImg = cv2.imread('https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe8%2F4e%2Fe84e3d6cf5155ac862bafa692f10346c3957fa96.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]')

    url = 'https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe8%2F4e%2Fe84e3d6cf5155ac862bafa692f10346c3957fa96.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]'
    response = requests.get(url)
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    userImg = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Convert BGR to HSV
    userHSV = cv2.cvtColor(userImg, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the skin tone in the HSV color space
    lower_skin = np.array([0, 20, 70])
    upper_skin = np.array([20, 255, 255])

    # Create a mask to segment the skin tone in the image
    userMask = cv2.inRange(userHSV, lower_skin, upper_skin)

    # Apply the mask to the original image to extract the skin tone area
    userSkin = cv2.bitwise_and(userImg, userImg, mask=userMask)
    userSkinHSV = cv2.cvtColor(userSkin, cv2.COLOR_BGR2HSV)



    userAvgHSV = avgHSVCalc(userSkinHSV)
    print(f"User Skin Avg HSV: {userAvgHSV}")
    return userAvgHSV

