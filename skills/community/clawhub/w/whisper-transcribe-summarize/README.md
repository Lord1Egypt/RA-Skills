# whisper-transcribe-summarize

本地语音转文字 + 文本清理 + 整理稿 + 总结稿。全程离线，不依赖外部接口。

## 功能

给一个音频或视频文件，自动输出三份文件：

- **转录文本**（.txt）— 简体、有标点、去重复、修错字
- **整理稿**（.txt）— 将口语重写为流畅的书面文章
- **总结稿**（.md + .html）— 结构化摘要，浏览器可直接查看

## 安装

```bash
openclaw skills install whisper-transcribe-summarize
```

依赖：`python3`、`ffmpeg`、`openai-whisper`

```bash
python3 -m pip install -U openai-whisper
```

## 使用

```
帮我转录并总结这个文件 /路径/视频.mp4
```

支持格式：mp3、wav、m4a、mp4、mov、mkv、webm

默认使用 medium 模型（中文推荐）。

## 隐私

全程本地运行，音频不上传到任何外部服务。
