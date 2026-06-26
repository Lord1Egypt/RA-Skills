---
name: Session Memory Extractor
slug: session-memory-extractor
version: 1.0.6
homepage: https://clawhub.ai/hasakyi/session-memory-extractor
description: OpenClaw 版 Claude-Mem：自动扫描旧 Session 文件，AI 提炼决策、偏好、事实，追加写入 memory/；同步清理 .jsonl + .trajectory.jsonl，释放数百 MB 磁盘。提炼比清理先跑，记忆不丢失；提炼失败的文件自动 Quarantine 不删，避免静默丢数据。
changelog: "v1.0.6: 安全加固-提炼失败的文件 Quarantine 不删除（__EXTRACT_OK__ marker 验证 + quarantine.log 审计）；v1.0.5: 修复审计问题-统一preview/dry-run语义+强化隐私保护建议+收窄触发词避免误触发+删除歧义别名SME+强化删除前确认；v1.0.4: 安全修复-收窄触发词避免误触发+删除歧义别名SME+强化删除前确认；v1.0.3: 修复飞书通知提取数为0的bug（key名extractions→results）；修复预览大小显示0B的bug（stat -f %s→-f %z）；飞书通知增加内容示例展示（3条snippet）；v1.0.2: 支持config.env配置化、快速预览、并行处理、自然语言触发、飞书通知"
metadata: {"clawhub":{"emoji":"🧠","requires":{"bins":["python3"]},"os":["linux","darwin","win32"],"configPaths":["~/.openclaw/workspace/skills/session-memory-extractor/"]}}
---

# Session Memory Extractor

> cn: OpenClaw 版 Claude-Mem：自动扫描旧 Session 文件，AI 提炼决策、偏好、事实，追加写入 memory/；同步清理 .jsonl + .trajectory.jsonl，释放数百 MB 磁盘。提炼比清理先跑，记忆不丢失。
>
> en: OpenClaw's answer to Claude-Mem (71k GitHub stars): AI-scans old .jsonl/.trajectory.jsonl files, extracts decisions and facts into memory/, then safely deletes raw files. Extract first, cleanup second — context preserved, disk freed.

---

## When to Use

用户**明确要求**提炼 session 记忆时，触发本 skill：

| 用户说（中文） | 用户说（英文） | 含义 |
|---------------|---------------|------|
| 用 session-memory-extractor 提炼 session 记忆 | use session-memory-extractor to extract session memories | 运行提炼 |
| 提炼旧 session 记忆 | extract memories from old sessions | 运行提炼 |
| 运行 session-memory-extractor | run session-memory-extractor | 运行提炼 |

**⚠️ 以下宽泛表达不触发技能（避免误触发导致数据丢失）：**
**⚠️ 以下宽泛表达不触发技能（避免误触发导致数据丢失）：**
- ❌「整理 session 记忆」
- ❌「清理 session 文件」
- ❌「整理记忆」
- ❌「清理文件」
- ❌「SME」单独使用

## 触发命令

识别到上述语句后，**先运行预览**，不直接执行删除：
```bash
bash ~/.openclaw/workspace/skills/session-memory-extractor/session-memory-extractor.sh --agent main --preview
```

**参数说明：**

| 参数 | 作用 |
|------|------|
| `--preview` | 仅扫描并显示统计数字（多少文件、多大空间、最早/最新日期），**不提炼、不删除、不修改任何数据** |
| `--dry-run` | 完整执行一次提炼（写入 memory/），但**不删除**原始文件，适合验证提炼质量 |
| `--parallel N` | 并行数，建议 3-5 |
| `--min-age 14` | 自定义保留天数 |

**⚠️ 确认步骤（必须严格执行）：**
1. 预览完成后，向用户展示扫描结果
2. 告知将执行的操作及风险：
   - **提炼内容**：将提取到 `memory/`，供后续 session 查阅
   - **删除原始文件**：提炼成功的 `.jsonl` 原始文件将被永久删除，**无法恢复**
   - **提炼失败的文件**：v1.0.6+ 自动 Quarantine（重命名为 `.quarantined-<reason>-<ts>.jsonl`），原文件**保留不删**，记录到 `reports/quarantine.log`
   - **隐私风险**：session 中可能包含密码、密钥、敏感对话等，提炼内容会写入 memory/，存在隐私泄露风险
3. 等待用户**明确输入 `YES`（大写）**后，才执行提炼
4. 提炼完成后，询问是否删除原始文件，需用户再次**输入 `YES`（大写）**确认删除

**⚠️ v1.0.6 安全保证：**
提炼失败的 session **绝对不会被静默删除**。三种隔离机制：
1. **marker 验证**：`extract_session.py` 输出 `__EXTRACT_OK__` marker，runner 必须看到这个 marker 才认定提炼成功
2. **内容验证**：提取内容必须 ≥ 50 字符且至少包含 1 个结构化标记（`[FACT]` / `[LEARN]` / `[TODO]` / `[INSIGHT]` / `[NOTE]` / `[REFERENCE]` / `[DECISION]`），否则视为无效
3. **Quarantine**：失败的 session 文件被重命名（不删除），保留在 sessions 目录里供事后审查；同时写入 `reports/quarantine.log` 包含失败原因

可用的 Quarantine reason：
- `no_marker`：API 调用失败 / 返回空内容
- `too_short`：提取内容不足 50 字符
- `no_structured_entries`：提取内容无结构化标记

**⚠️ 隐私保护建议（重要）：**
- 运行前建议先用 `--preview` 查看涉及哪些 session
- 如果 session 包含敏感内容（密码、密钥、业务敏感对话），建议先审查提炼结果再决定是否写入 memory/
- 如果 session 高度敏感，建议跳过提炼、直接清理旧文件即可
- 飞书通知会发送提炼摘要到指定用户，**不要**开启通知给不可信的第三方

用户确认后，再跑实际提炼：
```bash
bash ~/.openclaw/workspace/skills/session-memory-extractor/session-memory-extractor.sh --agent main --parallel 3
```

**可选参数：**
- `--preview` 快速预览（不执行）
- `--parallel 3` 并行数（默认 1，建议 3-5）
- `--min-age 14` 自定义保留天数
- `--dry-run` 只提炼不删除（需确认后执行）

---

## 版本历史

### v1.0.6 (2026-06-18) — Quarantine 安全加固

**背景：** 2026-06-18 老板主 agent 的 `auth-profiles.json` 已被 OAuth SQLite 取代，原 skill 只读 `auth-profiles.json`，导致 31 个 session 提炼调用全部静默失败返回 `NO_MEMORIES`，文件却被删除——**30/31 个 session 原始内容永久丢失**。这是原 skill 的“吞错误 + 无条件删文件”双重设计失误。

**修复：**

| 改动点 | 原状 | v1.0.6 |
|------|------|--------|
| `extract_session.py` | 成功就 print，失败抛 `RuntimeError` 被 runner 吞为 `NO_MEMORIES` | 成功 print `__EXTRACT_OK__\n<content>`；空内容抛 `RuntimeError`；失败 100% 走 stderr + 非零退出码 |
| `run_extractor.py` | 始终写 memory + 删文件 | **验证 marker + 内容 + 结构后才写 memory/删文件**；否则 Quarantine 文件 + 写 `quarantine.log` |
| Quarantine 机制 | 不存在 | 失败文件被 `os.rename` 为 `.quarantined-<reason>-<ts>.jsonl`（不删除）；保留原内容供事后恢复 |
| Shell wrapper `find` | 只排除 `.deleted.*` | 增加排除 `*.quarantined-*`，重跑不会再次处理已 quarantine 文件 |
| 审计 | 仅 report.json | 新增 `reports/quarantine.log`（append-only），含会话ID、文件日期、原因、文件大小 |

**影响范围：** 不影响成功路径（提炼成功的 session 仍会被删）。仅改变失败路径——原 session 不丢失。

### v1.0.5 (2026-05-28) — 审计问题修复

**审计问题修复（来自 ClawHub 安全审计）：**
- **统一 preview/dry-run 语义**：新增参数说明表格，明确 `--preview` 仅扫描不提炼不删除，`--dry-run` 提炼但不删除
- **强化隐私保护建议**：新增「隐私保护建议」段落，建议用户在使用前审查 session 内容、对敏感内容跳过提炼、飞书通知不发给不可信第三方

### v1.0.4 (2026-05-26) — 安全修复

**安全问题修复（来自 ClawHub 安全审计）：**
- **收窄触发词**：删除宽泛触发词（「整理 session 记忆」「清理 session 文件」），避免用户无意图时误触发导致数据丢失
- **删除歧义别名**：移除「SME skill」等歧义触发词，减少意外激活概率
- **强化确认步骤**：明确要求在预览后、执行前、执行后三次确认，确保用户全程知情

### v1.0.3 (2026-05-24)

**Bug 修复：**
- 飞书通知显示"（无提炼内容）"——实际提取了 300 条，原因是 JSON 报告 key 名是 `results` 但代码读的是 `extractions`，现已修复
- 预览 `total_size=0B`——原因是 macOS 上 `stat -f %s` 返回的是 512 字节块数量而非文件大小，现改用 `stat -f %z`

**体验改进：**
- 飞书通知新增 3 条提取内容示例（snippet），不只显示数字统计
- 飞书通知现在会显示所有类型计数（DECISION/PREFERENCE/FACT/TODO），即使某类为 0 也会显示

### v1.0.2 (2026-05-21)

**改进：**
- 支持 `config.env` 配置文件，所有参数可通过配置文件修改，无需触碰代码
- 模型选择从硬编码改为可配置（默认 MiniMax-M2）
- API Key 来源可选择（auth-profiles.json / 环境变量）
- 新增自然语言触发：用户可通过"用 sme 整理 session 记忆"等语句调用

---

## 痛点

OpenClaw 的 Session 文件（`.jsonl` / `.trajectory.jsonl`）越积越多，用了几个月轻松达到数百 MB。

**问题是：**
- 内置 Compaction 只在上下文快满时触发，不清理历史文件
- 内置 Dreaming 不会从旧 .jsonl 里提取内容
- 手动删除 .jsonl = 直接丢失所有上下文

---

## 解决思路

```
扫描 session 目录 → AI 提炼关键内容 → 写入 memory/ → 删除原始文件
```

- **提炼**：用 AI 从原始对话中提取决策、偏好、事实、待办，标注置信度
- **写入**：追加到 `memory/YYYY-MM-DD.md`，永久保留
- **删除**：同时清理 sessions.json 和磁盘上的 .jsonl / .trajectory.jsonl
- **通知**：完成后发送飞书报告（需配置）

---

## 快速开始

### 1. 安装

下载 skill 后，复制配置示例文件：

```bash
cd ~/.openclaw/workspace/skills/session-memory-extractor
cp config.env.example config.env
```

### 2. 配置

编辑 `config.env`，修改以下必填项：

```bash
# 模型（默认 MiniMax-M2）
EXTRACTION_MODEL=MiniMax-M2

# API Key 来源：auth_profiles（默认，从 auth-profiles.json 自动读）
API_KEY_SOURCE=auth_profiles

# 保留天数
MIN_AGE_DAYS=7

# 飞书通知（可选）
NOTIFY_TARGET=ou_your_open_id_here
NOTIFY_ENABLED=false
```

### 3. 运行

```bash
# 完整提取 + 清理
bash session-memory-extractor.sh --agent main

# 预览模式（只提炼，不删除）
bash session-memory-extractor.sh --agent main --dry-run

# 自定义保留天数
bash session-memory-extractor.sh --agent main --min-age 14
```

---

## 配置文件详解

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `EXTRACTION_MODEL` | `MiniMax-M2` | AI 提炼使用的模型 |
| `API_KEY_SOURCE` | `auth_profiles` | API Key 从哪读：`auth_profiles`=从 auth-profiles.json，`env`=从环境变量 |
| `MIN_AGE_DAYS` | `7` | 超过此天数的 session 文件才会被处理 |
| `CLEAN_TRAJECTORY` | `true` | 是否清理 .trajectory.jsonl 文件 |
| `NOTIFY_TARGET` | （空） | 飞书 DM 目标（用户 open_id 或群 chat_id） |
| `NOTIFY_ENABLED` | `false` | 是否启用飞书通知 |
| `DRY_RUN` | `false` | dry-run 模式（只提炼不删除） |

---

## 输出格式

### 控制台摘要

```
Sessions processed:   12
Entries extracted:    31
Total bytes freed:   47.3 MB
Memory written:       memory/2026-05-20.md
```

### memory/ 写入格式

```markdown
## Extracted from session: {session-id}

- **[DECISION]** 用户选择了航天赛道作为主要内容方向
  Confidence: HIGH

- **[PREFERENCE]** 用户喜欢先给结论再展开
  Confidence: HIGH
```

---

## 多 Agent 支持

```bash
bash session-memory-extractor.sh --agent main      # ~/.openclaw/workspace/memory/
bash session-memory-extractor.sh --agent space      # ~/.openclaw/agents/space/workspace/memory/
bash session-memory-extractor.sh --agent math-tutor # ~/.openclaw/agents/math-tutor/workspace/memory/
```

---

## 触发调度

Skill 本身不内置定时，由用户自行配置：

```xml
<!-- macOS LaunchAgent: 每周一 10:00 -->
<key>Label</key>
<string>com.user.session-memory-extractor</string>
<key>ProgramArguments</key>
<array>
    <string>/bin/bash</string>
    <string>/path/to/session-memory-extractor.sh</string>
    <string>--agent</string>
    <string>main</string>
</array>
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key><integer>1</integer>
    <key>Hour</key><integer>10</integer>
    <key>Minute</key><integer>0</integer>
</dict>
```

---

## 功能对比

| 功能 | 内置 Compaction | 内置 Dreaming | 本 Skill |
|------|:---:|:---:|:---:|
| 从 .jsonl 提炼内容 | ❌ | ❌ | ✅ |
| 写入 memory/ | 仅 compaction 时 | 仅 light 阶段 | ✅ |
| 提炼后删除原始文件 | ❌ | ❌ | ✅ |
| 释放磁盘空间 | ❌ | ❌ | ✅ |
| 支持 dry-run 预览 | ❌ | ❌ | ✅ |
| 配置文件化 | ❌ | ❌ | ✅ |

---

## 文件结构

```
session-memory-extractor/
├── SKILL.md                    ← 本文件
├── config.env.example           ← 配置示例（下载后复制为 config.env）
├── config.env                   ← 用户配置（下载更新时保留）
├── session-memory-extractor.sh  ← 主入口
├── run_extractor.py            ← Python 处理器
├── extract_session.py          ← AI 提炼
├── feishu_notify.py            ← 飞书通知
└── reports/                    ← 运行报告目录
```

---

## 安全说明

- **API Key 不写入日志**：API Key 只在内存中使用，不写入任何输出文件
- **auth-profiles.json 读取**：默认从 `~/.openclaw/agents/main/agent/auth-profiles.json` 读取，无需手动配置
- **环境变量回退**：如果 auth-profiles.json 读取失败，回退到 `MINIMAX_API_KEY` 环境变量

---

## 故障排除

### API 调用失败

检查项：
1. `config.env` 中 `API_KEY_SOURCE` 是否正确
2. `auth-profiles.json` 是否存在且包含有效的 API Key
3. 网络是否正常

### 提炼结果为空

可能原因：
- session 文件内容已被压缩/加密
- session 主要是闲聊无实质内容
- 文件日期未超过 `MIN_AGE_DAYS`

### 磁盘空间未释放

检查项：
1. 是否有其他进程正在读取 .jsonl 文件
2. `sessions.json` 是否有写权限