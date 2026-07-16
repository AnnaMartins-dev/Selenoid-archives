from urllib.parse import quote

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from generic_options import add_selenoid_options





def main() -> None:
    options = webdriver.ChromeOptions()

    options = add_selenoid_options(
        options,
        session_name="Simple Selenoid Test",
        enable_vnc=True,
        enable_log=True,
        enable_video=False,
        page_load_strategy="none",
    )

    driver = None

    try:
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options,
        )

        html = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Selenoid Test</title>
            </head>
            <body>
                <h1 id="status">Selenoid is working</h1>
                <button id="test-button">Test button</button>
            </body>
        </html>
        """

        driver.get(f"data:text/html;charset=utf-8,{quote(html)}")

        status = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "status"))
        )

        assert status.text == "Selenoid is working"

        print("Selenoid test completed successfully.")
        print(f"Page title: {driver.title}")
        print(f"Text found: {status.text}")
        print(f"Session ID: {driver.session_id}")
        time.sleep(10)

    finally:
        if driver is not None:
            driver.quit()
            print("WebDriver session closed.")


if __name__ == "__main__":
    main()