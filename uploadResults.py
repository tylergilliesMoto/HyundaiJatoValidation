import pandas as pd
import ast
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# This file will take the result of jatoAPICall where it got all the non matches
# This will upload those to basecamp or to a text file
# Also we are going to have a list of ones to ignore


def get_id(title, searchtype):  # This is for the web scraping process
    if searchtype == 1:
        Title = driver.find_element(By.LINK_TEXT, title)
    else:
        Title = driver.find_element(By.PARTIAL_LINK_TEXT, title)
    print(Title.text)
    Link = Title.get_attribute('href')
    temp = Link.split('/')
    ID = temp[-1]  # THIS IS THE IMPORTANT PART OF THIS STEP
    return ID


# ignore these ones
ignore = ['Premium Paint', 'Metallic Paint', 'Pearl Paint', 'Matte Paint', 'Mica Paint', 'Two-Tone Roof', 'Two-tone roof', 'PP', 'MP', 'MAP', 'MCP', 'TT', 'TTW', 'TTRM', 'TTRMI', 'TTRP', 'TTRPP']

# open file we created in jato api call file
df = pd.read_excel("Hyundai vs JATO.xlsx")
df.sort_values(by=['Year', 'Model'])

print("----------------------------------------------")
reportMode = input("Would you like this uploaded to basecamp (press 1) or outputted as a text file (press 2)? ")
print("----------------------------------------------")
outputMode = input("What do you want to report? Press corresponding number:\n1) Color Options in JATO but not in Hyundai API\n2) Color Options in the Hyundai API but not in JATO\n3) All of the Above\n")
print("----------------------------------------------")

f1 = open("Options Not in JATO.txt", "w")
f2 = open("Options Not in Hyundai API.txt", "w")

# Get 2 lists of the ones to upload, we know to upload it because the list of codes isnt blank
notInJatoTitles = []
notInHyunTitles = []
notInJato = []
notInHyun = []
for i in range(len(df)):
    # get all the ones not in jato
    missingJato = df.loc[i, 'Names Not in JATO']
    if str(missingJato) != '[]':
        output1 = str(df.loc[i, 'Year']) + " " + str(df.loc[i, 'Make']) + " " + str(df.loc[i, 'Model']) + " " + str(df.loc[i, 'Trim']) + " " + str(missingJato) + " " + str(df.loc[i, 'Not in JATO'])  # Full vehicle output
        title1 = str(df.loc[i, 'Year']) + " " + str(df.loc[i, 'Make']) + " " + str(df.loc[i, 'Model']) + " " + str(df.loc[i, 'Trim'])

        # Write that to text file, add full output to list and add title to another list
        f1.write(output1 + '\n')
        notInJato.append(output1)
        notInJatoTitles.append(title1)


    # get all the ones not in hyundai API, am filtering out the ones in ignore (list at the top of this file)
    missingHyun = df.loc[i, 'Names Not in Hyundai']
    if str(missingHyun) != '[]' and str(missingHyun) != "['Missing JATO ID']":
        arr = []
        arr = ast.literal_eval(str(missingHyun))
        # print(str(type(arr)) + str(arr))

        missing = []
        for j in arr:
            if j not in ignore:
                missing.append(j)

        arr = ast.literal_eval(str(df.loc[i, 'Not in Hyundai']))

        missing2 = []
        for j in arr:
            if j not in ignore:
                missing2.append(j)


        if str(missing) != '[]':
            output2 = str(df.loc[i, 'Year']) + " " + str(df.loc[i, 'Make']) + " " + str(df.loc[i, 'Model']) + " " + str(df.loc[i, 'Trim']) + " " + str(missing) + " " + str(missing2)
            title2 = str(df.loc[i, 'Year']) + " " + str(df.loc[i, 'Make']) + " " + str(df.loc[i, 'Model']) + " " + str(df.loc[i, 'Trim'])

            # Write that to text file, add full output to list and add title to another list
            f2.write(output2 + '\n')
            notInHyun.append(output2)
            notInHyunTitles.append(title2)


f1.close()
f2.close()



if reportMode == '1':
    print("______________________________________________")
    title = input("Please Enter the Exact Title of the To-Do List: ")
    print("______________________________________________")
    # lastMonth_title = input("Please Enter the Exact Title of the To-Do List of past Month: ")
    # print("______________________________________________")
    recip = input("Please Enter the Recipient (First Name Only): ")
    print("----------------------------------------------")

    # Init webdriver
    options = Options()
    options.headless = False
    options.add_argument("--log-level=3")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("start-maximized")
    options.add_argument("enable-experimental-web-platform-features")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(10)
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    wait = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions)

    # Site Info
    url = "https://3.basecamp.com/5167486/buckets/23586672/todosets/4050618286"
    email = "ba@motoinsight.com"
    password = "Unhaggle655"

    TIMEOUT_WAIT = 60 * 5  # in secs

    # Go to the website and log in
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(email + Keys.ENTER)
    time.sleep(0)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/form[2]/input[5]').click()
    time.sleep(2)


    # -------------------------------------------- Adding the New UIDs -----------------------------------------------------
    # This will get an id number we will need to identify which month to add the items to

    monthTitle = driver.find_element(By.LINK_TEXT, title)
    print(monthTitle.text)
    monthLink = monthTitle.get_attribute('href')
    temp = monthLink.split('/')
    monthID = temp[-1]  # THIS IS THE IMPORTANT PART OF THIS STEP

    monthID = get_id(title, 1)

    # Because of the way the html works on this site, adding consecutive things changes the value of the xpaths for some elements
    # so, we first find how many things are in the list already, the actual number is that number minus 1 because there is a hidden 'li' item
    test = driver.find_element(By.XPATH, '//*[@id="recording_' + monthID + '"]/ul')
    num = test.find_elements_by_tag_name('li')
    counter = len(num)
    print(str(counter - 1) + " to-do's in there already")

    # click button to add a to-do (ONLY NEED TO PRESS THIS THE FIRST TIME, AFTER THE FIRST ONE YOU CAN CONTINUOUSLY ADD MORE)
    time.sleep(2)
    WebDriverWait(driver, TIMEOUT_WAIT).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="recording_' + monthID + '"]/div[3]/button'))).click()
    time.sleep(2)

    # Loop through all the trims
    if outputMode == '1' or outputMode == '3':
        for i in range(len(notInHyun)):
            message = "API Inconsistency: " + str(notInHyunTitles[i])
            comment = 'Hey ' + recip + ', these colors are present in the JATO API for this trim but are not listed in the Hyundai API: ' + notInHyun[i]

            # enter the recipient
            WebDriverWait(driver, TIMEOUT_WAIT).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="todo_assignees"]'))).send_keys(recip + Keys.ENTER)

            # click to not notify --> comment this out if you want to notify them
            WebDriverWait(driver, TIMEOUT_WAIT).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '//*[@id="recording_' + monthID + '"]/ul/li[' + str(
                                                                                          counter) + ']/div/form/section/div[1]/div/div/label/span[1]/span'))).click()
            time.sleep(2)

            # click and add note/comment
            WebDriverWait(driver, TIMEOUT_WAIT).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '// *[ @ id = "recording_' + monthID + '"] / ul / li[' + str(
                                                                                          counter) + '] / div / form / section / div[5] / div[1]'))).click()
            WebDriverWait(driver, TIMEOUT_WAIT).until(EC.presence_of_element_located(
                (By.XPATH, '// *[ @ id = "new_todo_description_for_parent_' + monthID + '"]'))).send_keys(comment)

            # Enter the title and then press the enter key to submit. (Simpler than pressing submit button because that xpath changes)
            WebDriverWait(driver, TIMEOUT_WAIT).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="todo_content"]'))).send_keys(message + Keys.ENTER)

            time.sleep(1)
            counter += 1

    if outputMode == '2' or outputMode == '3':
        for i in range(len(notInJato)):
            message = "API Inconsistency: " + str(notInJatoTitles[i])
            comment = 'Hey ' + recip + ', these colors are present in the Hyundai API for this trim but are not listed in the JATO API: ' + notInJato[i]

            # enter the recipient
            WebDriverWait(driver, TIMEOUT_WAIT).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="todo_assignees"]'))).send_keys(recip + Keys.ENTER)

            # click to not notify --> comment this out if you want to notify them
            WebDriverWait(driver, TIMEOUT_WAIT).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '//*[@id="recording_' + monthID + '"]/ul/li[' + str(
                                                                                          counter) + ']/div/form/section/div[1]/div/div/label/span[1]/span'))).click()
            time.sleep(2)

            # click and add note/comment
            WebDriverWait(driver, TIMEOUT_WAIT).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '// *[ @ id = "recording_' + monthID + '"] / ul / li[' + str(
                                                                                          counter) + '] / div / form / section / div[5] / div[1]'))).click()
            WebDriverWait(driver, TIMEOUT_WAIT).until(EC.presence_of_element_located(
                (By.XPATH, '// *[ @ id = "new_todo_description_for_parent_' + monthID + '"]'))).send_keys(comment)

            # Enter the title and then press the enter key to submit. (Simpler than pressing submit button because that xpath changes)
            WebDriverWait(driver, TIMEOUT_WAIT).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="todo_content"]'))).send_keys(message + Keys.ENTER)

            time.sleep(1)
            counter += 1




if reportMode == '2':
    print("done")