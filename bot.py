"""
selenium based bot to guess countries on geohunter game
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from copy import deepcopy
from time import sleep

from load_rankings import load_rankings

OPTIONS = ['population', 'football', 'small size', 'corruption', 'forest cover', 'basketball', 'pollution', 'cuisine']
TARGET_SCORE = 119  # change this to your desired score the bot tries to achieve
EMAIL = 'uhtanynraohnggjqsd@xfavaj.com'
EMAIL = 'famac18739@agenra.com'
EMAIL = 'k0azfu14@trashlify.com'
PASSWORD = '123123'


def get_best_option(country, dicts, available_options):
    best_option = available_options[0]
    best_rank = 999
    for option in available_options:
        rank = dicts[option].get(country, 100)
        if rank < best_rank:
            best_rank = rank
            best_option = option
    return best_option, best_rank


def run_bot():
    dicts = load_rankings()
    chrome_options = Options()
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/120.0 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(
        driver,
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    url = "https://www.geohuntergame.com/"
    driver.get(url)
    sleep(3)
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'START GAME')]]"))).click()

    # login
    driver.find_element(By.XPATH, "//button[.//span[text()='Join']]").click()
    sleep(0.3)
    driver.find_element(By.ID, "email").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Sign In']").click()
    sleep(3)

    # start game
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,"//button[.//div[normalize-space()='World']]"))).click()
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//button[.//h2[normalize-space()='World']]"))).click()
    sleep(4)
    while True:
        success = game_loop(driver, dicts)
        if success:
            sleep(4)
            restart = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Play Again')]]")
        else:
            restart = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Restart Game']")
        restart.click()
        sleep(4)
        print()

def game_loop(driver, dicts) -> bool:
    available_options = deepcopy(OPTIONS)
    score = 0
    for attempt in range(len(OPTIONS)):
        country = driver.find_element(By.CSS_SELECTOR, "div.legacy-country-name.category-style-country").text.lower()
        best_option, best_rank = get_best_option(country, dicts, available_options)
        best_option = ' '.join([word.capitalize() for word in best_option.split(' ')])
        print(f'{country}: {best_option}, {best_rank}')
        driver.find_element(By.XPATH, f"//div[text()='{best_option}']/ancestor::button").click()
        available_options.remove(best_option.lower())
        score += best_rank
        if attempt != len(OPTIONS) - 1 and (score >= TARGET_SCORE or best_rank > TARGET_SCORE / (len(OPTIONS) - attempt - 2.5)):
            print(f'restart game: {score}')
            return False
        sleep(3.2)
    print(f'finished game: {score}')
    if score <= TARGET_SCORE:
        print('YES!')
        sleep(999)
        exit()
    return True


if __name__ == '__main__':
    run_bot()
