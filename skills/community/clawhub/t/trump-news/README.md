# 每日特朗普新闻（OpenClaw Skill）

本 Skill 从**确凿信息源**拉取特朗普相关新闻与总统文件，由 AI 翻译成中文、编辑后推送给用户。

## 信息源（与 SKILL.md 一致）

### 第一类：核心官方与首发

| 来源 | 说明 | 脚本接入 |
|------|------|----------|
| **Truth Social (@realDonaldTrump)** | 个人首发阵地 | ✅ **truthbrush**（可选，需凭证） |
| X (@TeamTrump / @CLF) | 竞选/PAC 官方 | 需 X API，未接入 |
| **The White House (Briefing Room)** | 政策权威 | ✅ RSS |
| **Federal Register** | 行政命令法律来源 | ✅ 官方 API |
| **SCOTUSblog** | 最高法院/诉讼解读 | ✅ RSS |

### 第二类：顶级通讯社

| 来源 | 说明 | 脚本接入 |
|------|------|----------|
| **Reuters** | 中立、快速 | ✅ RSS（政治类） |
| **Associated Press** | 事实采集 | ✅ RSS（Top News） |
| Bloomberg | 金融/宏观影响 | 多需订阅，未接入 |
| **AFP** | 国际视角 | ✅ RSS |

## 项目结构

```
trump-news-daily/
├── SKILL.md              # 技能说明与执行步骤
├── README.md
├── config/
│   └── sources.json      # 信息源清单说明
└── scripts/
    ├── fetch_trump_news.py   # 主拉取（RSS + Federal Register + 可选 Truth Social）
    └── fetch_truth_social.py # Truth Social 拉取（依赖 truthbrush）
```

## 依赖

- Python 3.8+
- **主流程**：仅用标准库（`urllib`、`xml.etree`、`json`），无需 pip 安装。
- **Truth Social（可选）**：需安装 [truthbrush](https://pypi.org/project/truthbrush/)（`pip install truthbrush`，Python 3.10+），并配置环境变量：
  - `TRUTHSOCIAL_USERNAME` + `TRUTHSOCIAL_PASSWORD`，或
  - `TRUTHSOCIAL_TOKEN`（从浏览器 Truth Social 登录后的 Local Storage 中获取）
  - 可选：`TRUTHSOCIAL_HANDLE` 指定账号，默认 `realDonaldTrump`

## 安装到 OpenClaw

1. 将本目录复制到 OpenClaw 的 skills 目录之一，例如：
   ```bash
   cp -r trump-news-daily ~/.openclaw/skills/
   ```
   或放到工作区 `workspace/skills/`，或在 `~/.openclaw/openclaw.json` 的 `skills.load.extraDirs` 中加入父目录。

2. 刷新 Skills（或重启 Gateway）。

3. 在对话中触发，例如：「请执行今日特朗普相关新闻拉取、翻译编辑并推送给用户」。

## 定时推送（可选）

若需每日固定时间推送（如北京时间 8 点），可添加 cron：

```bash
openclaw cron add --name "特朗普每日新闻" \
  --cron "0 8 * * *" \
  --session main \
  --message "请执行今日特朗普相关新闻拉取、翻译编辑并推送给用户"
```

若已配置 Telegram，可在 SKILL 中让助手在编辑完成后调用 `send_telegram.py` 推送；否则在对话中直接回复即可。

## 说明

- 部分 RSS 源可能对请求有访问限制（如 403），若在受限网络或代理环境运行失败，可在本机或服务器上直接执行 `python3 scripts/fetch_trump_news.py` 测试。
- Federal Register API 无需 Key，公开可用；若时间段内无特朗普签发的行政命令，该块会显示「No matching documents」。

## 拉取逻辑简述

- **Federal Register**：请求最近 14 天内、总统为 Donald Trump、类型为总统文件/行政命令的文档。
- **RSS**：请求各站 RSS，解析标题与摘要，保留含 Trump / 白宫简报 / 最高法院等关键词的条目；白宫与 SCOTUSblog 会多保留几条最近条目以便政策与法律相关覆盖。

输出为英文摘要，由 OpenClaw 助手翻译成中文、编辑后推送给用户。
