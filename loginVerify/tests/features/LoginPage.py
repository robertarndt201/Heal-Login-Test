# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import requests
import base64
from Crypto.Cipher import AES
from Crypto import Random
from lettuce import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import steps

@step('Enter credentials from PW file')
def enterCredentials(step):
    """Enters user credentials to log into patient site
    """

    _browser = world.browser
    pageName = "LoginPage"
    config = steps.getPageData(pageName)

    steps.objectWait("usernameField", config['usernameField'][0])
    userFld = _browser.find_element_by_css_selector(config['usernameField'][0])
    loginKeys = steps.getPageData("User")
    userFld.send_keys(decrypt(loginKeys['us'], "Dictionary"))
    pwFld = _browser.find_element_by_css_selector(config['passwordField'][0])
    pwFld.send_keys(decrypt(loginKeys['pa'], "Dictionary"))

    logInBtn = _browser.find_element_by_css_selector(config["loginBtn"][0])
    logInBtn.click()
    wait = WebDriverWait(_browser, 10)
    time.sleep(3)
    assert(steps.urlTranslation[steps.getPage()] == "BookVisitPage")
        
    pageName = "BookVisitPage"
    config = steps.getPageData(pageName)

    steps.objectWait("noEmergencyBtn", config["noEmergencyBtn"][0])
    assert(steps.urlTranslation[steps.getPage()] == "BookVisitPage")
    noEmergencyBtn = _browser.find_element_by_css_selector(
        config['noEmergencyBtn'][0])
    noEmergencyBtn.click()
    time.sleep(8)


def encrypt(raw, key):
    """Ecrypts raw phrase using a given key
    """
    
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    raw = pad(raw)
    key = pad(key)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, key):
    """Decrypts an encoded phrase using a given key
    """
    
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    key = pad(key)
    unpad = lambda s : s[:-ord(s[len(s)-1:])]
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt(enc[16:]))
