import cv2, pytesseract, pyautogui, numpy as np, keyboard, time, requests
from fuzzywuzzy import fuzz, process
import tkinter as tk
from tkinter import messagebox

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

gem_url = "https://poe.ninja/api/data/itemoverview?league=Crucible&type=SkillGem"
gems = open('gems.txt').read().lower().splitlines()
altGemNames = ['phantasmal', 'divergent', 'anomalous']

#Mouse coordinates, right now first click : top left, second click : bottom right
def getCoordinates():
    first_click = True
    mouse_x1, mouse_y1 = None, None
    mouse_x2, mouse_y2 = None, None

    while True:
        time.sleep(0.1)
        if keyboard.is_pressed('x'):
            if first_click:
                mouse_x1, mouse_y1 = pyautogui.position()
                print(f"First click: ({mouse_x1}, {mouse_y1})")
                first_click = False
                time.sleep(0.3)
            else:
                mouse_x2, mouse_y2 = pyautogui.position()
                print(f"Second click: ({mouse_x2}, {mouse_y2})")
                break

    coords = [mouse_x1, mouse_y1, mouse_x2, mouse_y2]
    return coords
#Finding the best match from extracted text  and gem from text
def findMatch(match):
    print(process.extractOne(match, gems))
    print(process.extract(match, gems, limit=6))
    return process.extractOne(match, gems)[0]

#Showing gem data on screen
def showGemInfo(gem_dict):
    print("Showing gem info")
    info_text = ""
    if gem_dict == False:
        info_text = "Gem not found"
    else:
        for gem in gem_dict:
            gemName = gem['name']
            gemLevel = gem['gemLevel']
            gemQuality = gem['gemQuality']
            gemCorrupted = gem['gemCorrupted']
            gemValue = gem['gemValue']
            info_text += f"Gem: {gemName} Lvl: {gemLevel} Q: {gemQuality} Corr: {gemCorrupted} Val: {gemValue}\n"
    messagebox.showinfo("Gem Information", info_text)

#Finding the first potential match from screenshot
def identifyGem(text):
    words = text.split()
    print (words)
    index = -1
    gemString = ""

    for i, word in enumerate(words):
        if word.lower() in altGemNames :
            index = i
            break
    if index != -1:
        next_four_words = words[index:index+3]
        gemString = " ".join(next_four_words)
        print("I got:", gemString)
    else:
        print("Substring not found or insufficient words.")
        return False

    return gemString

#Getting data about the gem from poe ninja  api
def priceCheck(gem_name):
    response = requests.get(gem_url)
    gem_dict = []
    if(gem_name == False):
        showGemInfo(False)
    else:
        for gem in response.json()['lines']:
            if(gem['name'].lower() == gem_name):
                #Level
                gemLevel = gem.get('gemLevel', 'No info')
                #Qual
                gemQuality = gem.get('gemQuality', 'No info')
                #Corrupted
                gemCorrupted = gem.get('corrupted', 'No info')
                #Value
                gemValue = gem.get('chaosValue', 'No info')

                gem_dict.append({
                    'name': gem['name'].lower(),
                    'gemLevel': gemLevel,
                    'gemQuality': gemQuality,
                    'gemCorrupted': gemCorrupted,
                    'gemValue': gemValue
                })
        #print(gem_dict)
        showGemInfo(gem_dict)

def main():
    print ("Running...")
    #coords = getCoordinates()
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    while True:
        time.sleep(0.1)

        if keyboard.is_pressed('F3'):
            print ("Screenshot taken")

            #screenshot = pyautogui.screenshot(region=( coords[0], coords[1], coords[2]-coords[0], coords[3]-coords[1]))
            screenshot = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            extracted_text = pytesseract.image_to_string(image, config='--psm 6')
            extracted_text = extracted_text.lower()
            #cv2.imshow('Screenshot', image)
            #print(extracted_text)
            gemPlace = identifyGem(extracted_text)
            if not gemPlace:
                priceCheck(False)
            else:
                gemMatch = findMatch(gemPlace)
                priceCheck(gemMatch)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

        if keyboard.is_pressed('q'):
            break
    root.mainloop()

main()