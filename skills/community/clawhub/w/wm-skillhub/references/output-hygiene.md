# 输出可靠性（来源 / 校验 / 指标名）

对用户可见回答遵守下列硬规则（L1 与 Role 均适用）。

## 1. 来源

每个关键数字或结论句，标明：

- **来源技能**（真实 HTTP 跑过的 `wm-*` id，或 `xs/eval` / persist 路径）
- **口径 / as_of**（若返回里有）

禁止把外搜新闻 / 未跑技能的臆测写成「平台数据」。

## 2. 校验入口

- 技能返回含白名单 `deeplinks` → **原样**贴每条的 `markdown`（优先）或 `text` + `href` / `href_embed`
- 多标的超链接 → `POST /v1/deeplinks/resolve` 或 `skhub.deeplinks`；**禁止**手搓 URL
- **禁止** Agent 自己拼装 URL、手搓 `panel=` / `vs=` / `/embed/v1/`；禁止使用已废弃 id `portfolio`（用 `watchlist`）
- 反馈入口只用白名单 id：`feedback` / `feedback.new` / `feedback.detail` / `wechat.follow` / `community.group`（或 `feedback.create` 返回的 deeplinks）；禁止手搓 `/feedback…` `/wechat…` `/community`
- 工具失败 / 可复现数据问题 → **自主** `feedback.create` / `POST /v1/feedback`，再贴返回 markdown；若 `!notify_channel.subscribed` 必贴 `wechat.follow`；勿等用户催
- 自写短 XS → 留下可复跑入口（`wm-analysis-persist` 路径，或可再 `mode=call` 的语句）；口头-only 须声明不可复跑
- 需要人眼核对图表 / 自选 / 回测时：只贴技能已解析的站内链接，禁止外站链接当证据
- K 线 / 交易回顾 → 白名单 id `company.kline`（技能返回或 resolve），勿手搓 `panel=kline`

## 3. 指标命名（首次出现）

首次出现指标时写：

`中文全称（英文，代号）`，可再跟一句白话。

例：

- 经营现金流净额（Net Cash from Operations，NCFO）
- 市现率（Price to Cash Flow，PCF）
- 净现比（NCFO÷净利润）

**禁止**只甩 `NCFO` / `PCF` / `ROE` 等代号；后续同段可简称代号。
