---
name: xiaohongshu-post
description: |
  Create and publish Xiaohongshu (小红书/RED) notes. Use when: user wants to publish a note to Xiaohongshu,
  schedule or batch post content, generate Xiaohongshu-style titles/body/hashtags, or automate note publishing.
  Supports API posting (requires open platform credentials), browser automation (personal accounts), or draft generation.
metadata:
  openclaw:
    emoji: "📕"
    requires: { bins: ["python3"] }
  env:
    optional:
      # API 模式（企业号）
      - XIAOHONGSHU_APP_KEY
      - XIAOHONGSHU_APP_SECRET
      # 浏览器模式 - 页面分析器
      - DASHSCOPE_API_KEY
      - OPENAI_API_KEY
      - XHS_ANALYZER_BASE_URL
      - XHS_ANALYZER_MODEL
      - OPENAI_BASE_URL
      # 代理
      - HTTPS_PROXY
      - HTTP_PROXY
---

# Xiaohongshu Post Skill

Create and publish notes to Xiaohongshu (小红书/RED).

## ⚠️ 安全与隐私（浏览器模式必读）

**浏览器模式会将页面内容发送到 LLM 进行分析**。默认使用百炼（DashScope）等外部 API，页面 HTML 可能包含登录态、token、后台数据等敏感信息。

- **若仅需服务号发文**：请使用 **API 模式**（`post.py`），仅配置 `XIAOHONGSHU_APP_KEY`/`XIAOHONGSHU_APP_SECRET`，**不要**配置 `DASHSCOPE_API_KEY`/`OPENAI_API_KEY`。
- **若必须使用浏览器模式**：
  - 优先使用 **本地模型**（Ollama）：`XHS_ANALYZER_BASE_URL=http://localhost:11434/v1`，不配置 API Key。
  - 或使用自托管/可信端点，并限制 API Key 权限。
  - 若不配置分析器 Key，脚本会回退为需手动操作，页面内容不会外发。

脚本会对 HTML 做脱敏（移除 script/style、常见 token 模式），但无法完全消除敏感信息。请评估后再使用。

## When to Use

- "发小红书" / "自动发小红书" / "发一篇小红书笔记"
- "把这段内容发到小红书" / "创建小红书草稿"
- "生成小红书文案" / "小红书标题 + 正文 + 标签"

## 三种模式

| 模式 | 适用 | 脚本 |
|------|------|------|
| **API 发布** | 企业号、已认证开放平台 | `post.py` |
| **浏览器自动化** | 个人账号（无 API 权限） | `publish_browser.py` |
| **草稿输出** | 快速生成，手动发布 | `post.py --draft-only` |

---

## 模式一：API 发布（企业号）

### Prerequisites

- 小红书企业号或已认证开发者
- 开放平台权限
- 环境变量：`XIAOHONGSHU_APP_KEY`、`XIAOHONGSHU_APP_SECRET`

### 安装配置

1. **注册开发者**
   - 访问 [open.xiaohongshu.com](https://open.xiaohongshu.com)
   - 完成开发者实名认证（企业或个人）

2. **创建应用**
   - 在控制台创建新应用
   - 申请「笔记发布」相关接口权限
   - 获取 **App Key** 和 **App Secret**

3. **配置环境变量**
   ```bash
   export XIAOHONGSHU_APP_KEY=your_app_key
   export XIAOHONGSHU_APP_SECRET=your_app_secret
   ```

### Commands

```bash
# 发布笔记（带图片）
python3 scripts/post.py --title "上海探店 | 这家咖啡馆太绝了" \
  --content "周末和朋友一起来打卡..." \
  --image cover.jpg img2.jpg img3.jpg \
  --tags "探店，咖啡，上海"

# 纯文字笔记
python3 scripts/post.py --title "今日穿搭" \
  --content "OOTD | 简约风穿搭分享..." \
  --tags "穿搭，日常"

# JSON 输出（便于脚本集成）
python3 scripts/post.py --title "..." --content "..." --json
```

### 参数

- `--title`：标题（必填，≤20 字）
- `--content`：正文内容（必填）
- `--image`：图片路径，可多个（空格分隔）
- `--tags`：标签，逗号分隔
- `--draft-only`：仅输出草稿，不调用 API
- `--json`：JSON 格式输出

### 限制与注意事项

- **内容审核**：发布的笔记需经平台审核，违规内容会被拒绝
- **频率限制**：API 有调用次数限制，避免短时间内大量发帖
- **图片要求**：JPG/PNG，单张 ≤10MB，建议 3:4 或 1:1 比例
- **标题长度**：≤20 字
- **正文长度**：≤1000 字

---

## 模式二：浏览器自动化（个人账号）

适用于**个人账号**，无需 API 权限。**无硬编码**：每次打开或跳转页面后，等待 → 获取页面代码 → 由模型分析当前状态及下一步操作。

### 安装

```bash
pip install -r requirements.txt   # playwright + openai
playwright install chromium
export DASHSCOPE_API_KEY=...      # 百炼 API Key（与 OpenClaw 主模型一致）
```

### 使用

```bash
# 发布笔记（模型驱动：自动登录检测、填表、上传图片）
python3 scripts/publish_browser.py --title "标题" --content "正文" --images img1.jpg,img2.jpg

# 从文件读取正文
python3 scripts/publish_browser.py --title "标题" --content-file note.md --images img1.jpg

# 仅检测（模型分析当前页面状态）
python3 scripts/publish_browser.py --check-only

# 指定模型（默认 bailian/qwen3.5-plus）
python3 scripts/publish_browser.py --title "..." --content-file x.md --images x.jpg --model gpt-4o-mini

# 本地 Ollama（无需 API Key，隐私更安全）
XHS_ANALYZER_BASE_URL=http://localhost:11434/v1 XHS_ANALYZER_MODEL=llama3.2 \
  python3 scripts/publish_browser.py --title "..." --content-file x.md --images x.jpg
```

### 流程（模型驱动）

1. 打开 creator.xiaohongshu.com，**等待** → **获取页面 HTML** → **模型分析**
2. 模型返回：`state`（login_required / logged_in_dashboard / note_editor）和 `next_action`（wait_for_scan / goto_publish / click_new_note / fill_note / done）
3. 脚本执行对应操作，每次跳转后重复步骤 1
4. 无硬编码特征，模型根据页面内容动态决策

### 参数

- `--title`：标题（必填，`--check-only` 时可不填，≤20 字）
- `--content` / `--content-file`：正文，支持 Markdown（≤1000 字）
- `--images`：图片路径，逗号分隔（1-9 张，建议 3:4 或 1:1）
- `--tags`：话题标签，逗号分隔（如：#穿搭 #日常）
- `--model`：分析用 LLM 模型（默认 qwen3.5-plus，百炼）
- `--headed` / `--headless`：是否显示浏览器
- `--user-data-dir`：浏览器配置目录（默认 `~/.openclaw/xhs-browser`）
- `--step`：每步截图并自动继续
- `--check-only`：仅分析当前页面状态
- `--debug`：保存截图和 HTML

### 环境变量

- `DASHSCOPE_API_KEY` / `OPENAI_API_KEY`：外部 API Key（**不配置则使用本地模型或回退手动**）
- `XHS_ANALYZER_BASE_URL`：分析器端点。**本地 Ollama**：`http://localhost:11434/v1`（无需 Key）
- `XHS_ANALYZER_MODEL`：模型名，默认 qwen3.5-plus；Ollama 用 `llama3.2` 等

### 注意

- 小红书后台 UI 可能更新，若选择器失效需调整脚本
- 登录状态保存在 `~/.openclaw/xhs-browser`，勿删除
- 图片建议尺寸：900×1200（3:4）或 1080×1080（1:1）

---

## 模式三：草稿输出（快速生成）

无 API 凭证时，自动生成格式化草稿，可手动复制到小红书 APP 发布。

```bash
# 生成草稿（带标签）
python3 scripts/post.py --draft-only \
  --title "周末穿搭分享" \
  --content "今天分享一套超好看的春日穿搭..." \
  --tags "穿搭，春日，OOTD"

# 从文件读取内容
python3 scripts/post.py --draft-only \
  --title "上海探店" \
  --content "$(cat note.md)" \
  --tags "探店，咖啡"
```

输出示例：

```
--- 小红书草稿（复制到 APP 发布） ---

标题：周末穿搭分享

正文:
今天分享一套超好看的春日穿搭...

标签：#穿搭 #春日 #OOTD

---
```

---

## Path

From workspace root:

```bash
# API 发布
python3 skills/xiaohongshu-post/scripts/post.py --title "..." --content "..." --image x.jpg --tags "标签 1，标签 2"

# 浏览器自动化（个人账号）
python3 skills/xiaohongshu-post/scripts/publish_browser.py --title "..." --content-file x.md --images x.jpg,y.jpg

# 草稿输出
python3 skills/xiaohongshu-post/scripts/post.py --draft-only --title "..." --content "..." --tags "标签 1，标签 2"
```

## Content Format

- 标题 ≤ 20 字
- 正文 ≤ 1000 字，支持换行
- 标签自动转为 `#标签` 格式
- 图片 1-9 张，JPG/PNG，单张 ≤10MB
