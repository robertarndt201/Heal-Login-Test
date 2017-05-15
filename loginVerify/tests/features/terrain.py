from lettuce import before, after, world
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@before.all  
def open_browser():  
    
    desired_cap = {
        'platform': "Linux",
        'browserName': "chrome",
        'version': "latest",
        'screenResolution': "1024x768",
        'browserConnectionEnabled': "true"
    }


    world.browser = webdriver.Remote(
        command_executor="http://robertarndt201:8e01dc39-65bd-480f-8720-3aebcd5be036@ondemand.saucelabs.com:80/wd/hub",
        desired_capabilities=desired_cap
    )


@after.all
def tearDown(self):
    world.browser.quit()

