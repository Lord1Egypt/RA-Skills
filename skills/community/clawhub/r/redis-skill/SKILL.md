---
name: redis-skill
description: Redis 缓存和数据结构管理技能。通过自然语言操作 Redis，支持 String、Hash、List、Set、ZSet、Stream 等数据结构操作。当用户提到 Redis、缓存、消息队列、会话存储时使用此技能。
---

# Redis Skill - 高性能缓存与数据结构管理

通过自然语言，轻松操作 Redis，利用其丰富数据结构！

---

## 🎯 功能特点

### 核心能力
- **🚀 高速缓存** - String 类型的键值缓存操作
- **📦 对象存储** - Hash 结构存储和查询对象
- **📋 队列操作** - List 实现队列、栈
- **🎯 集合运算** - Set 的交并差集操作
- **📊 排序集合** - ZSet 排行榜、范围查询
- **📡 消息流** - Stream 消息队列
- **⚡ 性能分析** - 慢查询、内存分析

---

## 📋 使用场景

### 缓存场景
- "缓存用户信息，过期时间 1 小时"
- "批量查询缓存，不存在的从数据库加载"
- "更新缓存，设置过期时间"

### 排行榜场景
- "更新游戏分数排行榜"
- "查询前 10 名玩家"
- "查询玩家排名"

### 队列场景
- "异步任务队列，添加任务"
- "消费者取任务"
- "延迟队列实现"

### 分布式锁
- "获取分布式锁，防止重复执行"
- "释放锁"
- "检查锁状态"

---

## 🔧 前置条件

### 1. 安装 Redis 客户端

**安装 redis-cli:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-tools
```

**macOS:**
```bash
brew install redis
```

**Python 客户端（高级操作）:**
```bash
pip install redis
```

### 2. 连接 Redis

**使用 redis-cli:**
```bash
redis-cli -h localhost -p 6379
```

**使用环境变量:**
```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_PASSWORD=your_password
```

---

## 💻 常用操作

### String 操作 - 基础缓存

```bash
# 设置缓存，过期时间 3600 秒
SET user:123 "{'name': 'Alice', 'email': 'alice@example.com'}" EX 3600

# 获取缓存
GET user:123

# 批量获取
MGET user:123 user:456 user:789

# 原子递增（计数器）
INCR page_views
INCRBY download_counter 100

# 不存在才设置（分布式锁）
SETNX lock:task_123 1
```

### Hash 操作 - 对象存储

```bash
# 存储对象
HSET user:123 name Alice email alice@example.com age 28

# 获取单个字段
HGET user:123 name

# 获取所有字段
HGETALL user:123

# 批量获取
HMGET user:123 name email age

# 删除字段
HDEL user:123 age

# 检查字段是否存在
HEXISTS user:123 email

#获取所有字段名
HKEYS user:123

# 获取所有值
HVALS user:123
```

### List 操作 - 队列/栈

```bash
# 左侧插入（队列头部）
LPUSH queue:task "task_data_1"

# 右侧插入（队列尾部）
RPUSH queue:task "task_data_2"

# 左侧弹出（队列消费）
LPOP queue:task

# 右侧弹出（栈弹出）
RPOP queue:task

# 范围查询（分页）
LRANGE queue:task 0 9

# 列表长度
LLEN queue:task

# 阻塞弹出（生产者-消费者）
BLPOP queue:task 30
```

### Set 操作 - 集合运算

```bash
# 添加成员
SADD users:online user_123 user_456 user_789

# 检查成员是否存在
SISMEMBER users:online user_123

# 获取所有成员
SMEMBERS users:online

# 集合大小
SCARD users:online

# 随机获取 N 个成员
SRANDMEMBER users:online 3

# 交集（共同在线的群成员）
SINTER group1:members group2:members

# 并集（所有群成员）
SUNION group1:members group2:members

# 差集（在一个集合但不在另一个）
SDIFF group1:members group2:members

# 将结果存储到新集合
SINTERSTORE common_members group1:members group2:members
```

### ZSet 操作 - 排行榜

```bash
# 添加成员及分数
ZADD leaderboard 1500 player_123 2000 player_456 1800 player_789

# 更新分数
ZINCRBY leaderboard 100 player_123

# 查询排名（倒序）
ZREVRANGE leaderboard 0 9

# 查询排名（正序）
ZRANGE leaderboard 0 9

# 查询成员分数
ZSCORE leaderboard player_123

# 查询成员排名
ZREVRANK leaderboard player_123

# 按分数范围查询
ZRANGEBYSCORE leaderboard 1500 2000

# 按分数范围删除
ZREMRANGEBYSCORE leaderboard 0 1000

# 集合大小
ZCARD leaderboard
```

### Stream 操作 - 消息队列

```bash
# 添加消息
XADD logs "*" timestamp 1700000000 level "INFO" message "User login"

# 消费消息
XREAD STREAMS logs 0

# 创建消费者组
XGROUP CREATE logs consumers_group 0

# 消费者读取消息
XREADGROUP GROUP consumers_group consumer_1 STREAMS logs >

# 确认消息处理完成
XACK logs consumers_group message_id
```

---

## 🔍 高级功能

### 分布式锁

```bash
# 获取锁（SETNX + 过期时间）
SET lock:resource_123 "unique_id" NX EX 30

# 检查锁是否属于自己
GET lock:resource_123

# 释放锁（Lua 脚本保证原子性）
EVAL "
if redis.call('get', KEYS[1]) == ARGV[1] then
    return redis.call('del', KEYS[1])
else
    return 0
end
" 1 lock:resource_123 "unique_id"
```

### 慢查询日志

```bash
# 配置慢查询阈值（毫秒）
CONFIG SET slowlog-log-slower-than 10000

# 查看慢查询
SLOWLOG GET 10

# 清空慢查询日志
SLOWLOG RESET
```

### 内存分析

```bash
# 查看内存使用情况
INFO memory

# 查看键的内存占用
MEMORY USAGE user:123

# 查找大键
SCAN 0 MATCH * COUNT 100
```

### 批量操作

```bash
# 使用 Pipeline 减少网络往返
EVAL "
local results = {}
for i = 1, #KEYS do
    table.insert(results, redis.call('GET', KEYS[i]))
end
return results
" 3 key1 key2 key3
```

---

## ⚡ 性能优化

### 连接池配置
```python
import redis

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    socket_timeout=5
)
client = redis.Redis(connection_pool=pool)
```

### 批量操作优化
- 使用 Pipeline 批量执行命令
- 使用 MGET/MSET 批量键值操作
- 使用 Lua 脚本保证原子性

### 内存优化
- 合理设置键的过期时间
- 使用 Hash 存储对象而非多个 String 键
- 定期清理无用键
- 启用 RDB + AOF 持久化

---

## 🎓 示例对话

### 示例 1：缓存管理
**用户：** "缓存用户信息，过期时间 1 小时"

**AI：** "正在设置缓存..."
```bash
SET user:123 '{"id": 123, "name": "Alice", "email": "alice@example.com"}' EX 3600
```

### 示例 2：排行榜更新
**用户：** "更新玩家得分 1500，然后查询前 10 名"

**AI：** "更新分数并查询排行榜"
```bash
ZADD leaderboard 1500 player_123
ZREVRANGE leaderboard 0 9 WITHSCORES
```

### 示例 3：分布式锁
**用户：** "获取任务 456 的分布式锁，防止重复执行"

**AI：** "尝试获取分布式锁（30秒过期）"
```bash
SET lock:task_456 "unique_id_$(date +%s%N)" NX EX 30
```

---

## ⚠️ 注意事项

### 安全建议
1. **启用认证** - 配置 requirepass密码
2. **网络隔离** - 不要暴露到公网
3. **最小权限** - 使用不同的 Redis 实例隔离不同业务
4. **敏感数据加密** - 存储在 Redis 的敏感数据要加密

### 性能建议
1. **避免大键** - 大键会阻塞 Redis
2. **合理设置过期** - 防止内存泄漏
3. **使用 Pipeline** - 减少网络往返
4. **监控内存** - 设置 maxmemory 防止 OOM

---

## 📚 参考资料

- [Redis 官方文档](https://redis.io/docs/)
- [Redis 命令参考](https://redis.io/commands/)
- [Redis 性能优化](https://redis.io/topics/latency)

---

**开始使用：** 告诉我你的 Redis 操作需求，我会帮你生成相应的命令！🚀
