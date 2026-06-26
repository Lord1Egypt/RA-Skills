# Reading Widget · 微信读书桌面小卡片

![preview](preview.png)

一个挂在 macOS 桌面的小组件，显示你的微信读书数据：连续阅读天数、今日/本月阅读时长、本月目标进度、正在读的书 + 进度、今年读完本数、当下金句。浅色 Material 3 配色，毛玻璃底，贴在屏幕角落。

带一个本地小后台（`server.py`，`127.0.0.1:47900`）：卡片上点数字改月度目标会**持久化**（重启不丢），数据每 30 分钟自动重抓。两个统计格子点一下能**翻面**看对比（今日 ↔ 本周、本月 ↔ 今年）。

> 本项目是微信读书官方 [`weread-skills`](https://cdn.weread.qq.com/skills/weread-skills.zip) 之上的一层**渲染壳**，数据全部来自微信读书官方 Agent API。详见下方[致谢](#致谢-acknowledgments)。


## 怎么装

### 给 OpenClaw / Claw 用户（最简单）

把本仓库放到 `~/.claw/skills/reading-widget/`（`git clone` 后改名即可），然后跟 Claw 说「装一下 reading-widget」，它会按 `SKILL.md` 走完整流程（含可选的开机自启）。

> Claude Code 用户同理：放到 `~/.claude/skills/reading-widget/`，跟 Claude 说「装一下 reading-widget」即可。

### 手动安装

前置：

- macOS
- Python 3（系统自带）
- Google Chrome（无边框 `--app` 窗口用；没有会退化到默认浏览器）
- 一个微信读书 Agent API key（格式 `wrk-xxxxxxxx`，下方有说明）

```bash
git clone https://github.com/TinaDu-AI/reading-widget.git
cd reading-widget
chmod +x install.sh
./install.sh
```

装完打开卡片：

```bash
bash ~/Desktop/reading-widget/open-widget.sh
```

它会先拉起本地小后台，再开一个无边框 Chrome 小窗指向 `http://127.0.0.1:47900/widget.html`，拖到屏幕角落即可。走 `http://127.0.0.1` 而不是 `file://`，是为了让卡片上手动改目标能 POST 回 `server.py` 存进 `config.json`。

### 开机自启（可选，推荐）

想让数据**一直**在后台每 30 分钟刷新、不用每次手动开卡片，就把 `server.py` 设成开机自启：

```bash
cp com.user.reading-widget.plist ~/Library/LaunchAgents/
# 把里面的 USERNAME 换成你的用户名，/usr/bin/python3 换成 `which python3` 的实际路径
launchctl load ~/Library/LaunchAgents/com.user.reading-widget.plist
```

plist 里**不放** API key —— `server.py` → `update.py` 会自己从 `~/.claw/settings.json` 的 `env` 读。日志在 `~/Desktop/reading-widget/helper.log`。

### 另一种摆法：Übersicht

不想跑后台、只想要个壁纸层挂件，可以用 [Übersicht](http://tracesof.net/uebersicht/)：把 `ubersicht/reading.widget/` 拷到 `~/Library/Application Support/Übersicht/widgets/`，菜单栏 👁️ → Refresh All Widgets。注意这条路径**不带**目标持久化（Übersicht 只渲染，不接 `server.py`）。

## 微信读书 API key 怎么拿

下载微信读书官方 skill 包，里面有 Agent Gateway 的鉴权说明：

```
https://cdn.weread.qq.com/skills/weread-skills.zip
```

解压后看 `SKILL.md` 的「鉴权」一节，按指引申请你自己的 `wrk-xxxxxxxx` key。拿到后写进 `~/.claw/settings.json`（Claude Code 用户为 `~/.claude/settings.json`；**别**写进 shell rc，免得泄露到其它进程）：

```json
{
  "env": {
    "WEREAD_API_KEY": "wrk-xxxxxxxx"
  }
}
```

## 自定义

- **月度目标小时**：直接在 widget 卡片上点那个数字改，会经 `server.py` 的 `POST /set-goal` 写回 `config.json`（重启不丢）；也可手动编辑 `~/Desktop/reading-widget/config.json` 的 `goal_hours`。
- **后台刷新间隔**：改 `server.py` 顶部的 `REFRESH_INTERVAL`（秒，默认 1800）。
- **卡片自刷间隔**：改 `config.json` 的 `refresh_seconds`（HTML meta refresh，默认 300）。
- **配色 / 尺寸**：直接改 `template.html` 的 CSS（Material 3 浅色 token 在 `:root`），重跑 `update.py` 生效。
- **金句过滤**：脏词黑名单在 `update.py` 顶部的 `QUOTE_BLOCKLIST`，命中的热门划线会跳过换下一条。

## 卡片显示什么

| 模块 | 来源 |
|---|---|
| 连续阅读天数 | `/readdata/detail` 周桶往前翻，阈值 60 秒/天 |
| 今日分钟 + 日均（点开翻面 → 本周时长 + 本周日均） | weekly 桶；本周合计 ÷ 已过天数 |
| 本月小时 + 上月对比（点开翻面 → 今年累计 + 今年日均） | `/readdata/detail` monthly / annually |
| 本月目标进度 | `config.json.goal_hours`，卡片上可点数字直接改 |
| 正在读 + 进度 % | `/shelf/sync` 找最近未读完的书 + `/book/getprogress` |
| 今年读完 / 笔记数 | `/readdata/detail` annually 的 `readStat` |
| 金句 | `/book/bestbookmarks` 当前在读书的热门划线，按日期轮换，过脏词黑名单 |

两个统计格子点一下翻面看对比（今日 ↔ 本周、本月 ↔ 今年），靠 CSS `.flipped` class 切换，无需额外 JS 文件。

## 文件结构

```
reading-widget/
├── README.md
├── SKILL.md                      # OpenClaw / Claude Code 自动安装指引
├── install.sh                    # 手动安装脚本
├── update.py                     # 抓数据 + 渲染脚本
├── template.html                 # 卡片模板（Material 3 浅色）
├── server.py                     # 本地小后台：发卡片 + 存目标 + 自动刷新
├── open-widget.sh                # 拉起后台 + Chrome --app 模式打开
├── com.user.reading-widget.plist # 开机自启 launchd 模板
├── config.default.json           # 默认配置
└── ubersicht/
    └── reading.widget/
        └── index.coffee          # 可选：Übersicht 壁纸层挂件
```

## 致谢 Acknowledgments

本项目**完全建立在微信读书官方 Agent skill 之上** —— 所有数据接口（阅读统计、书架、阅读进度、热门划线等）都来自微信读书官方维护的 Agent Gateway 和它附带的 [`weread-skills`](https://cdn.weread.qq.com/skills/weread-skills.zip) 包。本项目只是把这些接口的输出重新组合渲染成一个桌面 widget，**不涉及任何接口逆向、抓包或绕过鉴权**。如果没有官方开放这套 Agent 能力，这个 widget 不可能存在。

向微信读书团队致敬 🙏

## License

MIT（仅本仓库的渲染层代码；底层数据接口归微信读书所有，调用须遵守其 Agent 服务条款）
