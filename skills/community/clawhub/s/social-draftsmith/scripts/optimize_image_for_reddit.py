#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from PIL import Image

TARGET_MAX = 500 * 1024


def main():
    ap = argparse.ArgumentParser(description='Compress/resize image for Reddit upload limit')
    ap.add_argument('source')
    ap.add_argument('--dest', default=None)
    args = ap.parse_args()

    src = Path(args.source)
    dest = Path(args.dest) if args.dest else src.with_name(src.stem + '-reddit.jpg')

    img = Image.open(src).convert('RGB')
    width, height = img.size

    quality = 85
    while True:
        tmp = img.copy()
        if max(width, height) > 1600:
            ratio = 1600 / max(width, height)
            tmp = tmp.resize((int(width * ratio), int(height * ratio)))
        tmp.save(dest, format='JPEG', quality=quality, optimize=True)
        if os.path.getsize(dest) <= TARGET_MAX or quality <= 35:
            break
        quality -= 10

    print(dest)


if __name__ == '__main__':
    main()
