# Agent Memory V12 运维手册

> 凌晨3点被报警叫醒时，按这个手册操作。

## 快速诊断

```bash
# 1. 检查系统状态
agent-memory health

# 2. 检查组件降级
curl http://localhost:8000/v1/health/ready

# 3. 查看最近日志
tail -100 ~/.agent_memory/logs/agent_memory.log

# 4. 检查磁盘空间
df -h ~/.agent_memory/

# 5. 检查WAL文件大小
ls -lh ~/.agent_memory/*.wal
```

## 场景1：数据库锁定

### 症状
- API返回503 "系统繁忙"
- 日志中出现 "database is locked"
- 写入操作超时

### 止血步骤
1. 检查WAL文件大小：
   ```bash
   ls -lh ~/.agent_memory/*.wal
   ```
2. 如果WAL > 100MB，手动checkpoint：
   ```bash
   sqlite3 ~/.agent_memory/default.db "PRAGMA wal_checkpoint(TRUNCATE);"
   ```
3. 如果仍有锁定，检查活跃连接：
   ```bash
   sqlite3 ~/.agent_memory/default.db "SELECT * FROM pragma_list;"
   ```
4. 最后手段：重启服务
   ```bash
   # Docker
   docker compose restart agent-memory
   # 直接运行
   pkill -f agent-memory && agent-memory serve
   ```

### 验证恢复
```bash
curl http://localhost:8000/v1/health/ready
# 应返回 {"status": "ready", ...}
```

### 长期修复
- 设置 `AGENT_MEMORY_WAL_CHECKPOINT_INTERVAL=500`（更频繁checkpoint）
- 启用连接池 `AGENT_MEMORY_USE_CONNECTION_POOL=true`
- 检查是否有长时间运行的事务

## 场景2：磁盘空间不足

### 症状
- 写入操作失败
- 日志中出现 "disk I/O error"
- 备份失败

### 止血步骤
1. 检查磁盘使用：
   ```bash
   du -sh ~/.agent_memory/*
   du -sh ~/.agent_memory/backups/*
   ```
2. 清理旧备份（保留最近7天）：
   ```bash
   find ~/.agent_memory/backups/ -name "*.db" -mtime +7 -delete
   find ~/.agent_memory/backups/ -name "*.tar.gz" -mtime +7 -delete
   ```
3. 清理日志（保留最近3天）：
   ```bash
   find ~/.agent_memory/logs/ -name "*.log.*" -mtime +3 -delete
   ```
4. 清理软删除记忆：
   ```bash
   agent-memory purge-deleted
   ```

### 验证恢复
```bash
df -h ~/.agent_memory/
# 可用空间应 > 1GB
```

### 长期修复
- 设置自动备份清理 `AGENT_MEMORY_BACKUP_RETENTION_DAYS=7`
- 设置自动purge `AGENT_MEMORY_AUTO_PURGE_DAYS=30`
- 启用日志轮转 `AGENT_MEMORY_LOG_MAX_BYTES=10485760`

## 场景3：降级模式持续

### 症状
- health_check显示多个组件degraded
- 语义搜索不可用
- Spirit管家不响应

### 止血步骤
1. 检查组件状态：
   ```bash
   agent-memory health
   ```
2. 检查具体降级原因：
   ```bash
   curl http://localhost:8000/v1/health/ready | python -m json.tool
   ```
3. 常见降级原因及修复：

| 组件 | 常见原因 | 修复 |
|------|---------|------|
| embedding | sentence-transformers未安装 | `pip install agent-memory[embedding]` |
| fts5 | SQLite未编译FTS5 | 重新编译SQLite或使用系统SQLite |
| spirit | LLM函数未提供 | 检查llm_fn参数 |
| bm25 | jieba未安装 | `pip install agent-memory[chinese]` |

4. 重启服务使组件重新初始化：
   ```bash
   docker compose restart agent-memory
   ```

### 验证恢复
```bash
agent-memory health
# 所有组件应显示 healthy
```

## 场景4：备份恢复

### 症状
- 数据库损坏
- 误删重要记忆
- 系统启动失败

### 止血步骤
1. 停止写入（停止服务）：
   ```bash
   docker compose stop agent-memory
   ```
2. 查找最新备份：
   ```bash
   ls -lt ~/.agent_memory/backups/
   ```
3. 验证备份完整性：
   ```bash
   sqlite3 ~/.agent_memory/backups/latest.db "PRAGMA integrity_check;"
   ```
4. 恢复备份：
   ```bash
   # 方法1：使用CLI
   agent-memory restore --backup ~/.agent_memory/backups/latest.db

   # 方法2：手动替换
   cp ~/.agent_memory/default.db ~/.agent_memory/default.db.pre-restore
   cp ~/.agent_memory/backups/latest.db ~/.agent_memory/default.db
   ```
5. 重启服务：
   ```bash
   docker compose start agent-memory
   ```

### 验证恢复
```bash
agent-memory stats
# 记忆总数应与备份时一致
agent-memory recall "测试查询"
# 搜索应正常返回结果
```

### 重要提示
- 恢复前务必保留当前数据库副本
- 加密备份需要正确的加密密钥
- 恢复后建议立即创建新备份

## 告警配置

### Webhook通知
```bash
export AGENT_MEMORY_ALERT_WEBHOOK_URL=https://hooks.slack.com/services/xxx
export AGENT_MEMORY_ALERT_MIN_LEVEL=warning
```

### 告警类型

| 告警 | 级别 | 触发条件 |
|------|------|---------|
| 熔断器开启 | CRITICAL | Store操作连续失败5次 |
| 存储降级 | CRITICAL | 使用内存数据库运行 |
| 备份失败 | WARNING | 备份创建失败 |
| 磁盘空间不足 | WARNING/CRITICAL | 使用率>85%/>95% |
| LLM预算耗尽 | WARNING | 日调用达上限 |

## 紧急联系

| 场景 | 操作 |
|------|------|
| 数据丢失 | 从最新备份恢复，见场景4 |
| 服务不可用 | 重启服务，检查health |
| 性能骤降 | 检查WAL/磁盘/连接数 |
| 安全事件 | 立即轮换API Key和JWT Secret |
