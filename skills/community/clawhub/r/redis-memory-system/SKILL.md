---
name: redis-memory-system
description: "跨会话自动记忆系统 v3.3.0 — 单脚本+配置驱动+语义标签索引。支持标签检索、倒排索引、语义搜索。"
---

# Redis 记忆系统 v3.3.0

**核心思路：Agent 零负担，系统自动完成。cron 子 session 绕过 dmScope 限制，通过文件系统直读 transcript。**

## 架构

```
┌──────────────────────────────────────────────────────┐
│ OpenClaw Cron (每1h, isolated session)               │
│                                                      │
│  ① 分布式锁 (SET NX EX 600) 防并发                   │
│  ② ls -t 找最新 transcript 文件（排除cron自引用）     │
│  ③ extract_dialog.py 提取末尾200行对话               │
│  ④ LLM 语义去重 + 摘要生成                           │
│  ⑤ Lua EVAL 原子写入（HSET+EXPIRE+last_seen）       │
│  ⑥ 锁释放                                           │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────┴──────────────────────────────┐
│ 系统 Cron (每1h) — 监控哨兵                          │
│                                                      │
│  ① 心跳写入隔离 key: cron:health                     │
│  ② 逐用户检查 memory:<用户> 今天有无摘要              │
│  ③ 异常时写告警 flag 到 /tmp/                        │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────┴──────────────────────────────┐
│ Agent Session 启动时                                  │
│                                                      │
│  redis_memory.sh get <用户>  → 查最近3天              │
│  cat /tmp/*.flag              → 检查告警              │
└──────────────────────────────────────────────────────┘
```

## 关键解决的问题

| 问题 | 方案 |
|------|------|
| dmScope 隔离导致 cron 子 session 看不到主会话 | 文件系统直读 transcript JSONL |
| exec 间变量丢失（各自独立 shell） | 合并为单个 exec 脚本，变量只在进程内传递 |
| 重复追加相同摘要 | LLM 语义去重—新旧摘要表达相同信息时跳过 |
| cron 污染 memory hash | cron 心跳写到隔离 key `cron:health` |
| 并发执行风险 | Redis SET NX EX 分布式锁，防止两个 cron 同时写 |
| 非原子写入（HSET+EXPIRE 分开执行） | Lua 脚本（EVAL）保证一个事务内完成全部操作 |
| 文件查找顺序错误 | `ls -t` 按修改时间取最新，而非按匹配数 |

## 文件说明

| 文件 | 用途 |
|------|------|
| `scripts/memory.sh` | 核心脚本：sync / get / set / tag / search / heartbeat / ping / stats |
| `scripts/extract_dialog.py` | transcript 对话提取工具 |
| `scripts/setup.sh` | 一键安装（Redis + 脚本 + 系统cron） |


## 🔑 Redis Key 设计

| Key | 类型 | TTL | 说明 |
|-----|------|-----|------|
| `memory:<用户名>` | Hash | 7天 | 每日对话摘要，field=日期，value=文本 |
| `cron:health` | Hash | 7天 | 系统心跳（隔离，不污染记忆数据） |
| `activity:<用户名>:last_seen` | String | 12h | 最后活跃时间标记 |
| `cron_lock:memory_sync` | String | 10min | 分布式锁，防并发 |

## 部署 / Deployment

### 1. 基础安装 / Setup

```bash
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

### 2. 创建 OpenClaw cron（核心 / Core）

```bash
# Create auto-sync cron job (runs every 1h)
# 创建每 1 小时自动同步的 cron 任务

PROMPT=$(cat scripts/openclaw_cron_prompt.txt)
openclaw cron add \
  --name "memory-auto-sync" \
  --every 1h \
  --session isolated \
  --timeout-seconds 180 \
  --thinking minimal \
  --tools "exec,read" \
  --no-deliver \
  --message "$PROMPT"
```

**重要 / Important：**
- `--tools "exec,read"` — restricts cron to script execution & file reading only, prevents recursive tool triggers
- 限制 cron 只能执行脚本和读文件，防止递归触发其他工具
- `--session isolated` — runs cron in an isolated container, won't affect main session context
- 确保 cron 在独立容器跑，不影响主会话

## Session 启动检查 / Session Startup Check

每次新 session 启动时加载近期记忆。
Load recent memory on each new session start:

```bash
# Read last 3 days of memory
# 读取最近 3 天的记忆
bash scripts/memory.sh get <user>

# Check for memory loss warnings
# 检查是否有记忆丢失告警
cat /tmp/memory_warning_<user>.flag 2>/dev/null
```

### 日常运维命令 / Daily Operations

```bash
# Check Redis connection  · 检查 Redis 连通性
bash scripts/memory.sh ping

# View system overview  · 查看系统概览
bash scripts/memory.sh stats

# Read user memory (last 3 days)  · 查用户记忆（最近 3 天）
bash scripts/memory.sh get <user>

# Read memory for a specific date  · 查指定日期记忆
bash scripts/memory.sh get <user> 2026-05-26

# Search by semantic tags  · 按语义标签搜索
bash scripts/memory.sh search <keyword>

# Manually write a summary  · 手动写入摘要
bash scripts/memory.sh set <user> 2026-05-26 "Summary text here"

## v3.2.3 相比 v3.2 的改动（2026-05-26）

#### 语义标签索引（v3.2.3 新增）
- **LLM 语义标签：** cron 同步时自动提取 5 个概念级标签，替代向量检索
- **倒排索引：** `tagidx:<标签>` → 日期集合，Redis SINTER O(1) 查询
- **标签搜索：** `memory.sh search <关键词>` 配合 Agent 语义匹配
- **零额外内存：** 不用 embedding 模型和向量数据库，每日标签仅占 ~200 字节

### 核心架构改动
- **合并exec调用：** 文件查找+对话提取+Redis查重合并为一个脚本，变量不会跨exec丢失（原v3.1三步分离，变量会在独立shell中丢失）
- **Redis原子写入：** 用 Lua 脚本（`EVAL`）替代三次独立 `redis-cli` 调用，保证 HSET + EXPIRE + SET last_seen 在同一事务中完成
- **分布式锁：** `SET NX EX 600` 防并发，cron 卡住时最长600秒自动释放（`trap cleanup EXIT` 保底）
- **重试机制：** 文件读取失败时最多重试 2 次，间隔 1 秒

### 修复的 bug
- **找文件：** 从按匹配数取最多改为按 `ls -t` 修改时间取最新，避免旧文件碾压新 session
- **shell语法：** `grep -c` 后加 `|| echo 0` 兜底，消除 `[: 0: integer expression expected`
- **阈值：** 从 5 降到 2，短对话也能被收录

### 脚本改进
- **参数校验完善：** 所有脚本增加参数个数和内容校验，防止因参数不足产生幽灵记录
- **用户名校验：** `redis_memory_user.sh` 启动时检测 USERNAME 是否仍为占位符，防止写入 `memory:your_username`
- **用户列表外部化：** `cron_heartbeat_ping.sh` 支持环境变量 `REDIS_MEMORY_USERS`、配置文件 `/etc/redis-memory-users.conf` 或硬编码数组三种方式
- **redis_memory.sh 新增：** `ping` 命令（检查Redis连通性）、`stats` 命令（统计各用户记忆天数/字符数）
- **天数限制：** `recent` 命令上限 30 天，防止误传大数字导致遍历全部历史

## 版本历史

- v1.0 (2026-05-16) — 基础 Redis 记忆存储
- v1.1 (2026-05-17) — 多用户隔离 + SOUL 铁律
- v2.0 (2026-05-20) — draft 机制 + 三层保底 + 启动恢复
- v2.1 (2026-05-21) — cron 脚本增强 + 用户专用脚本
- v3.0 (2026-05-23) — 系统自动读会话写摘要，Agent 零负担
- **v3.1 (2026-05-23) — 修复 dmScope 隔离问题，改用文件路径；增加去重/过滤逻辑**
- **v3.1.1 (2026-05-25) — 架构大修：合并exec、Lua原子写入、分布式锁、重试机制**
- **v3.2 (2026-05-25) — 单脚本+配置驱动+JSON输出**
- **v3.2.3 (2026-05-26) — 语义标签索引 + 倒排检索 + 标签搜索**
- **v3.3.0 (2026-05-27) — 统一版本号；修复跨夜日期写入错误：sync改用transcript文件修改时间确定日期key，避免凌晨写入时日期错位**
