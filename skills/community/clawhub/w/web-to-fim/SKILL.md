---
name: web-to-FIM
label: 网页内容转 Markdown/飞书/IMA
description: >
  将任意网页链接或本地文件一键转为结构化 Markdown，并保存到 Obsidian Vault、飞书云文档或腾讯 IMA 笔记。
  支持的信源：(1) X/Twitter 推文、长文 Article、Thread 线程；(2) 微信公众号文章；
  (3) 小红书笔记；(4) 微博；(5) YouTube 视频；(6) 任意 HTML 网页；
  (7) 本地文件：PDF、Word、PPT、Excel、图片、音频等。
  工作流：自动识别 URL/文件类型 → 路由到最佳抓取工具 → 结构化 Markdown → 选择性保存到 Obsidian/飞书/IMA。
  触发词：转文档、抓网页存飞书、网页转文档、web to feishu、url转文档、文件转飞书、存到ima、存到obsidian、web to fim。
  当用户提供任意 URL 或本地文件并要求转存为文档时触发。
---

# Web-to-FIM | 网页内容转 Markdown/飞书/IMA

## 🤖 AI 时代必备的信息库基础技能

在 AI 时代，无论是使用 **OpenClaw**、**Hermes Agent**，还是实践 **Obsidian + LLM** 的信息管理方法论，**一键入库、人机共用**的 AI 信息库搭建都是必备的基础设施。

**Web-to-FIM** 就是这样一个基础技能：它将任意网络内容一键转换为结构化 Markdown，并同步到：
- 📝 **Obsidian Vault** - 本地个人知识库，带 frontmatter
- 📚 **飞书云文档** - 云端团队协作
- 🧠 **腾讯 IMA 笔记** - AI 原生知识库

将任意网页链接或本地文件一键转为结构化 Markdown，并保存到 Obsidian Vault、飞书云文档或腾讯 IMA 笔记。

## 支持的信源

| 信源 | URL 特征 | 抓取方式 |
|------|---------|---------|
| X/Twitter | `x.com` / `twitter.com` | x-tweet-fetcher |
| 微信公众号 | `mp.weixin.qq.com` | markitdown-plus |
| 小红书 | `xiaohongshu.com` / `xhslink.com` | markitdown-plus |
| 微博 | `weibo.com` | markitdown-plus |
| YouTube | `youtube.com` / `youtu.be` | markitdown-plus |
| 任意网页 | 其他 `http(s)://` 链接 | markitdown-plus |

### 本地文件支持

| 类型 | 扩展名 |
|------|--------|
| PDF | `.pdf` |
| Word | `.docx` / `.doc` |
| PowerPoint | `.pptx` / `.ppt` |
| Excel | `.xlsx` / `.xls` |
| 图片 | `.png` `.jpg` `.jpeg` `.gif` `.webp` |
| 音频 | `.mp3` `.wav` `.m4a` `.flac` |
| 数据 | `.csv` `.json` `.xml` |

## 输出目的地

| 目的地 | 环境变量 | 说明 |
|--------|---------|------|
| Obsidian Vault | `OBSIDIAN_VAULT_PATH` | 本地保存到指定目录，带 frontmatter（默认：`E:\Obsidian\md\inbox`） |
| 飞书云文档 | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` | 云端服务，参考 `references/feishu-setup.md` |
| 腾讯 IMA | `IMA_CLIENT_ID` + `IMA_API_KEY` | **云端 API**，无需本地客户端，参考 `references/ima-setup.md` |

### Obsidian Vault 路径配置
跨平台支持，通过环境变量 `OBSIDIAN_VAULT_PATH` 配置：

```bash
# Windows (PowerShell)
$env:OBSIDIAN_VAULT_PATH = "C:\Users\YourName\Obsidian\Vault\inbox"

# Windows (CMD)
set OBSIDIAN_VAULT_PATH=C:\Users\YourName\Obsidian\Vault\inbox

# macOS/Linux
export OBSIDIAN_VAULT_PATH=~/Obsidian/Vault/inbox
```

如果未设置，默认使用：
- Windows: `E:\Obsidian\md\inbox`
- macOS/Linux: `~/Obsidian/inbox`

## 一键保存到所有目的地

使用 `web_to_all.py` 一键转换并保存到 Obsidian/飞书/IMA：

```bash
python3 scripts/web_to_all.py --url "<url_or_path>"
python3 scripts/web_to_all.py --url "<url>" --title "自定义标题"
python3 scripts/web_to_all.py --url "<url>" --no-feishu --no-ima  # 仅保存 Obsidian
```

## 安全配置

⚠️ **凭证必须通过环境变量配置**，禁止硬编码：

### 飞书配置

```bash
# 设置环境变量
$env:FEISHU_APP_ID = "your_app_id"
$env:FEISHU_APP_SECRET = "your_app_secret"
```

参考 [references/feishu-setup.md](references/feishu-setup.md) 获取凭证。

### ima 配置

```bash
# 设置环境变量
$env:IMA_CLIENT_ID = "your_client_id"
$env:IMA_API_KEY = "your_api_key"
```

参考 [references/ima-setup.md](references/ima-setup.md) 获取凭证。

## 工作流

### 步骤 1：转换为 Markdown

```bash
python3 scripts/web_to_md.py --url "<url_or_path>" --output <output.md>
```

路由逻辑：
- **X/Twitter** → x-tweet-fetcher 抓取 JSON → tweet_to_md.py 结构化转换
- **其他所有** → markitdown-plus 直接转换

### 步骤 2：存入目的地

#### Obsidian Vault

```python
from scripts.web_to_all import save_to_obsidian
filepath = save_to_obsidian(markdown_content, title, url)
```

#### 飞书云文档

```python
from scripts.feishu_client import FeishuClient

client = FeishuClient()
result = client.create_document(title="文档标题", content_md=markdown_content)
print(f"文档 URL: {result['url']}")
```

#### 腾讯 ima

```python
from scripts.ima_client import IMAClient

client = IMAClient()
result = client.create_note(title="笔记标题", content=markdown_content)
print(f"笔记 URL: {result['url']}")
```

### 验证连接

```bash
# 验证飞书
python scripts/feishu_client.py --action test

# 验证 ima
python scripts/ima_client.py --action test
```

## 故障处理

| 问题 | 解决方案 |
|------|---------|
| x.com SSL 超时 | x-tweet-fetcher 使用 FxTwitter API 中转 |
| markitdown 模块丢失 | `pip install markitdown` |
| 微信反爬拦截 | markitdown 自动用移动端 UA 重试 |
| 飞书凭证无效 | 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` |
| ima 凭证无效 | 检查 `IMA_CLIENT_ID` 和 `IMA_API_KEY` |

## 依赖与安装

### 完整依赖列表

| 依赖 | 安装命令 | 说明 |
|------|---------|------|
| markitdown | `pip install markitdown` | 网页转 Markdown 核心库 |
| requests | `pip install requests` | HTTP 请求 |
| python-dotenv | `pip install python-dotenv` | 环境变量管理 |
| x-tweet-fetcher | 克隆到 `~/.aily/workspace/skills/x-tweet-fetcher` | X/Twitter 专用抓取（可选） |

### 一键安装所有依赖

```bash
# 安装 Python 依赖
pip install markitdown requests python-dotenv
```

### x-tweet-fetcher（可选，仅用于 X/Twitter）
```bash
# 克隆到技能目录
cd ~/.aily/workspace/skills
git clone https://github.com/EdwardWason/x-tweet-fetcher.git
```

如果不安装 x-tweet-fetcher，X/Twitter 链接将使用 markitdown 直接处理。

---

## 安全声明

### 🔒 安全设计原则

1. **凭证安全
   - 所有 API 凭证通过环境变量配置，**无硬编码**
   - 支持 `FEISHU_APP_ID, FEISHU_APP_SECRET, IMA_CLIENT_ID, IMA_API_KEY

2. **文件操作
   - 仅在用户明确指定时写入文件
   - Obsidian Vault 路径完全可控
   - 支持通过 `--no-feishu` / --no-ima` 选择性禁用功能

3. **隐私保护
   - 不读取任何未经授权的用户配置文件
   - 所有网络请求仅针对用户提供的 URL
   - 本地文件仅用于转换，不主动扫描

4. **权限透明
   - 文件写入范围：Obsidian Vault 目录、临时 Markdown 文件
   - 文件读取范围：用户指定的 URL、本地输入文件
