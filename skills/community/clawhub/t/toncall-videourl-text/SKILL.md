---
name: toncall-videourl-text
description: 唐潮Toncall工作室开发 - 视频URL语音转文字。支持任意可直接访问的视频URL，自动下载视频、提取音频、上传火山引擎TOS、调用火山引擎语音识别API识别文字，完成后自动清理本地和TOS的临时文件。使用：当用户发送视频URL并要求提取视频文案、语音转文字、转文字时直接执行；当用户只发送视频URL没有说明意图时，先询问用户是否需要提取视频文案。
---

# 视频URL转文字

> **唐潮Toncall工作室开发**

## 功能

用户发送可直接访问的视频URL后，自动完成全流程处理：

1. **下载视频** - 下载视频到本地临时目录
2. **提取音频** - 使用 ffmpeg 从视频中提取音频为 mp3
3. **上传TOS** - 上传音频到火山引擎对象存储TOS，供语音识别API访问
4. **语音识别** - 调用火山引擎大模型录音文件识别API进行语音转文字
5. **保存结果** - 保存识别结果文本到 `texts/` 目录，返回给用户
6. **自动清理** - 无论成功失败，都自动清理：
   - 本地下载的视频文件
   - 本地提取的音频文件
   - TOS对象存储上已上传的音频文件

## 配置

使用前必须配置，复制 `config.example.ini` 为 `config.ini`，然后填写你的凭证：

```ini
[tos]
ak = 你的火山引擎TOS Access Key
sk = 你的火山引擎TOS Secret Key
region = cn-beijing
bucket = 你的TOS存储桶名称
bucket_domain = 你的TOS存储桶域名，例如 your-bucket.tos-cn-beijing.volces.com

[asr]
app_key = 你的火山引擎语音识别App Key
access_key = 你的火山引擎语音识别Access Key
```

**获取方式：**
- TOS凭证：火山引擎控制台 → 对象存储TOS
- 语音识别凭证：火山引擎控制台 → 语音识别

## 使用方式

1. 用户发送**可直接访问的视频文件URL**
2. Skill 触发后**立刻回复**用户：`识别到视频URL，开始自动处理，请稍候...`
3. 执行脚本自动处理
4. 识别完成后返回结果文本给用户

**命令调用：**
```
py scripts/video_url_to_text.py <视频URL>
```

## 依赖

- Python 3.8+
- `requests` 库
- `ffmpeg` 已安装并添加到系统 PATH

**启动时自动检查：** 脚本启动会自动检查 `requests` 和 `ffmpeg`，如果未安装会提示用户安装，不需要手动检查。

## 文件结构

```
toncall-videourl-text/
├── SKILL.md
├── config.ini.example
└── scripts/
    └── video_url_to_text.py
```

- `config.ini` - 用户配置（需要用户创建）
- `scripts/video_url_to_text.py` - 主程序，独立完整，无需依赖其他文件
