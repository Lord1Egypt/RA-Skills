---
name: ynote-clip
version: '1.8.1'
description: 网页剪藏到有道云笔记。触发词：剪藏网页、保存网页、收藏网页、ynote clip、clip to ynote、网页摘录。
metadata: {"openclaw": {"emoji": "📎", "requires": {"bins": ["node", "curl", "jq", "dig"], "tools": ["browser"], "env": ["YNOTE_API_KEY"]}, "primaryEnv": "YNOTE_API_KEY"}}
---

# YNote Clip — 网页剪藏

将网页内容剪藏到有道云笔记。通过 `clip-note.mjs`（Node.js）完成图片处理和 MCP 调用。

## 前置条件

```bash
export YNOTE_API_KEY="your-api-key-here"   # 必需
node --version                              # 需要 Node.js >= 22.12.0
```

> **注意**：`YNOTE_API_KEY` 必须在执行脚本的 shell 环境中可用。若 API Key 在 `~/.zshrc` 或 `~/.bashrc` 中通过 `export` 设置，需在每次脚本执行前先 `source ~/.zshrc`（或对应的 shell 配置文件）。

图片压缩工具（按操作系统）：

- **macOS**：使用系统内置 `sips`，无需额外安装
- **Linux**：需安装 `imagemagick`

  ```bash
  # Ubuntu / Debian
  sudo apt install imagemagick

  # Alpine
  apk add imagemagick
  ```

> 工具不可用时会 graceful 降级——图片跳过压缩，以原图上传。

`dig`（DNS 查询工具）用于图片下载超时时的 DNS fallback，跳过系统 DNS 直接走 Google DNS 下载：

- **macOS**：系统内置，无需安装
- **Linux**：通常已预装；若缺失：

  ```bash
  # Ubuntu / Debian
  sudo apt install dnsutils

  # Alpine
  apk add bind-tools
  ```

> `dig` 不可用时 DNS fallback 会跳过，该张图片标记为下载失败（不影响整体剪藏流程）。

依赖 `tools/browser`（OpenClaw 内置，使用 `openclaw` profile 受控浏览器，无需安装 Chrome 扩展）。
> 浏览器默认以无头模式运行（安装脚本自动配置）。如需可见窗口调试，执行 `openclaw config set browser.headless false`。

## Quick Reference

| 操作 | 命令 |
|------|------|
| **剪藏网页** | 按「核心工作流」执行 |
| 创建笔记 | `bash {baseDir}/mcp-call.sh createNote '{"title":"标题","content":"# 内容","folderId":""}'` |
| 搜索笔记 | `bash {baseDir}/mcp-call.sh searchNotes '{"keyword":"关键词"}'` |
| 列出笔记 | `bash {baseDir}/mcp-call.sh listNotes '{"folderId":""}'` |
| 获取笔记内容 | `bash {baseDir}/mcp-call.sh getNoteTextContent '{"noteId":"<id>"}'` |

## 调试模式（默认关闭）

调试模式默认关闭。用户说"开启调试"或"debug"时，在后续命令前添加 `YNOTE_CLIP_DEBUG=1`：

```bash
YNOTE_CLIP_DEBUG=1 node {baseDir}/clip-note.mjs ...
YNOTE_CLIP_DEBUG=1 node {baseDir}/twitter-apify.mjs ...
```

开启后每步输出 `🔍` 前缀的中间结果及耗时，方便定位问题。用户说"关闭调试"或"quiet"时恢复默认。

## 核心工作流

收到用户的剪藏请求后，**先回复用户「正在保存中...」**，然后按以下工作流执行。

### 网页内容提取流程

> **性能关键**：bodyHtml（50-100KB）**绝不能经过 agent 的 context window**。
> 所有浏览器操作通过 `openclaw browser` CLI 执行，大数据直接管道到文件。

**输入**：URL
**输出**：`/tmp/ynote-clip-data.json`（包含 title、content、imageUrls、source）

#### Step 0：Twitter/X 专用流程

**Twitter/X 是本项目优化重点**，遇到 Twitter URL 时优先使用 Apify API 绕过 CSP 限制。

**URL 检测**：URL 包含 `x.com/` 或 `twitter.com/` 且含 `/status/` 时，触发 Twitter 专用流程。

```bash
node {baseDir}/twitter-apify.mjs --url "<Twitter URL>"
```

脚本自动完成：调用 Apify Twitter Scraper Unlimited → 等待结果 → 写入 `/tmp/ynote-clip-data.json`。

**成功时**：输出 metadata JSON（~200 字节），直接跳到「剪藏工作流 Step 2」。

**失败时**：脚本会以非零退出码退出并输出错误信息，此时 **不要重试**，直接报错并告知用户。

**非 Twitter URL**：继续执行下方「Step 1」通用网页提取流程。

#### Step 1：通用网页内容提取（browser CLI + collect SDK 注入）




通过 `openclaw browser` CLI 打开目标页面，注入收藏 SDK 提取正文。**全部在一条 bash 命令中完成，bodyHtml 直接写入文件，不进入 agent context**。

```bash
bash {baseDir}/collect-page.sh "<用户提供的 URL>"
```

脚本自动完成：打开页面 → 等待加载 → 注入 collect SDK → 等待挂载 → 解析内容写入 `/tmp/ynote-clip-data.json`。

**agent 只读取 stdout 最后一行的 metadata JSON**（~200 字节），bodyHtml 留在文件中。

**失败处理**（遇到以下任一错误，直接使用 Fallback）:

| 错误类型 | 识别特征 | 原因 |
|----------|----------|------|
| **CSP 阻止** | `Content Security Policy`、`unsafe-eval`、`EvalError` | 页面禁止 eval（Twitter/X、银行等）|
| **SDK 注入失败** | `evaluate` 报错、文件不存在 | collect-window.js 丢失 |
| **内容为空** | `collectParser.parse()` 返回空 content | 需登录或被反爬拦截 |
| **超时** | `timeout`、`timed out` | 页面加载过慢或网络问题 |

遇到上述错误时，**不要重试 collect-page.sh**，直接跳到下方「Fallback：web_fetch 降级」。

#### Fallback：web_fetch 降级

> **适用场景**：collect-page.sh 执行失败（CSP 阻止、SDK 注入失败、超时等）时的降级方案。

执行以下 3 步：
1. 调用 `web_fetch` 工具获取页面 Markdown：
   ```
   web_fetch(url="<目标URL>", extractMode="markdown")
   ```
2. 将返回的 Markdown 内容组装为 JSON 并写入数据文件：
   ```json
   // 写入 /tmp/ynote-clip-data.json
   {"title": "页面标题", "content": "<web_fetch 返回的 Markdown>", "imageUrls": [], "source": "<原始URL>"}
   ```
   > `imageUrls` 留空（Markdown 中的图片链接会保留在 HTML 中，但不做 base64 内联）。
3. 调用 `clip-note.mjs` 加 `--markdown` flag（自动将 Markdown 转为 HTML）：
   ```bash
   source ~/.zshrc && node {baseDir}/clip-note.mjs \
     --data-file /tmp/ynote-clip-data.json \
     --markdown \
     --source-url "原始URL"
   ```
   > `--markdown` 会在处理图片前，先用内置 marked 将 Markdown 转为 HTML。title 由脚本从 data-file 自动读取并处理。

### 剪藏工作流

**Step 1**：按上方「网页内容提取流程」执行 bash 脚本，获取 metadata 和 `/tmp/ynote-clip-data.json`。

**Step 2**：处理图片 + 创建剪藏笔记（调用 `clip-note.mjs`）

从 data-file 读取所有数据，agent 无需传递 bodyHtml：

```bash
source ~/.zshrc && node {baseDir}/clip-note.mjs \
  --data-file /tmp/ynote-clip-data.json \
  --source-url "原始 URL"
```

> `source ~/.zshrc` 确保 `YNOTE_API_KEY` 等环境变量对 Node 进程可见（agent 执行环境不会自动继承 shell 配置文件中的 `export`）。
> `--title` 无需传递，脚本从 data-file 读取 title，自动完成净化和后缀追加。
> `--source-url` 会覆盖 data-file 中的 source。

脚本自动处理：
- 图片：5 路并发下载、宽度 > 1920px 缩放、> 512KB 渐进压缩（JPEG 80→60→40）、GIF 转静态 JPEG、base64 编码
- MCP：优先 `clipperSaveWithImages`，若 Tool 未实现自动降级为 `createNote`
- 限制：最多 20 张图片，单张 < 512KB（超过则压缩，压缩后仍超则跳过）

> 调试信息（🔍 前缀）默认不输出；开启调试模式后由脚本自动输出，无需手动 echo。

**Step 3**：确认成功，按下方「响应格式」输出结果。

## 响应格式（必须遵守）

剪藏完成后，脚本输出一行 JSON：`{"ok":true,"message":"<MCP 返回的原始文本>"}`。

**必须**按以下模板回复用户（根据实际值填充）：

```
📎 **网页剪藏完成**

| 项目 | 详情 |
|------|------|
| 📌 输入标题 | {笔记标题} |
| 📁 保存位置 | {从 message 中理解的保存位置} |
| 🔗 来源网址 | {用户提供的原始 URL} |
| ⏰ 剪藏时间 | {yyyy-MM-dd HH:mm} |

> 标题以实际保存为准，可能会调整
```

**字段说明**：
- **输入标题**：原始页面标题（脚本自动净化并追加 `.clip` 后缀，非最终保存标题）
- **保存位置**：阅读 `message` 字段内容，自行理解并提炼保存路径（如「我的资源/收藏笔记」）

### 剪藏后引导提示（Step 3 响应之后执行）

剪藏成功后，检查是否满足引导条件。**全部满足**时，在剪藏成功响应之后追加一句提示：

**条件**（缺一不可）：
1. 剪藏成功（脚本输出 `{"ok":true,...}`）
2. 最近收藏笔记数 ≥ 3：
   ```bash
   bash {baseDir}/mcp-call.sh getRecentFavoriteNotes '{"limit":3}'
   ```
   返回结果数 ≥ 3 即满足
3. 尚未设置资讯推送定时任务：
   ```bash
   openclaw cron list --json | jq '.[] | select(.name == "ynote-daily-briefing")'
   ```
   返回为空即满足

**错误处理**：
- 若 MCP 调用失败（exit code ≠ 0 或返回错误），视为条件不满足
- 若 cron 查询失败，视为条件不满足
- **静默跳过，不在聊天界面输出任何错误或诊断信息**

**提示内容**（追加在剪藏成功响应之后，空一行）：

```
💡 你已经收藏了 N 篇文章，试试说「资讯推送」看看 AI 为你整理的简报吧～
```

> N 为 `getRecentFavoriteNotes` 返回的实际条数。条件不满足时不显示任何提示。

## 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `YNOTE_API_KEY` | ✅ | — | MCP Server API Key |
| `YNOTE_MCP_URL` | — | `https://open.mail.163.com/api/ynote/mcp/sse` | MCP SSE 端点 |
| `YNOTE_MCP_TIMEOUT` | — | `30` | 超时秒数 |

## 常见问题

**Q: 剪藏超时？**
调大超时：`export YNOTE_MCP_TIMEOUT=60`

**Q: collect SDK 注入失败？**
确认 `{baseDir}/static/collect-window.js` 文件存在。文件丢失时需重新部署 Skill。

**Q: 图片无法显示？**
部分网站有防盗链，图片可能无法在笔记中正常显示。剪藏工作流会将图片 base64 编码上传，规避防盗链问题。

**Q: 笔记内容被截断？**
有道云笔记 API 对单次内容有长度限制（约 100KB）。超长内容需精简后再保存。

**Q: 如何切换浏览器可见/无头模式？**
安装脚本默认配置无头模式。切换命令：无头 `openclaw config set browser.headless true`，可见 `openclaw config set browser.headless false`。仅影响 `openclaw` 托管浏览器，不影响用户真实 Chrome（`chrome` profile）。
