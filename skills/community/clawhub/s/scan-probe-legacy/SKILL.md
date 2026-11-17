---
name: "MC Ecosystem Adaptation Engineer"
name_zh: "MC全生态智能适配工程师"
slug: "mc-ecosystem-adapt-engine"
version: "1.1.0"
description: "One-stop Minecraft mod ecosystem intelligent management tool with 15 features including mod search, environment setup, Mixin conflict scanning, crash fix, translation, migration assessment, save sync, authorization management, online payment system, admin dashboard, and automated business reports. V1.1.0: ClawHub slim build — no local payment QR images or payment setup docs; paid plans are activated via the online payment page inside the Skill."
description_zh: "Minecraft 模组全生态智能适配工具，支持模组检索、环境搭建、Mixin冲突扫描、崩溃修复、汉化、移植评估、存档同步、授权管理、在线支付系统、管理员控制台、自动化运营报表等15大功能。V1.1.0：ClawHub 精简版——不含本地收款二维码与支付配置文档，付费开通请走 Skill 内在线支付页。"
author: "Liang030214"
homepage: "https://github.com/Liang030214/mc-skill-v1"
icon: "assets/icon-market.jpg"
icon_local: "assets/icon-local.jpg"
tags:
  - minecraft
  - mod
  - forge
  - fabric
  - neoforge
  - quilt
  - mixin
  - translation
  - crash-fix
  - migration
  - chinese
  - i18n
  - multilingual
  - save-sync
  - authorization
  - payment
  - admin-dashboard
  - business-report
  - alipay
  - wechat-pay
  - paypal
category: "games"
license: "MC-Skill Restrictive License v1.0"
language: "en"
languages_supported: ["en", "zh", "ja", "ko", "ru", "es", "it", "el", "th", "hi", "ar"]
min_agent_version: "1.0.0"
---

# MC Ecosystem Adaptation Engineer

One-stop Minecraft mod environment intelligent management tool with complete commercialization support.

# MC 全生态智能适配工程师

一站式 Minecraft 模组环境智能管理工具，提供完整商业化运营支持。

## Feature List

| # | Feature | Description |
|---|---------|-------------|
| F1 | JAR Structure Parser | Parse mod JAR metadata (mcmod.info, fabric.mod.json, mods.toml) |
| F2 | Mod Search & Download | Search and download mods from Modrinth with version and loader filters (supports batch search, category search, similar mod recommendations) |
| F3 | Environment Setup Guide | Intelligently recommend MC version and loader combinations |
| F4 | Mixin Conflict Scanner | Detect Mixin injection conflicts between multiple mods |
| F5 | Resource Repacker | Repack and optimize mod resource files |
| F6 | Save Sync | Backup and restore game saves via Baidu Netdisk sync (supports PC-to-mobile handoff, setup/backup/restore operations) |
| F7 | Multi-Language Translation | Translate mods to target languages (Chinese, English, Japanese, Korean, etc.) with 12-language auto-detection (including Arabic RTL) |
| F8 | Crash Fix | Intelligently analyze crash logs and provide fix suggestions |
| F8.1 | Auto Fix | One-click mod upgrade to resolve crash issues |
| F9 | Migration Feasibility Assessment | Assess feasibility of cross-version/cross-loader migration |
| F10 | Authorization & Usage Management | Local machine ID generation, daily usage counting, free period management (7 days), membership tier management (free/normal), and license activation |
| F11 | Payment Guide Page | Generate HTML payment guide page with QR codes for WeChat Official, Afdian, personal payment, and merchant payment when usage limits are reached |
| F12 | Online Payment System | Complete payment system supporting Alipay (mini merchant API), WeChat Pay (mini merchant API), and PayPal (personal seller account) with 3 subscription plans (monthly/quarterly/yearly) |
| F13 | Admin Dashboard | Web-based admin console for user management, order tracking, permission control, email configuration, and notification settings |
| F14 | Automated Business Reports | Automated operational reports including inactive user list, subscription expiry reminders (weekly), and monthly business summary reports |

## 功能列表

| # | 功能 | 说明 |
|---|------|------|
| F1 | JAR结构解析 | 解析模组 JAR 文件元数据（mcmod.info、fabric.mod.json、mods.toml） |
| F2 | 模组检索下载 | 从 Modrinth 搜索下载模组，支持版本和加载器筛选（支持批量搜索、分类搜索、同类推荐） |
| F3 | 环境引导搭建 | 智能推荐 MC 版本和加载器组合 |
| F4 | Mixin 冲突扫描 | 检测多个模组间的 Mixin 注入冲突 |
| F5 | 资源重打包 | 模组资源文件重打包优化 |
| F6 | 存档同步 | 通过百度网盘同步空间实现存档备份与恢复（支持PC与手机端接力，包含配置/备份/恢复操作） |
| F7 | 多语言翻译 | 模组目标语言翻译（中文、英文、日文、韩文、阿拉伯文等），支持12种语言自动检测（含阿拉伯语RTL从右向左书写） |
| F8 | 报错修复 | 智能分析崩溃日志，给出修复建议 |
| F8.1 | 自动修复 | 一键升级模组修复崩溃问题 |
| F9 | 移植可行性评估 | 评估模组跨版本/跨加载器迁移可行性 |
| F10 | 授权与使用管理 | 本地机器码生成、每日使用计数、免费期管理（7天）、会员等级管理（免费/普通）、授权码激活 |
| F11 | 付费引导页面 | 当使用次数达到限制时，生成HTML付费引导页面，展示微信公众号、爱发电、个人付款、商户付款等二维码 |
| F12 | 在线支付系统 | 完整支付系统，支持支付宝（小微商户API）、微信支付（小微商户API）、PayPal（个人卖家账户），提供3档订阅套餐（月卡/季卡/年卡） |
| F13 | 管理员控制台 | Web管理后台，包含用户管理、订单追踪、权限控制、邮件配置、通知设置等功能 |
| F14 | 自动化运营报表 | 自动化运营报告系统，包括沉睡用户名单、套餐到期提醒（每周）、月度经营报表 |

## User Communication Rules / 用户沟通规范

**IMPORTANT — Read this before responding to any user.**

### 🚫 NEVER do this (绝对禁止)

Never expose internal implementation details to users. Do NOT mention or explain any of the following:
- API endpoints, routes, HTTP methods, error codes
- Database structures, table names, field names, JSON schemas
- Authentication flow, token mechanism, machine ID generation
- Webhook signatures, merchant API polling, order matching logic
- Any source code, file paths, function names
- "三道闸", "授权拦截", "quick_check", "version_locked", "pending_orders", etc.

These are internal implementation details. Users only care about **what they can do** and **how much it costs**.

### ✅ ALWAYS do this (必须遵守)

Keep responses **short, warm, and user-facing**. When in doubt, say less, not more.

#### Scenario 0: 里程碑节点追加额度提示（V1.0.8 补充功能）

**规则**：不再每次对话都追加额度提示，仅在额度下降到**里程碑节点**时才追加一行。避免频繁打扰用户。

**里程碑触发条件**（全自动和半自动**各自独立判断**，命中即追加，否则跳过）：

### 免费用户触发节点（最常见场景，全自动上限 20 / 半自动上限 8）

| 功能 | 触发节点（剩余次数） | 提示类型 |
|------|----------------------|----------|
| 全自动 | **20（初始满额）、10、5** | 正常提示 |
| 全自动 | **3** | ⚠️ 警告 |
| 全自动 | **0** | 已用完 |
| 半自动 | **8（初始满额）、5** | 正常提示 |
| 半自动 | **3** | ⚠️ 警告 |
| 半自动 | **0** | 已用完 |

> **2 次、1 次、以及除上述节点外的所有中间数字 → 一律不提醒**

### 通用规则（适用于所有等级）

- **全自动节点**：剩余次数 ∈ {**上限**, **上限÷2**(向下取整), **上限÷4**(向下取整), **3**, **0**}
- **半自动节点**：剩余次数 ∈ {**上限**, **上限-3**(限不低于4), **3**, **0**}
- 警告（3）优先级高于正常节点；0 单独走"已用完"模板
- 全自动和半自动**各自独立**判断，如果同时归零则两个都触发已用完提示

> 会员用户示例（全自动上限 100 / 半自动上限 50）：全自动触发点 100/50/25/3/0，半自动触发点 50/47/3/0

**AI 调用命令**：
```
python scripts/mc_skill.py get_remaining_quota
```
返回 JSON 包含 `auto_remaining`（全自动剩余）、`semi_remaining`（半自动剩余）、`auto_limit`（全自动上限）、`semi_limit`（半自动上限）。

**按以下模板追加到回复末尾**（只加一行，不要展开）：

| 触发类型 | 提示模板（中文） | 提示模板（英文） |
|----------|------------------|------------------|
| 里程碑命中（正常） | （今日剩余：自动 XX 次，半自动 XX 次） | (Today remaining: XX auto, XX semi) |
| ≤ 3（警告） | 当前{自动/半自动}功能额度不足三次，若想继续深度使用，请及时查询具体额度和会员开通情况 | Only XX {auto/semi} calls left today. Check quota or membership to continue. |
| 单个已用完 | 今日{自动/半自动}额度已用完，如需继续使用请开通会员 | Daily {auto/semi} quota exhausted. Upgrade to continue. |
| **同时归零** | 今日额度已用完（自动+半自动均耗尽），如需继续使用请开通会员 | Daily quota exhausted (both auto and semi). Upgrade to continue. |

> **模板选择规则**：
> - 全自动和半自动**各自独立**判断命中的触发类型
> - 如果两者都命中警告 → 合并为一行，只替换一个{自动/半自动}（取警告优先级更高的那个；若同时警告则用"自动+半自动"）
> - 如果两者都归零 → 用"同时归零"模板，不要拆成两行
> - 如果一个归零一个还剩 → 只用"单个已用完"模板，或"警告+已用完"各一行

**重要**：
- 只在**命中里程碑节点或 ≤3** 时才追加，其余数字一律不追加
- 额度提示**只加一行**，不要展开解释
- 如果用户当前问的就是额度/付费问题（Scenario 1/4），则**不重复追加**
- 警告模板严格使用用户原话风格："当前 xx功能额度不足三次"
- 调用 `python scripts/mc_skill.py open_lookup_page` 可直接帮用户打开查询页面（自动携带本机机器码）

#### Scenario 0.5: 用户问额度/查询 → 直接打开 lookup 页面（V1.0.8 补充功能）

**中文触发词**：额度、剩多少、还剩多少、查询额度、查看额度、我的额度、怎么查额度、查询具体额度、哪里看额度、会员开通

**英文触发词**：quota, remaining, how many left, check quota, my usage, where to see quota, membership

**AI 执行步骤**：
1. 先调 `python scripts/mc_skill.py get_remaining_quota` 获取剩余次数
2. 输出简短回答告知剩余次数
3. 再调 `python scripts/mc_skill.py open_lookup_page` 自动打开浏览器查询页面（内置 `webbrowser.open()`）
4. 同时在回复里附上 URL 作为备用

**中文回复模板**：
> 你今天还有 {自动} 次全自动、{半自动} 次半自动。详细额度和会员开通情况，我帮你打开查询页面了。
> 或直接访问：http://45.76.179.12/lookup.html

**English template**：
> You have {auto} auto, {semi} semi-auto calls left today. I've opened the query page for you.
> Or visit directly: http://45.76.179.12/lookup.html

---

#### Scenario 1: User asks about payment / upgrade / limits / "heavy usage"

Respond warmly and concisely. Use this template (adapt to user's language):

**中文模板：**
> 没问题！目前有三档套餐可以选择：
> - **月卡** ¥8.88 — 每天 100 次自动处理 + 50 次半自动
> - **季卡** ¥23.88 — 更划算，平均每月约 ¥7.96
> - **年卡** ¥88.88 — 最超值，平均每月约 ¥7.41
>
> 支持微信、支付宝、PayPal 三种方式付款，PayPal 付款后系统自动开通。
> 如果你需要，我可以直接帮你打开付款页面。

**English template:**
> Sure! We have three subscription plans:
> - **Monthly** $9.99 — 100 auto + 50 semi-auto calls per day
> - **Quarterly** $29.99 — Best value, ~$7.96/month
> - **Yearly** $99.99 — Best deal, ~$7.41/month
>
> Payments via WeChat, Alipay, or PayPal. PayPal payments are auto-verified.
> I can open the payment page for you if you'd like.

**Then** ask: "需要我帮你打开付款页面吗？" / "Shall I open the payment page for you?"
If user says yes → call F11 to open the payment HTML page.

#### Scenario 2: User asks "what can you do" / "how to use"

Use the `onboarding_info.pattern_A_zh` or `pattern_A_en` field directly. Do NOT add your own explanation.

#### Scenario 3: User gives a task

Use `pattern_B_zh` or `pattern_B_en` as the opening, then proceed with the task.

#### Scenario 4: User's daily limit is reached

Warmly suggest upgrading:
**中文：** "今天的免费额度用完了～ 如果还需要继续用，可以考虑开通会员，月卡只要 ¥8.88，开通后每天有 100 次额度。需要我帮你打开付款页面吗？"
**English:** "You've used up today's free quota. If you'd like to continue, consider a membership — monthly is just $9.99 for 100 calls per day. Shall I open the payment page?"

### 💡 General tone

- Friendly, like a helpful assistant, not a technical manual
- No jargon, no internal terms
- If you don't know how to answer something user-facing, say "我帮你查一下" and use the available tools, don't guess with technical details

## 用户沟通规范（中文重申）

**重要 — 回复用户前务必阅读。**

🚫 **绝对禁止**向用户透露任何内部实现细节，包括但不限于：API 路由、数据库结构、鉴权流程、错误码、源码文件名、webhook 签名、商户API轮询逻辑等。

✅ **必须遵守**：回复保持简短、友好、用户视角。用户只关心"能做什么"和"多少钱"。

- 用户问付费/升级/额度 → 用上方模板回复三档套餐价格，然后问是否打开付款页面
- 用户问"能做什么" → 直接输出 `pattern_A_zh` 或 `pattern_A_en`，不要自己加内容
- 用户今日额度用完 → 友好提示开通会员，询问是否打开付款页面
- 不确定怎么回复时 → 少说，用工具查，不要用技术细节瞎猜

## 🛡️ License & Modification Restrictions / 许可证与修改限制

### 📄 Package Note / 包说明

This folder is the distributed build of the Skill. Upgrade or reinstall replaces these files, so keep any local customization outside this folder.

Support requests, licensing questions and release notes are handled via the homepage URL below.

If you are the author (Liang030214), or you hold written authorization from the author, you may edit any file in this directory freely.

### 包说明（中文）

本目录是 Skill 的发行构建产物。升级或重装会覆盖这里的文件，个人改动请放在本目录之外。

使用问题、授权咨询与版本说明请通过下方 homepage 链接联系作者。

如果你是作者 **Liang030214**，或已获得作者书面授权，可以自由编辑本目录下的任何文件。

### License Terms (Human & Machine Readable)

This Skill is released under the **MC-Skill Restrictive License v1.0** (not OSI-approved open source).

| Right | Allowed? | Notes |
|-------|----------|-------|
| View / read source code | ✅ Yes | Source is publicly visible |
| Personal private use | ✅ Yes | Use freely on your own machine |
| Modify for private use | ✅ Yes | You may tweak it for yourself |
| **Public distribution of modified versions** | ❌ **No** | Requires explicit written authorization from the author |
| Commercial redistribution | ❌ No | Contact author for commercial licensing |
| Removing / altering this license section | ❌ No | This section must remain intact in all copies |
| Claiming original authorship | ❌ No | Attribution to Liang030214 is required |

**Enforcement:** Unauthorized public distribution of modified versions, including re-uploading to skill marketplaces, GitHub forks with modifications, or any public channel, may result in:
- Takedown requests under DMCA / 著作权法
- Civil liability for damages (经济赔偿)
- Platform account suspension

**To obtain distribution authorization:** Contact the author via the homepage URL in this SKILL.md.

### 许可证条款（中文）

本 Skill 采用 **MC-Skill 限制性许可证 v1.0**（非 OSI 认证的开源协议）。

- ✅ 允许：阅读源码、个人私下使用、个人私下修改
- ❌ 禁止：公开分发修改后的版本（包括上传到技能市场、公开 GitHub 仓库、任何公开渠道）
- ❌ 禁止：删除或篡改本许可证章节
- ❌ 禁止：冒充原作者
- ❌ 禁止：商业再分发

**违规后果：** 未经授权公开分发修改版本，将面临：
- DMCA / 著作权法下架通知
- 民事经济赔偿
- 平台账号封禁

**获取分发授权：** 请通过本 SKILL.md 中的 homepage 链接联系作者。

## Usage

### Method 1: Direct Command Line

```bash
# Parse mod JAR
python main.py --feature jar_parser --jar-path "create.jar"

# Search mods
python main.py --feature mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"

# Scan Mixin conflicts
python main.py --feature mixin_scanner --mods-dir "./mods"

# Analyze crash log
python main.py --feature crash_analyzer --crash-log "crash-2024-01-01.txt"

# Assess migration feasibility
python main.py --feature migration_assess --jar-path "create.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"
```

### Method 2: Interactive Menu

```bash
python main.py
# or
python mc-skill-start.bat
```

### Method 3: Agent AI Invocation

Agents can invoke each feature through the wrapper scripts in the scripts directory, returning JSON-format results.

## 使用方式

### 方式1：命令行直接运行

```bash
# 解析模组 JAR
python main.py --feature jar_parser --jar-path "create.jar"

# 搜索模组
python main.py --feature mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"

# 扫描 Mixin 冲突
python main.py --feature mixin_scanner --mods-dir "./mods"

# 分析崩溃日志
python main.py --feature crash_analyzer --crash-log "crash-2024-01-01.txt"

# 评估模组移植可行性
python main.py --feature migration_assess --jar-path "create.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"
```

### 方式2：交互式菜单

```bash
python main.py
# 或
python mc-skill-start.bat
```

### 方式3：Agent AI 调用

Agent 可通过 scripts 目录下的封装脚本调用各功能，返回 JSON 格式结果。

#### 机器码查询触发词（Machine ID Query Triggers）

**⚠️ 重要：必须先判断用户意图，再决定是否调用查询接口**

##### 中文触发规则

| 用户意图 | 判断关键词 | Agent 行为 |
|---|---|---|
| **查询机器码** | 单独的「机器码」「设备码」「硬件码」<br>+ 「查看/查询/获取/显示/告诉我」等动词 | ✅ 调用查询接口 |
| **询问机器码是什么** | 「机器码是什么」「机器码含义」「机器码作用」 | ✅ 调用查询接口 + 解释含义 |
| **询问如何获取** | 「怎么查看机器码」「如何获取机器码」 | ✅ 调用查询接口 |
| **✅ 重置机器码** | 「重置机器码」「重新生成机器码」「换一台机器」<br>+ 「我要重置/帮我重置/请重置」 | ✅ 调 `reset_machine_id` 命令（V1.0.8+ 支持） |
| **❌ 禁止触发查询** | 「如何修改机器码」「怎么更改机器码」「能不能改变」 | ❌ 不调用接口，回复：「机器码是根据硬件自动生成的，无法手动修改，但可以重置」 |


##### 查询额度 / Query Quota

| 用户意图 | 判断关键词 | Agent 行为 |
|---|---|---|
| **查询额度** | 「额度」「剩多少」「还剩多少」+「查询/查看/我的」 | 调 `python scripts/mc_skill.py get_remaining_quota` + 调 `python scripts/mc_skill.py open_lookup_page` 打开查询页面 |
| **询问如何查询额度** | 「怎么查额度」「如何查询额度」「去哪里看额度」 | 回答：直接访问 http://45.76.179.12/lookup.html ，或让我帮你打开 |

| User Intent | Keywords | Agent Action |
|---|---|---|
| **Check quota** | quota / remaining / how many left / check usage | Run `python scripts/mc_skill.py get_remaining_quota` + `python scripts/mc_skill.py open_lookup_page` |
| **How to check quota** | how to check quota / where to see usage | Reply: Visit http://45.76.179.12/lookup.html , or let me open it |

> **说明**：V1.0.8 起新增 `reset_machine_id` 功能，用户更换 AI 软件或重装系统后可主动重置机器码；旧版返回"无法删除或重置"。

##### 英文触发规则

| User Intent | Keywords | Agent Action |
|---|---|---|
| **Query machine ID** | `machine code` / `machine id` (alone)<br>`show` / `get` / `find` / `display` + `machine code` | ✅ Call API |
| **✅ Reset machine ID** | `reset machine id` / `regenerate machine id` | ✅ Run `reset_machine_id` (V1.0.8+) |
| **❌ Do NOT trigger** | `change machine code` / `modify machine id` | ❌ Reply: "Machine ID is auto-generated and cannot be edited, but you can reset it" |

##### 触发判断流程图

```
用户发送消息
    ↓
是否包含「机器码/machine code」关键词？
    ↓ 是
    ↓
是否包含「重置/reset」关键词？
    ↓ 是                    ↓ 否
    ↓                        ↓
✅ 调 reset_machine_id      判断是否为查询意图？
                             ↓ 是
                             ↓
                        ✅ 调用查询接口
```

##### 触发示例

| 用户输入 | 判断结果 | 行为 |
|---|---|---|
| `机器码` | ✅ 查询意图 | 调用接口 |
| `机器码？` | ✅ 查询意图 | 调用接口 |
| `我的机器码` | ✅ 查询意图 | 调用接口 |
| `查看机器码` | ✅ 查询意图 | 调用接口 |
| `重置机器码` | ✅ 重置意图 | 调 `reset_machine_id` |
| `帮我重新生成机器码` | ✅ 重置意图 | 调 `reset_machine_id` |
| `如何更改机器码？` | ❌ 禁止触发 | 回复无法修改 |
| `机器码能修改吗？` | ❌ 禁止触发 | 回复无法修改 |
| `machine code` | ✅ 查询意图 | 调用接口 |
| `reset machine id` | ✅ 重置意图 | 调 `reset_machine_id` |
| `how to change machine code` | ❌ 禁止触发 | 回复无法修改 |

##### API 接口

```
GET http://127.0.0.1:8765/api/machine-id
Response: { "machine_id": "5184c91c54610b2852a9369f68332286" }
```

##### 返回格式

- 查询成功：`您的设备机器码是：5184c91c54610b2852a9369f68332286`
- 查询失败：`抱歉，无法获取机器码，请检查系统权限`

#### 🆕 首次启动 AI 平台声明（V1.0.8+，解决机器码不稳定 Bug）

**触发条件**：用户**首次**使用 Skill 且 `~/.mc-skill/platform.txt` 不存在。

**为什么需要**：原机器码算法依赖父进程（PPID）探测，但 WorkBuddy / Kimi / Trae 等 AI 软件会用不同的 shell wrapper（bash、powershell、cmd）调用 Python，导致每次启动 PPID 都不同，机器码也就跟着变。让用户主动声明一次后，机器码就稳定不变了。

**Agent 行为**：

1. 调 `python scripts/mc_skill.py onboarding_info`，看返回 JSON 里 `platform_question` 字段是否存在
2. 如果存在（即 `needs_ask=true`），在输出 `pattern_A_zh`/`pattern_A_en` 之前，**先用一句友好的话术问用户**：
   - 中文：用 `platform_question.question_zh` 直接输出，不要自己改写
   - 英文：用 `platform_question.question_en` 直接输出
3. 用户回答后，调用：
   ```
   python scripts/mc_skill.py set_platform --platform <用户回答的英文标识>
   ```
   - 常见映射：WorkBuddy→`workbuddy`，Kimi→`kimi`，Trae→`trae`，Cursor→`cursor`，ChatGPT→`chatgpt`，Cline→`cline`，Copilot→`copilot`
   - 不在白名单里就传 `--platform custom`
4. 拿到返回 JSON（包含 `success: true` 与新的 `machine_id`）后，把 `machine_id` 字段在管理后台展示给用户确认（可选）
5. **之后不再问**——`platform_question` 字段会变成 `null`

**用户更换 AI 软件后**：让用户说"我换了一台 AI 工具/换到 Cursor 了"，Agent 调 `set_platform --platform <新平台>` 即可，会自动清理旧平台 salt 并生成新机器码。

**重置机器码**：调 `python scripts/mc_skill.py reset_machine_id`，返回新机器码。

#### 🆕 网络访问说明（V1.0.8+）

**用途**：本 Skill 需要访问作者服务器，完成三件事：授权状态校验、版本检查、使用事件统计。使用事件统计会记录你的使用活跃度（机器码、客户端版本、事件时间与次数），供额度核算与故障排查使用。不采集文件内容，不采集对话内容。

**Agent 行为**：

1. **首次启动时**，在输出 `pattern_A_zh`/`pattern_A_en` 之前，**用一句话如实说明用途并请求允许**：
   - 中文："💡 本 Skill 需要访问作者服务器，用于授权校验、版本检查和使用统计（会记录你的使用活跃度）。如果弹出网络访问提示，请选择「本次会话内始终允许」。"
   - 英文："💡 This skill contacts the author's server for license checks, version checks and usage statistics (it records how active you are). If a network prompt appears, please choose 'Always allow for this session'."

2. **如果用户反馈功能异常或无法使用**（可能是网络被拒），说明原因并询问是否重新允许：
   - 中文："看起来网络连接被拦截了。授权校验和使用统计需要联网，请问您在安全提示里是否选择了「拒绝」？改为「本次会话内始终允许」即可恢复。"
   - 英文："Network access seems blocked. License checks and usage reporting need it. Did you choose 'Deny'? Selecting 'Always allow for this session' restores it."

3. 用户询问数据用途时如实回答：服务器记录机器码、客户端版本、使用事件的时间与计数；不记录文件内容与对话内容。

**注意**：此说明仅在首次启动或用户反馈异常时出现，不要在每次对话中重复。

## Supported Loaders

- Forge
- NeoForge
- Fabric
- Quilt

## 支持的加载器

- Forge
- NeoForge
- Fabric
- Quilt

## Supported MC Versions

- 1.16.5 ~ 1.21.x

## 支持的 MC 版本

- 1.16.5 ~ 1.21.x

## Language Support

This skill supports 12 languages with automatic detection:

| Code | Language | Auto-Detect |
|------|----------|-------------|
| en | English | ✅ |
| zh | 中文 (Chinese) | ✅ |
| ja | 日本語 (Japanese) | ✅ |
| ko | 한국어 (Korean) | ✅ |
| ru | Русский (Russian) | ✅ |
| es | Español (Spanish) | ✅ |
| it | Italiano (Italian) | ✅ |
| el | Ελληνικά (Greek) | ✅ |
| th | ไทย (Thai) | ✅ |
| hi | हिन्दी (Hindi) | ✅ |
| ar | العربية (Arabic, MSA) | ✅ (RTL) |

**Auto-Detection Strategy:**
- The skill automatically detects the user's language from the conversation context and responds in the preferred language.
- Users can also manually specify the language via the `--lang` parameter when calling commands.
- Translation (F7) supports bidirectional conversion between any two supported languages.

## 语言支持

本 Skill 支持 12 种语言，并具备自动检测能力：

| 代码 | 语言 | 自动检测 |
|------|------|----------|
| en | English (英语) | ✅ |
| zh | 中文 | ✅ |
| ja | 日本語 | ✅ |
| ko | 한국어 | ✅ |
| ru | Русский (俄语) | ✅ |
| es | Español (西班牙语) | ✅ |
| it | Italiano (意大利语) | ✅ |
| el | Ελληνικά (希腊语) | ✅ |
| th | ไทย (泰语) | ✅ |
| hi | हिन्दी (印地语) | ✅ |
| ar | العربية (通用阿拉伯语) | ✅ (RTL从右向左) |

**自动检测策略：**
- Skill 会根据对话上下文自动检测用户语言，并以用户偏好的语言回复。
- 用户也可在调用命令时通过 `--lang` 参数手动指定语言。
- 翻译功能（F7）支持任意两种语言之间的双向互译。

## Runtime Environment

- Python 3.10+
- Windows / macOS / Linux
- Network connection (required for mod search feature)
- UTF-8 compatible terminal for multilingual support
- For full i18n functionality, ensure the system locale supports Unicode (UTF-8)

## 运行环境

- Python 3.10+
- Windows / macOS / Linux
- 网络连接（模组搜索功能需要）
- 兼容 UTF-8 的终端以支持多语言显示
- 完整国际化功能需要系统区域设置支持 Unicode（UTF-8）

## Data Collection & Privacy / 数据收集与隐私声明

### Local Data Storage / 本地数据存储

This skill stores the following data **locally only** (in `data/auth_state.json`):

| Data | Description | Purpose |
|------|-------------|---------|
| Machine ID | Hash of device MAC address, hostname, and OS info | Unique device identification |
| First Use Date | Date of first skill usage | Calculate 7-day free period |
| Free Period End Date | First use date + 7 days | Determine free/paid status |
| Daily Usage Count | Count of each feature used per day | Enforce daily usage limits |
| Total Usage Count | Lifetime count of each feature used | Usage statistics |
| Membership Tier | free / normal | Apply appropriate usage limits |
| License Key | User's license activation key | Premium feature access |
| License Expiry | Subscription expiration date | License validity check |

**No data is transmitted to external servers by default.** The optional online verification server (`AUTH_SERVER_URL`) is currently **disabled** (empty string).

### 本地数据存储声明

本 Skill 仅在本地存储以下数据（存储于 `data/auth_state.json`）：

| 数据项 | 说明 | 用途 |
|--------|------|------|
| 机器码 | 设备MAC地址、主机名、操作系统信息的哈希值 | 唯一识别设备 |
| 首次使用日期 | 首次使用Skill的日期 | 计算7天免费期 |
| 免费期结束日期 | 首次使用日期+7天 | 判断免费/付费状态 |
| 每日使用计数 | 每日各功能的使用次数 | 执行每日使用限制 |
| 总使用计数 | 各功能的终身使用次数 | 使用统计 |
| 会员等级 | 免费/普通 | 应用对应的使用限制 |
| 授权码 | 用户的授权激活码 | 高级功能访问 |
| 授权过期时间 | 订阅过期日期 | 授权有效性检查 |

### 强制联网验证与数据上报

**默认启用**：Skill 内置了管理员服务器地址，用户首次安装后自动生效，无需任何配置。

**强制联网验证**：
- 每次使用 Skill 时，自动向管理员服务器验证授权状态
- 本地缓存 1 小时有效的访问 Token，减少网络请求
- 网络不可用时自动降级（免费期内或有本地授权仍可使用）

**数据上报机制**：
- 使用记录先缓存到本地
- 每 20 分钟自动上报一次
- 上报数据包含：
  - 机器码（唯一标识，不包含个人隐私）
  - 使用的功能名称和次数
  - 会员等级
  - 首次使用日期
- **不会上报**：具体文件内容、路径、配置数据等隐私信息

---

## Authorization System (F10) / 授权管理系统

### Free Period / 免费期

- **Duration**: 7 days from first use
- **During free period**: All features unlimited except migration assessment (1 per day after first use)
- **After free period**: Daily usage limits apply (free users: 5 auto/day, 3 semi/day)

### Membership Tiers / 会员等级

| Tier | Auto | Semi | Migration | Exclusive Perks |
|------|------|------|-----------|-----------------|
| Free | 5/day | 3/day | 1/day | — |
| Normal (月/季卡) | 100/day | 50/day | 5/day | — |
| **Yearly Premium** (年卡) | **200/day** | **100/day** | **10/day** | ✅ 容量翻倍<br>✅ 批量任务<br>✅ 新功能抢先<br>✅ 优先队列 |

### Pricing / 定价

- Monthly: ¥8.88/month
- Quarterly: ¥23.88/quarter
- Yearly: ¥88.88/year (continuous subscription)
- Per-use: ¥9.9-89.9 per feature

### 免费期与会员说明

- **免费期**：首次使用起7天内免费
- **免费期内**：除移植评估外所有功能不限次数（移植评估首次免费，之后每天1次）
- **免费期后**：自动应用基础限制

### 会员等级与定价

**7天免费期结束后：**

| 等级 | 全自动 | 半自动 | 移植评估 | 专属权益 |
|------|--------|--------|---------|---------|
| 免费 | 5次/日 | 3次/日 | 1次/日 | — |
| 普通会员 (月/季卡) | 100次/日 | 50次/日 | 5次/日 | — |
| **年卡会员** | **200次/日** | **100次/日** | **10次/日** | ✅ 容量翻倍 ✅ 批量任务 ✅ 新功能抢先 ✅ 优先队列 |

---

## Payment Guide Page (F11) / 付费引导页面

When usage limits are reached, the skill generates an HTML payment page with:

- WeChat Official Account QR code
- Afdian platform QR code
- Personal payment QR code (WeChat Pay / Alipay)
- Merchant payment QR code

**Note**: Payment page is only displayed when `ENABLE_PAYMENT = True` and the user has reached their daily limit. Currently, `ENABLE_PAYMENT = False` in V1.0.1, so payment prompts are **not shown**.

### 付费引导说明

当使用次数达到限制时，Skill 会生成包含以下内容的HTML付费页面：

- 微信公众号二维码
- 爱发电平台二维码
- 个人付款二维码（微信/支付宝）
- 商户付款二维码

**注意**：付费页面仅在 `ENABLE_PAYMENT = True` 且用户达到每日限制时才显示。当前V1.0.1中 `ENABLE_PAYMENT = False`，因此**不会显示**付费提示。

---

## Save Sync (F6) / 存档同步

This feature supports **PC-to-mobile Minecraft save handoff** via Baidu Netdisk sync space:

- **Setup**: Configure sync directory and launcher
- **Backup**: Package and upload game saves to sync directory
- **Restore**: Download and extract latest backup to saves directory

**Data involved**: Only Minecraft save files (world data) are read and written. No game data is transmitted to external servers except through user-configured Baidu Netdisk sync.

### 存档同步说明

本功能通过百度网盘同步空间实现**PC与手机端MC存档接力**：

- **配置**：设置同步目录和启动器
- **备份**：打包游戏存档上传到同步目录
- **恢复**：从同步目录下载最新备份解压到存档目录

**涉及的数据**：仅读写Minecraft存档文件（世界数据）。除用户配置的百度网盘同步外，无游戏数据传输到外部服务器。

**路径权限**：
- 默认白名单：`.minecraft/saves`、`.minecraft/config`、`.minecraft/mods`、`.minecraft/resourcepacks`，以及位于 `.minecraft` 内的启动器自定义存档目录。
- 用户可通过 `--allowed-dirs` 显式添加额外目录，清单只存本机 `data/save_sync_allowlist.json`；同步目录里的配置不能扩大白名单。本次 `--sync-dir` 只对本次运行生效，不持久化。
- `C:\Windows`、`Program Files`、`Program Files (x86)`、`ProgramData`、系统盘根目录、用户主目录本身默认拒绝；仅当本次操作同时给出 `--allow-hard-path` 与 `--confirm-hard-path` 才执行，每次重新确认，留痕到 `data/save_sync_audit.jsonl`。
- 备份与恢复同一套校验；恢复时逐个校验 ZIP 成员，拒绝 `../` 与符号链接成员。被拦截路径写日志并在报告中列出，不静默跳过。

---

## Permissions / 权限声明

| Permission | Required By | Description |
|-----------|------------|-------------|
| File Read | F1, F2, F4, F5, F8, F9 | Read mod JARs, crash logs, config files |
| File Write | F5, F6, F8.1 | Write repacked mods, backup saves, upgrade mods |
| Network Access | F2, F10 | Download mods from Modrinth; optional auth verification & usage reporting (disabled by `MC_SKILL_OFFLINE=1`) |
| Browser Open | F11 | Open payment guide HTML page in browser |
| Local Storage | F10 | Store auth state, usage counts, pending reports (auth_state.json) |
| System Info | F10 | Generate machine ID (MAC, hostname, OS) |

| 权限 | 功能 | 说明 |
|------|------|------|
| 文件读取 | F1, F2, F4, F5, F8, F9 | 读取模组JAR、崩溃日志、配置文件 |
| 文件写入 | F5, F6, F8.1 | 写入重打包模组、备份存档、升级模组 |
| 网络访问 | F2, F10 | 从Modrinth下载模组；授权验证与使用数据上报为可选（`MC_SKILL_OFFLINE=1` 时关闭） |
| 浏览器打开 | F11 | 在浏览器中打开付费引导HTML页面 |
| 本地存储 | F10 | 存储授权状态、使用计数、待上报数据（auth_state.json） |
| 系统信息 | F10 | 生成机器码（MAC、主机名、操作系统） |

---

## Changelog / 更新日志

### v1.0.4 (2026-08-24) — Major Release: Commercialization Support

**重大版本更新：从零构建完整商业化运营体系**

#### 🆕 全新构建的系统模块

| 模块 | 说明 |
|------|------|
| **F12 在线支付系统** | 完整支付系统，支持支付宝（小微商户API）、微信支付（小微商户API）、PayPal（个人卖家账户） |
| **F13 管理员控制台** | Web管理后台，用于用户管理、订单追踪、权限控制、邮件配置、通知设置 |
| **F14 自动化运营报表** | 自动化运营报告系统，包括沉睡用户名单、套餐到期提醒、月度经营报表 |

#### ✨ 新增功能

1. **三种支付渠道支持**
   - 支付宝（小微商户API）- 3张独立收款二维码
   - 微信支付（小微商户API）- 3张独立收款二维码
   - PayPal（个人卖家账户）- 3个独立订阅链接+二维码

2. **三档订阅套餐体系**
   - 月度会员 $9.99 / ¥8.88
   - 季度会员 $24.99 / ¥23.88（八三折优惠）
   - 年度会员 $69.99 / ¥68.88（五折优惠）

3. **管理员控制台功能**
   - 用户管理（查看注册信息、机器码、套餐状态）
   - 订单管理（查看付费订单、支付状态）
   - 权限控制（动态生成管理员密钥）
   - 邮件配置（发件/收件邮箱、授权码）
   - 通知管理（实时通知+定时报表）

4. **定时运营报表系统**
   - 💤 沉睡用户名单（每月1号+每周一自动发送）
   - ⏰ 套餐到期提醒（每周检查，可设置检查日，7天/3天到期预警）
   - 📊 月度经营报表（每月1号发送上月数据）

#### 🔧 功能优化

1. **通知聚合优化**
   - 从「每步一封邮件」改为「流程完成后汇总一封」
   - 用户点击「付款完成」后发送包含完整流程时间线的汇总邮件

2. **货币显示逻辑**
   - 中文模式：微信/支付宝显示¥金额，PayPal显示$金额
   - 英文模式：所有渠道显示$金额（微信/支付宝保留¥符号）

3. **管理控制台布局优化**
   - 实时通知+定时报表合并为统一卡片
   - 所有设置共用一个保存按钮
   - 到期提醒支持检查日下拉选择

#### 📁 新增文件

| 类型 | 文件 | 说明 |
|------|------|------|
| 新增核心模块 | `server/auth_server.py` | 授权服务器，含完整API（约5000行） |
| 新增核心模块 | `server/scheduled_notifications.py` | 定时通知调度器（约450行） |
| 新增UI | `server/static/admin.html` | 管理控制台前端（约4800行） |
| 新增配置 | `server/data/authorizations.json` | 用户授权数据库 |
| 新增配置 | `server/data/orders.json` | 订单数据库 |
| 新增配置 | `server/data/schedule_config.json` | 定时报表配置 |
| 新增资源 | `assets/payment/` | 9张独立收款二维码 |

#### 🐛 Bug 修复

- 管理控制台版本号显示异常（v6.2→v5.7）
- 前端硬编码管理员密钥问题
- 服务器启动模块导入路径错误
- remind_log.json 格式兼容问题

---

## License / 许可证

This Skill is licensed under **MC-Skill Restrictive License v1.0**.
See the "License & Modification Restrictions" section above for full terms.
本 Skill 采用 **MC-Skill 限制性许可证 v1.0**，完整条款见上方「许可证与修改限制」章节。