import requests
import cv2
import numpy as np
import json
# import colorsys

def lambda_handler(event, context):  
    print("testtttt")
    print('event',event)
    if event:
        url = event['url']

    else :
       url = 'https://d30ukgyabounne.cloudfront.net/face.jpeg'


    print("Hello AWS!")
    val = userSkinTone(url)
    print('vvvvvvvvvvvv',val)
    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': val
}

def avgHSVCalc(imgHSV):
    print('inside avgHSVCalc')

    # =-=-=-= UNOPTIMIZED =-=-=-=

    # imgHue = 0
    # imgSat = 0
    # imgVib = 0

    # pixelCount = len(imgHSV[0]) * len(imgHSV) # col * row
    # print('pixelCount',pixelCount)

    # for i in imgHSV: # i is a particular row
    #     for n in i: # n is a partcular column
    #         # if black, disregard pixel for averaging
    #         if n[0] == 0 and n[1] == 0 and n[2] == 0 : 
    #             pixelCount = pixelCount - 1

    #         else :
    #             imgHue = imgHue + n[0]
    #             imgSat = imgSat + n[1]
    #             imgVib = imgVib + n[2]
    #         # print(f"{n[0]} {n[1]} {n[2]}")


    # avgImgHue = imgHue / pixelCount
    # avgImgSat = imgSat / pixelCount
    # avgImgVib = imgVib / pixelCount


    # # HSV in CV2 is [179,255,255]. Conversions:
    # # avgImgHue = (avgImgHue / 179) * 360
    # # avgImgSat = (avgImgSat / 255) * 100
    # # avgImgVib = (avgImgVib / 255) * 100
    # # /\ If commented out, we are using 0-255 range for S&V.
    # print('3')
    # return [avgImgHue, avgImgSat, avgImgVib]

    # =-=-=-= OPTIMIZED =-=-=-=

    # Split HSV channels into separate arrays.
    imgHueChannel, imgSatChannel, imgVibChannel = cv2.split(imgHSV)

    # Getting average of each channels where pixel isn't black (0).
    imgHueChannel_np = np.array(imgHueChannel)
    imgSatChannel_np = np.array(imgSatChannel)
    imgVibChannel_np = np.array(imgVibChannel)

    avgImgHue = imgHueChannel_np.mean(where = imgHueChannel_np > 0)
    avgImgSat = imgSatChannel_np.mean(where = imgSatChannel_np > 0)
    avgImgVib = imgVibChannel_np.mean(where = imgVibChannel_np > 0)


    # HSV in CV2 is [179,255,255]. Conversions:
    # avgImgHue = (avgImgHue / 179) * 360
    # avgImgSat = (avgImgSat / 255) * 100
    # avgImgVib = (avgImgVib / 255) * 100
    # /\ If commented out, we are using 0-255 range for S&V.

    return [avgImgHue, avgImgSat, avgImgVib]


def userSkinTone(url):
    print('inside ust')

    response = requests.get(url)
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    userImg = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    ### userImg= cv2.imread('model.jpg')
    print('1')


    # Convert BGR to HSV
    userHSV = cv2.cvtColor(userImg, cv2.COLOR_BGR2HSV)


    # =-=-=-= UNOPTIMIZED MASKING BEGINS =-=-=-=

    # Define the lower and upper bounds of the skin tone in the HSV color space
    lower_skin = np.array([0, 20, 70])
    upper_skin = np.array([20, 255, 255])

    # Create a mask to segment the skin tone in the image
    userMask = cv2.inRange(userHSV, lower_skin, upper_skin)
    

    # Apply the mask to the original image to extract the skin tone area
    userSkin = cv2.bitwise_and(userImg, userImg, mask=userMask)
    userSkinHSV = cv2.cvtColor(userSkin, cv2.COLOR_BGR2HSV)
    
    print('2')

    userAvgHSV = avgHSVCalc(userSkinHSV)
    print('unoptimized avgHSV: ', userAvgHSV)


    # =-=-=-= OPTIMIZED MASKING BEGINS =-=-=-=

    if userAvgHSV[2] >= 181:
        lower_skin = np.array([6, 20, 90])
        upper_skin = np.array([16, 255, 255])
        print('light skin detected')

    elif userAvgHSV[2] < 181:
        lower_skin = np.array([0, 20, 45])
        upper_skin = np.array([16, 255, 255])
        print('dark skin detected')
    
    userMask = cv2.inRange(userHSV, lower_skin, upper_skin)
    # cv2.imwrite('Input1.jpg',userMask)
    userSkin = cv2.bitwise_and(userImg, userImg, mask=userMask)
    userSkinHSV = cv2.cvtColor(userSkin, cv2.COLOR_BGR2HSV)
    # cv2.imwrite('Input2.jpg',userSkin)

    userAvgHSV = avgHSVCalc(userSkinHSV)


    print('4')
    print(f"User Skin Avg HSV: {userAvgHSV}")
    return userAvgHSV

# lambda_handler('','')