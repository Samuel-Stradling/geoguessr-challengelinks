from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re


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


def validate_email(email):
    if re.search("^[^@]+@[^@]+(?:.com|.net|.org|.edu|.co.uk|.ac.uk)", email):
        return True
    else:
        return False



    


def login(username, password):
    """Logs into the geoguessr website. Navigates to the map screen. Returns the driver object, to be passed into subsequent functions"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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

    # singleplayer button
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div[2]/div/div[1]/div/div[1]/div/button').click()

    # classic maps button
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div[2]/div[2]/div[1]/div[2]/button').click()

    return driver


def world(driver, roundTime, move=True, pan=True, zoom=True):
    driver.get('https://www.geoguessr.com/maps/world/play')

    time.sleep(2)
    return driver

def uk(driver, roundTime, move=True, pan=True, zoom=True):
    pass
def us(driver, roundTime, move=True, pan=True, zoom=True):
    pass
def eu(driver, roundTime, move=True, pan=True, zoom=True):
    pass
def famous_places(driver, roundTime, move=True, pan=True, zoom=True):
    pass
def london(driver, roundTime, move=True, pan=True, zoom=True):
    pass

def close(driver):
    driver.close()

def main():
    username, password = get_username_password()
    loginPage = login(username, password)
    worldPage = world(loginPage, 0)






    close(worldPage)



if __name__ == "__main__":
    main()
