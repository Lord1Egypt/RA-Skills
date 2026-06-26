---
name: wechat-official-account
description: |
  Create and publish WeChat Official Account (公众号) articles. Use when: (1) User wants to auto-post
  to WeChat Official Account, (2) Create draft from title + content, (3) Publish draft to 公众号,
  (4) Schedule or automate 公众号 article publishing. Supports API (服务号) and browser automation (个人订阅号).
  Browser mode: interactive QR login, login detection via page HTML analysis.
metadata:
  openclaw:
    emoji: "📱"
    requires: { bins: ["python3"] }
  env:
    optional:
      - WECHAT_APPID
      - WECHAT_SECRET
      - DASHSCOPE_API_KEY
      - HTTPS_PROXY
      - HTTP_PROXY
---

# WeChat Official Account Skill

Create drafts and publish articles to WeChat Official Account (微信公众号).

## ⚠️ 安全与隐私（浏览器模式必读）

**浏览器模式会将页面内容发送到 LLM 进行分析**。默认使用百炼（DashScope）等外部 API，页面 HTML 可能包含登录态、token、后台数据等敏感信息。

- **若仅需服务号发文**：请使用 **API 模式**（`publish.py`），仅配置 `WECHAT_APPID`/`WECHAT_SECRET`，**不要**配置 `DASHSCOPE_API_KEY`/`OPENAI_API_KEY`。
- **若必须使用浏览器模式**：
  - 优先使用 **本地模型**（Ollama）：`WECHAT_MP_ANALYZER_BASE_URL=http://localhost:11434/v1`，不配置 API Key。
  - 或使用自托管/可信端点，并限制 API Key 权限。
  - 若不配置分析器 Key，脚本会回退为需手动操作，页面内容不会外发。

脚本会对 HTML 做脱敏（移除 script/style、常见 token 模式），但无法完全消除敏感信息。请评估后再使用。

## When to Use

- "发公众号" / "自动发公众号" / "发一篇公众号文章"
- "把这段内容发到公众号" / "创建公众号草稿"
- "定时发公众号" / "公众号自动发文"

## 两种方案

| 方案 | 适用 | 脚本 |
|------|------|------|
| **API** | 服务号、认证订阅号 | `publish.py` |
| **浏览器自动化** | 个人订阅号（无 API 权限） | `publish_browser.py` |

---

## 方案一：API（服务号）

### Prerequisites

- 服务号或认证订阅号
- 环境变量：`WECHAT_APPID`、`WECHAT_SECRET`
- IP 白名单

### Commands

```bash
python3 scripts/publish.py --title "标题" --content "正文" --cover cover.jpg [--publish]
```

---

## 方案二：浏览器自动化（个人订阅号）

适用于**个人订阅号**，无需 AppID/AppSecret。**无硬编码**：每次打开或跳转页面后，等待 → 获取页面代码 → 由模型分析当前状态及下一步操作。

### 安装

```bash
pip install -r requirements.txt   # playwright + openai
playwright install chromium
export DASHSCOPE_API_KEY=...      # 百炼 API Key（与 OpenClaw 主模型一致）
```

### 使用

```bash
# 首次运行：打开浏览器，模型分析页面后决定是否提示扫码
python3 scripts/publish_browser.py --title "标题" --content "正文" --cover cover.jpg

# 从文件读取正文
python3 scripts/publish_browser.py --title "标题" --content-file article.md --cover cover.jpg

# 仅检测（模型分析当前页面状态）
python3 scripts/publish_browser.py --check-only

# 指定模型（默认 bailian/qwen3.5-plus）
python3 scripts/publish_browser.py --title "..." --content-file x.md --model gpt-4o-mini

# 本地 Ollama（无需 API Key，隐私更安全）
WECHAT_MP_ANALYZER_BASE_URL=http://localhost:11434/v1 WECHAT_MP_ANALYZER_MODEL=llama3.2 \
  python3 scripts/publish_browser.py --title "..." --content-file x.md
```

### 流程（模型驱动）

1. 打开 mp.weixin.qq.com，**等待** → **获取页面 HTML** → **模型分析**
2. 模型返回：`state`（login_required / logged_in_dashboard / draft_editor）和 `next_action`（wait_for_scan / goto_draft / click_new_draft / fill_article / done）
3. 脚本执行对应操作，每次跳转后重复步骤 1
4. 无硬编码特征，模型根据页面内容动态决策

### 参数

- `--title`：标题（必填，`--check-only` 时可不填）
- `--content` / `--content-file`：正文，支持 Markdown
- `--cover`：封面图路径（建议 900×500）
- `--author`：作者名（可选）
- `--model`：分析用 LLM 模型（默认 qwen3.5-plus，百炼）
- `--headed` / `--headless`：是否显示浏览器
- `--user-data-dir`：浏览器配置目录（默认 `~/.openclaw/wechat-mp-browser`）
- `--step`：每步截图并自动继续
- `--check-only`：仅分析当前页面状态
- `--debug`：保存截图和 HTML

### 环境变量

- `DASHSCOPE_API_KEY` / `OPENAI_API_KEY`：外部 API Key（**不配置则使用本地模型或回退手动**）
- `WECHAT_MP_ANALYZER_BASE_URL`：分析器端点。**本地 Ollama**：`http://localhost:11434/v1`（无需 Key）
- `WECHAT_MP_ANALYZER_MODEL`：模型名，默认 qwen3.5-plus；Ollama 用 `llama3.2` 等

### 注意

- 公众号后台 UI 可能更新，若选择器失效需调整脚本
- 登录状态保存在 `~/.openclaw/wechat-mp-browser`，勿删除

---

## Path

From workspace root:

```bash
# API
python3 skills/wechat-official-account/scripts/publish.py --title "..." --content "..." --cover x.jpg

# 浏览器（模型驱动：每次跳转后获取页面→模型分析→执行）
python3 skills/wechat-official-account/scripts/publish_browser.py --title "..." --content-file x.md --cover x.jpg

# 仅分析当前页面
python3 skills/wechat-official-account/scripts/publish_browser.py --check-only
```

## Content Format

- Markdown 会转为 HTML（`\n` → `<br>`，`**bold**` → `<b>bold</b>`）
- 正文 < 2 万字符，标题 ≤ 32 字
