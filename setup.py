import sys
from multiprocessing import freeze_support

from sbs_image_scraper.__main__ import main

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        freeze_support()

    if (sys.argv[1:2] or ["-h"])[0] in ["-h", "--help"]:
        print("Usage:\n./sbs_image_scraper [board_no]")
    else:
        main(sys.argv[1])
