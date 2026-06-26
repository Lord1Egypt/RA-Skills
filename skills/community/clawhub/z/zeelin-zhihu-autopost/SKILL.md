---
name: ZeeLin 知乎自动发布
description: "用户给出选题，小龙虾爬取信息、整理成一篇深度有创新的文章，展示给用户确认后一键发布到知乎。用户只需登录知乎并在确认后点击「确定」，Agent 负责选题调研、成文与浏览器端自动填入并发布。Keywords: Zeelin, ZeeLin, 知乎, 自动发布, 选题, 深度文章, 一键发布."
user-invocable: true
metadata: {"openclaw":{"emoji":"📝","skillKey":"zeelin-zhihu-autopost"}}
---

# ZeeLin 知乎自动发布 📝

用户给一个**选题** → 小龙虾**爬取信息、整理成深度有创新的文章** → 展示给用户 → 用户说**「确定」「发布」** → 小龙虾用脚本在知乎写文章页**自动填入标题和正文并点击发布**。你只需登录知乎并点一次确定。

---

## ⚠️ 避免 request timed out（必读）

**严禁在同一轮内既「爬取+成文」又「写文件+exec 发布」**。单轮耗时过长会导致 request timed out。

**必须拆成两轮：**
- **第一轮**：只做爬取（web_fetch）+ 成文，把**标题和正文**发给用户，并说明：「请先登录知乎。确认无误后回复 **『发布』**，我再执行发布。」
- **第二轮**：等用户回复「发布」后，只做「将正文写入 `/tmp/zhihu_body.md` + exec 发布脚本（带 timeout 90000）」，不再重复爬取或成文。

即使用户一次说「爬取最新 AI 动态并发布到知乎」，你也**先只完成爬取和成文并展示**，等用户说「发布」后再执行发布。

**飞书 / 易超时环境下的「轻量第一轮」**：当用户说「爬取最新动态」并写知乎时，第一轮**不要**做大量爬取+整篇长文（容易单轮超时）。改为：**至多 1～2 次 web_fetch**，然后产出**短稿（约 500～800 字）或「大纲 + 首段」**，先快速回复；并说明：「这是首稿/大纲，需要全文请回复『展开成全文』，要发布请回复『发布』。」用户回复后再补全或发布，可显著降低 request timed out。

---

## 何时触发

- 「帮我发一篇知乎」「把这篇发到知乎」
- 「做个知乎选题：XXX」「以 XXX 为题写一篇知乎文章并发布」
- 「帮我写一篇知乎深度文，选题是 XXX，写好我确认后你发」
- 「知乎自动发布」「用小龙虾发知乎」
- **「爬取最新动态，写一篇知乎文章」**「爬取最新动态写知乎」「根据最新动态写一篇知乎」

---

## 知乎 API 在哪调

- **开放平台**：https://dev.zhihu.com/ — 注册应用、OAuth 2.0 获取 `access_token`。**注意**：知乎发布 API 目前仅对内侧用户开放，多数用户无法使用。
- **发布文章接口**（内侧）：一般为 `POST https://api.zhihu.com/v4/articles`。未开放前请用下方「网页端直接发布」。
- **本 skill 发布方式**：
  1. **API 发布**（仅内侧可用）：若环境变量已设置 `ZHIHU_ACCESS_TOKEN`，使用 `scripts/publish_via_api.sh`。
  2. **网页端直接发布（推荐）**：使用 `scripts/publish_article.sh`，在**已打开的知乎写文章页**上填表并点击发布；配合 **Browser Relay** 可大幅缩短耗时、降低 request timed out（见下）。

---

## 网页端直接发布（Browser Relay，参考 ClawHub zhihu-post）

与 [ClawHub 上的知乎发帖 skill](https://clawhub.ai/InuyashaYang/zhihu-post) 思路一致：**在网页端直接发布**，由 Agent 控制已打开的浏览器标签页完成填表与点击，无需知乎开放 API。

**推荐流程（耗时短、不易超时）：**

1. **安装 OpenClaw Browser Relay**：Chrome 扩展，让 Agent 控制你当前标签页。安装：`openclaw browser extension install`，在 Chrome 加载该扩展；详见 [Chrome extension (browser relay)](https://learnclawdbot.org/docs/tools/chrome-extension)。
2. **先打开知乎写文章页**：在 Chrome 打开 https://www.zhihu.com ，登录后进入「创作」→「写文章」，停留在**空编辑器页**（有标题框和正文区）。
3. **挂上 Relay**：在该标签页点击扩展图标，使 Badge 显示 **ON**（表示该页已交给 OpenClaw 控制）。
4. **发布时**：用户说「发布」后，用 **已打开编辑器页** 的方式执行脚本，即传 `ZHIHU_ALREADY_ON_EDITOR=1`，脚本**不再**打开知乎、不再点击「写文章」，只做：snapshot → 填标题 → 填正文 → 点发布。整体耗时可从 30～90 秒降到约 10～20 秒，显著降低飞书等环境的 request timed out。

**exec 示例（已打开写文章页时）：**

```json
{"tool": "exec", "args": {"command": "ZHIHU_ALREADY_ON_EDITOR=1 bash ~/.openclaw/workspace/skills/zeelin-zhihu-autopost/scripts/publish_article.sh \"文章标题\" /tmp/zhihu_body.md", "timeout": 60000}}
```

**可选：用 browser 工具分步发布**（不用 exec 脚本）：若当前已 attach 知乎写文章页，可依次调用：`browser` snapshot → 从 snapshot 中找标题输入框与正文编辑区的 ref → `browser` type/fill 填入标题和正文 → `browser` snapshot 找发布按钮 ref → `browser` click 发布。每一步为单独工具调用，适合希望完全用 browser 控制的场景。

---

## 使用前准备（必读）

1. **用户需先登录知乎**（浏览器方式）：用 `exec` 或 `browser` 打开 https://www.zhihu.com ，让用户完成登录。若使用 **网页端直接发布 + Browser Relay**，用户在自己 Chrome 打开知乎写文章页并挂上扩展即可。
2. **可选**：若已知「写文章」直达链接，可先打开写文章页；发布时传 `ZHIHU_ALREADY_ON_EDITOR=1` 可跳过导航，减少超时。

---

## 工作流程

### Step 1：确认选题

用户给出选题（一句话或一个方向）。若未给，询问：「请给一个知乎文章选题或方向。」

### Step 2：爬取信息并成文

- **优先用 web_fetch** 抓取与选题相关的网页（如科技媒体、知乎话题页等 URL），获取最新内容。若 **web_search 不可用**（如缺少 Brave API 密钥），**不要**因此放弃任务：用 web_fetch 抓取你已知的新闻/资讯链接，或基于已有知识成文。
- 整理成一篇**深度、有创新、结构清晰**的文章（建议 1500～4000 字）：
  - 标题：吸引点击、概括主题
  - 正文：分段、小标题、有论据与观点，可适当引用来源
- **不要**在未获得用户确认前就发布。

### Step 3：展示并请用户确认

把**标题**和**正文全文**发给用户，并说明：

> 「这是根据选题整理的文章。请先登录知乎（若尚未登录）。确认无误后回复 **『确定』或『发布』**，我会帮你在知乎上自动填入并发布。」

### Step 4：用户说「确定」或「发布」后

**4.1 必须先写入正文文件（否则会报「正文文件不存在」）**

在调用发布脚本**之前**，必须把确认后的**正文全文**写入一个文件，例如 `/tmp/zhihu_body.md` 或 workspace 内路径（如 `~/.openclaw/workspace/zhihu_draft_body.md`）。用 `write` 工具或 `exec` 写入均可，确保文件存在且内容为 Markdown 正文。

**4.2 再执行发布脚本**

先写正文到 `/tmp/zhihu_body.md`，再 exec 发布脚本。

- **若已配置 ZHIHU_ACCESS_TOKEN（推荐）**：用 API 发布，耗时短、不易超时，timeout 可设 15000～30000：
```json
{"tool": "exec", "args": {"command": "bash ~/.openclaw/workspace/skills/zeelin-zhihu-autopost/scripts/publish_via_api.sh \"文章标题\" /tmp/zhihu_body.md", "timeout": 30000}}
```
- **未配置 token**：用浏览器脚本。若用户**已打开知乎写文章页并挂上 Browser Relay**，用 `ZHIHU_ALREADY_ON_EDITOR=1`，timeout 可设 60000；否则完整流程需 **timeout 90000 或 120000**：
```json
{"tool": "exec", "args": {"command": "ZHIHU_ALREADY_ON_EDITOR=1 bash ~/.openclaw/workspace/skills/zeelin-zhihu-autopost/scripts/publish_article.sh \"文章标题\" /tmp/zhihu_body.md", "timeout": 60000}}
```
或（未预先打开写文章页时）：
```json
{"tool": "exec", "args": {"command": "bash ~/.openclaw/workspace/skills/zeelin-zhihu-autopost/scripts/publish_article.sh \"文章标题\" /tmp/zhihu_body.md", "timeout": 90000}}
```

❌ 错误：未先写入文件就直接执行（会报「正文文件不存在」）；或浏览器方式未传 timeout 导致 request timed out。  
✅ 正确：先写正文到 `/tmp/zhihu_body.md`，再 exec；已打开写文章页时加 `ZHIHU_ALREADY_ON_EDITOR=1` 可缩短耗时。

### Step 5：回报结果

根据 exec 输出告诉用户：发布成功 / 失败；若失败，提示用户检查是否已登录、是否在写文章页，或重试。

---

## exec 命令速查

| 操作 | 命令与 timeout |
|------|------|
| **API 发布**（需 `ZHIHU_ACCESS_TOKEN`，仅内侧可用） | `bash .../publish_via_api.sh "标题" /tmp/zhihu_body.md`，args 加 `"timeout": 30000` |
| **网页端发布（已打开写文章页 + Relay）** | `ZHIHU_ALREADY_ON_EDITOR=1 bash .../publish_article.sh "标题" /tmp/zhihu_body.md`，args 加 `"timeout": 60000` |
| 浏览器发布（从零打开页） | `bash .../publish_article.sh "标题" /tmp/zhihu_body.md`，args 加 `"timeout": 90000` |
| 浏览器发布（标题 + stdin） | `cat body.md \| bash .../publish_article.sh "标题" -`，args 加 `"timeout": 90000` |

- **API 脚本**：仅知乎内侧可用；直接 POST 开放平台接口，数秒内完成。
- **网页端直接发布**：用户先在 Chrome 打开知乎写文章页并挂上 Browser Relay，再执行脚本时加 `ZHIHU_ALREADY_ON_EDITOR=1`，只做填表+点击，约 10～20 秒，不易超时。
- **浏览器脚本（从零）**：打开知乎创作/写文章页 → 填入标题和正文 → 点击「发布」；耗时长，需 timeout 90000。

---

## 重要规则

- **未确认不发布**：必须等用户明确说「确定」「发布」后再执行发布脚本。
- **先写文件再发布**：执行 publish_article.sh 前，**必须先**将正文写入文件（如 `/tmp/zhihu_body.md`），再传该路径给脚本，否则会报「正文文件不存在」。
- **发布必须用 exec**：用脚本统一完成打开页面、填入、点击发布，不要用 browser 工具一步步手动点。
- **登录由用户完成**：不在脚本或 Agent 中输入知乎账号密码；只操作已登录状态下的写文章页。
- **无 web_search 时照常成文**：若缺少 Brave Search API 密钥导致 web_search 不可用，用 web_fetch 抓取链接或基于知识成文，不要向用户报「需要 API 密钥」并停止任务。
- **两轮发布防超时**：第一轮只成文并展示，等用户说「发布」后第二轮再写文件+exec；不要在同一轮内成文又发布，否则易 request timed out。

---

## 技术说明

- 知乎写文章页：通常从 https://www.zhihu.com 进入创作中心 → 写文章；或已知直达链接时直接打开。
- 脚本依赖 `openclaw browser`：打开页面、snapshot 找元素、type/fill、click 发布。
- 若页面结构变化导致找不到标题/正文/发布按钮，脚本会输出错误信息，便于排查或更新选择器。
- **若脚本报「未找到发布按钮」**：通常标题和正文已填入编辑器，请用户在**当前已打开的浏览器页面**中手动点击「发布」或「发表」即可完成发布。
