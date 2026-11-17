# video-analyzer

视频分析处理 — 本地视频反编译分析工具

## 快速开始

### 安装

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 安装 ffmpeg（必须）
# Windows: scoop install ffmpeg  أو  choco install ffmpeg
# macOS: brew install ffmpeg
# Ubuntu/Debian: sudo apt install ffmpeg

# 3. 验证安装
ffmpeg -version
```

### 使用

```bash
# 最简用法 — 自动检测硬件、自动选择模型
python main.py -i video.mp4

# 完整参数
python main.py -i video.mp4 -o ./report --model medium --lang zh

# 低配电脑 — 限制资源
python main.py -i video.mp4 --max-memory 4 --no-visual

# 仅语音转文字（最快）
python main.py -i video.mp4 --no-visual --no-ocr
```

## 常见问题

**Q: 模型下载慢怎么办？**
设置 pip 镜像：
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: 下载在线视频失败？**
工具已内置 3 次自动重试。如果仍然失败，请确认 URL 可访问；YouTube/B站等需安装 yt-dlp：`pip install yt-dlp`

**Q: 处理时电脑变卡？**
加 `--nice 15 --max-memory 4`，工具会自动降低优先级并限制内存。

**Q: 语音识别结果是空白？**
可能是音频编码不兼容，先用 ffmpeg 手动转码：
```bash
ffmpeg -i input.mp4 -vn -ar 16000 -ac 1 output.wav
```
然后用 `--input output.wav --no-visual` 重新分析。

## 输出

```
output/
├── report.html      # 交互式报告（用浏览器打开）
├── data.json        # 结构化数据
├── script.md        # Markdown 剧本
└── scenes/          # 关键帧缩略图
```

## License

MIT
