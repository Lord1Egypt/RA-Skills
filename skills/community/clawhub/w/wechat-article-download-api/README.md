# WeChat Article Download API

OpenClaw Skill — 通过 down.mptext.top API 抓取和导出微信公众号文章内容。

## 功能特性

- 📥 **多格式输出**：支持 HTML、Markdown、纯文本、JSON 四种格式
- 🔑 **无需 API Key**：直接调用，零配置
- 🤖 **OpenClaw 原生集成**：作为 Skill 安装后，AI 可自动调用
- 📦 **批量处理**：支持批量下载多篇文章

## 支持的输出格式

| 格式 | 说明 |
|------|------|
| `html` | 保留原始排版和样式的 HTML |
| `markdown` | 结构化 Markdown，适合阅读和二次编辑 |
| `text` | 纯文本，适合 AI 分析和处理 |
| `json` | 结构化 JSON，包含元数据 |

## 安装

### 方式一：作为 OpenClaw Skill 安装（推荐）

```bash
clawhub install wechat-article-download-api
```

### 方式二：手动安装

1. 将本仓库克隆到你的 OpenClaw skills 目录：
```bash
git clone https://github.com/Lniosy/wechat-article-download-api.git ~/.openclaw/workspace/skills/wechat-article-download-api
```

2. 重启 OpenClaw

### 方式三：作为独立 Python 工具使用

```bash
pip install requests
python scripts/fetch_wechat_article.py --url "https://mp.weixin.qq.com/s/xxxxx" --formats markdown text
```

## 使用方法

安装为 Skill 后，直接告诉 AI 文章链接即可：

> "帮我下载这篇文章：https://mp.weixin.qq.com/s/xxxxx"

### 命令行使用

```bash
# 下载单篇文章（全格式）
python scripts/fetch_wechat_article.py \
  --url "https://mp.weixin.qq.com/s/xxxxx" \
  --formats html markdown text json

# 指定输出目录和文件名
python scripts/fetch_wechat_article.py \
  --url "https://mp.weixin.qq.com/s/xxxxx" \
  --formats markdown \
  --outdir "./output" \
  --basename "my_article"

# 仅导出纯文本
python scripts/fetch_wechat_article.py \
  --url "https://mp.weixin.qq.com/s/xxxxx" \
  --formats text
```

## API 接口

本工具使用 [down.mptext.top](https://down.mptext.top) 提供的公开 API：

**接口地址：**
```
https://down.mptext.top/api/public/v1/download
```

**请求参数：**

| 参数 | 说明 | 必填 |
|------|------|------|
| `url` | 微信公众号文章链接 | 是 |

**返回格式：** 根据请求的 `format` 参数返回对应格式的内容。

## 与其他工具配合使用

### + [qiqing-liuyu（七情六欲）](https://github.com/Lniosy/qiqing-liuyu)
抓取文章后，用七情六欲 skill 进行内容分析、去 AI 味、提炼要点、改写成有人味的文章。

### + AI 对话/总结
抓取纯文本或 Markdown 格式后，直接喂给 AI 做内容分析、摘要、翻译、改写。

## 适用场景

- 📰 **内容分析**：快速获取公众号文章全文，供 AI 分析
- 📝 **内容创作参考**：研究优质文章结构和写法
- 🔄 **内容批量处理**：批量抓取多篇文章进行对比分析
- 📊 **数据采集**：为数据分析收集公众号文章素材
- 🌐 **内容改写**：抓取 Markdown 后用 AI 改写或二次创作

## 项目结构

```
wechat-article-download-api/
├── SKILL.md              # OpenClaw Skill 定义文件
├── scripts/
│   └── fetch_wechat_article.py  # 核心：文章下载脚本
├── agents/
│   └── openai.yaml           # Agent 配置
└── references/
    └── api.md              # API 接口文档
```

## 技术栈

- Python 3
- [requests](https://pypi.org/project/requests/) — HTTP 请求
- [down.mptext.top](https://down.mptext.top) — 文章解析 API

## 许可证

MIT License

## 作者

[Lniosy](https://github.com/Lniosy)

## 相关项目

> ⭐ **[qiqing-liuyu（七情六欲）](https://github.com/Lniosy/qiqing-liuyu)** — AI 情感与人格增强 Skill，让 AI 写作有人味、去 AI 味
> 
> 如果你在做内容创作，强烈推荐搭配使用。抓取的文章用七情六欲 skill 做内容分析、提炼要点、改写成有人味的文章，效果翻倍。
