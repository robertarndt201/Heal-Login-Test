# -*- coding: utf-8 -*-
import os
import time
import json
import requests
from Crypto.Cipher import AES
from Crypto import Random
import base64
from lettuce import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


urlTranslation = {"https://patient.heal.com/login": "LoginPage",
                    "https://patient.heal.com/register": "RegistrationPage",
                    "https://patient.heal.com/book-visit": "BookVisitPage",
                    "http://resetpassword.heal.com/": "ResetPasswordPage",
                    "https://patient.heal.com/book-visit/choose-profile": 
                        "ChooseProfilePage"}


def getPage():
    """Returns URL of currently loaded page
    """

    _browser = world.browser
    if(_browser is None):
        return None
    return _browser.current_url


def getPageData(pageName):
    """Returns dictionary from page data JSON file corresponding to 
    user-specified page
    """

    curDir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    with open(curDir + "/pageData.json",'r') as f:
        config = json.load(f)
        return config[pageName]


def objectWait(objName, objCSS):
    """Waits for objects loading including those loaded using AJAX
    """

    _browser = world.browser
    try:
        objectToTest = WebDriverWait(_browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, objCSS))
        )
        print "Object {0} found".format(objName)
        print
    except (TimeoutException, NoSuchElementException):
        print "Object {0} exceeded timeout or was not present".format(objName)
        print


@step('Open webpage (\w+[s]?.:.\/{1,}\w+.\w+.\w+\/\w+) in Chrome')
def openPage(step, url):
    """Opens user-specified webpage by url
    """

    _browser = world.browser
    _browser.get(url)


def printAllElements(pageName):
    """Prints out all elements from page data JSON file corresponding to
    user-specified page 
    """

    config = getPageData(pageName)
    for k in config:
        print
        print "Key: {0}\nValue: {1}\nType: {2}".format(k, 
            config[k][0], config[k][1])


@step('Test hyperlinks on (\w+)')
def testLinks(step, pageName):
    """Iterates through hyperlinks on user-specified page, click link,
    then make sure we can return to the start page safely
    """

    _browser = world.browser
    url = urlTranslation.keys()[urlTranslation.values().index(pageName)]
    if(pageName != urlTranslation[getPage()]):
        _browser.get(url)

    WebDriverWait(_browser, 8)
    time.sleep(3)
    pageName = urlTranslation[getPage()]
    config = getPageData(pageName)
    for k in config:
        if(config[k][1] == "lnk"):
            objectWait(k, config[k][0])
            time.sleep(2)
            href = _browser.find_element_by_css_selector(config[k][0])
            resp = requests.get(href.get_attribute('href'))
            if(resp.ok):
                print "Page loaded ok with status {0}".format(resp.status_code)
            else:
                print "Page had trouble loading.  Status: {0}".format(
                    resp.status_code)
            print "Now clicking {0}".format(k)
            href.click()
            WebDriverWait(_browser, 8)
            time.sleep(2)
            WebDriverWait(_browser, 8)
            time.sleep(3)
            print "Page is now {0}".format(getPage())
            print "Returning to start page"
            _browser.back()
            WebDriverWait(_browser, 8)
            time.sleep(3)
            print "Page is now {0}".format(getPage())
            if(urlTranslation[getPage()] != pageName):
                print "Error: Did not return to start page"
                time.sleep(3)
                openPage(None, url)
            else:
                print "Returned to {0}".format(pageName)


@step('Verify checkboxes on (\w+)')
def verifyCheckBoxes(step, pageName):
    """Verifies checkboxes on the user-specified page can be clicked
    """
    
    _browser = world.browser
    url = urlTranslation.keys()[urlTranslation.values().index(pageName)]
    if(pageName != urlTranslation[getPage()]):
        _browser.get(url)

    config = getPageData(pageName)
    for k in config:
        if(config[k][1] == "ckbx"):
            objectWait(k, config[k][0])
            time.sleep(3)
            ckbx1 = _browser.find_element_by_css_selector(config[k][0])
            ckbx1.click()
            time.sleep(2)
            parent = ckbx1.find_element_by_xpath("..")
            if(not(parent.get_attribute('class') == "md-checked")):
                print "Error: Could not select checkbox {0}".format(k)
            else:
                print "Checkbox {0} selected".format(k)
                ckbx1.click()
            time.sleep(3)



@step('Verify images on (\w+)')
def verifyImages(step, pageName):
    """Verifies images on user-specified page have loaded
    """

    _browser = world.browser
    url = urlTranslation.keys()[urlTranslation.values().index(pageName)]
    if(pageName != urlTranslation[getPage()]):
        _browser.get(url)

    config = getPageData(pageName)
    for k in config:
        if(config[k][1] == "img"):
            objectWait(k, config[k][0])
            time.sleep(3)
            image1 = _browser.find_element_by_css_selector(config[k][0])
            testImg = bool(_browser.execute_script(
                "return arguments[0].complete && typeof \
                arguments[0].naturalWidth != \"undefined\" \
                && arguments[0].naturalWidth > 0", image1))

            image1Src = image1.get_attribute("src")
            print "Image source is {0}".format(image1Src)
            myResponse = requests.get(image1Src)
            print "Image response code is {0}".format(myResponse.status_code)

            if(not testImg) and (not myResponse.ok):
                print('Image broken')
            else:
                print('Image not broken')


@step('Verify elements on (\w+)')
def verifyPageElements(step, pageName):
    """Verifies elements of the page from a k:v dict.  Uses Expected 
    Conditions in case object was loaded using AJAX
    """

    _browser = world.browser
    url = urlTranslation.keys()[urlTranslation.values().index(pageName)]
    if(pageName != urlTranslation[getPage()]):
        _browser.get(url)

    config = getPageData(pageName)
    for k in config:
        print "Key: {0}\nValue: {1}\nType: {2}".format(k, 
            config[k][0], config[k][1])
        testObj = config[k][0]
        objectWait(k, testObj)
