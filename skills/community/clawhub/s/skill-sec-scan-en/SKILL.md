# 🔒 Skill Security Scanner

**企业级 Skill 安全检测工具**

自动检测 ClawHub / GitHub / 本地 Skill 的安全风险，支持 JavaScript、TypeScript、Python、Shell 等多种文件类型，基于威胁情报驱动的静态分析引擎。

---

## 🎯 核心能力

| 能力 | 说明 |
|------|------|
| **多文件检测** | 支持 `.js`、`.ts`、`.py`、`.sh` 四种文件类型 |
| **威胁分类** | 4 大威胁类别：数据外泄、注入攻击、代码混淆、木马后门 |
| **检测规则** | 57 条精细化检测规则，覆盖 60+ 危险操作特征 |
| **智能评分** | 100 分制安全评分，量化风险等级 |
| **白名单机制** | 支持用户自定义信任的 Skill |

---

## 🛡️ 威胁分类体系

| 分类 | 代码 | 风险类型 |
|------|------|----------|
| **数据外泄 (EXFIL)** | EXFIL | 凭证访问、私钥泄露、网络后门、HTTP 服务 |
| **注入攻击 (INJECTION)** | INJECTION | 命令执行、npx/远程包执行、动态代码执行、提示注入、越狱攻击 |
| **代码混淆 (OBFUSCATION)** | OBFUSCATION | Base64 编码、环境触发、隐藏执行、持久化进程 |
| **木马后门 (TROJAN)** | TROJAN | 文件删除、凭证读取、进程终止、postinstall 攻击 |

---

## 📊 检测规则清单

| 威胁类型 | 规则数 | 代表性规则 |
|----------|--------|------------|
| INJECTION | 19 | cmd-execution、npx-exec、dynamic-exec、prompt-injection、jailbreak、backtick-injection、system-probing、crypto-operation |
| EXFIL | 18 | credential-access、vault-access、private-key、network-backdoor、database-access、config-write、wallet-access、port-listening、proxy-tor、git-operation、file-download |
| TROJAN | 14 | destructive-delete、process-kill、shell-injection、persistent-timer、archive-exploit、arbitrary-write、deserialize |
| OBFUSCATION | 6 | base64、env-trigger、hidden-exec、persistent-shell |
| **合计** | **57** | - |

---

## ⚡ 快速开始



---

## 触发方式

当用户提出以下问题时自动触发：

| 类型 | 触发短语 |
|------|----------|
| **扫描检测** | "扫描 [链接/名称] 的安全性" |
| | "检测一下 [skill名称]" |
| | "帮我扫描一下这个 skill" |
| **风险询问** | "[skill] 有风险吗" |
| | "这个 skill 安全吗" |
| | "检查 [链接] 是否有安全问题" |
| **安全评估** | "评估一下 [名称] 的安全性" |
| | "[skill] 会不会有恶意代码" |
| **通用触发** | "scan security" |
| | "安全检测" |

---

### 🤖 Agent 理解指南

当用户提到以下任一关键词时，执行扫描：

**必须触发**：检测、扫描、安全、风险、恶意代码、危险
**链接识别**：clawhub.ai、github.com
**Skill 名称**：任何后缀为 `-skill` 或在 skills 目录下的名称

---

### 💬 自然语言示例

```
用户: 帮我检测一下 https://clawhub.ai/AphobiaCat/aibtc
Agent: [识别到 clawhub.ai 链接 + 检测关键词]
      [执行 ./scripts/scan.sh https://clawhub.ai/AphobiaCat/aibtc]
      [生成完整报告]

用户: 这个 skill 安全吗？https://clawhub.ai/chrisochrisochriso-cmyk/clawsec
Agent: [识别到 clawhub.ai 链接 + 安全询问]
      [执行扫描]

用户: 检测一下 aibtc 这个 skill 有没有风险
Agent: [识别到 skill 名称 + 风险检测]
      [执行扫描]

用户: 帮我看看这个 skill：clawsec
Agent: [识别到 skill 名称]
      [执行扫描]
```

---

## ⚠️ 重要：完整报告规范

**每次扫描完成必须生成完整报告**，包含：

| 报告章节 | 必须包含 |
|----------|----------|
| 📋 基本信息 | Skill名称、功能描述、扫描文件数、检测问题数 |
| 📊 安全评分 | 评分 + 等级（安全/可疑/危险） |
| ⚠️ 风险详情 | 表格形式：序号、分类、风险、等级、文件 |
| 🎯 结论 | 明确建议（通过/谨慎/禁止）+ 具体原因 |

---

## 威胁分类

| 分类 | 说明 | 示例 |
|------|------|------|
| **EXFIL** | 数据外泄 | 凭证访问、私钥、API密钥 |
| **INJECTION** | 恶意注入 | 命令注入、提示投毒、越狱攻击 |
| **OBFUSCATION** | 混淆隐藏 | Base64、Hex 编码、条件触发 |
| **TROJAN** | 木马后门 | 远程执行、文件删除、进程控制 |

---

## 评分规则

| 评分 | 等级 | 建议 |
|------|------|------|
| 80-100 | ✅ 安全 | 可正常使用 |
| 60-79 | ⚠️ 可疑 | 建议审查后使用 |
| <60 | 🚫 危险 | 不推荐安装 |

---

## 使用方法

### 模式一：扫描远程 Skill（推荐）

直接粘贴 ClawHub 或 GitHub 链接，查看帮助：

```bash
./scripts/scan.sh --help
```

```bash
# 扫描 ClawHub Skill
./scripts/scan.sh https://clawhub.ai/owner/skill-name

# 示例
./scripts/scan.sh https://clawhub.ai/chrisochrisochriso-cmyk/clawsec

# 扫描 GitHub 仓库
./scripts/scan.sh https://github.com/user/repo
```

### 模式二：扫描本地 Skill

指定本地 skill 目录路径：

```bash
# 扫描本地 skill
./scripts/scan.sh /path/to/skill

# 示例：扫描已安装的 skill
./scripts/scan.sh ~/.openclaw/workspace/skills/crypto-wallet

# 扫描当前目录下的 skill
./scripts/scan.sh ./my-skill
```

### 高级选项

```bash
# JSON 格式输出（程序解析用）
./scripts/scan.sh --format json /path/to/skill

# JSONL 格式输出（日志系统用，每行一个 JSON）
./scripts/scan.sh --format jsonl /path/to/skill > report.jsonl

# 批量扫描所有已安装的 skill
./scripts/scan-all.sh
```

### 白名单管理

```bash
# 添加到白名单（需用户确认）
./scripts/scan.sh --whitelist-add skill-name

# 从白名单移除
./scripts/scan.sh --whitelist-remove skill-name

# 查看白名单
./scripts/scan.sh --whitelist-list
```

---

## 文件结构

```
skill-security-scanner/
├── SKILL.md              # 本文档
├── scripts/
│   ├── scan.sh          # 核心扫描脚本
│   └── scan-all.sh      # 批量扫描脚本
├── references/
│   ├── rules.md         # 详细检测规则
│   └── dangerous-commands.md  # 危险命令列表
└── whitelist.txt         # 白名单文件（自动创建）
```

### 支持的文件类型

| 类型 | 扩展名 | 状态 |
|------|--------|------|
| JavaScript | `.js` | ✅ 支持 |
| TypeScript | `.ts` | ✅ 支持 |
| Python | `.py` | ✅ 支持 |
| Shell | `.sh` | ✅ 支持 |

---

## 报告输出标准格式

检测完成后，报告必须使用以下标准 Markdown 格式输出：

### 标准模板

\`\`\`
🔒 **Skill 安全检测报告**
════════════════════════════════════════════════════════════════════

**Skill 名称:** <skill-name>
**扫描文件:** <N> 个
**检测问题:** <N> 个

📊 安全评分：✅/⚠️/🚫 <score>/100 — <status>

🔍 **检测清单：** ✅ 全部威胁分类已检测

| 文件类型 | 状态 |
|----------|------|
| JavaScript (.js) | ✅/➖ 无 |
| TypeScript (.ts) | ✅/➖ 无 |
| Python (.py) | ✅/➖ 无 |
| Shell (.sh) | ✅/➖ 无 |

**🛡️ 威胁检测规则（共 57 项）：**
- **EXFIL (18):** credential-access, vault-access, private-key...
- **INJECTION (19):** remote-script, cmd-execution, npx-exec...
- **TROJAN (14):** destructive-delete, process-kill...
- **OBFUSCATION (6):** base64, env-trigger...

📊 **检测结果：** 发现 <N> 个风险（有问题时显示）
- 🔴 critical: <N> 个
- 🟠 high: <N> 个
- 🟡 medium: <N> 个

---

**⚠️ 风险详情：**（有问题时显示）

| # | 分类 | 风险 | 等级 | 文件 |
|:---:|--------|------------------|-----------|------------|
| 1 | <分类> | <风险名> | <等级> | <文件> |

---

**每条风险解释：**（有问题时显示）
- <风险名> — <解释>

---

✅/⚠️/🚫 **结论：<结论>**

<补充说明>

════════════════════════════════════════════════════════════════════
\`\`\`

### 评分标准

| 评分 | 状态 | 结论 |
|------|------|------|
| 80-100 | ✅ 安全 | 建议使用 |
| 30-79 | ⚠️ 可疑 | 建议谨慎使用 |
| 0-29 | 🚫 危险 | 不推荐安装使用 |

### 示例三：批量扫描（scan-all）

批量扫描时，安全的 skill 仅显示汇总表，有风险的 skill 输出完整报告：

```bash
./scripts/scan-all.sh
```

```
════════════════════════════════════════════════════
     🔒 Skill 全盘安全扫描
════════════════════════════════════════════════════

📁 扫描目录: /Users/moer/.openclaw/workspace/skills

────────────────────────────────────────────────────
🔍 扫描: crypto-wallet
────────────────────────────────────────────────────
（安全 skill，跳过详细输出）

────────────────────────────────────────────────────
🔍 扫描: litcoin
────────────────────────────────────────────────────

════════════════════════════════════════════════════════════════════
                    🔒 Skill 安全检测报告
                     Skill Security Scanner v4.0
════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│ 📋 基本信息                                                    │
├─────────────────────────────────────────────────────────────────┤
│ Skill名称: litcoin
│ 扫描文件: 1 个
│ 检测问题: 2 个
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 📊 安全评分                                                    │
├─────────────────────────────────────────────────────────────────┤
│ 评分: 🚫 55/100 — 危险
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ⚠️  风险详情                                                    │
├─────┬──────────────┬──────────────────┬───────────┬─────────────┤
│  #  │ 分类         │ 风险             │ 等级      │ 文件        │
├─────┼──────────────┼──────────────────┼───────────┼─────────────┤
│  1  │ TROJAN       │ destructive-del  │ 🔴 critical │ miner.py   │
│  2  │ EXFIL        │ network-request  │ 🟠 high     │ miner.py   │
└─────┴──────────────┴──────────────────┴───────────┴─────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 🎯 结论                                                        │
├─────────────────────────────────────────────────────────────────┤
│ ⚠️  建议谨慎使用                                               │
│                                                               │
│ 原因: 检测到 2 个风险                                           │
│                                                               │
│ ⚠️  风险详情:                                                  │
│   • 文件删除 — 可删除/修改本地文件                              │
│   • 网络请求 — 可能向外部发送数据                               │
└─────────────────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════════════════

════════════════════════════════════════════════════════════
                    📊 扫描汇总
════════════════════════════════════════════════════════════

📦 扫描总数: 19

│ Skill                          │ 评分   │
├────────────────────────────────┼────────┤
│ crypto-wallet                  │ 100    │
│ minebean                       │ 100    │
│ ...                            │ ...    │
│ litcoin                        │ 55     │
└────────────────────────────────┴────────┘

✅ 通过: 18
🚫 禁止运行: 1

⚠️  需要关注的 skill:
  - litcoin (评分: 55)
```

**输出规则：**
- 安全 skill（100分）：仅在汇总表显示名称和评分
- 有风险 skill（<100分）：输出完整报告（含风险表格+每条解释）

---

### 🤖 Agent 行为指南

**批量扫描完成后**，Agent 应主动提示用户可以单独检测：

```
✅ 通过: 14
🚫 需关注: 5

⚠️ 有风险的 skill：
• binance-web3 (40分)
• crypto-wallet (0分)
• dune-api (25分)
• litcoin (55分)
• solana-wallet (25分)

💡 想看某个 skill 的完整报告？直接说「扫描 crypto-wallet」或「单独检测 litcoin」
```

**触发场景：**
- 用户执行 `scan-all` 或类似批量扫描
- 扫描结果中有 skill 评分 < 100

**提示原则：**
- 列出所有有风险的 skill 及其评分
- 说明可以单独检测获取完整报告
- 等待用户选择，不自动继续


---

## JSONL 输出格式

```jsonl
{"skill":"example","category":"INJECTION","rule":"npx-exec","level":"critical","file":"handler.js","snippet":"npx --yes"}
{"skill":"example","category":"TROJAN","rule":"destructive-delete","level":"critical","file":"handler.js","snippet":"unlinkSync"}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| skill | string | Skill 名称 |
| category | string | 威胁分类 |
| rule | string | 具体规则 |
| level | string | 风险等级 |
| file | string | 涉及文件 |
| snippet | string | 匹配片段 |

适用于日志系统、Elasticsearch 导入等场景。

### JSON 输出验证

使用 `--format json` 时，脚本会自动验证 JSON 格式：

```bash
./scripts/scan.sh --format json <target> > output.json
# 脚本会自动检查 JSON 格式有效性
```

**注意：** 验证结果仅供参考，静态扫描存在局限性。

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | - | 基础命令注入检测 |
| v2.0 | - | 混淆检测、间接执行、依赖审计 |
| v3.0 | 2026-03-18 | 整合 ClawHub jax 规则（AI投毒、木马检测） |
| v4.0 | 2026-03-18 | 威胁分类、完整报告规范、JSONL 输出 |

---

## 参考文档

详细检测规则：`references/rules.md`
