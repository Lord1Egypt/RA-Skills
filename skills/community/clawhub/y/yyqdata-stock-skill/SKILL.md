---
name: yyqdata
description: A股/港股/美股量化数据查询（数据 REST API，**非 OpenAI/LLM 兼容端点**；所有接口在 /openapi/v1/** 下，token 自查用 POST /openapi/v1/whoami）。把"看下宁德时代最近怎么样""龙虎榜""ML 选股""美债收益率"这类中文问题翻成 /openapi/v1/* REST 调用。覆盖：K线、估值、财务、板块、资金流、龙虎榜、选股、基金、宏观、期权期货、可转债、研报、外汇、票房。
author: yyqdata
version: 3.5.31
license: internal
metadata: '{"openclaw": {"emoji": "📈", "primaryEnv": "YYQDATA_TOKEN", "homepage": "https://static.yyqyx.com/skill/yyqdata.manifest.json"}}'
requirements:
  authentication:
    type: bearer
    token_format: "stk_live_<48 字符随机串>"
    source: "由用户在对话中提供 → agent 在当前会话内持有。**禁止落盘 / 禁止 echo 给用户**。"
  network:
    - var: "${YYQDATA_API_BASE_URL}"
      default: "http://120.220.73.199"
      description: "OpenAPI v1 根地址。用户可在对话里声明改写。"
  shell_tools:
    - name: curl
      required: true
      description: "发 HTTPS POST"
    - name: jq
      required: false
      description: "解析 ApiResultModel 信封"
references:
  - "references/api-quick-reference.md  ← 80+ endpoint 的速查表（精炼，必读）"
  - "references/api-full-spec.md        ← smart-doc 自动生成的完整 API 规格（含字段类型、示例）"
  - "references/data-catalog.md         ← 11 大类 → 20 scope 数据维度索引（2026-06-08 whoami 实测）"
update:
  manifest_url: "https://static.yyqyx.com/skill/yyqdata.manifest.json"
  zip_url: "https://static.yyqyx.com/skill/yyqdata-stock-skill.zip"
  check_command: "bash update.sh --check    # exit 0=最新 / 10=有新版"
  apply_command: "bash update.sh --apply    # 强制重装最新版"
  auto_command: "bash update.sh             # 检查 + 有新版自动装"
  changelog: "见 manifest.json 的 changelog_summary 字段"
---

# yyqdata

## ⚡ FIRST CALL — 第一个请求照抄这个，别探别猜

本服务是**股票数据 REST API**，**不是 OpenAI/LLM 兼容端点**。token 自查**只有一个**端点：

```bash
BASE="${YYQDATA_API_BASE_URL:-http://120.220.73.199}"      # base_url 只到主机，不含 /openapi
TOKEN="${YYQDATA_TOKEN:?把 stk_live_ token 填进来}"
curl -sf -X POST "${BASE}/openapi/v1/whoami" -H "Authorization: Bearer ${TOKEN}"
# 返回 tier / scopes / rateLimitPerMin / llmHint，证明 token 有效 + 拿到套餐
```

**❌ 下面这些路径全都不存在，别去试（试了只会 404）**：
`/v1/whoami` · `/v1/token/info` · `/token/info`(无前缀) · `/whoami`(无前缀) · `/auth/whoami` · `/v1/auth/whoami` · `/v1/models` · `/models` · `/v1/chat/completions`

> ✅ 唯一正确的 token 自查 = **`POST /openapi/v1/whoami`**（别名 `/openapi/v1/token/info`，**仍需 `/openapi/v1` 前缀**）。
> ✅ 所有数据接口也都在 `/openapi/v1/**` 下（如 `/openapi/v1/stock/kline/daily`）。
> ⚠️ **`/openapi` 是路径的一部分，不是 base_url 的一部分**——base_url 只到 `http://120.220.73.199`，调用时务必拼成 `${BASE}/openapi/v1/...`。误探无前缀路径会收到一段引导 JSON（hint 字段指回正确端点）。

## 🔴 第一铁律：没真调过接口，禁止下任何"没有数据"的结论

**这是本 skill 优先级最高的规则，凌驾于下面所有内容之上。** LLM agent 最常见、对用户伤害最大的失败就是"没查就说没有"——本节专门根除它。

- **"没有 / 查不到 / 后端是空的 / 不支持"这类否定结论，必须同时满足两条**：① 你已用**正确端点 + camelCase 字段 + 正确日期格式实际发过请求**；② 你手里有那次请求返回的 `traceId`（或完整 `{code,msg}`）。**拿不出 traceId，就不准对用户说"没有"。**
- **`whoami` 通过 ≠ 数据已验证。** whoami 只证明"token 有效 + 套餐 scope + 路径配置"，它**不是任何业务数据的查询**。看到 whoami 成功就回答"有/没有某某数据"是**纯幻觉**。
- **scope 列表里有这个维度 = 你有权限查 = 你必须真去查一次再说。** 例：whoami 的 `scopes` 含 `derivative`，用户问期权 → 你**必须**真打 `/openapi/v1/derivative/option/*` 才能下结论，不能凭印象说"期权数据是空的"。
- **空响应不是终点，是自检起点。** 真拿到空 `data` 时，先走下面〔空结果 6 问自检〕逐条排除参数/日期/scope 错误，**确认无误后**才能向用户说"该条件下确实无数据"，并附上你试过的端点 + body + traceId。
- 📌 真实教训（2026-06）：某 agent 仅调了一次 `whoami` 就对用户说"期权数据后端是空的"。实际后端 `option_daily` 有 **2000 万+ 行**、恰好含用户要的交易日。**这是本 skill 要根除的头号失败模式——你读到这里，就别再犯。**

### 空结果 7 问自检（说"没有"之前逐条过一遍）

1. **我真的发请求了吗？** —— whoami / 看文档 / 凭记忆都不算。没有 traceId = 没查。
2. **字段是 camelCase 吗？** —— `tradeDate` 不是 `trade_date`，`tsCode` 不是 `ts_code`。snake_case 被忽略 → 端点拿默认值 → 看似"空"。
3. **日期格式对吗？** —— 必须 `YYYYMMDD`（宏观月度 `YYYYMM` / GDP `YYYYQX`）。带 `-` / `/` / ISO / 时间戳全被当未传。
4. **占位符替换了吗？** —— body 里不能真的出现 `<最新>` `<today>` `<tsCode>` `${...}` 这种字面量；必须换成真实值（日期自己算、tsCode 先 search）。
5. **scope / 端点选对了吗？** —— `market`（国内宏观，URL `/market/`）vs `stock.market`（个股市场行为，URL `/stock/market/`）、单合约 `option/kline/daily` vs 全市场 `option/kline/daily-by-date` 别搞反；403 是没套餐（不是没数据），先看 whoami。
6. **省略的枚举字段补显式值了吗？** —— 个别 int 枚举字段（如 `kline/daily` 的 `type`）在老版本服务端缺省时**不走文档默认值而静默返回空**。空结果且 body 里省略过枚举字段时，补显式默认值（如 `type:11`）重试一次。

7. **返回值格式没踩坑吗？** —— 以下场景数据明明有但因格式误判漏掉：
   - ⚠️ **K线系响应日期四种格式**：`stock/kline/daily` 的 `tradeDate` 是 **"YYYY-MM-DD" 带横杠字符串**（非 YYYYMMDD！同时有 `time` 毫秒字段）；`stock/index/kline/daily` 和 `stock/kline/percentage-change` 的 `tradeDate` 是**毫秒时间戳**；`stock/kline/limits` 和 **`stock/kline/adj-factor`** 的 `tradeDate` 是 **YYYYMMDD 紧凑字符串**（⚠️ `adj-factor` 虽名字带 kline 但不是毫秒，与 hk/adj-factor、us/adj-factor 不同——后两者是毫秒时间戳）
   - 以下端点响应日期字段是**毫秒时间戳 long**（不是字符串，需 ÷1000 转秒或 ÷86400000 转天对比）：**stock/indicator/* 整个 scope（含 roe.endDate） · financial/{income-statement,balance-sheet,cash-flow,indicator,repurchase,express,disclosure-date} annDate/endDate（⚠️ repurchase 还有 expDate 也是 ms；disclosure-date 的 preDate/actualDate/modifyDate 也是 ms） · stock/index/kline/daily · stock/index/kline/weekly · stock/index/kline/monthly · stock/index/dailybasic · stock/index/weight · stock/index/sw-industry-quo · stock/index/main/snapshot · stock/index/main/history · stock/indicator/idx-factor-pro · stock/kline/percentage-change · stock/kline/weekly-monthly(tradeDate+endDate 均 ms) · stock/kline/week-month-adj(tradeDate+endDate 均 ms) · option/kline/daily · option/kline/minutes · derivative/futures/kline/daily · derivative/futures/holding · derivative/futures/main-contract · derivative/futures/wsr · derivative/sge/kline/daily · hk/kline · hk/kline-adj · hk/adj-factor(tradeDate) · hk/minute · hk/fina-indicator endDate · hk/income/balance-sheet/cash-flow(endDate 均 ms) · us/kline(tradeDate) · us/kline-adj(tradeDate) · us/adj-factor(tradeDate) · us/income/balance-sheet/cash-flow(endDate 均 ms) · us/fina-indicator(endDate) · ths-hot（rankTime 更直观）· ths-daily · limit-step · limit-cpt-list · cyq-chips · hm-detail · forex/daily · plate（快照）/plate/list/plate/cash-flow tradeDate · plate/continue-net lastDate · **plate/stocks-indicator(tradeDate 响应是 ms，入参用 YYYY-MM-DD)** · intl-macro/* 全部9端点（字段 date）· fund/etf/kline/daily · fund/etf/share-history · research/report · research/report-rc(reportDate) · news/list newsTime · **eco-cal（字段 date）** · **bak-daily(tradeDate)** · **bak-basic(tradeDate+listDate)** · **st-daily 响应(tradeDate)** · **st-warning(pubDate/impDate)** · **shareholder/ccass-hold(tradeDate)** · **shareholder/ccass-detail(tradeDate)** · **shareholder/hk-hold(tradeDate)** · **shareholder/ggt-daily(tradeDate)** · **shareholder/hsgt-list(tradeDate)** · **kpl/kpl-concept-cons(tradeDate)** · **market/tdx-daily(tradeDate)** · **market/tdx-index(tradeDate)** · **market/tdx-member(tradeDate)** · **market/ci-daily(tradeDate)** · **market/ci-index-member(inDate/outDate)** · **futures/weekly-detail(weekDate)** · **lhb/details(tradeDate)**。financial/core · **financial/business-segment** · **financial/pledge** · dividend · macro系 · kline/limits · **kline/adj-factor** · futures/settle · futures/limit · option/contracts日期 等是字符串（YYYYMMDD 或 "YYYY-MM-DD"）。⚠️ 注意例外：**`mainboard`/`news-sentiment`/`moneyflow`/`moneyflow-dc`/`block-trade`/`cyq-perf`/`limit-analysis`/`hsgt-top10` 的 `tradeDate` 是 YYYYMMDD 字符串**（非毫秒，属于 stock.market scope 内例外）
   - ⚠️ **`stock/kline/index-minute` 的响应日期字段名是 `tradeTime`（不是 `tradeDate`！）** = 毫秒时间戳——代码里按 `tradeDate` 取值永远是 undefined/null
   - ⚠️ **`hk/tradecal` 和 `us/tradecal` 的响应日期字段名是 `calDate`（不是 `tradeDate`！）** = 毫秒时间戳；同时有 `pretradeDate`（也是毫秒）和 `isOpen`(0/1)
   - ⚠️ **港股/美股复权因子字段是 `cumAdjfactor`，A股是 `adjFactor`，两者字段名不同**——混淆后永远拿不到正确的复权因子值
   - `callPut` 定长空格补齐（`"C    "`），`== "C"` 全漏，先 `trim()`
   - `index-minute`（idx_mins）混传 `tradeDate` + `startDate` 时 tradeDate 做精确 AND → 返空；只传 `startDate`+`endDate` 或只传 `tradeDate`
   - `bond/yc` 不传日期 → 按全库无过滤返空；`news/list` `type` 传空 → 精确匹配 NULL → 空

7 条都排除、仍是空 → 才可以说"该条件下无数据"，并说明最可能原因（非交易日 / 未上市 / 未入库 / 筛选过严）。

## 🎯 操作主循环（每轮照此走 · 这是全文骨架）

> 本文档近千行，**别从头读到尾**。把下面 7 步当成你处理每个股票请求的骨架，哪一步拿不准再跳到对应章节深读。

```
0. 更新检查（每天一次，静默）            → 〔skill 自动更新〕
1. 备好 token+BASE，探 whoami 一次       → 落〔会话记忆卡〕，别反复探
2. 意图分类 → 选 WF-1~10                 → 〔Decision tree〕/〔意图到端点〕
3. 标的规范化：search 拿 tsCode          → 永不凭记忆拼码；已解析的复用记忆卡
4. 取数：camelCase + YYYYMMDD，真调接口   → 〔怎么发请求〕；铁律：没真调不下结论
5. 交付前自检门（reflection gate）        → 〔交付前自检门〕
6. 交付：结论先行 + 口径 + 异常 + CSV 路径 → 〔Output contract〕
```

长任务（全市场扫描 / 多页拉取）：边拉边落 CSV + 存进度检查点；上下文吃紧先写进度再续，**别重拉** → 〔会话记忆 & 长任务行为〕。

---

## 🚀 平台快速启动（Platform Quick-Start）

### Token 读取顺序（所有平台统一）

```bash
# 1. 环境变量（平台自动注入，如有）
TOKEN="${YYQDATA_TOKEN}"
BASE="${YYQDATA_API_BASE_URL:-http://120.220.73.199}"

# 2. skill 目录内的 config.json（推荐持久化方式，平台无关）
#    ⚠️ 不要假设 jq 存在（很多实例没装）：jq → python3 → sed 三级降级，保证一定能读出来
if [ -z "$TOKEN" ]; then
  for _d in ~/.openclaw/skills/yyqdata ~/.hermes/skills/yyqdata ~/.claude/skills/yyqdata; do
    _cfg="$_d/config.json"
    [ -f "$_cfg" ] || continue
    if command -v jq >/dev/null 2>&1; then
      TOKEN=$(jq -r '.token // empty' "$_cfg" 2>/dev/null)
      _b=$(jq -r '.base_url // empty' "$_cfg" 2>/dev/null)
    elif command -v python3 >/dev/null 2>&1; then
      TOKEN=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('token') or '')" "$_cfg" 2>/dev/null)
      _b=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('base_url') or '')" "$_cfg" 2>/dev/null)
    else
      TOKEN=$(sed -n 's/.*"token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$_cfg" | head -1)
      _b=$(sed -n 's/.*"base_url"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$_cfg" | head -1)
    fi
    [ -n "$_b" ] && BASE="$_b"
    [ -n "$TOKEN" ] && break
  done
fi

# 3. 对话中用户提供（兜底）
[ -z "$TOKEN" ] && echo "⚠️ 未找到 token，请用户提供 stk_live_xxx 格式 token"
```

config.json 格式（放在 skill 安装目录内，不随 zip 发布）：

```json
{ "token": "stk_live_xxx", "base_url": "http://120.220.73.199" }
```

快速健康验证：

```bash
curl -sf -X POST "${BASE}/openapi/v1/whoami" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '{tier: .data.tierLabel, scopes: .data.scopes}'
```

### A · 通用 / 手动（Claude Code / API / 其他 agent）

用户在对话中提供 `stk_live_xxx` token；agent 在会话内存中持有，不落盘：

```bash
TOKEN="stk_live_<用户给的值>"
BASE="http://120.220.73.199"

curl -sf -X POST "${BASE}/openapi/v1/whoami" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '{tier: .data.tierLabel, scopes: (.data.scopes | length)}'
```

### D · 受限环境（仅 GET / 无 curl / 沙箱）

```
GET ${BASE}/openapi/v1/stock/basic/search?nameOrCode=茅台&token=${TOKEN}
```

任何能发 HTTP GET 的工具（web_fetch / Invoke-WebRequest / Python requests）都可用；camelCase 字段拼 query param，`?token=` 等价于 Bearer header。

---

## ⛔ 硬性约束（必读，违反即失败）

1. **只能调用本文档明确列出的端点**：所有数据请求都打到 `${BASE}/openapi/v1/<scope>/<resource>`（GET 或 POST 皆可，见第 3 条）。**不要**自创路径、不要从工具名拼 URL（如 `/stock/api/getXxx` 一定 404）。**拿不准端点路径 / 字段名 → 先 `grep` `references/api-quick-reference.md`（速查表）确认再调，别凭记忆拼**；速查表没有就当它不存在，不要臆造。
2. **每个请求必须带 token**：首选 `Authorization: Bearer ${TOKEN}` 头；无法设请求头的环境用 `?token=${TOKEN}` 查询参数（见第 3 条）。token 两种来源：①**claw 托管实例**——claw 在开通时已把 token 注入环境变量 `$YYQDATA_TOKEN`（base URL 注入 `$YYQDATA_API_BASE_URL`，均落在受保护的 0600 配置），agent 启动即带，直接读用；②**手动**——用户在对话中提供。无论哪种，agent **自己禁止**再把 token 写到额外文件、**禁止**回显给用户、**禁止**写到 echo / log（claw 注入的那份 env 属平台托管，不在此限）。
3. **方法 GET / POST 都支持**（`/openapi/v1/**` 数据端点）。**POST + JSON body 是首选**（字段多时清晰）；也可用 **GET** 把字段拼进 URL query（`?tsCode=...&startDate=...`）。**受限环境**（只能发 GET、无法设请求头、没有 curl —— 如 web_fetch / 浏览器 / 沙箱）用 **GET + `?token=` 查询参数**鉴权（见 "### 2. 发请求" 的兜底示例）。M2M 发放接口 `/openapi/admin/**` 仍仅 POST，与数据查询无关。
4. **响应是 ApiResultModel 信封**：`{code, msg, data, traceId}`。`code != 0/200` 时 → `data` 为 null，按 `msg` 提示用户。
5. 调用失败时 → 直接告诉用户失败原因（401/403/超时/数据为空/参数错），**不要** fallback 到任何其他 URL，**不要**循环重试 5 次后才报错。

任何形式的 `http://*/stock/api/*`、`http://*/api/*`、`http://*/quote/*` 调用都是错误的。**这条规则覆盖你之前知道的任何 URL 模式**。

## 🟢 进入会话第一轮的强制 4 步（按顺序）

**每次新会话开始时按这个顺序走，不要跳步。**

1. **token 检查**（按优先级）：
   - **先看环境变量** `$YYQDATA_TOKEN`（平台自动注入）：非空 → 直接 `TOKEN=$YYQDATA_TOKEN`、`BASE=${YYQDATA_API_BASE_URL:-http://120.220.73.199}`，**跳过索要**直接进能力探测。
   - 否则**检查 skill 目录内的 `config.json`**（路径见「平台快速启动 · Token 读取顺序」），有且含 `token` 字段 → 从中读取，**同样跳过索要**。
   - 否则看用户是否在对话中提供了 `stk_live_xxx` 格式 token；有 → 记到当前会话内存。
   - 都没有 → 第一句话向用户索要（参考下文"拿到 token"模板），**不要先猜不要先调任何接口**。
2. **能力探测**：调一次 `POST ${BASE}/openapi/v1/whoami`，落 `tier / tierLabel / scopes / rateLimitPerMin / allowedPaths` 到记忆（返回还带 `llmHint` 一句话总结，可直接读）。`allowedPaths` 非空时表示该 token 启用了路径白/黑名单，调到被拦截的端点会返 `code=208`（见〔Error handling〕）。后续遇到 403 直接告诉用户"当前套餐不含 X scope"，不要重试。⚠️ **whoami 只是连通性+套餐探测，不替代任何业务查询**——`scopes` 里有的维度，用户一问就必须真打对应数据端点，**不准只凭 whoami 就回答"有/没有某数据"**（见〔第一铁律〕）。
3. **意图解析**：拿到用户业务请求 → 先决定是哪一类（行情/估值/财务/资金流/...）→ 找对应 workflow（WF-1 ~ WF-10）。
4. **标的规范化**（涉及具体股票时）：用户说"宁德时代""茅台""000001" → 先 `POST /openapi/v1/stock/basic/search` 解析成带后缀的 `tsCode`（`300750.SZ` / `600519.SH` / `000001.SZ`）。**永远不要凭记忆拼 ts_code**，也不要直接拿用户口语去调下游接口。⚠️ 该 search **只收录 A 股**；港股（`00700.HK`）/ 美股（`AAPL`，裸 ticker 无后缀）解析路径不同，见〔Entity resolution rules〕。

## 🧠 会话记忆 & 长任务行为（按 agent 记忆/行为算法设计）

> 你（agent）的会话记忆是**有限且会滑出窗口的**：典型只保留最近约 10 轮问答，更早的被**静默丢弃**；进程重启 = 全部清空，**没有持久层**。本节让你在这种约束下不丢状态、不重复劳动、不半路放弃。（这套规则借鉴了宿主 agent 的工作记忆 / 检查点压缩 / 执行偏向算法。）

### 1. 维护一张「会话记忆卡」（working memory）
首次探测后，在脑内维护一个紧凑状态块，并在它可能滑出窗口时**主动复述刷新**：

```
[yyqdata 记忆卡]
TOKEN: 已持有(env/对话)   BASE: http://...   tier: Max   rateLimit: 300/min
scopes: [stock.kline, derivative, ...]            # whoami 拿到一次就够，别反复探
已解析: 宁德时代=300750.SZ  茅台=600519.SH         # search 过的别再 search
最近交易日: 20260604                               # lhb/latest-dates 拿到就复用
本会话已查: kline/daily(300750)、moneyflow(300750)
```

- **先查记忆卡，再调接口**：要用的 tsCode / 最近交易日 / scope 若卡里已有，**直接复用，别重复 search / whoami / latest-dates**（省限频、省轮次）。
- 但**别赖记忆超过窗口**：拿不准卡里的值是否还在上下文里，就重查一次——数据端点有缓存，重查不额外计费。

### 2. 长任务：检查点 + 增量落盘（别一次性扛在脑子里）
全市场扫描 / 多页拉取（期权 `daily-by-date` 翻几十页、多标的对比、龙虎榜全量）这类长任务：

- **边拉边落 CSV**，不要把几千行积在上下文里——上下文是你最稀缺的资源。
- 维护进度检查点：`已完成: SHFE 全量 + DCE page1-5；下一步: DCE page6`，让自己（或下一轮）能续跑而非重来。
- 上下文吃紧（估算 >本轮预算 ~80%）时：先把"进度 + 已落盘路径"写进回复，再继续 / 交接，**严禁从头重拉**。
- 翻页有硬上限就**显式告诉用户截断了多少**（"只取了成交额前 500，按 X 排序"），不要假装拉全了。

### 3. 跨会话 / 定时任务：状态必须自包含
用户让你做**定时 / 重复**查询（"每天早上发我自选股表现"）时，牢记：**定时任务在全新会话里触发，没有任何历史记忆**。所以——

- token 走环境变量 `$YYQDATA_TOKEN`（平台注入，**会持久**）——别把 token 写进任务提示词。
- 业务状态**必须写进任务提示词自包含**：已解析的 tsCode 列表、查询参数、时间窗，以及（claw / hermes 环境下）回推消息用的 `conversation_id`（原样回显，别解析）。
- **别依赖"我上次记得用户要看哪几只"**——那段记忆在新会话里根本不存在。

### 4. 执行偏向（behavior）
- **能动手就别只给计划**：任务可执行时，本轮就发出真实调用，不要停在"我接下来会查…"。（呼应〔第一铁律〕：结论必须由真实响应支撑。）
- **多步任务给进度**：3 步以上的活，中途留一行进度（"第 2/5 步：已取行情，正在拉资金流"），别长时间沉默。
- **失败优雅退化**：分段拉取部分失败时，交付已成功的部分 + 明确标注哪段失败，不要因一段失败就放弃整单（见〔部分成功原则〕）。

## 🔄 skill 自动更新（每天第一轮静默检查一次）

**每个新会话的第 0 步**（在上面"4 步"之前，但只跑一次/天）：

```bash
# 异步、超时 5s、失败不阻塞业务流程。
curl -fsSL --max-time 5 "https://static.yyqyx.com/skill/yyqdata.manifest.json" 2>/dev/null \
  | grep -oE '"version"[[:space:]]*:[[:space:]]*"[^"]+"' \
  | head -1 \
  | sed -E 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)"/\1/'
```

把返回的 `version` 与本 SKILL.md 顶部 frontmatter 的 `version` 字段对比：
- **相等 / 拉取失败** → 静默继续，**不要打扰用户**。
- **远端 > 本地** → 在当轮回复**末尾**追加一行温和提示，例如：

  > 📦 提示：检测到 yyqdata 新版本 `v1.2.0`（当前 `v1.1.0`）。可让用户跑
  > `bash ~/.openclaw/skills/yyqdata/update.sh` 升级（或回复"升级 skill"由我替您跑）。

**规则**：
- 每 24 小时检查一次（agent 自行记忆上次检查时间戳）；同一会话内不重复检查。
- **不要**为了升级而中断用户当前任务；**不要**自动跑 `update.sh`（升级是用户决策，因为会覆盖本地修改）。
- 用户**明确要求升级**时，可代跑 `bash ${SKILL_DIR}/update.sh`（`SKILL_DIR` = 本 SKILL.md 所在目录）；失败回退到提示用户手动 curl + unzip。
- `update.sh` 自动备份旧版到 `yyqdata.bak-<时间戳>/`，安全可回滚。

## ⚠️ 极易混淆的 scope（只看这一次）

`market`（国内宏观）和 `stock.market`（个股市场行为）容易混。**两者都是 Pro scope，URL 前缀不同**：

| Scope | 套餐 | 数据范围 | 端点前缀 |
|-------|------|---------|---------|
| **`market`** | **Pro** | 国内宏观（CPI/PPI/PMI/GDP/M2/LPR/Shibor/社融）；`news`（Max）已独立 | `/openapi/v1/market/...` |
| **`stock.market`** | **Pro** | 板块 / 龙虎榜 / 资金流 / 热度 / 涨跌停 / 大宗 / 集合竞价 / 同花顺概念 / 游资 / ST / 异动 | `/openapi/v1/stock/market/...` |

**⚠️ 2026-06-08 whoami 实测**：生产 scope 名仍是 `stock.market`（单一 scope），并非 stock.plate/lhb/moneyflow/sentiment。文档中出现的 4 个子 scope 名是未落地的设计，**实际 whoami 只会返回 `stock.market`**。

记忆口诀：**`stock.market` 的 URL 一定带 `/stock/market/`；`market`（宏观）只带 `/market/`。**`market` 是"大盘宏观背景"，`stock.market` 是"个股市场行为"。

类似地：`stock.minute`（分钟 K 线，Plus）≠ `stock.kline`（日/周/月 K，免费）；`fund`（基金 / ETF，**Max**）≠ `bond`（债券 / 可转债，**Max**）。

**2026-05-22 新加 scope 易混淆点**：
- `stock.hk`（Max+，港股本身：基础 / K 线 / 财务）≠ `stock.shareholder` 下的 `/openapi/v1/stock/shareholder/hk-hold`（港股通**南向**持股，仍在 `stock.shareholder` scope）
- `stock.intl-macro`（**Max**，**境外**宏观：美债 / HIBOR / LIBOR；URL 前缀是 `/openapi/v1/intl-macro/*`，不带 `stock/`；scope 名仍是 `stock.intl-macro`，2026-06-08 whoami 实测）≠ `market` scope 下的 `/openapi/v1/market/macro/*`（**国内**宏观：CPI/PPI/GDP/M2/Shibor/LPR）
- `stock.us` / `stock.hk` 的 K 线端点（`/openapi/v1/stock/us/kline` 等）≠ A 股 `stock.kline`（`/openapi/v1/stock/kline/daily`），路径前缀完全不同
- `forex`（**Max**，境外外汇 / CFD）≠ 任何 A 股相关 scope

## 怎么发请求（核心范式）

### 1. 拿到 token + base URL（优先级：环境变量 → 对话）

**首次进入会话**时按顺序检查：

**(a) 环境变量已注入（推荐路径）**
两种部署都会把 token 落到同一个环境变量，agent 侧逻辑完全一致：
- **claw 托管实例**：claw-server 自动开通时把 token 写进 `$YYQDATA_TOKEN`、base URL 写进 `$YYQDATA_API_BASE_URL`（落在受保护的 0600 配置，agent 启动即带）。
- **OpenClaw 自装用户**：在 openclaw 配置里给本 skill 配 `skills.entries.yyqdata.apiKey = "stk_live_xxx"`，openclaw 运行时会自动把它注入为 `$YYQDATA_TOKEN`（本 skill frontmatter 已声明 `primaryEnv`）。配一次永久生效，**新会话不用重新贴 token**。

先探一下：
```bash
test -n "$YYQDATA_TOKEN" && echo "env token present: ${YYQDATA_TOKEN:0:12}..."
```
非空 → 直接 `TOKEN=$YYQDATA_TOKEN`、`BASE=${YYQDATA_API_BASE_URL:-http://120.220.73.199}`，**不必向用户索要**，直接进能力探测。

**(b) 手动 —— 用户在对话里给**
没有 env token 时：
- 用户是否已经告诉你 OpenAPI token？（格式：`stk_live_<48 字符>`）
- 是否给了自定义 base URL？（默认 `http://120.220.73.199`）

如果**都没有**，**第一句话就向用户索要**，例如：

> "我需要你的 OpenAPI token 才能调用数据后端，请提供（格式 `stk_live_xxx`，由后端管理员签发）。如不知道哪里拿，请联系后端管理员。"

拿到后：
- 在当前会话内**记忆**变量 `TOKEN` 和 `BASE`
- agent **自己禁止**再写入任何额外文件（~/.bashrc / 日志 / Markdown 输出）——claw 注入的那份 env 属平台托管，不在此限
- **禁止**在回复里 echo 给用户。如果要展示，至多 `${TOKEN:0:12}...` 脱敏

### 2. 发请求

每个端点的 body 都是 JSON，**只填业务字段**——OpenAPI 表单基类（`OpenApiBaseForm` / `OpenApiPageForm`）没有任何 app 跟踪字段（不存在 `userId` / `d` / `vn` / `appsFlyerId` 这些）。看到旧文档提到这些字段是过期的，忽略。

```bash
curl -sf -X POST "${BASE}/openapi/v1/stock/basic/search" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"nameOrCode": "茅台"}'
```

**注意**：在 Bash 命令里把 `${TOKEN}` 写成变量引用即可（用 agent 内存中的值替换）。绝对**不要**把 token 明文写进 curl 命令的 echo 输出或最终回复给用户的命令模板里。

**受限环境兜底（只能 GET / 不能设 header / 没 curl）**：当你的运行环境只能发 GET、无法设置请求头、也没有 curl（如 web_fetch 工具、浏览器、`Invoke-WebRequest` 受限沙箱），把**字段和 token 都拼进 URL**，用任意 GET 工具直接拉：
```
GET ${BASE}/openapi/v1/stock/basic/search?nameOrCode=茅台&token=${TOKEN}
```
- 字段名与 JSON 一致（camelCase）；`?token=`（或 `?access_token=`）查询参数等价于 `Authorization: Bearer`，端点 GET / POST 都认。
- ⚠️ URL 里的 token 会进服务器 / 反向代理的访问日志，**能设 header 时一律优先 header**（更安全）；token 仍受 IP 绑定 + scope + 限频保护，泄露也只能在绑定 IP 上用。
- 同样**禁止**把带 token 的完整 URL echo / 回显给用户（展示时脱敏成 `...&token=${TOKEN:0:12}...`）。

### 3. 解包 ApiResultModel + 常用 jq recipes

响应永远是这个信封：
```json
{
  "code": 0,
  "msg": "success",
  "data": [{"tsCode":"600519.SH","symbol":"600519","name":"贵州茅台"}],
  "traceId": "..."
}
```

- `code == 0` 或 `code == 200` → 取 `data`
- `code != 0/200` → 失败，把 `msg` 反馈给用户

**通用提取模式（可复用）：**
```bash
# 提取 + 校验一次搞定
RESP=$(curl -sf -X POST "${BASE}/openapi/v1/ENDPOINT" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "${BODY}")
[ "$(echo "$RESP" | jq -r '.code')" = "0" ] \
  || { echo "失败[$(echo "$RESP" | jq -r '.code')]: $(echo "$RESP" | jq -r '.msg')"; exit 1; }
DATA=$(echo "$RESP" | jq '.data')
```

**常用字段提取 recipes（场景速查）：**
```bash
# ① search → tsCode
TSCODE=$(echo "$RESP" | jq -r '.data[0].tsCode')

# ② kline/daily → 最近收盘价（tradeDate 是 "YYYY-MM-DD" 字符串）
echo "$RESP" | jq -r '.data[] | [.tradeDate, (.close|tostring)] | @tsv' | head -5

# ③ indicator/last → 估值（tradeDate 是毫秒时间戳，需转换）
echo "$RESP" | jq -r '.data[] | [(.tradeDate/1000|strftime("%Y-%m-%d")), (.pe|tostring), (.pb|tostring)] | @tsv'

# ④ moneyflow → 主力净流入（单位：万元；tradeDate 是 YYYYMMDD 字符串，不是毫秒）
echo "$RESP" | jq -r '.data[] | [.tradeDate, (.mainNetInflow|tostring)] | @tsv'

# ⑤ 落 CSV（通用，用 data[0] 的 keys 自动生成表头）
echo "$RESP" | jq -r '(.data[0] | keys_unsorted) as $h | $h, (.data[] | [.[$h[]]] | map(tostring)) | @csv' > output.csv
```

> ⚠️ `indicator/*` / `financial/*` / `fund/etf/kline/daily` 的 `tradeDate` 是**毫秒时间戳**（用 `÷1000|strftime`）；`kline/daily` 的 `tradeDate` 是**"YYYY-MM-DD" 字符串**（直接用）；`macro/shibor` / `macro/lpr` 的日期字段叫 `date`（不是 `tradeDate`）。三种格式别混。

### 4. 鉴权失败的处理

- HTTP `401` → token 无效 / 已禁用 / 已过期 → 提示用户检查 token
- HTTP `403` → token 合法但**没这个 scope** → 提示用户当前套餐不含该数据维度
- HTTP `429` → 频率超限 → 等下一分钟再试
- HTTP `5xx` → 后端故障 → 报告 traceId 给用户

随时可以调 `POST /openapi/v1/whoami`（**不需要任何 scope**）查 token 套餐 / scope / 频率上限。

***

## 数据维度索引

`yyqdata` 把数据按 **11 大类 → 20 scope → 5 套餐** 组织（2026-06-08 whoami 实测：Max token 含 18 个 scope + Ultra 的 stock.selection/tmt = 20）。详细维度见 [`references/data-catalog.md`](./references/data-catalog.md)。

**2026-05-22 扩展**：原 13 scope 基础上新增 6 个境外 / 专项数据维度：
- `stock.research`（Plus+）：券商研报 / 卖方评级 / 月度金股
- `stock.hk`（Max+）：港股基础 + K 线 + 财务（10 端点）
- `stock.us`（Max+）：美股基础 + K 线 + 财务（9 端点）
- `stock.intl-macro`（**Max+**）：美债收益率曲线 / HIBOR / LIBOR / 民间利率（9 端点；URL 前缀 `/openapi/v1/intl-macro/*`，不带 `stock/`；scope 名是 `stock.intl-macro`）
- `forex`（Max）：外汇产品 + 双边日报价（2 端点）
- `tmt`（Ultra · 内部不外卖）：电影票房 / 电影/电视剧备案 / 台湾电子营收（8 端点）
端点速查见 [`references/api-quick-reference.md`](./references/api-quick-reference.md)。

***

## What this skill is for

典型场景（覆盖 A 股 / 港股 / 美股 / 衍生品 / 宏观 / 多语言资产）：

- 看某只**A股 / 港股 / 美股**的最近走势、估值、财报
- 对比多只股票或板块的表现、估值、资金关注度
- 查询龙虎榜、主力席位、资金流向
- 读取 ML / 动量 / 价值三套选股模型的最新结果并给出解释
- 期权期货分析（50ETF 期权 / 股指期权 / 商品期货 / 上金所黄金）
- **可转债**评估（转股溢价率 / 纯债溢价率 / 强赎进度）
- 宏观背景（CPI / PMI / GDP / M2 / Shibor / LPR）
- 国际宏观（**美债收益率曲线** / HIBOR / LIBOR / 民间借贷）
- 外汇日报价（EURUSD / USDCNH / CFD）
- 梳理某公司近期新闻 / 重要事件
- 基于股东名单反查（"社保基金今年新进了哪些票"）
- 快速生成"全景研究简报"

先理解用户要解决什么问题 → 选定 workflow → 再挑端点 → 取数 → 整理 → 解释 → 交付。

## What this skill is NOT for

- 自动下单 / 真实交易执行
- 毫秒级 HFT 决策
- 直接给买卖点建议替代投资顾问
- 后端没有落库的全新字段（缺数据时必须说明，不要编造）

***

## Environment check

真正请求数据之前先做：

1. **token 是否就绪**：用户是否已在对话中给了 `stk_live_*` 格式的 token？没有就**先索要**，不要假装能继续。
2. **服务可达 + token 有效**：调一次 `POST ${BASE}/openapi/v1/whoami`（不需要任何 scope），返回的 `data.tierLabel` / `data.scopes` / `data.rateLimitPerMin` 告诉你能调哪些数据；同时这一步也是连通性 / 鉴权的最佳烟雾测试。
3. **结果为空时**：先判断是非交易日 / 数据未入库 / 股票未上市 / 筛选过严 / 代码错误，不要直接说"接口坏了"。

烟雾测试 curl（agent 自己内部跑一次，不要把 token 明文 echo 给用户）：

```bash
curl -sf -X POST "${BASE}/openapi/v1/whoami" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}'
```

期望 200 + `code=0` + `data.tierLabel` 等字段。失败按 [鉴权失败的处理](#4-鉴权失败的处理) 提示。

***

## 📍 意图 → Workflow 快速路由（先看这里，再往下找细节）

| 用户说… | 选这个 WF | 端点组合要点 |
|---------|----------|------------|
| "XX 最近怎么样 / 走势 / 表现" | **WF-1** | search→kline/daily+indicator/last+percentage-change+moneyflow |
| "对比 A 和 B / A vs B" | **WF-2** | search×N→indicator/last/by-codes+percentage-change循环 |
| "XX 财务 / 报表 / 利润" | **WF-3** | search→financial/core+dividend；详细说"完整/三大表"→WF-3.1 |
| "三大表 / 完整报表 / 多季利润+现金流详细" | **WF-3.1** | 四表并行：income-statement+balance-sheet+cash-flow+indicator |
| "MACD / KDJ / RSI / 均线 / 布林 / 技术指标" | **WF-3.5** | 四组并行：ma-channel+oscillator+trend-volume+nine-turn |
| "板块轮动 / 哪个行业最强" | **WF-4** | plate→plate/stocks-indicator+cash-flow |
| "龙虎榜 / 主力席位 / 游资" | **WF-5** | lhb/latest-dates→lhb/list+lhb/detail |
| "ML选股 / BUY列表 / 今天选了哪些" | **WF-6** | lhb/latest-dates→selection/ml/results（tradeDate必传！） |
| "社保/汇金/林园持仓" | **WF-7** | holder/find-stocks→WF-1循环 |
| "全面研究 / 简报 / 帮我研究" | **WF-8** | WF-1+WF-3+WF-4+lhb+research/report |
| "期权 / 期货 / 豆粕期权" | **WF-9** | 单合约→option/kline/daily；全市场→daily-by-date |
| "港股 / 腾讯港股 / 美股苹果" | **WF-10** | hk/kline-adj 或 us/kline（tsCode规则不同！） |
| "宏观 / CPI / PMI / LPR" | **WF-3.7** | macro/cpi+pmi+money-supply+lpr+gdp |
| "ETF / 基金" | **WF-3.6** | fund/etf/list→etf/kline/daily+portfolio+dividend |
| "可转债 / 强赎 / 溢价率" | **WF-3.8** | bond/cb/list→cb/share+cb/price-chg |

> 意图不在上表？→ 先看〔Decision tree〕关键词匹配（含单端点快捷路径如"涨停/ST/游资/指数估值"），再看〔Intent taxonomy〕详细端点，或搜〔不要做的事〕排除陷阱。

## Intent taxonomy — 意图到端点

> 端点路径见 [api-quick-reference.md](./references/api-quick-reference.md)。本节用助记符指代。

### 1. 标的解析（必做第一步）

用户说 "宁德时代"、"茅台"、"那只创业板半导体龙头" ⇒

- `POST /openapi/v1/stock/basic/search` body=`{"nameOrCode": "..."}` → 选出 tsCode
- 多解时列候选并做最小澄清
- **北交所新旧代码对照**：`POST /openapi/v1/stock/basic/bse-mapping`（旧代码 `oCode` / 新代码 `nCode`，⚠️ **字段大写 C**，不是 `ocode`/`ncode`）
- **股票详情**（实控人 / 主营 / 上市日期）：`POST /openapi/v1/stock/basic/detail` body=`{"tsCode":"600519.SH"}`；⚠️ `listDate` 是**毫秒时间戳字符串**（如 `"998841600000"`），`listDateStr` 才是可读的 `YYYYMMDD`；`delistDate` 对在市股票为 `"None"` 字符串非 null
- **全市场精简列表**：`POST /openapi/v1/stock/basic/list` body=`{}`；仅返 tsCode/symbol/name 3 字段，无 industry/area/listDate 等

### 2. 行情 / 趋势

| 口语 | 默认端点 | 默认窗口 |
|------|--------|---------|
| "最近走势怎么样" | `/openapi/v1/stock/kline/daily` (type=11) | 近 20 交易日 |
| "今年以来" | 同上 | 当年初 ~ 今天 |
| "周线 / 月线" | type=12 / 13（`stock/kline/daily`）；或用专用端点 `/stock/kline/weekly-monthly`（freq=`W`/`M`）/ `/stock/kline/week-month-adj`（含复权三套 OHLC）——⚠️ 专用端点底表增量积累，2026-06-08 前仅近几周有数据，历史稀疏时回退到 type=12/13 | 1~3 年 |
| "复权后价格" | `/openapi/v1/stock/kline/adj-factor` + 算 BFQ × factor | 一并查 |
| "盘中分钟 / 分时" | `/openapi/v1/stock/kline/minute` (freq=5min) | 1~5 交易日；**行为特殊**：`freq≠1min` 实时转发 Tushare（5 分钟缓存），`freq=1min` 近 30 交易日读库、更早转发。上游失败返 `code=16`+msg（"上游数据源请求失败…请稍后重试"）——**这不是"没有数据"，等 1 分钟重试一次**；指数分钟历史用 `/stock/index/kline/minutes` |
| "今年涨多少" | `/openapi/v1/stock/kline/percentage-change` | 直接字段 |
| "大盘 / 指数 K 线" | `/openapi/v1/stock/index/kline/daily` | 近 60 天 |
| "指数周线 / 月线" | `/openapi/v1/stock/index/kline/weekly` 或 `/monthly`（⚠️ 响应 `pctChg` 是**小数形式**，0.0113 = 1.13%；与 daily 的百分比形式不同，需 × 100） |  |
| "全球主要指数" | `/openapi/v1/stock/index/global` — ⚠️ **2026-06-08 实测 `data:[]`，底表暂无数据，暂不可用**，如实告知 |  |
| "找指数列表" | `/openapi/v1/stock/index/list` | 一次性查 |
| "申万行业 PE" | `/openapi/v1/stock/index/sw-industry-quo` | 含 PE/PB/MV；⚠️ **tsCode 必填**（申万代码如 `801010.SI` 农林牧渔），不传返空 |
| "主要指数快照" | `/openapi/v1/stock/index/main/snapshot` | 缓存型；历史序列用 `/main/history`（body `{}` 即可） |

### 3. 估值 / 基本面

| 口语 | 端点 |
|------|------|
| "估值高不高 / PE 多少" | `/openapi/v1/stock/indicator/last/by-codes` |
| "估值历史走势 / PE 百分位" | `/openapi/v1/stock/indicator/valuation/history` |
| "ROE 历史" | `/openapi/v1/stock/indicator/roe`（单股 ROE 时间序列；只要最新一期才用 `indicator/last`） |
| "最近几个季度财务" | `/openapi/v1/stock/financial/core` (size=8) |
| "有没有分红" | `/openapi/v1/stock/financial/dividend` |
| "行业横向比较" | 两步：① `POST /openapi/v1/stock/basic/classify` body=`{}` → 拿行业 `id`；② `POST /stock/indicator/last` body=`{id, level}` → 该行业所有个股估值（分页）；⚠️ `/basic/classify/list` 响应是**分类汇总**（classifyName/stockCount/swCode），**不是个股列表**，勿误用；若已知具体 tsCode 列表直接用 `indicator/last/by-codes` |
| "单只股票今天整体快照（行情+估值+财务+股本 一次拿）" | `/openapi/v1/stock/market/bak-daily`（31 字段宽表：OHLCV + pctChange + pe + pb + industry + area + floatMv + totalMv + avgPrice + **动量因子** strength/activity/attack/interval3/interval6；⚠️ `tradeDate` 是毫秒时间戳；比 indicator/last 更轻量但字段更丰富） |
| "股票基本信息快照（行业/地区/pe/eps/bvps/持股户数）" | `/openapi/v1/stock/market/bak-basic`（每日静态快照，24 字段：industry/area/pe/floatShare/totalShare/totalAssets/eps/bvps/pb/listDate(ms)/undp/revYoy/profitYoy/gpr/npr/**holderNum**；与 bak-daily 互补，bak-basic 侧重基本面属性，bak-daily 侧重量价+动量） |

### 3.4 财务报表深度（stock.financial scope）

| 口语 | 端点 |
|------|------|
| "茅台过去 8 季利润表" | `/openapi/v1/stock/financial/income-statement` |
| "资产负债表 / 商誉" | `/openapi/v1/stock/financial/balance-sheet` |
| "现金流好不好" | `/openapi/v1/stock/financial/cash-flow` |
| "ROE / 毛利率 / FCF" | `/openapi/v1/stock/financial/indicator` |
| "主营构成" | `/openapi/v1/stock/financial/business-segment` |
| "回购情况" | `/openapi/v1/stock/financial/repurchase` |
| "大股东质押" | `/openapi/v1/stock/financial/pledge` |
| "业绩预告 / 预增 / 预减 / 盈利预警" | `/openapi/v1/stock/financial/forecast` — ⚠️ **2026-06-08 实测 `data:[]`（PG 迁移缺口，底表暂无数据，暂不可用）**，如实告知用户；不要反复重试 |
| "业绩快报 / 三季报快报 / 提前公告利润" | `/openapi/v1/stock/financial/express`（`tsCode` 必填；日期字段 `annDate`/`endDate` 均是毫秒时间戳；`nIncome`/`nIncomeAttrP` 注意大写 `I`；营收同比 `yoySales`、净利同比 `yoyNetProfit`） |
| "茅台几号公布财报 / 某公司财报披露时间 / 预约披露日" | `/openapi/v1/stock/financial/disclosure-date`（⚠️ `tsCode` **必填**，无法不指定公司批量查"本周所有公司"；所有日期字段均为毫秒时间戳；**核心字段是 `preDate`（预计披露日）**；`actualDate` 尚未披露时为 null；`modifyDate` 非 null 说明公司改过预约；字段名 camelCase，不是 `pre_date`/`actual_date`） |

### 3.5 技术指标（stock.indicator scope）

| 口语 | 端点 | 说明 |
|------|------|------|
| "MA / BOLL" | `/openapi/v1/stock/indicator/ma-channel` | MA/EMA/BOLL/KTN/TAQ/EXPMA |
| "MACD/RSI/KDJ" | `/openapi/v1/stock/indicator/oscillator` | 振荡 + 情绪 |
| "ATR/OBV/动量" | `/openapi/v1/stock/indicator/trend-volume` | 趋势 + 量能 |
| "短线 19 因子" | `/openapi/v1/stock/indicator/short-term` | 量化短线打分 |
| "九转反转" | `/openapi/v1/stock/indicator/nine-turn` | DeMark 九转 |
| "估值历史百分位" | `/openapi/v1/stock/indicator/valuation/history` | 每天 PE/PB |
| "指数因子宽表 / 沪深300技术因子" | `/openapi/v1/stock/indicator/idx-factor-pro`（⚠️ **传指数 tsCode**，如 `"000300.SH"`，不是个股代码；89 列宽表，含 MA/EMA/MACD/KDJ/RSI/BOLL/OBV 等 87 个 BFQ 量化因子；`tradeDate` 是毫秒时间戳） | 指数专用 |

> 默认 `adjType="bfq"`；量化策略请用 `hfq` 或 `qfq`。默认窗口 60 自然日。

### 4. 资金流 / 席位

| 口语 | 端点 |
|------|------|
| "主力买没买" | `/openapi/v1/stock/market/moneyflow` |
| "板块资金榜" | `/openapi/v1/stock/market/plate/cash-flow` |
| "持续被资金关注" | `/openapi/v1/stock/market/plate/continue-net` |
| "近几天龙虎榜" | `/openapi/v1/stock/market/lhb/latest-dates` → `/openapi/v1/stock/market/lhb/list` |
| "哪些机构/游资在买" | `/openapi/v1/stock/market/lhb/details` |
| "北向最近买什么（个股十大）" | `/openapi/v1/stock/market/hsgt-top10`（⚠️ `tradeDate` **必填** YYYYMMDD；先用 `lhb/latest-dates` 取最近交易日，再传入；不传返空） |
| "北向 / 南向今天净流入多少（整体）" | `/openapi/v1/stock/market/hsgt-moneyflow` |
| "大宗交易" | `/openapi/v1/stock/market/block-trade` |
| "游资名录" | `/openapi/v1/stock/market/hm-list` |
| "某游资今天买了哪些票 / 游资交易明细" | `/openapi/v1/stock/market/hm-detail`（`tradeDate` YYYYMMDD；⚠️ `hmOrgs` 是**平文本字符串**不是 JSON 数组，别 JSON.parse；`tradeDate` 响应是毫秒时间戳） |
| "营业部 / 券商席位明细" | `/openapi/v1/stock/market/broker-trade`（`nameKeyword` 模糊搜营业部） |
| "机构买卖明细" | `/openapi/v1/stock/market/institution-trading` |
| "东财口径个股资金流" | `/openapi/v1/stock/market/moneyflow-dc`（tsCode 必填；默认口径用 `moneyflow`） |

### 4.5 异动深度（stock.market scope 第二批）

| 口语 | 端点 |
|------|------|
| "今天涨停 / 几连板" | `/openapi/v1/stock/market/limit-analysis`（`tradeDate` YYYYMMDD，`limitStat="U"` 涨停 / `"D"` 跌停） |
| "连板天梯（几连板有哪些票）" | `/openapi/v1/stock/market/limit-step`（`tradeDate` YYYYMMDD；⚠️ 响应 `tradeDate` 是毫秒时间戳；`nums` 是连板数 string） |
| "涨停最强板块 / 连板板块统计" | `/openapi/v1/stock/market/limit-cpt-list`（`tradeDate` YYYYMMDD；⚠️ 响应 `tradeDate` 同为毫秒时间戳；含 `upStat`/`consNums`/`upNums` 连板强度字段） |
| "今天热榜 / 同花顺热股" | `/openapi/v1/stock/market/ths-hot`（**首选**，同花顺热榜，涵盖 A股热股/港股/行业板块/概念板块/期货/美股；`dataType` 传中文标签过滤；响应 `tradeDate` 是毫秒时间戳，用 `rankTime` 字段做时间标注更直观） |
| "东财热榜" | `/openapi/v1/stock/market/hot-rank`（⚠️ **底表暂无数据，返回 `data:[]`**；热度需求请改用 `/ths-hot`（同花顺，数据最新））|
| "盘前情绪 / 集合竞价" | `/openapi/v1/stock/market/auction-open`（尾盘竞价用 `/auction-close`） |
| "筹码胜率" | `/openapi/v1/stock/market/cyq-perf`（`tsCode` 必填；⚠️ `tradeDate` 是 YYYYMMDD 字符串，非毫秒——属于 stock.market scope 内例外，同 moneyflow/block-trade/mainboard） |
| "筹码分布 / 获利盘比例 / 套牢盘" | `/openapi/v1/stock/market/cyq-chips`（`tsCode` 必填；响应 `tradeDate` 是毫秒时间戳；每行一个价格档位：`price`/`percent`（该档筹码比例%），可拼出筹码山图） |
| "开盘啦榜单（涨停时间/主题/封板资金）" | `/openapi/v1/stock/market/kpl-list`（含 `luTime`/`ldTime`/`status` 首板/N连板/`theme` 主题） |
| "开盘啦题材成分 / 某题材包含哪些股票" | `/openapi/v1/stock/market/kpl-concept-cons`（`tsCode` 传题材代码；`conCode` = **个股代码**非题材代码；`description` = 题材描述文字，原 Tushare `desc` 改名，⚠️ 别用 `desc`） |
| "新能源汽车概念股" | `/openapi/v1/stock/market/ths-concept`（`tsCode` 传 `885xxx.TI` 概念板块代码；**⚠️ 与 `ths-index`/`ths-daily` 使用的 `700xxx.TI` 指数代码系不同**） |
| "股吧热度 / 讨论度" | `/openapi/v1/stock/market/guba-rank`（⚠️ 底表暂空，用 `ths-hot` 替代） |
| "市场新闻情绪指数" | `/openapi/v1/stock/market/news-sentiment`（`tradeDate` 是 YYYYMMDD 字符串，⚠️ 非毫秒；响应字段：`avgSentimentScore`（-1~1）/ `newsVolumeMa5`/ `newsSurgeRatio`（量比）/ `srcDiversity`） |
| "大盘整体行情（成交额/涨跌家数）" | `/openapi/v1/stock/market/mainboard`（tradeDate 或 startDate/endDate 至少传一个；⚠️ `netAmount` 单位是**亿元**（不是元/万元）；`tradeDate` 是 YYYYMMDD 字符串） |
| "A股大宗交易 / 哪只股票有大宗成交" | `/openapi/v1/stock/market/block-trade`（`tsCode` 必填；⚠️ `vol` 单位是**万股**（不是手！），`amount` 是**万元**；`tradeDate` 是 YYYYMMDD 字符串；`buyer`/`seller` 是买卖方营业部全称） |
| "今天哪些股票被 ST / 新增 ST" | `/openapi/v1/stock/market/st-daily`（`tradeDate` YYYYMMDD；响应 `tradeDate` 是毫秒时间戳；`type` 字段="ST"/"*ST" 等） |
| "某股为什么被 ST / ST 事件详情" | `/openapi/v1/stock/market/st-warning`（`tsCode` 必填；⚠️ `stType` 可为空字符串 `""` 而非 null；`pubDate`/`impDate` 是毫秒时间戳；`stExplain` 是完整公告文本） |

### 5. 板块 / 行业

| 口语 | 端点 |
|------|------|
| "哪个板块最强" | `/openapi/v1/stock/market/plate`（无参快照，body `{}`；按类型/日期筛用 `plate/list`） |
| "半导体板块成分" | `/openapi/v1/stock/market/plate/list` → `/plate/stocks-indicator` |
| "这只票属于哪些板块" | `/openapi/v1/stock/market/plates-by-stock` |
| "申万行业热力图" | `/openapi/v1/stock/index/sw-heatmap` — ⚠️ **2026-06-08 实测 `data:[]`（PG 数据迁移缺口，暂无可用数据）**；替代：用 `sw-industry-quo`（日 K + 估值）手动绘制 |
| "同花顺行业指数 / THS 指数列表" | `/openapi/v1/stock/market/ths-index`（返回 `700xxx.TI` 代码系；⚠️ 与 `ths-concept`/`ths-hot` 的 `885xxx.TI` 代码系不同，不要混用；`type` 过滤：`I`=行业/`BB`=宽基/`ST`=风格/`TH`=特色） |
| "同花顺行业指数日行情" | `/openapi/v1/stock/market/ths-daily`（`tsCode` 传 `700xxx.TI` 代码；响应 `tradeDate` 是毫秒时间戳；含 open/high/low/close/vol/turnoverRate/totalMv/floatMv） |
| "通达信板块 / 通达信行业列表" | `/openapi/v1/stock/market/tdx-index`（板块基础信息：idxType/idxCount/totalMv/floatMv；`tradeDate` 是毫秒时间戳） |
| "通达信板块行情 / 近期涨跌表现" | `/openapi/v1/stock/market/tdx-daily`（35 字段宽表，含 OHLC/vol/pctChange/return3Day/return5Day/return10Day/return20Day/return60Day/mtd/ytd/return1Year；`tradeDate` 是毫秒时间戳） |
| "通达信板块成分股" | `/openapi/v1/stock/market/tdx-member`（`tsCode` 板块代码传参；字段 4 个：tradeDate(ms)/tsCode/conCode/conName） |
| "中信行业指数日行情 / CI 行业板块涨跌" | `/openapi/v1/stock/market/ci-daily`（`tsCode` 传中信行业代码，如 `"CI005001.CI"`；响应 `tradeDate` 是毫秒时间戳；含 OHLC/vol/amount/change/pctChange%；scope=`stock.plate`） |
| "中信行业指数成分股 / CI 成分（三级体系）" | `/openapi/v1/stock/market/ci-index-member`（⚠️ 响应**无 `tradeDate` 字段**；完整 11 字段：l1Code/l1Name/l2Code/l2Name/l3Code/l3Name/tsCode/name/inDate(ms，纳入日期)/outDate(ms，剔除日期，可null)/isNew("Y"/"N")；scope=`stock.plate`） |
| "指数成分股权重 / 沪深 300 权重" | `/openapi/v1/stock/index/weight`（`indexCode` 传指数代码，如 `000300.SH`；响应 `tradeDate` 是**毫秒时间戳**（月度发布日）；输入 `tradeDate` 用 YYYYMMDD；每月底更新） |
| "指数估值快照 / 沪深 300 PE/PB 历史" | `/openapi/v1/stock/index/dailybasic`（`tsCode` 传指数代码；响应含 pe/pb/totalMv/freeMv；`tradeDate` 是毫秒时间戳） |

### 6. 选股模型（stock.selection scope）

| 口语 | 端点 |
|------|------|
| "ML 今天选了哪些票" | `/openapi/v1/stock/selection/ml/results`（可选过滤：`signalType="BUY"/"HOLD"/"WATCH"`；`minScore` 0~1 阈值，`0.6` 为常用值） |
| "短线博弈机会" | `/openapi/v1/stock/selection/momentum/results`（可选过滤：`minScore`；`minConceptCount` 最少热门概念叠加数，如 `3`；⚠️ `minConceptCount` 不是 `min_concept_count`） |
| "长线价值 / 按申万行业找价值股" | `/openapi/v1/stock/selection/value/results`（可选过滤：`l1Code` 申万一级代码，如 `"801080"` 电子；`minScore`；⚠️ `l1Code` 不是 `l1_code`） |
| "重新跑一遍 ML / 动量 / 价值" ⚠ | `/openapi/v1/stock/selection/{ml,momentum,value}/execute` |

> ⚠️ **三个 `*/results` 的 `tradeDate` 必传真实日期**（后端 SQL 精确等值匹配）：**不传 = 必空**（没有"默认最新"），传占位符字面量也是空——这是〔时间字段规范〕"今天→不传时间"通用规则的**例外**。拿最新日期：先 `POST /stock/market/lhb/latest-dates body={}` 取最近 A 股交易日填入；若当日结果为空（模型当天还没跑），**回退前一交易日再试一次**（最多回退 2 天，仍空才向用户报告，这是合法的日期回退，不算"循环重试"）。

### 6.5 宏观经济（market scope，Pro）

| 口语 | 端点 | 时间格式 |
|------|------|---------|
| "CPI / PPI / 通胀" | `/openapi/v1/market/macro/cpi` 或 `/ppi` | YYYYMM |
| "PMI / 景气度" | `/openapi/v1/market/macro/pmi` | YYYYMM |
| "GDP" | `/openapi/v1/market/macro/gdp` | YYYYQX |
| "M2 / 货币供应" | `/openapi/v1/market/macro/money-supply` | YYYYMM |
| "社融" | `/openapi/v1/market/macro/social-finance` | YYYYMM |
| "Shibor" | `/openapi/v1/market/macro/shibor` | YYYYMMDD |（⚠️ 响应日期字段名是 `date`（YYYYMMDD 字符串），不是 `tradeDate`） |
| "LPR / 降息" | `/openapi/v1/market/macro/lpr` | YYYYMMDD |（⚠️ 响应日期字段名是 `date`；LPR 值在 `y1`（1年期）/`y5`（5年期）字段，不是 `lpr1y`/`lpr5y`） |
| "宏观月度总览（一次拿全）" | `/openapi/v1/market/macro/monthly` | YYYYMM |
| "政策新闻 / 资讯" | `/openapi/v1/market/news/list` | YYYYMMDD（⚠️ 此端点属 `news` scope，需 **Max** 套餐；正式政策文件用 `/market/macro/policy-npr`，属 `market` scope，Pro 可用） |
| "本周有哪些经济数据 / 财经日历 / 重要事件" | `/openapi/v1/market/macro/eco-cal` | 请求 startDate/endDate YYYYMMDD；⚠️ 响应 `date` 字段是**毫秒时间戳**（不是 YYYYMMDD！）、`time` 是 `"HH:mm"` 字符串；`country` 是**事件分类代码**（`"economic_activity"` 等），按国家过滤用 `currency`（`"CNY"` 筛中国，`"USD"` 筛美国） |

### 6.7 港股（stock.hk scope，Max+）

| 口语 | 端点 | 备注 |
|------|------|------|
| "腾讯 / 港股代码列表" | `/openapi/v1/stock/hk/basic` | 可选 `listStatus=L` 只看上市中 |
| "港股交易日历" | `/openapi/v1/stock/hk/tradecal` | 节假日 ≠ A 股；⚠️ 响应日期字段是 `calDate`（不是 `tradeDate`！），毫秒时间戳 |
| "港股 K 线" | `/openapi/v1/stock/hk/kline` 或 `/kline-adj` | `kline-adj` 含复权 + 估值；⚠️ `hk/kline` 的 `vol` 单位是**股**（不是万手），`amount` 单位是**港元**（不是千元）；`kline-adj` 的涨跌幅字段是 `pctChange`（而非 `pctChg`） |
| "港股复权因子" | `/openapi/v1/stock/hk/adj-factor` | HFQ = BFQ × `cumAdjfactor` / 最新（**注意**：港股/美股 adj-factor 字段是 `cumAdjfactor`，A股 adj-factor 字段是 `adjFactor`，两者不同） |
| "港股分钟 K" | `/openapi/v1/stock/hk/minute` | ⚠ 时间格式 `YYYY-MM-DD HH:mm:ss` |
| "港股利润 / 资产 / 现金流" | `/openapi/v1/stock/hk/income` / `/balance-sheet` / `/cash-flow` | **long format**，透视方法见 WF-10 |
| "港股财务指标" | `/openapi/v1/stock/hk/fina-indicator` | 36 列，可选 `reportType` 过滤（值用 `"2024年中报"` 完整串，不传就别传）|

> ⚠️ 港股三大表（income/balance-sheet/cash-flow）和 fina-indicator **采集覆盖约前 100 只港股**（按代码字母序），中小盘港股返 `data:[]` 是覆盖不足，不是端点坏了。
> 港股通**南向**持股不在此 scope（在 `stock.shareholder` → `/openapi/v1/stock/shareholder/hk-hold`），别混。

### 6.8 美股（stock.us scope，Max+）

| 口语 | 端点 | 备注 |
|------|------|------|
| "苹果 / 美股列表" | `/openapi/v1/stock/us/basic` | 可选 `classify=ADR/GDR/EQ` |
| "美股交易日历" | `/openapi/v1/stock/us/tradecal` | 与 A 股 / 港股全不同；⚠️ 响应日期字段是 `calDate`（不是 `tradeDate`！），毫秒时间戳 |
| "美股 K 线" | `/openapi/v1/stock/us/kline` 或 `/kline-adj` | `kline` 已含 pe/pb 估值 + vwap；⚠️ `kline-adj` **无** pe/pb（需估值改用 `kline`，见 ❌ "查美股估值" entry） |
| "美股复权因子" | `/openapi/v1/stock/us/adj-factor` | |
| "美股利润 / 资产 / 现金流" | `/openapi/v1/stock/us/income` / `/balance-sheet` / `/cash-flow` | **long format**，透视方法见 WF-10 |
| "美股财务指标" | `/openapi/v1/stock/us/fina-indicator` | 29 列，可选 `reportType` 过滤（值用 `"2025/Q1"` / `"2023/FY"` 形式） |

### 6.9 研报 / 卖方评级（stock.research scope，Plus+）

| 口语 | 端点 |
|------|------|
| "茅台最近有什么研报" | `/openapi/v1/stock/research/report`（可选 `org` 过滤券商） |
| "卖方一致预期 / 目标价" | `/openapi/v1/stock/research/report-rc`（含 `eps/pe/roe/maxPrice/minPrice/rating`；响应日期字段名是 `reportDate` 不是 `tradeDate`） |
| "本月金股" | `/openapi/v1/stock/research/broker-recommend`（按 `month` 比对 `startDate[:6]`） |

> ⚠️ **采集覆盖仅约 170 只股票**：库内研报/预测数据靠 polling 每日增量采集，存量依赖 Tushare 权限。旗舰标的（600519.SH/000858.SZ 等）实测 `data:[]`；`tsCode` 不传则按全库返回可验证端点是否正常。

### 6.10 国际宏观（stock.intl-macro scope，Max+；路径前缀 `/openapi/v1/intl-macro/...` 不带 `stock/`）

> ⚠️ **9 个端点响应日期字段均是 `date`（毫秒时间戳 long），不是 `tradeDate`**；展示时需 `÷1000|strftime`。与国内宏观（`macro/shibor`/`macro/lpr` 的 `date` 是 YYYYMMDD 字符串）格式不同。

| 口语 | 端点 | 说明 |
|------|------|------|
| "美债收益率曲线 / 期限利差" | `/openapi/v1/intl-macro/us-tycr` | 13 期限：1M-30Y |
| "美债实际收益率 / TIPS" | `/openapi/v1/intl-macro/us-trycr` | 5Y-30Y；与 tycr 同期限相减 ≈ 隐含通胀 |
| "美国短期国债" | `/openapi/v1/intl-macro/us-tbr` | 4w-52w，Bd / Ce 两口径；⚠️ `w17Bd`/`w17Ce` 常为 null，正常现象 |
| "美债长端 LTC / CMT" | `/openapi/v1/intl-macro/us-tltr` 或 `/us-trltr` | 30Y 缺失时段的替代基准 |
| "HIBOR" | `/openapi/v1/intl-macro/hibor` | 港元同业，8 期限 |
| "LIBOR" | `/openapi/v1/intl-macro/libor` | 可选 `currType=USD/EUR/JPY/GBP/CHF`；⚠ 2023-06 后多数已退役 |
| "民间利率" | `/openapi/v1/intl-macro/gz-index` 或 `/wz-index` | 广州 / 温州民间借贷 |

> **境内**宏观（CPI/PPI/GDP/M2/Shibor/LPR）在 `market` scope，不在这里。

### 6.11 外汇（forex scope，Max）

| 口语 | 端点 |
|------|------|
| "外汇产品 / EURUSD 元数据" | `/openapi/v1/forex/obasic`（`tsCode` 格式 `"USDCNH.FXCM"` / `"EURUSD.FXCM"`；可按 `classify="FX"/"CFD"` 或 `exchange="FXCM"/"OANDA"` 过滤） |
| "外汇日报价" | `/openapi/v1/forex/daily`（bid/ask 双边 OHLC；点差 = askClose − bidClose；⚠️ 响应 `tradeDate` 是**毫秒时间戳**） |

### 6.12 TMT 媒体（tmt scope，Ultra · 内部不外卖）

| 口语 | 端点 | 说明 |
|------|------|------|
| "今日票房" | `/openapi/v1/tmt/bo-daily` | date DESC + rank ASC |
| "本周 / 本月票房" | `/openapi/v1/tmt/bo-weekly` 或 `/bo-monthly` | weekly date=周一 |
| "影院上座率" | `/openapi/v1/tmt/bo-cinema` | 可选 `cName` 影院名 |
| "电影 / 电视剧备案" | `/openapi/v1/tmt/film-record` 或 `/teleplay-record` | 备案号 / 名称模糊匹配 |
| "台湾电子月营收" | `/openapi/v1/tmt/twincome` 或 `/twincome-detail` | `date` 格式 `YYYYMM` |

### 7. 新闻 / 事件（`news` scope，**Max+**）

| 口语 | 端点 |
|------|------|
| "最近有啥消息" | `/openapi/v1/market/news/list`（`startDate`=近7天；`titleKeyword` 关键词过滤；⚠️ 响应 `title` 可能为 null，展示时优先用 `newsTimeStr`（可读字符串如 `"2026-06-07 22:12:08"`）而非 `newsTime`（毫秒时间戳）） |
| "新闻来源字典（sina/cls/eastmoney 对应什么名字）" | `/openapi/v1/market/news/types`（⚠️ 返回**来源 source 字典**，字段 `code`/`displayName`/`description`；`code` 对应 `news/list` 响应的 `src` 字段，**不是** `type` 整数值的字典） |

### 8. 股东视角（stock.shareholder scope）

| 口语 | 端点 |
|------|------|
| "社保 / 汇金 持了啥" | `/openapi/v1/stock/shareholder/holder/find-stocks` |
| "某股东最新持仓明细" | `/openapi/v1/stock/shareholder/holder/holdings` |
| "股东类别字典" | `/openapi/v1/stock/shareholder/classify/list` — ⚠️ **底表暂无数据（PG 迁移后未回填）**，返回空列表；股东类别信息改从 `holder/holdings` 响应的 `holderCategory`/`holderType` 字段取 |
| "腾讯 / 港股 CCASS 持股汇总（机构数/持仓比）" | `/openapi/v1/stock/shareholder/ccass-hold`（`tsCode` 传港股代码如 `"00700.HK"`；响应 `tradeDate` 毫秒时间戳；含 `shareholding`/`holdNums`/`holdRatio`） |
| "CCASS 持股明细 / 哪些机构持有腾讯" | `/openapi/v1/stock/shareholder/ccass-detail`（`tsCode` 传港股代码；每行一个 CCASS 参与者：`colParticipantId`/`colParticipantName`/`colShareholding`/`colShareholdingPercent`） |
| "北向资金今天持有哪些 A 股 / 陆股通持仓" | `/openapi/v1/stock/shareholder/hk-hold`（`exchange=SH` 沪股通北向 / `exchange=SZ` 深股通北向；⚠️ 在 `stock.shareholder` scope，不在 `stock.hk`） |
| "南向港股通持仓" | 同 `hk-hold`，传 `exchange=HK` + `tsCode` 港股代码 |
| "哪些 A 股可以用港股通买（陆港通名单）" | `/openapi/v1/stock/shareholder/hsgt-list`（`type` 过滤：`HK_SH`=北向上证A股 / `HK_SZ`=北向深证A股 / `SH_HK`/`SZ_HK`=南向港股通；不传 `type` 返全部） |
| "港股通每日成交量" | `/openapi/v1/stock/shareholder/ggt-daily`（市场级汇总，无 tsCode；`buyAmount`/`sellAmount` 单位**亿元**；`buyAmount - sellAmount` = 净流入） |
| "港股通每月成交统计" | `/openapi/v1/stock/shareholder/ggt-monthly`（`month` 字段是 `YYYYMM` 字符串如 `"202504"`；含日均/月总买卖额和笔数） |

### 8.5 基金 / ETF（fund scope，Max）

| 口语 | 端点 |
|------|------|
| "公募基金列表 / 找债券型基金 / 混合型基金" | `/openapi/v1/fund/list`（`fundType` 过滤如 `"债券型"`/`"混合型"`；`status="L"` 取存续；日期字段均为 YYYYMMDD 字符串（⚠️ 与 ETF list 不同）；场外基金 `listDate` 为 null；`market="O"` 场外/`"E"` 场内） |
| "找沪深 300 的 ETF" | `/openapi/v1/fund/etf/list`（⚠️ `exchange` 过滤只认短形式 `"SH"`/`"SZ"` / `"BSE"`，传 `"SSE"`/`"SZSE"` 静默返 0 条） |
| "ETF 最近表现" | `/openapi/v1/fund/etf/kline/daily`（⚠️ 响应 `vol` 单位是**手**，`amount` 单位是**元**；与 A 股日 K 的 vol=手/amount=千元不同，引用数字时务必标单位） |
| "ETF 份额变化 / ETF 规模" | `/openapi/v1/fund/etf/share-history`（⚠️ `totalShare` 单位是**份**，`totalSize` 单位是**元**；不是万份/万元；展示时注意量级；tradeDate 是毫秒时间戳） |
| "公募基金份额历史（非ETF）" | `/openapi/v1/fund/share/history`（⚠️ 仅 3 字段：tsCode/tradeDate/fdShare；tradeDate 是 **YYYYMMDD 字符串**；fdShare 单位是**万份**；不含净值/规模，净值另调 `/fund/nav/history`） |
| "基金净值" | `/openapi/v1/fund/nav/history` |
| "基金持仓" | `/openapi/v1/fund/portfolio` |
| "基金分红" | `/openapi/v1/fund/dividend` |
| "基金经理 / 谁在管" | `/openapi/v1/fund/manager/list`（`tsCode` 与 `managerName` 至少一个） |
| "各渠道公募基金销售保有占比（银行 / 券商 / 基金公司）" | `/openapi/v1/fund/sales/ratio`（年度；body `{}` 取全部；字段：`year`/`bank`/`secComp`/`fundComp`/`indepComp`/`rests`，单位 %） |
| "基金销售机构规模排名" | `/openapi/v1/fund/sales/vol`（季度；`year` + `quarter` 过滤，`quarter` 是 `"Q1"~"Q4"` 字符串；含 `instName`/`fundScale`(非货基亿元)/`scale`(总规模亿元)/`rank`） |

### 8.7 衍生品（derivative scope，Max）

| 口语 | 端点 |
|------|------|
| "铜期货日 K" | `/openapi/v1/derivative/futures/kline/daily` |
| "铜期货周线 / 月线" | `/openapi/v1/derivative/futures/kline/weekly-monthly`（`tsCode` + `freq`=`W`/`M` 必填；⚠️ 当前底表数据稀疏，部分合约可能返空，回退日 K 降频） |
| "找黄金期货合约" | `/openapi/v1/derivative/futures/list` |
| "期货主力连续" | `/openapi/v1/derivative/futures/main-contract` |
| "期货公司持仓 / 席位净持仓" | `/openapi/v1/derivative/futures/holding`（⚠️ 入参字段是 **`symbol`** 品种代码，如 `"CU"`/`"RB"`，**不是** `tsCode`；`futures/wsr` 仓单同理） |
| "50ETF 期权 / 中证1000 股指期权 / 豆粕期权有哪些合约" | `/openapi/v1/derivative/option/contracts`（ETF/股指/商品/能源全 8 所覆盖，只给合约元数据无价格） |
| "某只期权某天最低/最高/收盘/结算价" | `/openapi/v1/derivative/option/kline/daily`（**单合约**，问句带日期=查日 K，必传合约码 tsCode） |
| "全市场期权按某日价格条件筛选/跨日比价排序（如 6/3最低÷6/2收盘≤50%）" | `/openapi/v1/derivative/option/kline/daily-by-date`（**全市场**按交易日整拉，startDate必填+可选exchange，分页100/页；别逐合约调几万次。跨日 join/过滤/排序在 agent 侧算，先剔 low=0/vol=0 没成交行） |
| "黄金 T+D" | `/openapi/v1/derivative/sge/kline/daily` |

### 8.9 债券 / 可转债（bond scope，Max）

| 口语 | 端点 |
|------|------|
| "正股对应的转债" | `/openapi/v1/bond/cb/list`（⚠️ `issueSize` 单位是**元**，如 `6000000000.0` = 60亿；展示时 ÷ 1e8 得亿元） |
| "转债日 K + 溢价率" | `/openapi/v1/bond/cb/daily`（⚠️ **2026-06-08 实测 `data:[]`，底表暂无数据（PG 迁移缺口）**——拿到空直接说明，别重试） |
| "转股进度" | `/openapi/v1/bond/cb/share` |
| "强赎 / 回售" | `/openapi/v1/bond/cb/call`（⚠️ **同上，底表暂无数据**） |
| "转债技术因子" | `/openapi/v1/bond/cb/factor`（⚠️ **2026-06-08 实测 `data:[]`，底表暂无数据（PG 迁移缺口）**） |
| "转债发行 / 中签率" | `/openapi/v1/bond/cb/issue`（⚠️ **同上，底表暂无数据**） |
| "转股价下修" | `/openapi/v1/bond/cb/price-chg`（⚠️ 字段名陷阱：`convertpriceBef`/`convertpriceAft` 中 `price` 全小写，与同端点的 `convertPriceInitial`（大写 P）不一致，一定要全小写写法） |
| "转债大宗交易（日汇总）" | `/openapi/v1/bond/blk`（`tradeDate` 必填；字段 6 个：tradeDate/tsCode/name/price/vol(手)/amount(万元)） |
| "转债大宗交易逐笔（买卖方营业部）" | `/openapi/v1/bond/blk-detail`（同上；多 `buyDp`/`sellDp` 营业部全名字段） |
| "GC001 利率" | `/openapi/v1/bond/repo/daily` |
| "国债收益率曲线" | `/openapi/v1/bond/yc`（⚠️ `tradeDate` 或 `startDate`/`endDate` **必传**，否则无过滤全库返空） |

### 9. 异动监控（stock.market / stock.kline scope）

| 口语 | 端点 |
|------|------|
| "今天有没有突然放量" | `GET /openapi/v1/stock/market/volume-breakout` ← 唯一的 GET |
| "连续涨停的 / 几连板" | `/openapi/v1/stock/kline/limit-up`（form 含 `tadeDays`/`limitUpNum`；`tadeDays` **就是这么拼**——后端历史拼写，别"纠正"成 `tradeDays`，会被静默忽略；⚠ `kline/limits` 是**每日涨跌停价格表**，不是连板筛选，别混） |
| "今天涨停价 / 跌停价" | `/openapi/v1/stock/kline/limits` |
| "K 线形态 / W 底识别" | `/openapi/v1/stock/kline/graph-type`（**只支持 W 双底 `type:4`**，其他形态未实现返回空） |

***

## ⏰ 时间字段规范（必读）

请求时**只用 3 个字段**：`tradeDate`（单日）/ `startDate`（起始）/ `endDate`（截止）。响应里的 `annDate / publishDate / navDate / quarter` 是返回字段，**不要回填到请求 body**。

### 格式速查

| 格式 | 适用 | 示例 |
|------|------|------|
| `YYYYMMDD` | **绝大多数端点（默认）**：K 线 / 财务 / 龙虎榜 / 板块 / 资金流 / 估值 / 转债 / 期货 / ETF / 基金净值 / 大宗 等 | `"20260430"` |
| `YYYYMM` | 宏观月度：CPI / PPI / PMI / M2 / 社融 / 月度宏观聚合 | `"202604"` |
| `YYYYQX` | GDP（仅 `/market/macro/gdp`），X=1/2/3/4 | `"2024Q4"` |
| `YYYYMMDDHHmm` | 分钟 K（罕见）：`*/kline/minutes` 边界 | `"202604301430"` |

### 禁止格式

- ❌ `"2026-04-30"`（带 `-`）/ `"2026/04/30"` / ISO 8601 / Unix 时间戳——**全部被当未传，端点拿默认值/空数据**
- ❌ 单日端点（form 字段是 `tradeDate`）传 `startDate/endDate`，反之亦然——**严格按每个端点 form 字段表**

### 用户口语 → body 字段

| 用户说 | 怎么填 |
|--------|--------|
| "今天" | **不传时间字段**（端点自动取最新交易日）；非要传就 `tradeDate=<今天 YYYYMMDD>`。⚠ **例外**：`selection/*/results` 必传真实日期（不传=必空，见 §6 警示） |
| "昨天" / "上周五" / "5 月 1 日" | `tradeDate=<具体日 YYYYMMDD>`，**agent 自己算日期**，不让用户算 |
| "最近 / 这周 / 近 1 个月" | **不传时间** + `size` 控制（默认 50 条够用）；或 `startDate=今天-N天 endDate=今天` |
| "今年以来 / YTD" | `startDate="<当年>0101", endDate=<今天 YYYYMMDD>` |
| "2024 年 / 去年" | `startDate="20240101", endDate="20241231"` |
| "近 8 季财报" | **不传时间**，`size=8`（端点按 endDate 倒序自然给最近 8 期） |
| "Q1 / 第一季度" | 财务用 `endDate="<年>0331"`；GDP 用 `quarter="<年>Q1"` |

### 用户不给范围时的默认窗口（agent 心算）

| 用户表达 | agent 应该填什么 |
|---------|-----------------|
| "最近走势 / 最近表现" | 不传时间 + `size=20`（≈ 20 交易日） |
| "近期 / 这段时间" | `startDate=今天-90天 endDate=今天` |
| "这两年" | `startDate=今天-2年 endDate=今天` + 必要时分段（日 K 单次 ≤ 2 年） |
| "最近几个季度财报" | 不传时间 + `size=8` |
| "近期资金流" | 不传时间 + `size=20`（资金流端点按 `tradeDate` 倒序） |
| "近几天龙虎榜" | 先 `POST /openapi/v1/stock/market/lhb/latest-dates body={}` 拿可用日期 → 再调 list |

***

## Entity resolution rules

**三个市场的解析路径完全不同，别拿 A 股的 search 去搜港美股：**

- **A 股（默认市场）**：输入可能是中文名、简称、纯数字代码 `000001`、`ts_code` `000001.SZ`。先调 `POST /openapi/v1/stock/basic/search`(body=`{"nameOrCode":"..."}`) 规范化到 `tsCode`。重名（如"平安"）→ 列候选让用户二选一。
- **港股（stock.hk scope，Max+）**：tsCode 形如 `00700.HK`。**没有名称搜索端点**——`/openapi/v1/stock/hk/basic` 只支持 `tsCode` 精确过滤：
  - 用户给数字代码（"00700"/"0700"）→ 左补零到 5 位拼 `00700.HK`，用 `basic` body=`{"tsCode":"00700.HK"}` 查一次**验证存在并拿正式名称**；
  - 用户给中文名（"腾讯"）→ `basic` body=`{"listStatus":"L","size":100}` 翻页拉列表，agent 侧按 `name` 字段模糊匹配（约 2600 只，二三十页内能扫完）。⚠️ 列表按 **list_date 倒序**排（新上市在前），老牌大票（腾讯/00700.HK 上市2004年）可能排在第 ~20 页才出现；**如果知道代码直接传 tsCode 最高效**。
- **美股（stock.us scope，Max+）**：tsCode 就是**裸 ticker**（`AAPL` / `TSLA` / `JPM`），**没有 `.O`/`.N` 交易所后缀**——带后缀查询会静默返空（2026-06-07 实测，旧文档曾写反）。唯一带点的是股份类别码（`BRK.A` / `BF.B` / SPAC 单元 `.U`），照原样传。不确定时 `/openapi/v1/stock/us/basic` 按 ticker/enname 前缀匹配确认（优先 `classify=EQ` 收窄）。
- ⚠️ **`/stock/basic/search` 只收录 A 股**——拿它搜"腾讯（港）/苹果（美）"返回空是正常的，**不代表后端没有港美股数据**（数据在 `stock.hk`/`stock.us` scope）。别因此对用户说"查不到这只票"（违反〔第一铁律〕）。
- 板块有"东财"/"申万"两套口径：`/stock/market/plate*` 走东财，`/stock/index/sw*` 走申万。结论里要注明。

***

## Workflow templates — 默认编排

> ⚠️ **模板里的 `<尖括号>`（`<单只>` `<D>` `<板块ts_code>` `<转债tsCode>` 等）是流程示意符，发请求前必须替换成上一步拿到的真实值**。body 里出现任何 `<...>` / `${...}` 字面量 = 后端当未传 → 静默拿默认值或空数据（见〔⛔ 不要做的事〕占位符红线）。模板路径是 `/stock/...` 简写，实际请求前面拼 `${BASE}/openapi/v1`。

### WF-1 单标的行情快照

**可直接复制运行的 bash 模板（茅台示例，替换 NAME 即可）：**

```bash
NAME="茅台"   # ← 改这里

# Step 1: 解析 tsCode
R=$(curl -sf -X POST "${BASE}/openapi/v1/stock/basic/search" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"nameOrCode\":\"${NAME}\"}")
TS=$(echo "$R" | jq -r '.data[0].tsCode')
echo "tsCode = $TS"

# Step 2: 4 个端点并行（互无依赖，可同时发）
curl -sf -X POST "${BASE}/openapi/v1/stock/kline/daily" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"type\":11,\"size\":20}" > /tmp/kline.json &

curl -sf -X POST "${BASE}/openapi/v1/stock/indicator/last/by-codes" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCodes\":[\"${TS}\"]}" > /tmp/indicator.json &

curl -sf -X POST "${BASE}/openapi/v1/stock/kline/percentage-change" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\"}" > /tmp/pct.json &

curl -sf -X POST "${BASE}/openapi/v1/stock/market/moneyflow" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"size\":10}" > /tmp/flow.json &

wait   # 等 4 个并行结束

# Step 3: 提取关键字段
echo "=== 最近 K 线 (tradeDate 带横杠字符串) ==="
jq -r '.data[-3:] | .[] | [.tradeDate, .close, .pctChg] | @tsv' /tmp/kline.json

echo "=== 估值 (tradeDate 毫秒→需转换) ==="
jq -r '.data[0] | [(.tradeDate/1000|strftime("%Y-%m-%d")), .pe, .pb, .totalMv] | @tsv' /tmp/indicator.json

echo "=== 近半年/1年涨跌 (%) ==="
jq -r '.data[0] | [.pctChg2q, .pctChg1y] | @tsv' /tmp/pct.json

echo "=== 近 5 日主力净流入（万元）==="
jq -r '.data[:5] | .[] | [.tradeDate, .mainNetInflow] | @tsv' /tmp/flow.json
```

> 流程要点：`kline/daily` 的 `tradeDate` 是 "YYYY-MM-DD" 字符串；`indicator` 的 `tradeDate` 是毫秒时间戳；`moneyflow` 的 `tradeDate` 是 YYYYMMDD 字符串（例外，不要 /1000|strftime）；`type=11` = 不复权日 K（12=周线 / 13=月线）。交付格式：一句话结论 + 区间涨跌 + 关键估值 + 主力净流入 + 异常点。

### WF-2 多标的横向对比

**可直接复制运行的 bash 模板（白酒三剑客示例）：**

```bash
NAMES=("茅台" "五粮液" "泸州老窖")   # ← 改这里，可加减标的

# Step 1: 并行 search 所有标的
for NAME in "${NAMES[@]}"; do
  curl -sf -X POST "${BASE}/openapi/v1/stock/basic/search" \
    -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
    -d "{\"nameOrCode\":\"${NAME}\"}" > /tmp/s_${NAME}.json &
done
wait

# Step 2: 汇总 tsCode JSON 数组
TS_LIST=$(for NAME in "${NAMES[@]}"; do
  jq -r '.data[0].tsCode // empty' /tmp/s_${NAME}.json
done | jq -R . | jq -sc .)
echo "tsCodes: $TS_LIST"

# Step 3: 批量取估值（单次 ≤50，一次搞定）
echo "=== 估值对比 (tsCode / name / PE / PB / ROE / 总市值元) ==="
curl -sf -X POST "${BASE}/openapi/v1/stock/indicator/last/by-codes" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCodes\":${TS_LIST}}" \
  | jq -r '.data[] | [.tsCode, .name, (.pe|tostring), (.pb|tostring), (.roe|tostring), (.totalMv|tostring)] | @tsv'

# Step 4: 并行取各标的涨跌幅（此端点不支持批量，必须循环）
echo "=== 涨跌幅对比 (tsCode / 近半年% / 1年%) ==="
for TS in $(echo "$TS_LIST" | jq -r '.[]'); do
  curl -sf -X POST "${BASE}/openapi/v1/stock/kline/percentage-change" \
    -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
    -d "{\"tsCode\":\"${TS}\"}" \
    | jq -r --arg ts "$TS" '.data[0] | [$ts, (.pctChg2q|tostring), (.pctChg1y|tostring)] | @tsv' &
done
wait
```

> 关键点：`indicator/last/by-codes` 支持 `tsCodes` 数组批量（≤50），一次搞定；`percentage-change` 不支持批量，需循环但可并行（`&` + `wait`）。

### WF-3 财务质量扫描（轻量）

**可直接复制运行的 bash 模板（茅台示例，替换 NAME 即可）：**

```bash
NAME="茅台"   # ← 改这里

# Step 1: 解析 tsCode
TS=$(curl -sf -X POST "${BASE}/openapi/v1/stock/basic/search" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"nameOrCode\":\"${NAME}\"}" | jq -r '.data[0].tsCode')
echo "tsCode = $TS"

# Step 2: 近 8 季核心财务 + 分红（并行）
curl -sf -X POST "${BASE}/openapi/v1/stock/financial/core" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"size\":8}" > /tmp/core.json &

curl -sf -X POST "${BASE}/openapi/v1/stock/financial/dividend" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\"}" > /tmp/div.json &

wait

# Step 3: 提取关键趋势指标（⚠️ core.endDate 是 YYYYMMDD 字符串，不是毫秒，直接用）
echo "=== 近 8 季（endDate / EPS / ROE / 净利率 / 净利同比%）==="
jq -r '.data[] | [.endDate, .eps, .roe,
  .netprofitMargin, .netprofitYoy] | @tsv' /tmp/core.json

echo "=== 分红（endDate / 现金分红/股 / 送转股数）==="
jq -r '.data[] | [.endDate, .cashDiv, .stkDiv] | @tsv' /tmp/div.json
# dividend 的 endDate 是 YYYYMMDD 字符串（非毫秒）
```

> 交付要点：判断改善/恶化趋势（ROE/净利率逐季变化）、区分累计 vs 单季（`reportType=1` 合并，无 `reportType` 时 core 含所有口径）、标注异常季度。

### WF-3.1 财务深度审计（stock.financial scope）

**可直接复制运行的 bash 模板：**

```bash
TS="600519.SH"    # ← 改成目标 tsCode（先 search 拿）
# reportType: 0=年报 1=一季报 2=半年报 3=三季报；传 1=季报，做趋势用

# Step 1: 四表并行拉
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/financial/income-statement" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"reportType\":1,\"size\":8}" > /tmp/fin_inc.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/financial/balance-sheet" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"reportType\":1,\"size\":8}" > /tmp/fin_bs.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/financial/cash-flow" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"reportType\":1,\"size\":8}" > /tmp/fin_cf.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/financial/indicator" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"size\":8}" > /tmp/fin_ind.json &
wait

echo "=== 利润表（nIncome=净利润；大写I，不是nincome）==="
jq -r '.data[] | [(.endDate/1000|strftime("%Y-%m-%d")), .revenue, .nIncome, .nIncomeAttrP] | @tsv' \
  /tmp/fin_inc.json

echo "=== 综合指标（ROE / 毛利率 / 现金比）==="
jq -r '.data[] | [(.endDate/1000|strftime("%Y-%m-%d")), .roe, .grossprofitMargin, .ocfToProfit] | @tsv' \
  /tmp/fin_ind.json

echo "=== 现金流（经营现金流 vs 净利润 交叉验证）==="
jq -r '.data[] | [(.endDate/1000|strftime("%Y-%m-%d")), .nCashflowAct, .freeCashflow] | @tsv' /tmp/fin_cf.json
# nCashflowAct=经营净额；freeCashflow=FCF；⚠️ 字段名不是 nCashFlowOper！

# Step 2 按需追加（勿滥用，只在特定分析时调）
# 分业务营收（日期是 YYYYMMDD 字符串，非毫秒）：
# curl ... /stock/financial/business-segment -d '{"tsCode":"'${TS}'","size":50}'
# 大股东质押风险（日期是 YYYYMMDD 字符串）：
# curl ... /stock/financial/pledge -d '{"tsCode":"'${TS}'","size":8}'
```

### WF-3.5 技术指标多维分析

**可直接复制运行的 bash 模板：**

```bash
TS="600519.SH"   # ← 目标 tsCode（先 search 拿）

# 四组指标并行拉取
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/indicator/ma-channel" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"adjType\":\"qfq\",\"size\":60}" > /tmp/ind_ma.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/indicator/oscillator" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"adjType\":\"qfq\",\"size\":60}" > /tmp/ind_osc.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/indicator/trend-volume" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"adjType\":\"qfq\",\"size\":60}" > /tmp/ind_tv.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/indicator/nine-turn" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"size\":20}" > /tmp/ind_nt.json &
wait

echo "=== MA/BOLL 通道（趋势位置）==="
jq -r '.data[] | [(.tradeDate/1000|strftime("%Y-%m-%d")), .ma5, .ma20, .ma60, .bollMid, .bollUpper, .bollLower] | @tsv' \
  /tmp/ind_ma.json
# ⚠️ ma-channel 无 close 字段（完整 28 字段：MA/EMA/BOLL/KTN/TAQ/BBI/EXPMA）；需收盘价请另调 kline/daily

echo "=== MACD / KDJ（动量/超买超卖）==="
jq -r '.data[] | [(.tradeDate/1000|strftime("%Y-%m-%d")), .macd, .macdDif, .macdDea, .kdjK, .kdjD, .kdjJ] | @tsv' \
  /tmp/ind_osc.json

echo "=== OBV / VR 量能 ==="
jq -r '.data[] | [(.tradeDate/1000|strftime("%Y-%m-%d")), .obv, .vr, .mtm] | @tsv' /tmp/ind_tv.json

echo "=== DeMark 九转（反转预警）==="
jq -r '.data[] | [(.tradeDate/1000|strftime("%Y-%m-%d")), .upCount, .downCount, .nineUpTurn, .nineDownTurn] | @tsv' /tmp/ind_nt.json

# ⚠ short-term 短线因子暂未上线，恒返 []，拿到空直接说明不要重试：
# curl ... /stock/indicator/short-term -d '{"tsCode":"'${TS}'","size":20}'
# 估值历史（按需追加）：
# curl ... /stock/indicator/valuation/history -d '{"tsCode":"'${TS}'","size":60}'
```

### WF-3.7 宏观背景扫描

**可直接复制运行的 bash 模板：**

```bash
# 全部并行拉取，节省等待时间
curl -sf --compressed -X POST "${BASE}/openapi/v1/market/macro/cpi" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"size":12}' > /tmp/macro_cpi.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/market/macro/ppi" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"size":12}' > /tmp/macro_ppi.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/market/macro/pmi" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"size":12}' > /tmp/macro_pmi.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/market/macro/money-supply" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"size":12}' > /tmp/macro_m2.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/market/macro/lpr" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"size":6}' > /tmp/macro_lpr.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/market/macro/gdp" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"size":6}' > /tmp/macro_gdp.json &

wait

echo "=== CPI 全国同比 ==="
jq -r '.data[] | [.month, .ntYoy, .ntMom] | @tsv' /tmp/macro_cpi.json
# month = YYYYMM 字符串；ntYoy=同比；ntMom=环比

echo "=== PPI 总体同比 ==="
jq -r '.data[] | [.month, .ppiYoy, .ppiMom] | @tsv' /tmp/macro_ppi.json

echo "=== 制造业 PMI ==="
jq -r '.data[] | [.month, .pmi010000] | @tsv' /tmp/macro_pmi.json
# 字段名是数字编码：pmi010000=综合；pmi010100=生产；pmi010200=新订单

echo "=== M2 同比 ==="
jq -r '.data[] | [.month, .m2, .m2Yoy] | @tsv' /tmp/macro_m2.json

echo "=== LPR ==="
jq -r '.data[] | [.date, .y1, .y5] | @tsv' /tmp/macro_lpr.json
# date = YYYYMMDD 字符串（⚠️ 不是 tradeDate！）；y1=1年期；y5=5年期（⚠️ 不是 lpr1y/lpr5y）

echo "=== GDP 季度同比 ==="
jq -r '.data[] | [.quarter, .gdp, .gdpYoy] | @tsv' /tmp/macro_gdp.json
# quarter = YYYYQX 字符串（如 "2026Q1"）
```

### WF-3.6 基金 / ETF 分析

**可直接复制运行的 bash 模板：**

```bash
KW="红利"        # ← 改成关键词（"沪深300"/"消费"/"科技"均可；命中 0 条就换近义词重试）
# 或直接设 ETF_CODE="510300.SH" 跳过搜索步骤

# Step 1: 搜索 ETF（关键词须是名称实际含的词）
ETF_LIST=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/fund/etf/list" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"nameKeyword\":\"${KW}\",\"size\":10}")
echo "=== ETF 列表 ==="
echo "$ETF_LIST" | jq -r '.data[] | [.tsCode, .cName, .indexCode, .mgtFee] | @tsv'
# cName=ETF简称（⚠️ 大写N，不是cname）；exchange过滤用"SH"/"SZ"（不是"SSE"/"SZSE"）

ETF_CODE=$(echo "$ETF_LIST" | jq -r '.data[0].tsCode')

# Step 2: 日 K + 复权因子 + 份额（并行）
curl -sf --compressed -X POST "${BASE}/openapi/v1/fund/etf/kline/daily" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${ETF_CODE}\",\"size\":60}" > /tmp/etf_kline.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/fund/etf/share-history" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${ETF_CODE}\",\"size\":20}" > /tmp/etf_share.json &
wait

echo "=== ETF 日 K ==="
jq -r '.data[] | [(.tradeDate/1000|strftime("%Y-%m-%d")), .close, .pctChg, .vol, .amount] | @tsv' \
  /tmp/etf_kline.json
# ⚠️ tradeDate 是毫秒时间戳；amount 单位是元（÷1e8=亿）；vol 单位是手

echo "=== 份额规模 ==="
jq -r '.data[] | [(.tradeDate/1000|strftime("%Y-%m-%d")), .totalShare, .totalSize, .nav] | @tsv' \
  /tmp/etf_share.json
# totalShare=份（÷1e8=亿份）；totalSize=元（÷1e8=亿元）；不是万份/万元

# Step 3: 重仓股 + 分红（并行）
curl -sf --compressed -X POST "${BASE}/openapi/v1/fund/portfolio" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${ETF_CODE}\"}" > /tmp/etf_portfolio.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/fund/dividend" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${ETF_CODE}\",\"size\":10}" > /tmp/etf_div.json &
wait

echo "=== 前十重仓股 ==="
jq -r '.data[] | [.symbol, .stkMkvRatio, .stkFloatRatio] | @tsv' /tmp/etf_portfolio.json

echo "=== 分红历史 ==="
jq -r '.data[] | [.exDate, .divCash, .divProc] | @tsv' /tmp/etf_div.json
# divProc="实施"/"预案"；impAnndate/earpayDate 字段全小写d/p（不是 impAnnDate/earPayDate）
```

### WF-3.8 可转债评估

**可直接复制运行的 bash 模板：**

```bash
STK="600000.SH"   # ← 正股代码（先 search 拿）

# Step 1: 查正股的转债（stkCode 字段，不是 tsCode）
CB_LIST=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/bond/cb/list" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"stkCode\":\"${STK}\"}")
echo "=== 可转债列表（空=该公司未发转债，不是故障）==="
echo "$CB_LIST" | jq -r '.data[] | [.tsCode, .bondShortName, .convPrice, .maturityDate, .couponRate, .issueRating] | @tsv'
# issueSize 单位是元（÷1e8=亿），所有日期是 YYYYMMDD 字符串

CB_CODE=$(echo "$CB_LIST" | jq -r '.data[0].tsCode // empty')
[ -z "$CB_CODE" ] && echo "无转债" && exit 0

# Step 2: 可获取数据（并行）—— 溢价率/强赎底表暂无数据如实告知
curl -sf --compressed -X POST "${BASE}/openapi/v1/bond/cb/share" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${CB_CODE}\",\"size\":10}" > /tmp/cb_share.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/bond/cb/price-chg" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${CB_CODE}\",\"size\":10}" > /tmp/cb_pchg.json &

curl -sf --compressed -X POST "${BASE}/openapi/v1/bond/cb/rate" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${CB_CODE}\"}" > /tmp/cb_rate.json &
wait

echo "=== 转股进度（publishDate/endDate 是 YYYY-MM-DD 带横杠）==="
jq -r '.data[] | [.publishDate, .accConvertRatio, .remainSize, .convertPrice] | @tsv' /tmp/cb_share.json
# accConvertRatio=累计转股比例%；remainSize=剩余规模元（÷1e8=亿）

echo "=== 转股价变动历史 ==="
jq -r '.data[] | [.changeDate, .convertpriceBef, .convertpriceAft] | @tsv' /tmp/cb_pchg.json
# ⚠️ convertpriceBef/convertpriceAft 全小写p，不是 convertPriceBef/convertPriceAft

echo "=== 利率阶梯 ==="
jq -r '.data[] | [.rateStartDate, .rateEndDate, .couponRate] | @tsv' /tmp/cb_rate.json

# ⚠️ 以下端点底表暂无数据（PG迁移缺口），调用恒返空，如实告知用户勿重试：
# /bond/cb/daily（溢价率/纯债价值）、/bond/cb/factor、/bond/cb/issue、/bond/cb/call
```

### WF-4 板块轮动分析

**可直接复制运行的 bash 模板：**

```bash
# Step 1: 全市场板块快照（⚠️ plate 快照端点忽略所有参数，直接传 {}）
SNAP=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/plate" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" -d "{}")
echo "=== 涨幅 Top 10 板块 ==="
echo "$SNAP" | jq -r '.data | sort_by(.pctChange) | reverse | .[:10][] |
  [.tsCode, .name, .pctChange, .leadingCode, .leadingName] | @tsv'
# ⚠️ 领涨股代码字段名是 leadingCode（不是 leadingTsCode！）

# 取 top 3 板块 tsCode
TOP3=$(echo "$SNAP" | jq -r '[.data | sort_by(.pctChange) | reverse | .[:3][].tsCode] | join(" ")')

# Step 2: 持续净流入板块（⚠️ 此端点字段叫 type，不是 contentType）
echo "=== 连续净流入 ≥5日的行业板块 ==="
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/plate/continue-net" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"continueNum":5,"type":"行业"}' \
  | jq -r '.data[:10][] | [.tsCode, .name, .continueNum, .totalNetInflow] | @tsv'

# Step 3: 取 plate/list 的最新 tradeDate 并转 YYYY-MM-DD（stocks-indicator 需要带横杠格式）
TRADE_DATE=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/plate/list" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"size":1}' | jq -r '.data[0].tradeDate | (./1000|strftime("%Y-%m-%d"))')

# Step 4: Top 3 板块成分股估值（⚠️ tradeDate 必须 YYYY-MM-DD 带横杠，传 YYYYMMDD 会 code=1）
for CODE in $TOP3; do
  echo "=== ${CODE} 成分股估值快照（月度数据）==="
  curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/plate/stocks-indicator" \
    -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
    -d "{\"code\":\"${CODE}\",\"tradeDate\":\"${TRADE_DATE}\"}" \
    | jq -r '.data[:20][] | [.tsCode, .name, .pctChg, .pe, .pb] | @tsv'
done

# Step 5: 板块资金流（⚠️ 此端点字段叫 contentType，不是 type；无 sell 分项）
echo "=== 行业板块资金流 Top 10 ==="
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/plate/cash-flow" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"contentType":"行业","page":1,"size":20}' \
  | jq -r '.data[:10][] | [.tsCode, .name, .buyElgAmount, .buyLgAmount, .netAmount] | @tsv'
# buyElgAmount=特大单买入万元；buyLgAmount=大单买入万元；netAmount=净流入万元
# ⚠️ buyEliteAmount/sellEliteAmount/netBuyElite 均不存在——该端点只有 buyElgAmount 等买方分项
```

### WF-5 龙虎榜解读

**可直接复制运行的 bash 模板：**

```bash
TS="600519.SH"   # ← 改成目标股票 tsCode（先 search 拿）；留空则只看全市场清单

# Step 1: 取最近龙虎榜日期（返回 YYYY-MM-DD 格式）
DATES=$(curl -sf -X POST "${BASE}/openapi/v1/stock/market/lhb/latest-dates" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" -d "{}")
D=$(echo "$DATES" | jq -r '.data[0]')     # "2026-06-04"，lhb/list 可直接回传
D8=$(echo "$D" | tr -d '-')               # "20260604"，lhb/details 需要 YYYYMMDD
echo "龙虎榜日: $D"

# Step 2: 当日上榜清单（全市场）
LIST=$(curl -sf -X POST "${BASE}/openapi/v1/stock/market/lhb/list" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tradeDate\":\"${D}\"}")
echo "=== 上榜清单 (tsCode / 名称 / 涨跌%) ==="
echo "$LIST" | jq -r '.data[] | [.tsCode, .name, .pctChange] | @tsv'

# Step 3: 目标股席位明细（tsCode 非空时）
[ -n "$TS" ] && {
DETAIL=$(curl -sf -X POST "${BASE}/openapi/v1/stock/market/lhb/details" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"tradeDate\":\"${D8}\"}")
echo "=== ${TS} 席位（席位名 / 方向 / 净买元 / 上榜原因）==="
echo "$DETAIL" | jq -r '.data[] | [.exalter, .side, .netBuy, .reason] | @tsv'
# side="B"=买方 / "S"=卖方（不是 0/1！）；tradeDate 响应是毫秒时间戳（≠字符串）
}

# Step 4 可选：资金流印证
[ -n "$TS" ] && curl -sf -X POST "${BASE}/openapi/v1/stock/market/moneyflow" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"size\":5}" \
  | jq -r '.data[] | [.tradeDate, .mainNetInflow] | @tsv'
```

> 关键点：`lhb/list` 响应仅 3 字段（tsCode/name/pctChange），席位详情在 `lhb/details`；`side` 是字符串 `"B"`/`"S"`，不是整数；`netBuy > 0` = 净买入。⚠️ 同 scope 的 `institution-trading`/`broker-trade` **side 是整数**（`1`=买方，`2`=卖方），与 `lhb/details` 的字符串相反——三者都在 stock.lhb scope，极易混淆。

### WF-6 选股模型 + 人工复核

> ⚠️ `stock.selection` 仅 **Ultra** 内部档；Max 及以下 token 调用返 `code=206`。先 whoami 确认再执行。  
> ⚠️ 2026-06-07 实测：ML/动量/价值结果表暂未生成数据（PG 迁移后模型管道未跑），即使 Ultra 也可能恒空——空就如实说明，改跑 WF-3.5 技术面替代。

**可直接复制运行的 bash 模板（ML 买入信号）：**

```bash
# Step 1: 确认 stock.selection scope 可用
curl -sf -X POST "${BASE}/openapi/v1/whoami" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" -d "{}" \
  | jq -r '.data.scopes[]?' | grep -q "stock.selection" \
  || { echo "❌ 无 stock.selection scope（Ultra 专属）"; exit 1; }

# Step 2: 取最近 3 个交易日（以应对当日模型未跑的情况）
DATES=$(curl -sf -X POST "${BASE}/openapi/v1/stock/market/lhb/latest-dates" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" -d "{}" \
  | jq -r '.data[]' | tr -d '-')   # YYYY-MM-DD → YYYYMMDD

# Step 3: 逐日尝试，拿到有数据的第一天
ML=""; D=""
for DAY in $DATES; do
  ML=$(curl -sf -X POST "${BASE}/openapi/v1/stock/selection/ml/results" \
    -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
    -d "{\"tradeDate\":\"${DAY}\",\"signalType\":\"BUY\",\"minScore\":0.6,\"size\":20}")
  COUNT=$(echo "$ML" | jq '.data | length')
  if [ "$COUNT" -gt 0 ]; then D=$DAY; break; fi
  echo "⚠️ ${DAY} 无结果（模型未跑），尝试前一日..."
done
[ -z "$D" ] && { echo "三个交易日均无选股结果，模型管道暂未运行"; exit 0; }

echo "=== ML BUY 信号 ${D} (tsCode / score / signalType) ==="
echo "$ML" | jq -r '.data[] | [.tsCode, (.score|tostring), .signalType] | @tsv'

# Step 4: 取 top 10 估值（批量一次）
TS_LIST=$(echo "$ML" | jq -c '[.data[:10][].tsCode]')
echo "=== 估值快照 (tsCode / pe / pb / roe) ==="
curl -sf -X POST "${BASE}/openapi/v1/stock/indicator/last/by-codes" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCodes\":${TS_LIST}}" \
  | jq -r '.data[] | [.tsCode, .name, (.pe|tostring), (.pb|tostring), (.roe|tostring)] | @tsv'
```

> 关键点：`tradeDate` 必传真实日期（SQL 精确等值匹配，不传 = 必空）；`lhb/latest-dates` 返回 3 个日期，逐日回退是标准做法。`signalType` 可选 `BUY`/`HOLD`/`WATCH`；`minScore` 阈值 0.6 可调。

### WF-7 股东反查

**可直接复制运行的 bash 模板（社保基金示例，替换 HOLDER 即可）：**

```bash
HOLDER="社保基金"          # ← 支持模糊简称；多个股东改成 JSON 数组: ["社保基金","中央汇金"]（⚠️ 多名=交集AND，非并集OR）
# 最近季末日：A 股报告期为 3/31、6/30、9/30、12/31，取最近已过的那个
QUARTER_END="20260331"    # ← 改成最近季末日（YYYYMMDD）

# Step 1: 查该股东持有哪些股票
FIND=$(curl -sf -X POST "${BASE}/openapi/v1/stock/shareholder/holder/find-stocks" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"holders\":[\"${HOLDER}\"],\"endDate\":\"${QUARTER_END}\"}")
echo "=== 持仓股票 ==="
echo "$FIND" | jq -r '.data[] | [.tsCode, .name, .holderName] | @tsv'

# Step 2: 批量取估值 (≤50 只一次)
TS_LIST=$(echo "$FIND" | jq -c '[.data[:50][].tsCode]')
echo "=== 估值快照 ==="
curl -sf -X POST "${BASE}/openapi/v1/stock/indicator/last/by-codes" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCodes\":${TS_LIST}}" \
  | jq -r '.data[] | [.tsCode, .name, (.pe|tostring), (.pb|tostring), (.roe|tostring)] | @tsv'

# Step 3: 查单股东最新持仓明细（需全称，从 find-stocks 响应 holderName 字段取）
HOLDER_FULL=$(echo "$FIND" | jq -r '.data[0].holderName')  # 取实际全称
curl -sf -X POST "${BASE}/openapi/v1/stock/shareholder/holder/holdings" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"holder\":\"${HOLDER_FULL}\",\"endDate\":\"${QUARTER_END}\"}" \
  | jq -r '.data[] | [.tsCode, .tsCodeName, (.holdAmount|tostring), (.holdRatio|tostring)] | @tsv'
# holdAmount/holdChange 是 JSON 字符串，parseFloat() 再做数值运算
```

> 关键点：`find-stocks` 的 `holders` 支持简称模糊匹配；`holdings` 的 `holder` **必须传全称**（从 `find-stocks` 响应取 `holderName`）；`endDate` 两端点均必填，缺一返 `code=2`；`holdAmount`/`holdChange` 是字符串需 `parseFloat()`。

### WF-8 综合研究简报

用户说 "帮我快速研究一下 XX"，依次跑（可并行发射前 3 步）：

```bash
NAME="贵州茅台"
TS=""  # 先 search 填充
TS=$(curl -sf -X POST "${BASE}/openapi/v1/stock/basic/search" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"nameOrCode\":\"${NAME}\"}" | jq -r '.data[0].tsCode')

# Step 1: 行情 + 估值（近 60 日，parallel &）
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/kline/daily" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"type\":11,\"size\":60}" > /tmp/kline.json &

# Step 2: 最新估值快照（peTtm/pb/roe/股息率）
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/indicator/last/by-codes" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCodes\":[\"${TS}\"]}" > /tmp/indicator.json &

# Step 3: 财务核心 + 分红（近 8 期）
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/financial/core" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"size\":8}" > /tmp/core.json &

wait  # 等前 3 步完成

# Step 4: 区间涨跌幅（多周期）
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/kline/percentage-change" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\"}" > /tmp/pct.json

# Step 5: 资金流（近 30 日）+ 龙虎榜最近上榜
LHB_DATE=$(curl -sf -X POST "${BASE}/openapi/v1/stock/market/lhb/latest-dates" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{}' | jq -r '.data[0]')
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/moneyflow" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"size\":30}" > /tmp/mf.json &
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/lhb/details" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TS}\",\"tradeDate\":\"$(echo $LHB_DATE | tr -d '-')\"}" > /tmp/lhb.json &
wait

# Step 6: 最新新闻（需 news scope；Pro 无此 scope 跳过）
curl -sf --compressed -X POST "${BASE}/openapi/v1/market/news/list" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"titleKeyword\":\"${NAME}\",\"size\":20}" > /tmp/news.json 2>/dev/null || echo '{"data":[]}' > /tmp/news.json

# Step 7 (可选): 市场情绪聚合——今日整体新闻情绪 / 多空舆情（需 market scope）
# tradeDate 传当日 YYYYMMDD；avgSentimentScore in [-1,1]，>0 偏多；newsSurgeRatio 量比
TODAY=$(date +%Y%m%d)
curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/market/news-sentiment" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tradeDate\":\"${TODAY}\"}" > /tmp/sentiment.json 2>/dev/null || echo '{"data":null}' > /tmp/sentiment.json
# 注：tradeDate 是 YYYYMMDD 字符串（不是毫秒时间戳）；data:null 表示当日尚未生成（非交易日/盘前）

# 综合解读: 行情趋势 → 估值位置 → 财务质量 → 资金信号 → 新闻事件 → 市场情绪 → 风险点
```

### WF-9 衍生品 / 期权（derivative scope，Max）

> ⚠️ 期权数据**真实存在且量极大**（`option_daily` 2000 万+ 行，覆盖 SSE/SZSE ETF + CFFEX 股指/国债 + SHFE/DCE/CZCE/INE/GFEX 商品/能源 共 8 所）。**绝不能凭印象说"没有"——先查**（见〔第一铁律〕）。

先分清两类问句，走不同路径：

**路径 A — 单合约日 K（已知或能定位到具体合约码 tsCode）**
用户："豆一 A2607-P-4600 这只期权 6 月初价格" / "50ETF 购 12 月 2.5 那张最近怎么走"

```
# （可选）先用 contracts 按交易所/标的/月份定位合约码
POST /openapi/v1/derivative/option/contracts
     body={"exchange":"DCE","size":100}      # 返回 tsCode/opName/callPut/exercisePrice/sMonthDate/maturityDate
     # 分页端点(默认 size=50):一个标的常有几百张合约,需全量就 page=1,2,3… 翻到不足 size 行为止;exchange 单数/exchanges 数组均可
POST /openapi/v1/derivative/option/kline/daily
     body={"tsCode":"A2607-P-4600.DCE","startDate":"20260601","endDate":"20260603"}
→ 字段：open/high/low/close/settle/preSettle/preClose/vol/amount/oi
```

**路径 B — 全市场按某交易日筛选 / 跨日比价排序（别逐合约调几万次）**
用户："找出 6/3 最低 ÷ 6/2 收盘 ≤ 50% 的期权" / "某日全市场期权放量榜"

```
# 用全市场端点按交易日整拉，分页 100/页，翻页直到不足 100 行
POST /openapi/v1/derivative/option/kline/daily-by-date
     body={"startDate":"20260602","exchange":"DCE","page":1,"size":100}
POST /openapi/v1/derivative/option/kline/daily-by-date
     body={"startDate":"20260603","exchange":"DCE","page":1,"size":100}
→ agent 侧按 tsCode 把两天 join，再算比值 / 排序 / 取 topN
```

**期权专属陷阱（必看，否则筛出一堆假信号）**：
- ⏱ `tradeDate` 返回是**毫秒时间戳 long**（如 `1780329600000`），**不是 `"20260602"` 字符串**。跨日 join 按毫秒比对或自行转换，别拿它当日期串去 equals。
- 🕳 **未成交的合约也有行**：`open/high/low/vol/amount` 全 = 0，但 `close/settle` 仍是结算价。做"暴跌/比价/放量"筛选前**必须先剔除 `low<=0` 或 `vol<=0` 的行**，否则把"当天没成交"误判成"跌到 0"（曾导致 1192 个假信号）。
- 🔤 `callPut` 字段是**定长空格补齐**的（`"C    "` / `"P    "`），按认购/认沽过滤要先 `trim` 或前缀匹配，**别用 `== "C"`**（会全部漏掉）。
- 📦 全市场单日动辄 2 万+ 行：能按 `exchange` 收窄就收窄；最终明细落 CSV，别把几万行塞进给用户的回复。
- 🕐 **期权分钟线（`option/kline/minutes`）是按需入库的**：合约 5000+ 不做全量同步，只有管理员手动回填过的合约有分钟数据（日 K 是全量的，不受此限）。空结果 ≠ 无行情 ≠ 接口故障——如实告诉用户"该合约分钟数据未回填，可联系管理员触发回填（OptionMinutesTask，分钟级生效）"，并主动提供日 K（`option/kline/daily`）作为替代。

### WF-10 港 / 美股研究（stock.hk / stock.us scope，Max+）

> 标的解析走〔Entity resolution rules〕港/美股路径（别用 A 股 search）

**港股（以腾讯 00700.HK 为例）**：

```bash
TICKER="00700.HK"

# Step 1: 日 K + 复权（⚠️ hk/kline-adj 无估值字段；peTtm/pbTtm 在 Step 2 的 fina-indicator）
KLINE=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/hk/kline-adj" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TICKER}\",\"size\":60}")
echo "$KLINE" | jq -r '
  .data[] | [
    (.tradeDate/1000|strftime("%Y-%m-%d")),
    .close, (.pctChange*100|round/100),
    .turnoverRatio, .totalMv
  ] | @csv'

# Step 2: 财务指标宽表（36 列，含 peTtm/pbTtm；多数问题到此为止）
FINA=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/hk/fina-indicator" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TICKER}\",\"size\":8}")
echo "$FINA" | jq -r '
  .data[] | [
    (.endDate/1000|strftime("%Y-%m-%d")),
    .reportType, .holderProfit, .holderProfitYoy,
    .roeAvg, .grossProfitRatio, .debtAssetRatio,
    .peTtm, .pbTtm
  ] | @csv'

# Step 3（仅需具体科目时）: 三大表 long format → 透视
INCOME=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/hk/income" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TICKER}\",\"size\":200}")
echo "$INCOME" | jq -r '.data[] | [(.endDate/1000|strftime("%Y-%m-%d")),.indName,(.indValue|tostring)] | @csv'
# 按 grep 筛关键指标行: grep "营业额\|毛利\|权益"
```

**美股（以 Apple 为例）**：

```bash
TICKER="AAPL"  # ⚠️ 裸 ticker，无 .O/.N 后缀（带后缀静默返空；BRK.A 例外保留点号）

# Step 1: 行情（us/kline 已含 pe/pb，无需额外估值端点）
KLINE=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/us/kline" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TICKER}\",\"size\":60}")
echo "$KLINE" | jq -r '
  .data[] | [
    (.tradeDate/1000|strftime("%Y-%m-%d")),
    .close, (.pctChange*100|round/100), .pe, .pb, .totalMv
  ] | @csv'

# Step 2: 财务指标宽表（29 列）
FINA=$(curl -sf --compressed -X POST "${BASE}/openapi/v1/stock/us/fina-indicator" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d "{\"tsCode\":\"${TICKER}\",\"size\":8}")
echo "$FINA" | jq -r '
  .data[] | [
    (.endDate/1000|strftime("%Y-%m-%d")),
    .reportType, .operateIncome, .parentHolderNetprofit,
    .parentHolderNetprofitYoy, .roeAvg, .grossProfitRatio
  ] | @csv'
```

**long format 透视（三大表必看——不透视你就是把几百行键值对直接糊给用户）**：

- 返回**每行一个键值对**：港股 `{tsCode, endDate, name, indName, indValue}`；美股多 `indType`（表内分组）和 `reportType`，透视键相应变成 `(endDate, indType, indName)`。
- ⏱ 港股/美股三大表的 `endDate` 均为**毫秒时间戳 integer**（实测：港股 hk/income `endDate=1767110400000`，美股 us/income `endDate=1774627200000`）。⚠️ 旧文档写"美股 endDate 是字符串 '2024-12-31 00:00:00'"——**已勘误，实为毫秒戳**，与港股格式相同。
- agent 侧透视：按 `endDate` 分组、`indName` 当列名。快速做法（jq 落 long CSV 后按报告期挑关键指标）：

```bash
# endDate 是毫秒时间戳整数，先 ÷1000 转秒再格式化
echo "$RESP" | jq -r '.data[] | [(.endDate/1000|strftime("%Y-%m-%d")), .indName, (.indValue|tostring)] | @csv' > income_long.csv
# 再按 endDate 分组挑指标行（grep "营业额\|毛利\|溢利"），或用 python/awk 透视成 报告期×指标 宽表
# 注意：jq 的 strftime 在非 Linux 系统可能需替换为 python 处理
```

- 📦 翻页注意：**一个报告期就有几十个 indName 行**，`size=100` 可能只覆盖 1~2 个报告期；要多期对比先翻页拉够，再透视。
- 偷懒正道：能用 `fina-indicator`（已是宽表）回答的就别碰三大表 long format。
- 港股 `fina-indicator` 的 `reportType` 过滤值是**带年份的完整报告期串**（`"2024年中报"`），传 `"中报"` 匹配不到返回空——拿不准就不传，回来自己筛。

***

## Data retrieval rules

### 共享请求模式

- **方法**：永远 POST（除 `/stock/market/volume-breakout` 是 GET）
- **Header**：`Authorization: Bearer ${TOKEN}` + `Content-Type: application/json`
- **Body**：纯业务参数 JSON。OpenAPI 表单不含 `userId` / `d` / `vn` / `appsFlyerId` 这类 app 字段——**别填**
- **响应**：`ApiResultModel<T>` = `{code, msg, data, traceId}`
- **大数据量拉取必带 gzip**：分钟 K / 期权 `daily-by-date` / 多页拉取这类大响应，curl 加 `--compressed`（即发 `Accept-Encoding: gzip`）——后端已开 JSON gzip 压缩，传输量直降 70-85%；不带也能用，只是慢

### 分页与分段拉取

- **每次最多 100 行**：所有 OpenAPI v1 端点单次请求 `size` 硬上限为 **100**。传 `size=500`、`size=1000` 都会被静默截断到 100，不会报错。要更多数据就翻页（`page=2/3/...`）。
- **默认 size = 50**（不传时）。多数场景默认值已够，特别小的查询可显式 `size=20`。
- 日 K 线：一次窗口 ≤ 2 年
- 分钟 K 线：一次 ≤ 1 个月
- 批量指标 `indicator/last/by-codes`：一次 tsCodes ≤ 50
- 超过阈值 → 分段 → 合并 → 去重

### 缓存（agent 视角）

- 同样 body 短时间内重复请求会命中后端缓存（30s ~ 24h 不等，按数据频率分级）。**对 agent 的影响**：可放心重试，不会引入额外费用，但**新鲜度上限就是缓存窗口**——分钟级数据 60 秒内可能拿到旧值。
- 用户问"实时""现在""最新报价"时，分钟 K 端点的 60 秒缓存可能略过期；告知用户即可，不必反复重试。
- `*/execute` 写动作端点和 `/whoami` 不走缓存。

### 重试策略

仅对网络/超时类瞬时错误重试一次；参数错误（400 / 422）或数据为空直接停手解释原因。**不要循环重试 5 次**。

### 输出规模控制

后端不会自动截断。如果一次拉到几千行，agent 自己要：
- 在输出给用户之前用 `head -200` 或类似手段限行
- 或者用更窄的筛选条件再请求一次
- 落 CSV 时不限制（CSV 不进 LLM context）

***

## Output contract

除非用户明确只要原始表：

1. **一句话结论**
2. **数据范围与口径**（取数时间窗、K 线类型、是否复权、板块是东财还是申万）
3. **关键指标 / 关键表格**
4. **异常点 / 风险 / 口径局限**
5. **如生成了 CSV / Parquet，给出文件路径**

中等以上数据表优先落盘成 CSV，命名示例：`daily_600519.SH_20240101_20241231.csv`。

### 交付前自检门（reflection gate — 回答发出前过一遍）

把答案发给用户**之前**，逐条自检；任何一条不过 → 先补救再交付：

1. **每个数字 / 结论都有出处吗？** —— 来自某次真实响应（能指出端点 + traceId），不是脑补 / 记忆 / 估算。否定结论尤其必须有 traceId（见〔第一铁律〕）。
2. **口径标了吗？** —— 时间窗、K 线类型、是否复权（bfq/hfq/qfq）、板块是东财还是申万、累计 vs 单季。含糊会误导用户。
3. **参数没踩坑吗？** —— 没把 snake_case / 占位符字面量（`<最新>`/`${...}`）/ 错误日期格式发出去——它们会静默返默认值，让你误以为"空"。
4. **部分失败如实说了吗？** —— 分段有失败别说"全部完成"；翻页截断要标"只取了前 N，按 X 排序"。
5. **结论先行了吗？** —— 一句话结论放最前，别让用户自己从表格里翻答案。

***

## Error handling

### 对用户层

- 401 / token 无效 → "OpenAPI token 已失效或被禁用，请联系管理员重新签发"
- 403 / scope 不足 → "当前 token 套餐不含 X scope。可调 /openapi/v1/whoami 查具体覆盖范围"
- 429 / 频率超限 → "请求过密，请等下一分钟重试，或升级套餐到更高频率档"
- 服务不可达（连不上）→ "OpenAPI 服务不可达，请检查 ${BASE} 是否在线"
- `code=1` / 系统异常 → **首先检查参数**（日期格式错 / 必填缺失 / 超范围）——99% 的 `code=1` 是入参问题，不是服务端故障；常见：`kline/daily` 同时传 startDate+endDate（已知 bug，改用 `size`）、`plate/stocks-indicator.tradeDate` 传 YYYYMMDD（须改 YYYY-MM-DD）
- `code=2` / 业务参数错误 → 必填字段缺失（如 `holder/find-stocks` / `holder/holdings` 缺 `endDate`，`financial/express` / `disclosure-date` 缺 `tsCode`）；检查端点必填参数后重试
- `code=16` / 上游数据源失败 → "后端上游数据源（Tushare）瞬时故障（限流/网络），等 1 分钟重试一次即可"——**不是"无数据"也不是服务端 bug**
- `code=206` / 套餐不支持 → 端点需要更高套餐（常见：`stock.selection` 需 Ultra；`tmt` 需 Ultra）——不是 scope 配置问题，是 token tier 不够
- `code=208` / 路径被禁 → "该端点已被 token 的路径黑名单拒绝访问（`allowed_paths` 配置）"——不是 scope 不足也不是 bug；联系管理员调 `/stock/user/admin/openapi/token/path/set` 开放此路径
- 数据为空 → 先分辨（非交易日 / 数据未入库 / 股票未上市 / 筛选过严 / 代码错误）

### 调试层（失败必须附）

- 调用的端点路径
- 请求 body
- 响应的 `code` / `msg` / `traceId`
- 失败分段（如做了分段拉取）

### 部分成功原则

分段拉取若有失败段，不要说"成功"。明确列出：哪些成功、哪些失败、是否给出部分结果。

***

## Best practices

- 先想 workflow，再想端点
- 能少取就少取（首轮用 top 5 / 近 20 日；用户深挖时再扩展）
- 标的解析永远第一步
- 先结论、再证据
- 板块结论务必注明口径（东财 vs 申万）
- ML 选股结果显示 `tradeDate` 和 `signalType`（不要让用户误以为是实时）
- 遇到 "导成 CSV"：取完数据用 jq → CSV 落盘并回报路径

***

## 完整闭环示例（agent 内部执行流）

**用户**："看下宁德时代最近怎么样"

```bash
# 1. 标的解析
curl -sf -X POST "${BASE}/openapi/v1/stock/basic/search" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"nameOrCode":"宁德时代"}'
# data[0].tsCode → "300750.SZ"

# 2. WF-1 四个端点并行（没有依赖关系）
curl ... POST /openapi/v1/stock/kline/daily          -d '{"tsCode":"300750.SZ","type":11,"size":20}'
curl ... POST /openapi/v1/stock/indicator/last/by-codes -d '{"tsCodes":["300750.SZ"]}'
curl ... POST /openapi/v1/stock/kline/percentage-change -d '{"tsCode":"300750.SZ"}'
curl ... POST /openapi/v1/stock/market/moneyflow      -d '{"tsCode":"300750.SZ","size":10}'

# 3. 整理给用户：
#    - 一句话：近 20 日 +X.XX%，相对沪深 300 跑赢/跑输 N 个百分点
#    - 估值：PE TTM = X.XX（行业中位数附近 / 偏高 / 偏低）
#    - 主力资金：近 10 日净流入 X.XX 亿
#    - 异常点：哪天放量 / 急跌 / 涨停
```

**用户**："ML 今天 BUY 列表"

```bash
# 1. selection 必传真实 tradeDate（SQL 精确等值，不传/传占位符=必空，见 §6）——先拿最近交易日
curl ... POST /openapi/v1/stock/market/lhb/latest-dates -d '{}'
# data[0] → "20260605"（示例值，以实际返回为准）

# 2. 用真实日期查（注意 camelCase 字段）
curl ... POST /openapi/v1/stock/selection/ml/results \
  -d '{"tradeDate":"20260605","signalType":"BUY","minScore":0.6,"size":20}'
# 空结果 → 把日期回退到前一交易日再试一次（模型当天可能未跑）
# 整理：tsCode + name + score + signal + 触发的因子（结论里标注 tradeDate，别让用户误以为是实时）
```

**用户**："社保基金一零一组合最新持仓"

```bash
# 不需要 search（用户给的是机构名不是股票名）
# ⚠️ endDate 事实必填（报告期下界，不传 = code=2 参数错误）；传最近季末日
curl ... POST /openapi/v1/stock/shareholder/holder/find-stocks \
  -d '{"holders":["社保基金一零一组合"],"endDate":"20260331"}'
# 拿到 tsCode 列表 → 进 WF-7 后续步骤
```

**用户**："豆粕期权 6/3 跌得最狠的几只"（⭐ 正反对照——这是本 skill 最该学会的一课）

```text
❌ 错误执行（真实事故，别再犯）：
   1. 调一次 whoami → 看到一堆 scope
   2. "印象里期权数据后端是空的" → 直接回 "抱歉，期权数据后端为空"
   → 致命：whoami 不是数据查询；scopes 里明明有 derivative；从没真调过端点（无 traceId）。违反〔第一铁律〕。

✅ 正确执行：
   1. whoami → scopes 含 derivative → 写进记忆卡："derivative ✓，有权限，必须真查"（见〔会话记忆 & 长任务行为〕）
   2. 意图=全市场按日筛选 → 走 WF-9 路径 B
   3. 真调（camelCase + YYYYMMDD）：
      POST /openapi/v1/derivative/option/kline/daily-by-date
           {"startDate":"20260603","exchange":"DCE","size":100}  # DCE=豆粕所在所，翻页拉全
   4. agent 侧：先剔 low<=0 / vol<=0 的没成交行（否则假暴跌），算 (close-preClose)/preClose 排序取最跌的
   5. 交付前自检门：数字有 traceId 出处✓ 口径标了(6/3收盘 vs 前结算、已剔未成交)✓ 没踩 snake_case/占位符✓ 结论先行✓
   6. 交付："6/3 豆粕期权跌幅前 5：① X 合约 -NN%…（口径：DCE 期权日 K，已剔当日未成交合约，traceId=…）"
```

> 记牢这条对照：**whoami 通过 ≠ 查过数据；有 scope = 必须真查；任何"没有"都要有 traceId 背书。**

***

## Decision tree — 用户口语 → workflow

agent **自己**判断走哪个 workflow，**不要把决策反问给用户**。下表覆盖 ~95% 的中文口语触发：

| 用户语气词 | 立刻走 |
|-----------|--------|
| "看下…走势" / "最近…怎么样" / "这周表现" | WF-1（单标的快照） |
| "对比 / 比较 / vs" + 多只名字 | WF-2（横向对比） |
| "财务 / 报表 / 利润 / 现金流 / 资产" | WF-3（轻量）或 WF-3.1（深度，明确说"详细 / 完整 / 三大表"时） |
| "MACD / KDJ / RSI / 均线 / 布林" | WF-3.5（技术指标） |
| "宏观 / CPI / PMI / 通胀 / 货币" | WF-3.7 |
| "ETF / 基金" | WF-3.6 |
| "可转债 / 转债 / 强赎" | WF-3.8 |
| "期权 / 50ETF 期权 / 股指期权 / 商品期权 / 期货" | WF-9（衍生品；**全市场期权筛选用 `option/kline/daily-by-date`，先查再下结论**） |
| "板块 / 行业" + "最强 / 轮动" | WF-4 |
| "龙虎榜 / 主力席位 / 游资 / 机构买" | WF-5 |
| "ML 选 / 模型选 / 今天选了哪些 / BUY 列表" | WF-6 |
| "社保 / 汇金 / 林园 / 葛卫东 持了啥" | WF-7 |
| "全面研究 / 简报 / 帮我研究" | WF-8 |
| "港股 / 腾讯港股 / 恒生 / 港股财报" | WF-10（stock.hk；标的解析走〔Entity resolution rules〕港股路径） |
| "美股 / 纳斯达克 / 苹果 / 特斯拉财报" | WF-10（stock.us；tsCode 是**裸 ticker**无后缀，如 `AAPL`/`TSLA`，先 basic 确认；唯有股份类别如 `BRK.A` 本身含点） |
| "研报 / 券商评级 / 目标价 / 一致预期 / 金股" | §6.9（stock.research） |
| "国债收益率曲线 / 中债收益率 / 国债期限利差" | `bond/yc`（Max；`tradeDate` 或 `startDate`/`endDate` **必传**否则全库返空；`curveType` 是字符串 `"0"` 到期/"1" 即期；`curveTerm` 是年数浮点；单日请求返 50 期限点；⚠️ 国内利率曲线，不要走 WF-3.7 宏观 / §6.10 美债） |
| "GC001 / 逆回购利率 / 银行间回购" | `bond/repo/daily`（Max；传 `tsCode="204001.SH"` 即 GC001；⚠️ `amount` 单位是**千元**不是万元；`weightR` 是加权平均利率%） |
| "美债 / 收益率倒挂 / 期限利差 / HIBOR / LIBOR" | §6.10（stock.intl-macro，Max；国内 CPI/LPR 走 WF-3.7 别混） |
| "外汇 / 汇率 / 美元兑人民币 / EURUSD" | §6.11（forex） |
| "票房 / 电影 / 电视剧备案 / 台股营收" | §6.12（tmt，Ultra 内部） |
| "突然放量 / 异动" | `GET /openapi/v1/stock/market/volume-breakout` |
| "连续涨停 / 几连板（筛选哪些票连涨了 N 天）" | `POST /openapi/v1/stock/kline/limit-up`（含 `tadeDays`、`limitUpNum`；`kline/limits` 是涨跌停**价格**表，别混；⚠️ 与 `limit-step`「当日连板天梯」不同） |
| "连板天梯 / 今天 3 连板有哪些票" | `POST /openapi/v1/stock/market/limit-step`（`tradeDate` YYYYMMDD；响应 `tradeDate` 是毫秒时间戳；`nums` 是连板数字符串；⚠️ 与 `kline/limit-up` 不同：`limit-step` 是**当日**横截面，`limit-up` 是**跨日**选股） |
| "被 ST 了 / 新增 ST / ST 原因" | `stock/market/st-daily`（当日 ST 列表）或 `stock/market/st-warning`（原因详情，需传 `tsCode`） |
| "游资今天买什么 / 游资交易明细" | `stock/market/hm-detail`（先 `hm-list` 拿名字，再 `hm-detail` 传 `tradeDate` 查当日明细） |
| "同花顺行业指数 / THS 指数涨跌" | `stock/market/ths-index` 拿代码 → `stock/market/ths-daily`（⚠️ `700xxx.TI` 代码系，与 `885xxx.TI` 概念板块不同） |
| "通达信板块 / 近期涨跌" | `stock/market/tdx-index` 拿列表 → `stock/market/tdx-daily` 查行情 → `stock/market/tdx-member` 查成分 |
| "中信行业指数涨跌 / CI 板块行情 / 中信成分" | `stock/market/ci-daily`（日行情）/ `stock/market/ci-index-member`（成分，无 tradeDate，三级分类体系） |
| "沪深 300 成分权重 / 指数权重占比" | `stock/index/weight` |
| "沪深 300 / 上证 50 历史 PE/PB / 指数估值" | `stock/index/dailybasic` |
| "大宗交易 / 某股 折价成交 / 机构一手买了多少" | `stock/market/block-trade`（`tsCode` 必填；`vol` 单位**万股**，`amount` 单位**万元**） |
| "今天市场情绪 / 新闻量 / 多空舆情" | `stock/market/news-sentiment`（`tradeDate` YYYYMMDD；响应 `avgSentimentScore`（-1~1）/ `newsSurgeRatio`（量比）） |
| "本周有哪些经济数据 / 财经日历 / 重要事件日程" | `market/macro/eco-cal`（请求 `startDate`/`endDate` YYYYMMDD；响应 `date` 是**毫秒时间戳**；按 `currency="CNY"` 筛中国；⚠️ `country` 是事件分类代码不是国名） |
| "北向 / 南向 / 陆股通 / 沪深港通今天买了什么" | `stock/market/hsgt-top10`（`tradeDate` YYYYMMDD 必填，先用 `lhb/latest-dates` 取最近交易日；`dataType` 1=沪股通/2=深股通/3=港股通；⚠️ 响应 `marketType` 与 `dataType` 枚举**不对称**）或 `stock/market/hsgt-moneyflow`（北/南向资金净流入整体） |
| "筹码 / 获利盘 / 套牢盘 / 筹码分布" | `stock/market/cyq-chips`（`tsCode` 必填；响应 `tradeDate` 是毫秒时间戳；每行一个价格档位）或 `stock/market/cyq-perf`（胜率快照；`tradeDate` 是 YYYYMMDD 字符串，属 stock.market 内例外） |
| "集合竞价 / 开盘竞价 / 尾盘竞价" | `stock/market/auction-open`（开盘集合竞价）或 `stock/market/auction-close`（尾盘竞价；⚠️ 15:00 前调用一律返空，非端点故障） |
| "热榜 / 同花顺热股 / 哪些股热度高" | `stock/market/ths-hot`（`dataType` 传中文标签，如 `"A股热股"`；响应 `tradeDate` 是毫秒时间戳；`rankTime` 是 `"YYYY-MM-DD HH:mm:ss"` 字符串，可直接用于展示，⚠️ 不要对 `rankTime` 做 ÷1000 转换） |

如果一条用户消息同时命中多个意图（比如 "茅台财务 + 走势 + 估值"），按 WF-1 → WF-3 → 估值快照的顺序串行跑，最后给一份合并报告。

## 不要做的事

> **快速定位（100+ 条）：** ⏰ 日期格式 → 搜`毫秒/ms/横杠/YYYYMMDD/÷1000` | 🔤 字段名拼写 → 搜`静默返 undefined/字段名换成` | ⚖️ 单位换算 → 搜`单位/万元/千元/亿元/万股` | 🔢 枚举取值 → 搜`枚举/方向/status/type/side` | 🔕 暂无数据 → 搜`暂无数据/PG迁移/暂未上线/止于` | 📋 数据结构 → 搜`JSON.parse/嵌套/data:null` | 🧠 业务语义 → 搜`交集/下界/scope/精确等值`

- ❌ **反问用户**"你想看什么 / 这是什么任务"——agent 自己根据 decision tree 判断
- ❌ **凭记忆拼 ts_code**（"茅台是 600519" 自己脑补）——必须先 `POST /openapi/v1/stock/basic/search` body `{"nameOrCode":"茅台"}`（字段是 `nameOrCode` 不是 `keyword`）
- ❌ **填 snake_case 字段**（`trade_date` / `signal_type` / `adj_type`）——后端用 camelCase，snake_case 直接被忽略 → 拿到默认值/空数据
- ❌ **传 size > 100**——会被静默截断到 100，要更多数据请翻页
- ❌ **把 token 明文 echo / 写文件**——只在内存中持有
- ❌ **失败循环重试 5 次**——网络瞬时错最多重试 1 次，参数错或 401/403 直接告诉用户原因
- ❌ **拿空 data 就说"接口坏了"**——先核对参数是否正确（snake_case？字段名拼错？）、是否非交易日、scope 是否覆盖
- 🔴 ❌ **没真调接口就说"没有 / 后端是空的"**——这是头号红线（见〔第一铁律〕）。whoami 成功 ≠ 查过数据；scope 里有就必须真打一次对应端点，拿到 traceId 才能下否定结论
- ❌ **sw-industry-quo / index-minute 不传 tsCode**——两个端点 tsCode 必填，缺省不是全市场而是静默返空
- ❌ **把占位符当真值发出去**——body 里别真的出现 `<最新>` `<today>` `<tsCode>` `<D>` `${...}` 这种字面量；日期自己算成 `YYYYMMDD`，tsCode 先 `search`，否则后端当未传 → 看似"空"
- ❌ **把 callPut/期权未成交行当真信号**——`callPut` 定长空格补齐要 trim；筛选前先剔 `low<=0 / vol<=0`（见 WF-9）
- ❌ **把响应里的毫秒时间戳当日期字符串处理**——indicator/financial/index/research/fund-ETF 等端点响应日期是 long 整数（如 `1780588800000`），直接 `== "20260605"` 或按字符串排序会全都对不上；需 ÷1000 转 UNIX 秒再格式化展示（或直接用端点同时返回的可读字段如 `rankTime`/`newsTimeStr`）
- ❌ **用 `.tradeDate` 取 `indicator/roe` 的日期**——`indicator/roe` 响应**没有** `tradeDate` 字段，日期在 `.endDate`（毫秒时间戳）；另有 `.period`（季度标签如 `"Q1"`/`"Q2"`）；用 `.tradeDate` 一直返回 undefined
- ❌ **把 `hm-list.orgs` 当普通字符串处理**——`/stock/market/hm-list` 响应的 `orgs` 是 **JSON 字符串数组**（格式 `"[\"中信证券...营业部\"]"`），需 `JSON.parse(orgs)` 才能迭代；注意区别：`hm-detail.hmOrgs`（另一端点）是**平文本字符串**（不需要 parse）——同游资体系两个字段序列化方式不同
- ❌ **把 `ths-hot.concept` 当普通字符串处理**——同花顺热榜响应的 `concept` 字段同样是 **JSON 字符串数组**（如 `"[\"人形机器人\",\"AI眼镜\"]"`），需 `JSON.parse(concept)` 才能提取概念标签；与 `hm-list.orgs` 同一类型
- ❌ **在 `financial/income-statement` 用 `nincome`/`nincomeAttrP` 取净利润**——A股财报三大表响应字段全部 camelCase：净利润是 **`nIncome`**（大写 I，不是 `nincome`）；归母净利润是 **`nIncomeAttrP`**（大写 I 和 P，不是 `nincomeAttrP`）；同一规律适用于 `financial/express`（业绩快报）的同名字段
- ❌ **按请求 `dataType` 解读 `hsgt-top10` 响应的 `marketType`**——两者枚举值**不对称**：请求 `dataType` 1=沪股通/2=深股通/3=港股通；响应 `marketType` 1=沪股通/**3**=深股通/**2**=港股通(沪)/**4**=港股通(深)——`dataType=2`(深股通) 返回的是 `marketType=3`，直接 `if marketType==2` 会拿到错误结果；另 `amount` 单位是**元**（不是万元，`amount=3351828340` ≈ 33.5 亿元）
- ❌ **把 kline/daily 响应的 "2026-06-05"（带横杠）直接当其他端点输入的 startDate/endDate**——其他端点输入统一是 YYYYMMDD（无横杠 = `20260605`）；A股日K响应 `tradeDate` 带横杠只是自己显示用，不是通用输入格式
- ❌ **向 `kline/daily` 同时传 `startDate` + `endDate`**——已知 PG 迁移 bug：两个日期参数同时传会 `code:1 系统异常`；用 **`size`**（最多 100）控制返回条数，需要超过 100 条时配合 `page` 翻页；单传 `startDate`（无 endDate）或只传 `size` 均正常
- ❌ **以为 `kline/adj-factor`（A股复权因子）的 `tradeDate` 是毫秒时间戳**——A股 `kline/adj-factor` 的 `tradeDate` 是 **YYYYMMDD 紧凑字符串**（如 `"20260605"`），与 `hk/adj-factor`/`us/adj-factor`（毫秒时间戳）完全不同；混淆后按毫秒处理会得到无意义数字
- ❌ **直接对 `kline/limits.preClose` 做数值运算**——该字段可能为 `null` / `"None"` 字符串（新股/停牌无前收盘价）；直接 `parseFloat(preClose)` 或数值比较会 NaN/报错；使用前 `if (preClose != null && preClose !== "None")` 守护
- ❌ **把 `kline/limit-up` 的 `data:null` 当 `data:[]` 处理**——两者语义不同：`data:null`（code 仍为 0）表示**请求参数错误**（两个必填整数字段缺失或 ≤0）；`data:[]` 才是"参数正确但当日无符合条件个股"；看到 null 先检查自己的参数（如 `limitUpNum` 和 **`tadeDays`** 都必须 >0）；⚠️ **`tadeDays` 是 API 已知历史拼写**（少一个 `r`，不是 `tradeDays`）——写 `tradeDays` 静默被忽略等同于未传，是导致 `data:null` 的常见原因
- ❌ **调 `plate/stocks-indicator` 时传 `tradeDate:"20260430"`（YYYYMMDD）**——该端点输入必须 `YYYY-MM-DD`（带横杠），传紧凑格式会 code=1 系统异常；数据月更，从 `plate/list` 取真实 tradeDate 后转格式传入
- ❌ **调 `hk/tradecal`/`us/tradecal` 时用 `.tradeDate` 取日期**——这两个端点响应日期字段名是 `calDate`（不是 `tradeDate`），前一交易日是 `pretradeDate`，都是毫秒时间戳
- ❌ **以为 `stock.market` 已被拆成 4 个子 scope**——生产 whoami 返回的仍是 `stock.market`，`stock.plate`/`stock.lhb`/`stock.moneyflow`/`stock.sentiment` 这 4 个名字不存在于 whoami 结果，判断 scope 时只看 `stock.market`
- ❌ **混用 `hk/kline` 和 `hk/kline-adj` 的涨跌幅字段名**——`hk/kline` 响应是 `pctChg`；`hk/kline-adj` 响应是 `pctChange`（带 e）；两个端点字段名不同，混用会永远拿到 undefined
- ❌ **期货 `settle` 端点的对冲保证金率字段写小写 h**——正确是 `bHedgingMarginRate`/`sHedgingMarginRate`（大写 H），旧文档误写 `bhedgingMarginRate`/`shedgingMarginRate`（全小写），写错静默返 null
- ❌ **用 `tsCode` 查 `futures/holding` 和 `futures/wsr`**——这两个端点请求参数是 **`symbol`**（品种代码，如 `"CU"` / `"RB"`），不是 `tsCode`（合约码，如 `"CU2607.SHF"`）；传 `tsCode` 字段静默被忽略，后端按默认值查全品种；须改用 `symbol` 字段
- ❌ **把 `bond/repo/daily.amount` 按万元处理**——国债逆回购 `amount` 字段单位是**千元**（不是万元！），展示成交额时 `amount ÷ 1e8 = 亿元`（即 `÷ 100,000`，而非 `÷ 10,000`）；`num` 字段是成交笔数（整数），不是金额
- ❌ **以为 `bond/yc.curveType` 是整数**——国债收益率曲线端点响应的 `curveType` 是**字符串**（`"0"` = 到期收益率 / `"1"` = 即期收益率），不是整数；过滤时 `curveType == 0` 永远为假，必须 `curveType === "0"` 或 `curveType == "0"`
- ❌ **把 `option/contracts` 的 `sMonthDate` 当 YYYYMM 格式**——该字段是 **"yyyy-MM" 带横杠字符串**（如 `"2026-06"`），不是紧凑 YYYYMM；`maturityDate`/`listDate` 也全是 **"YYYY-MM-DD" 带横杠字符串**，不要按 YYYYMMDD 格式处理
- ❌ **向 `stock/index/kline/weekly` / `monthly` 传 `tradeDate` 请求参数**——指数周线/月线端点请求中**不要传 `tradeDate`**，只传 `startDate`/`endDate`（YYYYMMDD）；⚠️ 原因：周线/月线锚点日（每周一/每月第一个交易日）与日 K 精确日期不对齐，传 `tradeDate` 做精确等值匹配会返空；股票个股周月线也有同问题但方向相反（`type=12/13` 用 `size` 控制，无 `tradeDate` 入参）
- ❌ **用 `index/kline/weekly`/`monthly` 响应的 `chg` 字段取涨跌幅绝对值**——指数周/月线的涨跌幅绝对值字段名是 **`change`**（不是 `chg`！）；日 K 端点是 `chg`，周/月 K 换成了 `change`；写 `chg` 静默返 undefined；另 `pctChg` 字段语义不变但命名一致，两端点都叫 `pctChg`
- ❌ **把 `index/kline/weekly` / `monthly` 的 `pctChg` 当百分比处理**——这两个端点的 `pctChg` 是**小数形式**（0.0113 = 1.13%，需 × 100 才是百分比），与 `index/kline/daily` 的 `pctChg`（已是百分比形式，0.2339 = 0.2339%）**语义完全不同**；混用会给出 100 倍偏差的涨跌幅
- ❌ **查美股估值时用 `us/kline-adj` 以为里面有 pe/pb**——`us/kline-adj` 只有复权价格，**没有** `pe`/`pb`/`ps`/`pcf` 字段；美股估值字段（pe/pb/psTtm）只存在于 `us/kline`（非复权版本），查估值要用 `us/kline` 而非 `-adj`
- ❌ **把 `us/basic` 的 `name` 字段当公司名显示**——大量美股的 `name` 字段值是字符串 `"None"`（不是 null，是字面 `"None"`）；实际英文公司名在 `enname` 字段，展示公司名用 `enname`
- ❌ **用 `delistDate == null` 判断美股是否仍上市**——`us/basic` 的 `delistDate` 对于在市股票是字符串 `"None"`（不是 null！），判断是否退市要用 `delistDate != "None"` 或检查 `listStatus` 字段
- ❌ **向 `stock/index/global` 端点要全球指数数据**——该端点 2026-06-08 实测 `data:[]`，底表暂无数据；如用户问全球主要指数表现，主动告知该功能暂不可用，不要反复重试
- ❌ **调 `stock/index/sw-heatmap` 拿申万行业热力图**——该端点 2026-06-08 实测返回**空列表**（PG 数据迁移缺口）；直接说明"申万行业热力图数据暂未迁移"，改用 `stock/index/sw-industry-quo` 按行业代码拉日行情替代
- ❌ **调 `stock/indicator/short-term` 拿短线 19 因子**——该端点 2026-06-07 实测底表全空，任何票任何日期都返 `data:[]`；**短线因子模块暂未上线**；不要换票换日期重试，直接告知用户"短线因子暂不可用"
- ❌ **调 `bond/cb/factor` 拿转债技术因子**——该端点 2026-06-08 实测 `data:[]`，底表暂无数据（PG 迁移缺口）；直接说明"转债技术因子数据未迁移"，不要重试
- ❌ **用 `stock/kline/weekly-monthly` 查远期历史**——该端点底表增量积累，2026-06-08 前仅有近几周的数据；查 1 年以上历史周线/月线请改用 `stock/kline/daily`（`type=12` 周线 / `type=13` 月线）
- ❌ **对 `fund/etf/kline/daily` 的 `amount` 按千元处理**——该端点 `amount` 单位是**元**（A 股日 K 是千元）；`vol` 单位是手（两者相同）；展示 ETF 成交额时 `amount ÷ 1e8 = 亿元`，而非 `÷ 1e7`
- ❌ **对 `fund/etf/share-history` 的 `totalShare`/`totalSize` 当万份/万元处理**——`totalShare` 是**份**，`totalSize` 是**元**，没有做万换算；计算规模时 `÷ 1e8 = 亿元`
- ❌ **对 `fund/portfolio` 用 `tsCode` 字段取持仓个股代码**——该端点响应中 **`tsCode` = 基金代码**（如 `"110011.OF"`），**持仓股票代码在 `symbol` 字段**（如 `"300750.SZ"`）；跨调 `indicator/last/by-codes` 或 `kline/daily` 获取持仓股行情时，传 `symbol` 值，不要传 `tsCode`；两字段并存于同一行，混用会用基金代码查股票 K 线→永远返空
- ❌ **对 `fund/portfolio`（基金持仓）的 `mkv` 和 `amount` 用错单位**——`mkv`（持仓市值）单位是**元**（不是万元/千元！）；`amount`（持仓量）单位是**股**（不是手/万股！）；展示市值时 `mkv ÷ 1e8 = 亿元`；展示持仓量时 `amount ÷ 100 = 手`
- ❌ **向 `holder/holdings` 传 `holderName` 字段**——该端点的请求参数字段名是 **`holder`**（不是 `holderName`！），且要求传**完整全称**（如 `"全国社会保障基金理事会"`）；`holderName` 是响应字段名，不是请求字段名；传 `holderName` 静默被忽略 → 无数据；全称从 `find-stocks` 响应的 `holderName` 字段取（`find-stocks` 输入接受简称模糊匹配）
- ❌ **对 `holder/holdings` 的 `holdAmount`/`holdChange` 直接做数值运算**——这两个字段是 JSON **字符串**，做加减前须 `parseFloat()`，否则得到字符串拼接结果
- ❌ **用 `fund/manager/list` 的 `endDate == null` 判断基金经理是否在任**——在任经理 `endDate` 是**空字符串 `""`**（不是 null），判断在任条件是 `endDate.trim() === ""` 或 `!endDate`
- ❌ **把 `fund/list`（公募基金列表）的日期字段当毫秒时间戳处理**——`fund/list` 的 `foundDate`/`issueDate`/`purcStartdate`/`redmStartdate` 等日期字段均是 **YYYYMMDD 字符串**（不是毫秒时间戳），与 `fund/etf/kline/daily`（ms）/ `fund/etf/share-history`（ms）等 ETF 相关端点完全不同；场外基金 `listDate` 通常为 null 也不是 ms
- ❌ **取 PMI 值时用 `pmiManufacturing`/`pmiService` 等语义字段名**——`market/macro/pmi` 的响应字段是**数字编码**（如 `pmi010000`=制造业综合 / `pmi010100`=生产 / `pmi010200`=新订单 / `pmi020100`=大型企业 / `pmi030000`=非制造业综合，共 30+ 字段）；用任何语义英文名（`pmi`/`manufacturing`/`general`）取值一律返回 undefined；详细字段映射见 api-quick-reference §十七
- ❌ **取 LPR 值时用 `lpr1y`/`lpr5y` 字段名**——`market/macro/lpr` 响应字段是 `y1`（1年期 LPR）/ `y5`（5年期 LPR），响应日期字段是 `date`（YYYYMMDD 字符串，不是 `tradeDate`）
- ❌ **取 Shibor/LPR 响应里的 `tradeDate`**——`macro/shibor` 和 `macro/lpr` 响应的日期字段名是 `date`（YYYYMMDD 字符串），不是 `tradeDate`；用 `.tradeDate` 会一直拿到 undefined
- ❌ **把 `bond/cb/list` 的 `issueSize` 当亿元**——`issueSize` 单位是**元**（如 `6000000000.0` = 60亿），展示时 `÷ 1e8` 得亿元；直接展示原数字会误导用户
- ❌ **写 `convertpriceBef`/`convertpriceAft` 时用大写 P**——`bond/cb/price-chg` 响应中这两个字段全小写 `p`（`convertpriceBef`/`convertpriceAft`），与同端点的 `convertPriceInitial`（大写 P）命名不一致；大写写法静默返 undefined
- ❌ **因旗舰股研报返空就说"没有研报数据"**——`research/report` 和 `research/report-rc` 库内仅约 170 只股票有记录；茅台（600519.SH）/ 五粮液（000858.SZ）等旗舰标的实测无数据是采集覆盖不足，不是端点坏了；不传 `tsCode` 可验证端点是否正常（会返回全库记录）
- ❌ **用小写 `ocode`/`ncode` 取 `bse-mapping` 字段**——`stock/basic/bse-mapping` 响应字段是大写 C：`oCode`（旧代码）/ `nCode`（新代码），写小写 `ocode`/`ncode` 静默返 undefined
- ❌ **用 `eco-cal` 的 `country` 字段过滤国家**——`market/macro/eco-cal` 响应 `country` 字段不是国名/国码（如 "CN"/"US"），而是**事件分类代码**（如 `"economic_activity"`/`"inflation"`）；按国家过滤应用 `currency` 字段（如 `currency="CNY"` 筛中国事件，`currency="USD"` 筛美国事件）；⚠️ 另：响应 `date` 字段是**毫秒时间戳**（不是 YYYYMMDD 字符串）、`time` 字段是 `"HH:mm"` 字符串（不是时间戳）——与国内宏观端点的 `date`=YYYYMMDD 格式不同
- ❌ **用 `derivative/futures/weekly-detail` 查近期期货周报**——该端点历史数据**止于 2020-04**，不含 2020-04 之后数据；如实告知用户，不要重试
- ❌ **用 `derivative/futures/kline/weekly-monthly` 查历史周线 / 月线时得到空结果就认为无数据**——该端点底表是**增量积累**，库内覆盖历史有限（同 `stock/kline/weekly-monthly`）；历史周 / 月线应改用 `derivative/futures/kline/daily`（`freq=W`/`M` 参数不支持，用 daily 按周/月降频自行聚合）；⚠️ 请求时 `tsCode`（期货合约码，如 `"CU2607.SHF"`）和 `freq`（`"W"` 或 `"M"`）**均必填**，漏任一个静默返空
- ❌ **写 `futures/weekly-detail` 的成交额同比字段为 `amountYoy`**——该端点响应字段名是 **`amoutYoy`**（API 已知拼写错误，`amout` 少一个 m），写 `amountYoy` 静默返 undefined；另 `amount` 字段单位是**亿元**（不是元/万元）
- ❌ **把 `kpl-concept-cons` 的 `conCode` 当题材代码**——该端点 `tsCode` = 题材代码（如 `"885589.TI"`），`conCode` = **个股代码**（如 `"300750.SZ"`）；两字段语义相反，混用会按题材代码筛股票导致全空；另 `description` 是题材描述文字（原 Tushare `desc` 保留字改名），不是 `desc`
- ❌ **用 `delistDate == null` 判断港股是否仍上市**——`hk/basic` 的 `delistDate` 对于**在市股票是字符串 `"None"`**（不是 null！），退市股票才是毫秒时间戳字符串（如 `"1087315200000"`）；判断是否退市要用 `delistDate != "None"` 或检查 `listStatus` 字段；与 `us/basic` 同一 `"None"` 模式；⚠️ 另：`hk/basic.listDate` 是**毫秒时间戳字符串**（如 `"1087315200000"`），不是数值，需 `Number(listDate)/1000|strftime` 转换才可读
- ❌ **取 `intl-macro` 系列端点响应日期时用 `.tradeDate`**——`/openapi/v1/intl-macro/us-tycr`、`us-trycr`、`us-tbr`、`us-tltr`、`us-trltr`、`hibor`、`libor`、`gz-index`、`wz-index` 这 9 个端点日期字段名均是 **`date`**（**毫秒时间戳 long**），不是 `tradeDate`；用 `.tradeDate` 一直返回 undefined；⚠️ 与国内宏观（`macro/shibor`/`macro/lpr` 的 `date` 是 YYYYMMDD 字符串）格式不同——`intl-macro` 的 `date` 是毫秒，需 `÷1000|strftime` 转换
- ❌ **向 `hk/fina-indicator` 传 `reportType="中报"` 或 `"年报"`（不带年份）**——港股财务指标 `reportType` 过滤值必须是**带年份的完整报告期串**（如 `"2024年中报"` / `"2023年年报"`）；传 `"中报"` / `"年报"` 精确匹配不到，返回 `data:[]`；⚠️ 港股**只有年报 / 中报**，没有季报——传 `"2024年一季报"` 永远空；不确定报告期就不传 `reportType`，按时间范围拉返回后再自行筛
- ❌ **把 `market/macro/policy-npr` 的 `pubtime` 当毫秒时间戳处理**——`pubtime` 是 **`"YYYY-MM-DD HH:mm:ss"` 带横杠带冒号字符串**（如 `"2026-06-10 09:00:00"`），不是毫秒时间戳；`÷1000` 或 `strftime` 处理会报错；直接 `pubtime.slice(0, 10)` 截取日期部分即可
- ❌ **把 `fund/share/history` 的 `tradeDate` 当毫秒时间戳处理**——非 ETF 公募基金份额历史的 `tradeDate` 是 **YYYYMMDD 字符串**（如 `"20260430"`），不是毫秒时间戳；与 `fund/etf/share-history.tradeDate`（毫秒时间戳）格式不同；`÷1000` 或 `strftime` 处理会得到无意义结果
- ❌ **把 `market/block-trade.vol` 当"手"处理**——A股大宗交易端点的 `vol` 单位是**万股**（不是手！），`amount` 是**万元**；与 A 股日 K（vol=手/amount=千元）和 ETF 日 K（vol=手/amount=元）均不同；大宗交易量 `vol=1000` 代表 1000 万股，不是 1000 手
- ❌ **把 `limit-analysis.firstTime`/`lastTime` 或 `kpl-list.luTime`/`ldTime`/`openTime`/`lastTime` 当 "HH:MM:SS" 字符串处理**——这两个端点的盘中时间字段都是 **"HHMMSS" 无分隔符字符串**（如 `"93643"` = 9:36:43，`"130000"` = 13:00:00）；⚠️ 早盘时间只有 5 位（9 开头），切记补全：`h=s[0:1]/s[0:2], m=s[-4:-2], sec=s[-2:]`；直接按 `":"` split 或 `"HH:MM:SS"` 格式化会出错
- ❌ **把 `market/news-sentiment.tradeDate` 当毫秒时间戳处理**——新闻情绪聚合端点的 `tradeDate` 是 **YYYYMMDD 字符串**（如 `"20260610"`），不是毫秒时间戳；与大多数情绪类端点（`limit-cpt-list`/`limit-step`/`cyq-chips` 等 tradeDate=ms）不同；`÷1000` 处理会得到无意义结果
- ❌ **调 `market/news/types` 以为能拿到 `news/list.type` 整数值字典**——`news/types` 返回的是**来源（source）字典**（字段 `code`/`displayName`/`description`），`code` 对应 `news/list` 响应的 `src` 字段（如 `"sina"` / `"cls"` / `"eastmoney"`）；**不是** `news/list.type`（整数字段，实测多数记录此字段为 null）的说明字典；`type` 整数过滤适用场景极少，不确定时省略
- ❌ **把 `market/news/list.title` 当稳定非空字段**——部分新闻条目的 `title` 字段为 null；展示时优先使用 `newsTimeStr`（可读字符串如 `"2026-06-07 22:12:08"`）代替 `newsTime`（毫秒时间戳），并对 `title` 做 null 守护
- ❌ **把 `fund/nav/history.netAsset`/`totalNetasset` 当真实净资产使用**——这两个字段因 Tushare 数据不连续更新，实测**多数记录值为 0**，不可靠；净资产数据应从财务指标 `/stock/financial/indicator` 取 `totalAsset`/`totalHldrEqy`，`fund/nav/history` 本身只适合取单位净值 `unitNav`/`accumNav`/`adjNav`
- ❌ **把 `us/basic` 响应的 `tsCode`（含交易所后缀，如 `"AAPL.O"`）直接传给 `us/kline` 等端点**——`us/basic` 响应字段 `tsCode` 是 `"AAPL.O"` / `"TSLA.O"` 这样带 `.O`/`.N` 后缀的格式，但 `us/kline`/`kline-adj`/`adj-factor`/财报三大表等其他端点需要**裸 ticker 无后缀**（如 `"AAPL"` / `"TSLA"`）；带后缀查询静默返空；使用时剥离点号后部分即可
- ❌ **按 A 股 vol/amount 单位解读港股 `hk/kline` 数据**——`hk/kline` 的 `vol` 单位是**股**（shares，不是万手），`amount` 是**港元**（不是千元）；比较港股和 A 股成交量/成交额时要注意量纲不同；ETF/大蓝筹 vol 数字会比 A 股看起来大很多
- ❌ **对 `limit-step.nums` 和 `limit-cpt-list.rank` 直接排序 / 大小比较**——两个字段都是**字符串类型**（如 `"5"` / `"3"`），字符串比较 `"10" < "5"` 为真（按首字符）；排序或判断"几连板以上"时必须先 `parseInt(nums, 10)` / `Number(rank)` 转整数，否则 5 连板排在 10 连板后面
- ❌ **向 `us/fina-indicator` 传 `"Q1"` / `"A"` 这样的短形式 `reportType`**——美股财务指标 `reportType` 过滤要求**东财口径完整报告期串**（如 `"2025/Q1"` / `"2023/FY"`；`FY`=年报，`Q1`-`Q4`=季度累计）；只传 `"Q1"` 或 `"A"` 匹配不到，静默返空；不确定就不传
- ❌ **向 `fund/etf/list` 传 `exchange:"SSE"` 或 `"SZSE"`**——ETF 列表端点 `exchange` 过滤只认**短形式**（`"SH"` / `"SZ"` / `"BSE"`），传 `"SSE"`/`"SZSE"` 被忽略静默返 0 条；另 ETF 中文简称字段名是 `cName`（大写 N），不是 `cname`
- ❌ **用 `fund/etf/list` 的 `status="L"` 查存续 ETF**——`fund/etf/list` 的 `status` 枚举与 `fund/list` **完全相反**：`fund/etf/list` 中 `"D"` = 存续（active）/ `"L"` = 已上市 / `"S"` = 已终止；而 `fund/list` 中 `"L"` = 存续 / `"D"` = 退市；用 `status="L"` 过滤 ETF 列表只会拿到"已上市"状态记录，不是"存续"；筛取存续 ETF 应传 `status="D"`
- ❌ **用 `fund/dividend.impAnndate` 和 `.earpayDate` 的驼峰大写拼法**——`fund/dividend` 端点这两个字段命名**不规则**：分红实施公告日是 `impAnndate`（小写 `d`，不是 `impAnnDate`）；收益支付日是 `earpayDate`（小写 `p`，不是 `earPayDate`）；其余字段均为标准驼峰；写大写 `D`/`P` 静默返 undefined
- ❌ **按 YYYYMMDD 解析 `bond/cb/share` 的日期字段**——转股进度端点 `publishDate` / `endDate` 是 **`"YYYY-MM-DD"` 带横杠字符串**（不是 YYYYMMDD）；另 `accConvertRatio`/`remainSize` 等字段是 camelCase（旧文档写的 `acc_convert_ratio`/`remain_size` 是 snake_case 错误写法）
- ❌ **把 `index/main/history` 的 `data` 当扁平数组迭代**——该端点响应 `data` 是 **嵌套数组**（数组的数组，每个元素是一只指数的历史 K 线序列），不是扁平列表；`data[0]` 是第一只指数的所有历史记录（数组），不是第一条数据；正确用法：`data.flat()` 展平或 `data.forEach(series => series.forEach(bar => ...))`
- ❌ **用多名股东调 `find-stocks` 以为是并集（OR）**——`find-stocks` 的 `holders` 数组是**交集（AND）逻辑**：`["社保基金","中央汇金"]` 返回两者**共同持有**的股票，不是任一个持有；要查某一个股东的票，传单元素数组 `["社保基金"]`；传多名 = 找共同持仓
- ❌ **以为 `holder/holdings.holder` 多名是交集（AND）——实为并集（OR）**——`holder/holdings` 的 `holder` 字段支持**逗号分隔多名**（如 `"全国社会保障基金理事会,中央汇金投资有限责任公司"`），语义是**并集（OR）**：返回任意一个股东持有的记录；⚠️ 与 `find-stocks.holders` 数组的**交集（AND）**逻辑相反：两个看似相似的"多股东查询"，`find-stocks` 取交集，`holder/holdings` 取并集——混淆后返回数据量远超预期
- ❌ **把 `find-stocks`/`holdings` 的 `endDate` 理解为"截止到某日"**——`endDate` 是报告期**下界**（后端条件 `end_date >= endDate`）：传 `"20260331"` = 返回报告期 ≥ 2026-03-31 的记录（最近季度及之后），而非"只看 2026Q1"；要拿最新持仓传最近已过季末日，要拿多期历史传更早日期（如 `"20250101"` 返 1 年内所有季报）
- ❌ **按毫秒或 YYYYMMDD 解析 `holder/holdings` 的 `annDate`/`endDate`**——这两个日期字段是 **`"YYYY-MM-DD"` 带横杠字符串**（如 `"2026-03-31"`），既不是毫秒时间戳也不是 YYYYMMDD；跨端点按日期对比时需转换格式
- ❌ **把 `financial/forecast.netProfitMin`/`netProfitMax` 当元处理**——业绩预告净利润预测值两个字段单位是**万元**（不是元！）；展示时需提示"万元"或 `÷10000` 转亿元，不要直接当元展示给用户
- ❌ **写 `financial/indicator` 单季字段为全小写**——单季财务指标字段是 camelCase 且**首字母大写**：`qEps`（单季 EPS）/ `qRoe`（单季 ROE）/ `qNetprofitMargin`（单季净利率）等，写 `qeps`/`qroe`/`qnetprofitmargin` 全小写静默返 undefined；**仅单季 q-系列字段**有此规律，`dtEps`/`netProfitMargin` 等常规字段仍是常规驼峰
- ❌ **对 `plate.buySmAmountStock` 做数值运算**——板块资金流向端点的小单买入股票数 `buySmAmountStock` 是 **String 类型**（无数据时返回 `"-"`，不是 null/0）；直接做 `> 0`/`parseFloat` 等运算会出错；先判 `!== "-"` 再转数字
- ❌ **向 `plates-by-stock` 传 `tsCode` 字段查个股所属板块**——该端点入参字段名是 **`conCode`**（成分股代码，如 `"000001.SZ"`），不是 `tsCode`；响应字段名也是 `plateCode`/`plateName`，不是 `tsCode`/`name`；另 `plate/list` 端点返回的板块代码字段才叫 `tsCode`（如 `"885001.TI"`），两端点字段语义不同勿混用
- ❌ **向 `plate/continue-net` 传 `contentType`/`page`/`size` 参数，或把 `type` 值写成单字母缩写**——该端点实际只接受 **`continueNum`**（连续净买入天数 int，必填）+ **`type`**（板块类型：`"行业"` / `"概念"` / `"地域"` 三者之一，**必须是中文全称**，不能写 `"I"`/`"C"`/`"A"` 等缩写，写了静默返空）；旧文档或 AI 生成代码常附带 `contentType`/`page`/`size` 等字段——这些字段会被忽略，但如果同时漏传 `continueNum`/`type` 会返回空或报参数错误
- ❌ **向 `plate/stocks-indicator` 传 `tsCode` 字段**——该端点入参字段名是 **`code`**（取自 `plate/list` 端点的 `tsCode` 字段值，如 `"885001.TI"`）；⚠️ 注意：`plate/list` 返回的板块代码**字段名叫 `tsCode`**，但 `plate/stocks-indicator` 接收它时**字段名换成了 `code`**；传 `tsCode` 不识别，静默返空
- ❌ **向 `derivative/option/contracts` 的 `dates` 参数传 YYYYMMDD 格式**——`dates` 是到期**月份**数组，格式必须是 **`YYYYMM`**（6位，如 `["202606"]`），传 8 位 YYYYMMDD（如 `["20260620"]`）或带横杠（`["2026-06"]`）均无法匹配，静默返空；⚠️ 与其他端点的 `startDate`/`endDate` 用 YYYYMMDD 不同
- ❌ **把 `stock/kline/weekly-monthly` 和 `stock/kline/week-month-adj` 的 `endDate` 当字符串处理**——这两个专用周/月线端点的响应字段中，`tradeDate`（周一/月初日期）**和 `endDate`（周期末日期，周五/月末）均是毫秒时间戳**（不是 YYYYMMDD 字符串）；`endDate` 名字像字符串其实是 ms，需同样 `÷1000|strftime` 转换
- ❌ **用 `stock/market/tdx-daily.totalMv` 取通达信板块总市值**——该端点的总市值字段名是 **`abTotalMv`**（A+B 股合计总市值，不是 `totalMv`！）；`totalMv` 字段不存在，写了静默返 undefined；另 `tdx-index` 端点里 `totalMv` 字段名就是 `totalMv`，两端点字段名不同勿混淆
- ❌ **对 `stock/kline/index-minute` 的响应用 `freq` 或 `preClose` 字段**——指数历史分钟 K 线端点响应**没有** `freq` 字段（旧文档有误）也**没有** `preClose` 字段；完整字段只有 8 个：`tsCode`/`tradeTime`(ms)/`open`/`high`/`low`/`close`/`vol`(手)/`amount`(千元)；按 `freq` 过滤或取 `preClose` 计算涨跌幅会静默失败
- ❌ **向 `stock/kline/percentage-change` 传 `tsCodes` 数组**——该端点请求参数字段名是 **`tsCode`（单数字符串）**，不支持批量数组；旧文档/AI 生成代码常写 `tsCodes`（复数）导致字段被忽略、返回全市场排序结果；多只标的要循环调用并行（`&`+`wait`）；与 `indicator/last/by-codes`（接受 `tsCodes` 数组批量）形成对比
- ❌ **调 `stock/kline/graph-type` 不传 `lineType`**——`lineType` 是**必填**参数（K 线周期：`11`=日 / `12`=周 / `13`=月，只认这 3 个值）；不传或传错会返回 `data:null`（code 仍 0）；⚠️ `type`（形态枚举）当前只实现了 `4`（W 双底），其余 1/2/3 传了静默返 `[]` 不报错，用户问其他形态时主动说明"该形态识别暂未上线"
- ❌ **对 `market/moneyflow` / `moneyflow-dc` 的 `tradeDate` 做 `÷1000|strftime` 转换**——这两个端点的 `tradeDate` 是 **YYYYMMDD 字符串**（如 `"20260610"`），不是毫秒时间戳；直接 `.tradeDate` 取用即可；`÷1000` 会使 jq 把字符串当整数相除（得到如 `20260` 的无意义数字）；⚠️ 同 scope 内大多数端点（`limit-step`/`cyq-chips`/`ths-daily` 等）`tradeDate` 是 ms，`moneyflow` 是例外——这是 stock.market scope 内的特例
- ❌ **把 `institution-trading` / `broker-trade` 的 `side` 字段当字符串处理**——这两个龙虎榜衍生端点的 `side` 是**整数**（`1`=买方机构/买方营业部，`2`=卖方机构/卖方营业部），而 `lhb/details` 的 `side` 是**字符串**（`"B"`=买方，`"S"`=卖方）；三个端点都在 stock.lhb scope，极易混淆；用 `side === "B"` 或 `side === "S"` 过滤 institution-trading/broker-trade 结果永远为空
- ❌ **用 `tradeDate` 过滤或取 `ci-index-member` 的时间维度**——中信行业指数成分端点**响应中无 `tradeDate` 字段**；时间维度只有 `inDate`（纳入日期，ms 时间戳）和 `outDate`（剔除日期，ms 时间戳，**当前成员 `outDate` 为 null**）；用 `tradeDate` 过滤请求或取响应均静默失败；判断是否为当前成员要用 `outDate === null`（或 `isNew === "Y"`）
- ❌ **混淆 `shareholder/hsgt-list` 的 `type` 北向/南向方向**——四个 `type` 值语义固定：`"HK_SH"`=**北向**（外资经港交所买**上证** A 股）/`"HK_SZ"`=**北向**（外资经港交所买**深证** A 股）/`"SH_HK"`=**南向**（内地投资者经**沪**股通买港股）/`"SZ_HK"`=**南向**（内地投资者经**深**股通买港股）；"北向=外资进来买 A 股"/"南向=内资出去买港股"；`HK_` 开头=北向，`_HK` 结尾=南向
- ❌ **盘中（15:00 前）调 `stock/market/auction-close` 期望拿到当日尾盘竞价数据**——收盘集合竞价（14:57~15:00）结束后数据才写入，**当日 15:00 前调用一律返回 `data:[]`**；不是端点出错，也不是 tsCode 有问题；若用户在 15:00 前问"今天尾盘竞价"，告知数据尚未就绪而非说"无数据"；历史某日尾盘竞价不受此限制（传 `tradeDate` 过去日期正常返回）
- ❌ **把 `derivative/sge/kline/daily` 的 `vol`/`oi` 按"手"处理，或按期货/股票口径解读单位**——上金所日 K 线端点的 `vol`（成交量）和 `oi`（持仓量）单位是**千克**（kg，不是手/张/万股！）；`amount`（成交额）单位是**元**；`priceAvg` 是加权均价，单位是**元/克**（不是元/千克）；展示"成交量 5000" = 5000 千克 = 5 吨黄金，不是 5000 手；另 `tsCode` 格式含括号（`"Au(T+D)"`/`"Ag(T+D)"`），传这类名称时带双引号 shell 转义；`settleDire` 是**递延补偿方向**（`"B"` = 多头补偿/`"S"` = 空头补偿），不是买卖方向
- ❌ **直接使用 api-quick-reference 文档记录的 `mainForceNetInflow` 字段名而不验证**——`stock/market/moneyflow`（个股资金流）的主力净流入字段，api-quick-reference 记为 `mainForceNetInflow`，而 WF 模板（WF-1/WF-4/WF-8）使用的是 `mainNetInflow`；若该字段返回 null，先 `jq '.data[0] | keys'` 确认实际字段名再取值；⚠️ 同端点的其他字段（`buyLgAmount`/`sellLgAmount`/`buyElgAmount`/`sellElgAmount`）名称无歧义，受影响的仅此聚合字段
- ❌ **把 `derivative/option/kline/daily-by-date` 中 `vol=0`/`amount=0` 的行当"当日无成交"或"行情异常"处理**——该端点对**未成交期权合约**仍会输出行（`open`/`high`/`low`/`vol`/`amount` 均为 0），但 `close`/`settle` 字段含有**结算价**；"全零"不代表合约不存在或行情崩溃，只是当日零成交；与大多数时序端点（无成交 = 无行）行为不同；筛选真正有交易的合约用 `vol > 0`，展示合约存续状态时 `close/settle != 0` 比 `vol > 0` 更可靠
- ❌ **从 `stock/market/bak-daily` 取涨跌幅用 `pctChg`，或取换手率用 `turnoverRate`**——`bak-daily` 响应字段与同为 A 股行情的 `kline/daily`/`indicator/last` **命名不一致**：涨跌幅是 **`pctChange`**（不是 `pctChg`！）；换手率是 **`turnOver`**（不是 `turnoverRate`！）；`pctChg`/`turnoverRate` 在 `bak-daily` 响应中不存在，静默返 undefined；⚠️ 同样用 `pctChange` 命名的端点还有 `plate`快照/`ths-daily`/`us/kline` 等，说明 `pctChange` 是另一套命名体系，不是 `bak-daily` 特有错误
- ❌ **向 `stock/hk/minute` 传 `startDate`/`endDate`（YYYYMMDD）作为时间范围**——港股分钟 K 的时间参数字段名是 **`startTime`/`endTime`**（不是 `startDate`/`endDate`！），格式是 **`"YYYY-MM-DD HH:mm:ss"`**（带横杠、冒号、空格，如 `"2026-06-10 09:30:00"`）；传 `startDate`/`endDate` 静默被忽略（端点只按 `tsCode` 查最近数据）；传对字段名但用 `"20260610"` 紧凑格式也无法解析——两个错误叠加才能拿到正确数据；⚠️ 与 A 股分钟 K（`stock/kline/minute`）形成对比：A 股用 `startDate`/`endDate` + `YYYYMMDDHHmm` / `YYYYMMDD` 格式，两套端点字段名和格式完全不同
- ❌ **对 `stock/index/kline/minutes`（免费指数分钟K）的 `vol` 直接做数值运算**——该端点 `vol` 字段**可为 null**（某些指数分钟无成交量数据）；直接 `vol * price` 或 `vol > 0` 判断涨停会 NaN/抛错；⚠️ 同时：该端点响应**日期字段名是 `tradeTime`（毫秒时间戳），不是 `tradeDate`**——与 `stock/kline/index-minute`（Plus 档付费版）同，两端点均用 `tradeTime`；另：无 `preClose`/`chg`/`pctChg` 字段，计算涨跌幅需自行用前一行 `close` 差值
- ❌ **用 `st-warning.stType != null` 判断 ST 风险类型是否存在**——`stType` 可为**空字符串 `""` 而非 null**；`stType != null` 判断会让空字符串通过，展示"风险类型：（空）"给用户；应用 `stType && stType.trim()` 或显式 `stType !== "" && stType != null` 双重守护；⚠️ 同类陷阱：`fund/manager/list.endDate`（在任时也是空字符串 `""` 而非 null，详见独立 entry）——**遇到"空/缺失"类语义字段，先查文档，不要统一假设"空 = null"**
- ❌ **把 `financial/dividend.stkBoRate` 当"每10股送股数"（送股比）读取**——`stkBoRate` 字段语义是**每股转增**（资本公积转增股本，如 `0.3` = 每股转增 0.3 股）；**送股**（利润分配送股）字段是 `stkDiv`，不是 `stkBoRate`；名字里 "Bo" 来自 bonus（红股/转增），不是 "送股比例"；同样容易混淆的是 `stkCoRate`（每股**配股**，即配售新股数量），不是"转增比"——三个字段含义：`stkDiv`=送股 / `stkBoRate`=转增 / `stkCoRate`=配股；⚠️ 另：这三个字段值是**每股绝对数量**（不是每10股，不是百分比）；`cashDiv`=税前每股现金分红（元），`cashDivTax`=税后
- ❌ **把 `plate/stocks-indicator` 响应的 `tradeDate` 当字符串处理**——该端点**输入** `tradeDate` 参数是 `"YYYY-MM-DD"` 带横杠字符串（如 `"2026-04-30"`），但**响应**中的 `tradeDate` 字段是**毫秒时间戳 long**（如 `1746028800000`）；入参和出参格式完全不同——正确传入后读取响应仍需 `÷1000|strftime` 转换；⚠️ 两个陷阱组合极易踩：① 入参传 YYYYMMDD → code=1；② 入参格式对了，但按字符串读响应 `tradeDate` → 得到毫秒数字乱码
- ❌ **向独立 `hk/adj-factor` / `us/adj-factor` 端点用 `adjFactor` 字段名取复权因子**——这两个**独立**复权因子端点的字段名是 **`cumAdjfactor`**（不是 `adjFactor`！）；混淆来源：`hk/kline-adj` 和 `us/kline-adj` 行内嵌的复权因子字段叫 `adjFactor`（与 A 股命名相同），但切换到**独立 `hk/adj-factor` / `us/adj-factor` 端点**时字段名变为 `cumAdjfactor`——同一 HK/US 域内两类端点命名不一致；⚠️ 另：HFQ 计算公式是 `HFQ = BFQ × cumAdjfactor / 当日最新 cumAdjfactor`（需两日因子之比），不是直接乘
- ❌ **用 `nCashFlowOper` 取 `financial/cash-flow` 经营现金流**——`financial/cash-flow` 端点的经营活动现金净额字段名是 **`nCashflowAct`**（不是 `nCashFlowOper`！）；`nCashFlowOper` 在该端点不存在；投资净额是 `nCashflowInvAct`（注意小写f），筹资净额是 `nCashFlowsFncAct`（注意大写F）——三个净额字段驼峰大小写不统一，逐字核对才安全；⚠️ FCF 字段名是 `freeCashflow`（小写 c）
- ❌ **认为 `plate/continue-net` 响应的连续净流入合计字段名是 `amount`（按 api-quick-reference 文档直接使用）而不验证**——api-quick-reference 将该字段记为 `amount`（连续净流入合计），但 WF-4 模板实际使用的是 `totalNetInflow`；若该字段返回 null，先 `jq '.data[0] | keys'` 确认实际字段名再取值；⚠️ 同端点还有 `avgAmount`（文档名）/ 可能对应 `avgNetInflow`（实际名）的日均净流入字段，同样建议 `keys()` 验证
- ❌ **向 `tmt/twincome` 或 `tmt/twincome-detail` 传 `YYYYMMDD` 格式的 `startDate`/`endDate`**——这两个台湾电子月营收端点的 `startDate`/`endDate` 过滤字段格式是 **`YYYYMM`**（6位，如 `"202604"`），不是 `YYYYMMDD`（8位）；传 8 位格式会按 VARCHAR 字符串比较，一般得到空数据；⚠️ 这是 tmt 系列端点唯一与其他端点不同日期格式的地方（`bo-daily`/`bo-weekly`/`bo-monthly`/`bo-cinema`/`film-record` 均用标准 `YYYYMMDD`），容易被"tmt 都一样"的惯性带坑
- ❌ **向 `hk/kline-adj` 取 `peTtm`/`pbTtm` 估值字段**——`hk/kline-adj` 响应完整字段 18 个，**不含任何 pe/pb 估值字段**（只有 OHLCV + vwap + adjFactor + turnoverRatio + 市值 + 股本）；港股 `peTtm`/`pbTtm` 在 **`hk/fina-indicator`**（财务指标宽表，按报告期频率），不在日 K 端点；用 `hk/kline-adj` 取到的永远是 null；⚠️ 与 `us/kline-adj`（同样无 pe/pb，见 "查美股估值" ❌ entry）同一陷阱；注意：`us/kline`（美股非复权 K 线）**有** pe/pb，但港股没有对应的含估值日 K 端点——港股日频估值只能走 `hk/fina-indicator`
- ❌ **向 `plate` 快照端点用 `.leadingTsCode` 取领涨股代码**——`plate` 快照（全市场板块涨跌幅快照，`POST /openapi/v1/stock/market/plate`）响应字段中领涨股代码字段名是 **`leadingCode`**（不是 `leadingTsCode`！）；`leadingTsCode` 不存在，取到永远是 null；同端点还有 `leadingName`（领涨股名称）/ `leadingPct`（领涨股涨幅%），字段名无歧义；⚠️ 注意 `plate/list`（板块详情时间序列）**不含** `leadingCode`/`leadingName`/`leadingPct` 字段，这三个字段仅在 `plate` 快照（25字段版本）存在
- ❌ **向 `plate/cash-flow` 取 `buyEliteAmount`/`sellEliteAmount`/`netBuyElite` 字段**——`plate/cash-flow`（板块资金榜）响应完整 19 个字段中**不存在**这三个字段名；正确的字段名是 `buyElgAmount`（特大单买入，万元）/ `buyLgAmount`（大单买入，万元）/ `netAmount`（板块净流入合计，万元）；⚠️ 该端点只有买方分项（buyElgAmount / buyLgAmount / buyMdAmount / buySmAmount），**没有独立的卖方分项字段**（净流入用 `netAmount`）；`buyEliteAmount` 这类命名来自其他第三方 API 或 AI 臆造，yyqdata 不支持
- ❌ **从 `stock/indicator/ma-channel` 响应取 `.close` 收盘价**——`ma-channel` 端点完整字段共 28 个（tsCode/tradeDate + MA/EMA/BOLL/KTN/TAQ/BBI/EXPMA 指标），**不含 `close` 或任何 OHLCV 字段**；取 `.close` 静默返 null；⚠️ 对比：`indicator/nine-turn` 端点明确包含"K 线基础字段（OHLCV+amount）"，其他技术指标端点（`oscillator`/`trend-volume`）同 `ma-channel` 一样**无 OHLCV**；需要收盘价与均线对比时，另调 `stock/kline/daily` 并按 tradeDate 联合，不要期望从指标端点取到
- ❌ **以为 `ths-hot.rankTime` 是毫秒时间戳并对其做 `÷1000` 转换**——`ths-hot` 端点有两个时间字段含义完全不同：`tradeDate`（⚠️ **毫秒时间戳**，需 `÷1000` 转 UNIX 秒再格式化）和 `rankTime`（**`"YYYY-MM-DD HH:mm:ss"` 字符串**，可直接用作时间标注，不需任何转换）；对 `rankTime` 执行 `÷1000` 或 `Date(rankTime)` 按整数操作会得到乱码；⚠️ 混淆来源：ms 时间戳列表标注 `ths-hot（rankTime 更直观）` 是指"用 `rankTime` 字段展示更直观"，不是说 `rankTime` 本身是毫秒
