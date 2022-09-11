import os
from pathlib import Path

import requests
from loguru import logger


def get_image(url: str) -> int:
    filename = url.split("/")[-1]
    if (Path(os.getcwd()) / filename).exists():
        return 1
    try:
        res = requests.get(url)
    except requests.exceptions.MissingSchema as e:
        logger.error(str(e))
        return 1
    except Exception as e:
        logger.error(str(e))
        return 1

    if not res.ok:
        logger.error(f"ConnectionError at: {url}")
        return 1

    with open(Path(os.getcwd()) / filename, "wb+") as f:
        for chunk in res.iter_content(chunk_size=1024):
            f.write(chunk)
    return 0
