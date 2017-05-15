Feature: Test Heal Login
    In order to log into Heal
    We'll use Robert's login
    And confirm arrival and button presence on the homepage

    Scenario:  Verify Heal Login
        Open webpage http://patient.heal.com/login in Chrome
        Verify elements on LoginPage
        Verify checkboxes on LoginPage
        Test hyperlinks on LoginPage
        Enter credentials from PW file
        Verify elements on BookVisitPage
        Verify images on BookVisitPage
