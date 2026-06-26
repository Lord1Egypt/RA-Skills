---
name: veritas-memory
description: "Veritas Memory v4.2 — 四层记忆架构 + 凭据索引 + 缺口检测 + deep history retrieval。Identity/Working/Short-Term/Long-Term 分层管理。Conversation is ground truth, files are cache. 部署即验证。"
---

# Veritas Memory v4 🧠

**Conversation is ground truth. Files are cache. 部署即验证。**

> v1：STATE.md 被当作记忆本体，手动漏。
> v2：对话即记忆，文件是自动索引。
> v3（2026-06-06）：启动缺口检测。
> v4（2026-06-11）：凭据索引层 + 多源扫描 + deep history retrieval。
> v4.2（2026-06-11）：引入四层记忆架构，区分 stability/recceny；日志归档；部署即验证。

## 四层架构

```
Layer 1 — IDENTITY    SOUL.md + IDENTITY.md   人格锚点，只读
Layer 2 — WORKING     STATE.md                当前状态，≤50行
Layer 3 — SHORT-TERM  memory/YYYY-MM-DD.md    每日日志，14 日归档
Layer 4 — LONG-TERM   MEMORY.md              精华摘要，≤100行
BONUS   — CREDS       CREDENTIALS_INDEX.md    凭据地图
BONUS   — DEEP        sessions + grep JSONL    历史检索兜底
BONUS   — DEPLOY      改代码→部署→验证        不过轮
```

## Quick Start

### 1. AGENTS.md 启动协议 v4

```markdown
新会话启动时：
1. sessions_history(your_last_session, limit=30) → 读对话原文
2. STATE.md 当前状态区 → 快速索引
3. 🔍 缺口检测：STATE.md 最后事件时间 < 上次会话结束时间？
   → YES → spawn 子 agent 补同步 → 完成后再继续
4. MEMORY.md → 长期上下文
5. CREDENTIALS_INDEX.md → 凭据分布图（快速查 Key）
6. 冲突 → 对话为准，修正 STATE.md
```

**缺口检测逻辑（v3 核心）：**

```
STATE_LAST_EVENT_TIME = 从 STATE.md 最后更新时间戳解析
LAST_SESSION_END_TIME = sessions_list 中上一个 session 的 endedAt

if STATE_LAST_EVENT_TIME < LAST_SESSION_END_TIME:
    # State 比对话旧 → 上次会话结束后 sync 漏了
    → spawn sub-agent 读上次会话 transcript
    → 补同步 STATE.md + MEMORY.md
    → 完成后再回答用户
```

这是 2026-06-06「没修好」事故的根因：上次修了 breakout-trade，sync 没触发，STATE.md 不知道。

### 2. 两层同步保障

**A. 会话结束前（主动）:**

对话中不打断写文件。会话结束前：

```markdown
## Session End Auto-Sync

spawn sub-agent with:
  task: "Read this conversation transcript. Extract key changes:
    - Decisions made
    - Company/project status changes
    - System/infrastructure changes
    - New todos or completed todos
    Append to STATE.md event timeline. Update MEMORY.md if long-term facts changed."
```

**B. 下次启动时（兜底）:**

```markdown
# 检查 STATE.md 最后更新时间
# 如果比 sessions_history 最后一条消息还旧 → sync 漏了
→ 先 spawn 子 agent 补同步，再继续对话
```

### 3. Context Loss Recovery（v3 新增）

当 agent 收到不完整上下文的消息时（如「没修好」「上次那个呢」「修好了没」），遵循：

1. **先自查** — 当前 session 里是否有上一段对话？
2. **无则补** — sessions_history(prev_session) → 读上次对话原文
3. **不要反问** — 用户已经说了关键信息，是你没记住。反问浪费用户时间
4. **优先修缓存** — 找到缺口后先写 STATE.md，再回答

> 今早事故：agent 反问「你说的是哪件事没修好？」→ 用户被迫转发告警截图。不该发生。v3 的缺口检测 + 启动协议可以防止。

### 4. Credential Layer（v4 新增）

**凭据不依赖 sync。** 对话中收到任何 API Key / Token / 密码 → **本轮立即处理，不过夜。**

#### 写入流程（对话中收到凭据时）

```markdown
收到凭据 → 本轮回复中立即：
1. 写入 CREDENTIALS_INDEX.md（service → key_name → location）
2. 写入目标服务器 .env 或 systemd Environment=
3. 加密存 CREDENTIALS.md.gpg（如敏感）
4. 验证连通性（curl 测试）
```

**为什么不在会话结束时才写：** 凭据是单点故障。sync 漏一次 → Key 丢失 → agent 失忆。

#### 查询流程（需要凭据时）

```markdown
需要 Key → 按顺序查：
1. CREDENTIALS_INDEX.md（最快，1 秒）
2. 目标服务器 .env（cat /opt/*/ .env）
3. systemd service（systemctl cat <service> | grep Environment）
4. 最后才反问用户
```

**多源扫描清单：**
- `.env` 文件（各项目目录）
- `systemctl cat <service>` 的 `Environment=` 行
- `/etc/environment`
- `export` / `env` 当前进程环境
- GPG 加密文件 `CREDENTIALS.md.gpg`

#### CREDENTIALS_INDEX.md 格式

```markdown
# Credential Index

| Service | Key Name | Location | Status |
|---------|----------|----------|--------|
| TokenMall | TOKENMALL_API_KEY | systemd flintapi-overseas | ✅ verified |
| DeepSeek | BUILT_IN_FORGE_API_KEY | systemd flintapi-overseas | ✅ |
| Stripe | STRIPE_SECRET_KEY | systemd flintapi-overseas | ✅ |
```

### 5. Log Archiver（v4.2 新增）

每日日志膨胀 → 定期归档。memory/ 目录超过 30 个文件时触发归档。

```bash
mkdir -p memory/archive
find memory/ -maxdepth 1 -name '????-??-??.md' -mtime +14 -exec mv {} memory/archive/ \;
```

在 HEARTBEAT.md 或 Memory Tender 中触发，每 1-2 周运行。

### 6. 部署即验证（v4.2 新增）

**说修了 ≠ 部署了。** 三次教训（Key 没存、C1 参数未部署、trade_direction 修了没推）。

硬规则：**改代码 → 部署到服务器 → 立刻验证 → 验证通过才算 done。不过夜、不过轮。**

验证清单：
- [ ] 文件已推送到目标服务器
- [ ] 服务已重启 (`systemctl restart`)
- [ ] 服务 active (`systemctl is-active`)
- [ ] 关键端点返回预期值 (curl / grep)
- [ ] 参数变更已确认生效

### 7. Deep History Retrieval（v4.1 新增）

**sessions_history 有窗口限制。** 长对话中大量 tool call 会挤掉用户消息，历史对话成黑洞。

#### 检索优先级

```markdown
需要找某条历史对话：

1. sessions_history(limit=200)                     ← 最快，但要够得着
2. 够不着 → 读 transcript 文件直接搜                  ← 兜底
   exec: grep -i "关键词" /root/.openclaw/agents/m/sessions/{sessionId}.jsonl
3. 不知道在哪个 session → spawn 子 agent 扫全部 session 文件
   subagent task: "Search all M session transcript files for [query]. Return matching messages with timestamps."
```

#### 为什么 sessions_history 不够

- sessions_history 返回 N 条消息（含 tool call），200 条窗口可能只覆盖 30 条用户消息
- 今天跟 mooze 聊了 20 轮 FlintAPI，200 条 limit 只拉到今天会话，昨天的 Key 消息完全够不着
- 对话越长、tool call 越多，窗口越浅

#### 兜底命令模板

```bash
# 搜当前 session 的所有用户消息
grep '"role":"user"' /root/.openclaw/agents/m/sessions/{sessionId}.jsonl

# 搜所有 M session 文件中的关键词
grep -rl "关键词" /root/.openclaw/agents/m/sessions/*.jsonl | xargs grep -l '"role":"user"'
```

### 8. Memory Tender（可选，每 2-3 天）

合并旧事件、清理过时记忆、交叉验证。同步更新 CREDENTIALS_INDEX.md。

## Core Files

| File | Purpose | Writer |
|------|---------|--------|
| `sessions_history` | Ground truth memory | System (auto) |
| `STATE.md` | Event timeline + current state | Auto-sync + gap fix |
| `MEMORY.md` | Curated long-term memory | Auto-sync + Tender |
| `memory/YYYY-MM-DD.md` | Optional raw notes | Agent (on demand) |

## Lessons

1. **对话是记忆本体。** 新会话先读 sessions_history，不依赖二手笔记。
2. **不打断写文件。** 手工 WAL 必然漏。自动同步比勤奋可靠。**但同步可能漏，启动必须检测。**
3. **缺口检测是硬要求，不是优化。** 每次启动必须比对 STATE.md 时间戳和上次会话时间。
4. **小文件大索引。** STATE.md 保持 ≤50 行、MEMORY.md ≤100 行。信息膨胀就删旧留新。
5. **冲突时对话赢。** 文件过期了就修文件，不要用过期信息反驳对话。
6. **丢失上下文时不要反问。** 先用 sessions_history 自己补。补不全再问。
7. **凭据不走 sync。** 凭据类信息（API Key / Token / 密码）收到后本轮立即写入索引 + 目标服务器，不等到会话结束。
8. **查凭据走多源扫描。** `.env` + systemd `Environment=` + `/etc/environment` + GPG，全查完再反问。

## Real-World Failures

### 2026-06-06 — 缺口检测缺失

| 环节 | 发生了 | 应该发生 |
|------|--------|---------|
| 上次会话修了 breakout-trade | ✅ | — |
| 会话结束 sync | ❌ 未触发（会话中断） | ✅ 写入 STATE.md |
| 下次启动 gap 检测 | ❌ v2 无此步骤 | ✅ 发现缺口→补同步 |
| 用户说「没修好」| ❌ agent 反问「哪件事」 | ✅ agent 已读过上次对话 |

### 2026-06-11 — 凭据索引缺失 + 历史检索黑洞

| 环节 | 发生了 | 应该发生 |
|------|--------|---------|
| mooze 给 TokenMall Key | ✅ 存在 systemd Environment= | — |
| 凭据索引写入 | ❌ 未创建 CREDENTIALS_INDEX.md | ✅ 本轮立即写索引 |
| 下次会话找 Key | ❌ sessions_history(200) 只拉到今天消息 | ✅ 先读索引，找不到直接 grep transcript 文件 |
| 回退检索 | ❌ 不知道可以直接搜 transcript JSONL | ✅ v4.1：Deep History Retrieval 三步回退 |
| 根因 1 | systemd 存了 Key 但 agent 不知道去那里找 | v4：凭据索引 + 多源扫描 |
| 根因 2 | sessions_history 窗口太浅，老旧消息不可达 | v4.1：transcript 文件直接搜索 |

## ClawHub Package

```
veritas-memory/
  SKILL.md              ← This file
  templates/
    STATE.md            ← Template
    MEMORY.md           ← Template
    AGENTS_startup.md   ← Startup protocol snippet
  scripts/
    auto-sync.md        ← Sub-agent prompt for session-end sync
    memory-tender.md    ← Periodic maintenance prompt
```

## Bidirectional Verification

Logs are the referee between user and agent.

```
Agent says X, user says Y:
  → Check sessions_history
  → Agent wrong → "You're right. I misremembered." → Fix cache
  → User wrong → "According to our conversation on [date], we said X. Want to change?"
  → Both right, different times → Clarify timeline
```

Never say "You're wrong." Present facts neutrally.
