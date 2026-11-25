#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261125.

Copies the finished front-page image (entry.png, built in this repository
by build_image.py) to /output/entry.png.

No network. Fully deterministic: the same bytes are written on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    try:
        os.chmod("/output", 0o755)
    except OSError:
        pass
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)


if __name__ == "__main__":
    main()
