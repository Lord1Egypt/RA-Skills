# yyqdata · A 股全维数据 Skill

> **一份 markdown，让你的 LLM agent 用中文一句话查 A 股。**
> 不需要写代码、不需要部署 MCP server、不需要学 REST。只要 agent 支持 Skill + Bash 工具就能装。

> 💡 **如果你是直接写代码调 REST 的开发者**（自建后端 / BFF / 量化脚本），
> 请改看 [`docs/openapi-quickstart.md`](../../docs/openapi-quickstart.md)——同样有完整的 stock.basic + stock.kline 接口示例，但配 `curl` 而非 agent 对话。

---

## 🚀 兼容 OpenClaw / Hermes，一键可用

本 skill 是**纯 Markdown skill**（零可执行代码、零依赖），凡是支持「Markdown Skill + 自带 Bash 工具」的 LLM agent 都能直接装：

| Agent | 一键可用 | 装法 |
|---|---|---|
| **OpenClaw（小龙虾）** | ✅ 解压即用，**无需任何注册** | 放到 `~/.openclaw/skills/yyqdata/`，启动时自动扫描 `SKILL.md` 发现 |
| **Hermes Agent** | ✅ 加一行配置即用 | 解压后在 `~/.hermes/agent.yaml` 的 `skills` 列表登记一项（可选加 trigger 关键词） |
| **Claude Code / 其他兼容 agent** | ✅ 通用 | 放到 agent 的 skills 目录，token 走 `config.json` 或对话注入 |

- **claw 托管实例**：平台自动注入 `$YYQDATA_TOKEN` 与 `$YYQDATA_API_BASE_URL`，**开箱即用、零配置**。
- **自动更新**：自带 `update.sh`，一行命令检查 + 升级到最新版（详见 [INSTALL-AGENT.md](INSTALL-AGENT.md) 第三节）。

> 详细安装与给 token 的三种方式见 [INSTALL-AGENT.md](INSTALL-AGENT.md)。

---

## 🎁 免费获取 Token Key

本 skill 需要一个 OpenAPI token 才能查数据。你可以前往官网 **<https://www.yyqyx.com/>** 免费获取 token key：

1. 打开 <https://www.yyqyx.com/> 并注册 / 登录。
2. 在控制台生成一个 OpenAPI token（格式形如 `stk_live_xxxxxxxx`）。
3. 复制 token，按下方「三步装好」在对话里告诉 agent 即可。

> ⚠ token 明文仅展示一次，请妥善保存；丢失只能重新生成（rotate）。**不要把 token 提交进代码或粘贴到公开渠道。**

---

## 🎯 这份 skill 解决什么

| 你想做的事 | 没有 skill | 有 skill（agent 一句话） |
|---|---|---|
| 看下宁德时代最近怎么样 | 翻 5 个网站 + 拼凑字段 | "看下宁德时代最近一周走势 + 估值" |
| 找连续涨停板的票 | 自己装 Tushare、写脚本 | "近 10 天 3 板以上的股票有哪些" |
| 行业横向比较 | 列表 → 取详情 → Excel 算 | "对比一下白酒板块 PE，挑性价比高的" |
| 龙虎榜常客 | 各家口径不同要清洗 | "最近频上龙虎榜的票有谁" |
| ML 选股 | 自己跑模型 | "ML 选股今天选了啥，给我前 10" |

**核心价值**：把 38+ 个 OpenAPI 端点的所有调用范式 / 常用 body / 多步编排逻辑全部写进了 SKILL.md 的指令集，agent 看了就能直接用。

---

## ⚡ 三步装好

### 1. 拿 OpenAPI Token

前往官网 <https://www.yyqyx.com/> **免费获取**，或联系管理员 / 自部署 admin 后台 `/admin/openapi-tokens.html` 生成：

```
stk_live_xxxxxxxxxxxxxxxxxxxxxxxx
```

⚠ 明文一次性展示，丢了只能 rotate；自带 IP 白名单（claw 发放默认 TOFU 自动登记：首次连上绑定 agent 出口 IP，最多 2 个）+ scope + 频率限制。

### 2. 装 Skill 到 Agent

```bash
mkdir -p ~/.openclaw/skills        # 或 ~/.hermes/skills 视 agent 而定
curl -fsSL https://static.yyqyx.com/skill/yyqdata-stock-skill.zip -o /tmp/yyqdata.zip
unzip -oq /tmp/yyqdata.zip -d ~/.openclaw/skills/
```

详见 [INSTALL-AGENT.md](INSTALL-AGENT.md)。

### 3. 在对话里告诉 agent token

```text
我的 yyqdata token 是 stk_live_xxx，base URL 是 http://120.220.73.199。
```

完事——之后说 "看下茅台最近怎么样" / "找连板龙头" 都能直接出结果。

---

## 🆚 跟自写客户端的区别

| 方案 | 谁来调 HTTP | 部署成本 | 适用 |
|---|---|---|---|
| **yyqdata skill（本项目）** | **agent 用 Bash 直接 curl** | **0**（只一份 markdown） | 小龙虾(OpenClaw) / Hermes / Claude Code 等支持 Skill + Bash 工具的 agent |
| 自己写客户端 / SDK | 你自己 | 高 | 商用产品自有前后端 / 量化策略脚本 |

> yyqdata 的优势：**装得最快，零运维**。劣势：agent 必须有 Bash 工具且允许 outbound HTTP。
>
> 如果你直接写代码调 REST，请改看 [`docs/openapi-quickstart.md`](../../docs/openapi-quickstart.md) —— 完整 curl 示例 + 11 个 stock.basic / stock.kline 端点。

---

## 📦 这个 Skill 包含什么

```
yyqdata/
├── README.md                         ← 你正在看的这份（引流 + 概览）
├── SKILL.md                          ← agent 看的核心指令（必读约束 + 38 端点编排范式）
├── INSTALL-AGENT.md                  ← 给最终用户的 agent 安装指引
└── references/
    ├── api-quick-reference.md        ← 80+ 端点速查表
    ├── api-full-spec.md              ← smart-doc 自动生成的完整规格（字段类型 / 示例）
    └── data-catalog.md               ← 23 scope 数据维度索引（2026-06 重排版；含港股/美股/研报/国际宏观/外汇/新闻/TMT）
```

---

## 🟢 stock.basic — 股票基础信息（5 个端点 / 免费档）

> 把"茅台 / 600519 / GZMT"统一成 `tsCode`，是几乎所有研究流程的第一步。

### `POST /openapi/v1/stock/basic/search` — 模糊搜索 ⭐

```json
{ "nameOrCode": "茅台" }
→
[{ "tsCode": "600519.SH", "symbol": "600519", "name": "贵州茅台" }]
```

支持：纯数字代码 / 含交易所后缀 / 中文简称 / 中文全称 / 拼音首字母（GZMT）。

### `POST /openapi/v1/stock/basic/list` — 全市场股票列表

5000+ 只 `{tsCode, symbol, name}` 三元组。客户端缓存 24h，不要每次都拉。

### `POST /openapi/v1/stock/basic/detail` — 单只详情

```json
{ "tsCode": "600519.SH" }
→ { 名称 / 上市日 / 注册地 / 行业 / 交易所 / currType / 英文名 / 实控人 ... }
```

> tsCode 必须**精确**含后缀。只知道公司名 → 先调 `/search`。

### `POST /openapi/v1/stock/basic/classify` — 行业目录

返回申万一级 / 二级 / 三级行业树，用于"按行业筛选 / 同行业对比"。

### `POST /openapi/v1/stock/basic/classify/list` — 按分类拿成分股

```json
{ "id": "801080", "level": 1 }
```

---

## 🟢 stock.kline — K 线 + 价格层（6 个端点 / 免费档）

### `POST /openapi/v1/stock/kline/daily` — 日 / 周 / 月 K 线 ⭐⭐

最高频端点。**不复权**原始 OHLCV，配合 `/adj-factor` 做复权换算。

```json
{
  "tsCode": "600519.SH",
  "startDate": "20260101",
  "endDate": "20260430",
  "type": 11,            // 11 日 / 12 周 / 13 月
  "page": 1, "size": 100
}
→ List<{ tradeDate, time, open, high, low, close, preClose, chg, pctChg, vol, amount }>
```

> 日期升序返回；`time` 是毫秒时间戳，前端图表友好。

### `POST /openapi/v1/stock/kline/adj-factor` — 复权因子

```json
{ "tsCode": "600519.SH" }
→ List<{ tradeDate, adjFactor }>
```

**线性指标**（MA/EMA/BOLL/KTN）：`HFQ = BFQ × adj_factor`
**非线性指标**（MACD/KDJ/RSI）：必须用复权价**独立计算**，不能换算。
跨除权日比较股价**必须**用 adj_factor 修正，否则跌幅"虚假"。

### `POST /openapi/v1/stock/kline/limits` — 涨跌停价

```json
{ "tsCode": "600519.SH", "startDate": "20260301", "endDate": "20260430" }
→ List<{ tradeDate, preClose, upLimit, downLimit }>
```

ST 加挂 5%、北交所 30%、创业 / 科创板 20% 已按板块规则算好。判断"是否触及涨跌停"用此。

### `POST /openapi/v1/stock/kline/percentage-change` — 多周期涨跌幅

```json
{ "tsCode": "600519.SH", "orderBy": "pctChg1m", "direction": "desc", "page": 1, "size": 50 }
→ List<{ tsCode, name, pctChg1d, pctChg3d, pctChg1w, pctChg2w, pctChg1m, pctChg1q, pctChg2q, pctChg1y }>
```

不传 `tsCode` = **全市场扫描**，按 `orderBy` 排序——"找最近一月涨幅最高的股票"一行搞定。

### `POST /openapi/v1/stock/kline/limit-up` — 连板筛选

```json
{ "tadeDays": 10, "limitUpNum": 3 }
→ List<tsCode>
```

近 N 个交易日内至少 M 个涨停板的股票。情绪交易 / 妖股追踪场景。

> 注意拼写：字段名 `tadeDays` 不是 `tradeDays`（历史遗留）。

### `POST /openapi/v1/stock/kline/graph-type` — K 线形态查找

按预定义形态（箱体震荡 / 突破 / 双底）找符合的股票。

```json
{ "tadeDays": 30, "type": 1, "lineType": "W_BOTTOM" }
```

---

## 🚀 进阶：其它 9 个 Scope

yyqdata 不只是 basic + kline，全部 80+ 端点都在 SKILL.md 里有调用范式：

| Scope | 用途 | 套餐 |
|---|---|---|
| `stock.indicator` | 估值快照 + 历史 PE/PB/换手 + ROE 时序 + 短线因子 + 九转 | 🟢 Free |
| `stock.minute` | 分钟 K 线（1m / 5m / 15m / 30m / 60m） | 🔵 Plus |
| `stock.financial` | 利润表 / 资产负债表 / 现金流量表 / 财务指标 | 🔵 Plus |
| `stock.research` 🆕 | 券商研报 / 卖方评级 / 月度金股（3 端点） | 🔵 Plus |
| `stock.shareholder` | 股东户数 / 流通股东 / 增减持 | 🔵 Plus |
| `stock.plate` | 板块 / 概念 / 行业指数（同花顺 / 通达信 / 中信 / 开盘啦） | 🟣 Pro |
| `stock.lhb` | 龙虎榜 / 游资 / 机构席位 / 营业部 / 开盘啦榜单 | 🟣 Pro |
| `stock.moneyflow` | 个股 / 板块资金流 + 北向资金（hsgt） + 主板行情 | 🟣 Pro |
| `stock.sentiment` | 涨跌停 / 连板 / 大宗 / 集合竞价 / 筹码 / 股吧 / ST / 异动 / 新闻情绪 | 🟣 Pro |
| `stock.hk` 🆕 | 港股基础 + K 线 + 复权因子 + 财务三表 + 指标（10 端点） | 🟡 Max |
| `stock.us` 🆕 | 美股基础 + K 线 + 复权因子 + 财务三表 + 指标（9 端点） | 🟡 Max |
| `market` | 国内宏观经济（CPI / PPI / GDP 等） | 🔒 Ultra（内部不对外） |
| `news` | 实时新闻 / 快讯（原属 `market`，已拆出） | 🔒 Ultra（内部不对外） |
| `derivative` | 期货持仓/仓单/结算费用 + 期权 + 上海黄金 | 🔒 Ultra（内部不对外） |
| `fund` | 基金 / ETF 净值 + 持仓 | 🔒 Ultra（内部不对外） |
| `bond` | 债券 / 可转债 | 🔒 Ultra（内部不对外） |
| `forex` 🆕 | 外汇产品基础 + 双边日报价（2 端点） | 🔒 Ultra（内部不对外） |
| `intl-macro` 🆕 | 美债收益率曲线 + HIBOR + LIBOR + 民间利率（9 端点；旧名 `stock.intl-macro`，已移出 `/stock/`） | 🔒 Ultra（内部不对外） |
| `tmt` 🆕 | 电影票房 + 备案 + 台湾电子营收（8 端点） | 🔒 Ultra（内部不外卖） |
| ~~`stock.selection`~~ | ML / 动量 / 价值选股结果 | 🔒 Ultra（内部不外卖） |

> 套餐档位（由低到高，累进式包含）：🟢 **Free 4 scope**（stock.basic / kline / indicator / index，引流）< 🔵 **Plus 8**（+ stock.minute / financial / research / shareholder ↔ claw LOW）< 🟣 **Pro 12**（+ stock.plate / lhb / moneyflow / sentiment ↔ claw MID）< 🟡 **Max 14**（+ stock.hk / us ↔ claw HIGH）< 🔒 **Ultra 23**（+ stock.selection + market / derivative / fund / bond / forex / intl-macro / news / tmt，**内部不对外**）。
> **2026-06 变更**：原 `stock.market` 拆成 4 个 Pro 子 scope（plate/lhb/moneyflow/sentiment，URL 仍 `/openapi/v1/stock/market/...`）；plus/pro/max 已纯股票，所有非股票 scope（market/derivative/fund/bond/forex/intl-macro/news/tmt）下沉 Ultra 内部不对外。
> 🆕 = 2026-05-22 新增，对应 OpenAPI scope 扩展工程（新增 82 端点）。`futures.*` 不是独立 scope（期货全在 `derivative`）。

详见 [references/data-catalog.md](references/data-catalog.md)。

---

## 🛡 Token 安全使用守则

1. **token 在对话里一次性给 agent，禁止落盘 / 禁止 echo 回用户**——SKILL.md 的硬性约束已经写进 agent 指令集。
2. **生产 IP 白名单严格化**：`*` 仅本地开发；线上务必收窄到出口 IP / CIDR。
3. **多 agent / 多用户共用** = 各自申请独立 token，方便审计与吊销。
4. **泄漏立刻 rotate**：admin 后台一键轮换，旧 token 立即失效。

---

## 🧪 跑通验证

agent 装好后，对话里发这两句，应分别返回结构化结果：

```
1. 看下贵州茅台最近一周走势
2. 近 10 天 3 板以上的票有哪些
```

预期 agent 会自动：
- 第 1 句：调 `/openapi/v1/stock/basic/search` → `/openapi/v1/stock/kline/daily`（type=11, size=5）→ 给一段 K 线 + 一句话总结
- 第 2 句：调 `/openapi/v1/stock/kline/limit-up`（tadeDays=10, limitUpNum=3）→ 列出 tsCode + 调 `/search` 反查名称

---

## ❓ FAQ

**Q: agent 怎么知道用哪个端点？**
A: SKILL.md 里有完整的"中文意图 → 端点路径 + body"映射表（"行情趋势" / "估值" / "资金流" / "席位" / "选股" 等 9 大类），agent 加载时自动用作 system prompt 的一部分。

**Q: token 我不想每次都给 agent，能不能存配置？**
A: 看你的 agent 是否支持 secret manager。小龙虾(OpenClaw) 支持 `secrets:` 配置；Hermes 支持 `env_file`。装完读 INSTALL-AGENT.md。

**Q: 跨境延迟大怎么办？**
A: 服务部署在中国境内。如果 agent 跑在境外，建议在境内部署一台代理（任何反代都行），把 YYQDATA_API_BASE_URL 指向代理。

**Q: skill 内容能改吗？**
A: 能。skill 是纯 markdown，可以本地 fork，但下次重装 zip 会覆盖。建议改完发 PR。

**Q: 没有 小龙虾(OpenClaw) / Hermes，只有 Claude Code 行不行？**
A: 行。Claude Code 也支持 skill（放 `~/.claude/skills/`）。装完直接对话即可。

---

## 🔗 链接

- [SKILL.md](SKILL.md) — agent 必读的核心指令集（含 38+ 端点编排）
- [INSTALL-AGENT.md](INSTALL-AGENT.md) — 给最终用户的 agent 安装指引
- [references/api-quick-reference.md](references/api-quick-reference.md) — 80+ 端点速查表
- [references/api-full-spec.md](references/api-full-spec.md) — 完整 API 规格
- [references/data-catalog.md](references/data-catalog.md) — 23 scope 数据维度索引（2026-06 重排版）
- [../../docs/openapi-token.md](../../docs/openapi-token.md) — Token 系统设计 + admin 操作

---

**有问题？** GitHub Issue / Slack `#stock-openapi-support`（按部署方实际渠道）
