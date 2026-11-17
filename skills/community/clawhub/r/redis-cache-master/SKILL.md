---
slug: redis-cache-master
name: redis-cache-master
version: "2.0.0"
displayName: Redis缓存大师
summary: 生产级Redis实战：TTL纪律+淘汰决策树+集群哈希标签+原子陷阱防控，避坑指南。
license: MIT
description: |-
  面向生产环境的 Redis 实战指南，直击"无 TTL 内存泄漏、淘汰策略错配、集群跨槽报错、原子性陷阱、大 Key 拖垮 eviction"五大高频生产事故。提供决策树、模式库、故障排查清单，而非零散命令罗列。

  核心能力包括 TTL 纪律规范（每个缓存键必设过期）、淘汰策略决策树（allkeys-lru/volatile-lru/noeviction 场景化选择）、集群哈希标签模式（多键操作同槽保证）、原子操作模式（SETNX/WATCH/Lua 选择指南）、可靠消息用 Streams 替代 Pub/Sub、持久化决策矩阵（RDB/AOF/both/none 四象限）、大 Key 检测与拆分、内存监控与告警、连接池与管道优化。

  适用场景：缓存设计、限流、分布式锁、消息队列、会话存储、排行榜、计数器、生产 Redis 运维与故障排查、集群规划与扩容。

  差异化：相比零散命令清单，本系统提供决策树式选择指南（淘汰策略/持久化/原子方案）、生产事故案例与预防、大 Key 检测方法、集群哈希标签实战模式、Streams 替代 Pub/Sub 的可靠消息方案。所有内容按场景组织，按需查阅降低 token 消耗。

  触发关键词：Redis、缓存、TTL、淘汰策略、集群、分布式锁、限流、消息队列、eviction、cluster
tags:
- 智能代理
- 数据存储
- 缓存优化
tools:
- read
- exec
---

# Redis 缓存大师（Redis Cache Master）

**不是命令清单，而是生产避坑指南。** 直击五大高频 Redis 生产事故：无 TTL 内存泄漏、淘汰策略错配、集群跨槽报错、原子性陷阱、大 Key 拖垮 eviction。提供决策树与模式库，让每次选型都有依据。

## 痛点与对策速查

| 用户痛点 | 事故场景 | 本系统对策 |
|:---|:---|:---|
| 内存泄漏 | 缓存键无 TTL，内存涨到 OOM | TTL 纪律：每个键必设过期 |
| 淘汰策略错配 | 缓存用 noeviction 导致写入失败 | 淘汰策略决策树：按场景选 |
| 集群跨槽报错 | MGET/MSET 跨槽报错 | 哈希标签模式：相关键同槽 |
| 原子性陷阱 | GET-then-SET 竞态条件 | 原子操作选择指南 |
| 大 Key 拖垮 | 单个 1GB key 导致 eviction 失效 | 大 Key 检测 + 拆分策略 |
| KEYS * 阻塞 | 生产用 KEYS 卡死全库 | SCAN 替代 + 异步扫描 |
| Pub/Sub 丢消息 | 订阅者离线时消息丢失 | Streams 替代：持久化+ACK |
| 持久化选型难 | 不知该用 RDB 还是 AOF | 持久化决策矩阵 |
| 连接管理差 | 频繁创建连接耗资源 | 连接池 + 管道优化 |
| 主从切换丢数据 | Sentinel 故障切换丢近期数据 | AOF everysec + 副本确认 |

## TTL 纪律（核心规则）

**每个缓存键必须设 TTL。** 无 TTL 的键会永远存活，最终导致内存泄漏。

| 命令 | TTL 设置 | 说明 |
|:---|:---|:---|
| `SET key value EX 3600` | 3600 秒 | 推荐写法 |
| `SETEX key 3600 value` | 3600 秒 | 等价旧写法 |
| `SET key value` | 无 TTL | ❌ 危险 |
| `SET key value KEEPTTL` | 保留旧 TTL | Redis 6+，更新值不丢 TTL |

### TTL 陷阱

| 陷阱 | 说明 | 解决 |
|:---|:---|:---|
| SET 覆盖丢失 TTL | `SET` 不带 EX 会清除原 TTL | 用 `SET ... KEEPTTL` 或重新设 EX |
| EXPIRE 后更新不重置 | 更新值后 TTL 仍倒计时 | 按需重设 EXPIRE |
| 懒过期占内存 | 过期键访问时才删 | 配置 `hz` 提高主动清理频率 |
| SCAN 仍显示过期键 | 清理周期未到 | 正常现象，访问时自动删除 |

### TTL 分级建议

| 数据类型 | 建议 TTL | 示例 |
|:---|:---|:---|
| 会话数据 | 30 分钟~24 小时 | `session:{id}` EX 1800 |
| 缓存查询结果 | 5~60 分钟 | `cache:query:{hash}` EX 600 |
| 限流计数器 | 按窗口 | `rate:{ip}:{minute}` EX 60 |
| 分布式锁 | 业务超时×1.5 | `lock:{resource}` EX 30 |
| 排行榜 | 不过期（主动更新） | `leaderboard:{game}` |
| 计数器 | 不过期（主动维护） | `counter:{entity}` |

## 淘汰策略决策树（差异化核心）

```text
数据是纯缓存吗？
├─ 是 → allkeys-lru（推荐）或 allkeys-lfu
│        所有键均可淘汰，LRU 最近最少使用
└─ 否（混合持久+缓存）
   ├─ 持久数据设了 TTL 吗？
   │  ├─ 是 → volatile-lru（只淘汰有 TTL 的）
   │  └─ 否 → noeviction（写入失败而非淘汰）
   └─ 数据可丢失吗？
      ├─ 是 → allkeys-lru
      └─ 否 → noeviction + 扩容
```

| 策略 | 淘汰范围 | 适用场景 | 风险 |
|:---|:---|:---|:---|
| allkeys-lru | 所有键，LRU | 纯缓存 | 持久数据被淘汰 |
| allkeys-lfu | 所有键，LFU | 访问频率差异大的缓存 | 同上 |
| volatile-lru | 仅有 TTL 的键 | 混合存储 | 无 TTL 键不淘汰 |
| volatile-lfu | 仅有 TTL 的键 | 同上 | 同上 |
| volatile-ttl | 有 TTL 的，优先快过期的 | TTL 分级缓存 | — |
| noeviction | 不淘汰 | 持久数据 | 写入失败需应用处理 |
| volatile-random | 随机有 TTL 的 | 低要求缓存 | 可能淘汰热数据 |

## 集群哈希标签模式（差异化核心）

Redis Cluster 用 16384 个哈希槽分布键。多键操作必须同槽。

### 哈希标签语法

```text
{user:1}:profile   →  槽由 "user:1" 决定
{user:1}:sessions  →  同槽（都由 "user:1" 哈希）
{user:1}:cart      →  同槽
```

### 同槽操作模式

```bash
# 相关键用相同哈希标签
SET {user:1}:profile '{"name":"Alice"}'
SET {user:1}:sessions "active"
HSET {user:1}:prefs theme dark lang zh

# 多键操作（同槽才能执行）
MGET {user:1}:profile {user:1}:sessions
MSET {user:1}:profile "updated" {user:1}:sessions "idle"
```

### 跨槽报错与解决

```text
错误：CROSSSLOT Keys in request don't hash to the same slot
原因：多键操作涉及不同槽的键
解决：
  1. 相关键加相同哈希标签 {tag}:key
  2. 或拆分为多次单键操作
  3. 或用 hash tag 让相关键落同槽
```

### 哈希标签设计原则

| 原则 | 说明 |
|:---|:---|
| 按实体分组 | 同实体的相关键用同一标签 |
| 避免热点 | 标签应分散，不要所有键用同一标签 |
| 标签即实体 ID | `{user:1}` 而非 `{all}` |
| 预估槽分布 | 确保标签均匀分布到各节点 |

## 原子操作选择指南（差异化核心）

```text
需要原子性吗？
├─ 单命令能完成？
│  ├─ 是 → 用 INCR/SETNX/DECR 等原子命令
│  └─ 否 → 需要多步
│     ├─ 步骤间有条件依赖？
│     │  ├─ 是 → WATCH/MULTI/EXEC 乐观锁
│     │  └─ 否 → Pipeline 批量
│     └─ 逻辑复杂？
│        └─ 是 → Lua 脚本（EVAL）
```

| 方案 | 适用场景 | 示例 |
|:---|:---|:---|
| 原子命令 | 单步操作 | `INCR counter` |
| SETNX | 分布式锁 | `SET lock NX EX 30` |
| WATCH/MULTI/EXEC | 条件更新 | 乐观锁 |
| Lua 脚本 | 复杂原子逻辑 | `EVAL "script" keys args` |
| Pipeline | 批量无依赖 | 减少往返 |

### 分布式锁模式（安全版）

```bash
# 加锁（NX 保证互斥，token 防误删）
SET lock:resource {unique_token} NX EX 30

# 解锁（Lua 保证"检查+删除"原子）
EVAL "
if redis.call('get', KEYS[1]) == ARGV[1] then
  return redis.call('del', KEYS[1])
else
  return 0
end
" 1 lock:resource {unique_token}
```

**关键**：解锁必须验证 token，否则会误删别人的锁。

### 限流模式

```text
固定窗口：
  INCR rate:{ip}:{minute}
  EXPIRE rate:{ip}:{minute} 60
  → 超过阈值则拒绝

滑动窗口（更精确）：
  ZADD rate:{ip} {timestamp_ms} {request_id}
  ZREMRANGEBYSCORE rate:{ip} 0 {now - 60000}
  ZCARD rate:{ip}
  → 超过阈值则拒绝

令牌桶（允许突发）：
  Lua 脚本实现：检查余量 → 消费 → 补充
```

## 可靠消息：Streams 替代 Pub/Sub（差异化核心）

Pub/Sub 的缺陷：消息不持久、订阅者离线丢消息、无 ACK 无重试。

| 特性 | Pub/Sub | Streams |
|:---|:---|:---|
| 持久化 | 否 | 是 |
| 离线消息 | 丢失 | 保留 |
| ACK 确认 | 无 | XACK |
| 重试 | 无 | XPENDING + XCLAIM |
| 消费者组 | 无 | 支持 |
| 顺序保证 | 无 | 严格顺序 |

### Streams 可靠消息模式

```bash
# 生产者
XADD events:* data "事件内容"

# 消费者组（一次性创建）
XGROUP CREATE events:* group1 0

# 消费者处理
XREADGROUP GROUP group1 consumer1 COUNT 10 BLOCK 5000 STREAMS events:* >

# 处理完成后确认
XACK events:* group1 {message_id}

# 检查未确认消息（重试）
XPENDING events:* group1
XCLAIM events:* group1 consumer2 60000 {message_id}
```

## 持久化决策矩阵（差异化核心）

| 场景 | RDB | AOF | 都开 | 都关 |
|:---|:---|:---|:---|:---|
| 纯缓存 | | | | ✅ |
| 允许少量丢失 | ✅ | | | |
| 最少丢失 | | ✅ everysec | | |
| 数据安全最高 | | | ✅ | |
| 快速恢复 | ✅ | | | |
| 恢复完整 | | ✅ | ✅ | |

### 配置建议

```text
# 纯缓存（数据可重建）
save ""              # 关闭 RDB
appendonly no        # 关闭 AOF

# 平衡（推荐大多数场景）
save 900 1           # RDB：15分钟内有1个变更则快照
save 300 10          # RDB：5分钟内有10个变更
appendonly yes
appendfsync everysec # AOF：每秒刷盘（最多丢1秒）

# 最高安全
save 60 10000        # 频繁 RDB
appendonly yes
appendfsync always   # 每条命令刷盘（性能低）
```

## 内存管理（关键）

| 配置/命令 | 作用 | 建议值 |
|:---|:---|:---|
| maxmemory | 内存上限 | 物理内存的 60-70% |
| maxmemory-policy | 淘汰策略 | 按决策树选 |
| INFO memory | 查看用量 | 监控 used_memory vs maxmemory |
| MEMORY USAGE key | 单键内存 | 检查大 Key |
| CONFIG SET maxmemory | 动态调整 | 不重启生效 |

### 大 Key 检测与拆分

```bash
# 扫描大 Key
redis-cli --bigkeys

# 检查单键
MEMORY USAGE mykey

# 查看键类型和大小
TYPE mykey
HLEN mykey   # hash 元素数
LLEN mykey   # list 长度
ZCARD mykey  # sorted set 数量
SCARD mykey  # set 数量
```

| 大 Key 类型 | 风险 | 拆分策略 |
|:---|:---|:---|
| 大 String（>10KB） | 网络阻塞、eviction 失效 | 拆为 Hash 或分片 |
| 大 List（>1万元素） | 阻塞操作、内存集中 | 分段 list 或 Stream |
| 大 Hash（>1万字段） | 同上 | 按字段分片到多键 |
| 大 Set（>1万元素） | 同上 | 分片 set |
| 大 ZSet（>1万元素） | 排序开销 | 分桶 zset |

## 常用数据结构场景

| 结构 | 被低估的用法 | 命令 |
|:---|:---|:---|
| Sorted Set | 滑动窗口限流、排行榜 | `ZADD` + `ZREMRANGEBYSCORE` |
| HyperLogLog | 唯一计数（12KB 算数十亿） | `PFADD` + `PFCOUNT` |
| Streams | 可靠消息队列 | `XADD` + `XREAD` + `XACK` |
| Hash | 对象存储（比 JSON 省内存） | `HSET` + `HGETALL` |
| Bitmap | 布隆过滤器、签到 | `SETBIT` + `GETBIT` |
| Geo | 地理位置 | `GEOADD` + `GEORADIUS` |

## 连接管理

| 策略 | 说明 | 收益 |
|:---|:---|:---|
| 连接池 | 复用连接 | 避免创建开销 |
| Pipeline | 批量发送不等响应 | 减少往返延迟 |
| MULTI/EXEC | 事务批量 | 原子+减少往返 |
| QUIT | 优雅关闭 | 释放服务端资源 |
| 超时设置 | 防止连接泄漏 | 客户端 read/write timeout |

## 常见生产事故与预防

| 事故 | 根因 | 预防 |
|:---|:---|:---|
| OOM 崩溃 | 无 maxmemory 或无 TTL | 设 maxmemory + 强制 TTL |
| KEYS * 阻塞 | 生产用了 KEYS | 用 SCAN 替代 |
| 写入失败 | noeviction + 内存满 | 换 allkeys-lru 或扩容 |
| 数据丢失重启 | 无持久化 | 开 AOF everysec |
| 跨槽报错 | 多键不同槽 | 用哈希标签 |
| 锁误删 | 解锁未验证 token | Lua 脚本验证后删 |
| 主从切换丢数据 | 异步复制延迟 | AOF everysec + WAIT 命令 |
| 大 Key 阻塞 | DEL 大 Key 卡主线程 | UNLINK 异步删除 |
| 缓存雪崩 | 大量键同时过期 | TTL 加随机抖动 |
| 缓存穿透 | 查不存在的 Key | 布隆过滤器 + 空值缓存 |

## 缓存模式

| 模式 | 流程 | 适用 |
|:---|:---|:---|
| Cache-aside | 查 Redis→miss→查 DB→写 Redis | 标准缓存 |
| Write-through | 写 DB+Redis 同步 | 缓存新鲜 |
| Write-behind | 写 Redis→异步写 DB | 高写入 |
| Read-through | 代理层自动回源 | 应用无感 |

## 真实场景示例

### 场景 1：用户会话缓存

```bash
# 存储会话（30分钟过期）
HSET session:{token} user_id 123 last_active {ts} ip {ip}
EXPIRE session:{token} 1800

# 更新活跃时间（保留 TTL）
HSET session:{token} last_active {new_ts}
EXPIRE session:{token} 1800  # 重置 TTL

# 检查会话
HGETALL session:{token}
```

### 场景 2：分布式锁

```bash
# 加锁
SET lock:order:123 "uuid-abc" NX EX 30

# 业务处理...

# 解锁（Lua 验证 token）
EVAL "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end" 1 lock:order:123 "uuid-abc"
```

### 场景 3：滑动窗口限流

```bash
# 每分钟最多 100 请求
ZADD rate:{ip} {now_ms} {request_uuid}
ZREMRANGEBYSCORE rate:{ip} 0 {now_ms - 60000}
COUNT=$(ZCARD rate:{ip})
EXPIRE rate:{ip} 120

if [ $COUNT -gt 100 ]; then
  echo "限流触发"
fi
```

## 常见问题 FAQ

**Q1：纯缓存该用哪种淘汰策略？**
A：allkeys-lru。所有键都是缓存，LRU 淘汰最久未用的最合理。

**Q2：maxmemory 设多少合适？**
A：物理内存的 60-70%。留余量给操作系统和 RDB fork（BGSAVE 需要内存副本）。

**Q3：RDB 和 AOF 能同时开吗？**
A：能。数据安全要求高时都开。重启时优先用 AOF 恢复（更完整），RDB 作为备份。

**Q4：集群最少几个节点？**
A：最少 3 主 3 从（6 节点）。3 主保证哈希槽全覆盖，3 从保证高可用。

**Q5：大 Key 怎么安全删除？**
A：用 `UNLINK`（Redis 4+）异步删除，不阻塞主线程。旧版本用 `DEL` 会阻塞。

## 故障排查

| 现象 | 排查命令 | 解决方案 |
|:---|:---|:---|
| 内存持续增长 | `INFO memory` | 检查 TTL；执行淘汰；清理大 Key |
| 写入失败 | `INFO stats` 看 evicted | 检查 maxmemory-policy |
| 响应变慢 | `SLOWLOG GET 10` | 找慢查询；避免 KEYS/大 Key |
| 连接数高 | `INFO clients` | 检查连接池配置；查泄漏 |
| 主从延迟 | `INFO replication` | 检查网络；减少大命令 |
| 槽未覆盖 | `CLUSTER NODES` | 重新分片；检查节点状态 |
| AOF 文件大 | `BGREWRITEAOF` | 定期重写压缩 |

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Redis**：5.0+（推荐 7.0+，支持 Streams/UNLINK 等新特性）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---|:---|:---|:---|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| Redis Server | 数据库 | 必需 | https://redis.io/download 或 Docker |
| redis-cli | 命令行工具 | 必需 | 随 Redis 安装 |
| Redis 客户端库 | 编程库 | 可选 | 按语言选择（ioredis/redis-py 等） |

### API Key 配置
- **本 Skill 无需 API Key**
- Redis 连接通过 `redis-cli` 或客户端库配置 host/port/password
- 生产环境建议配置 `requirepass` 或 ACL

### 可用性分类
- **分类**：MD+EXEC（Markdown 指令 + exec 命令行执行）
- **说明**：基于 Markdown 的 AI Skill 驱动 Agent 执行 Redis 操作。设计与决策指南纯 Markdown 可理解；实际命令执行需 Redis 环境与 redis-cli。
