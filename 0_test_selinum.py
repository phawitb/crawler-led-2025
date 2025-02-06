from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Set up Firefox options
options = webdriver.FirefoxOptions()
# options.add_argument("--headless")  # Run Firefox in headless mode (no GUI)

# Start Firefox browser
driver = webdriver.Firefox(options=options)

try:
    # Open Google
    driver.get("https://www.google.com")

    # Perform a search
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium with Firefox on Ubuntu" + Keys.RETURN)

    # Print the page title
    print("Page title:", driver.title)
finally:
    # Close the browser
    driver.quit()