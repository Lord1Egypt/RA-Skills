---
name: web-to-FIM
label: 网页内容转 Markdown/飞书/IMA
slug: web-to-fim
displayName: web-to-FIM
version: 3.7.0
summary: 将任意网页链接或本地文件一键转为结构化 Markdown，并三处存放到 Obsidian、飞书云盘、腾讯 IMA 知识库。
license: MIT-0
description: >
  将任意网页链接或本地文件一键转为结构化 Markdown，并三处存放到 Obsidian Vault、飞书云盘、腾讯 IMA 知识库。
  支持的信源：(1) X/Twitter 推文、长文 Article、Thread 线程（逐字转录）；(2) 微信公众号文章（带图片，IMA 服务端抓取保留排版）；
  (3) 飞书 wiki 文档（v3.7.0 改用 lark-cli docs +fetch 抓取完整内容，WebFetch 截断严重已弃用）；
  (4) 小红书笔记；(5) 微博；(6) YouTube 视频；
  (7) 任意 HTML 网页（带图片，IMA 服务端抓取）；(8) 本地文件：PDF、Word、PPT、Excel、图片、音频等。
  三处存放：Obsidian（本地 Markdown+frontmatter+tags）+ 飞书云盘（.md 原文件，用户身份上传立即可见）+ IMA 知识库（FIM知识库，AI 原生）。
  v3.7.0 飞书 wiki 抓取改造：从 WebFetch（截断严重，200-1000 字符）改为 lark-cli docs +fetch（完整内容，3K-25K 字符），实测 33 篇文章中 19 篇被 WebFetch 截断。
  v3.6.0 飞书存储改造：从应用身份创建在线 docx 改为 lark-cli drive +upload 上传 .md 原文件到用户云盘，用户在飞书"我的空间 > 云盘"立即可见。
  IMA 智能路由：公众号/普通网页 → import_urls 保留图片；X/Twitter/飞书/GitHub → 纯文本笔记逐字转录。
  飞书 wiki 原文链接优先转录：检查文章头部"原文链接"，有则优先抓取原文内容作为最终产物存三处，IMA 只存原文链接地址自动识别。
  X 链接转录流程：飞书 wiki 中发现 X 原文链接时，用 x-tweet-fetcher 抓取完整长文（10K-15K 字符），失败时降级到飞书 wiki 内容。
  批量模式支持断点恢复，Obsidian 写入失败自动 fallback。
  工作流：自动识别 URL/文件类型 → 路由到最佳抓取工具 → 结构化 Markdown → 三处存放。
  触发词：抓网页存飞书、web to feishu、url转文档、文件转飞书、存到ima、存到obsidian、web to fim、三处存放。
  当用户明确要求将 URL 或本地文件转存为文档并存储到 Obsidian/飞书/IMA 时触发。
  Do NOT use for 创建文档内容、编辑飞书文档正文、代码开发、非文档转存任务、普通文档格式转换（非三处存放意图）。
---

# Web-to-FIM | 网页内容转 Markdown/飞书/IMA

## 🤖 AI 时代必备的信息库基础技能

在 AI 时代，无论是使用 **OpenClaw**、**Hermes Agent**，还是实践 **Obsidian + LLM** 的信息管理方法论，**一键入库、人机共用**的 AI 信息库搭建都是必备的基础设施。

**Web-to-FIM** 就是这样一个基础技能：它将任意网络内容一键转换为结构化 Markdown，并同步到：
- 📝 **Obsidian Vault** - 本地个人知识库，带 frontmatter
- 📁 **飞书云盘** - .md 原文件，用户身份上传立即可见（v3.6.0）
- 🧠 **腾讯 IMA 知识库** - AI 原生知识库（FIM知识库）

将任意网页链接或本地文件一键转为结构化 Markdown，并三处存放到 Obsidian Vault、飞书云盘、腾讯 IMA 知识库。

## 支持的信源

| 信源 | URL 特征 | 抓取方式 |
|------|---------|---------|
| X/Twitter | `x.com` / `twitter.com` | x-tweet-fetcher（逐字转录） |
| 微信公众号 | `mp.weixin.qq.com` | markitdown + 移动端 UA fallback |
| 飞书 wiki | `*.feishu.cn/wiki/` | **lark-cli docs +fetch**（v3.7.0 改造，完整内容） |
| 小红书 | `xiaohongshu.com` / `xhslink.com` | markitdown |
| 微博 | `weibo.com` | markitdown |
| YouTube | `youtube.com` / `youtu.be` | markitdown |
| 任意网页 | 其他 `http(s)://` 链接 | markitdown |

> ⚠️ **v3.7.0 飞书 wiki 抓取方式变更**：
> - **旧版本（v3.6.0 及更早）**：用 WebFetch 抓取飞书 wiki 内容，但实测会严重截断（200-1000 字符，完整文章应有 3K-25K 字符）。第十批 33 篇飞书 wiki 文章转录时，19 篇被 WebFetch 截断，导致飞书云盘上保存的内容大量丢失。
> - **新版本（v3.7.0）**：改用 `lark-cli docs +fetch --doc <url> --doc-format markdown --scope full` 抓取完整内容。lark-cli 通过用户身份认证，可读取全文，实测 33 篇全部完整获取（800-24000 字符）。
> - WebFetch 对飞书 wiki 的截断问题源于飞书 wiki 页面需 JS 渲染 + 登录认证，WebFetch 无法处理。lark-cli 通过官方 OpenAPI 直接获取结构化内容，无此问题。

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

| 目的地 | 依赖 | 说明 |
|--------|------|------|
| Obsidian Vault | `OBSIDIAN_VAULT_PATH` 环境变量 | 本地保存到指定目录，带 frontmatter（默认：`E:\Obsidian-Vault\00-Inbox`） |
| 飞书云盘 | `lark-cli`（用户身份登录） | **v3.6.0 改造**：用 `lark-cli drive +upload` 上传 .md 原文件到用户云盘根目录，用户在飞书"我的空间 > 云盘"立即可见。无需 `FEISHU_APP_ID`/`FEISHU_APP_SECRET` |
| 腾讯 IMA | `IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY` | **云端 API v1.1.7**，两步流程存入知识库，参考 `references/ima-setup.md` |

### 飞书云盘配置（v3.6.0）

飞书存储改为依赖 `lark-cli`（用户身份），不再使用应用身份：

```bash
# 1. 安装 lark-cli（一次性）
npm i -g @larksuiteoapi/lark-cli

# 2. 用户身份登录（一次性，浏览器授权）
lark-cli auth login

# 3. 验证身份
lark-cli whoami
# 应显示：identity: user, tokenStatus: ready
```

> **v3.6.0 变更说明**：旧版本用 `FEISHU_APP_ID`+`FEISHU_APP_SECRET`（应用身份 tenant_access_token）创建在线 docx，文档归属应用而非用户，用户在飞书"我的空间"看不到。v3.6.0 改用 lark-cli 用户身份上传 .md 原文件到云盘，立即可见。
>
> 旧的 `feishu_client.py` 已标记为废弃，保留供历史参考，新流程不再调用。

### Obsidian Vault 路径配置
跨平台支持，通过环境变量 `OBSIDIAN_VAULT_PATH` 配置：

```bash
# Windows (PowerShell)
$env:OBSIDIAN_VAULT_PATH = "C:\Users\YourName\Obsidian-Vault\00-Inbox"

# Windows (CMD)
set OBSIDIAN_VAULT_PATH=C:\Users\YourName\Obsidian-Vault\00-Inbox

# macOS/Linux
export OBSIDIAN_VAULT_PATH=~/Obsidian-Vault/00-Inbox
```

如果未设置，默认使用：
- Windows: `E:\Obsidian-Vault\00-Inbox`
- macOS/Linux: `~/Obsidian-Vault/00-Inbox`

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

飞书存储使用 `lark-cli`（用户身份），无需环境变量。配置方法见上方 [飞书云盘配置（v3.6.0）](#飞书云盘配置v360) 章节。

> **v3.6.0 废弃**：旧的 `FEISHU_APP_ID`/`FEISHU_APP_SECRET` 环境变量不再使用（应用身份创建的在线 docx 用户不可见）。`feishu_client.py` 保留但已废弃。

### ima 配置

```bash
# 设置环境变量（v3.0 — IMA OpenAPI v1.1.7）
$env:IMA_OPENAPI_CLIENTID = "your_client_id"
$env:IMA_OPENAPI_APIKEY = "your_api_key"

# 可选：指定知识库名称（默认 "FIM知识库"）
$env:IMA_KB_NAME = "FIM知识库"
```

> ⚠️ **v3.0 变更**：环境变量从 `IMA_CLIENT_ID`/`IMA_API_KEY` 改为 `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY`（旧名仍兼容回退）。IMA 存储从"笔记本"改为"知识库"两步流程。

参考 [references/ima-setup.md](references/ima-setup.md) 获取凭证。

## 工作流

### 步骤 1：转换为 Markdown

```bash
python3 scripts/web_to_md.py --url "<url_or_path>" --output <output.md>
```

路由逻辑：
- **X/Twitter** → x-tweet-fetcher 抓取 JSON → tweet_to_md.py 结构化转换（逐字转录）
- **飞书 wiki**（`*.feishu.cn/wiki/`）→ **lark-cli docs +fetch** 抓取完整 Markdown（v3.7.0）→ 检查原文链接 → 有则尝试抓取原文（更长则覆盖）
- **公众号**（`mp.weixin.qq.com`）→ markitdown 转换，反爬时自动 fallback 到移动端 UA
- **其他网页/本地文件** → markitdown 直接转换

> **v3.4.0 X 链接转录流程修正**：
> - 飞书 wiki 中发现 X 原文链接时，用 **x-tweet-fetcher**（`web_to_md.py`）抓取完整长文（10K-15K 字符）
> - **不用 WebFetch**（对 X 链接超时失败率高）
> - x-tweet-fetcher 失败时降级到飞书 wiki 内容（降级机制）
> - 全文完整性验证：转录后检查内容长度，<500 字符时警告可能不完整

> **v3.3.0 飞书 wiki 原文链接优先转录**：
> - 抓取飞书 wiki 后，检查文章头部是否有"原文链接"（如 `🔗 原文链接：[url]`）
> - 有原文链接 → 优先抓取原文链接内容（公众号/X 等），获得更完整的正文和图片
> - 无原文链接 → 用飞书 wiki 内容
> - IMA 存放：有公众号原文链接 → import_urls（保留图片）；无 → 纯文本笔记

> **v3.0 新增信源支持**：
> - 飞书 wiki 文档：通过 WebFetch 转录飞书知识库文章全文
> - 公众号反爬 fallback：markitdown 返回验证页时自动切换移动端 UA 重试

> **v3.5.0 新增**：
> - Obsidian 文件命名升级：`YYYYMMDD-标题-关键信息.md`（如 `20260718-数字人口播实战攻略-数字人、口播、heygen.md`）
> - 关键信息由 AI 从标题和内容提取 2-4 个关键词，用顿号"、"分隔
> - 未提供 keywords 时 fallback 到来源（waytoagi/wechat/x/github）
> - CLI 新增 `--keywords` 参数；`save_fetched.py` JSON 配置新增 `keywords` 字段

> **v3.6.0 飞书存储改造**：
> - 飞书存储从应用身份（`FeishuClient.create_document` 创建在线 docx）改为用户身份（`lark-cli drive +upload` 上传 .md 原文件到云盘）
> - 旧版本文档归属应用，用户在飞书"我的空间"看不到；新版文件归属用户，立即可见
> - 不再需要 `FEISHU_APP_ID`/`FEISHU_APP_SECRET` 环境变量，改用 `lark-cli auth login` 用户授权
> - 飞书上传依赖 Obsidian 保存的 .md 文件路径，Obsidian 失败时飞书自动跳过
> - `feishu_client.py` 标记为废弃，保留供历史参考
> - `save_to_feishu()` 函数签名变更：`(content, title)` → `(md_file_path, title=None)`

> **v3.7.0 飞书 wiki 抓取改造**：
> - 飞书 wiki 抓取从 WebFetch（截断严重，200-1000 字符）改为 `lark-cli docs +fetch`（完整内容，3K-25K 字符）
> - `web_to_md.py` 新增 `_convert_feishu_wiki()` 函数和 `feishu_wiki` source 类型
> - `convert()` 函数新增 feishu_wiki 分支，自动调用 lark-cli
> - 飞书 wiki 原文链接优先转录流程：lark-cli 抓取后检测原文链接，自动用 markitdown 或 x-tweet-fetcher 抓取原文（更长则覆盖）
> - 实测数据：第十批 33 篇飞书 wiki 文章转录，v3.6.0 用 WebFetch 时 19 篇被截断，v3.7.0 用 lark-cli 后 33 篇全部完整

> **v3.2.0 新增**：
> - Obsidian 文件命名规范化：`YYYYMMDD-标题-来源.md`（如 `20260712-歸藏：GPT-5.6 Sol 帮我做了个小工具-waytoagi.md`）
> - 来源自动提取：从 URL 域名提取来源标识（waytoagi/feishu/x/wechat/weibo/xiaohongshu/github/youtube/webpage）
> - 飞书 wiki 原文链接优先转录：抓取飞书 wiki 后检查原文链接，有则优先抓取原文内容（更完整）
> - Windows 文件名安全：禁止字符替换为下划线，中文标点（含：）保留

> **v3.1 新增**：
> - 批量模式断点恢复：崩溃后重跑自动跳过已完成 URL（`.progress.json` 进度文件）
> - Obsidian frontmatter 自动 tags：根据 URL 来源分类标签
> - 推文结构化转换通用化：去硬编码，基于启发式规则识别段落标题
> - subprocess 加 120 秒 timeout：防止网络异常永久挂起
> - 公众号正文提取改进：保留图片、段落结构、引用块

### 步骤 2：存入目的地

#### Obsidian Vault

文件名规则：`YYYYMMDD-标题-关键信息.md`（v3.5.0）
- **关键信息**：AI 从标题和内容提取 2-4 个关键词，用顿号"、"分隔
- 未提供关键词时 fallback 到来源（waytoagi/feishu/x/wechat 等）
- 示例：`20260718-数字人口播实战攻略-数字人、口播、heygen.md`
- 旧示例（v3.2.0）：`20260712-歸藏：GPT-5.6 Sol 帮我做了个小工具-waytoagi.md`

```python
from scripts.web_to_all import save_to_obsidian
filepath = save_to_obsidian(markdown_content, title, url, keywords="数字人、口播、heygen")  # v3.5.0 keywords
```

#### 飞书云盘（v3.6.0）

用 `lark-cli drive +upload` 上传 .md 原文件到用户云盘根目录。文件归属于用户身份，立即可见。

```python
from scripts.web_to_all import save_to_obsidian, save_to_feishu

# v3.6.0 流程：先存 Obsidian 得到文件路径，再用该路径上传飞书
obs_path = save_to_obsidian(markdown_content, title, url, keywords="关键词1、关键词2")
feishu_result = save_to_feishu(obs_path, title)  # 上传 .md 文件到飞书云盘
print(f"飞书云盘 URL: {feishu_result['url']}")
```

或者直接命令行：

```bash
# 先用 web_to_all.py 一次性三处存放
python3 scripts/web_to_all.py --url "<url>" --keywords "关键词1、关键词2"
# 飞书会自动复用 Obsidian 保存的 .md 文件上传到云盘
```

> **v3.6.0 变更**：
> - 旧版本用 `FeishuClient.create_document` 创建在线 docx（应用身份，用户不可见）
> - 新版本用 `lark-cli drive +upload` 上传 .md 原文件（用户身份，立即可见）
> - 必须先存 Obsidian 得到文件路径，飞书上传依赖该文件
> - Obsidian 失败时飞书会自动跳过（输出 `Feishu skipped: Obsidian file not available`）

#### 腾讯 ima（v3.0 — 知识库两步流程 + 图片保留）

IMA 有**两套独立 API**，不可混用：
- **Notes API**（`/openapi/note/v1/`）：管笔记、笔记本
- **Knowledge Base API**（`/openapi/wiki/v1/`）：管知识库、知识条目

「FIM知识库」是**知识库**（wiki API），不是笔记本（note API）。必须用两步流程。

> **v3.0 核心功能 — 公众号/网页带图片转录**：
> - 公众号和普通网页 URL 通过 `import_urls` 让 IMA 服务端抓取，**保留原文图片和排版**
> - X/Twitter 和飞书 wiki 走纯文本笔记（逐字转录），因为 X 要求逐字转录、飞书需登录认证

```python
from scripts.web_to_all import save_to_ima

# 方式1：直接用 save_to_ima（推荐，自动路由）
# - 公众号/普通网页 URL → import_urls（服务端抓取，保留图片）
# - X/Twitter/飞书 URL → 纯文本笔记（逐字转录）
result = save_to_ima(content, title, knowledge_base="FIM知识库", source_url=url)

# 方式2：手动两步流程
from scripts.ima_client import IMAClient
client = IMAClient()
# Step 1: 创建笔记（Notes API）
note = client.create_note(title="标题", content=markdown_content)
# Step 2: 添加到知识库（Wiki API）
kb_id = client.find_knowledge_base_by_name("FIM知识库")
client.add_note_to_knowledge_base(note_id=note["note_id"], title="标题", knowledge_base_id=kb_id)
```

**IMA 存放路由规则（v3.0）**：

| source_url 类型 | IMA 存放方式 | 原因 |
|----------------|------------|------|
| 公众号（`mp.weixin.qq.com`） | `import_urls`（服务端抓取） | 保留图片和排版 |
| 普通网页 | `import_urls`（服务端抓取） | 保留图片和排版 |
| **X/Twitter** | **纯文本笔记（逐字转录）** | 技能规则要求逐字转录 |
| 飞书 wiki | 纯文本笔记（逐字转录） | 需登录认证，IMA 无法抓取 |
| 无 URL | 纯文本笔记 | 手动内容/飞书转录 |

### 验证连接

```bash
# 验证飞书（v3.6.0：lark-cli 用户身份）
lark-cli whoami
# 应显示：identity: user, tokenStatus: ready

# 验证 ima
python scripts/ima_client.py --action test
```

## 故障处理

| 问题 | 解决方案 |
|------|---------|
| x.com SSL 超时 | x-tweet-fetcher 使用 FxTwitter API 中转 |
| markitdown 模块丢失 | `pip install markitdown` |
| 微信反爬拦截 | markitdown 返回72字符验证页，需 fallback 到 WebFetch 或移动端 UA |
| 飞书 wiki 内容截断（v3.6.0 旧问题） | **v3.7.0 已修复**。旧版本用 WebFetch 截断严重，升级到 v3.7.0 后改用 `lark-cli docs +fetch` 抓取完整内容 |
| 飞书 wiki 抓取报"lark-cli 未安装" | 运行 `npm i -g @larksuiteoapi/lark-cli` 安装，再 `lark-cli auth login` 用户授权 |
| 飞书 wiki 抓取报"lark-cli API 返回 ok=false" | 1) `lark-cli whoami` 检查登录状态；2) 文档权限不足时联系飞书 wiki 管理员开通访问权限 |
| 飞书云盘上传失败（v3.6.0） | 1) 运行 `lark-cli whoami` 检查登录状态；2) 未登录则 `lark-cli auth login`；3) lark-cli 未安装则 `npm i -g @larksuiteoapi/lark-cli` |
| 飞书上传报"unsafe file path" | lark-cli `--file` 必须是 cwd 下的相对路径，代码会自动复制到 scripts 目录 |
| 飞书存储跳过 | Obsidian 失败时飞书会跳过（提示 `Feishu skipped: Obsidian file not available`），先修复 Obsidian 写入权限 |
| 飞书文档不可见（v3.5 旧版问题） | v3.6.0 已修复。旧版本用应用身份创建 docx 导致不可见，升级到 v3.6.0 后改用 lark-cli 用户身份上传云盘 |
| 飞书 blocks 400 错误（v3.5 旧版） | v3.6.0 不再创建在线 docx，无 blocks 概念。如使用旧 feishu_client.py：单次最多 50 个 blocks，长文章需分批插入 |
| ima 凭证无效 | 检查 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY`（v3.0） |
| IMA 笔记不在知识库中 | 知识库≠笔记本，必须用两步流程：create_note → add_knowledge |
| IMA import_urls 文件夹不存在 | folder_id 不等于 knowledge_base_id，需用 `get_root_folder_id()` 获取 |
| X 链接 IMA 存储错误 | X/Twitter 必须逐字转录（纯文本笔记），不可用 import_urls |

## 依赖与安装

### 完整依赖列表

| 依赖 | 安装命令 | 说明 |
|------|---------|------|
| markitdown | `pip install markitdown` | 网页转 Markdown 核心库 |
| requests | `pip install requests` | HTTP 请求 |
| python-dotenv | `pip install python-dotenv` | 环境变量管理 |
| lark-cli | `npm i -g @larksuiteoapi/lark-cli` | **v3.6.0 飞书云盘上传必需**，运行 `lark-cli auth login` 登录 |
| x-tweet-fetcher | 克隆到 `~/.aily/workspace/skills/x-tweet-fetcher` | X/Twitter 专用抓取（可选） |

### 一键安装所有依赖

```bash
# 安装 Python 依赖
pip install markitdown requests python-dotenv

# 安装 lark-cli 并登录（v3.6.0 飞书存储必需）
npm i -g @larksuiteoapi/lark-cli
lark-cli auth login
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

### 🔒 权限声明（MCP Least Privilege）

本技能运行时需要以下权限：

| 权限类型 | 具体内容 | 用途 |
|---------|---------|------|
| **文件读取** | 用户指定的 URL、本地输入文件、Obsidian 保存后的 .md 文件（飞书上传源） | 转换源内容、上传到飞书云盘 |
| **文件写入** | Obsidian Vault 目录（`OBSIDIAN_VAULT_PATH`）、scripts 目录下的临时 .md 文件（上传后删除） | 存储转换结果、临时复制给 lark-cli 上传 |
| **网络请求** | 用户提供的 URL（网页抓取）、腾讯 IMA OpenAPI | 抓取内容和存储到 IMA |
| **subprocess** | `lark-cli`（v3.6.0 飞书云盘上传）、x-tweet-fetcher（可选，仅 X/Twitter 链接） | 飞书云盘上传、X 平台内容抓取 |
| **环境变量** | `IMA_OPENAPI_CLIENTID`、`IMA_OPENAPI_APIKEY`、`OBSIDIAN_VAULT_PATH` | 凭证和路径配置 |

> ⚠️ 本技能**不读取** Windows registry、不读取 GitHub token、不调用 GitHub API、不执行 git 操作。仅做文档转换和三处存放。
>
> **v3.6.0 变更**：不再需要 `FEISHU_APP_ID`/`FEISHU_APP_SECRET` 环境变量，飞书凭证由 lark-cli 通过用户授权管理（`lark-cli auth login`）。

### ⚠️ 用户警告（运行前必读）

1. **数据外传**：运行本技能会将您提供的 URL 或本地文件内容上传到以下第三方云端服务：
   - **飞书云盘**（v3.6.0：通过 lark-cli 用户身份上传，需预先 `lark-cli auth login`）
   - **腾讯 IMA 知识库**（需 `IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY`）
   - 如果内容包含敏感、机密或受监管数据，请先确认是否允许上传到这些服务

2. **本地写入**：默认会向 Obsidian Vault 目录写入 Markdown 文件。可通过 `--no-obsidian` 禁用本地写入

3. **选择性禁用**：支持通过参数禁用特定存储目的地：
   - `--no-feishu`：跳过飞书云盘
   - `--no-ima`：跳过腾讯 IMA
   - `--no-obsidian`：跳过本地 Obsidian

4. **IMA URL 导入**：公众号/普通网页 URL 会通过 IMA `import_urls` 让 IMA 服务端抓取，URL 会被发送给腾讯服务器

5. **飞书云盘文件归属**（v3.6.0 新增）：lark-cli 上传的文件归属于 lark-cli 当前登录用户，文件出现在用户飞书"我的空间 > 云盘"根目录

### 🔒 安全设计原则

1. **凭证安全**
   - IMA 凭证通过环境变量配置，**无硬编码**
   - 飞书凭证由 lark-cli 管理（用户授权），不再需要环境变量（v3.6.0）
   - 支持 `IMA_OPENAPI_CLIENTID`, `IMA_OPENAPI_APIKEY`（v3.0）
   - 旧变量名 `IMA_CLIENT_ID`/`IMA_API_KEY` 仍兼容回退
   - 旧变量 `FEISHU_APP_ID`/`FEISHU_APP_SECRET` 已废弃（v3.6.0），保留供 feishu_client.py 历史参考

2. **文件操作**
   - 默认写入 Obsidian Vault 目录（可通过 `OBSIDIAN_VAULT_PATH` 配置）
   - 飞书上传前会临时复制 .md 文件到 scripts 目录（lark-cli 限制），上传后立即删除
   - 支持通过 `--no-feishu` / `--no-ima` / `--no-obsidian` 选择性禁用功能
   - 不扫描、不读取用户目录下的其他文件

3. **隐私保护**
   - 不读取任何未经授权的用户配置文件
   - 所有网络请求仅针对用户提供的 URL
   - 本地文件仅用于转换，不主动扫描

4. **权限透明**
   - 文件写入范围：Obsidian Vault 目录、临时 Markdown 文件（上传后删除）
   - 文件读取范围：用户指定的 URL、本地输入文件、Obsidian 保存后的 .md 文件
