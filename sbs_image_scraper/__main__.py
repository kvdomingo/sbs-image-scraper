import os
import sys
from multiprocessing import Pool, cpu_count

from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
)
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from .get_image import get_image

NUM_CORES = cpu_count() // 2


def main(board_number: str):
    service = Service(log_path=os.devnull)
    options = Options()
    options.headless = True
    with Firefox(options=options, service=service) as driver:
        url = f"https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no={board_number}"
        logger.info(f"Retrieving URL: {url}...")
        driver.get(url)
        WebDriverWait(driver, 10).until(presence_of_all_elements_located((By.CLASS_NAME, "aba_img")))
        logger.info(f"Scraping page source...")
        html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    images = soup.find_all(attrs={"class": "aba_img"})
    sources = [img.get("src") for img in images]
    logger.info(f"Downloading media...")
    with Pool(processes=NUM_CORES - 1) as pool:
        with tqdm(total=len(sources)) as pbar:
            for _ in pool.imap_unordered(get_image, sources):
                pbar.update()


if __name__ == "__main__":
    if (sys.argv[1:2] or ["-h"])[0] in ["-h", "--help"]:
        print("Usage:\n./sbs_image_scraper [board_no]")
    else:
        main(sys.argv[1])
