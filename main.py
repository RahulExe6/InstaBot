import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

USERNAME = "botx_2025"
PASSWORD = "botx_201"

KEYWORD_RESPONSES = {
    "rules": "Group Rules:\n1. Be respectful.\n2. No spam.\n3. Follow the topic.\n4. Enjoy!",
    "help": "Type 'rules' to see our group rules!"
}

WELCOME_TRIGGERS = ["joined the group", "added to the group"]
WELCOME_MESSAGE = "Hey there! Welcome to the group. Let’s have fun!"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Login
        driver.get("https://www.instagram.com/")
        time.sleep(7)

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)

        # Go to inbox
        driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(10)

        # Open the group chat
        group = driver.find_elements(By.XPATH, "//div[contains(text(),'Group')]")
        if group:
            group[0].click()
        else:
            print("Group chat not found.")
            return
        time.sleep(6)

        print("Bot is running...")

        last_message = ""

        while True:
            try:
                messages = driver.find_elements(By.CSS_SELECTOR, "div._a9zr span")
                if messages:
                    current_message = messages[-1].text.strip().lower()
                    if current_message != last_message:
                        print("New message:", current_message)

                        for keyword in KEYWORD_RESPONSES:
                            if keyword in current_message:
                                response = KEYWORD_RESPONSES[keyword]
                                message_box = driver.find_element(By.TAG_NAME, "textarea")
                                message_box.send_keys(response)
                                message_box.send_keys(Keys.RETURN)
                                break

                        for trigger in WELCOME_TRIGGERS:
                            if trigger in current_message:
                                message_box = driver.find_element(By.TAG_NAME, "textarea")
                                message_box.send_keys(WELCOME_MESSAGE)
                                message_box.send_keys(Keys.RETURN)
                                break

                        last_message = current_message

                time.sleep(5)
            except Exception as inner_error:
                print("Error inside loop:", inner_error)
                time.sleep(5)

    except Exception as e:
        print("Bot crashed with error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
