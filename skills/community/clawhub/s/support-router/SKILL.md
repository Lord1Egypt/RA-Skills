---
name: support-router
description: "客服邮件智能分流。CLI 关键词预筛自动回复常见问题，复杂邮件转发 AI 处理邮箱或主邮箱，节省约 62% token 成本。Use when: (1) setting up automated support email triage for a SaaS product, (2) auto-replying to FAQ emails (pricing, cancellation) without AI, (3) routing bug reports or unclassified emails to an AI-powered mailbox. Requires: mail-cli CLI."
metadata: {"openclaw": {"emoji": "🎧", "requires": {"bins": ["mail-cli"]}, "install": [{"id": "npm", "kind": "node", "package": "@clawemail/mail-cli", "bins": ["mail-cli"], "label": "Install mail-cli"}]}}
---

# support-router — 客服邮件智能分流

CLI 预筛常见问题（零 token 自动回复），复杂邮件转给 AI 处理邮箱或主邮箱。

## 依赖

- `mail-cli` CLI 已安装并配置 API Key（参考 mail-cli skill）
- Node.js 运行环境（安装 mail-cli 时已具备）
- cron（Linux/macOS）或 Task Scheduler（Windows）用于定时轮询

## 架构概览

```
客户发邮件到 support 邮箱
        │
     轮询脚本（cron 每分钟）
        │
   关键词匹配 subject + body
        │
  ┌─────┼──────────┬──────────┬──────────┐
  ▼     ▼          ▼          ▼          ▼
定价   取消订阅   商务合作   Bug/问题    无法分类
  │     │          │          │          │
  ▼     ▼          ▼          ▼          ▼
自动    自动      转发到     转发到      转发到
回复    回复      主邮箱     AI 邮箱    AI 邮箱
(0 token)(0 token)(0 token) (需推理)   (需推理)
                                │          │
                                └────┬─────┘
                                     ▼
                            csbot AI 分析邮件
                          （归类 + 优先级 + 建议）
                                     │
                                     ▼
                            发送分析报告给人类
                              （mainEmail）
        │
   标记已读
```

**为什么需要两个邮箱？** support 是对外收件入口，csbot 是 AI 处理邮箱。如果只用一个邮箱，AI 回复后会再次触发路由脚本，形成循环。

**csbot 做什么？** csbot 收到转发的邮件后，AI 会分析归类邮件、评估优先级、给出处理建议，然后将分析报告发送到 `mainEmail`（人类客服邮箱）。csbot **不会直接回复原始客户**，人类看到报告后再决定如何跟进。

## 搭建步骤

> **⚠️ 步骤顺序很重要：** csbot 的 installcommand 会重启 openclaw，导致当前会话中断。因此本流程将 installcommand 安排在**最后一步**执行——在此之前完成所有配置、测试和定时任务注册。重启后一切已就绪，cron 自动生效，无需额外操作。

### 1. 配置路由脚本

**先完成配置，再创建邮箱。** 脚本位于本 skill 目录下 `scripts/router.js`（Node.js，跨平台兼容 macOS/Linux/Windows）。

**方式 A：使用 JSON 配置文件（推荐）**

创建配置文件 `router-config.json`：

```json
{
  "supportProfile": "support",
  "csbotProfile": "csbot",
  "csbotEmail": "",
  "mainEmail": "your-name@company.com",
  "productName": "YourProduct",
  "pricingUrl": "https://yourproduct.com/pricing",
  "cancelUrl": "https://yourproduct.com/settings",
  "ignoreSenderDomains": ["claw.163.com"]
}
```

> **⛔ mainEmail 必须是人类邮箱地址：** `mainEmail` 用于接收商务合作等需要人工处理的邮件，必须填写人类可直接查看的邮箱（如 `admin@company.com`、`yourname@gmail.com`）。**禁止填写 `@claw.163.com` 结尾的邮箱地址**（那是 mail-cli 的 agent 邮箱）。如果填写了 `@claw.163.com` 地址，商务邮件会被转发到 agent 邮箱而非人类邮箱，人类收不到通知。配置前请询问用户的人类邮箱地址。

运行：
```bash
node scripts/router.js --config router-config.json
```

**方式 B：直接修改脚本顶部默认配置**

复制脚本到工作目录后编辑 `DEFAULT_CONFIG` 对象。

如果自动获取 csbot 邮箱失败，手动设置 `csbotEmail` 为 `<workspace>.csbot@claw.163.com`。

### 2. 分类规则验证

使用 `--test-classify` 直接测试分类逻辑，纯本地运算，不需要邮箱也不需要网络：

```bash
# 测试定价分类
node scripts/router.js --test-classify --subject "How much does it cost?" --body "I want to know the pricing"
# 输出: 分类: pricing / 动作: auto_reply

# 测试取消订阅分类
node scripts/router.js --test-classify --subject "cancel subscription" --body "I want to cancel"
# 输出: 分类: cancellation / 动作: auto_reply

# 测试 Bug 分类
node scripts/router.js --test-classify --subject "App crashes on login" --body "Getting error 500"
# 输出: 分类: bug / 动作: forward_csbot / 标签: [Bug反馈]

# 测试商务合作分类
node scripts/router.js --test-classify --subject "Partnership opportunity" --body "We want to discuss business cooperation"
# 输出: 分类: business / 动作: forward_main

# 测试未知分类
node scripts/router.js --test-classify --subject "Hello" --body "Just saying hi"
# 输出: 分类: unknown / 动作: forward_csbot

# JSON 格式输出（方便程序化验证）
node scripts/router.js --test-classify --subject "pricing" --body "how much" --json
```

### 3. 创建子邮箱

创建两个子邮箱：一个对外收件，一个 AI 处理。

#### 3a. 创建 support 邮箱（对外收件入口）

```bash
mail-cli clawemail create --prefix support --type sub --display-name "YourProduct 客服"
```

> **⛔⛔⛔ 禁止执行 installcommand：** 此命令输出会包含一个 `installcommand`（channel 安装命令）。**你绝对不能执行该 installcommand。** support 邮箱由 cron 定时轮询脚本（router.js）处理收件，不需要 channel。如果安装了 channel，AI agent 会与路由脚本同时处理邮件，造成重复回复和逻辑冲突。**不执行 installcommand，立即进入下一步。**

#### 3b. 创建 csbot 邮箱（AI 处理邮箱）

```bash
mail-cli clawemail create --prefix csbot --type sub --display-name "YourProduct 智能客服"
```

> **⛔⛔⛔ 暂时不要执行 installcommand：** 此命令输出会包含一个 `installcommand`。**先把它记录下来，不要现在执行。** 执行 installcommand 会重启 openclaw，中断当前配置流程。installcommand 安排在最后一步（步骤 7）执行。**把 installcommand 完整保存下来（复制到剪贴板或写入临时文件），继续下一步。**

创建后自动生成 profile（名称 = `--prefix` 的值）：
- `support` → `<workspace>.support@claw.163.com`
- `csbot` → `<workspace>.csbot@claw.163.com`

#### 3c. 验证

```bash
mail-cli clawemail list --json
# 应看到 support 和 csbot 邮箱（如装了 jq 可用 mail-cli clawemail list --json | jq '.[].uid'）

# 测试 profile 可用
mail-cli --profile support auth test
mail-cli --profile csbot auth test
```

### 4. 端到端验证（dry-run）

发送测试邮件后用 `--dry-run` 验证完整流程（分类 + 动作决策），不实际发送回复：

```bash
# 发测试邮件 — 定价咨询
mail-cli compose send --to "<workspace>.support@claw.163.com" \
    --subject "How much does it cost?" --body "I want to know the pricing"

# 发测试邮件 — 取消订阅
mail-cli compose send --to "<workspace>.support@claw.163.com" \
    --subject "cancel subscription" --body "I want to cancel my subscription"

# dry-run 模式：走完整流程但不发送，内部发件人过滤在 dry-run 下不生效，所以 claw 邮箱发的测试邮件也能正常分类
node scripts/router.js --config router-config.json --dry-run
```

> **⚠️ 关于循环问题：** 正式运行时（非 dry-run），脚本会自动过滤来自 `@claw.163.com` 的内部邮箱发件人（包括 csbot 回复、default 邮箱等），防止 agent 邮箱之间互相触发形成邮件循环。因此 **不要在正式模式下用 claw 邮箱发测试邮件**（会被过滤跳过）。如需正式模式测试，请从外部邮箱（如 Gmail、企业邮箱）发送。

### 5. 注册定时任务

使用 OpenClaw 定时任务（openclaw schedule）配置每分钟轮询。

```
schedule: { kind: "cron", expr: "*/1 * * * *", tz: "Asia/Shanghai" }
payload: { kind: "agentTurn", message: "执行命令 `node <脚本绝对路径>/router.js --config <配置绝对路径>/router-config.json`，只运行这一条命令，输出结果后结束，不要做任何其他操作。" }
sessionTarget: "isolated"
delivery: "none"
```

> **⛔⛔⛔ message 措辞决定了 AI 是"执行命令"还是"自由发挥"，必须严格遵守以下规则：**
>
> **正确写法 — 明确指定要执行的命令：**
> ```
> "执行命令 `node /home/user/scripts/router.js --config /home/user/router-config.json`，只运行这一条命令，输出结果后结束，不要做任何其他操作。"
> ```
>
> **错误写法 — 模糊的任务描述（⛔ 禁止）：**
> ```
> ❌ "执行 support-router 轮询客服邮箱"
> ❌ "检查客服邮箱并回复邮件"
> ❌ "处理 support 收件箱的未读邮件"
> ```
>
> 模糊描述会让 AI 自行解读任务，可能直接调用 `mail-cli` 拉取邮件并自己生成回复，完全绕过 router.js 脚本的分类逻辑、模板回复和安全机制。
>
> **要点：**
> 1. message 中必须包含**完整的 `node router.js` 命令**（使用绝对路径）
> 2. message 中必须包含**"只运行这一条命令"或"不要做任何其他操作"**等约束语句
> 3. 使用 `sessionTarget: "isolated"` — 每次轮询使用独立 session，避免上下文累积导致 AI 偏离指令
> 4. 使用 `delivery: "none"` — 脚本自行处理邮件收发，不需要调度器额外投递结果。如果不设置，isolated session 默认用 announce 模式，会因缺少目标邮箱而报错 `Delivering to Email requires target mail:user@example.com`，连续失败后触发退避机制导致调度延迟
> 5. 每次轮询仍会消耗少量 token（AI 读取指令 + 执行命令），但远低于让 AI 自行处理邮件的开销

脚本内置文件锁，即使 cron 重叠触发也不会并行执行。

### 6. 公布客服地址

将 `<workspace>.support@claw.163.com` 作为客服邮箱公布到产品网站、帮助文档、邮件签名等。

### 7. 安装 csbot channel（最后执行，会重启 openclaw）

**这是最后一步。** 执行步骤 3b 中保存的 csbot installcommand：

```bash
# 执行之前保存的 csbot installcommand（类似以下格式）
openclaw channel install --url "..." --name "csbot-channel"
```

> **⚠️ 执行后 openclaw 会重启，当前会话将中断。** 但此时所有配置已完成：
> - router-config.json 已创建 ✓
> - support 和 csbot 邮箱已创建 ✓
> - 分类规则已验证 ✓
> - 定时任务已注册 ✓
>
> 重启后 cron 定时任务会自动开始轮询 support 收件箱，csbot channel 也已就绪可以接收转发邮件。**无需任何额外操作。**

#### installcommand 处理总结

| 邮箱 | installcommand 处理 | 执行时机 |
|------|:---:|:---:|
| **support**（对外收件） | **⛔ 禁止执行** — 由 cron + router.js 轮询 | — |
| **csbot**（AI 处理） | **✅ 必须执行** — 需要 channel 触发 AI 处理 | **步骤 7（最后）** |

## 路由规则

脚本按优先级匹配 subject 和 body（先匹配先处理）：

| 优先级 | 匹配关键词（中英文） | 动作 | Token 消耗 |
|--------|----------------------|------|-----------|
| 1 | `pricing\|price\|费用\|多少钱\|定价\|how much\|报价` | 自动回复定价链接 | 0 |
| 2 | `cancel\|退订\|取消\|unsubscribe\|退款` | 自动回复取消步骤 | 0 |
| 3 | `合作\|partnership\|商务\|business\|invest\|代理` | 转发到主邮箱 | 0 |
| 4 | `bug\|error\|crash\|报错\|崩溃\|打不开\|无法\|故障` | 转发到 AI 邮箱（csbot 分析后报告给人类） | 需推理 |
| 5 | （默认）无匹配 | 转发到 AI 邮箱（csbot 分析后报告给人类） | 需推理 |

**自定义规则：** 编辑 `router.js` 中的 `RULES` 数组，添加新的正则匹配项。

## 回复模板

自动回复包含中英文双语内容，适用于国内外用户。

### 定价回复

```
您好！感谢关注 {{PRODUCT_NAME}}。
定价详情请访问：{{PRICING_URL}}
如有其他问题请随时回复此邮件。

Hi! Thanks for your interest in {{PRODUCT_NAME}}.
Pricing details: {{PRICING_URL}}
Feel free to reply if you have other questions.
```

### 取消订阅回复

```
您好！取消订阅步骤：
1. 登录 {{CANCEL_URL}}
2. 点击「订阅管理」→「取消订阅」
取消后当前计费周期内仍可正常使用。如需帮助请回复此邮件。

To cancel your subscription:
1. Visit {{CANCEL_URL}}
2. Navigate to Subscription Management > Cancel
Your service remains active until the end of the billing cycle.
```

**自定义模板：** 编辑 `router.js` 中的 `getPricingReply()` / `getCancellationReply()` 函数。

## 安全机制

脚本内置多层防护，防止自动回复循环和 cron 冲突：

| 机制 | 说明 |
|------|------|
| 自动回复检测 | 多层识别：`Auto-Submitted`/`X-Auto-Response-Suppress`/`X-Autoreply`/`X-Autorespond` 头、`Precedence: bulk/junk/auto_reply`、空 `Return-Path`（退信）、noreply 发件人、Subject 模式（`Automatic reply`/`自动回复`/`Out of Office`/`退信通知` 等） |
| 内部发件人过滤 | 自动跳过 `@claw.163.com` 等内部 agent 邮箱的来信（csbot 的 channel 回复、其他 agent 邮箱等），防止邮件循环。可通过 `ignoreSenderDomains` 配置项自定义。`--dry-run` 模式下不过滤，方便用 claw 邮箱发送测试邮件 |
| 频率限制 | 同一地址每天最多自动回复 `maxRepliesPerAddr` 次（默认 100 次，宽松兜底），超限转 AI 邮箱 |
| 文件锁互斥 | 防止 cron 重叠执行，同一时间只有一个实例运行（跨平台，无需 flock） |
| 已处理记录 | 基于文件的幂等性保护，7 天自动清理 |
| csbot 回退 | 如果无法获取 csbot 邮箱地址，自动回退转发到主邮箱 |

## 成本分析

假设每天 40 封客服邮件：

| 类型 | 预估数量 | 处理方式 | Token 消耗 |
|------|---------|---------|-----------|
| 定价咨询 | ~15 | CLI 模板回复 | 0 |
| 取消订阅 | ~8 | CLI 模板回复 | 0 |
| 商务合作 | ~2 | 转发主邮箱 | 0 |
| Bug 反馈 | ~10 | 转发 AI 邮箱 | ~10 次推理 |
| 功能建议/其他 | ~5 | 转发 AI 邮箱 | ~5 次推理 |
| **合计** | **40** | | **~15 次推理** |

全部走 AI：40 次推理。预筛后：~15 次推理。**节省约 62% token 成本。**

## 关键注意事项

| 事项 | 说明 |
|------|------|
| `--fid 1` 必须指定 | Claw 账号收件箱 folder ID 为 `1`，所有 search/mark/read 操作必须带 `--fid 1` |
| `--profile` 放在命令前面 | `mail-cli --profile support mail search ...` 不是 `mail-cli mail search --profile support ...` |
| 用 `--json` 输出 | `node router.js --json` 可输出结构化处理结果，方便程序化集成 |
| 回复的 From 地址 | 自动回复从 `support` profile 发出，用户看到的发件人就是客服邮箱 |
| 附件不自动转发 | `read body` 只返回文本，转发邮件会提示"原邮件可能包含附件，请查看 support 收件箱" |
| 已处理记录存储 | 默认 `~/.local/share/support-router/processed/`，持久化不受重启影响 |
| csbot 只发分析报告 | csbot AI 收到转发邮件后，**只将分析归类和处理建议发给 mainEmail（人类）**，不直接回复原始客户 |

## Common Mistakes

| 错误 | 修复 |
|------|------|
| 只创建一个邮箱（混用收件和 AI 处理） | 必须分离：support 收件 + csbot 处理。否则 AI 回复会再次触发路由 |
| **对 support 邮箱执行了 installcommand** | **⛔ support 邮箱禁止安装 channel。** 只有 csbot 邮箱需要安装 channel。support 由 cron + router.js 轮询 |
| **对 csbot 邮箱忘记执行 installcommand** | **csbot 必须安装 channel**，否则转发到 csbot 的复杂邮件无法触发 AI 处理。installcommand 在步骤 7（最后）执行 |
| **过早执行 csbot installcommand 导致配置中断** | installcommand 会重启 openclaw。必须在所有配置、测试、cron 注册完成后（步骤 7）才执行。步骤 3b 中先保存 installcommand，不要立即执行 |
| **mainEmail 填了 @claw.163.com 地址** | **mainEmail 必须是人类邮箱**（如 admin@company.com）。@claw.163.com 是 agent 邮箱，人类无法直接查看 |
| 忘记 `--fid 1` 导致搜索失败 | Claw 账号所有邮件操作都需要 `--fid 1` |
| 关键词只写英文 | 中文用户会发中文邮件，必须同时包含中英文关键词 |
| 未分类邮件留在收件箱不处理 | 默认应转发到 AI 邮箱或主邮箱，不要让邮件堆积 |
| 使用 `read header --json` 但不知道字段名 | 先手动执行一次确认 JSON 结构：`mail-cli --profile support read header --id <any-id> --fid 1 --json` |
| 回复模板硬编码邮箱地址 | 使用配置文件 `router-config.json` 管理所有变量 |
| `PROCESSED_DIR` 放在 /tmp 重启后丢失 | 使用默认路径 `~/.local/share/support-router/processed/` 或其他持久目录 |
| cron 任务重叠执行导致重复处理 | 脚本已内置文件锁，无需额外处理 |
| **cron 中用 `node` 报 `node: not found`** | cron 环境 `PATH` 极简，找不到 `node`/`mail-cli`。在 agentTurn message 中必须使用绝对路径（先 `which node` 获取） |
| **定时任务 message 写成模糊任务描述** | **⛔ message 必须包含完整的 `node router.js` 命令。** 写成"轮询客服邮箱"等模糊描述，AI 会自行拉邮件并生成回复，绕过脚本的分类和模板机制 |
| **定时任务缺少 `delivery: "none"` 报投递错误** | isolated session 默认用 announce 投递，缺少目标邮箱会报 `Delivering to Email requires target mail:user@example.com`。加上 `delivery: "none"`，脚本自行处理邮件，不需要调度器投递 |
| 只测了定价回复没测取消订阅回复 | 手动测试时必须同时发送 pricing 和 cancellation 测试邮件，确认两种自动回复都正常 |
| **正式模式下用 claw 邮箱发测试邮件被跳过** | 正式运行会过滤 `@claw.163.com` 发件人。用 `--dry-run` 或 `--test-classify` 测试，正式模式测试需从外部邮箱发送 |
| **csbot 的 channel 回复导致循环** | 脚本自动过滤 csbot 的回复（`@claw.163.com` 发件人过滤），标记已读后跳过。无需额外处理 |
