---
name: trump-news-daily
description: 每日拉取特朗普相关新闻（来自官方与主流通讯社信息源），经 AI 翻译成中文、编辑后推送给用户
user-invocable: true
---

# 每日特朗普新闻 · 信息源与推送

## 功能说明

当用户或定时任务触发「今日特朗普新闻」「Trump 新闻汇总」「拉取特朗普相关新闻并推送」等请求时，按以下流程执行：

1. **拉取新闻**：运行本技能目录下的 `scripts/fetch_trump_news.py`，从下方**确凿信息源**拉取当日/近期特朗普相关内容。
2. **翻译与编辑**：根据脚本输出的原文摘要，由你（AI）翻译成中文，并做简洁编辑（保留事实、去掉冗余、可加一句简短点评或背景）。
3. **推送**：将整理好的中文版推送给用户（若已配置 Telegram，可调用同环境下的 `send_telegram.py` 或用户指定的推送方式；否则在对话中直接回复）。

---

## 信息源清单（确切推荐）

脚本会从以下**两类**信息源拉取，均可在脚本或配置中指定具体 URL / API。

### 第一类：核心官方与首发渠道（Real-time & Authoritative）

| 来源 | 说明 | 脚本中的使用方式 |
|------|------|------------------|
| **Truth Social (@realDonaldTrump)** | 特朗普个人首发阵地，重大声明第一出口 | **已接入**：通过 Python 库 **truthbrush** 拉取。需 `pip install truthbrush` 并配置环境变量 `TRUTHSOCIAL_USERNAME` / `TRUTHSOCIAL_PASSWORD` 或 `TRUTHSOCIAL_TOKEN`；主脚本会可选调用 `scripts/fetch_truth_social.py` 并合并到摘要最前 |
| **X (@TeamTrump / @CLF)** | 竞选团队与关联 PAC 官方账号 | 需 Twitter/X API，脚本不默认拉取；可选配置 |
| **The White House (Briefing Room)** | 政策类唯一权威出处 | RSS：`https://www.whitehouse.gov/briefing-room/feed/` |
| **Federal Register** | 行政命令（Executive Orders）最准确法律来源 | 官方 API：`https://www.federalregister.gov/api/v1/documents.json`，条件 `president=donald-trump`、`presidential_document_type=executive_order` |
| **SCOTUSblog** | 特朗普相关法律诉讼与最高法院的专业解读 | RSS：`https://www.scotusblog.com/feed/` |

### 第二类：顶级通讯社（Fast & Fact-based）

| 来源 | 说明 | 脚本中的使用方式 |
|------|------|------------------|
| **Reuters (路透社)** | 中立、快速，偏见较少 | RSS：政治/美国版块或站点提供的 RSS（见脚本内 SOURCES） |
| **Associated Press (美联社)** | 全球标准化事实采集 | RSS：AP 提供的 Top News / 政治类 feed（见脚本内 SOURCES） |
| **Bloomberg (彭博社)** | 侧重其言论对金融市场与宏观经济的影响 | 多需订阅，脚本可选配置或仅提供链接说明 |
| **AFP (法新社)** | 国际视角，便于观察海外反馈 | RSS：AFP 英文 feed（见脚本内 SOURCES） |

脚本 `fetch_trump_news.py` 已内置 **Truth Social（truthbrush）**、RSS 与 Federal Register API；Truth Social 为可选，配置凭证后会自动出现在摘要最前。X、Bloomberg 等需 API Key 的仍在 SKILL 中仅作推荐。

---

## 执行步骤

1. **运行拉取脚本**（在技能根目录或指定工作目录下）：
   ```bash
   python3 scripts/fetch_trump_news.py
   ```
   脚本会输出一段**英文原文摘要**（按来源分块：标题、链接、日期、摘要），并注明信息源。

2. **翻译与编辑**：阅读上述输出，将内容翻译成中文，并做编辑：
   - 保留事实与关键信息；
   - 去掉重复与无关枝节；
   - 可加一句简短点评或背景（如「此条来自美联社」）；
   - 保持客观、不捏造信源。

3. **推送**：
   - 若用户已配置 Telegram 且环境中有 `send_telegram.py`（例如与 polymarket-telegram-picks 同机），可调用：
     ```bash
     python3 /path/to/send_telegram.py "（你整理好的中文内容）"
     ```
   - 否则在对话中直接回复整理好的中文版即可。

---

## 定时任务（每日推送）

在 OpenClaw 中可用 cron 每天固定时间触发，例如北京时间早 8 点：

```bash
openclaw cron add --name "特朗普每日新闻" \
  --cron "0 8 * * *" \
  --session main \
  --message "请执行今日特朗普相关新闻拉取、翻译编辑并推送给用户"
```

若 cron 支持时区，可加 `--tz "Asia/Shanghai"`。

---

## 输出格式建议（推送给用户的中文版）

- **标题**：如「特朗普相关新闻摘要 · YYYY-MM-DD」
- **按来源分块**：白宫简报 / Federal Register 行政命令 / SCOTUSblog / 路透 / 美联社 / 法新社 等，每块下为 1～3 句中文摘要 + 可选链接。
- **信源说明**：在结尾注明「以上来自 White House、Federal Register、SCOTUSblog、Reuters、AP、AFP 等公开渠道」，避免用户误以为来自 Truth Social/X 等未在脚本中拉取的渠道。

所有内容均基于脚本拉取到的公开信息源，由你翻译、编辑后推送，不保证实时覆盖 Truth Social / X 上的首发内容。
