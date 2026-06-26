# Anime Image Downloader (Safebooru, download-only)

Platform-agnostic **anime / 二次元 image downloader** powered by Safebooru (booru).

## What it does / does not do

- ✅ Tag-based “image search” → extract original image URLs → download files to local disk
- ❌ Does **not** send/upload/post images to QQ/Discord/Feishu/etc.

## Features

- Download high-quality **original** images
- Tag-based search (single or multiple tags)
- Uses Safebooru **DAPI JSON** (no browser automation, no external CLI)

## Requirements

- Python 3
- `pip install -r requirements.txt`

## Usage

### Download

```bash
python3 safebooru.py "genshin_impact maid" 5 --sort score_desc --min-score 5
python3 safebooru.py "blue_archive shiroko" 10 --page 2 --sort id_desc
python3 safebooru.py "cat_girl solo" 5 --sort random
```

### Tag suggestions

```bash
python3 safebooru.py --suggest genshin
```

## Output

The script prints the downloaded file paths and the output directory.
By default, images are saved under `./downloads/` (relative to the skill folder).

## Common tags (short list)

- Quality/format: `wallpaper`, `portrait`, `full_body`, `solo`
- Outfits: `maid`, `school_uniform`, `swimsuit`
- Cute: `cat_girl`, `nekomimi`
- Exclude: `-comic`, `-greyscale`

Tip: `python3 safebooru.py --suggest <keyword>` to discover more tags.

## Keywords (discoverability)

anime, 二次元, wallpaper, waifu, catgirl, booru, safebooru, tag search, image downloader
