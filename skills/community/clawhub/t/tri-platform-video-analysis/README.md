# tri-platform-parse

三平台视频解析 — 丢一条链接，还你一份标准化 HTML 分析报告。

## 支持平台

- 抖音 (douyin.com)
- B站 (bilibili.com)  
- 小红书 (xiaohongshu.com)

## 快速开始

```bash
# 安装依赖
pip install yt-dlp faster-whisper

# 解析视频
python scripts/parse.py "https://www.bilibili.com/video/BV1xxxx"
```

## AI 分析（可选）

```bash
# 设置后自动启用 LLM 分析
export LLM_API_KEY=sk-xxx
# 可选
export LLM_BASE_URL=https://api.openai.com/v1
export LLM_MODEL=gpt-4o
```

## 输出

每次运行生成三个文件：

| 文件 | 说明 |
|------|------|
| `报告.html` | 标准化分析报告（可直接浏览器打开） |
| `连贯稿.txt` | 纯文本字幕 |
| `逐字稿.txt` | 带时间戳字幕 |

## 特性

- 纯本地转写，零费用，无需 API Key
- AI 分析可选，有 Key 自动启用，无 Key 本地智能提取
- 标准化 HTML 输出，含摘要、核心观点、金句、结构拆解、内容判断
- 适用于所有 AI Agent 平台

## 注意

- 小红书链接需通过「分享 → 复制链接」获取
- 首次运行自动下载 Whisper 模型（约 500MB）
