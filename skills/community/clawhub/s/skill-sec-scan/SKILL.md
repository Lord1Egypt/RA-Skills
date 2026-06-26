# 🔒 Skill Security Scanner

**企业级 Skill 安全检测工具**

自动检测 ClawHub / GitHub / 本地 Skill 的安全风险，支持 JavaScript、TypeScript、Python、Shell 等多种文件类型，基于威胁情报驱动的静态分析引擎 + LLM 语义分析双层检测。

---

## ⚡ 交互流程（必须遵循）

```
用户提出检测请求
     ↓
Agent 运行 scan.sh 执行静态扫描
     ↓
Agent 输出完整安全报告（Markdown 格式）
     ↓
Agent 询问用户是否需要语义分析
     ↓
用户确认后
     ↓
Agent 生成 LLM 语义分析提示（从脚本输出中提取）
     ↓
用户将提示复制给 Agent
     ↓
Agent 执行 LLM 语义分析
     ↓
Agent 输出最终结论
```

### 重要原则

- **必须先输出完整静态报告，再询问用户**
- **必须由用户确认后才生成 LLM 语义分析提示**
- **禁止替用户做决定或跳过询问步骤**
- **完整报告包含：下载信息 → 安全评分 → 风险详情 → 每条风险解释**

---

## 🎯 核心能力

| 能力 | 说明 |
|------|------|
| **多文件检测** | 支持 `.js`、`.ts`、`.py`、`.sh` 四种文件类型 |
| **威胁分类** | 4 大威胁类别：数据外泄、注入攻击、代码混淆、木马后门 |
| **检测规则** | 57 条精细化检测规则，覆盖 60+ 危险操作特征 |
| **智能评分** | 100 分制安全评分，量化风险等级 |
| **LLM 语义分析** | 静态扫描定位疑似问题，用户确认后生成提示，Agent 执行深度分析 |
| **白名单机制** | 支持用户自定义信任的 Skill |
| **双层检测** | 静态规则精准定位 → LLM 语义判断真伪 |

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

### 扫描 ClawHub / GitHub Skill

```bash
./scripts/scan.sh https://clawhub.ai/owner/skill-name
./scripts/scan.sh https://github.com/user/repo
```

### 扫描本地 Skill

```bash
./scripts/scan.sh /path/to/skill
./scripts/scan.sh ~/.openclaw/workspace/skills/crypto-wallet
```

### JSON 格式输出

```bash
./scripts/scan.sh --format json https://clawhub.ai/owner/skill-name
```

### 批量扫描

```bash
./scripts/scan-all.sh
```

---

## 📊 评分标准

| 评分 | 等级 | 建议 |
|------|------|------|
| 80-100 | ✅ 安全 | 可正常使用 |
| 30-79 | ⚠️ 可疑 | 建议审查后使用 |
| 0-29 | 🚫 危险 | 不推荐安装使用 |

---

## 🤖 双层检测机制

### 第一层：静态扫描

- **作用**：精准定位疑似风险点（规则匹配）
- **局限**：误报率高（工具函数、检测库本身会被标记）
- **输出**：完整安全报告 + 风险详情表格

### 第二层：LLM 语义分析

- **触发条件**：用户确认后才生成提示
- **作用**：理解代码真实意图，区分恶意行为与正常工具功能
- **输入**：LLM 语义分析提示（包含：风险文件代码 + 上下文）

### 为什么需要双层？

静态扫描适合找"有没有危险操作"，但判断不了"这个危险操作是不是工具本身的功能"。例如：
- `credential-access` — 安全工具检测 credential 是正常功能，不是泄露
- `backtick-injection` — 可能是 Markdown 转义，不是命令注入
- `npx-exec` — 可能是构建/安装脚本，不是运行恶意包

---

## 📋 Agent 操作规范

### 正确流程（必须遵循）

```
1. 用户："检测 [skill] 的安全性"

2. Agent 执行：
   bash scripts/scan.sh https://clawhub.ai/owner/skill-name

3. Agent 输出完整报告（包含所有章节）

4. Agent 询问：
   "发现 {N} 个风险，安全评分 {score}/100。
    是否需要我进行 LLM 语义分析来判断这些是真实威胁还是误报？"

5. 用户确认后，Agent 从脚本输出中提取 LLM 语义分析提示，
   执行语义分析并输出结论

6. 用户选择不分析时，Agent 仅输出报告，不追问
```

### 禁止行为

- ❌ 不输出报告就跳过询问直接生成语义分析
- ❌ 替用户决定要不要分析
- ❌ 自行调用 API 或外部工具
- ❌ 修改或删除报告内容
- ❌ 只输出摘要而非完整报告

---

## 报告输出格式

### 标准模板（完整章节）

```
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
- **EXFIL (18):** credential-access, vault-access...
- **INJECTION (19):** remote-script, cmd-execution...
- **TROJAN (14):** destructive-delete, process-kill...
- **OBFUSCATION (6):** base64, env-trigger...

📊 **检测结果：** 发现 <N> 个风险
- 🔴 critical: <N> 个
- 🟠 high: <N> 个
- 🟡 medium: <N> 个

---

**⚠️ 风险详情：**

| # | 分类 | 风险 | 等级 | 文件 |
|:---:|--------|------------------|-----------|------------|
| 1 | <分类> | <风险名> | <等级> | <文件> |

---

**每条风险解释：**
- <风险名> — <解释>

---

✅/⚠️/🚫 **结论：<结论>**

---

⚠️ 发现 {N} 个风险，安全评分 {score}/100。
是否需要我进行 LLM 语义分析来判断这些是真实威胁还是误报？
```

---

## LLM 语义分析提示格式

当用户确认后，从脚本输出中提取以下内容生成提示：

```
# Skill 安全语义分析请求

## 任务
你是一位专业的代码安全审计员。请从安全产品角度分析以下 Skill，判断它是否可以安全安装使用。

## 安全评估六维框架

| 维度 | 问题 | 权重 |
|------|------|------|
| **1. 数据透明** | 它访问/发送了什么数据？去了哪里？是否告知用户？ | 高 |
| **2. 权限边界** | 申请的权限（网络/文件/进程/环境变量）是否超出声明功能？ | 高 |
| **3. 行为透明** | 有没有未声明的偷偷执行行为？ | 极高 |
| **4. 供应链风险** | 执行外部包（npx/pip/git）来源可信吗？版本固定吗？ | 高 |
| **5. 用户控制** | 用户能随时停止/禁用吗？敏感操作有确认吗？ | 中 |
| **6. 成本告知** | 有没有隐性成本（Gas费/算力消耗/付费API）？ | 中 |

## 额外判断

如存在以下任一情况，直接标记为 failed：

1. **数据外泄**：向非功能必需的第三方发送用户数据
2. **偷偷执行**：在用户不知情时执行额外行为
3. **权限超出**：申请的权限超出 Skill 声明的功能范围
4. **供应链攻击**：执行来源不明的外部包
5. **用户无控制**：无法停止、或停止后自动重启
6. **成本不透明**：产生用户无法预估的成本

## 分析要求

请按以下格式输出：

### 1. 六维评估
- **[维度名]**：[通过/关注/警告] — [简要说明]

### 2. 总体评估
- 语义检测结果：✅ passed / ⚠️ failed / 🚫 failed
- 理由：综合六维判断，给出整体结论

### 3. 逐文件分析

对每个有风险的文件，以表格形式输出：

| 风险 | 判断 | 说明 | 越界行为 |
|------|------|------|---------|
| [风险名] | ✅误报/⚠️低风险/🚨真实威胁 | [详细解释] | ⚠️ 维度X+Y / 无明显越界行为 |

### 4. 最终建议
- 是否可以安装使用？
- 需要注意什么？

## 静态扫描报告
[从脚本输出中提取风险表格 + 相关文件代码]
```

## 触发方式

当用户提出以下问题时触发检测流程：

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

---

## JSON 输出格式

```bash
./scripts/scan.sh --format json <target>
```

```json
{
  "skill": "example-skill",
  "score": 55,
  "files": 3,
  "issues": [
    {"category":"INJECTION","rule":"backtick-injection","level":"critical","file":"handler.js","snippet":"backtick"}
  ]
}
```

---

## 白名单管理

```bash
# 添加到白名单
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

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | - | 基础命令注入检测 |
| v2.0 | - | 混淆检测、间接执行、依赖审计 |
| v3.0 | 2026-03-18 | 整合 ClawHub jax 规则（AI投毒、木马检测） |
| v4.0 | 2026-03-18 | 威胁分类、完整报告规范、JSONL 输出 |
| v4.1 | 2026-03-21 | 新增 LLM 语义分析提示生成（解决静态扫描误报） |
| v4.3 | 2026-03-21 | 重构 LLM 语义分析 prompt：引入安全评估六维框架 + 六维额外判断标准（数据透明/权限边界/行为透明/供应链风险/用户控制/成本告知）；修复文件内容重复输出 bug |
