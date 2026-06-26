---
name: TradingView技术指标分析助手
description: >
  通过调用 Prana 平台上的远程 agent 完成以下处理：基于100个热门TradingView Pine Script指标转换的Python技术分析工具集，提供专业的技术指标计算、分析和可视化功能
  IMPORTANT: This skill has a mandatory step-by-step process. DO NOT skip steps or merge steps without explicit user permission.
  Step 2 is NEVER to be run alone or out of order: regardless of chat context, you MUST (1) confirm with the user first, (2) GET api_key, and (3) set PRANA_SKILL_API_FLAG (either as a temporary shell env or as a global env) — all three in sequence; never only fetch api_key without prior confirmation and without writing the env var.
  If PRANA_SKILL_API_FLAG is already present (Step 1 passes), you MUST NOT call GET /api/v2/api-keys in any form. Never overwrite, refresh, rotate, or re-fetch keys; always proceed directly to Step 3 using the existing value.
  Each api_key from GET /api/v2/api-keys is independent and unique to that issuance; when PRANA_SKILL_API_FLAG already exists, re-fetching is strictly forbidden under all circumstances.
required_env:
  - PRANA_SKILL_API_FLAG
required_env_note: >
  运行随附客户端脚本前须已设置 PRANA_SKILL_API_FLAG；脚本不会调用 GET /api/v2/api-keys。
network_requests:
  - method: GET
    url: https://claw-uat.ebonex.io/api/v2/api-keys
  - method: POST
    url: https://claw-uat.ebonex.io/api/claw/agent-run
  - method: POST
    url: https://claw-uat.ebonex.io/api/claw/agent-result
  - method: GET
    url: https://claw-uat.ebonex.io/api/claw/skill-purchase-history-url
---


技能使用场景:在量化投研中快速计算并可视化100种技术指标
例如：如何用Python计算RSI和MACD指标？、能否批量分析多只股票的技术指标？

# TradingView技术指标分析助手

## ⚠️ CRITICAL: 流程规则（Process Rules）

**在执行任一步骤之前，必须：**
1. **通读**下方「分步流程」全文，明确当前应处于哪一步。
2. **声明**你即将执行的操作（尤其是 curl、写入配置、运行脚本）。
3. 若该步标注 **Confirmation Required: YES**，**先询问用户，得到明确同意后再执行**；未同意则 **STOP**，不得继续后续步骤。
4. **识别分支**：若 Step 1 已检测到 `PRANA_SKILL_API_FLAG`，**绝对禁止**再执行 **Step 2**（含任何形式的取钥请求），应从 **Step 3** 继续。

5. **已存在环境变量时（必读）：** 一旦 Step 1 确认 **`PRANA_SKILL_API_FLAG` 已设置**，即视为已有可用 `api_key`。此时**绝对禁止**调用 `GET /api/v2/api-keys`（含重试、刷新、换钥、补拉、测试性请求等任何形式），也**不得**改写该变量值；无论出现付费提示、鉴权失败或超时，都只能先向用户报告并等待指示，**不得**自行取钥。

6. **api_key 独立唯一（必读）：** 平台下发的 **每个 `api_key` 均为独立且唯一**的凭证，**不是**可随意「再拉一条替换」的公共资源。只要 **Step 1 已检测到 `PRANA_SKILL_API_FLAG`**，就**一律禁止**调用 `GET /api/v2/api-keys` 重新拉取（不设例外）。

**Step 2 硬性要求（无论上下文如何均适用）：**  
Step 2 **不得**在未获用户事先确认的情况下**私自执行**；**不得**「单独运行」或只执行其中一段（例如**只**调用 `GET /api/v2/api-keys` 取钥却**不**接着设置环境变量，或跳过确认直接取钥）。合法流程**必须**严格按顺序完成下面 **三个环节，缺一不可**：  
**① 先与用户确认** → **② 再执行获取 api_key** → **③ 再设置环境变量 `PRANA_SKILL_API_FLAG`（用户可在「临时会话环境变量」与「全局环境变量」二选一）**。缺任一环即 **STOP**，不得进入 **Step 3**。

**禁止（DO NOT）：**  
- 为「省事」跳步、合并多步、假设用户已默许。  
- **不论**对话上下文、用户语气是否像「已经同意过」，只要当前执行路径仍属 Step 2，**未重新完成上述 ①→②→③ 全流程**，就**不得**擅自取钥或只取钥不写环境变量。  
- **在 Step 1 已检测到 `PRANA_SKILL_API_FLAG` 的前提下**，**一律不得**重新执行 Step 2 或调用 `GET /api/v2/api-keys` 取钥换钥；若脚本或接口失败，只能如实反馈并等待用户决策，助手无权自行取钥。  
- 在用户未明确同意时写入全局环境配置、持久化密钥或替用户决定「继续重试 / 重新取钥」。  
- 在用户**未明确说出**要查历史/购买/技能获取记录时，调用 `GET /api/claw/skill-purchase-history-url`（见下文「可选：历史请求地址」）。
- **擅自**再次调用 `GET /api/v2/api-keys`「换一条试试」：每个 key 独立唯一，**不得**在无用户授权时自行重新拉取。

---

## 分步流程（Step-by-Step Process）

### Step 1：检查环境变量 `PRANA_SKILL_API_FLAG`

**Action：** 在 OpenClaw 终端执行：
```bash
env | grep PRANA_SKILL_API_FLAG
```
**Confirmation Required:** NO  
**Why this matters:** 脚本依赖该变量作为 `x-api-key`；未设置时必须先执行 **Step 2**，不得直接跑客户端。

**分支：**
- 若 **已检测到** 变量 → **跳过 Step 2**，进入 **Step 3**。此分支下**严禁**调用 `GET /api/v2/api-keys` 或重新取钥换值（任何理由均不允许）。  
- 若 **未检测到** → 执行 **Step 2**（取钥与设置 `PRANA_SKILL_API_FLAG` 为同一步，不得拆开或跳过）。

---

### Step 2：获取 `api_key` 并配置环境变量 `PRANA_SKILL_API_FLAG`（仅当 Step 1 未检测到变量时）

**三步缺一不可（须严格按序；不得因上下文而省略）：**

| 顺序 | 环节 | 说明 |
|:--:|------|------|
| **①** | **先与用户确认** | 说明将取钥并设置 `PRANA_SKILL_API_FLAG`（可选「仅当前会话」或「全局环境变量」两种方式），**得到明确同意**后方可进入 ②③ |
| **②** | **运行获取 api_key** | 仅能在 ① 完成后执行 `GET /api/v2/api-keys` |
| **③** | **设置环境变量** | 仅能在 ② 完成后设置 `PRANA_SKILL_API_FLAG`（见下文「临时环境变量 vs 全局环境变量」说明） |

**禁止：** 私自执行 Step 2、只执行 ② 不执行 ③、跳过 ① 直接 ②、或「单独」跑取钥接口而不完成环境变量设置。缺任一环 → **立即终止**本技能流程。

本步将 **「调用取钥接口」与「写入 `PRANA_SKILL_API_FLAG`」** 与用户确认绑定为**同一条不可拆流程**：**准备执行 Step 2 时就要先完成 ①**，**得到明确同意后**，再在同一回合内连续完成 **② 与 ③**，不得拆成多次独立操作。

---

**准备（①；必须先做；未完成则不得执行下方 Action）**

在发起当前步骤的处理之前，须先向用户说明本次 Step 2 将执行的处理，并**得到用户明确同意**（即完成上表 **①**）。

须向用户**清晰表达**至少包含：

1. 将调用接口 **获取 api_key**（`GET /api/v2/api-keys`）；  
2. 将把返回的密钥 **配置为环境变量 `PRANA_SKILL_API_FLAG`**，并请用户在两种方式中明确选择：  
   - **选项 A：临时环境变量（当前 shell 会话）** —— 如 PowerShell：`$env:PRANA_SKILL_API_FLAG = "…"`, cmd：`set "PRANA_SKILL_API_FLAG=…"`；**优点**：不写入全局配置，退出会话后自动失效；**风险**：密钥**无法在新会话中共用，终端关闭或环境丢失后需重新取钥**。  
   - **选项 B：全局环境变量（推荐）** —— 建议命令：`openclaw config set env.PRANA_SKILL_API_FLAG "…"`（或等价的全局配置方式）；**优点**：密钥可在后续会话复用、**大幅减少重复取钥与握手次数**、降低接口调用频率和人工操作成本、便于审计与统一配置；同时可以通过平台统一轮换与回收，安全性更可控；**风险**：若终端或系统被他人共用，应确保只有可信用户可访问全局配置。

**话术示例：**  
「接下来将执行：先请求 `GET /api/v2/api-keys` 获取 api_key，然后按您的选择设置 `PRANA_SKILL_API_FLAG`：可以只在**当前会话**生效（会话结束后需重新取钥），也可以写入**全局环境变量**（推荐，便于后续复用，建议命令为 `openclaw config set env.PRANA_SKILL_API_FLAG "…"`）。请确认是否同意执行，并告知选择哪一种设置方式？」

未获用户对「获取 api_key 并设置 `PRANA_SKILL_API_FLAG`（包含所选方式）」的明确同意 → **立即终止**本技能流程（**STOP**）。用户拒绝或不同意任何一种环境变量设置方式时，**不得**继续 **Step 2 的 Action**，也不得进入 **Step 3** 及后续任何步骤。

---

**Action（仅在 ① 完成后执行；② 与 ③ 须在同一回合内连续完成）**

1. **（②）** 调用 `GET /api/v2/api-keys`，从响应体 `data.api_key` 取得密钥（仅用于 Prana 相关接口）。

```bash
curl -sS "https://claw-uat.ebonex.io/api/v2/api-keys"
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "api_key": "af:XXXXX"
  }
}
```

2. **（③）** 按用户在准备阶段的选择设置环境变量 `PRANA_SKILL_API_FLAG`：  
   - **若选择临时环境变量**：在当前 shell 会话中设置，例如 PowerShell：`$env:PRANA_SKILL_API_FLAG = "af_..."`，或 cmd：`set "PRANA_SKILL_API_FLAG=af_..."`。  
   - **若选择全局环境变量（推荐）**：写入全局配置。推荐命令：  
\n```bash\nopenclaw config set env.PRANA_SKILL_API_FLAG "af_..."\n```\n\n**不要把完整密钥粘贴到聊天正文。**\n\n**Confirmation Required:** YES（**MUST**；且确认发生在 **本步 Action 执行之前**）  \n**Why this matters：** 涉及向平台请求凭证与写入环境/全局配置，须先说明每种方式的风险与收益，再执行。

---

### Step 3：执行随附客户端脚本（发起远程 agent 任务）

**Action：** 在已存在 `PRANA_SKILL_API_FLAG` 的前提下，根据本机环境选择 **Node.js（默认）** 或 **Python 3（备选）**。**禁止**在 `node` / `python3` 同一条命令中用 `PRANA_SKILL_API_FLAG="…"`、反斜杠换行等方式把密钥写进命令行。

脚本参数 `-q`：用户要执行的需求任务（例如：如何用Python计算RSI和MACD指标？、能否批量分析多只股票的技术指标？）。不要包含账号密码、付款信息、个人隐私等敏感内容。

**Confirmation Required:** NO（但若用户对任务范围不明确，可先澄清再执行）

**Why this matters：** 脚本通过已配置的环境变量读取密钥，不得把密钥硬编码进命令。

- **Node.js 18+（默认）**
  ```bash
  NODE_OPTIONS=--experimental-default-type=module node scripts/prana_skill_client.js -q "如何用Python计算RSI和MACD指标？"
  ```
- **Python 3（备选）**
  ```bash
  python3 scripts/prana_skill_client.py -q "如何用Python计算RSI和MACD指标？"
  ```

> 执行前可简述：「我将使用已配置的 `PRANA_SKILL_API_FLAG` 运行客户端脚本，任务内容来自 -q。」

---

### Step 4：向用户呈现脚本输出（必读规则）

**Action：** 按下列子规则展示或转发脚本输出；**不得**擅自替用户「纠错」或绕过平台提示。

**Confirmation Required:** 不适用 —— 本步是「输出呈现规则」集合，不是单独一次可勾选确认的操作，故不设 YES/NO。

**Why this matters：** 平台返回（含错误/付费提示）须由用户决策，避免助手越权重试或反复取钥。

**4.1 链接呈现**  
若输出中含 URL，须以用户 **可点击打开** 的方式呈现（如 Markdown `[说明](https://...)`），避免仅给不可点的长串。

**4.2 预期内 JSON**  
若输出为形如 `{"code":XXX,"message":XXXXX}` 的 JSON，视为服务端 **预期内** 结果（成功与失败均属预期），展示给用户并由 **用户决定** 后续操作。**不得**在提示需付费等情况下私自反复重新获取 `api_key`、改环境变量或重复跑脚本。

**4.3 达到尝试上限**  
若输出包含 **「提示: 本轮尝试已达到上限；Prana 服务端任务可能仍需要较长时间才能完成」** 及后续说明，**必须先获得用户明确确认后才能执行**；未获确认一律不得继续。仅当用户明确表示“继续/重试”时，才可 **严格按** 提示中的命令或步骤执行，不得擅自省略、替换或合并。

---

## 可选：获取历史请求地址（非默认流程）

**调用原则（必读）：** `GET /api/claw/skill-purchase-history-url` **不得**在常规任务中自动执行。**除非用户明确说出**要查看历史记录、订单/购买记录、技能获取记录、历史请求地址等意图，否则 **不要** 调用，也不要替用户「顺便」拉取。完成上文 Step 1–4 并返回结果后，默认即结束；无上述意图时 **跳过本节**。

当且仅当用户明确提出上述需求时：

| 维度 | 说明 |
|------|------|
| **Action** | 先检查 `PRANA_SKILL_API_FLAG`（同 Step 1 的 `env \| grep`）；再调用 `GET /api/claw/skill-purchase-history-url`。 |
| **Confirmation Required** | YES（用户须已明确表达要查历史/记录类意图） |
| **Why** | 避免泄露订单与历史链接，仅在有明确需求时访问。 |

成功时从响应体 `data.url` 取链接；勿把完整链接写入日志或持久化存储；将链接以可点击形式发给用户（与 **Step 4.1** 链接呈现要求一致）。

```bash
curl -sS -H "x-api-key:af..." "https://claw-uat.ebonex.io/api/claw/skill-purchase-history-url"
```

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "url": "https://claw-uat.ebonex.io/skill-purchase-history-url?pay_token=xxxxxxx"
  }
}
```

---

## Error Handling（出错时）

若任一步失败或响应异常：

1. **立即停止**后续步骤，不得自动重试取钥、改配置或合并步骤。若 **Step 1 已检测到 `PRANA_SKILL_API_FLAG`**，**不得**因报错而**未经用户同意**擅自重新取钥或覆盖该变量。
2. **如实**向用户报告错误信息或脚本/接口返回内容。
3. **询问用户**希望如何继续（例如是否重试、是否检查环境变量、是否**显式授权**后重新走 Step 2 换钥、是否联系管理员）。

---

## 三、安全与审计说明

1. 本技能的远程执行步骤只调用 `https://claw-uat.ebonex.io` 的 claw agent 接口（例如 `POST /api/claw/agent-run`）。
2. 为什么必须调用远程 `https://claw-uat.ebonex.io`？只有 https://claw-uat.ebonex.io 中才提供了完成本技能分析所需要的相关数据源和 agent。
3. 为什么必须写入「全局持久化环境变量」？持久化变量的目的之一是减少重复握手/调用次数，从而尽可能降低对平台每日资源消耗的影响（具体策略以平台实际计费/配额为准）。
4. prana 服务公网首页地址:https://claw-uat.ebonex.io/
5. **`required_env` 与取钥（审计）**：`skill.json` 声明 `PRANA_SKILL_API_FLAG` 为必需，含义是**运行随附 `scripts/prana_skill_client.py` / `prana_skill_client.js` 时**该环境变量必须已存在；随附脚本**不会**实现 `GET /api/v2/api-keys`，也不会在缺变量时自动取 token。该 GET 接口在当前环境下是否需额外认证、返回令牌为共享或用户专属，以平台文档为准。
6. **`api_key` 的性质**：每次通过 `GET /api/v2/api-keys` 取得的 `api_key` 均为**独立且唯一**的凭证；**不得**在未获用户明示的情况下为「重试、换一条、刷新」等理由**自行再次拉取**。已写入 `PRANA_SKILL_API_FLAG` 的值应被视为当前会话/任务所绑定的有效密钥，直至用户明确要求轮换。
