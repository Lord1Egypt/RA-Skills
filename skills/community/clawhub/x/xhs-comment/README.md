# xhs-comment-scraper

Xiaohongshu (Little Red Book) comment scraper. Send a Xiaohongshu profile URL in chat — the skill automatically scrapes comments from all notes, saves them as JSON files, and generates an HTML analysis report.

## Features

- Auto-scrape comments from all notes on a Xiaohongshu profile
- Fields: author, content, timestamp, likes
- One JSON file per note
- Auto-expand nested replies
- Generate HTML analysis report (word cloud, intent analysis, top words, dual-note comparison)
- Handles Vue dynamic rendering automatically

## Usage

1. Install the skill
2. Send a Xiaohongshu profile URL in chat (e.g. `xiaohongshu.com/user/profile/xxx`)
3. Scan the QR code in the popup Chrome window
4. Wait for scraping to complete — JSON files saved to `Downloads\xhs_comments\`
5. Analysis report saved to `Downloads\xhs_comments_analysis\`

## Platform

- Windows
- Python 3 (optional, for analysis report generation)

## Key Tricks

- Uses built-in Chrome instead of Browser Relay to avoid token issues
- Vue-rendered pages extracted via `innerText`
- Captchas require manual completion by user

## Permissions

Requires browser tool and exec tool.

## License

MIT
