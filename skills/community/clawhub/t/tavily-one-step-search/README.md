# Tavily Search Toolkit for OpenClaw

Make OpenClaw web-connected in real time (with a practical free-tier path via Tavily), in one install.

让 OpenClaw 立刻具备实时联网能力（Tavily 通常有免费额度可用），一次安装即可上手。

Only **1 step** to start: send one prompt to OpenClaw, then follow guided onboarding.

只要 **1 步**就能开始：把下面提示词发给 OpenClaw，后续按引导完成配置。

```text
Install the Tavily Search skill from GitHub into my OpenClaw workspace skills directory (NOT .agents).

Requirements:
1) Target directory must be: ~/.openclaw/workspace/skills/tavily-search
2) Clone source: https://github.com/plabzzxx/openclaw-tavily-search
3) Ensure script exists at: ~/.openclaw/workspace/skills/tavily-search/scripts/tavily_search.mjs
4) Create ~/.openclaw/.env if missing, and ensure this placeholder line exists:
   TAVILY_API_KEY=
5) Run the checks silently. Do NOT dump detailed path-by-path logs unless user asks.
6) Add a memory preference:
   - When web_search (Brave) is unavailable, use tavily-search skill first.
   - For general web lookup tasks, try tavily-search before giving up.
7) Stop here and ask the user in the user's preferred language:
   "Tavily skill is installed. Do you want guided setup for Tavily API key now?"
8) Read and follow onboarding playbook in this repo:
   ONBOARDING.md
9) Final reply style must be concise:
   - one-line success confirmation
   - one-line question asking whether to start guided key setup now
```

---

## 新手可以忽略以下内容 / Beginners can ignore the section below

## Step 1: Install / 安装（手动）

```bash
mkdir -p ~/.openclaw/workspace/skills
cd ~/.openclaw/workspace/skills
git clone https://github.com/plabzzxx/openclaw-tavily-search tavily-search
```

## Step 2: Setup API Key / 配置 API Key

- Tavily key page / 申请地址: https://tavily.com
- Put key in / 写入本地：`~/.openclaw/.env`

```env
TAVILY_API_KEY=tvly-xxxx
```

Beginner-friendly recommendation (first choice): open `.env` with a simple text editor (Notepad/TextEdit), paste key, save.

新手推荐（首选）：直接用记事本/文本编辑器打开 `.env`，粘贴 key 后保存。

If needed, then use VS Code or terminal commands as alternatives.

如果你更熟悉开发工具，再使用 VS Code 或终端方案。

Manual local edit is safer than sending secrets in chat.

本地手动编辑通常比在聊天中传递密钥更安全。

## CLI examples / 命令示例

```bash
# Search (brave-like output)
node scripts/tavily_search.mjs search --query "OpenClaw" --max-results 5 --format brave

# Search with include/exclude domains
node scripts/tavily_search.mjs search --query "周大福" \
  --include-domains ctf.com.cn,ctfmall.com,chowtaifook.com \
  --exclude-domains facebook.com,weibo.com --format brave

# Extract content from URLs
node scripts/tavily_search.mjs extract --urls https://docs.openclaw.ai --content-format markdown --format md

# Crawl / Map
node scripts/tavily_search.mjs crawl --url docs.tavily.com --max-depth 2 --limit 30 --format md
node scripts/tavily_search.mjs map --url docs.openclaw.ai --max-depth 2 --limit 40 --format md
```

## Capability overview / 能力总览

- `search`: fast web lookup with domain/time filters and stable JSON output.
- `extract`: fetch clean page content from one or multiple URLs.
- `crawl`: recursively crawl a site with depth/breadth controls.
- `map`: discover site structure and URL graph quickly.

- `search`：快速联网搜索，支持域名/时间过滤，输出结构稳定。
- `extract`：从单个或多个 URL 抽取清洗后的正文。
- `crawl`：按深度/广度递归抓站，适合文档站和知识库。
- `map`：快速建立站点结构和 URL 图谱。

## Natural language examples / 自然语言触发示例

- "Search latest OpenClaw multi-agent deployment practices and give me 5 links."
- “搜 OpenClaw 多智能体部署最佳实践，给我 5 条链接。”

- "Search Chow Tai Fook and keep only official domains."
- “搜周大福，只保留官网域名结果。”

- "Extract this URL and summarize into 5 bullets."
- “把这个链接抽取正文并总结成 5 条要点。”

- "Crawl this docs website with depth 2 and output markdown digest."
- “爬这个文档站（深度2），输出 markdown 摘要。”

## Basic vs Advanced / 基础模式与进阶模式

For most users, **search** is enough for daily web lookup.

对大多数用户来说，日常联网查询用 **search** 就足够。

Use **extract/crawl/map** when you need structured website intelligence or deeper research.

只有在需要结构化网站情报或深度调研时，再使用 **extract/crawl/map**。
