# SKILL.md — Reddit Archive

_Download and archive Reddit posts (images, GIFs, videos) from users or subreddits._

## Auto-Installation

This script automatically checks for and installs its dependencies on first run:

- **requests** — Python HTTP library
- **yt-dlp** — video downloader

If missing, it will attempt to install them via `pip install --user`. You can also:
- Pre-install: `pip3 install requests yt-dlp`
- Override yt-dlp path: `export YTDLP_PATH=/your/custom/path/yt-dlp`

## Browser Login Required for Reddit Videos

As of mid-2026, downloading `v.redd.it` videos requires an authenticated
Reddit session — yt-dlp's Reddit extractor reads cookies from your
browser to satisfy this. **Stay logged into Reddit in Safari** (or
another browser, see below) and the script handles it automatically.

- Default browser: `safari` (macOS default).
- Override: `export REDDIT_COOKIES_BROWSER=chrome` (or `firefox`,
  `brave`, `edge`, `vivaldi`). Set to `none` to skip cookie loading
  if you don't need Reddit videos.
- Image-only / redgifs-only archives don't need this — the cookie
  loader is harmless if you're not logged in (those URLs won't try to
  use Reddit credentials), but `v.redd.it` posts will fail with an
  `Account authentication is required` error.

## When to Use

You want to archive content from Reddit — either from a specific user (`u/username`) or a subreddit (`r/subname`).

## Usage

```bash
python3 ~/path/to/reddit_archive.py [options]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-u, --user` | Reddit username (either this OR --subreddit required) | — |
| `-s, --subreddit` | Subreddit name (either this OR --user required) | — |
| `-o, --output` | Output directory | `~/temp/.reddit_<target>` |
| `--sort` | Sort order: hot, new, rising, top, controversial | `hot` |
| `--time` | Time filter for top/controversial: hour, day, week, month, year, all | — |
| `--after` | Start date (YYYY-MM-DD) | No filter |
| `--before` | End date (YYYY-MM-DD) | No filter |
| `--limit` | Max posts to fetch (0 = unlimited) | 0 |
| `--images` | Download images (jpg, png, webp) | ✓ |
| `--gifs` | Download GIFs/videos (gfycat, redgifs, imgur) | ✓ |
| `--skip-existing` | Skip already-downloaded files | ✓ |
| `--workers` | Parallel download workers | 4 |

### Examples

```bash
# All posts from a user
python3 reddit_archive.py -u someuser

# Subreddit with date range
python3 reddit_archive.py -s orlando --after 2025-01-01 --before 2025-12-31

# Top 10 most upvoted posts of all time from a subreddit
python3 reddit_archive.py -s funny --sort top --time all --limit 10

# New posts only
python3 reddit_archive.py -s orlando --sort new

# GIFs only, specific user
python3 reddit_archive.py -u someguy --gifs

# Custom output dir
python3 reddit_archive.py -u someuser -o ~/Downloads/reddit_archive
```

## Output

Downloads are saved to the output directory with the following structure:

```
output_directory/
├── Pictures/
│   ├── {target}_{post_id}.jpg
│   ├── {target}_{post_id}.png
│   └── ...
└── Videos/
    ├── {target}_{post_id}.mp4
    └── ...
```

## File Organization

The skill is organized as:

```
reddit-archive/
├── SKILL.md              ← This file
└── scripts/
    ├── reddit_archive.py ← Main downloader script
    └── requirements.txt  ← Python dependencies
```

## Rate Limiting

- Pauses 0.8s between listing-page fetches
- Presents as Safari on macOS (Reddit's anti-bot blocks descriptive bot
  User-Agents in 2026)
- Sets the `over18` cookie so NSFW subreddits don't return an interstitial
- Run one instance at a time — parallel runs trigger rate limits

## Technical Notes

- **Data source**: scrapes old.reddit.com listing HTML
  (`old.reddit.com/r/<name>/<sort>/` or
  `old.reddit.com/user/<name>/submitted/`). Reddit's anonymous JSON API
  started returning 403 + an anti-bot HTML page in mid-2026, and the
  self-serve OAuth flow is gated behind a Responsible Builder Policy
  approval. old.reddit's server-rendered listings still work and embed
  the same metadata in `<div class="thing" data-*>` attributes (schema
  stable since ~2010).
- **Pagination**: uses the `after=t3_<id>` cursor extracted from the
  page's `next ›` button rather than a JSON `after` field.
- **Galleries**: old.reddit embeds `preview.redd.it/<id>.<ext>` URLs
  for each gallery item inline. Each image is also available unsigned at
  `i.redd.it/<id>.<ext>` (full resolution, no expiry), which is what we
  download.
- **v.redd.it videos**: routed through `yt-dlp` with
  `--cookies-from-browser` (HTML scraping doesn't expose the DASH
  manifest URL the way the old JSON API did, and yt-dlp's Reddit
  extractor in 2026 needs an authenticated session to fetch the
  manifest itself).
- **GIF/video downloads** use `yt-dlp` (redgifs, gfycat, v.redd.it);
  direct images and direct mp4/gif URLs are streamed via `requests`.
- **Date filtering** is done client-side after fetching (filters by
  the post's `created_utc`, which we derive from `data-timestamp`).
