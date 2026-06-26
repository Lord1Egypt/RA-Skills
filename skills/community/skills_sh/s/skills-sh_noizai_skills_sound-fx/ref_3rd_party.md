# Third-Party Integration Reference

Generated sound effect files (WAV/MP3/FLAC) can be sent directly to chat platforms, embedded in videos, or used as audio assets in any downstream workflow.

Recommended flow:

1. Generate the sound effect with `sfx.py` and save to a local file.
2. Upload/send the file via each platform's API.

## 1) Generate a sound effect

```bash
# WAV (default)
python3 skills/sound-fx/scripts/sfx.py "a cat purring" -d 8 -o purr.wav

# MP3 (smaller, more compatible)
python3 skills/sound-fx/scripts/sfx.py "dramatic fail horn" -d 3 --format mp3 -o fail.mp3
```

## 2) Integrate by platform

- **Discord**
  - Send as a regular file attachment via `POST /channels/{channel.id}/messages` with `files[0]=@purr.wav`
  - For a proper "audio player" embed, use Discord's attachment upload flow:
    1. Request attachment slot (`POST /channels/{channel.id}/attachments`)
    2. Upload file to returned `upload_url`
    3. Create message with the attachment metadata
  - Docs:
    - [Uploading Files](https://discord.com/developers/docs/reference#uploading-files)
    - [Create Message](https://discord.com/developers/docs/resources/channel#create-message)

- **Telegram**
  - Send audio clip: `sendAudio` with `audio=@fail.mp3` (shows as playable audio card with title/duration)
  - Send as raw file: `sendDocument` if you just want a downloadable attachment
  - Docs:
    - [sendAudio](https://core.telegram.org/bots/api#sendaudio)
    - [sendDocument](https://core.telegram.org/bots/api#senddocument)

- **Feishu (Lark)**
  - Upload file: `im/v1/files` (`file_type=mp4` for audio files — Feishu treats audio as `mp4` type)
  - Send message: `im/v1/messages` (`msg_type=audio`, include the `file_key` from upload step)
  - Docs:
    - [Upload file](https://open.feishu.cn/document/server-docs/im-v1/file/create)
    - [Send message](https://open.feishu.cn/document/server-docs/im-v1/message/create)

- **Video post-production (ffmpeg)**
  - Mix sound effect into a video:
    ```bash
    ffmpeg -i video.mp4 -i purr.wav -filter_complex "[0:a][1:a]amix=inputs=2:duration=first" output.mp4
    ```
  - Add sound at a specific timestamp (e.g., 3 seconds in):
    ```bash
    ffmpeg -i video.mp4 -i fail.mp3 -filter_complex "[1:a]adelay=3000|3000[sfx];[0:a][sfx]amix=inputs=2:duration=first" output.mp4
    ```

## Notes

- MP3 is the most broadly compatible format for third-party platforms; prefer it over WAV when uploading to chat APIs.
- WAV is lossless and preferred if you plan to further mix or process the audio (e.g., in ffmpeg or a DAW).
- Keep auth/token handling in your integration layer, not in the `sfx.py` script.
