---
name: youtube-summarizer-bot
description: A Python bot that monitors YouTube channels via RSS, summarizes new videos using Google Gemini AI (with audio fallback for videos without subtitles), and sends bilingual (Chinese + English) summaries to a Telegram chat daily.
---

# YouTube 每日视频总结 Telegram 机器人

This skill deploys a YouTube monitoring bot that:
1. Polls configured YouTube channels via RSS feed (no API key needed for this step)
2. Extracts video transcripts using `youtube-transcript-api`
3. Falls back to audio download via `yt-dlp` if no subtitles are available
4. Summarizes content using Google Gemini 2.5 Flash (supports both text and audio input natively)
5. Sends a beautifully formatted bilingual (Chinese + English) summary to Telegram

## Prerequisites

You need these three secrets configured in your environment:
- `GEMINI_API_KEY` — from Google AI Studio
- `TG_BOT_TOKEN` — from Telegram @BotFather
- `TG_CHAT_ID` — your personal or group Telegram chat ID

## File Structure

| File | Purpose |
|------|---------|
| `config.py` | All configuration, API keys, and YouTube channel settings |
| `youtube_monitor.py` | RSS polling and local deduplication via `db.json` |
| `extractor.py` | Transcript fetching or audio download fallback |
| `ai_summarizer.py` | Gemini API integration (text + audio) |
| `tg_notifier.py` | Telegram message delivery with chunking |
| `main.py` | Main entry point with daily 8:00 AM scheduling |
| `requirements.txt` | All Python dependencies |

## Setup & Usage

### Step 1: Configure channels and secrets
Edit `config.py` and add your API keys and the YouTube Channel IDs you want to monitor:
```python
YOUTUBE_CHANNELS = {
    "UCxxxxxxxxxxxxxxxxxxxxxx": "Channel Name Here"
}
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run
For a one-off immediate check:
```bash
python main.py
```

For long-running background mode (runs daily at 8 AM Izmir time):
```bash
nohup python main.py > bot.log 2>&1 &
```

## How to Find a YouTube Channel ID

1. Go to the YouTube channel page
2. Click the channel name, then go to About
3. Click "Share Channel" and copy the link — the ID starts with `UC...`
4. Or use [commentpicker.com/youtube-channel-id.php](https://commentpicker.com/youtube-channel-id.php)

## Notes

- The bot tracks processed videos in `db.json` so it never sends duplicate summaries
- If Gemini API is not configured, the bot will fail gracefully with a clear error message
- Long videos with audio fallback may take 1–2 minutes to upload and process
