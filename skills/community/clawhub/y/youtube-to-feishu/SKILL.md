---
name: youtube-to-feishu
description: Download YouTube video audio and upload to Feishu cloud storage
version: 1.0.0
user-invocable: true
disable-model-invocation: false
command-dispatch: tool
command-tool: youtube_upload
command-arg-mode: raw
metadata: {"openclaw":{"emoji":"🎵","primaryEnv":"FEISHU_USER_ID","requires":{"bins":["python","yt-dlp"],"env":["FEISHU_USER_ID"],"os":["win32","darwin","linux"]}}}
---

# YouTube to Feishu Audio Upload

## What it does
Downloads audio from YouTube video and uploads to Feishu cloud storage, then sends file link to user's Feishu chat.

## Usage Examples

- "Download this YouTube video audio and send to my Feishu: https://www.youtube.com/watch?v=dyJUscv7b9g"
- "Convert YouTube to MP3 and upload to Feishu: <URL>"
- "Save this YouTube audio to Feishu cloud: <URL>"

## Workflow

1. **Extract video info** - Fetch YouTube video title, duration, thumbnail
2. **Download audio** - Use yt-dlp to extract and convert to MP3
3. **Upload to Feishu** - Upload file to Feishu cloud drive
4. **Send to user** - Send interactive card with download link to Feishu chat
5. **Cleanup** - Remove temporary local files

## Tools

### youtube_upload — Download and upload YouTube audio

When user sends a YouTube URL:

1. **Parse URL** - Extract video ID from YouTube URL
2. **Download** - Use yt-dlp to download audio as MP3
3. **Upload** - Upload to Feishu cloud drive via feishu_drive_file
4. **Send** - Send interactive card to user via feishu_im_user_message
5. **Report** - Return file info and links

## Output Format

For each upload, return:
- Video title
- Audio file size
- Duration (if available)
- Feishu cloud file link
- Feishu message card

## Dependencies

- **yt-dlp** - YouTube download tool (`pip install yt-dlp`)
- **Python 3.8+**
- **Feishu OAuth** - User authorization for cloud drive and IM

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `FEISHU_USER_ID` | User's Feishu open_id | Required |
| `TEMP_DIR` | Temporary download directory | `./temp` |

## Guardrails

- Only download from YouTube (validate URL)
- Respect copyright - warn user about downloaded content usage
- Auto-cleanup temp files after upload
- Max file size: 100MB (Feishu limit)
- Report errors honestly if download/upload fails

## Example Flow

```
User: Download this to Feishu: https://www.youtube.com/watch?v=dyJUscv7b9g

Bot: [1/4] Extracting video info...
Bot: [2/4] Downloading audio (MP3, 17.5MB)...
Bot: [3/4] Uploading to Feishu cloud...
Bot: [4/4] Sending to your Feishu chat...
Bot: ✅ Done! File sent to your Feishu.
```
