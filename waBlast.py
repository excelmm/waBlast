from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import keyboard
import pyautogui as gw
import copy
import re
import argparse
import sys
import time

WAIT = 300
CURRENT_NUMBER = "+00 000-0000-000" # Enter your WhatsApp number here

def main():
    pic = 1
    if len(sys.argv) not in [2, 3]:
        print("Usage: python", sys.argv[0], "salesNumbers.txt")
        sys.exit()

    # Parse arguments
    parser = argparse.ArgumentParser(description='PyWhatsapp Guide')
    parser.add_argument(sys.argv[1])
    try:
        parser.add_argument(sys.argv[2])
    except:
        pass
    parser.add_argument('--i', action='store', type=bool, default=False)
    parser.add_argument('--chrome_driver_path', action='store', type=str, default='C:/bin/chromedriver', help='chromedriver executable path (MAC and Windows path would be different)')
    parser.add_argument('--message', action='store', type=str, default='', help='Enter the msg you want to send')
    parser.add_argument('--remove_cache', action='store', type=str, default='False', help='Remove Cache | Scan QR again or Not')
    args = parser.parse_args()

    global driver
    driver = whatsapp_login(args.chrome_driver_path)
    gotoSavedContact(CURRENT_NUMBER)
    # driver.get("https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(CURRENT_NUMBER.replace("+","").replace(" ","").replace("-","")))
    # sendMessage("starting")
    messageNum = int(input("Enter number of messages to forward... "))
    time.sleep(2)
    driver.save_screenshot("logged.png")

    salesList = loadtxt(sys.argv[1])
    salesListChunks = []
    count = 0

    print("Sales List -->>", salesList)
    
    # Breaks up the broadcast list into chunks of 5
    i = 1
    while True:
        if i * 5 > len(salesList):
            break
        salesListChunks.append([salesList[i * 5 - 5], salesList[i * 5 - 4], salesList[i * 5 - 3], salesList[i * 5 - 2], salesList[i * 5 - 1]])
        i += 1
    
    print(salesListChunks)
    # exit()

    # while True:
    time.sleep(1)
    wa = gw.getWindowsWithTitle("Chrome")[0]

    start = time.perf_counter()

    # Start forwarding the messages
    for item in salesListChunks:
        try:
            gotoSavedContact(CURRENT_NUMBER)
            forwardMessage(messageNum, item, False)
            count += 5
            end = time.perf_counter()
            print(f"Entry number {count} finished. Time elapsed: {end-start:0.2f} seconds. Average time per entry: {(end - start) / count:0.2f} seconds.")
            print(f"ETA: {((end - start) / count) * (len(salesList) - count):0.1f} seconds")
        except Exception as e:
            print("Failed to send message.")
            print("Error:", e)
            # driver.save_screenshot(str(pic) + ".png")
            pic = 0
            continue

        

    driver.close()
    driver.quit()
    


def loadtxt(filename):
    results = []
    with open(filename, "r") as f:
        data = f.read().splitlines()
        for line in data:
            results.append(line)
    return results


def gotoSavedContact(name):  
    i = 0       
    while True:
        if getName(i) != name:
            i += 1
            if i == 200:
                return -1
            continue
        unread = getUnread(i)
        clickName(i)
        break
    return unread


def sendMessage(message):
    try:
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
    except:
        print("Couldn't load page.")
        return

    input_boxes = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    input_box = input_boxes[0]
    input_box.send_keys(message)
    input_box.send_keys(Keys.RETURN)
    time.sleep(3)


def forwardMessage(messageNum, numbers, sent):

    albumNum = 0
    albums = driver.find_elements_by_xpath('//div[@class="_269XL _3sKvP wQZ0F"]')
    # print("albumlen:",len(albums))
    if len(albums):
        albumNum = 3
        #albumNumText = driver.find_elements_by_xpath('//div[@class="_2iyx0"]/span')
        albumNumText = driver.find_elements_by_css_selector('.YZNwM.uslS5')

        # print("albumnumtextlen:",len(albumNumText))
        if len(albumNumText):
            # print(albumNumText[-1].text)
            albumNum += (int(albumNumText[-1].text.replace('+','')) - 1)
            # print("albumNum:", albumNum)
            
    messageNum -= albumNum

    num = str((-1)*(messageNum - 1)) if messageNum > 1 else ''
    if sent:
        # print("take from left")
        x_arg = '(//div[@class="tSmQ1"]/div[contains(@data-id,"false")]/div/div/div/div)[last()]'
    else:
        # print("take from right")
        x_arg = '(//div[@class="tSmQ1"]/div[contains(@data-id,"true")]/div/div/div/div)[last()]'

    action = ActionChains(driver)
    action.move_to_element(driver.find_element_by_xpath(x_arg)).perform()
    
    time.sleep(0.5)

    driver.find_element_by_xpath('//div[@data-js-context-icon="true"]').click()
    time.sleep(0.5)
    
    try:
        driver.find_element_by_xpath('//div[@title="Forward all"]').click()
    except:
        while True:
            try:
                driver.find_element_by_xpath('//div[@title="Forward message"]').click()
                break
            except:
                gotoSavedContact(CURRENT_NUMBER)
                continue
    time.sleep(1)

    # print (messageNum)
    if sent:
        # checkbox = driver.find_elements_by_xpath('//div[@class="z_tTQ"]/div[contains(@data-id,"false")]//div[@class="_2XWkx"]')
        checkbox = driver.find_elements_by_css_selector("div.message-in.focusable-list-item")
    else:
        # checkbox = driver.find_elements_by_xpath('//div[contains(@data-id,"true")]//div[@class="_2KoSK"]')
        checkbox = driver.find_elements_by_css_selector("div.message-out.focusable-list-item")

    print("checkboxlen:", len(checkbox))
    for i in range(messageNum - 1):
        time.sleep(0.5)
        num = -1 * (i + 2)
        checkbox[num].click()
    # print("click")
    
    try:
        driver.find_element_by_xpath('//button[@title="Forward messages"]').click()
    except:    
        driver.find_element_by_xpath('//button[@title="Forward message"]').click()
    input_box = driver.find_element_by_xpath('//div[@contenteditable="true"][1]')
    for number in numbers:
        input_box.clear()
        input_box.send_keys(number)
        time.sleep(0.5)
        input_box.send_keys(Keys.RETURN)
        time.sleep(0.4)
    try:
        driver.find_element_by_xpath('//div[@class="_3FwbN"]/div/div').click()
    except:
        # time.sleep(1)
        # keyboard.press_and_release("escape")
        # time.sleep(4)
        # keyboard.press_and_release("escape")
        # time.sleep(4)
        # keyboard.press_and_release("escape")
        driver.get("https://web.whatsapp.com")
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CLASS_NAME,'_1MZWu')))
        time.sleep(4)
        
    time.sleep(3)


def getName(pos):
    x_arg = '//div[contains(@style,"Y(' + str(pos*72) + 'px")]//div[@class="_3Tw1q"]'
    try:
        incoming = driver.find_element_by_xpath(x_arg)
    except:
        return None
    # print(incoming.text)
    return incoming.text


def clickName(pos):
    x_arg = '//div[contains(@style,"Y(' + str(pos*72) + 'px")]//div[@class="_3Tw1q"]'
    try:
        incoming = driver.find_element_by_xpath(x_arg)
    except:
        return None
    incoming.click()


def getUnread(pos):

    x_arg = '//div[contains(@style,"Y(' + str(pos*72) + 'px")]//div[@class="VOr2j"]'
    try:
        bubble = driver.find_element_by_xpath(x_arg)
    except:
        return None
    # print(bubble.text)
    return bubble.text


def whatsapp_login(chrome_path):

    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=./User_Data_touress")
    # chrome_options.add_argument("--profile-directory=Default")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-software-rasterizer')
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument('--remote-debugging-port=9222')
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--verbose")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3641.0 Safari/537.36")
    
    driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
    
    # driver = ChromeRemote()
    print(driver.current_url)
    driver.save_screenshot("test.png")
    
    driver.get("https://web.whatsapp.com")
    time.sleep(2)
    driver.save_screenshot("login.png")

    # try:
        # WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CLASS_NAME,'_210SC')))
    # except:
        # print("Unable to login.")
        # exit()
    
    print("QR scanned")

    return driver


if __name__ == "__main__":
    main()