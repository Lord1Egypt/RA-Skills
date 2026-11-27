---
slug: smartlib-citation-checker
name: smartlib-citation-checker
displayName: 参考文献验真、AI引用核查（12亿全球文献，有原始文献链接可核验）
version: 4.0.2
description: 核查用户提交的论文稿件或AI生成参考文献是否真实，防止AI幻觉。基于SmartLib API，输出HTML核查报告（含差异标记、验证链接、统计分析）。支持GB/T 7714-2025（2026年7月1日起实施）/APA/MLA/Chicago/BibTeX多格式解析与输出，并行检索（8条/批）+ Token缓存复用 + 智能提前终止回退。✨ 亮点：核查结果附带原始数据库来源链接（覆盖300+数据库，如Scopus/WoS/EI/PubMed等，有检索结果的条目均附原始来源链接供交叉验证），可交叉验证文献真实性。全程自动化：首次使用自动注册开通（免费100次/月），配额自动消耗，用尽后引导充值续费。触发词：核查引用、验证参考文献、检查引用、查引用、论文引用检查、AI引用核查、参考文献真假、文献核实、引用验证、引用格式检查、AI论文引用检查、参考文献审计、论文参考文献是真的吗、AI写的论文引用靠谱吗、ChatGPT引用核查、verify citation、check references。
agent_created: true
recommends:
  - keji-skill-showcase
  - owlwrite-paper
---

# SmartLib 文献引用核查与纠错 / Citation Authenticity Checker

> 中文 / Chinese | [English below each section]

本技能基于 `global-biblio-base` 的文献检索能力，对用户提交的论文稿件或文本引用进行核查与纠错，最终输出一个结构化的 HTML 核查报告文件。**与 global-biblio-base 共享凭证和配额。**

> This skill uses `global-biblio-base` to verify academic references and detect errors, generating a structured HTML report. **Shares credentials and quota with global-biblio-base.**

---

## ⚡ 启动前必须执行 / Pre-flight Checklist（每次调用都必须执行）

### Step A：凭证自动检测 & 注册 / Auto Credential Check & Registration

> ## ⚠️ 邮箱规则（唯一口径，v3.7.0 统一）
>
> **判定顺序（从上往下，命中即停）：**
>
> | 顺序 | 条件 | 动作 |
> |---|---|---|
> | 1 | 用户本轮消息中出现了邮箱 | 直接使用该邮箱；与 config 不一致时先确认一句"检测到新邮箱 X，是否改用该账户？" |
> | 2 | config.json 的 `SMARTLIB_EMAIL` 已有值 | **直接使用，不再追问**（已绑定即为本人账户） |
> | 3 | 以上都无 | 停止执行，询问一次：<br>"请提供您的邮箱地址以注册 SmartLib 文献引用核查服务（新用户免费 100 次/月）" |
>
> **禁止项（永久有效）：**
> - 禁止自动生成/猜测邮箱（`user@example.com`、`auto@xxx.com` 等一律不允许）
> - 禁止用"示例邮箱"发起真实请求
> - 用户未给邮箱且 config 为空时，不得调用 `/register`、`/quota`、`/consume`、`/search`
>
> **邮箱识别自动化**：消息中出现完整邮箱地址（含 `@`）、或"我的邮箱是 xxx" / "email: xxx" / "用 xxx 注册" / "邮箱 xxx" → 按第 1 条处理。

本技能与 `global-biblio-base` **共享凭证和配额**。每次执行时按以下流程处理：

> Shares credentials and quota with global-biblio-base. Auto-detection flow:

```
① 先读取 global-biblio-base 技能目录下的 config.json
   Read config.json from global-biblio-base skill directory first

② 检查 SMARTLIB_EMAIL 是否已配置
   Check if SMARTLIB_EMAIL is already configured
  ├── 已配置 → 进入 Step B (配额检查) / Already configured → proceed to Step B
  │
  └── 未配置 → 验证码注册流程:
        ├── ① 展示核查计划 + 询问邮箱（一句话）:
        │      "📋 我将核查您的参考文献真实性... 首次使用需绑定邮箱（免费 100 次/月，仅用于配额管理），请输入邮箱即可开始:"
        │      用户输入 → 写入 global-biblio-base 的 config.json
        │
        ├── ② 发送验证码:
        │     POST {SMARTLIB_GATEWAY_URL}/register/send-code
        │     Body: {"email": "{用户邮箱}"}   ← 此接口无需鉴权头
        │
        │     返回 code_sent → 请用户查收 6 位数字验证码（15 分钟内有效，
        │       未收到提示检查垃圾邮件箱），收到后请用户把验证码发回来
        │     返回 already_registered → 该邮箱已注册，跳过 ③④ 直接进 Step B
        │     返回 429 → 发送过于频繁/IP 限流，按 retry_after_seconds 提示稍后再试
        │
        ├── ③ 提交验证码完成注册:
        │     POST {SMARTLIB_GATEWAY_URL}/register/verify
        │     Body: {"email": "{用户邮箱}", "code": "{6位数字验证码}"}
        │
        │     返回 registered → 注册+验证一步完成，提示:
        │       "✅ 注册成功！本月免费 100 次，可立即使用。"
        │       追加引导: "请把您的参考文献发给我，现在就可以开始核查——"
        │     返回 verify_failed → 验证码错误或已过期 → 回到 ② 重发
        │     返回 403 disposable_email → 临时邮箱不可用，请用户换正式邮箱
        │
        └── ④ 继续 Step B 配额检查 → 核查
```

> **注意**：注册需邮箱验证码（6 位数字，15 分钟有效）。**注册即完成邮箱验证**，注册后即可立即使用。

### Step B：配额检查 / Quota Check

```
凭证就绪后, 调网关查询配额:
  GET <SMARTLIB_GATEWAY_URL>/quota?email=<SMARTLIB_EMAIL>
  Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}

  返回字段: total_remain, email_verified, plan, download_quota_free, download_reset_at, download_paid_remain, download_remain
  （完整返回: user_id, email, plan, trial_total, trial_used, trial_remain, paid_total, paid_used, paid_remain, paid_expires_at, total_remain, email_verified, download_quota_free, download_reset_at, download_paid_remain, download_remain）

  如果返回 404 "not_registered" → 用户可能已被重置/删除
    → 提示: "检测到您的账户需要重新绑定，正在自动重新注册..."
    → 跳回 Step A ②（调 /register 重新注册，使用同一邮箱）
    → 注册成功后继续配额检查

  total_remain > 20 → 静默进入核查
  total_remain 5-20 → 尾部轻提示: "📊 本月剩余 {n} 次"
  total_remain 1-5  → 警告: "⚠️ 接近用尽（剩余 {n} 次），说「我要升级」查看套餐（详见 global-biblio-base 的 references/account.md）"
  total_remain 0    → ⚠️ 先做 Step B2 账户模式判定，**不可直接判"拒绝服务"**

  额外检查:
```

### Step B2：账户模式判定 / Account Mode Detection（v3.7.0 新增，必须执行）

> 账户有两种计费模式，**调用形态完全不同**。判错模式 = 100% 失败。这一步不看会踩坑。

```
读 /quota 返回的 longterm 对象:
  longterm.mode == "balance"          → 【余额计费账户】走 §B2-A
  longterm.mode == "quota"            → 【配额账户】走现有 Step C（按次计费）
  无 longterm 对象 / longterm 为 null  → 【普通账户】走现有 Step C

⚠️ 余额计费账户的可用性不靠 total_remain 判断:
   total_remain == 0 但 longterm.mode == "balance"  → 仍可正常消费，继续服务
   真实可用额度看 GET /balance 的 balance_remain_yuan
```

#### B2-A 余额计费账户（长期包 / 充值客户）

**① 必须持专属私钥（sk-user），共享密钥对余额账户一律拒绝**

```
若 config.json 的 SMARTLIB_API_KEY 为空 → 引导换取（一次性，约 1 分钟）:

  a) POST {SMARTLIB_GATEWAY_URL}/register/send-code
     Body: {"email": "<SMARTLIB_EMAIL>", "kind": "apikey"}      ← kind 必填且必须是 apikey
     返回 code_sent → 请用户查收 6 位验证码

  b) POST {SMARTLIB_GATEWAY_URL}/auth/api-key/issue
     Body: {"email": "<SMARTLIB_EMAIL>", "code": "<6位验证码>", "client_id": "smartlib-citation-checker"}
     返回 api_key: "sk-user-..."（51 字符，有效期 1 年）→ 写入 config.json 的 SMARTLIB_API_KEY

  c) 换钥后所有请求改用 Authorization: Bearer <SMARTLIB_API_KEY>
```

**② 调用形态：只能用语义化端点，禁止代理模式**

| 要做的事 | 余额账户唯一可用写法 |
|---|---|
| 中文期刊检索 | `POST /search` `{"endpoint":"/search/cn", "email":"...", "rule":"...", "filter_rule":"...", "page_size":20}` |
| 全球文献检索 | `POST /search` `{"endpoint":"/search/global", ...}` |
| 中文期刊详情 | `POST /search` `{"endpoint":"/detail/cn", "article_ids":["..."]}` |
| 全球文献详情 | `POST /search` `{"endpoint":"/detail/global", "article_ids":["..."]}` |

> ⚠️ **详情接口参数双轨**：语义化模式（余额账户）用 `article_ids` 数组；代理模式（`api_path` 直连上游，如 `"/openapi/t/data0011/doccenter/Articledetail"`）必须用 `Identifier` 字符串（单个 ID，如 `"20621610706"`）。两者混用会返回「文献id不能为空」——按当前账户模式选对参数，不要互换。

> ❌ **余额账户禁止使用 `api_path` + `api_body` 代理模式**——网关会返回 403 `upgrade_required`。这是安全设计，不是故障，**不要重试、不要尝试绕过**，直接切语义化端点。
>
> 语义化端点仍需 `email` 字段，**且 `email` 必须与私钥所属账户一致**。

**③ 检索式：`Rule` 里不能出现 `Y`（年份），年份/类型/语言一律放 `filter_rule`**

| | 写法 | 结果 |
|---|---|---|
| ✅ 正确 | `rule: "T=attention all you need"`<br>`filter_rule: "Y=2017"` | 正常返回 |
| ❌ 错误 | `rule: "(T=attention all you need) AND Y=2017"` | 余额账户 **400 `invalid_rule`**；普通/配额账户可能「通过」但结果不可靠——**为统一实现一律禁止**，年份只走 `filter_rule` |

- `rule` 只允许：`T` 题名 / `A` 作者 / `K` 关键词 / `P` 出版者 / `PU` 出版单位 / `O` 机构 / `U` 任意字段
- `filter_rule` 允许：`L` / `C` / `Y` 年份 / `TY` 类型 / `LA` 语言 / `IS` 期 / `IB` / `MO` 载体

**④ 计费口径：按「条」计价，不是按「次」**

- 每次调用返回多少条 → 按实际返回条数计价（详情接口按 `article_ids` 的条数计价）
- 失败调用不计费（预扣回补）
- **不要用 `/quota` 的 total_remain 做成本预估**，用 `GET /balance` 与 `GET /balance/transactions` 逐笔对账
- 多会话并发时每笔请求必须带 `client_request_id`（自定义唯一串），否则流水无法区分会话

**⑤ 常见错误码处理**

| 错误码 | 含义 | 正确处理 |
|---|---|---|
| `403 upgrade_required` | 用了共享密钥调余额账户 | 走 ①换钥 → ②语义化端点 |
| `400 invalid_rule` | `rule` 里混入了 `Y` 或语法残缺 | 把年份搬到 `filter_rule`；**不要重试原式** |
| `403 balance_exhausted` | 余额不足 | 告知用户联系 vipsmart@vipslib.com 充值，附余额与可调用次数估计 |
| `401 unauthorized` / `missing_token` | 私钥失效或漏传 email | 重新换钥 / 补 email |

### Step B3：夜猫子账户联动 / Owl Account Link（v4.0.1 双栈编排）

> **首次核查照常出结果、不打断**；报告尾部一行轻提示引导绑定（"验真只是开始——查撤稿、写作、查重、排版也能在这接着做"）。用户点头后按下方流程绑定；已绑定用户进入**双栈并扣**。
> **深度核验 / 查撤稿 / 撤稿把关**仍走夜猫子独立计费（用户明确点头才跑付费能力）。
> 双栈期的"记数"只记权益次数、**不扣夜猫子积分、不因余额不足卡用户**——用户仍按 SmartLib 权益主扣费。

**双栈并扣编排（v4.0.1 新增）**：绑定后每次核查，除 SmartLib 侧 `/consume`→`/search` 扣 1 次外，另调一次夜猫子影子记数端点 `POST {OWL_API_BASE}/v1/entitlement/shadow-note`，body `{"run_id": "<本次核查唯一ID>", "used": 2}`（分词1+详情1），带同一 `Authorization: Bearer <OWL_API_KEY>`。该端点**只记次数、不扣积分、不生成报告**；失败静默忽略、不影响验真主流程。这是为将来 SmartLib 权益耗尽后平滑全切积累数据，用户此刻无需额外付费。

夜猫子（斟知）与 SmartLib 是**两套独立账户与钱包，互不相通**：

| | SmartLib | 夜猫子 |
|---|---|---|
| 计费 | 配额制（按次） | 积分制（按实时报价扣积分） |
| 新用户赠礼 | 免费 100 次/月 | 注册赠积分可用于参考文献核验，其余能力以实时报价为准 |
| 币值 | — | 1 积分 = ¥0.01 |

> **口径必须说清**：SmartLib 配额不能抵扣夜猫子积分，反之亦然。对用户只讲一句：
> 「深度核验走夜猫子的独立计费，注册赠积分可用于参考文献核验，其余以实时报价为准。」

- **基址**：`config.json` 的 `OWL_API_BASE`（默认 `https://owl.skillsutra.cn`）
- **鉴权**：`Authorization: Bearer <OWL_API_KEY>`（key 形如 `owl_sk_...`）

**判定顺序（严格按序，不可跳步）：**

**① 本地已有 `OWL_API_KEY`？** → `GET /v1/me` 验活
- 200 → 直接进 Step D
- 401 → 清掉本地 key（记「失效」），进 ②

**② `POST /v1/auth/register`** body `{"email": "<用户邮箱>"}`

| 响应 | 分支 |
|---|---|
| `409 email_exists` | → ③L 老用户找回 |
| `400 code_required` | → ③R 新用户注册 |
| `429 register_rate_limited` | 停止重试，告知"注册过于频繁，请一小时后再试"；**本次核查继续走 SmartLib** |
| 其他 | 按「错误处理」章节降级 |

**③R 新用户注册（两段式，必须等用户回码）**
1. `POST /v1/auth/send-code` `{"email":"..."}`
2. 提示用户：「验证码已发到 xxx（15 分钟内有效），把 6 位数字发我」
3. **停止执行，等用户回复** — 禁止自行编造验证码、禁止跳过、禁止循环重发（60 秒冷却 + 24h 上限，会被封 IP）
4. 收到码后 `POST /v1/auth/register` `{"email":"...","code":"123456"}`
5. 成功响应里的 `api_key` **只出现这一次** → 立即写入 `config.json` 的 `OWL_API_KEY` → 进 Step D
6. 失败（`code_invalid` / `code_expired`）→ 提示可重新发码；用户放弃则退回 SmartLib 路径

**③L 老用户找回**
1. `POST /v1/auth/login-code` `{"email":"..."}`
2. 同样等用户贴 6 位码
3. `POST /v1/auth/login-code/verify` `{"email":"...","code":"..."}` → 签发新 key（旧 key 继续有效）
4. 落盘同 ③R-5

**key 落盘规矩**
- 只写 `~/.workbuddy/skills/smartlib-citation-checker/config.json` 的 `OWL_API_KEY`
- **绝不**写进 `config.example.json`、**绝不**回显给用户、**绝不**写进报告或日志
- 只用一行告知：「已存在你本机，等同登录凭据，别外传」

**禁止事项**
- ❌ 未得用户点头就跑注册流程（报告尾部一行轻提示不算主动跑注册）
- ❌ 把 `OWL_API_KEY` 回显或写入任何输出
- ❌ 把 SmartLib 配额当夜猫子积分用
- ❌ 验证码失败后反复重发
- ❌ 把影子记数端点失败当成验真失败——记数失败一律静默忽略，验真结果照常交付

### Step C：按接口调用次数消耗配额 / Per-API-Call Quota Consumption

本技能与 global-biblio-base **共享配额和计次规则**。配额按**实际 API 接口调用次数**计费，不是按核查会话计费。

共涉及 **5 个接口**（分3类），每次调用其中任意一个接口计 **1 次**配额。

> Quota shared with literature-search. Consumed **per API call**, not per verification session. **5 interfaces** in 3 categories, each call = 1 quota.

**计费接口清单（5个）/ Billable Interfaces (5 total):**

| 类别 | 接口 | API 端点 | 计费 |
|------|------|---------|------|
| **检索** | 中文期刊检索 | API 1 `Articlesearch` | 每次调用 **1 次** |
| **检索** | 全球文献检索 | API 4 `Articlesearch` | 每次调用 **1 次** |
| **详情** | 中文期刊详情 | API 1/5 `Articledetail` | 每次调用 **1 次** |
| **详情** | 全球文献详情 | API 4/5 `Articledetail` | 每次调用 **1 次** |
| **下载** | 中文期刊全文下载 | API 3 `GetArticleFile` | 每次调用 **1 次** |

> 注：全球文献（API 4）无全文下载接口，仅返回元数据。外文文献下载走十级多渠道 OA 探测，不计 SmartLib 配额。

**计次示例 / Counting Examples:**

```
示例1：核查 10 条参考文献（含中英文各5条）
  → 检索接口：中文5次 + 英文5次（并行，每篇独立检索）= 10 次
  → 详情接口：匹配后查 8 篇详情 = 8 次
  → 下载接口：中文期刊下载 2 篇 = 2 次
  → 合计消耗: 20 次配额
```

```
示例2：核查 1 条参考文献
  → 检索接口：1 次
  → 详情接口：匹配后查 1 篇详情 = 1 次
  → 合计消耗: 2 次配额
```

**扣减方式 / Deduction Method:**

每次调用计费接口前，必须先调 `/consume` 获取 token，再用 token 调 `/search`。**两种账户用不同写法，选错必失败：**

```
① POST <SMARTLIB_GATEWAY_URL>/consume
   Headers: {"Authorization": "Bearer <凭证>"}
     普通/配额账户 → SMARTLIB_GATEWAY_SECRET
     余额账户     → SMARTLIB_API_KEY（sk-user-…）
   Body: {"email": "<SMARTLIB_EMAIL>", "skill_source": "smartlib-citation-checker"}
   → 获取 consume_token

② POST <SMARTLIB_GATEWAY_URL>/search
   Headers: {"Authorization": "Bearer <同一凭证>"}
```

| 账户模式 | ② 的 Body 写法 |
|---|---|
| 普通 / 配额账户 | 代理模式：`{"email":"…","consume_token":"…","api_path":"/openapi/t/skrs2/doccenter/Articlesearch","api_body":{"Rule":"T=…","FilterRule":"Y=2017","PageIndex":1,"PageSize":20,"Sort":1}}` |
| **余额账户** | 语义化模式：`{"email":"…","consume_token":"…","endpoint":"/search/global","rule":"T=…","filter_rule":"Y=2017","page_index":1,"page_size":20,"sort":1}`<br>**禁用 api_path**（403 `upgrade_required`） |

**接口 ↔ api_path 对照（代理模式用）：**

| 语义化 endpoint | 代理模式 api_path |
|---|---|
| `/search/cn` | `/openapi/t/data0012/doccenter/Articlesearch` |
| `/detail/cn` | `/openapi/t/data0011/doccenter/Articledetail` |
| `/download/cn` | `/openapi/t/data0013/doccenter/GetArticleFile` |
| `/search/global` | `/openapi/t/skrs2/doccenter/Articlesearch` |
| `/detail/global` | `/openapi/t/skrs1/doccenter/Articledetail` |

> Call `/consume` → `/search` for **each** billable API call. Token single-use, 60s TTL.

**🛡️ Token 绑定调用链 / Token-Bound Call Chain:**

> **强制安全机制 — 不可绕过：**
> 每次调用计费接口前，必须通过 `/consume` 获取 `consume_token`，然后将 token 传给 `/search`。
> Gateway 验证 token 签名 + 有效期 + 防重放后才转发检索请求。无有效 token 则 `/search` 直接 401。
>
> **注意**：每个 consume_token 只能使用一次（防重放），有效期 60 秒。每次检索 API 调用前都需要先 `/consume` 获取新 token。
>
> ⚠️ `400 invalid_rule` 走的是**语法校验前置**通道：不消耗配额，且该 token 未被消费，60 秒内改正检索式可复用同一 token，不必重新 `/consume`。

**🆕 v36 行为：仅成功调用消耗配额 / Quota Deducted on Success Only:**

> `/consume` 仅验证配额可用性 + 签发 token，**不预扣配额**。配额在实际调用 SmartLib API 且返回成功后，由 Gateway 自动扣除。失败的 API 调用不消耗配额。
> 这意味着：核查时若某条文献检索失败（如关键词匹配不到），不会浪费配额，可放心重试。

**不计费的操作 / Non-billable Operations:**

| 操作 / Operation | 说明 / Note |
|------|------|
| /consume 配额消费 | Gateway 验证，不计费 |
| 引用格式解析（GB/T 7714/APA/MLA等） | 本地处理，不计费 |
| 匹配度计算与比对 | 本地处理，不计费 |
| HTML 报告生成 | 本地处理，不计费 |
| 外文 OA PDF 探测 | 外部免费 API（Unpaywall等），不计 SmartLib 配额 |
| 统计分析 | 本地处理，不计费 |

---

## 💰 支付与充值 / Payment & Recharge

### 触发时机
1. 配额为 0 (gateway 返回 429)
2. 用户说 "充值" "续费" "购买" "我要升级"

### 计费与升级（统一钱包）

本技能与 global-biblio-base **共享统一钱包配额**，所有文献检索技能**统一定价、配额共享**。

- 套餐价格、额度、注册与升级流程：**见 global-biblio-base 的 `references/account.md`（smartlib-account）**。
- 配额不足或想升级：在对话中说「我要升级」即可（由 global-biblio-base 的统一钱包处理，无需在本技能操作）。
- 企业 / 机构定制：联系 vipsmart@vipslib.com。

---

## 🔒 配额耗尽处理 / Quota Exhaustion

> ⚠️ **先判账户模式（Step B2），再判是否"耗尽"。** 余额账户 `total_remain=0` 不代表不可用——直接拒绝会把付了钱的客户挡在门外（v3.6.8 及以前的实际故障点）。

| 账户模式 | 状态 | 行为 |
|---|---|---|
| 配额账户（trial/paid） | 配额充足 (>0) | 完整展示所有核查结果（含差异标记、验证链接、统计分析、HTML 报告） |
| 配额账户（trial/paid） | 配额耗尽 (=0) | Gateway 返回 429，**拒绝服务**，自动弹出套餐卡片（由 global-biblio-base 统一处理） |
| **余额账户** | `balance_remain_yuan > 0` | **正常服务，不看 total_remain**；可在报告尾部附余额提示 |
| **余额账户** | `balance_remain_yuan ≤ 0` | 返回 `403 balance_exhausted`，提示联系服务方充值（vipsmart@vipslib.com / 023-63016015） |

配额耗尽后的提示格式（**仅配额账户适用**）：

```
⚠️ 您的 SmartLib 检索配额已用尽（0/100次）。

当前配额不支持发起新的文献核查请求。请在对话中说「我要升级」查看套餐（详见 global-biblio-base 的 `references/account.md`），支付后立即恢复配额。
```

**重要**：配额耗尽后，**所有核查请求一律拒绝**，不展示任何部分结果。余额账户不适用本条，按余额判定。

---

## 输出规范 / Output Standards

**每次核查结果末尾必须展示配额状态：**

```
📊 本次消耗 {n} 次 | 剩余 {remain} 次 (共 {total} 次/月)
```
或接近耗尽时：
```
⚠️ 剩余 3 次 (共 100 次/月)，说「我要升级」查看套餐
```

```
```

---

## 核心能力 / Core Capabilities

| 能力 / Capability | 说明 / Description |
|------|------|
| **引用解析 / Citation Parsing** | 自动识别并解析 GB/T 7714、APA、MLA、Chicago、BibTeX 等多种格式 / Auto-detect and parse multiple formats |
| **BibTeX支持 / BibTeX Support** | 完整解析 .bib 文件，支持 @article/@book/@inproceedings 等 entry 类型 |
| **真实性核查 / Authenticity Check** | 通过 SmartLib API 联网核查文献是否真实存在，**防止 AI 幻觉** / Verify via SmartLib API, detect AI hallucinations |
| **信息比对 / Field Comparison** | 将原始引用与数据库记录逐字段对比，识别差异 |
| **纠错输出 / Error Correction** | 对错误的作者、年份、期刊名、页码等信息提供修正版本（使用 `[删除]`/`[新增]` 标记） |
| **引用分析 / Citation Analytics** | 对批量文献进行年份分布、作者集中度、期刊集中度等统计分析 |
| **验证链接 / Verification Links** | 为每条匹配的文献提供可点击的验证链接 |
| **原始来源交叉验证 / Cross-Source Verification** | 提供 Scopus/WoS/EI/PubMed 等 300+ 数据库的原始来源链接，多维度交叉验证文献真实性；有检索结果的条目均附来源链接，平均约 4.75 个链接/篇 |
| **批量导出 / Batch Export** | 提供全量下载（Blob+createObjectURL，兼容所有浏览器环境） |
| **多格式输出 / Multi-format Output** | 保留原始格式，同时额外输出 GB/T 7714、APA、MLA、Chicago、BibTeX 五种常用格式 |

## 适用场景 / Use Cases

**主要场景（核心价值）：**
- **AI 幻觉验真**：用户使用豆包、ChatGPT、Kimi、文心一言等 AI 生成了参考文献，担心 AI "编造"了不存在的文献，提交核查
- **论文初稿审查**：作者对自己论文稿件中的参考文献进行真实性与格式规范性的自查，投稿前确保引用准确
- **粘贴式核查**：用户直接粘贴参考文献列表，快速批量验证和纠错

**其他场景（Other Scenarios）：**
- 提交 .bib 文件或粘贴 BibTeX 条目（Zotero/EndNote/LaTeX 用户）
- 编辑/审稿人批量核查来稿的引用准确性
- 对文献引用进行统计分析（年份分布、期刊偏好、作者集中度等）

---

## 工作流程 / Workflow

### Step 1: 解析引用 / Parse Citations

从用户输入中提取每一条参考文献，识别以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| `title` | 文献题名 | 深度学习在医学影像中的应用 |
| `authors` | 作者列表 | 张三, 李四, 王五 |
| `year` | 出版年份 | 2024 |
| `journal` | 期刊/会议名称 | 计算机学报 |
| `volume` | 卷号 | 45 |
| `issue` | 期号 | 3 |
| `pages` | 页码范围 | 123-145 |
| `doi` | DOI标识 | 10.1234/example.2024.001 |
| `type` | 文献类型 | 期刊/会议/学位论文/专利/图书 |

**引用格式识别规则：**

```
GB/T 7714-2025（2026.7.1实施，替代2015版）:
  期刊[J]: [1] 张三, 李四. 深度学习综述[J]. 计算机学报, 2024, 45(3): 123-145.
  图书[M]: [1] 张伯伟. 全唐五代诗格汇考[M]. 南京: 江苏古籍出版社, 2002: 288.
  学位论文[D]: [1] 王琦. 融合星载GNSS-R和SAR数据的土壤湿度反演方法研究[D]. 武汉: 武汉大学, 2022: 87.
  会议[C]: [1] 李妍, 王莹. 医疗机构保洁人员手卫生干预效果研究[C]//中华预防医学会第31次全国医院感染学术年会, 2022: 2.
  专利[P]: [1] 邓一刚. 全智能节电器: CN200610171314.3[P]. 2008-01-16: 8-9.
  标准[S]: [1] NB/T 10386-2020 水电工程水温实时监测系统技术规范[S].
  预印本[PP/OL]: [1] 肖玲, 张雪, 王永. 数据要素的统计测算方法探究[PP/OL]. PSSXiv (2024-07-02)[2024-09-30]. https://...
  数据集[DS/OL]: [1] 周壮, 李盛阳, 吴薇, 等. 天宫二号遥感图像分类科学数据[DS/OL]. V1.0. 国家基础学科公共科学数据中心 (2023-09-10)[2025-07-15]. https://...
  网页[EB/OL]: [1] 高等教育文献保障系统. 馆际互借与文献传递服务[EB/OL]. [2025-06-21]. http://...
**GB/T 7714-2025 关键变化（2026年7月1日实施，替代2015版）：**

| 变化项 | 2015版 | 2025版 |
|--------|--------|--------|
| 外文作者姓名 | 姓氏全大写（EINSTEIN A） | 仅首字母大写（Einstein A） |
| 中文拼音作者 | 无规定 | 姓全大写、名取首字母（LI J N） |
| "专著"术语 | 专著[M] | 图书[M] |
| DOI标识 | 数字对象唯一标识符 | 永久标识符（含DOI/ARK/CSTR等） |
| 引用日期 | 所有文献必填 | 仅电子资源保留，纸质文献去掉 |
| 文献类型标识 | 任选项 | 必选项 |
| 新增类型 | — | 预印本[PP/OL]、数据集[DS/OL]、地图[CM]、档案[A] |
| 标准[S] | 需标注出版地/出版者 | 仅需标准编号+名称（大幅简化） |
| 专利[P] | 无页码要求 | 有则必填引文页码 |
| 学位论文[D] | 无页码要求 | 必须标注引用页码 |
| 会议[C] | 格式模糊 | 明确格式：作者.题目[C]//会议名称, 年份: 页码 |
| 网页[EB/OL] | 需出版地/出版者 | 仅需责任者+题名+创建日期+引用日期+URL |

> **注意**：各期刊在国标基础上可能有自己的格式要求，核查时应以期刊具体投稿规范为准。

APA: Zhang, S., & Li, Y. (2024). Deep learning survey. 计算机学报, 45(3), 123-145.
MLA: Zhang, San, and Si Li. "Deep Learning Survey." 计算机学报, vol. 45, no. 3, 2024, pp. 123-145.
Chicago: Zhang, San, and Si Li. 2024. "Deep Learning Survey." 计算机学报 45 (3): 123-145.
BibTeX: @article{zhang2024deep, author = {Zhang, San and Li, Si}, ...}
```

**格式识别 → 表头标注规则**：HTML 报告表头展示——`原始参考文献 (输入格式)` → `GB/T 7714-2015 (旧国标)` → `GB/T 7714-2025 (新国标)`，后跟变化说明列。

**GB/T 7714 新旧对比输出规则（过渡期专用）：**

每次输出 GB/T 7714 格式时，同时生成 2015 版和 2025 版两列，并在「变化说明」列标注命中的变化项编号：

| 编号 | 变化项 | 触发条件 |
|------|--------|---------|
| ① | 外文作者仅首字母大写 | 外文作者在2015版全大写，2025版改为首字母大写 |
| ② | 拼音作者规范 | 中文拼音作者：姓全大写、名首字母 |
| ③ | "专著"→"图书" | 原2015版标注为"专著[M]" |
| ④ | 永久标识符 | DOI/ARK/CSTR 等永久标识符 |
| ⑤ | 文献类型标识必选 | 2015版为可选，2025版强制必选 |
| ⑥ | 去引用日期 | 纸质文献不再需要引用日期（电子资源保留） |
| ⑦ | 预印本[PP/OL] | 文献类型为预印本 |
| ⑧ | 数据集[DS/OL] | 文献类型为数据集 |
| ⑨ | 标准[S]简化 | 标准文献仅保留编号+名称 |
| ⑩ | 专利[P]加页码 | 专利增加引文页码（有则必备） |
| ⑪ | 学位论文[D]加页码 | 学位论文必须标注引用页码 |
| ⑫ | 会议[C]新格式 | 会议论文新格式：`//会议名, 年份: 页码` |

> **变化说明格式**：在核查表格的「变化说明」列中，以简洁编号标注，如 `①②⑤` 表示该条文献涉及外文作者、拼音规范、类型必选三项变化。鼠标悬停显示完整变化说明。

**BibTeX 解析规范**：识别 `@article{`、`@book{`、`@inproceedings{` 等 entry 类型，提取 author/title/journal/year/volume/number/pages/doi 字段。

### Step 2: 联网核查 / Online Verification（调用 SmartLib API）

**性能优化（必须遵守）：**

- **Gateway 管理 Token**：Gateway 全权管理 SmartLib OAuth Token，无需获取或缓存 Token。每次调用通过 /consume → /search 完成
- **并行检索**：每批 8 条并行发送 API 请求（30 条文献 8-15s 完成，串行需 60-120s）
- **智能提前终止**：优先级 1（题名+年份）返回高质量结果时跳过回退
- **进度反馈**：实时展示核查进度

**检索优先级：**

| 优先级 | 检索方式 | 适用条件 |
|--------|---------|---------|
| 1 | 题名核心词（`rule`）+ 年份（`filter_rule`） | 题名可提取（所有文献） |
| 2 | 去掉年份，仅题名核心词 | 优先级 1 返回 **0 条**时 |
| 3 | 切换另一接口重试 1 次 | 优先级 2 仍 0 条 |
| 4 | 前 3 词 + 作者姓，`page_size=100` | 两接口均 0 条 |
| — | DOI 仅做格式校验与链接生成 | **不参与检索**（全球库不支持 `Identifier_DOI` 字段） |

**检索表达式构建（v3.7.0 统一口径，唯一实现 / single implementation — 不要自行发明）：**

```python
# ① 关键词处理（全流程只此一套规则，删掉任何第二条分支）
stopwords = {"a", "an", "the", "in", "of", "for", "and", "on", "to", "is", "by",
             "with", "using", "based", "from", "we", "our", "this", "these"}
def keywords(title, n=6):
    raw = title.lower().replace(",", " ").replace(":", " ").replace("—", " ").replace("-", " ")
    seen, out = set(), []
    for w in raw.split():
        w = w.strip(".?!;()[]\"'")
        if not w or w in stopwords or w in seen:
            continue          # 必须去重（v3.7.0 起唯一写法）
        seen.add(w); out.append(w)
        if len(out) >= n: break
    return out

# ② 优先级 1：题名核心词（年份走 filter_rule，绝不进 rule）
rule        = f"T={' '.join(keywords(title, 6))}"
filter_rule = f"Y={year}" if year else ""

# ③ 优先级 2：去掉年份限制（仅题名关键词，提高召回）
rule        = f"T={' '.join(keywords(title, 5))}"
filter_rule = ""

# ④ 短题名加固（核心词 ≤3 时强制加限定，避免短题名被长题名吞并）
if len(keywords(title, 6)) <= 3 and first_author_surname:
    rule = f"(T={' '.join(keywords(title, 6))}) AND A={first_author_surname}"
```

> 🔴 **强制约束**：`rule` 里出现 `Y=` → 余额账户 100% 返回 `400 invalid_rule`；普通/配额账户虽可能通过，但为统一实现一律禁止。年份只走 `filter_rule`。

**接口路由（按文献类型与语种归属，不按引用书写语言）：**

| 文献类型 | 主接口 | 依据 / 说明 |
|---|---|---|
| 中文期刊论文（含中文著录的英文题名文献） | `/search/cn`（接口1） | 8000 万授权中文期刊；英文题名用 `Title_Alternative` 反查 |
| 英文期刊/会议论文 | `/search/global`（接口4） | 12.28 亿全球元数据 |
| 学位论文 [D] / 专利 [P] / 报纸 [N] / 标准 [S] | `/search/global`（接口4） | 中文库对这些类型返回 0 条，走接口1 必落空 |
| 图书 [M] | **不支持核查** | 全球库不含图书，见「能力边界」 |

**回退规则（v3.7.0 明确触发条件，不要再凭感觉）：**

| 优先级 | 条件 | 动作 |
|---|---|---|
| 1 | 始终先执行 | 题名核心词 + `filter_rule: Y=<年份>` |
| 2 | 优先级 1 返回 **0 条**（不是"无匹配"，是 0 条） | 去掉年份，仅题名核心词 |
| 3 | 优先级 2 仍 0 条 | **切换另一接口重试 1 次**，并在报告中注明"已切换接口" |
| 4 | 两接口均 0 条，且题名核心词 >3 | 放宽为前 3 词 + 作者姓，PageSize 提到 100 |
| — | 优先级 1 有结果但无一条相似度 ≥0.45 | 直接判 `NOT_FOUND`，**不要无限回退** |

**检索参数：**

```json
{
  "endpoint": "/search/global",
  "email": "<SMARTLIB_EMAIL>",
  "rule": "T=attention all you need",
  "filter_rule": "Y=2017",
  "page_index": 1,
  "page_size": 20,
  "sort": 1
}
```

> `page_size`：默认 20；结果集 >100 条或短题名场景提到 **100**（配合"精确题名优先"重排）。代理模式写法为 `Rule` / `PageIndex` / `PageSize` / `Sort`（首字母大写），语义化模式为全小写——**不要混用大小写**。

### Step 3: 匹配与比对 / Match & Compare

**题名相似度算法（v3.7.0 唯一实现 / the only formula）：**

```python
def title_similarity(cite_title, db_title):
    A = set(keywords(cite_title, 99))     # 引用侧词集
    B = set(keywords(db_title, 99))       # 库侧词集
    if not A or not B:
        return 0.0
    dice = 2 * len(A & B) / (len(A) + len(B))     # 对称分母，双向惩罚
    # 超集包含检测：引用词集被库题名吞并时额外降权
    if A <= B and len(B) > len(A) + 2:
        dice *= (len(A) / len(B)) ** 0.5
    # 副标题例外：库题名含 ":" 时，用主标题段再算一次取较高值
    if ":" in db_title:
        main = db_title.split(":")[0]
        dice = max(dice, title_similarity(cite_title, main))
    return dice
```

> ❌ 禁止使用 `|A∩B| / |A|`。该式在「引用题名是库题名子集」时恒等于 1.0，会把任意短题名匹配到毫不相关的长题名论文上（实测案例见验收用例 A16 / SP06 / D01 / H03）。

**四态判定阈值表（必须严格按分数区间判定，不得凭印象）：**

| 状态 | 判定条件（全部满足） | 验证链接 |
|------|--------------------|---------|
| `VERIFIED` | 题名相似度 ≥ **0.90** **且** 至少 1 位作者姓命中 **且** 年份差 ≤1 **且** 无风险标记 | 提供 |
| `VERIFIED ⚠️`（风险态） | 上述全部成立，但**命中撤稿信号**：夜猫子 `retraction=retracted`/`concern`（优先），或库记录题名含 `RETRACTED` / `撤稿` / `Retraction` / `<sup>撤</sup>`（无夜猫子时的弱信号） | 提供 + **顶部红旗警示** |
| `MISMATCH` | 题名相似度 0.60–0.90；**或** 题名 ≥0.90 但作者/年份/卷/期/页存在字段级差异 | 提供 |
| `FUZZY_MATCH` | 题名相似度 0.45–0.60；**或多候选间相似度差 <0.05 无法择优** | 不提供，标注存疑 |
| `NOT_FOUND` | 题名相似度 < 0.45 | 不提供 |

**全字段命中例外（防误杀真文献）**：题名相似度 0.70–0.90，但作者 + 年份 + 期刊 + 卷期 + 页码 **全部**命中 → 允许判 `VERIFIED`，并在报告注明"题名存在副标题/截断差异"。

**强制规则（三条硬约束，缺一即视为执行错误）：**

1. **题名逐字符 diff 硬规则** — 相似度 ≥0.95 时仍须逐词比对，列出差异词及位置。单词级替换（如 `all we need` → `all you need`、`we` → `you`）一律 **不得** 判 `VERIFIED`，必须降为 `MISMATCH` 并指认差异词。
2. **多候选全扫** — 同一题名返回 ≥2 条记录时，**必须扫描全部记录的状态标记（撤稿/更正/勘误）后再择优**，禁止机械取首条。择优顺序：① 有撤稿标记者优先展示 ② 字段最全者 ③ 与引用声明版本一致者（预印本 vs 正式版）。
3. **空缺即"无法核验"** — 库记录字段为空（DOI / 期刊 / 卷 / 期 / 页）时，该字段输出 `⚠️ 库内该字段为空，无法核验`，**不得计入"一致"，也不得据此判 VERIFIED**。

**匹配结果分类：**

| 结果 | 状态码 | 说明 | 验证链接 |
|------|--------|------|---------|
| 验证通过 | VERIFIED | 高度匹配，信息准确 | 提供（SmartLib + 多数据库原始来源） |
| 通过但有风险 | VERIFIED ⚠️ | 文献真实，但已被撤稿/更正 | 提供 + 红旗警示 |
| 存在差异 | MISMATCH | 找到匹配文献，但部分字段有差异（含题名单词级篡改） | 提供 |
| 未找到 | NOT_FOUND | 未匹配到（含疑似幻觉） | 不提供；**须给替换建议**，见下方 |
| 疑似匹配 | FUZZY_MATCH | 疑似结果，需人工确认 | 不提供（标注存疑） |

**NOT_FOUND 的替换建议（v3.7.0 起为必选输出）**：判 `NOT_FOUND` 时，用题名核心词在库内检索 3–5 条相近真实文献，作为「可点验的替换候选」列出（含标题、作者、年份、DOI/详情链接）。若相近候选也找不到，明确写"库内亦无相近文献，疑似虚构"。

### Step 4: 差异分析 / Diff Analysis（针对 MISMATCH）

**第一步：字段归一化（v3.7.0 新增，归一化后再比对，否则必然误报）**

| 类型 | 归一化规则 | 示例 |
|---|---|---|
| 页码缩写 | 末段不足前段位数时补全前缀 | `2139-74` ≡ `2139-2174` |
| 破折号 | `–` `—` `－` `~` 一律视作 `-` | `2139–2174` ≡ `2139-2174` |
| 卷期前缀 | 去掉 `v` / `V` / `Vol` / `N` / `No` 及空格 | `v 27/N 3-4` ≡ `27(3-4)` |
| DOI | 去 `https://doi.org/`、去 `doi:`、小写、去尾部标点 | `10.1000/ABC` ≡ `10.1000/abc` |
| 占位符 | `Variouspages` / `XXXX` / `待定` / `n/a` / `-` **一律视为缺失** | 不得参与差异比对 |
| 期刊名 | 去 `The `、去句点、大小写不敏感；缩写与全称互认（`J.` ≡ `Journal`） | `Phys Rev Lett` ≡ `Physical Review Letters` |
| 题名 | 去标点、去副标题后比对；大小写不敏感 | — |

**第二步：字段级差异判定**

| 字段对比 | 差异类型 | 纠错建议 | 库字段为空时 |
|---------|---------|---------|------------|
| 作者姓名 | 拼写错误、缺少中间名、顺序错误 | 提供正确作者列表 | ⚠️ 无法核验 |
| 作者形态变体 | 拼音 / 集团作者 / 标准起草委员会 **不算差异** | 不做纠错 | — |
| 年份 | 年份错误 | 提供正确年份 | ⚠️ 无法核验 |
| 期刊名 | 缩写不规范、全称/简称混淆 | 提供标准期刊名 | ⚠️ 无法核验 |
| 卷期号 | 卷号/期号错误 | 提供正确卷期 | ⚠️ 无法核验 |
| 页码 | 起止页码错误（归一化后仍不同才算） | 提供正确页码范围 | ⚠️ 无法核验 |
| 题名 | 打字错误、遗漏词汇、**单词级替换** | 提供正确题名 + 差异词位置 | — |
| DOI | DOI错误或缺失 | 提供正确DOI | ⚠️ 无法核验（**不得判"DOI 一致"**） |

**作者形态变体白名单（不误报为"作者差异"）：**

| 形态 | 示例 | 处理 |
|---|---|---|
| 拼音作者 | `Zhang San` / `Zhang S` / `Zhang, S.` / `ZHANG S` | 姓氏精确等值 + 名首字母匹配即视为同一人 |
| 集团作者 | `The X Collaboration` / `XX 研究组` / `XX 协作组` | 整体字符串比对，不做姓名拆分 |
| 机构起草人 | `全国XX标准化技术委员会` / `XX Standardization Technical Committee` | 视为一个作者单位，不与个人作者混比 |

> 🔴 **空缺字段的铁律**：库记录某字段为空 → 输出 `⚠️ 数据库该字段为空，无法核验`，**明确告知用户"未比对"而不是"一致"**。把空字段当"一致"会让篡改的 DOI / 期刊名直接放行（这是验收用例 D12、G01 的失败原因）。

### Step D: 深度核验 / Deep Verification（夜猫子，v3.7.0 新增）

> 用于撤稿把关与强判定。**不是默认路径**——用户没要求就用 SmartLib 结果出报告。

**三步契约（顺序不可颠倒）：**

```
① POST /v1/quote   {"action":"verify","params":{"refs_text":"<编号参考文献原文>"}}
   → {"quote_id":"...", "points": <预估积分>}     有效期 24 小时

② POST /v1/runs    {"quote_id":"..."}
   → {"run_id":"...", "status":"reserved"}        执行即开始计费

③ GET /v1/runs/{run_id}    轮询：1.5s 起，×1.5 退避，封顶 5s，总超时 180s
   → status: reserved / queued / running / succeeded / failed
   → succeeded 时取 result.summary + result.items（逐条 verdict + retraction）
```

**`refs_text` 拼接规范**
- `[1] 原文\n[2] 原文` 编号列表，一条一行
- 保留用户原始引用文本，**不要**预先改写格式（夜猫子自己解析）
- **支持格式（v4.0.2）**：GB/T 7714（2015/2025）、APA、MLA、Chicago、BibTeX——夜猫子后端已做格式归一化，五种格式均能正确提取题名/年份/刊名/卷期/页码/DOI。其他小众格式建议先归一化为 GB/T 7714 再送深核，避免误判
- 单次上限：10 万字符 / 500 条；超出分批，每批 ≤200 条

**判定映射（夜猫子 → 本技能状态）**

| 夜猫子 `verdict` | `retraction` | 本技能状态 | 处理 |
|---|---|---|---|
| `VERIFIED` | `clean` | `VERIFIED` | 正常 |
| `VERIFIED` | `retracted` | **`VERIFIED ⚠️`** | 置顶红旗「该文献已撤稿」，**不得显示通过** |
| `VERIFIED` / `LIKELY` | `concern` | `VERIFIED ⚠️` | 标「编辑关切」 |
| `LIKELY` | 任意 | `FUZZY_MATCH` | 题名接近，需人工确认 |
| `METADATA_MISMATCH` | 任意 | `MISMATCH` | 直接采用其 `diffs` 作纠错建议 |
| `SUSPECT` | 任意 | `FUZZY_MATCH` | 标存疑 |
| `NOT_FOUND` | — | `NOT_FOUND` | 附替换建议 |
| `ERROR` | — | 不写结论 | 标「本条未核验」，按下方降级 |

> **撤稿三态铁律**：`clean` 仅在**确实拿到该条 DOI 并查到记录**时才是「未撤稿」；无 DOI 或查询失败一律写 `⚠️ 未核撤稿状态`，**不得显示「未撤稿」**。

> 🔴 **撤稿题名兜底（v4.0.2）**：夜猫子返回条目若 `retraction` 字段缺失/为空，但 `hit.title`（命中题名）或引用题名含 `RETRACTED:` / `Withdrawn:` / `已撤稿` 等强标记，一律按**已撤稿**处理、置顶红旗，**不得显示「通过」**。后端已内置同款兜底并标 `retraction_source=title_marker`；Agent 侧见字段缺失时按此规则复核，形成双保险。若后端已给 `retraction`（clean/retracted/concern），**以后端为准，不覆盖**。题名标记来自数据源原始记录，仅供参考，报告须注明「以出版社撤稿声明为准」。

**计费提示（必须告知）**
- 报价阶段就报 `points`（按实时报价，72h 内重复核验更省）
- 用户确认后才 `POST /v1/runs`
- 余额不足（`insufficient_points`）→ 报当前余额与所需量，给充值入口，**不得自动充值**

**降级（任一环节失败都不许让整次核查失败）**

| 失败点 | 处理 |
|---|---|
| 夜猫子不可达 / 5xx / 超时 | 退回 SmartLib 结果，报告注「本次未做撤稿把关」 |
| 轮询 180s 未完成 | 告知 run_id 可稍后查，本次先用 SmartLib 结论 |
| `failed` | 如实告知（夜猫子失败自动退款），**不重复扣费** |

**与题名标记法的关系（v4.0.2 修订）**：拿到夜猫子结果时，撤稿判定**优先以后端 `retraction` 字段为准**；但当该字段缺失时，**回退用命中题名的 `RETRACTED:`/`Withdrawn:` 强标记兜底**（见上方撤稿三态铁律下的兜底条款），不直接判通过。完全没有夜猫子结果的条目才退化为弱信号，措辞必须是「库内未见撤稿标记，不代表未撤稿」。

### Step 5: 生成 HTML 核查报告 / Generate HTML Report

最终输出为一个完整的 HTML 文件，预览窗口自动打开，并交付给用户下载保存。

**报告结构：**

```
┌─────────────────────────────────────────────────────────┐
│ 报告头部：标题 + 核查时间 + 汇总徽章（总数/差异/存疑）    │
├─────────────────────────────────────────────────────────┤
│ 核查结果表格（7列）                                      │
│ # / 状态 / 原始参考文献 (格式名) / 2015版 / 2025版修正 / 变化说明 / 验证链接 │
├─────────────────────────────────────────────────────────┤
│ 修正后参考文献纯文本区块（可复制）                       │
├─────────────────────────────────────────────────────────┤
│ 多格式参考文献区块（Tab页签切换）                        │
│ GB/T 7714 | APA | MLA | Chicago | BibTeX               │
├─────────────────────────────────────────────────────────┤
│ 引用统计分析（文献数 >= 3 时输出，4栏卡片布局）           │
├─────────────────────────────────────────────────────────┤
│ 页脚：数据来源说明                                       │
└─────────────────────────────────────────────────────────┘
```

**差异标记（HTML + 纯文本双重兼容）：**

| 标记 | HTML样式 | 纯文本等价 |
|------|---------|---------|
| 删除内容 | 红色背景高亮 + `[删除]`前缀 | `[删除]"旧值"` |
| 新增内容 | 绿色背景高亮 + `[新增]`前缀 | `[新增]"新值"` |
| 转换箭头 | 蓝色箭头 → | → |

**下载按钮：**
- **表头按钮**："修正后文献"列顶部有下载图标，点击将所有文献打包为 `参考文献-核查结果.txt` 下载
- **行级按钮**：每行右侧下载单条文献为 `参考文献-N.txt`
- **实现方式**：`Blob` + `URL.createObjectURL` + 动态 `<a>` 标签

**统计分析（文献数>=3时）：** 年份分布横向条形图 / 期刊分布横向条形图 / 作者分析 / 机构来源 / 整体建议（3-5条）

**纯文本参考文献区块：** 位于表格下方，`<pre>` 标签保留原始格式，全部引用按序号顺序拼接（修正后的 + 未找到的），可一键复制。

**多格式参考文献区块（文献数 >= 3 时输出）：** Tab 页签切换，GB/T 7714 拆分为两个子 Tab：

| Tab | 内容 |
|-----|------|
| **GB/T 7714-2025** | 最新国标（2026年7月1日实施），默认选中 |
| GB/T 7714-2015 | 旧版国标（过渡期兼容） |
| APA | APA 7th |
| MLA | MLA 9th |
| Chicago | Chicago 17th |
| BibTeX | BibTeX 条目 |

如果所有文献原始输入格式一致，则从 Tab 中移除该格式。

**各格式转换规则：**

| 格式 | 作者格式 | 年份格式 | 题名格式 | 期刊格式 | 其他 |
|------|---------|---------|---------|---------|------|
| GB/T 7714-2025 | `张三, 李四`；`Wang L`（外文仅首字母大写） | `(2024)` | 不加引号 | 正体，后加 `[J]` | 文献类型必选；无卷号时不加逗号 |
| GB/T 7714-2015 | `张三, 李四`；`WANG L`（外文全大写） | `(2024)` | 不加引号 | 斜体，后加 `[J]` | 文献类型可选；需引用日期 |
| APA 7 | `Zhang, S., & Li, S.` | `(2024)` | 正体不加引号 | 斜体 | — |
| MLA 9 | `Zhang, San, and Si Li` | `2024.` | 加引号 | 斜体 | — |
| Chicago | `Zhang, San, and Si Li.` | `2024.` | 加引号 | 斜体 | — |
| BibTeX | `{Zhang, San and Li, Si}` | `year = {2024}` | `title = {...}` | `journal = {...}` | — |

> **过渡期策略**：GB/T 7714-2025 尚未正式实施（2026年7月1日），当前同时输出新旧两版格式，标注差异项。用户可根据投稿期刊要求选择使用。

**FUZZY_MATCH 特殊处理：** 修正后文献列显示灰色斜体提示；下载按钮保留原始引用文本；底部纯文本区块顶部插入黄色警告框。

**文件命名规则：** 报告文件 `citation_check_report.html`，全量下载 `参考文献-核查结果.txt`，单条下载 `参考文献-{序号}.txt`

---

## 错误处理 / Error Handling

> **先分「确定性错误」和「临时性错误」再决定要不要重试。** 对确定性错误重试 3 次 = 白等 7 秒 + 用户看到假故障（v3.7.0 修正）。

### 确定性错误 → **不重试**，立即修正或引导

| 错误码 | 含义 | 正确处理 |
|------|------|---------|
| `400 invalid_rule` | 检索式语法错误，或 `rule` 里混入了 `Y` | 按 message 改正；年份搬到 `filter_rule`；**禁止原式重试** |
| `400 invalid_filter_rule` | `filter_rule` 字段代码非法 | 只用 `L/C/Y/TY/LA/IS/IB/MO` |
| `400 invalid_field_type` / `invalid_page_size` / `invalid_sort` | 参数类型或取值越界 | 按提示修参数；PageSize 20–1000 |
| `401 invalid_token` / `missing_token` | consume_token 失效或漏传 email | 重新 `/consume`；补 email 字段 |
| `403 upgrade_required` | 余额账户用了共享密钥 / 代理模式 | 走「Step B2-A」换钥 + 语义化端点 |
| `403 balance_exhausted` | 余额不足 | 告知联系 vipsmart@vipslib.com，附余额与可调用次数 |
| `403 email_not_verified` | 邮箱未验证 | 走 `/register/send-code` → `/register/verify` |
| `404 not_registered` | 账户不存在 | 重新注册（同一邮箱） |

### 临时性错误 → 可重试（指数退避 1s/2s/4s，最多 3 次）

| 情况 | 处理方式 |
|------|---------|
| 服务端 5xx | 重试 3 次，全失败提示"服务暂时不可用，通常 5 分钟内恢复" |
| 网络超时 / 连接重置 | 重试 3 次，全失败提示"请检查网络连接" |
| 429 频率超限 | 按 `retry_after_seconds` 等待后重试；连续 2 次 429 → 降并发到 4 条/批并提示用户 |

### 其它

| 情况 | 处理方式 |
|------|---------|
| 用户输入为空 | 提示"请提供需要核查的参考文献" |
| 引用格式完全无法解析 | 标注"无法解析，请检查格式"，尝试提取关键词检索 |
| Token 过期 | Gateway 自动管理，重新 `/consume` 即可，无需提示用户 |
| 凭证未配置 | 自动触发 Pre-flight 注册流程 |
| 无结果 | 判 `NOT_FOUND` + 给替换建议（见 Step 3） |

---

## 能力边界 / Capability Boundaries

### 支持的功能 / Supported

- 验证参考文献是否真实存在（基于 SmartLib API 联网核查）
- 对作者、年份、期刊名、卷期、页码等字段进行纠错
- 支持 GB/T 7714、APA、MLA、Chicago、BibTeX 五种格式
- 输出结构化 HTML 核查报告（含差异标记、验证链接、统计分析）
- 识别并标注 AI 幻觉生成的虚假文献
- 支持 .bib 文件批量导入

### 不支持的功能 / Not Supported

- **图书 [M] 核查**：全球文献库仅覆盖期刊 / 专利 / 会议 / 学位论文 / 标准，**不含图书**。遇到 `[M]` 引用时，一律输出"⚠️ 图书类文献不在本库核查范围，无法判断真伪（未收录 ≠ 虚构）"，并按能力边界给出人工核验指引（出版社官网 / WorldCat / 国家图书馆 OPAC）。**严禁**把图书题名拿去检索后把命中的期刊论文当成"纠正结果"
- **英文文献全文下载**：本技能不直接提供。外文文献核查时自动复用 global-biblio-base 的十级多渠道 OA PDF 探测流程，结果以标记形式展示（见下方「外文文献全文获取」）
- **实时数据**：文献元数据非实时更新，有数小时至数天的延迟
- **主动联网爬取**：不爬取 Google Scholar、ResearchGate 等外部站点
- **文献查重/查新**：不具备论文查重或科技查新功能
- **自动补全缺失信息**：仅核查与纠错，不主动补充缺失的 DOI/页码等信息

### 外文文献全文获取 / Foreign Literature Full-text Retrieval

核查到的外文文献（API 4 全球文献），自动复用 global-biblio-base 的多渠道下载策略获取 OA PDF。结果以标记形式展示在核查报告中：

| 获取状态 | 标记 | 说明 |
|------|------|------|
| **OA 已下载** | `[全文:已获取]` | 通过十级渠道成功获取 PDF，报告提供下载链接 |
| **OA 在线阅读** | `[全文:在线]` | 可通过 OA 链接在线阅读，但无法自动下载（如 Bronze OA） |
| **付费墙** | `[全文:付费]` | Closed access，需机构订阅或个人购买 |
| **需手动获取** | `[全文:手动]` | 所有渠道均失败，建议通过机构图书馆、科研通或联系作者获取 |
| **未尝试** | `[全文:未获取]` | 无 DOI 或未触发下载流程 |

### 使用限制 / Limitations

| 限制项 / Limit | 说明 / Description |
|------|------|
| **单次核查条数 / Per-query limit** | 建议 ≤50 条，超出时分批处理 / Recommend ≤50, batch if exceeded |
| **请求频率 / Rate limit** | 有频率限制（未公开数值），触发 429 时按 `retry_after_seconds` 等待重试 |
| **Token 有效期 / Token TTL** | Gateway 自动管理，每个 consume_token 60 秒有效，单次使用 |
| **网络依赖 / Network Dependency** | 完全依赖 SmartLib API 和网络连接，离线不可用 |
| **中文期刊全文 / Chinese Full-text** | 仅接口1（中文期刊）支持全文下载链接，接口4（全球检索）仅返回元数据 |
| **图书类文献** | 不在核查范围（见「不支持的功能」） |
| **计费口径差异（重要）** | **配额账户按「次」计费**（每次接口调用 = 1 次，不受返回条数影响）；**余额账户按「条」计价**（详情接口按 `article_ids` 条数计价）。同一批核查在两种账户下的成本并不等价，向用户报成本时必须先确认账户模式 |
| **`/quota` 不可作可用性判据** | 余额账户 `total_remain` 恒为 0 但余额充足。可用性只看 `longterm.mode` + `GET /balance` 的 `balance_remain_yuan` |

### 与 global-biblio-base 的职责区分 / Role Differentiation

| 用户表达 / User Expression | 系统行为 / System Behavior | 区分逻辑 / Rationale |
|------|------|------|
| "查论文"、"找文献"、"检索 XX" | **触发 global-biblio-base** | 明确的检索意图 |
| "这篇文献是真的吗"、"核查引用"、"验证参考文献" | **触发本 Skill** | 引用核查是独立能力 |
| "帮我写论文"、"写作辅助" | **不触发本 Skill** | 论文写作不是引用核查功能 |
| "下载这篇论文的 PDF"（中文期刊） | **触发 global-biblio-base** | 下载是检索的延伸功能 |

---

## 样例演示 / Examples

### 样例一：论文稿件核查 / Sample 1: Paper Draft Verification

以一篇 2026 年最新发表的 EACFM 期刊论文为例，展示完整 5 步流程。完整报告见 `examples/citation_check_paper_draft_sample.html`。

> Full report: `examples/citation_check_paper_draft_sample.html`

**样例论文**：Band, S. S., Qasem, S. N., Mansor, Z., Pai, H.-T., Mehdizadeh, S., Gupta, B. B., & Mosavi, A. (2026). Hybrid machine learning and deep learning models for river suspended sediment load forecasting. *Engineering Applications of Computational Fluid Mechanics*, *20*(1), 2591799.

### 输入：原始引用（APA 格式）

```
Band, S. S., Qasem, S. N., Mansor, Z., Pai, H.-T., Mehdizadeh, S., Gupta, B. B., & Mosavi, A.
(2026). Hybrid machine learning and deep learning models for river suspended sediment load
forecasting. Engineering Applications of Computational Fluid Mechanics, 20(1), 2591799.
https://doi.org/10.1080/19942060.2025.2591799
```

### Step 1 — 解析引用

| 字段 | 提取值 |
|------|--------|
| 作者列表 | Band SS, Qasem SN, Mansor Z, Pai HT, Mehdizadeh S, Gupta BB, Mosavi A（7位作者） |
| 年份 | 2026 |
| 题名 | Hybrid machine learning and deep learning models for river suspended sediment load forecasting |
| 期刊 | Engineering Applications of Computational Fluid Mechanics |
| 卷/期/页 | Vol.20, No.1, 2591799 |
| DOI | 10.1080/19942060.2025.2591799 |

### Step 2 — 联网检索

```
停用词过滤后核心词: hybrid, machine, learning, deep, learning, models, river, suspended, sediment, load, forecasting
去重后取前6: hybrid, machine, learning, deep, models, river

rule        = "T=hybrid machine learning deep models river"
filter_rule = "Y=2026"        ← 年份必须在 filter_rule，写进 rule 会 400 invalid_rule
endpoint    = "/search/global"（全球文献检索）
page_size   = 20
```

### Step 3 — 匹配与比对

API 返回首条记录题名高度匹配、作者全部匹配、年份一致，判定为 `VERIFIED`。

### Step 4 — 差异分析

题名大小写差异属格式差异，不计为错误。作者 APA 缩写 → 完整全名属正常格式转换。DOI 完全一致。**结论：信息一致，无实质性错误。**

### Step 5 — 输出结果

**状态：** `API验证通过` | **差异：** 信息一致，无差异

修正后 APA 格式（与原始引用格式一致）：

```
Band, S. S., Qasem, S. N., Mansor, Z., Pai, H.-T., Mehdizadeh, S., Gupta, B. B., &
Mosavi, A. (2026). Hybrid machine learning and deep learning models for river suspended
sediment load forecasting. Engineering Applications of Computational Fluid Mechanics,
20(1), 2591799. https://doi.org/10.1080/19942060.2025.2591799
```

其他格式导出：

| 格式 | 输出 |
|------|------|
| **GB/T 7714** | Band, Shahab S., Qasem, Sultan Noman, Mansor, Zulkefli, Pai, Hao-Ting, Mehdizadeh, Saeid, Gupta, Brij B., Mosavi, Amir. Hybrid Machine Learning and Deep Learning Models for River Suspended Sediment Load Forecasting[J]. Engineering Applications of Computational Fluid Mechanics, 2026. |
| **MLA 9** | Band, Shahab S., Sultan Noman Qasem, Zulkefli Mansor, Hao-Ting Pai, Saeid Mehdizadeh, Brij B. Gupta, and Amir Mosavi. "Hybrid Machine Learning..." *Engineering Applications of Computational Fluid Mechanics*, vol. 20, no. 1, 2026, 2591799. |
| **Chicago** | Band, Shahab S., Sultan Noman Qasem, Zulkefli Mansor, Hao-Ting Pai, Saeid Mehdizadeh, Brij B. Gupta, and Amir Mosavi. "Hybrid Machine Learning..." *Engineering Applications of Computational Fluid Mechanics* 20, no. 1 (2026): 2591799. |
| **BibTeX** | `@article{band2026hybrid, author = {Band, Shahab S. and ...}, title = {...}, journal = {Engineering Applications of Computational Fluid Mechanics}, year = {2026}, ...}` |

---

## 注意事项 / Notes

- **题名检索优先**：SmartLib 全球检索 API 不支持 `Identifier_DOI` 字段，检索式用「题名核心词 → `rule`」+「年份 → `filter_rule`」。**年份不得写进 `rule`**（余额账户会 400）。DOI 仅用于格式验证和输出链接
- **中文期刊**：优先使用接口1（含全文下载链接），英文文献用接口4；学位/专利/报纸/标准一律接口4（中文库对这些类型返回 0 条）
- **批量处理**：单次核查不超过50条，超出时分批处理；多会话并发务必带 `client_request_id`（余额账户按笔对账靠它）
- **多格式输出**：核查结果同时输出 GB/T 7714-2015、GB/T 7714-2025、APA、MLA、Chicago、BibTeX 六种格式。**修正后主输出始终与原始输入格式一致**。GB/T 7714 拆分新旧两版以兼容过渡期需求。
- **格式保持原则**：修正后文献输出格式 = 原始输入格式。逐条识别并保持一致，不改变用户原始引用的格式体系
- **FUZZY_MATCH处理原则**：不瞎编修正内容，保留原始引用并明确标注存疑，要求用户手动核实
- **隐私保护**：用户上传的内容仅用于本次核查，不做存储
- **验证链接格式**：SmartLib 详情页（通过 Gateway 代理访问）+ 原始数据库来源链接（Source_Link，300+数据库，100%覆盖率）
- **统计分析触发条件**：文献数量 >= 3 时自动输出，少于3条时跳过
- **输出格式**：HTML报告文件，差异内容使用 `[删除]`/`[新增]` 文字标记（CSS样式区分颜色）
- **下载兼容性**：使用 Blob+createObjectURL 实现，兼容 file:// / http:// / https:// 所有环境

---

## 常驻通知转述（v52.2 起）

若任意 SmartLib 网关响应（`/search` 或 `/quota`）的 `notifications` 数组非空，将其中每条的 `text` **原样转述**给用户（含其中的 `url` 链接，用该 `text` 引导用户点击）。**不要改写措辞**，也不要合并多条。

## 版本历史 / Version History


| v4.0.2 | 2026-11-27 | 深度核验更可靠：已撤稿文献即使撤稿库暂未收录，只要来源题名带撤稿标记也会明确提示、不再误判为通过；核验现支持 APA、MLA、Chicago、BibTeX 等更多引用格式；写作任务开始时会说明「按最终字数计费、报价为预估」。 |
| v4.0.1 | 2026-11-27 | 绑定夜猫子后，每次验真会在后台同步记一次权益使用次数（不额外扣费、不影响验真结果），为将来额度用尽后平滑衔接做准备；首次使用照常出结果，报告末尾给一行轻提示。 |
| v4.0.0 | 2026-11-26 | **核验报告现提供原始数据库来源链接**，可对每条文献交叉验证；验真能力可平滑衔接论文写作、检索、查重等更多科研服务，按需取用，不影响原有验真流程。 |
| 版本 | 日期 | 核心变更 |
|------|------|---------|
| v1.0 | 2026-05 | 初次上线：支持GB/T 7714/APA/MLA 格式解析+核查，输出HTML报告 |
| v1.5 | 2026-05 | 新增 BibTeX、Chicago 格式支持；批量核查速度提升（并行处理） |
| v1.6 | 2026-05 | 报告新增多格式切换展示；统计分析更详细 |
| v2.0 | 2026-05 | 计费方式优化，按实际核查次数计费更公平 |
| v2.1 | 2026-05 | 支持外文文献全文获取路径提示；不使用时不扣费 |
| v2.2 | 2026-05 | 安全防护升级，防止第三方盗用配额 |
| v2.3 | 2026-05 | 核查结果附带原始数据库来源链接，可一键跳转核验 |
| v2.4 | 2026-05 | 服务架构升级，响应更稳定 |
| v2.5 | 2026-06 | 核查失败不再消耗配额 |
| v2.6 | 2026-06 | 服务连接优化，检索速度提升 |
| v2.7 | 2026-06 | 注册流程简化，新用户开通更快捷 |
| v2.8 | 2026-06 | 注册赠送次数增加至100次；可订阅套餐最低1000次起 |
| v2.9 | 2026-06 | 新用户引导体验优化，首次使用自动配置 |
| v3.0 | 2026-06 | 检索范围扩展至12亿全球文献 |
| v3.1 | 2026-06 | 技能间联动增强，文献检索与核查无缝衔接 |
| v3.2 | 2026-06 | 文献入口统一，核查链路更顺畅 |
| v3.3 | 2026-06 | 技能名称更新为「参考文献验真、AI引用核查」；优化技能来源追踪 |
| v3.4 | 2026-06 | 技能展示名称与描述优化 |
| v3.5 | 2026-06 | **全面升级至 GB/T 7714-2025**：新增预印本、数据集、地图、档案等文献类型；更新作者姓名格式、文献类型必选等规则；网页/标准/专利著录格式优化 |
| v3.6 | 2026-06 | **新旧国标对比输出**：核查报告同时展示GB/T 7714-2015和2025格式；新增变化说明列标注12项差异编号；兼容过渡期投稿需求 |
| v3.6.3 | 2026-07-19 | 文档对齐 v52.1 统一钱包：Production URL 版本标注更新为 v52.1；/quota 返回字段补充下载额度（download_quota_free / download_reset_at / download_paid_remain / download_remain） |
| v3.6.7 | 2026-10-28 | **修复安装包缺失配置文件导致的运行问题**：恢复 config.json / config.example.json 随包发布，新装用户开箱即用；技能内容与 v3.6.3 一致 |
| v3.6.8 | 2026-11-09 | **新增配套技能推荐**：核查完引用后，AI 会按你的下一步顺手推荐配套技能（继续写论文 / 深挖文献诚信 / 科研技能总路由），不用自己去找装哪个；核查功能本身无变化 |
| v3.7.0 | 2026-11-10 | **新增「深度核验」**：需要查撤稿时，用邮箱一次性绑定夜猫子账号，逐条给出「已撤稿 / 编辑关切 / 未撤稿」，遇到已撤稿文献会顶部红旗警示（¥0.05/条，新用户赠 ¥20，不用不收费）。**购买长期包/充值的用户现在开箱可用**：此前试用额度用完后会提示"升级"却无法继续核查，现已支持余额账户直接使用。**核查结论更可预期**：题名被改动一个词（如 all we need → all you need）也会被指出；引用与库内字段不一致时，明确告诉你"该字段库内为空、无法核验"，不再笼统说"一致"。**新增两项提示**：图书类引用会直接说明"不在核查范围"（不收录 ≠ 虚构）；查不到的文献会附 3–5 条可点验的真实替代文献 |
