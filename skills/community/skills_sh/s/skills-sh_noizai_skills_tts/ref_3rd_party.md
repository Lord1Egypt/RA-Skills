# Third-Party Voice Delivery Reference

This skill now keeps third-party integration outside `tts.sh`.

Recommended flow:

1. Use `tts.sh speak` to generate voice audio in `opus` (or `ogg` alias).
2. Upload/send the generated file with each platform's official API.

## 1) Generate voice audio

```bash
# Opus output
bash skills/tts/scripts/tts.sh speak -t "Hello world" --format opus -o voice.opus

```

## 2) Integrate by platform

- **Feishu (Lark)**
  - Upload file: `im/v1/files` (`file_type=opus`)
  - Send message: `im/v1/messages` (`msg_type=audio`)
  - Docs:
    - [Upload file](https://open.feishu.cn/document/server-docs/im-v1/file/create)
    - [Send message](https://open.feishu.cn/document/server-docs/im-v1/message/create)

- **Telegram**
  - Send voice directly via `sendVoice` with multipart `voice=@voice.opus` (or `.ogg`)
  - Docs:
    - [sendVoice](https://core.telegram.org/bots/api#sendvoice)

- **Discord**
  - Voice message flow:
    1. Request attachment slot (`POST /channels/{channel.id}/attachments`)
    2. Upload file to returned `upload_url`
    3. Create message with voice flags/attachment metadata (`POST /channels/{channel.id}/messages`)
  - Docs:
    - [Uploading Files](https://discord.com/developers/docs/reference#uploading-files)
    - [Create Message](https://discord.com/developers/docs/resources/channel#create-message)

## Notes

- If your downstream API requires `audio/ogg`, you can still send the `opus`-encoded output file with MIME `audio/ogg`.
- Keep auth/token handling in your integration layer (service, bot, workflow tool), not in the core TTS script.
