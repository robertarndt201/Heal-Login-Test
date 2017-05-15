# Heal-Login-Test
Some basic tests on the Heal.com patient portal

Environment:  Linux Mint 17.3 64-bit

Dependencies:
  -Python 2.7
  -sudo apt-get install python-selenium
  -Download ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
  (might just be able to install via sudo apt-get install chromium-chromedriver)
  -pip install selenium
  -pip install lettuce_webdriver
  -pip install nose
  -pip install requests
  -pip install Crypto
  -Sauce Labs account for automated cloud testing (I used the 14-day free trial)
  
Description:
  For this task I developed a basic skeleton of an automation testing framework using the Lettuce package for Python.   
  Lettuce is the Python version of Ruby's Cucumber, providing non-technical users a way to create automated tests simply by     writing natural phrases expressing test actions.  These phrases activate snippets (functions) of Python code called Steps.   A feature is made up of steps.  A test scenario contains a feature or features to test.  A scenario is nicely contained in   a single directory.
  
  Each function logs it's activity as it iterates over elements or accesses a page, checking element presence based on a JSON   object storage file, verifying links or checkbox functionality, or making sure an image loaded.  Because Selenium does not   provide a way to get http responses, the requests module was imported (works well).  Once I took the design farther, there   would be a module for each major type of page (e.g. login with credentials page/access pulldown page/book visit page, etc)   while keeping common functions in the steps.py file.  Lettuce iterates over all Python files in the features directory, so   you just have to use the @step decorator to identify functions corresponding to behaviors in the .feature file (where the     natural phrases are written out that correspond to a @step.
  
  Object detection was done using AJAX-style explicit waits, but waits with time constants were also used to slow execution     to a more natural speed mimicking a real user (very important).
  
What I Would Add With More Time:
  -More pageObjects
  -Possibly format unit testing (but I prefer not to have the program end on a single failed assertion sometimes)
  -Text field validation with a negative-path approach, using improper characters and trying to break the form in various        ways
  -Pulldown menu testing
  -Much more

Execution:
  -Clone loginVerify directory after installing dependencies
  -Make sure you're connected to the internet to reach Sauce Labs
  -From loginVerify/tests directory, run "lettuce -v4".  The -v is verbosity level.
  -Output can be saved with "lettuce -v4 | tee [output file]"
  -Lettuce allows easy conversion of output to XML using subunit package, but probably manual print statements would need to    go into a separate logfile first
  
Bugs Found:
  -Invalid characters in the patient login aren't reported, just tells user that username/password don't match
  -Takes two attempts hitting the back button (in Chrome) to go back from Forgot Password page
  -Subpages two levels deep like http://www.heal.com/blah/blah show an undeveloped page with broken images
  
Conclusion:
  Lettuce is very powerful, and was easy to setup with Sauce Labs' concurrent automated cloud testing.  BDD gives test         creation to any business unit that understands the basics of writing out a test.  The framework is scalable thanks to its     inclusion of Regex for passing parameters through the behavior phrases.  Tons of possibilities, helps tester hit the ground   running.
