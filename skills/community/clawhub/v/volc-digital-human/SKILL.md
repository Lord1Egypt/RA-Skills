---
name: volc-digital-human
description: 火山引擎数字人视频生成技能。当用户发送照片并提供对白或配音文案，要求生成数字人口播视频时触发。全自动完成：图片上传、形象创建、TTS配音（自动性别检测、多音色匹配）、视频合成、最后发回给用户。触发词包括数字人、视频合成、口播视频、数字人视频。
required_env_vars:
  - VOLC_AK
  - VOLC_SK
runtime_dependencies:
  - python3
  - opencv-python (cv2)
  - numpy
  - edge-tts
  - ffmpeg
file_upload_hosts:
  - catbox.moe
  - 0x0.st
---

# Volcengine Digital Human Video Generator

## ⚠️ First-Time Setup Required

This skill requires Volcengine Access Key (AK) and Secret Key (SK).

### Get AK/SK

1. Register Volcengine account: https://console.volcengine.com/
2. Enable "Digital Human Video Generation" service
3. Create Access Key: https://console.volcengine.com/iam/keymanage/

### Configuration (choose one)

**Option 1: Config file (recommended)**

Create `config.json` (in the skill directory):
```json
{
  "ak": "your_access_key_here",
  "sk": "your_secret_key_here"
}
```

**Option 2: Environment variables**

```bash
export VOLC_AK="your_access_key_here"
export VOLC_SK="your_secret_key_here"
```

> ⚠️ **Security**: Never hardcode AK/SK in scripts or commit to public repos!

---

## ⚠️ Privacy Notice

This skill uploads images and generated audio/video to **third-party file hosts** (catbox.moe, 0x0.st) to create publicly accessible URLs required by the Volcengine API.

- **Do not use** with sensitive/private images you don't want uploaded to public hosts
- User images and generated content will be publicly accessible during the video generation process
- Download and use videos promptly; URLs may expire

---

## Core Flow

1. **Get image**: Fetch from `/root/.openclaw/media/inbound/`
2. **Gender detection**: OpenCV Haar cascade for eyes/nose features
3. **Upload image**: Upload to catbox.moe for public URL
4. **Create avatar**: Call `realman_avatar_picture_create_role` API
5. **TTS audio**: Auto-match voice by gender + edge-tts → upload to catbox.moe
6. **Video synthesis**: Call `realman_avatar_picture_v2` API, poll for result
7. **Download video**: Save locally, generate thumbnail preview
8. **Deliver**: Send thumbnail + video via `message` tool

## Quick Run

```bash
cd /root/.openclaw/workspace-employee-xiaozhua
python3 skills/volc-digital-human/scripts/volc_digital_human.py "$image_path" "$dialog_text" [gender]
```

Parameters:
- `image_path`: Image path, None=auto-fetch latest image
- `dialog_text`: Script/dialog content
- `gender`: Optional, `male`|`female`|None (auto-detect)

## Voice Matching Rules

| Detected Gender | Human Voice | Cartoon Voice |
|----------------|-------------|---------------|
| female | `zh-CN-XiaoxiaoNeural` (natural female) | `zh-CN-XiaoyiNeural` (lively female) |
| male | `zh-CN-YunxiNeural` (sunny male) | `zh-CN-YunxiaNeural` (cute male) |
| unknown | `zh-CN-XiaoxiaoNeural` (default female) | `zh-CN-XiaoyiNeural` |

**Manual override**:
- Say "male"/"男生"/"男的" → force male voice
- Say "female"/"女生"/"女的" → force female voice
- Say "cartoon"/"卡通角色"/"动物" → use cartoon voice

## Detailed API Reference

See `references/volc_api.md`

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `image_url` | Public URL (required), uploaded to file host |
| `audio_url` | Public URL for audio MP3 (required) |
| `resource_id` | Avatar ID returned after creation, can be reused |
| `req_key` | create=`realman_avatar_picture_create_role`, synthesize=`realman_avatar_picture_v2` |

## Notes

- **Image tips**: Closed-mouth photos work better; WeChat thumbnails also work
- **Gender detection**: Heuristic based on Haar eye/nose features, not 100% accurate; confirm with user if needed
- **Cartoon/animal**: Use lively female voice `zh-CN-XiaoyiNeural` as default
- **Video URL expiry**: ~1 hour, download promptly
- **Generation time**: Usually 30 sec ~ 3 min
- **Rate limit**: Volcengine has request frequency limits; wait 1-5 min if 50430 error
- **TTS**: edge-tts (Microsoft free), no API key needed

## Error Handling

| Error Code | Meaning | Solution |
|------------|---------|----------|
| `50430` | Rate limit | Wait 1-5 min, retry |
| `50207` | Image decode error | Use jpg/png format |
| `401` | AK/SK error | Check credentials |
