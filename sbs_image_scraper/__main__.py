import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
)
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


def main(board_number: int):
    options = Options()
    options.headless = True
    driver = Firefox(options=options, log_path=os.devnull, service_log_path=os.devnull)
    driver.get(f"https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no={board_number}")
    try:
        WebDriverWait(driver, 10).until(presence_of_all_elements_located((By.CLASS_NAME, "aba_img")))
    finally:
        html = driver.page_source
        driver.close()
    soup = BeautifulSoup(html, "lxml")
    images = soup.find_all(attrs={"class": "aba_img"})
    sources = [img.get("src") for img in images]
    for src in tqdm(sources):
        filename = src.split("/")[-1]
        if (Path(os.getcwd()) / filename).exists():
            continue

        try:
            res = requests.get(src)
        except requests.exceptions.MissingSchema as e:
            logger.error(str(e))
            continue
        except Exception as e:
            logger.error(str(e))
            continue

        if not res.ok:
            logger.error(f"ConnectionError at: {src}")
            continue

        with open(Path(os.getcwd()) / filename, "wb+") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)


if __name__ == "__main__":
    if (sys.argv[1:2] or ["-h"])[0] in ["-h", "--help"]:
        print("Usage:\n./sbs_image_scraper [board_no]")
    else:
        main(int(sys.argv[1]))
