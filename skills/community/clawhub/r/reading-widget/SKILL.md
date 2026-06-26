---
name: reading-widget
description: 在 macOS 桌面上放一个微信读书数据小卡片，自动显示连续阅读天数、今日/本月阅读时长（可点开看本周/今年对比）、本月目标进度、当前在读、年度读完本数和当下金句。安装后通过 Chrome --app 模式打开成无边框窗口贴在屏幕角落。触发：用户说"装阅读 widget"、"做个读书桌面小卡片"、"reading widget"、"放个微信读书的桌面 widget"、"我想 track 我的阅读"。
version: 1.1.1
---

# Reading Widget — 微信读书桌面小卡片

把当前用户的微信读书数据渲染成一个 264px 宽的暗色小卡片（Material 3 配色），放在桌面上。

数据由一个本地小后台 `server.py`（`127.0.0.1:47900`）提供：它一边按 http 把卡片发给浏览器，一边每 30 分钟自动重抓一次微信读书数据，并接收卡片上手动改目标的请求写回 `config.json`。所以目标改了重启不丢、数据不用手动 update。

## 安装流程（Claw 按顺序执行）

### Step 1 — 确认前置依赖

1. 检查 `WEREAD_API_KEY` 是否已设置：
   - 先看 `~/.claw/settings.json`（Claude Code 用户为 `~/.claude/settings.json`）的 `env` 字段
   - 再看当前 shell 环境变量
2. **如果没有 API key**：
   - 告诉用户 key 格式是 `wrk-xxxxxxxx`，绑定用户身份（vid）
   - 让用户参考微信读书官方 skill 包获取：`https://cdn.weread.qq.com/skills/weread-skills.zip`，解压后看 `SKILL.md` 的"鉴权"章节
   - 拿到 key 后写进 `~/.claw/settings.json` 的 `env` 字段（不要写进 shell rc，避免泄露到其它进程），格式：
     ```json
     { "env": { "WEREAD_API_KEY": "wrk-xxxxxxxx" } }
     ```
3. 检查 `python3` 是否可用（`which python3`）。macOS 自带；如缺失提示装 Xcode Command Line Tools。

### Step 2 — 安装到桌面

1. 创建 `~/Desktop/reading-widget/` 目录
2. 从 skill 目录复制文件过去：
   - `update.py` → 抓数据+渲染
   - `template.html` → 模板
   - `server.py` → 本地小后台（发卡片 + 存目标 + 自动刷新）
   - `open-widget.sh` → 一键打开脚本
   - `config.default.json` → 重命名为 `config.json`
   - `com.user.reading-widget.plist` → launchd 模板（Step 4 用，先别动）
3. 跑一次 `WEREAD_API_KEY=xxx python3 ~/Desktop/reading-widget/update.py` 生成首版 `widget.html`
4. 如果脚本报错（key 无效、网络等），把错误原样给用户看，不要瞎猜原因

### Step 3 — 一键打开 widget

跑打开脚本，它会先确保本地小后台 `server.py` 起着（没起就拉起来），再用 Chrome `--app` 模式打开一个无边框小窗，指向 `http://127.0.0.1:47900/widget.html`：

```bash
bash ~/Desktop/reading-widget/open-widget.sh
```

走 `http://127.0.0.1` 而不是 `file://`，是为了让卡片上手动改目标能 POST 回 `server.py` 存进 `config.json`（`file://` 下同源请求会被拦，目标改了重启就丢）。没装 Chrome 时脚本退化到默认浏览器；后台拉不起来时退化到 `file://`（此时改目标不持久）。

### Step 4（可选，但推荐）— 开机自启后台

Step 3 是「打开时才拉起后台」。如果想让数据**一直**在后台每 30 分钟刷新（不用每次手动开卡片），把 `server.py` 设成开机自启。

> ⚠️ 这是给用户电脑加一个常驻 LaunchAgent，属于持久化系统改动。**装之前必须明确问一句用户同不同意**，不要默默 load。

1. 把 skill 目录里的 `com.user.reading-widget.plist` 复制到 `~/Library/LaunchAgents/`，并把里面的 `USERNAME` 换成真实用户名、`/usr/bin/python3` 换成 `which python3` 实际路径。
2. 加载：`launchctl load ~/Library/LaunchAgents/com.user.reading-widget.plist`

注意 plist 里**不放** `WEREAD_API_KEY`——`server.py` → `update.py` 会自己从 `~/.claw/settings.json` 的 `env` 读 key，别把 key 落进 plist。日志在 `~/Desktop/reading-widget/helper.log`。

## 自定义

- **月度目标**：直接在 widget 卡片上点那个数字改即可，会经 `server.py` 的 `POST /set-goal` 写回 `config.json`（重启不丢）；也可以手动编辑 `config.json` 的 `goal_hours`。
- **后台刷新间隔**：改 `server.py` 顶部的 `REFRESH_INTERVAL`（秒，默认 1800）。
- **卡片自刷间隔**：改 `config.json` 的 `refresh_seconds`（HTML meta refresh，默认 300）。
- **配色/尺寸**：直接改 `template.html` 的 CSS（Material 3 暗色 token 在 `:root`），重跑 `update.py` 生效。
- **金句过滤**：脏词黑名单在 `update.py` 顶部的 `QUOTE_BLOCKLIST`，命中的热门划线会跳过换下一条。

## 卡片显示了什么

| 模块 | 数据源 |
|------|--------|
| 连续阅读天数 | `/readdata/detail` weekly 桶往前翻，阈值 60 秒/天 |
| 今日分钟 + 日均（点开 → 本周时长 + 本周日均） | weekly 桶今天的值；本周合计 ÷ 已过天数 |
| 本月小时 + 上月对比（点开 → 今年累计 + 今年日均） | `/readdata/detail` monthly / annually |
| 本月目标进度 | `config.json.goal_hours`，卡片上可点数字直接改 |
| 正在读 + 进度% | `/shelf/sync` 找最近未读完的书，`/book/getprogress` 拿 progress |
| 今年读完本数 / 笔记数 | `/readdata/detail` annually 的 `readStat` |
| 金句 | `/book/bestbookmarks` 拿当前在读书的热门划线，按日期轮换，过 `QUOTE_BLOCKLIST` 脏词过滤 |

两个 stat 卡片可点击翻面看对比（今日↔本周、本月↔今年），靠 CSS `.flipped` class 切换，无需 JS 文件。

## 触发用户调用本 skill 的场景

- 安装/重装：用户说"装这个 widget"、"让我也用上"
- 排错：widget 数据没刷新、卡片打不开、API 报 401、目标改了重启又变回去（多半是没走 `server.py` / 没用 `http://`）
- 改样式/改目标：用户想调小、换色、改月度目标
- 卸载：`launchctl unload ~/Library/LaunchAgents/com.user.reading-widget.plist` 并删该 plist；删 `~/Desktop/reading-widget/`；从 `settings.json` 拿掉 key
