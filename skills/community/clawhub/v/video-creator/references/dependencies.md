<!--
 * @Author: zhoujianping zhoujianping@delilegal.com
 * @Date: 2026-06-02 07:07:56
 * @LastEditors: zhoujianping zhoujianping@delilegal.com
 * @LastEditTime: 2026-06-04 14:09:07
 * @FilePath: /video-creator/references/dependencies.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 依赖安装说明

## Python 依赖

```bash
pip install edge-tts pillow httpx dashscope
```

| 包名 | 用途 | 必须 |
| ------ | ------ | ------ |
| edge-tts | 免费微软TTS引擎 | 是（默认方案） |
| pillow | 图像格式转换 | 是 |
| httpx | 调用阿里百炼声音复刻接口 | 仅执行声音复刻时 |
| dashscope | 阿里百炼语音合成 SDK | 仅用我的声音时 |

## 系统依赖：ffmpeg

视频合成的核心工具，必须安装。

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt update && sudo apt install ffmpeg

# CentOS / RHEL
sudo yum install epel-release && sudo yum install ffmpeg

# Windows
# 下载：https://ffmpeg.org/download.html
# 解压后将 bin 目录加入 PATH
```

## voice_config.json 配置（可选）

仅在需要使用自有平台服务（声音复刻、文生图、口播视频）时配置。

将以下文件保存为项目根目录的 `voice_config.json`：

```json
{
  "Voice-id": "复刻声音成功后保存的voice-id"
}
```

## 声音复刻（自有平台 SkillController）

### 方式A：你已有公网 URL

先将符合要求的音频上传到公网可访问地址（例如 OSS），再执行：

```bash
/usr/local/bin/python3 scripts/enroll_my_voice.py \
  --audio-url "https://your-public-audio-url" \
  --prefix "myvoice" \
  --language zh
```

### 方式B：直接传本地文件（自动转换为 data URI）

直接执行：

```bash
/usr/local/bin/python3 scripts/enroll_my_voice.py \
  --audio-file "/absolute/path/to/your_voice_sample.wav" \
  --prefix "myvoice" \
  --language zh
```

voice_id 复刻成功后写入配置文件。

若不配置，系统会自动使用 edge-tts（完全免费）。

## 支持的图片格式

JPG、JPEG、PNG、WEBP、BMP

建议使用 16:9（1920×1080）或 9:16（1080×1920）比例的图片以获得最佳效果。
