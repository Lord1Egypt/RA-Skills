# Telegram Bot API File Sending Reference

## File Size Limits

- **Maximum**: 2GB per file
- **Bot mode**: 2GB (Telegram Premium users get higher limits in some cases)
- **URL mode**: Recommended under 20MB for reliability

## Supported File Types

### Documents
- PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, RTF, ODT
- ZIP, RAR, 7Z, TAR, GZ
- APK (may be blocked by Telegram for security)

### Images
- PNG, JPG, JPEG, GIF, WEBP, BMP, SVG
- Maximum: 10MB for compression

### Audio
- MP3, OGG (Opus), WAV, M4A, FLAC

### Video
- MP4, AVI, MOV, MKV, WEBM
- Maximum: 2GB (64MB for some formats)

## API Methods

Note: python-telegram-bot v20+ uses async API. Use `await` or wrap with `asyncio.run()`.

### sendDocument
```python
import asyncio
from telegram import Bot

async def main():
    bot = Bot(token="TOKEN")
    with open("file.pdf", "rb") as f:
        result = await bot.send_document(
            chat_id=chat_id,
            document=f,
            caption="Optional caption",
            parse_mode="HTML",  # or "Markdown"
        )
    print(result["document"]["file_id"])

asyncio.run(main())
```

### sendPhoto
```python
result = await bot.send_photo(
    chat_id=chat_id,
    photo=open("photo.jpg", "rb"),
    caption="Optional caption",
    parse_mode="HTML",
    has_spoiler=True,  # Blur sensitive content
)
```

### sendVideo
```python
result = await bot.send_video(
    chat_id=chat_id,
    video=open("video.mp4", "rb"),
    caption="Optional caption",
    parse_mode="HTML",
    duration=120,
    width=1920,
    height=1080,
    supports_streaming=True,
)
```

### sendAudio
```python
result = await bot.send_audio(
    chat_id=chat_id,
    audio=open("audio.mp3", "rb"),
    caption="Optional caption",
    parse_mode="HTML",
    duration=180,
    performer="Artist",
    title="Song Title",
)
```

### sendVoice
```python
result = await bot.send_voice(
    chat_id=chat_id,
    voice=open("voice.ogg", "rb"),
    caption="Optional caption",
    parse_mode="HTML",
    duration=30,
)
```

## Parse Modes

### HTML
```python
result = await bot.send_message(
    chat_id=chat_id,
    text="<b>Bold</b> <i>Italic</i> <code>Code</code> <a href='https://example.com'>Link</a>",
    parse_mode="HTML"
)
```

### MarkdownV2
```python
result = await bot.send_message(
    chat_id=chat_id,
    text=r"\*Bold\* \_Italic\_ \`Code\` \[Link\](https://example.com)",
    parse_mode="MarkdownV2"
)
```

## File ID

Once a file is sent, Telegram assigns a permanent `file_id`. You can forward this file without re-uploading:

```python
result = await bot.send_document(
    chat_id=chat_id,
    document="AQADABJDKDGkXZvwAAAD"  # Permanent file_id
)
```

Note: File IDs are bound to the bot that received them. You cannot use a file_id from another bot.

## Best Practices

1. **Reuse file_ids**: Store file_ids to avoid re-uploading
2. **Compress large files**: Use gzip/zip for large documents
3. **Set proper mime_type**: Helps Telegram display correctly
4. **Handle errors**: Network issues may require retry logic

## Error Handling

```python
import asyncio
from telegram import Bot
from telegram.error import TelegramError, BadRequest, NetworkError

async def main():
    bot = Bot(token="TOKEN")
    try:
        await bot.send_document(chat_id=chat_id, document=open("file.pdf", "rb"))
    except BadRequest as e:
        # Invalid file or request
        print(f"Bad request: {e}")
    except NetworkError as e:
        # Network issues - retry
        print(f"Network error: {e}")
    except TelegramError as e:
        # Other errors
        print(f"Telegram error: {e}")

asyncio.run(main())
```
