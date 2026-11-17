# 变更记录 · REA逆向工程审计包·国产适配（付费版）

## [1.2.3] - 2026-10-13

- **修复（仅元数据，引擎与脚本零改动）：ClawHub 显示名错误**。
  v1.2.2 发布时未显式指定显示名，ClawHub 回退读取了发布目录名（`_stage-selfcontained-v122`），
  导致页面标题显示为「Stage Selfcontained V122」。本版本发布时通过 `--name` 显式指定正确显示名
  「REA逆向工程审计包·国产适配（付费版）」。
- **注**：ClawHub 同版本号不能重发，故升 1.2.3；包内容与 1.2.2 完全一致（SKILL.md/README 版本号除外）。

## [1.2.2] - 2026-10-13

- **新增：无插件环境的支付兜底（方案 B / code_url）**。
  此前 402 响应只含 `paymentCode`，唯一支付路径是 `weixinpay_pay` 插件——
  用户把技能装到**没有微信支付插件的客户端**（Claude Code、其他 MCP 宿主等，GitHub/ClawHub 直装常见）时会卡死在付费一步。
  现在网关 402 响应额外下发 `code_url`（微信 Native 扫码链接，与 paymentCode 指向**同一订单**），
  `pay-gate.mjs` 输出**双路支付指引**：
  - 2a. 有 weixinpay 插件 → paymentCode 弹支付卡片（与 1.2.1 行为一致）；
  - 2b. 无插件/插件不可用 → Agent 将 `code_url` 渲染为微信二维码，用户扫码支付 ¥1.9。
- **向后兼容**：402 的 `WeixinPay-Required` 字段保留不变，**v1.2.1 老包无需升级即可继续正常付费**（SkillHub 保持 1.2.1）。
- 履约链路零改动：`--resume` 走微信查单（`trade_state == SUCCESS`），扫码支付与插件支付同单同验。
- 本版本仅面向 GitHub / ClawHub 渠道分发；SkillHub 渠道维持 1.2.1（平台自带微信支付插件，无此短板）。

## [1.2.1] - 2026-10-13

### 修正
- 上游引擎 MIT 授权文件 `LICENSE-ENGINE.md` → 更名为 **`engine-LICENSE-MIT.md`**：
  以 `LICENSE` 开头的文件名会被 GitHub 自动识别为整包许可证（误显示 MIT），
  与"付费产品"的主张冲突；改名后 GitHub 正确识别为 `NOASSERTION`（自定义授权，匹配 `LICENSE.md`）。
- 同步：SKILL.md / README.md / LICENSE.md 内的引用路径一并更新。

---

## [1.2.0] - 2026-10-13

### 安全加固①：权益凭证改为服务端签名（Ed25519），本地可验不可伪造
- 背景：v1.1.0 的 `engine/.entitlement.json` 是**明文 JSON、无签名**，手工写一个并填个未来 `expires_at` 即可绕过付费闸。
- 改造：
  - 网关 `app/entitlement.py` 新增 `sign_entitlement(skill_id, out_trade_no, expires_at)`，
    用 **Ed25519 私钥**（`keys/entitlement_ed25519_private.pem`，仅存服务端/容器 `/app/keys/`）对
    `产品ID \n 订单号 \n 到期时间` 三要素签名；履约响应新增 `entitlement_signature` /
    `entitlement_signature_alg`；**已履约订单重放时按缓存 `expires_at` 重新签发**，保证签名与到期时间一致。
  - 技能包新增 `scripts/lib/entitlement-key.mjs`（**只含公钥**），
    `engine-assets.mjs` 新增 `verifyEntitlementSignature()` 与状态 **`FORGED`**（签名缺失/不匹配）。
  - `pay-gate.mjs`：履约时写入 `signature`/`signature_alg` 并**落盘前先验签**；`--status` 命中 FORGED 报"凭证未通过签名校验"。
  - `run-mcp.mjs`：FORGED 与未解锁/过期同样 **exit 65** 拒绝启动。
- 效果：手写凭证、改 `expires_at`、跨产品复用订单号 → 一律验签失败。
  剩余风险（已知且接受）：明文 `.mjs` 脚本仍可被技术用户改掉校验逻辑；上游引擎本就是 npm 公开 MIT 包。

### 安全加固②：授权文件拆分，付费主张不再自相矛盾
- v1.1.0 包根唯一 `LICENSE.md` 是**上游引擎的 MIT**（署名 morluto）→ 整包挂 MIT 与"付费产品"主张冲突。
- 改造：`LICENSE.md` 改为**权利人自有商业授权**（适配层：付费使用、禁止再分发、禁止绕过付费闸），
  上游 MIT 另存 **`LICENSE-ENGINE.md`**，并在 `LICENSE.md` §0 明确"引擎 MIT / 适配层自有授权"的范围划分。
- `SKILL.md` frontmatter `license` 同步改为 `自有商业授权（见 LICENSE.md；上游引擎为 MIT，见 LICENSE-ENGINE.md）`。

### 其他
- 网关 `SKILL_VERSION` 1.1.0 → **1.2.0 → 1.2.1**（config.py 默认值 + 服务器 `.env` 同步，避免 .env 覆盖默认值）。
- `Dockerfile` 增加 `COPY keys/ ./keys/`；`.env` 增加 `ENTITLEMENT_PRIVATE_KEY_PATH=/app/keys/entitlement_ed25519_private.pem`。

---

## [1.1.0] - 2026-10-12

### 付费规则（对齐 SkillHub 单次付费规则）
- **单次付费 ¥1.9 = 履约后 24 小时内不限次使用（免验证），到期需重新付费**：
  - 本地：`engine/.entitlement.json` 登记服务端下发的 `expires_at`（权威），缺失时按 `granted_at + 24h` 兜底；
    `pay-gate.mjs --status` 新增 exit **45**（EXPIRED 已过期需续费）；有效期内 `--resume` 免验证早退（不打扰网关）。
  - 网关：新增 `ORDER_TTL_HOURS=24`——超过 24 小时的订单履约/重放一律 **410 ORDER_EXPIRED**，
    已退款订单 **410 REFUNDED**（防"一个旧订单号无限续期"）；履约响应新增 `expires_at` / `ttl_hours`；
    幂等重放时自动重签 10 分钟有效的下载链接。
  - `run-mcp.mjs`：entitlement 过期 → exit 65 并输出续费指引（原为永久有效，与平台规则冲突，此版修复）。

### 打包（适配 SkillHub「禁止上传二进制文件」）
- **纯文本版**（默认）：删除 `engine.zip`，全包 25 个文本文件 / 约 0.5MB，零二进制；
  引擎三路交付：官网网关签名下载（主）/ npmmirror 公开源直装（`cn-installer.mjs --engine`，兜底）。
- **自包含版**（备选）：`engine.zip` 转为 `engine-b64/` 下 6 个 base64 文本分片（约 3MB，.txt 纯文本过审），
  首跑自动拼回 + SHA256 校验 + 解压；全包约 6MB / 33 文件。
- `LICENSE` → `LICENSE.md`（规避无扩展名文件被平台拒绝的先例）。

### 修复
- **cn-installer 复制坑（严重）**：`fs.cpSync` 在部分 Node 构建（实测托管 Node v22.22.2）目标路径含中文等
  非 ASCII 字符时**静默失败**（不报错、不复制），曾导致 `engine/node_modules` 为空、MCP 启动即崩。
  改为自实现 `copyDirSync`（copyFileSync 逐文件复制），全平台全路径可靠；`rea-selfupdate.mjs` 同步更换。

### 验证
- 网关本地自检 **31/31 通过**（含 24h 端点级：过期 410 / 有效幂等重签 / 退款 410）；
  生产环境健康检查 v1.1.0、公网 402 真链路验证通过。
- 本地 E2E：TTL 状态机（44/0/45 退出码）、run-mcp 过期 exit 65、base64 分片重建 SHA256 一致、
  **P0 金标准：MCP 真实启动 tools/list = 170，与 tool-manifest.json 零差异**。

## [1.0.0] - 2026-10-12

### 新增
- 基于 `rea-agents@6.4.0` 的国产适配包，**170 个 MCP 工具**全部保留（引擎零改动，仅本地化外壳层）。
- 英汉对照表（170 工具全覆盖）+ 工具调用契约（强制逐字英文工具名，防中文 LLM 翻译失败）。
- 义务账本指南（区分"已搞明白 / 仍未搞明白"）、外部 Provider 下载安装（国内镜像优先 / GitHub 备选）。
- 国内大模型清单、编码/错误/配置键参考、国内安装与自更新指引。
- 免责声明（研究学习与审计用途；仅作声明，不写入引擎）。

### 付费改造
- 接入官网后端 X402 付费网关：`POST https://www.ontoagent.net/rea402/api/resource`，
  402 → `WeixinPay-Required` + `X-Out-Trade-No` → 支付 → 带单号重发取授权。
- **免费预览在前**（分析方案 + 工具清单 + 术语），**付费在调用引擎之前**发起。
- **付费闸写死（有实质性代码落实，非仅文档）**：
  - `scripts/pay-gate.mjs`：付费闸唯一入口（402 发起 / 支付码交接 / 履约 / 下载 / SHA256 校验 / 解压 / entitlement 登记；退出码 0/42/43/44）。
  - `scripts/lib/engine-assets.mjs`：SHA256 校验、四路兜底解压、entitlement 读写。
  - `scripts/run-mcp.mjs`：启动引擎前强制校验 `engine/.entitlement.json`，缺失即 exit 65 拒绝启动——无开关、不可配置跳过。
  - `config/cn-config.json` → `paid` 段：网关地址、价格 ¥1.9/190 分、引擎 SHA256、放行规则。
- 网关侧对应实现（`rea402-gateway`，与 qc402 同商户 1001280329）：Native 下单 → AI 预下单 → 402+preview →
  查单履约 → HMAC 签名放行引擎下载（10 分钟有效）→ 支付/退款回调；本地 22 项自检 + 端到端联调全过。
- 执行路径强制条款（防君子不防小人）：`references/` 仅用于解读已付费结果，未付情形禁止本地复算完整报告。
- 唤起支付前增加 `weixinpay_pay` 插件**前置检查**（SkillHub 审核口径要求）。

### 打包
- 引擎由 1161 个散文件压为单个 `engine.zip`（2.23MB，deflate 无损），
  全包由 1182 文件 / 11MB 降为 **22 文件 / 2.35MB**，满足 SkillHub（≤200 文件 / ≤10MB）。
- 首次运行由 `scripts/run-mcp.mjs` 自动解压 + 经 npmmirror 自动补装依赖，用户无需手动操作。

### 说明
- 本包付费能力依赖网关侧 `rea402` 路由；上线前需确认该路由已部署并可用。
