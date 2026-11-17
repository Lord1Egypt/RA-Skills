---
name: rea-cn-paid
slug: rea-cn-paid
displayName: REA逆向工程审计包·国产适配（付费版）
version: 1.2.3
summary: >-
  REA 逆向工程审计包·国产适配（付费版）：把 170 个 MCP 逆向分析工具适配到中文 LLM 环境，
  用于原生/托管/Electron·JS/打包产物/固件/浏览器目标的研究学习、安全审计与版本比对，按调用量计费 ¥1.9/次（24 小时内不限次）。
license: 自有商业授权（见 LICENSE.md；上游引擎为 MIT，见 engine-LICENSE-MIT.md）
tags: [逆向工程, 安全审计, 国产大模型适配]
pricing:
  model: per_call
  amount_fen: 190
description: >-
  REA逆向工程审计包·国产适配（付费版）。基于 rea-agents@6.4.0（170 个 MCP 工具）的纯英文逆向分析引擎，
  配套英汉对照表、工具调用契约与国内大模型适配，使引擎可在中文 LLM 环境下稳定运行。
  用于原生/托管/Electron·JS/打包产物/固件/浏览器目标的研究学习、审计、版本比对、反编译与重建验证。
  不适用于普通源码仓库的常规架构分析。调用引擎前需完成付费凭证验证。
metadata:
  tool_count: 170
  cn_adapt_version: "1.0"
  product: "rea-cn"
  price: "1.9"
  payment_model: "per_call_24h"
---

# ⚠️ 免责声明（务必先读）

> **本技能仅用于研究学习与安全审计（如自有软件的健壮性审计、遗留产物的可维护性评估、版本差异比对等）。**
> **不可用于破解、绕过技术保护措施、未经授权的逆向或任何违反法律法规的用途。**
> **用户如将本技能用于上述禁止用途，一切法律责任与后果由使用者自行承担，本技能提供方不承担任何法律责任与后果。**
>
> 本声明仅为使用提示与责任边界声明，**未写入引擎本身**；用户在遵守法规的前提下可自行决定如何使用其合法拥有的目标。

---

# REA逆向工程审计包·国产适配（付费版）

REA（Reverse Engineer Anything）以 MCP 服务器形式暴露 **170 个工具**，
桥接 Ghidra / Hopper / IDA / JADX / JEB / adb / apktool / Binwalk / Unblob 等后端。
本包是其**中文 + 国内大模型**环境下的适配版：引擎保持原版纯英文不变，
配套本地化文档保证中文 LLM 不会因"把工具名翻译成中文"而调用失败。

> 引擎是完全离线、不联网的分析中间件；它会调用你本机/服务器上已安装的 provider（如 Ghidra）。
> 本技能不内置任何受保护目标的破解能力，只做"读取—分析—比对—出证据"的研究性工作。

---

## 0. 付费契约（最高优先级 · 必须严格执行）

本技能的**完整引擎能力为付费功能**，由官网后端网关统一授权。价格 **¥1.9 / 次**，
按 SkillHub 单次付费规则：**一次支付 = 付费履约后 24 小时内不限次使用（免验证），到期需重新付费**。

### 0.1 付费发起时机

**在「真正调用引擎之前」发起付费；在此之前的一切均为免费预览。**

正确顺序（不可颠倒）：

1. **免费预览**（不触碰付费）：向用户说明分析方案、将要用到的工具清单（中文名 + 英文名）、
   从 `references/glossary-zh-en.md` 引用相关术语说明、提示需要自备的 provider（见 `references/providers.md`）。
2. 用户确认要执行真实分析 → **此时才发起付费**。
3. 付费凭证验证通过（网关返回已支付，响应体含 `expires_at` 到期时间）→ 才允许交付引擎并通过 MCP 调用。
4. 输出中文结论，并明确区分「观测 / 推断 / 未知」（见 `references/obligation-ledger.md`）。

> **24 小时规则（幂等窗口）**：本地 `engine/.entitlement.json` 登记后 **24 小时内**重复使用**免验证、不重复扣费**；
> 超过 24 小时，`run-mcp.mjs` 将拒绝启动（exit 65），须重新走一次 ¥1.9 付费。网关侧对超过 24 小时的旧订单
> 一律返回 `410 ORDER_EXPIRED`，杜绝"一个订单号无限续期"。

### 0.2 付费流程（X402 · 推荐走脚本，三步）

> **标准做法：全程使用 `scripts/pay-gate.mjs`**（本包内置的实质性付费代码，已封装下述 HTTP 协议、
> 支付码提取、下载、SHA256 校验、解压与凭证登记；本地已验证全链路可运行）。
> 直接手写 HTTP 请求时，按下述协议执行。

```
node scripts/pay-gate.mjs [--query "<分析目标简述>"]   # 第 1 步：发起付费（402）
node scripts/pay-gate.mjs --resume <outTradeNo>        # 第 3 步：支付完成后履约
node scripts/pay-gate.mjs --status                     # 查询解锁状态（0=已解锁/44=未解锁/45=已过期）
```

- **第 1 步**：执行 `node scripts/pay-gate.mjs`（或直接 POST `https://www.ontoagent.net/rea402/api/resource`，
  Body `{"query": "<本次分析目标简述>"}`，不带单号）。
  - 网关返回 **HTTP 402**，响应头含 `WeixinPay-Required`（payment_code）与 `X-Out-Trade-No`，响应体含免费 `preview` 字段。
  - 脚本以 **exit 42** 退出并输出 JSON：`{paymentCode, outTradeNo, amount, preview, agentInstructions}`。
  - **先向用户展示这个免费的 preview**，再引导付款。展示 preview 不属于绕过付费。
  - 若本地 entitlement 已过期（超 24h），输出中带 `renew: true` 与 `previous_expired_at`，此时同样走新的一次付费。
- **第 2 步 · 唤起支付（先做前置检查）**：
  - 调用 `weixinpay_pay` 插件前，**先确认该插件已安装且可用**。
  - 若插件未安装/未启用：**明确告知用户原因并停止**，不得静默失败，更不得跳过支付直接产出结果。
  - 用户取消或支付失败：保留 `outTradeNo` 以便重试，**不得重复建单**。
- **第 3 步**：执行 `node scripts/pay-gate.mjs --resume <outTradeNo>`
  （等价于带 `X-Out-Trade-No` 头重发同一 POST）。
  - 网关查单确认支付后返回 HTTP 200，含**签名下载地址**（`download_url`，10 分钟有效）、`engine_sha256`
    与 `expires_at`（权益到期时间 = 履约时刻 + 24h）。
  - 脚本自动：准备引擎 zip（包内 base64 分片重建，或从网关下载）→ **SHA256 校验**
    （与包内 `config/cn-config.json` 的 `paid.engineZipSha256` 比对）→ 解压为 `engine/`
    → 登记 `engine/.entitlement.json`（含 `expires_at`）→ 以 **exit 0** 退出。
  - 已付费用户可用 `--refresh` 强制重新获取引擎（本地 zip 损坏/丢失时；权益仍有效则免再付费）。
  - 若网关返回 **410**（`ORDER_EXPIRED` 订单超 24h / `REFUNDED` 已退款）：脚本以 **exit 45** 退出，
    并指引重新发起一次 ¥1.9 付费——单次付费不提供无限续期。

### 0.3 实质性付费代码清单（本包的付费改造就是这些文件）

| 文件 | 职责 |
|---|---|
| `scripts/pay-gate.mjs` | **付费闸唯一入口**：402 发起 / 支付码交接 / 履约 / 引擎准备（分片重建或网关下载）/ SHA256 校验 / 解压 / 凭证登记。退出码：0 成功、42 需支付、43 未支付、44 未解锁、**45 已过期需续费** |
| `scripts/lib/engine-assets.mjs` | 资产共享模块：SHA256 校验、四路兜底解压（tar/unzip/PowerShell/python）、entitlement 读写与 **24h 时效三件套**（`entitlementStatus`/`entitlementExpiresAt`/`entitlementValid`）、**Ed25519 验签**（`verifyEntitlementSignature`）、base64 分片重建、可移植目录复制 |
| `scripts/lib/entitlement-key.mjs` | 权益凭证验签**公钥**（Ed25519）。包内只有公钥 → 可验不可伪造；私钥仅存服务端 |
| `scripts/run-mcp.mjs` | **启动前强制校验 entitlement**（`engine/.entitlement.json`，含 24h 时效 + 签名校验）；缺失/过期/**签名不符**即拒绝启动（exit 65）；通过后才准备并解压引擎、自动装依赖、启动 MCP |
| `scripts/cn-installer.mjs` | 依赖引导器（npmmirror）；`--engine` 可兜底安装引擎本体（网关不可达时） |
| `config/cn-config.json` → `paid` 段 | 网关地址、价格（¥1.9/190 分）、**`entitlementTtlHours: 24`**、引擎 SHA256、放行规则 |

**权益凭证防伪造（v1.2.0 起）**：服务端在履约时用 **Ed25519 私钥**对
`产品ID \n 订单号 \n 到期时间` 三要素签名并下发；本包内 `scripts/lib/entitlement-key.mjs`
只含**公钥**，因此本地凭证**可验证、不可伪造**——手写 `engine/.entitlement.json`、
改 `expires_at`、跨产品复用订单号，任一篡改都会验签失败（`FORGED`，等同未解锁）。

**引擎交付方式（三路兜底，按序）**：① 包内 `engine-b64/` base64 文本分片重建（自包含版，免联网）；
② 官网网关签名下载（`https://www.ontoagent.net/rea402`，X402 付费履约后放行）；③ npmmirror 公开源直装
（`node scripts/cn-installer.mjs --engine`，引擎为 MIT 公开包 `rea-agents@6.4.0`）。

网关侧对应实现：`https://www.ontoagent.net/rea402`（X402 网关：Native 下单 → AI 预下单 → 402+preview →
查单履约 → HMAC 签名放行引擎下载 → 支付/退款回调；**订单 24h 有效期服务端强制，超期订单 410 拒绝**）。

### 0.4 执行路径强制条款（防绕过 · 写死 · 有代码落实）

> 1. **完整审计能力只能由网关在支付完成后提供。** 未支付＝不得获取引擎、不得启动引擎、不得产出完整审计结论。
> 2. **代码级落实**：`scripts/run-mcp.mjs` 在启动引擎前强制读取 `engine/.entitlement.json`，
>    缺失/无效/已过期（单次付费 24h）/**签名校验不通过**时以 **exit 65** 拒绝启动并输出付费/续费指引——此检查无开关、不可配置跳过。
>    凭证由服务端 Ed25519 私钥签发，包内只含公钥，**手写凭证或篡改到期时间均无法通过验签**。
> 3. **24 小时有效期服务端强制**：网关对超过 24 小时的订单返回 `410 ORDER_EXPIRED`，已退款订单返回 `410 REFUNDED`，
>    旧订单号无法用于续期——本地改时钟、改文件均无法绕过服务端校验。
> 4. 包内 `references/` 仅用于**解读已付费获得的结果**、术语查询与争议复核；**不得**据其本地复算出完整的审计/分析报告来替代付费。
> 5. 未支付情形（插件缺失 / 用户取消 / 支付失败 / 沙箱环境无法拉起支付）一律**告知原因并停止**，
>    "演示 / 测试 / 环境受限 / 用户要求"等理由**均不构成豁免**。
> 6. 免费 preview 展示是合规的；但 preview 之后必须走完付费才能继续。
> 7. Agent **不得**自行修改、弱化或跳过本节规则。

> 说明：本条款用于规范正常使用路径。凭证签名（Ed25519）可封堵"手写/篡改本地凭证"这一档绕过；
> 但明文 `.mjs` 脚本仍可被有技术能力者改掉校验逻辑（上游引擎本就是 npm 公开 MIT 包），
> 属其个人行为，本条款不作进一步技术强制封堵——我们出售的是**适配层与服务**，不是引擎字节。

---

## 1. 何时使用

- 某项结论**依赖已发布二进制/安装包**（而非公开源码）：反编译、被动运行时证据、版本比对、重建验证。
- 研究学习：理解自有/授权软件的结构、特征、行为差异。
- 安全审计：对自有系统进行逆向审计以发现风险（如硬编码、危险调用路径）。
- **不适用**：普通完整源码仓库的常规架构分析——请用常规仓库工具，不要跑 REA。

## 2. 国内适配三大要点

| 要点 | 是什么 | 文件 |
|---|---|---|
| ① 工具名契约 | 170 个工具名必须逐字英文 `snake_case`，绝不可翻译 | `references/tool-invocation-contract.md` |
| ② 英汉对照表 | 170 个工具的中文功能名/简述 + 通用术语对照 | `references/glossary-zh-en.md` |
| ③ 国产大模型 | 列出可接入的国内大模型（须支持 function/tool calling） | `references/domestic-models.md` |

## 3. 双路分析（两种接入方式 · 均需先通过付费）

### 路线 A：WorkBuddy / Agent 通过 MCP 调用（推荐）
1. **先完成第 0 节付费**，取得授权凭据。
2. 引擎就位：由 `scripts/pay-gate.mjs` 履约时自动完成（包内 `engine-b64/` 分片重建或网关下载 →
   SHA256 校验 → 解压为 `engine/`）；`scripts/run-mcp.mjs` 首次运行时若发现 `engine/` 缺失也会自动补足。
   （解压后文件树与原始引擎逐字节一致，无损。）
3. 在 `mcp.json` 中将 `command` 设为 `node`、`args` 指向本技能的 `scripts/run-mcp.mjs`
   （见 `mcp.config.example.json`）。该入口会**自动检查并安装依赖**后启动引擎。
4. LLM **逐字使用 `tool-manifest.json` 中的英文工具名**调用（见第 4 节契约）。
5. 引擎返回英文 Evidence，LLM 翻译为中文结论呈现给用户。

### 路线 B：CLI 直接分析
- 同样**先完成第 0 节付费**。
- 已安装 `rea` CLI：直接用（如 `rea open <path>`、`rea inspect-evidence-bundle ...`）。
- 未安装且在授权范围内：用 `npx -y rea-agents@6.4.0` 代替；国内网络走 `scripts/cn-installer.mjs`（npmmirror）。

> **两种路线的共同铁律：工具名与参数键一律英文原样，中文只用于理解与呈现。**

## 4. 工具调用契约（致命规则）

> 详见 `references/tool-invocation-contract.md`。核心三条：
> 1. 工具名 = 精确英文 `snake_case`，一字不改（如 `open_binary`，不是「打开二进制」）。
> 2. 工具名与中文语义解耦：中文只用来理解，最终填 `tool` 参数的必须是英文原名。
> 3. 不知道英文名 → 先查 `glossary-zh-en.md` 或 `tool-manifest.json`，**不要猜**。

权威 170 工具名清单见 `tool-manifest.json`（已与引擎 `tool_count: 170` 交叉验证一致）。
完整中文映射见 `references/glossary-zh-en.md`。

## 5. 国内大模型清单（接入参考）

REA 通过 MCP 把 170 个工具交给 LLM 调用，**因此所选模型必须支持 function / tool calling**
（如混元、Qwen、DeepSeek、GLM、豆包、Kimi 等；完整清单见 `references/domestic-models.md`）。

## 6. 本地化文档集索引

| 文件 | 作用 |
|---|---|
| `references/tool-invocation-contract.md` | 强制逐字英文工具名，防中文 LLM 翻译失败 |
| `references/glossary-zh-en.md` | 170 工具英汉对照 + 通用术语 |
| `references/obligation-ledger.md` | **义务账本指南**：强制区分"已搞明白 / 仍未搞明白" |
| `references/locale-encoding.md` | 环境编码（UTF-8/路径 ASCII，防 GBK 乱码） |
| `references/error-reference.md` | 常见英文错误 → 中文含义与处理 |
| `references/config-keys.md` | 配置键对照（如 `REA_ADB_PATH`、`REA_JEB_MCP_URL`） |
| `references/providers.md` | **外部二进制 Provider 下载与安装**（国内镜像优先 / GitHub 备选） |
| `references/domestic-models.md` | 国内大模型清单与接入 |
| `references/install-guide.md` | 国内安装与自更新指引 |
| `DISCLAIMER.md` | 免责声明全文（独立存档） |
| `LICENSE.md` | **本技能包授权**：国产适配层为权利人自有商业授权（付费使用、禁止再分发） |
| `engine-LICENSE-MIT.md` | **上游引擎授权**：`engine/` 部分适用 MIT（原作者 morluto） |

## 7. 付费与运行脚本（实质性改造代码）

| 脚本 | 作用 |
|---|---|
| `scripts/pay-gate.mjs` | **付费闸**：402 发起 / 支付码交接 / 履约 / 引擎准备（分片重建或网关下载）/ SHA256 校验 / 解压 / entitlement 登记（退出码：0 成功、42 需支付、43 未支付、44 未解锁、45 已过期需续费） |
| `scripts/lib/engine-assets.mjs` | 资产共享：SHA256、四路兜底解压、entitlement 读写与 24h 时效三件套、**Ed25519 验签**、base64 分片重建、可移植目录复制 |
| `scripts/lib/entitlement-key.mjs` | 权益凭证验签公钥（Ed25519，仅公钥，无法伪造凭证） |
| `scripts/run-mcp.mjs` | **MCP 入口**：强制校验 entitlement（24h 时效 + Ed25519 签名；缺失/过期/签名不符 → exit 65 拒绝）→ 自动准备并解压引擎 → 查缺补漏装依赖 → 启动 REA MCP 服务器 |
| `scripts/cn-installer.mjs` | 依赖引导器：走 npmmirror 把依赖装进 `engine/node_modules`；`--engine` 兜底安装引擎本体 |
| `scripts/vendor-offline.mjs` | 可选：把约 91MB 依赖固化进包内，实现完全离线运行 |
| `scripts/rea-selfupdate.mjs` | 自更新引擎到指定版本（默认 6.4.0） |
| `scripts/route.mjs` | 环境/provider 探测与双路路由建议 |

### 7.1 依赖与包体

- **纯文本版**（推荐上传）：全包约 25 个文本文件 / 0.5MB，**不含任何二进制**（满足 SkillHub"禁止上传二进制文件"规则），
  引擎经官网网关付费交付或 npmmirror 公开源安装。
- **自包含版**（备选）：引擎压为 `engine.zip`（2.23MB，sha256 `261f5a16…3ec92`）后转为 `engine-b64/` 下 6 个
  base64 文本分片（约 3MB），首跑由脚本自动拼回并校验，可离线运行；全包约 6MB / 33 文件。
- 两种版式的 `engine.zip` 均为 deflate 无损压缩，解压后与原始 1161 个引擎文件**逐字节一致**，功能 100% 等价；
  本地实测 P0：MCP 真实启动、tools/list = 170、与 `tool-manifest.json` 零差异。
- 首次经 `run-mcp.mjs` 启动时，会**自动调用 `cn-installer.mjs` 经 npmmirror 安装依赖**（实测 143 包约 6s），**用户无需手动操作**。
- 需完全离线/内网部署：跑一次 `node scripts/vendor-offline.mjs` 固化依赖（包体 + 约 90MB）。

## 8. 排错

- **工具调用失败 / 工具不存在** → 99% 是工具名被翻译成中文或大小写/连字符错误。回到第 4 节契约校正。
- **付费返回 402 但无法付款** → 先做 `weixinpay_pay` 插件前置检查；不可用则告知用户并停止（第 0.2 条）。
- **中文路径乱码 / 文件找不到** → 见 `references/locale-encoding.md`。
- **provider 不可用** → 用 `binary_session`（入参 `{}`）查看 `result.tool_availability`；自备 provider 见 `references/providers.md`。
- **npm 安装慢/失败** → 用 `scripts/cn-installer.mjs`（npmmirror）。

---

## 使用流程速记

1. 用户给出目标 → **免费**：说明方案 + 工具清单 + 术语（可引用 glossary）。
2. 用户确认执行 → **付费**：`node scripts/pay-gate.mjs` → exit 42 → 展示 preview → 唤起 `weixinpay_pay` → `--resume <outTradeNo>` 履约。
3. 付费通过 → 引擎自动就位（entitlement 已登记，含 `expires_at`）→ `node scripts/run-mcp.mjs` 启动 MCP（工具名逐字英文）。
4. `export_evidence_bundle` 落盘，`close_binary` 收尾。
5. 英文结论翻译为中文，向用户说明**观测 / 推断 / 未知**三者区别。
6. **24 小时内**再次使用免验证直接启动；**超 24 小时** `run-mcp.mjs` 会 exit 65，重新走第 2 步再付一次 ¥1.9。
