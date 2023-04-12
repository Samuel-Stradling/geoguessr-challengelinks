from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re
import sys


def get_username_password():
    valid = False
    while not valid:
        username = input("Enter email: ")
        if validate_email(username):
            valid = True
        else:
            print("Invalid email. Please try again")

    password = input("Password: ")

    return (username, password)


def validate_email(email) -> bool:
    if re.search("^[^@]+@[^@]+(?:.com|.net|.org|.edu|.co.uk|.ac.uk)", email):
        return True
    else:
        return False


def write_to_txt(link, mapName, roundTime, move, pan, zoom):
    with open("links.txt", "a") as file:
        file.write(f"{mapName} time:{roundTime} move:{move} pan:{pan} zoom:{zoom}  : {link}\n")


def login(username, password) -> webdriver.Chrome() :
    """Logs into the geoguessr website. Navigates to the map screen. Returns the driver object, to be passed into subsequent functions"""

    ## run this to install the chrome driver first time
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    driver = webdriver.Chrome()
    driver.switch_to.window(driver.current_window_handle)
    driver.maximize_window()
    
    url = "https://www.geoguessr.com/signin"
    driver.get("https://www.geoguessr.com/signin")
    driver.implicitly_wait(10)

    usernameEL = driver.find_element(By.NAME, "email")
    passwordEL = driver.find_element(By.NAME, "password")

    # accept cookies
    driver.find_element(By.ID, "accept-choices").click()
    
   
    usernameEL.send_keys(username)
    passwordEL.send_keys(password)

    
    # login button
    driver.find_element(
        By.XPATH,
        '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/form/div/div[3]/div[1]/div/button',
    ).click()
    time.sleep(2)
    return driver


def get_link(driver, roundTime: int=0, map: str="world", move: bool=True, pan: bool=True, zoom: bool=True) -> webdriver.Chrome() :

    """get_link fetches a challenge link given the driver (also returned by get_link). Optional args:
    => roundTime: an integer specifing the length of time for each round. Maximum is 10. 0[default] is infinite time
    => map: a string specifing the map to be played. Words should be non capitalised and hyphen delimited. Default is world
    => move: a boolean specifing if the player should be able to move in the map. Default is True
    => pan: a boolean specifing if the player should be able to pan in the map. Default is True
    => zoom: a boolean specifing if the player should be able to zoom in the map. Default is True"""
    try:
    
        mapUrls = {
            'world': 'https://www.geoguessr.com/maps/world/play',
            'famous-places': 'https://www.geoguessr.com/maps/famous-places/play',
            'united-kingdom': 'https://www.geoguessr.com/maps/uk/play',
            'united-states': 'https://www.geoguessr.com/maps/usa/play',
            'european-union': 'https://www.geoguessr.com/maps/european-union/play',
            'london': 'https://www.geoguessr.com/maps/london',
            'slovakia': 'https://www.geoguessr.com/maps/slovakia'
        }

        timeSliderXCoordinateOffset = {
            0: -21,
            1: -11,
            2: 0,
            3: 10,
            4: 21,
            5: 31, 
            6: 41,
            7: 52,
            8: 62,
            9: 73,
            10: 83
        }

        if type(roundTime) != int or roundTime < 0 or roundTime > 10:
            raise ValueError()
        if type(map) != str or not map in mapUrls:
            raise ValueError()
        if type(move) != bool and type(pan) != bool and type(zoom) != bool:
            raise ValueError()
        

        

        driver.get(mapUrls[map])

        # click challenge
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[2]/div[2]/label/div[1]').click()

        # click default settings
        try:
            driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]')
        except:
            driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div/div[2]/input').click()

        # this stays unchecked on the same session
        #driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div/div[2]/input').click()

        # move slider
        setTime = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[1]/div/label/div[3]')
        setTime = setTime.get_attribute('innerHTML')
        if setTime[0:setTime.index(" ")] != roundTime and roundTime != 0:
            handle = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[1]/div/label/div[2]/div/div/div[2]')
            ActionChains(driver).drag_and_drop_by_offset(handle, timeSliderXCoordinateOffset[roundTime], 0).perform()

        if not move:
            setStatus = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[1]/div[2]')
            setStatus = setStatus.get_attribute('innerHTML')
            if "no" not in setStatus.lower():
                driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[1]/div[3]/input').click()
        if not pan:
            setStatus = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[2]/div[2]')
            setStatus = setStatus.get_attribute('innerHTML')
            if "no" not in setStatus.lower():
                driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[2]/div[3]/input').click()
        if not zoom:
            setStatus = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[3]/div[2]')
            setStatus = setStatus.get_attribute('innerHTML')
            if "no" not in setStatus.lower():
                driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[3]/div[3]/input').click()
        
        time.sleep(0.5)
        # go to the link
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/div[3]/button').click()
        #time.sleep(0.5)

        # select link
        linkContainer = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div/div/div/section/article/div/span/input')
        link = linkContainer.get_attribute('value')

        
        write_to_txt(link, map, roundTime, move, pan, zoom)


        return driver

    except Exception as e:
        sys.exit(f"Error: {e}")

def close(driver):
    driver.close()



def main():
    username, password = get_username_password()
    driver = login(username, password)

    
    count = 0
    while count < 10:
        defaultWorld = get_link(driver)
        count+=1






    close(driver)



if __name__ == "__main__":
    main()