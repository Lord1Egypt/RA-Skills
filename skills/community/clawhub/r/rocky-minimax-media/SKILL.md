---
name: rocky_minimax_media
description: MiniMax 媒体生成插件 - 图片/视频/TTS/音乐生成，支持交互式选择模型
plugin: true
metadata:
  openclaw:
    type: plugin
    requires:
      models:
        - minimax-portal/MiniMax-M2.7-highspeed
      bins:
        - curl
        - bash
version: 1.3.0
---

# MiniMax 媒体生成插件 v1.3.0

> ⚠️ **前置要求**: 必须先配置 MiniMax API Key

## 安装步骤

### 1. 放置插件
```bash
# 把插件放到 skills 目录
cp -r rocky-minimax-media/ ~/.openclaw/skills/
```

### 2. 添加到 openclaw.json
在 `skills.entries` 中添加：
```json
"rocky-minimax-media": {
  "enabled": true
}
```

### 3. 运行安装脚本（输入 API Key）
```bash
cd ~/.openclaw/skills/rocky-minimax-media/scripts
./install.sh
```
→ 交互式输入 MiniMax API Key
→ 自动写入 openclaw.json

### 4. 重启网关
```bash
openclaw gateway restart
```

## 功能特性

| 功能 | 模型 | 说明 |
|------|------|------|
| 🎨 图片生成 | `image-01` | 交互式输入描述 |
| 🎬 视频生成 | `MiniMax-Hailuo-2.3` / `2.3-Fast` | 用户可选 |
| 🔊 TTS语音 | `speech-2.8-hd` | 3种音色可选 |
| 🎵 音乐生成 | `music-2.6` / `music-2.5` | 用户可选 |

## 前置配置

### 在 OpenClaw 中配置 MiniMax

获取 API Key: https://platform.minimaxi.com/

安装时会自动提示输入，或手动在 `openclaw.json` 添加：

```json
{
  "models": {
    "providers": {
      "minimax-portal": {
        "apiKey": "你的MiniMax API Key",
        "baseUrl": "https://api.minimaxi.com/anthropic",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "MiniMax-M2.7-highspeed",
            "name": "MiniMax-M2.7-highspeed"
          }
        ]
      }
    }
  }
}
```

## 调用方式

插件读取 `~/.openclaw/openclaw.json` 中的 MiniMax 配置。

输出目录可通过环境变量指定：
```bash
MINIMAX_OUTPUT_DIR=/path/to/output ~/.openclaw/skills/rocky-minimax-media/scripts/minimax.sh image
```

## 命令

```bash
./minimax.sh test   # 测试所有API
./minimax.sh image  # 生成图片
./minimax.sh tts    # TTS语音
./minimax.sh video  # 视频生成
./minimax.sh music  # 音乐生成
```

## 交互选项

### 视频模型选择
```
1) MiniMax-Hailuo-2.3        - 文生视频
2) MiniMax-Hailuo-2.3-Fast  - 图生视频
```

### 音乐模型选择
```
1) music-2.6  - 最新版本
2) music-2.5  - 经典版本
```

### TTS音色选择
```
1) male-qn-qingse   - 男声-青年-青涩
2) female-tianmei   - 女声-甜妹
3) female-yujie     - 女声-御姐
```

## API信息

- **API Base URL**: `https://api.minimaxi.com`
- **TTS API**: `POST /v1/t2a_v2`
- **图片API**: `POST /v1/image_generation`
- **视频API**: `POST /v1/video_generation`
- **音乐API**: `POST /v1/music_generation`
