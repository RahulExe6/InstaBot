import time
from playwright.sync_api import sync_playwright

USERNAME = "botx_2025"
PASSWORD = "botx_201"

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

        # Go to Instagram
        page.goto("https://www.instagram.com/")
        page.wait_for_selector("input[name='username']", timeout=20000)

        # Login
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.press('input[name="password"]', "Enter")
        page.wait_for_timeout(10000)

        # Go to DMs
        page.goto("https://www.instagram.com/direct/inbox/")
        page.wait_for_timeout(10000)

        # Click the pinned group (change if you want to select by name)
        try:
            group_chat = page.query_selector("text=Group")
            if group_chat:
                group_chat.click()
                page.wait_for_timeout(5000)
            else:
                print("Group not found!")
                return
        except Exception as e:
            print("Could not open group:", e)
            return

        print("Bot is running...")

        last_message = ""

        while True:
            try:
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

            except Exception as e:
                print("Error inside loop:", e)
                time.sleep(5)

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print("Bot crashed with error:", e)
