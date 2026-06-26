# 舆情数据同步 - 增强版说明

## 🚀 新增功能

### 1. 自动重试机制
- **最大重试次数**：3 次
- **重试间隔**：60 秒
- **自动修复**：第 1 次重试前执行自动修复

### 2. 健康检查
每次同步前自动检查：
- ✅ Python3 环境
- ✅ .env 配置文件
- ✅ 主脚本文件
- ✅ 磁盘空间（>90% 告警）
- ✅ 缓存目录

### 3. 自动修复
发现问题自动修复：
- 🔧 .env URL 引号问题
- 🔧 Python 缓存清理
- 🔧 死锁文件清理
- 🔧 日志文件轮转（>10MB）

### 4. 状态追踪
- 📊 实时同步状态（JSON 格式）
- 📈 成功率统计
- 🔢 连续失败计数
- ⏱️ 执行耗时记录

### 5. 失败告警
- 连续失败 ≥3 次时发送告警
- 错误日志单独记录
- 健康检查失败时立即告警

### 6. 锁机制
- 防止并发执行
- 死锁自动检测（>10 分钟）
- 异常退出自动清理

---

## 📋 文件说明

| 文件 | 说明 |
|------|------|
| `sync.sh` | 增强版同步脚本（带重试和修复） |
| `monitor.sh` | 监控工具（查看状态、手动修复等） |
| `.sync_status.json` | 同步状态文件 |
| `.sync.lock` | 锁文件 |
| `sync.log` | 主日志 |
| `error.log` | 错误日志 |
| `alerts.log` | 告警日志 |
| `.cache/` | 缓存目录（Token、唯一键） |

---

## 🔧 使用方法

### 查看状态
```bash
bash monitor.sh status
```

### 查看日志
```bash
# 最近 20 条日志
bash monitor.sh logs

# 最近 50 条日志
bash monitor.sh logs 50
```

### 查看错误
```bash
bash monitor.sh errors
```

### 健康检查
```bash
bash monitor.sh health
```

### 手动修复
```bash
bash monitor.sh fix
```

### 手动执行同步
```bash
bash monitor.sh run
# 或
bash sync.sh
```

### 重置状态
```bash
bash monitor.sh reset
```

---

## 📊 状态文件示例

```json
{
    "last_run": "2026-03-13T21:52:41+08:00",
    "status": "success",
    "inserted_count": 22,
    "duration_seconds": 8,
    "retry_count": 0,
    "error_message": "",
    "consecutive_failures": 0
}
```

---

## 🔄 定时任务

已配置 cron，每 10 分钟执行一次：
```bash
*/10 * * * * /home/admin/.openclaw/workspace/skills/yuqing-data-to-bitable/sync.sh
```

---

## ⚠️ 故障排查

### 连续失败处理
```bash
# 1. 查看状态
bash monitor.sh status

# 2. 查看错误日志
bash monitor.sh errors

# 3. 执行健康检查
bash monitor.sh health

# 4. 尝试修复
bash monitor.sh fix

# 5. 手动执行测试
bash monitor.sh run
```

### 常见问题

**Q: 提示"BITABLE_URL 未初始化"**
```bash
# 检查 .env 文件
cat .env | grep BITABLE_URL

# 确保 URL 用引号包裹
BITABLE_URL='https://xxx.feishu.cn/base/XXX?table=XXX'
```

**Q: 提示"已有任务在运行"**
```bash
# 检查锁文件
ls -la .sync.lock

# 如果是死锁（超过 10 分钟），清理它
rm -f .sync.lock
```

**Q: 同步很慢**
```bash
# 检查缓存是否生效
bash monitor.sh health

# 查看 Token 缓存和唯一键缓存状态
ls -la .cache/
```

---

## 📈 性能优化

- **Token 缓存**：2 小时有效期
- **唯一键缓存**：5 分钟有效期
- **连接池**：复用 HTTP 连接
- **批量操作**：500 条/批（飞书上限）
- **分页优化**：500 条/页

---

## 🆘 需要帮助？

```bash
bash monitor.sh help
```

---

*版本：2.0.0（增强版）*  
*更新时间：2026-03-13*
