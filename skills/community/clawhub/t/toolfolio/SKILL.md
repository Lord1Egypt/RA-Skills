---
name: toolfolio
description: 分析视频文件的运镜方式并生成 AI 视频生成提示词。上传视频后自动检测镜头切分、识别运镜方式（推/拉/摇/移/变焦/环绕/手持等 14 种）、为每个镜头生成英文 AI 生成提示词。Use when: 用户发来视频文件并要求分析运镜、分析镜头、生成提示词、拆镜、或说 "分析这个视频"、"帮我拆镜"、"这个视频用了什么运镜"、"toolfolio"。支持 mp4、avi、mov、mkv、webm 格式。
---

# 视频运镜分析（toolfolio）

## 依赖

```bash
py -m pip install opencv-python-headless numpy pillow
```

## 使用

```bash
py scripts/analyze_shots.py "<视频文件路径>"
```

输出 JSON 到 `output/<视频名>/analysis.json`，含：
- 每个镜头的时间范围、运镜类型、置信度
- AI 生成提示词（英文）
- 缩略图 base64
- 运动数据（X/Y 位移、缩放、抖动）

## 输出示例

```
── 📹 镜头 1 ──
   时间: 00:00:00.0 → 00:00:03.5
   运镜: 推镜头 (Slow push in)
   置信度: 85%
   AI 提示词: Slow push in, 4 second clip
   运动数据: X=-45px, Y=+2px, 缩放=+1.20%, 抖动=5.0%
```
