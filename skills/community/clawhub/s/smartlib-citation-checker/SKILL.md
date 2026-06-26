---
name: smartlib-citation-checker
version: 3.6
homepage: https://www.vipslib.com
description: 核查用户提交的论文稿件或AI生成参考文献是否真实，防止AI幻觉。基于SmartLib API，输出HTML核查报告（含差异标记、验证链接、统计分析）。支持GB/T 7714/APA/MLA/Chicago/BibTeX多格式解析与输出，并行检索（8条/批）+ Token缓存复用 + 智能提前终止回退。✨ 亮点：核查结果附带原始数据库来源链接（覆盖300+数据库，如Scopus/WoS/EI/PubMed等，覆盖率100%），可交叉验证文献真实性。全程自动化：首次使用自动注册开通（免费100次/月），配额自动消耗，用尽后引导充值续费。触发词：核查引用、验证参考文献、检查引用、查引用、论文引用检查、AI引用核查、参考文献真假、文献核实、引用验证、引用格式检查、AI论文引用检查、参考文献审计、论文参考文献是真的吗、AI写的论文引用靠谱吗、ChatGPT引用核查、verify citation、check references。
  Production URL: read from global-biblio-base/config.json → SMARTLIB_GATEWAY_URL (Gateway v47, version 67)
displayName: 参考文献验真、AI引用核查（12亿全球文献，有原始文献链接可核验）
metadata:
  openclaw:
    emoji: "✅"
    requires:
      env:
        - SMARTLIB_GATEWAY_SECRET
        - SMARTLIB_GATEWAY_URL
    envVars:
      - name: SMARTLIB_GATEWAY_URL
        required: true
        description: SmartLib Gateway 服务地址
      - name: SMARTLIB_GATEWAY_SECRET
        required: true
        description: SmartLib Gateway API 密钥
      - name: SMARTLIB_EMAIL
        required: false
        description: 注册邮箱（首次使用时自动注册，与 literature-search 共享凭证）
agent_created: true
---

# SmartLib 文献引用核查与纠错 / Citation Authenticity Checker

> 中文 / Chinese | [English below each section]

本技能基于 `global-biblio-base` 的文献检索能力，对用户提交的论文稿件或文本引用进行核查与纠错，最终输出一个结构化的 HTML 核查报告文件。**与 global-biblio-base 共享凭证和配额。**

> This skill uses `global-biblio-base` to verify academic references and detect errors, generating a structured HTML report. **Shares credentials and quota with global-biblio-base.**

---

## ⚡ 启动前必须执行 / Pre-flight Checklist（每次调用都必须执行）

### Step A：凭证自动检测 & 注册 / Auto Credential Check & Registration

> ## ⚠️ 强制规则 — 必须先询问邮箱
> 1. **执行任何操作前，必须先询问用户邮箱地址**
> 2. 禁止使用 global-biblio-base/config.json 中预填的邮箱（即使存在且非 null）
> 3. 禁止自动生成邮箱（如 `user@example.com`、`auto@xxx.com` 等）
> 4. 用户未提供邮箱 → 停止执行，回复：
>    "请提供您的邮箱地址以注册 SmartLib 文献引用核查服务（新用户免费 100 次/月）"
> 5. 只有用户明确输入邮箱后，才能调用 /register 或 /quota
>
> ## 邮箱识别自动化
> 当用户消息中出现以下模式时，自动提取邮箱 → 无需再次询问：
> - 明确的邮箱地址（包含 @ 符号的完整地址，如 `xxx@xxx.xxx`）
> - "我的邮箱是 xxx" / "email: xxx" / "用 xxx 注册" / "邮箱 xxx"

本技能与 `global-biblio-base` **共享凭证和配额**。每次执行时按以下流程处理：

> Shares credentials and quota with global-biblio-base. Auto-detection flow:

```
① 先读取 global-biblio-base 技能目录下的 config.json
   Read config.json from global-biblio-base skill directory first

② 检查 SMARTLIB_EMAIL 是否已配置
   Check if SMARTLIB_EMAIL is already configured
  ├── 已配置 → 进入 Step B (配额检查) / Already configured → proceed to Step B
  │
  └── 未配置 → 自动注册流程 / Auto-registration:
        ├── ① 展示核查计划 + 询问邮箱（一句话）:
        │      "📋 我将核查您的参考文献真实性... 首次使用需绑定邮箱（免费 100 次/月，仅用于配额管理），请输入邮箱即可开始:"
        │      用户输入 → 写入 global-biblio-base 的 config.json
        │
        ├── ② 调智能网关注册（无需验证码）:
        │     POST {SMARTLIB_GATEWAY_URL}/register
        │     Headers: {"Authorization": "Bearer {SMARTLIB_GATEWAY_SECRET}"}
        │     Body: {"email": "{用户邮箱}"}
        │
        ├── 成功 (201/200) → Gateway 返回配额信息
        │     提示: "✅ 注册成功！本月免费 100 次，可立即使用。确认邮件已发送（邮箱验证仅充值时需要，现在不验证也能用）。"
        │     追加引导: "请把您的参考文献发给我，现在就可以开始核查——"
        │     → 继续 Step B 配额检查 → 核查
        │
        └── 失败 → 提示原因 (服务暂不可用 / 网络错误等) → 终止
```

> **注意**：注册无需验证码，极速完成。**注册后即可立即使用**，邮箱验证可选（仅充值时需验证）。

### Step B：配额检查 / Quota Check

```
凭证就绪后, 调网关查询配额:
  GET <SMARTLIB_GATEWAY_URL>/quota?email=<SMARTLIB_EMAIL>
  Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}

  返回字段: total_remain, email_verified, plan
  （完整返回: user_id, email, plan, trial_total, trial_used, trial_remain, paid_total, paid_used, paid_remain, paid_expires_at, total_remain, email_verified）

  如果返回 404 "not_registered" → 用户可能已被重置/删除
    → 提示: "检测到您的账户需要重新绑定，正在自动重新注册..."
    → 跳回 Step A ②（调 /register 重新注册，使用同一邮箱）
    → 注册成功后继续配额检查

  total_remain > 20 → 静默进入核查
  total_remain 5-20 → 尾部轻提示: "📊 本月剩余 {n} 次"
  total_remain 1-5  → 警告: "⚠️ 接近用尽（剩余 {n} 次），回复「充值」查看套餐（数字 1-4 选）"
  total_remain 0    → 拒绝服务，提示充值（见下方配额耗尽处理章节）

  额外检查:
```

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

每次调用计费接口前，必须先调 `/consume` 获取 token，再用 token 调 `/search`：

```
① POST <SMARTLIB_GATEWAY_URL>/consume
   Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
   Body: {"email": "<SMARTLIB_EMAIL>", "skill_source": "smartlib-citation-checker"}
   → 获取 consume_token

② POST <SMARTLIB_GATEWAY_URL>/search
   Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
   Body: {"email":"...", "consume_token":"...", "api_path":"...", "api_body":{...}}
   → Gateway 验证 token → 代理转发 → 返回检索结果
```

> Call `/consume` → `/search` for **each** billable API call. Token single-use, 60s TTL.

**🛡️ Token 绑定调用链 / Token-Bound Call Chain:**

> **强制安全机制 — 不可绕过：**
> 每次调用计费接口前，必须通过 `/consume` 获取 `consume_token`，然后将 token 传给 `/search` 代理端点。
> Gateway 验证 token 签名 + 有效期 + 防重放后才转发检索请求。
> Token 由 GATEWAY_SECRET 签名，AI 无法伪造。无有效 token 则 /search 直接 401。
>
> **调用流程 / Call Flow:**
> ```
> 1. POST /consume {"email":"...", "skill_source":"smartlib-citation-checker"} → 返回 consume_token
> 2. POST /search {"email":"...", "consume_token":"...", "skill_source":"smartlib-citation-checker", "api_path":"...", "api_body":{...}}
>    → Gateway 验证 token → 代理转发到检索 API → 返回检索结果
> ```
>
> **注意**：每个 consume_token 只能使用一次（防重放），有效期 60 秒。每次检索 API 调用前都需要先 /consume 获取新 token。

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
2. 用户说 "充值" "续费" "购买"

### 套餐列表

| 套餐 | plan key | 价格(元) | 配额 | 说明 |
|------|----------|---------|------|------|
| 体验包 | `trial` | 9.90 | 1000 次 | 限购 1 次 |
| 基础月付 | `basic` | 29.00 | 5000 次/月 | 个人用户 |
| 进阶月付 | `pro` | 99.00 | 20000 次/月 | 轻度团队 |
| 专业月付 | `enterprise` | 299.00 | 100000 次/月 | 重度使用 |

> **plan key**：调用 `/api/pay/create` 时传 `trial`/`basic`/`pro`/`enterprise`。金额单位为**元**（非分）。

### 支付流程（对话交互，数字选套餐）

全部在对话中完成，用户只需回复数字：

```
配额耗尽/用户说"充值" →
    ↓
⓪ 展示套餐卡片（show_widget），用数字①②③④标注:
   ① 体验包 ¥9.90 — 1,000 次/月
   ② 基础月付 ¥29.00 — 5,000 次/月
   ③ 进阶月付 ¥99.00 — 20,000 次/月 [推荐]
   ④ 专业月付 ¥299.00 — 100,000 次/月
   用户回复数字 (如 "3")
    ↓
   映射: "1"→trial, "2"→basic, "3"→pro, "4"→enterprise
    ↓
① 调 Gateway 生成订单:
  POST {SMARTLIB_GATEWAY_URL}/api/pay/create
  Headers: {"Authorization": "Bearer {SMARTLIB_GATEWAY_SECRET}"}
  Body: {"plan": "basic", "amount": 29.00, "quota": 5000, "email": "{SMARTLIB_EMAIL}"}

  返回: {"code_url": "weixin://...", "out_trade_no": "WB...", "amount": 29.00, "plan": "basic", "quota": 5000}
    ↓
② 生成带订单信息的二维码 HTML 页面，用 preview_url 在对话内展示:

  **页面必须包含：套餐名称、金额、配额标签、二维码、订单号**
  用 qrcode.js CDN 将 code_url 渲染为二维码。
  样式参考：渐变紫色背景 + 白色卡片 + 居中布局。

  ⚠️ 不要在卡片内容中显示用户邮箱

    ↓
③ 轮询支付状态:
  GET {SMARTLIB_GATEWAY_URL}/api/pay/status?out_trade_no=xxx
  (间隔 3s 轮询,最多轮询 20 次 ≈ 60s，超时提示重新发起)

  支付成功时返回:
  {"status":"paid", "auto_recharged":true, "quota_remain":5000, "quota_total":5100, "quota_used":100}
    ↓
④ 对话中通知结果:
  "✅ 支付成功! 已自动充值 5000 次，当前剩余 5000 次。"
    ↓
  自动重试上次中断的核查
```

### 为什么不需要 /recharge？
支付回调 (`/api/pay/notify`) 由微信支付服务器直接通知 Gateway，Gateway 在回调中**同一事务内**完成标记订单 paid + 累加配额。`/api/pay/status` 查询到 paid 时配额已到账，无需额外操作。

### 安全机制
- 网关通过 `out_trade_no` UNIQUE 索引防重复充值
- 二维码 5 分钟有效, 超时需重新发起
- `/api/pay/status` 为公开端点（无需 Bearer Token），可直接轮询
- `SMARTLIB_GATEWAY_SECRET` 仅供后端调用, 不在对话中输出
- ⚠️ 生成的支付 HTML 页面上**禁止显示用户邮箱**，仅显示套餐信息

---

## 🔒 配额耗尽处理 / Quota Exhaustion

所有用户享有以下免费体验权益：

> All users get the following free trial:

| 状态 | 行为 |
|------|------|
| **配额充足** (>0) | 完整展示所有核查结果（含差异标记、验证链接、统计分析、HTML 报告） |
| **配额耗尽** (=0) | Gateway 返回 429，**拒绝服务**，直接提示充值 |

配额耗尽后的提示格式：

```
⚠️ 您的 SmartLib 检索配额已用尽（0/100次）。

当前配额不支持发起新的文献核查请求。请充值后继续使用。

> 💰 充值套餐：
> 体验包：¥9.90 / 1000次
> 月付基础：¥29.00 / 5000次/月
> 月付进阶：¥99.00 / 20000次/月
> 月付专业：¥299.00 / 100000次/月
> 回复「充值」查看套餐（回复数字 1-4 选择），支付后立即生效。
```

**重要**：配额耗尽后，**所有核查请求一律拒绝**，不展示任何部分结果。用户需先充值恢复配额。

---

## 输出规范 / Output Standards

**每次核查结果末尾必须展示配额状态：**

```
📊 本次消耗 {n} 次 | 剩余 {remain} 次 (共 {total} 次/月)
```
或接近耗尽时：
```
⚠️ 剩余 3 次 (共 100 次/月)，回复「充值」选套餐
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
| **原始来源交叉验证 / Cross-Source Verification** | 提供 Scopus/WoS/EI/PubMed 等 300+ 数据库的原始来源链接，多维度交叉验证文献真实性，覆盖率 100%，平均 4.75 个链接/篇 |
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
GB/T 7714-2015: [1] 张三, 李四. 深度学习综述[J]. 计算机学报, 2024, 45(3): 123-145.
APA: Zhang, S., & Li, Y. (2024). Deep learning survey. 计算机学报, 45(3), 123-145.
MLA: Zhang, San, and Si Li. "Deep Learning Survey." 计算机学报, vol. 45, no. 3, 2024, pp. 123-145.
Chicago: Zhang, San, and Si Li. 2024. "Deep Learning Survey." 计算机学报 45 (3): 123-145.
BibTeX: @article{zhang2024deep, author = {Zhang, San and Li, Si}, ...}
```

**格式识别 → 表头标注规则**：HTML 报告中的两列均需在表头标注格式名——`原始参考文献 (APA)` 和 `修正后文献 (APA，与原始格式一致)`。

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
| 1 | 题名关键词 + 年份检索 | 题名可提取（所有文献） |
| 2 | 放宽年份检索（仅题名关键词） | 优先级1无结果时 |
| 3 | 提取DOI做格式校验 | DOI存在时作为辅助验证 |

**检索表达式构建：**

```python
# 优先级1: 题名核心词 + 年份（去停用词后取前6个词）
stopwords = {"a", "an", "the", "in", "of", "for", "and", "on", "to", "is", "by", "with", "using", "based", "from"}
words = [w for w in title.lower().replace(",", "").replace(":", "").split() if w not in stopwords][:6]
rule = f"(T={' '.join(words)}) AND Y={year}"

# 优先级2: 仅题名关键词（去掉年份限制，提高召回）
words_loose = [w for w in title.lower().replace(",", "").replace(":", "").split() if w not in stopwords][:5]
rule = f"T={' '.join(words_loose)}"
```

**接口选择：** 中文期刊优先用接口1（中文期刊检索），英文论文/学位论文/专利用接口4（全球文献检索）。

**检索参数：**

```json
{
  "Rule": "<检索表达式>",
  "PageIndex": 1,
  "PageSize": 10,
  "Sort": 1
}
```

### Step 3: 匹配与比对 / Match & Compare

**匹配度计算：**

| 因素 | 权重 | 说明 |
|------|------|------|
| 题名相似度 | 60% | 使用共同词比例算法，>50%认为匹配 |
| 作者匹配 | 25% | 至少一位作者匹配，且顺序基本一致 |
| 年份匹配 | 15% | 年份完全一致 |
| DOI辅助验证 | 加分项 | DOI匹配可增加置信度 |

**匹配结果分类：**

| 结果 | 状态码 | 说明 | 验证链接 |
|------|--------|------|---------|
| 验证通过 | VERIFIED | 找到高度匹配的文献，信息准确 | 提供（SmartLib + 多数据库原始来源） |
| 存在差异 | MISMATCH | 找到匹配文献，但部分字段有差异 | 提供（SmartLib + 多数据库原始来源） |
| 未找到 | NOT_FOUND | 未在数据库中找到匹配的文献 | 不提供 |
| 疑似匹配 | FUZZY_MATCH | 找到疑似结果，需人工确认 | 不提供（标注存疑） |

### Step 4: 差异分析 / Diff Analysis（针对 MISMATCH）

逐字段对比原始引用与数据库记录：

| 字段对比 | 差异类型 | 纠错建议 |
|---------|---------|---------|
| 作者姓名 | 拼写错误、缺少中间名、顺序错误 | 提供正确作者列表 |
| 年份 | 年份错误 | 提供正确年份 |
| 期刊名 | 缩写不规范、全称/简称混淆 | 提供标准期刊名 |
| 卷期号 | 卷号/期号错误 | 提供正确卷期 |
| 页码 | 起止页码错误 | 提供正确页码范围 |
| 题名 | 打字错误、遗漏词汇 | 提供正确题名 |
| DOI | DOI错误或缺失 | 提供正确DOI |

### Step 5: 生成 HTML 核查报告 / Generate HTML Report

最终输出为一个完整的 HTML 文件，预览窗口自动打开，并交付给用户下载保存。

**报告结构：**

```
┌─────────────────────────────────────────────────────────┐
│ 报告头部：标题 + 核查时间 + 汇总徽章（总数/差异/存疑）    │
├─────────────────────────────────────────────────────────┤
│ 核查结果表格（6列）                                      │
│ # / 状态 / 原始参考文献 (格式名) / 修正后文献 / 主要差异 / 验证 │
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

**多格式参考文献区块（文献数 >= 3 时输出）：** Tab 页签切换（GB/T 7714 | APA | MLA | Chicago | BibTeX），默认选中第一个 Tab。如果所有文献原始输入格式一致，则从 Tab 中移除该格式。

**各格式转换规则：**

| 格式 | 作者格式 | 年份格式 | 题名格式 | 期刊格式 |
|------|---------|---------|---------|---------|
| GB/T 7714 | `张三, 李四`；`Wang L` | `(2024)` | 不加引号 | 斜体，后加 `[J]` |
| APA 7 | `Zhang, S., & Li, S.` | `(2024)` | 正体不加引号 | 斜体 |
| MLA 9 | `Zhang, San, and Si Li` | `2024.` | 加引号 | 斜体 |
| Chicago | `Zhang, San, and Si Li.` | `2024.` | 加引号 | 斜体 |
| BibTeX | `{Zhang, San and Li, Si}` | `year = {2024}` | `title = {...}` | `journal = {...}` |

**FUZZY_MATCH 特殊处理：** 修正后文献列显示灰色斜体提示；下载按钮保留原始引用文本；底部纯文本区块顶部插入黄色警告框。

**文件命名规则：** 报告文件 `citation_check_report.html`，全量下载 `参考文献-核查结果.txt`，单条下载 `参考文献-{序号}.txt`

---

## 错误处理 / Error Handling

| 情况 | 处理方式 |
|------|---------|
| 用户输入为空 | 提示"请提供需要核查的参考文献" |
| 引用格式完全无法解析 | 标注"无法解析，请检查格式"并尝试提取关键词检索 |
| API调用失败 | 静默重试3次（指数退避 1s/2s/4s），仍失败则提示"网络问题，请稍后重试" |
| Token过期 | Gateway 自动管理 Token 刷新，无需处理 |
| API凭证未配置 | 自动触发 Pre-flight 注册流程 (调 gateway /register) |
| 请求频率超限 (429) | 等待 5 秒后自动重试，若连续 429 提示降速 |
| 服务端错误 (5xx) | 自动重试 3 次，全部失败后提示"服务暂时不可用，通常 5 分钟内恢复" |
| 无结果 | 标注为 NOT_FOUND，提示用户核对原始引用 |
| 网络超时 | 自动重试 3 次，全部失败后提示"请检查网络连接" |

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
| **请求频率 / Rate limit** | 有频率限制（未公开数值），触发 429 时自动等待重试 |
| **Token 有效期 / Token TTL** | Gateway 自动管理，每个 consume_token 60 秒有效，单次使用 |
| **网络依赖 / Network Dependency** | 完全依赖 SmartLib API 和网络连接，离线不可用 |
| **中文期刊全文 / Chinese Full-text** | 仅接口1（中文期刊）支持全文下载链接，接口4（全球检索）仅返回元数据 |

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

检索规则：(T=hybrid machine learning deep models river) AND Y=2026
检索接口：接口4（全球文献检索）
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

- **题名检索优先**：SmartLib 全球检索 API 不支持 `Identifier_DOI` 字段，请使用题名核心词 + 年份构建 Rule 进行检索。DOI 仅用于格式验证和输出链接
- **中文期刊**：优先使用接口1（含全文下载链接），英文文献用接口4
- **批量处理**：单次核查不超过50条，超出时分批处理
- **多格式输出**：核查结果同时输出 GB/T 7714、APA、MLA、Chicago、BibTeX 五种格式。**修正后主输出始终与原始输入格式一致**
- **格式保持原则**：修正后文献输出格式 = 原始输入格式。逐条识别并保持一致，不改变用户原始引用的格式体系
- **FUZZY_MATCH处理原则**：不瞎编修正内容，保留原始引用并明确标注存疑，要求用户手动核实
- **隐私保护**：用户上传的内容仅用于本次核查，不做存储
- **验证链接格式**：SmartLib 详情页（通过 Gateway 代理访问）+ 原始数据库来源链接（Source_Link，300+数据库，100%覆盖率）
- **统计分析触发条件**：文献数量 >= 3 时自动输出，少于3条时跳过
- **输出格式**：HTML报告文件，差异内容使用 `[删除]`/`[新增]` 文字标记（CSS样式区分颜色）
- **下载兼容性**：使用 Blob+createObjectURL 实现，兼容 file:// / http:// / https:// 所有环境

---

## 版本历史 / Version History

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
