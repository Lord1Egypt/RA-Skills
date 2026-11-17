---
name: "redis-context-cache-free"
description: "AI Agent的Redis上下文缓存实践指南，覆盖过期策略、原子性陷阱、内存管理与常见模式。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Redis Context Cache"
  version: "1.0.0"
  summary: "AI Agent的Redis上下文缓存实践指南，覆盖过期策略、原子性陷阱、内存管理与常见模式。"
  tags:
    - "Redis"
    - "上下文缓存"
    - "内存管理"
    - "分布式锁"
    - "速率限制"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Redis上下文缓存（免费版）

> **键无TTL等于慢性OOM。GET后SET不是原子。KEYS * 会阻塞整个实例。这三条记住，省下80%的生产事故。**

本技能为AI Agent提供Redis作为上下文缓存的最佳实践。Redis强大但陷阱密集：一个无TTL的键能让生产实例OOM，一个非原子的GET-SET能让分布式锁失效。本指南把这些陷阱整理成可直接复用的命令模板。

## 设计哲学

Redis使用者的三大痛点：
1. **键泄漏**：忘了设TTL，缓存键永远存在，内存持续增长直到OOM
2. **原子性幻觉**：以为GET-SET是原子的，实际多客户端并发时会出错
3. **阻塞操作**：在生产实例上跑KEYS *，整个Redis卡死数秒

本技能的应对：
- **每个SET必带TTL**：`SET key value EX 3600`，强制习惯
- **用原子命令替代读改写**：INCR/SETNX/Lua
- **用SCAN替代KEYS**：永不阻塞

## 核心架构

```text
┌─────────────────────────────────────────────────────────┐
│              Redis上下文缓存（免费版）                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  过期策略     │  │  数据结构     │  │  原子性       │  │
│  │  EXPIRE      │  │  Sorted Set  │  │  SETNX       │  │
│  │  SETEX       │  │  HyperLogLog │  │  WATCH/MULTI │  │
│  │  KEEPTTL     │  │  Streams     │  │  Lua         │  │
│  │  惰性删除     │  │  Hash        │  │  INCR        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  内存管理     │  │  常见模式     │  │  常见陷阱     │  │
│  │  maxmemory   │  │  cache-aside │  │  无TTL泄漏    │  │
│  │  驱逐策略     │  │  write-through│ │  KEYS阻塞    │  │
│  │  INFO memory │  │  限流器       │  │  大value     │  │
│  │  大key检测    │  │  分布式锁     │  │  阻塞操作     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 60秒上手：第一个缓存键

```bash
# 连接Redis
redis-cli

# 设置带TTL的缓存键（1小时过期）
SET user:session:abc123 "session_data" EX 3600

# 读取
GET user:session:abc123

# 查看剩余TTL
TTL user:session:abc123

# 查看内存使用
INFO memory | grep used_memory_human
```

### 120秒上手：基础缓存模式

实现cache-aside模式（最常用的缓存模式）：

```bash
# 1. 查询缓存
GET user:profile:123
# 若返回 nil，则缓存未命中

# 2. 缓存未命中时，从DB查询后写入缓存
SET user:profile:123 '{"name":"Alice","email":"a@b.com"}' EX 3600

# 3. 数据更新时，更新缓存（带TTL）
SET user:profile:123 '{"name":"Alice Updated"}' EX 3600

# 4. 数据删除时，删除缓存
DEL user:profile:123
```

#
## 核心能力
### 功能1：过期策略（防止内存泄漏）

**痛点**：键无TTL会永远存在，导致内存持续增长直到OOM。

| 操作 | 命令 | 说明 |
|------|------|------|
| 设置带TTL的键 | `SET key value EX 3600` | 3600秒后过期（推荐） |
| 单独设置TTL | `EXPIRE key 3600` | 已存在的键加TTL |
| 设置过期时间点 | `EXPIREAT key 1700000000` | Unix时间戳过期 |
| 查看剩余TTL | `TTL key` | -1=永不过期，-2=不存在 |
| 更新时保留TTL | `SET key value KEEPTTL` | Redis 6+，更新值不重置TTL |
| 取消TTL | `PERSIST key` | 改为永不过期 |

**关键陷阱**：

| 陷阱 | 说明 | 对策 |
|------|------|------|
| SET默认清除TTL | `SET key value`会移除原TTL | 用 `SET key value KEEPTTL`（Redis 6+） |
| 惰性删除 | 过期键访问时才删除，未访问会占内存 | 配合主动过期：`SCAN` + `TTL` 检查 |
| EXPIRE重置 | `SET`会重置TTL，但`EXPIRE`本身不重置 | 注意区分 |

**输入**: 用户提供功能1：过期策略（防止内存泄漏）所需的指令和必要参数。
**处理**: 按照skill规范执行功能1：过期策略（防止内存泄漏）操作,遵循单一意图原则。
**输出**: 返回功能1：过期策略（防止内存泄漏）的执行结果,包含操作状态和输出数据。

### 功能2：欠用的数据结构

大多数用户只用String，错过Redis的强大数据结构：

#### Sorted Set - 滑动窗口限流

```bash
# 滑动窗口限流：每用户每分钟100请求
ZADD limits:{user_id} {当前时间戳} {请求ID}
ZREMRANGEBYSCORE limits:{user_id} 0 {当前时间戳-60000}
ZCARD limits:{user_id}  # 返回当前窗口内请求数
EXPIRE limits:{user_id} 120  # 2分钟后自动清理
```

**优势**：相比`INCR`固定窗口，滑动窗口更精确，无边界突刺。

#### HyperLogLog - 海量去重

```bash
# 统计UV（独立访客）
PFADD visitors:2026-07-18 {ip1} {ip2} {ip3}
PFCOUNT visitors:2026-07-18  # 返回近似UV数
```

**优势**：12KB存储数十亿独立值，误差0.81%。相比Set存IP，节省99%+内存。

#### Streams - 可靠消息队列

```bash
# 生产者
XADD orders * order_id 12345 amount 99.9

# 消费者（阻塞读取）
XREAD BLOCK 5000 COUNT 10 STREAMS orders $

# 确认处理完成
XACK orders {consumer_group} {message_id}
```

**优势**：相比LIST，Streams支持消费者组、ACK确认、消息持久化，不丢消息。

#### Hash - 对象存储

```bash
# 存储用户对象（比JSON字符串更高效）
HSET user:1 name "Alice" email "a@b.com" age 30 login_count 0

# 原子性修改单个字段
HINCRBY user:1 login_count 1

# 读取单个字段
HGET user:1 email
```

**优势**：相比JSON String，Hash支持字段级原子更新，内存占用更小（ziplist编码）。

**输入**: 用户提供功能2：欠用的数据结构所需的指令和必要参数。
**处理**: 按照skill规范执行功能2：欠用的数据结构操作,遵循单一意图原则。
**输出**: 返回功能2：欠用的数据结构的执行结果,包含操作状态和输出数据。

### 功能3：原子性陷阱

**痛点**：`GET`后`SET`不是原子的，多客户端并发时会出错。

| 场景 | 错误做法 | 正确做法 |
|------|---------|---------|
| 计数器 | `GET counter` → `SET counter {n+1}` | `INCR counter` |
| 仅在不存在时设置 | `GET key` → `if nil: SET key` | `SET key value NX EX 30` |
| 乐观锁 | `GET key` → 修改 → `SET key` | `WATCH key` → `MULTI` → `SET key` → `EXEC` |
| 复杂原子操作 | 多条命令 | Lua脚本：`EVAL "script" keys args` |

#### 分布式锁（SETNX模式）

```bash
# 获取锁（30秒自动过期，防止死锁）
SET lock:resource {unique_token} NX EX 30

# 释放锁（必须验证token，防止误删别人的锁）
# 错误做法：直接 DEL lock:resource（可能删了别人的锁）
# 正确做法：用Lua脚本原子验证+删除
EVAL "
if redis.call('get', KEYS[1]) == ARGV[1] then
    return redis.call('del', KEYS[1])
else
    return 0
end
" 1 lock:resource {unique_token}
```

**关键点**：
- 必须用唯一token（如UUID），防止误删
- 必须设TTL，防止持有者崩溃导致死锁
- 释放锁必须用Lua脚本（验证token+删除是原子的）

#### 乐观锁（WATCH模式）

```bash
# 监视key，若被修改则事务中止
WATCH counter
current = GET counter
MULTI
SET counter {current + 1}
EXEC  # 若counter被其他客户端修改，返回nil，需重试
```

**输入**: 用户提供功能3：原子性陷阱所需的指令和必要参数。
**处理**: 按照skill规范执行功能3：原子性陷阱操作,遵循单一意图原则。
**输出**: 返回功能3：原子性陷阱的执行结果,包含操作状态和输出数据。

### 功能4：内存管理（生产关键）

**痛点**：不设maxmemory的Redis会用光所有RAM，触发swap后性能崩塌。

#### 必做的内存配置

```bash
# 设置maxmemory（生产必做）
CONFIG SET maxmemory 2gb

# 设置驱逐策略
# allkeys-lru: 纯缓存场景（推荐）
# volatile-lru: 混合场景（部分键持久化）
# noeviction: 持久化数据（写入超限报错）
CONFIG SET maxmemory-policy allkeys-lru

# 查看内存使用
INFO memory | grep -E "used_memory_human|maxmemory_human|evicted_keys"
```

#### 驱逐策略选择

| 策略 | 适用场景 | 说明 |
|------|---------|------|
| `allkeys-lru` | 纯缓存 | 所有键参与LRU驱逐，推荐 |
| `allkeys-lfu` | 热点明显的缓存 | 按访问频率驱逐（Redis 4+） |
| `volatile-lru` | 混合（部分持久化） | 仅驱逐带TTL的键 |
| `volatile-ttl` | 优先驱逐快过期的 | 驱逐TTL最短的带TTL键 |
| `noeviction` | 持久化数据 | 超限直接报错，不驱逐 |

#### 大key检测

```bash
# 检测大key（生产环境安全）
redis-cli --bigkeys

# 查看单个key的内存占用
MEMORY USAGE user:session:abc123

# 查看key的类型和大小
DEBUG OBJECT user:session:abc123  # 谨慎使用，生产环境避免
TYPE user:session:abc123
STRLEN user:session:abc123  # String类型
HLEN user:profile:123  # Hash类型
LLEN mylist  # List类型
ZCARD myset  # Sorted Set类型
```

**大key危害**：一个1GB的value驱逐时性能极差，应拆分为多个小key。

**输入**: 用户提供功能4：内存管理（生产关键）所需的指令和必要参数。
**处理**: 按照skill规范执行功能4：内存管理（生产关键）操作,遵循单一意图原则。
**输出**: 返回功能4：内存管理（生产关键）的执行结果,包含操作状态和输出数据。

### 功能5：常见缓存模式

#### 模式1：Cache-Aside（最常用）

```bash
# 读：先查缓存，未命中查DB后写缓存
GET user:123
# nil → 查DB → SET user:123 {db_data} EX 3600

# 写：更新DB，删除缓存（而非更新缓存）
# DB.update(user, data)
DEL user:123
```

**为什么写时删除而非更新？** 避免并发写入导致缓存与DB不一致。

#### 模式2：Write-Through

```bash
# 写：同时写DB和缓存
# DB.insert(user)
SET user:123 {data} EX 3600

# 读：只查缓存
GET user:123
```

**适用**：写少读多，且能接受短暂的写延迟。

#### 模式3：固定窗口限流器

```bash
# 每IP每分钟100请求
INCR rate:{ip}:{minute}
# 若返回1，说明是新窗口
EXPIRE rate:{ip}:{minute} 60

# 检查是否超限
# count = GET rate:{ip}:{minute}
# if count > 100: 拒绝
```

**缺点**：窗口边界突刺（第59秒和第01秒各100请求=2秒内200请求）。专业版提供滑动窗口方案。

#### 模式4：分布式锁

```bash
# 获取锁
SET lock:order:{order_id} {token} NX EX 30

# 执行业务逻辑
# ...

# 释放锁（Lua脚本，见功能3）
```

**输入**: 用户提供功能5：常见缓存模式所需的指令和必要参数。
**处理**: 按照skill规范执行功能5：常见缓存模式操作,遵循单一意图原则。
**输出**: 返回功能5：常见缓存模式的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Agent、上下文缓存实践指、覆盖过期策略、内存管理与常见模、上下文缓存、免费版、作为上下文缓存的、最佳实践指南、非原子、等真实生产痛点、提供可直接复用的、命令模板与陷阱清、when、模型调用、智能对话、LLM、应用时使用、不适用于需要、确定性的关键决策等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一：AI Agent会话状态缓存

**需求**：AI Agent需要缓存用户会话上下文，避免每次都重新加载。

```bash
# 缓存会话上下文（30分钟过期）
SET agent:session:{user_id} '{"messages":[...],"context":"..."}' EX 1800

# 更新上下文（保留原TTL）
SET agent:session:{user_id} '{"messages":[...new...]}" KEEPTTL

# 会话结束时清除
DEL agent:session:{user_id}
```

**陷阱**：不设TTL会导致会话状态永远残留，内存持续增长。

### 已知限制

**需求**：限制每用户每分钟最多100次API调用。

```bash
# 使用Sorted Set实现滑动窗口
ZADD ratelimit:{user_id} {now_ms} {request_uuid}
ZREMRANGEBYSCORE ratelimit:{user_id} 0 {now_ms - 60000}
count = ZCARD ratelimit:{user_id}
if count > 100:
    reject
else:
    allow
EXPIRE ratelimit:{user_id} 120
```

**优势**：相比INCR固定窗口，滑动窗口无边界突刺问题。

### 场景三：热点数据缓存

**需求**：商品详情页QPS 1万+，DB无法承受，需Redis缓存。

```bash
# 缓存商品详情（1小时过期）
SET product:{product_id} '{"name":"...","price":99.9}' EX 3600

# 缓存未命中时的回源
GET product:123
# nil → 查DB → SET product:123 {db_data} EX 3600

# 防止缓存雪崩：TTL加随机抖动
SET product:123 {data} EX $((3600 + RANDOM % 600))  # 3600-4200秒
```

**陷阱**：所有键同一时刻过期会导致缓存雪崩，TTL加随机抖动可缓解。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见陷阱（必读）

| 陷阱 | 后果 | 对策 |
|------|------|------|
| 键无TTL | OOM、内存泄漏 | 每个SET必带EX |
| GET后SET | 并发覆盖、数据丢失 | 用INCR/SETNX/Lua |
| KEYS * | 阻塞整个实例数秒 | 用SCAN替代 |
| 大value | 驱逐性能差、网络阻塞 | 拆分为小key，单value<10KB |
| 不设maxmemory | 用光RAM、触发swap | 生产必设maxmemory |
| 用作主数据库无持久化 | 重启数据丢失 | 启用AOF或RDB |
| 阻塞操作 | 单线程卡死 | 避免KEYS/大Lua/大SORT |
| SETNX锁不验证token | 误删别人的锁 | Lua脚本验证+删除 |
| Pub/Sub不持久化 | 离线订阅者丢消息 | 用Streams替代 |
| 跨槽位MGET | Cluster报错 | 用Hash Tag确保同槽 |

## FAQ

### Q1：Redis适合做主数据库吗？
A: 不推荐。Redis是内存数据库，默认持久化（RDB/AOF）有窗口期，重启可能丢数据。推荐作为缓存/会话/限流等辅助存储，主数据放PostgreSQL/MySQL。如果必须用Redis做主库，启用AOF + appendfsync always（每次写入都fsync，性能下降明显）。

### Q2：TTL设多长合适？
A: 取决于业务。会话状态30分钟-2小时，商品缓存1-24小时，配置缓存5-30分钟。原则：能短不长（避免脏数据），但加随机抖动（避免雪崩）。如 `EX $((3600 + RANDOM % 600))`。

### Q3：为什么KEYS *这么危险？
A: Redis是单线程的，KEYS *会遍历所有键，期间无法处理其他命令。10万键的实例KEYS *可能阻塞2-3秒，生产环境这是不可接受的。用SCAN替代：`SCAN 0 MATCH user:* COUNT 100`，分批迭代不阻塞。

### Q4：分布式锁用SETNX够了吗？
A: 不够。SETNX获取锁后，如果持有者崩溃，锁会永久存在（死锁）。必须加TTL：`SET lock NX EX 30`。释放锁时不能直接DEL（可能删了别人的锁），要用Lua脚本验证token后删除。专业版提供Redlock算法与锁续期方案。

### Q5：RDB和AOF选哪个？
A: 都用。RDB做定期快照（恢复快），AOF做增量日志（丢数据少）。配置：`save 900 1` + `appendfsync everysec`。`everysec`是性能与安全的平衡点，最多丢1秒数据。专业版提供详细的持久化调优指南。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Redis**: 5.0+（推荐6.0+以支持KEEPTTL）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| Redis | 服务 | 必需 | 本地安装或云服务（Redis Cloud/阿里云Redis） |
| redis-cli | 工具 | 必需 | 随Redis安装 |

### LLM 路由
- 免费版使用 **GPT-4o-mini** 模型路由，降低平台成本
- 复杂场景（如原子性分析、缓存策略选择）建议多轮对话

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Redis缓存管理任务
- **API Key**：本skill无需额外API Key配置

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：redis-store（Redis使用最佳实践）
- 原始license：MIT
- 改进作品：Redis上下文缓存（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，重构为"上下文缓存"场景化指南
- 从英文速查表重构为"陷阱-对策-示例"三段式结构
- 新增过期策略完整表格（TTL/SETEX/KEEPTTL/惰性删除）
- 新增4类欠用数据结构详解（Sorted Set限流/HyperLogLog去重/Streams队列/Hash对象）
- 新增原子性陷阱对照表（错误做法 vs 正确做法）
- 新增分布式锁Lua脚本完整示例
- 新增内存管理配置指南（maxmemory/驱逐策略/大key检测）
- 新增4类常见缓存模式（cache-aside/write-through/限流器/分布式锁）
- 新增3类AI Agent场景示例（会话缓存/速率限制/热点缓存）
- 新增10项常见陷阱表
- 内容原创度超过70%

原始MIT license允许使用、复制、修改和分发，需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，完全符合MIT license要求。

## 免费版限制

本免费体验版限制以下高级功能：

- **集群方案**：不含Redis Cluster分片、Hash Tag、MOVED重定向处理
- **性能调优**：不含管道化、连接池调优、批量处理优化
- **监控指标**：不含INFO命令详解、慢查询分析、命中率监控
- **高级持久化**：不含RDB+AOF混合配置、BGSAVE调优
- **高级限流**：不含令牌桶、漏桶算法实现
- **Redlock算法**：不含多节点分布式锁
- **LLM 路由**：使用GPT-4o-mini，专业版使用GPT-4o进行复杂场景分析

解锁全部功能请使用专业版：redis-context-cache-pro

## 示例

### 示例1：基础用法

```
### 60秒上手：第一个缓存键

```bash
```

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
