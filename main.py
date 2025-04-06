import time
from playwright.sync_api import sync_playwright

USERNAME = "botx_2025"
PASSWORD = "botx_1"

KEYWORD_RESPONSES = {
    "rules": "Group Rules:\n1. Be respectful.\n2. No spam.\n3. Follow the topic.\n4. Enjoy!",
    "help": "Type 'rules' to see our group rules!"
}

WELCOME_TRIGGERS = ["joined the group", "added to the group"]
WELCOME_MESSAGE = "Hey there! Welcome to the group. Let’s have fun!"

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/")
        time.sleep(5)

        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.press('input[name="password"]', "Enter")
        time.sleep(7)

        page.goto("https://www.instagram.com/direct/inbox/")
        time.sleep(10)

        page.click("text=Group")  # Clicks first group with "Group" in title
        time.sleep(5)

        last_message = ""

        print("Bot is running...")

        while True:
            messages = page.query_selector_all("div._a9zr span")
            if messages:
                current_message = messages[-1].inner_text().strip().lower()

                if current_message != last_message:
                    print("New message:", current_message)

                    for keyword, response in KEYWORD_RESPONSES.items():
                        if keyword in current_message:
                            page.fill("textarea", response)
                            page.press("textarea", "Enter")
                            break

                    for trigger in WELCOME_TRIGGERS:
                        if trigger in current_message:
                            page.fill("textarea", WELCOME_MESSAGE)
                            page.press("textarea", "Enter")
                            break

                    last_message = current_message

            time.sleep(5)

if __name__ == "__main__":
    run_bot()