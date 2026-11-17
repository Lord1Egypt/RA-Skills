---
name: tingdong-skill
description: 将任意文章/链接/文本转换为个性化播客音频。当用户需要将公众号文章、知乎回答、网页内容或纯文本转换为语音播客时使用。支持渐进式内容分析、多风格播客生成和音频输出。适用于通勤学习、碎片时间知识获取场景。
---

# 听懂了 (TingDong) - 文章转播客 Skill

## 核心工作流

```
用户输入内容（链接/文本）
    ↓
识别内容类型 → 选择抓取策略
    ↓
内容抓取/接收 → 清洗结构化
    ↓
AI 深度分析 → 生成播客脚本
    ↓
TTS 语音合成 → 输出音频
```

## 第一步：内容接收

询问或识别用户输入的内容类型：

| 类型 | 识别方式 | 处理方式 |
|------|---------|---------|
| 微信公众号文章 | URL 含 `mp.weixin.qq.com` | Playwright 抓取（反爬） |
| 知乎回答/文章 | URL 含 `zhihu.com` | 公开 API 或页面抓取 |
| 普通网页 | 以 `http://`/`https://` 开头 | 通用抓取 + 正文提取 |
| 纯文本 | 无 URL，直接文本输入 | 直接接收，无需抓取 |

**渐进式提问**：
1. "请粘贴文章链接或输入文本内容"
2. 根据输入自动识别类型，无需用户手动选择

## 第二步：内容处理

### 抓取策略（由后端处理）

```python
# 伪代码 — 实际由后端 API 执行
def fetch_content(url):
    if "mp.weixin.qq.com" in url:
        return playwright_fetch(url)  # 解决微信反爬
    elif "zhihu.com" in url:
        return zhihu_api_fetch(url)
    else:
        return generic_web_fetch(url)
```

### 内容清洗
- 去除广告、导航栏、评论区
- 提取正文核心内容
- 保留标题、作者、来源信息（用于归因）

## 第三步：播客生成

### 调用后端 API

```python
# 使用 scripts/generate_podcast.py
from scripts.generate_podcast import generate_podcast

result = generate_podcast(
    content="文章正文或链接",
    content_type="url",  # 或 "text"
    style="conversational",  # conversational | summary | deep_dive
    duration="medium",  # short (~5min) | medium (~10min) | long (~20min)
    voice="zh-CN-XiaoxiaoNeural"  # Edge-TTS 语音
)
# 返回: {"audio_url": "...", "title": "...", "duration": 600}
```

### 播客风格选项

| 风格 | 适用场景 | 特点 |
|------|---------|------|
| `conversational` | 通用 | 对话式讲解，像朋友聊天 |
| `summary` | 快速了解 | 要点提炼，3-5分钟精华版 |
| `deep_dive` | 深度学习 | 逐段分析，保留论证过程 |

## 第四步：结果交付

向用户返回：
- 音频文件或链接
- 播客标题和时长
- 原文来源标注（如果是 URL）

**示例输出**：
> 已为你生成播客《AI Agent 正在重构软件交互——深度解读》
> 
> 🔊 [点击收听](audio_url) | ⏱️ 12分钟
> 
> 📎 原文：公众号「机器之心」

## 资源引用

- **API 文档**: 见 [references/api_docs.md](references/api_docs.md)
- **内容源处理策略**: 见 [references/content_sources.md](references/content_sources.md)
- **生成脚本**: 见 [scripts/generate_podcast.py](scripts/generate_podcast.py)

## 注意事项

1. **版权合规**：用户主动提供链接 = 个人使用，平台主动抓取 = 风险
2. **微信反爬**：公众号文章必须用 Playwright（curl 只能拿到"请用微信打开"）
3. **语音选择**：默认中文女声，可通过 `voice` 参数切换
4. **错误处理**：抓取失败时回退到"请手动粘贴正文"
