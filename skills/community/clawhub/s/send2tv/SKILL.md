---
name: send2tv
description: "Push text messages, images, or audio to Huawei Smart Screen via DLNA/UPnP. Use when user wants to display something on TV or play audio/TTS on TV. Triggers: send to TV, push to TV, display on TV, 电视上显示, 发到电视, 推送到电视, 电视播放, 语音播报."
---

# send2tv

Push text, images, or audio to Huawei Smart Screen V75 (or other DLNA-compatible TVs) via UPnP AVTransport protocol.

## Quick Usage

```bash
# Text (Chinese supported)
python3 scripts/send2tv.py "快去写作业！"

# Text with custom font size
python3 scripts/send2tv.py "Warning!" --font-size 300

# Image file
python3 scripts/send2tv.py --image /path/to/photo.jpg

# Image with text overlay
python3 scripts/send2tv.py --image /path/to/photo.jpg --text "Hello!"

# Audio file
python3 scripts/send2tv.py --audio /path/to/music.mp3

# TTS - Text to speech (requires edge-tts skill)
python3 scripts/send2tv.py --tts "这是一段要朗读的文字"
python3 scripts/send2tv.py --tts "Hello world" --voice en-US-MichelleNeural
python3 scripts/send2tv.py --tts "快点！" --rate +20%
```

## How It Works

**Image/Text mode:**
1. Renders text to 1920x1080 black image (or serves image directly)
2. Starts local HTTP server on port 8082
3. Sends DLNA/UPnP SOAP SetAVTransportURI + Play commands to TV
4. TV downloads image via HTTP and displays it

**Audio mode:**
1. Prepares audio file (converts to MP3 if needed)
2. Starts local HTTP server on port 8082
3. Sends DLNA/UPnP SOAP commands to TV
4. TV streams audio via HTTP and plays it

**TTS mode:**
1. Uses edge-tts to convert text to speech
2. Pushes audio to TV via DLNA

## TV Configuration

- **IP**: 192.168.3.252
- **UPnP Port**: 25826
- **HTTP Server Port**: 8082
- **UPnP Service**: urn:schemas-upnp-org:service:AVTransport:1

## Font Notes

- Chinese text uses WenQuanYi Zen Hei (文泉驿正黑), auto-detected
- English text uses DejaVu Sans Bold
- Font auto-scales to fit 1920x1080 (90% width max)

## TTS Voices (for --tts mode)

**Chinese:**
- `zh-CN-XiaoxiaoNeural` - female, natural (default)
- `zh-CN-YunyangNeural` - male, natural
- `zh-CN-XiaoyiNeural` - female, sweet
- `zh-CN-YunjianNeural` - male, mature

**English:**
- `en-US-MichelleNeural` - female, natural
- `en-US-AriaNeural` - female, natural
- `en-US-GuyNeural` - male, natural

See full list: https://speech.microsoft.com/portal/voicegallery

## Troubleshooting

**TV转圈不显示**: 端口8082被防火墙拦。需要在Windows防火墙添加入站规则允许8080-8090端口。

**文字太小/太大**: 用 `--font-size` 调整，默认200像素。

**图片推送失败**: 确认图片路径存在且为有效图片文件。

**音频不播放**: 确认电视支持MP3格式，检查DLNA服务是否开启。

**TTS失败**: 确认已安装 edge-tts skill (`skillhub install openclaw/skills/edge-tts`)
