---
name: xiaohongshu-note-fetcher
description: 抓取并整理小红书笔记公开页面信息（标题、正文摘要、作者、发布时间、互动数据、标签、封面图等）为结构化 JSON 或 Markdown。用于“根据笔记链接提取内容”“批量收集笔记基础信息”“生成笔记摘要素材”等场景；当用户提供小红书笔记 URL、URL 列表或需要导出机器可读结果时触发。
---

# 小红书笔记获取

## 极简规则

输入 `TikHub API Key` + `需求（关键词、页码）` 即可抓取小红书搜索数据。

最小示例：

```bash
make tikhub-fetch \
  KEYWORD="女性力量" \
  TIKHUB_PAGE=2 \
  TIKHUB_TOKEN="<YOUR_TIKHUB_KEY>" \
  TIKHUB_ENDPOINT=web \
  TIKHUB_AUTH_MODE=bearer
```

输出文件：
- `workspace/xiaohongshu-note-fetcher-skill-data/tikhub_search_page2.json`

## 快速开始

1. 收集输入来源：
- 单条链接：直接给 URL。
- 批量链接：准备一个文本文件，每行一个 URL。
- 若目标页面需登录态：提供 Cookie 字符串或 Cookie 文件。

2. 运行脚本抓取（页面解析模式）：

```bash
python3 scripts/fetch_xiaohongshu_notes.py \
  --url "https://www.xiaohongshu.com/explore/<note_id>" \
  --format both \
  --output result.json
```

3. 批量抓取示例：

```bash
python3 scripts/fetch_xiaohongshu_notes.py \
  --url-file ./urls.txt \
  --format json \
  --output notes.json
```

4. 运行 TikHub API 搜索（推荐用于关键词搜笔记）：

```bash
python3 scripts/search_notes_tikhub.py \
  --token "<YOUR_TIKHUB_TOKEN>" \
  --keyword "女性主义" \
  --page 1 \
  --output search_page1.json
```

也可以使用 Makefile 一键调用（推荐长期使用）：

```bash
make tikhub-fetch \
  KEYWORD="美食" \
  TIKHUB_TOKEN="<YOUR_TIKHUB_TOKEN>" \
  TIKHUB_ENDPOINT=web \
  TIKHUB_AUTH_MODE=bearer
```

若你不想每次手输 token，可把 token 放到文件（如 `./.tikhub_token`）：

```bash
make tikhub-fetch \
  KEYWORD="美食" \
  TIKHUB_TOKEN_FILE=./.tikhub_token \
  TIKHUB_ENDPOINT=web \
  TIKHUB_AUTH_MODE=bearer
```

5. 使用其他服务商 API（通用适配）：

```bash
python3 scripts/search_notes_generic.py \
  --base-url "https://your-api.example.com/search_notes" \
  --auth-mode bearer \
  --auth-header Authorization \
  --token "<YOUR_API_TOKEN>" \
  --keyword "美食推荐" \
  --page 1 \
  --param sort_type=general \
  --output generic_search.json
```

6. 从 TikHub 响应生成文章列表（按点赞过滤）：

```bash
python3 scripts/build_article_list_from_tikhub.py \
  --input ./tikhub_search.json \
  --min-likes 1000 \
  --rank-by hot \
  --md-output ./xhs_article_list.md \
  --csv-output ./xhs_article_list.csv \
  --json-output ./xhs_article_list.json \
  --template-output ./xhs_publish_templates.md
```

7. 自动翻页抓取并合并（直接调 TikHub）：

```bash
python3 scripts/build_article_list_from_tikhub.py \
  --token "<YOUR_TIKHUB_TOKEN>" \
  --keyword "美食" \
  --pages 5 \
  --sort general \
  --note-type _0 \
  --min-likes 1000 \
  --rank-by hot \
  --top 50
```

8. 交互式筛选与查看（会先问你筛选方式，含默认方案）：

```bash
python3 scripts/interactive_filter_view.py \
  --input ./tikhub_search.json
```

直接回车会采用默认方案：
- 点赞阈值：`1000`
- 排序：`hot`（综合热度）
- 条数：`20`
- 查看：`summary`
- 同时导出 `md/csv`

若你不想交互，直接用默认方案：

```bash
python3 scripts/interactive_filter_view.py \
  --input ./tikhub_search.json \
  --non-interactive
```

9. 导图输出（保留）：

```bash
python3 scripts/generate_wow_pack.py \
  --input ./xhs_article_list.json \
  --keyword 美食 \
  --url-output ./xhs_topic_mindmap_url.txt
```

6. 本机浏览器抓取（不走第三方 API，推荐）：

```bash
node scripts/fetch_xiaohongshu_note_playwright.js \
  --url "https://www.xiaohongshu.com/explore/<note_id>" \
  --cookie-file ./cookie.txt \
  --output note_browser.json \
  --screenshot note_browser.png \
  --html-out note_browser.html
```

若首次运行提示 `playwright_not_installed`，先安装：

```bash
cd scripts
npm i playwright
npx playwright install chromium
```

## 参数说明

- `--url`: 单条小红书笔记 URL。
- `--url-file`: 批量 URL 文件（每行一个 URL，支持 `#` 注释行）。
- `--cookie`: 原始 Cookie 请求头字符串。
- `--cookie-file`: Cookie 文件（纯文本 Cookie 字符串）。
- `--format`: `json`、`md`、`both`，默认 `json`。
- `--output`: 输出路径；`json`/`both` 写该文件，`md` 会在同目录生成 `.md`。
- `--timeout`: 请求超时秒数，默认 `20`。
- `search_notes_tikhub.py` 关键参数：
- `--keyword`、`--page` 必填。
- `--sort-type` 可选：`general`、`time_descending`、`popularity_descending` 等。
- `--note-type` 支持中英文：`不限`/`all`、`视频笔记`/`video`、`普通笔记`/`image`、`直播笔记`/`live`。
- `--time-filter` 支持中英文：`不限`/`all`、`一天内`/`day`、`一周内`/`week`、`半年内`/`half_year`。
- `--ai-mode` 使用整数 `0` 或 `1`。
- `search_notes_generic.py` 关键参数：
- `--base-url`：新 API 的搜索端点。
- `--auth-mode`：`none`、`bearer`、`apikey`。
- `--auth-header`：鉴权头名称，默认 `Authorization`。
- `--keyword-param` / `--page-param`：当对方字段不是 `keyword/page` 时改这里。
- `--param key=value`：补充任意查询参数，可重复。
- `--header key=value`：补充任意请求头，可重复。
- `fetch_xiaohongshu_note_playwright.js` 关键参数：
- `--url`：笔记 URL。
- `--cookie-file`：浏览器 Cookie 文本（建议提供，提高字段完整度）。
- `--headed`：显示浏览器窗口调试。
- `--screenshot` / `--html-out`：输出调试文件，方便排查风控页和登录页。

`--url` 与 `--url-file` 至少给一个。

## 工作流程

1. 读取 URL 列表。
2. 发送 HTTP 请求拉取页面 HTML（带浏览器 UA，可选 Cookie）。
3. 从页面中提取：
- OpenGraph 元信息（`og:title`、`og:description`、`og:image`）
- JSON-LD（发布时间、作者、关键词、互动统计）
- 页面脚本中的 `noteId`（若存在）
4. 产出统一字段结构，见 `references/output-schema.md`。

## 常见问题处理

1. 仅返回基础字段或计数缺失：
- 小红书前端结构会变化，且部分互动字段需要更完整会话态；优先补充 `--cookie` 后重试。

2. 返回 403 或风控页：
- 更换网络环境或降低抓取频率，避免高并发。
- 仅用于你有权访问的数据，不要绕过平台安全机制。

3. 需要深度字段（如评论明细）：
- 本 skill 默认仅做页面级基础信息抽取；如需更深层数据，先确认合规性，再扩展独立脚本。

4. TikHub `400 Request failed`：
- 首次请求尽量只保留 `keyword`、`page`，确认成功后再加筛选项。
- 避免把数值参数写成字符串语义值：`page` 用整数、`ai_mode` 用 `0/1`。
- 分页时优先使用上一页返回的 `search_id`、`search_session_id`。
- 先用官方默认演示参数跑通，再逐项加入自定义参数。

## 合规边界

- 只抓取你有权限访问的公开或授权内容。
- 遵守小红书服务条款、robots、隐私和数据保护要求。
- 不执行账号盗用、验证码绕过、反爬绕过等违规行为。

## 资源

- 脚本：[scripts/fetch_xiaohongshu_notes.py](scripts/fetch_xiaohongshu_notes.py)
- API 搜索脚本：[scripts/search_notes_tikhub.py](scripts/search_notes_tikhub.py)
- 通用 API 适配脚本：[scripts/search_notes_generic.py](scripts/search_notes_generic.py)
- 响应转列表脚本：[scripts/build_article_list_from_tikhub.py](scripts/build_article_list_from_tikhub.py)
- 交互筛选脚本：[scripts/interactive_filter_view.py](scripts/interactive_filter_view.py)
- 惊艳组合脚本：[scripts/generate_wow_pack.py](scripts/generate_wow_pack.py)
- 浏览器抓取脚本：[scripts/fetch_xiaohongshu_note_playwright.js](scripts/fetch_xiaohongshu_note_playwright.js)
- 字段说明：[references/output-schema.md](references/output-schema.md)
