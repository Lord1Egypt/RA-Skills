# 定时任务排查指南

## 常见问题及解决方案

### 1. OpenClaw Cron 任务没有执行

**排查步骤**：

```bash
# 1. 检查任务是否存在
openclaw cron list

# 2. 检查 Gateway 是否运行
openclaw gateway status

# 3. 检查任务是否 enabled
openclaw cron list | grep <任务名>

# 4. 手动触发测试
openclaw cron run <jobId>

# 5. 查看运行历史
openclaw cron runs --id <jobId> --limit 10
```

**常见原因**：
- Gateway 未运行（cron 依赖 Gateway 进程）
- 任务被禁用（`enabled: false`）
- 时区错误（默认 UTC，中国需要 `Asia/Shanghai`）
- cron 表达式写错

---

### 2. 系统 Crontab 任务没有执行

**排查步骤**：

```bash
# 1. 确认 crontab 已添加
crontab -l

# 2. 检查日志
tail -50 /tmp/<task-name>.log

# 3. 检查脚本权限
ls -la /path/to/script.sh
# 需要有执行权限 (chmod +x)

# 4. 手动执行脚本
bash /path/to/script.sh

# 5. 检查 cron 服务
systemctl status cron
```

**常见原因**：
- 脚本没有执行权限（`chmod +x`）
- PATH 环境变量不完整（cron 环境很干净）
- 脚本路径错误
- cron 服务未运行
- 日志目录不存在

---

### 3. 飞书消息没有送达

**排查步骤**：

```bash
# 1. 检查 Agent 飞书账号配置
# 方法 A: 使用环境变量（推荐）
echo $OPENCLAW_AGENT_ID

# 方法 B: 查看您的配置文件（请谨慎操作）
# 注意：此命令仅用于查找您自己的配置，技能本身不访问这些文件
# grep -A 10 "agent-id" /path/to/your/openclaw.json

# 2. 检查 open_id 是否正确
# open_id 格式：ou_xxxxxxxxxxxx（完整 32+ 位）

# 3. 检查飞书应用权限
# 需要"以应用身份发消息"权限

# 4. 手动测试发送
openclaw agent --agent <id> --deliver \
  --reply-account <account> \
  --reply-to "user:<open_id>" \
  -m "测试消息"
```

**常见原因**：
- `--reply-to` 格式错误（必须是 `user:ou_xxx`）
- `--reply-account` 与 Agent 飞书账号不匹配
- 飞书应用缺少发消息权限
- open_id 不完整或错误
- 未使用 `--deliver` 参数

---

### 4. `openclaw agent` 命令报错

**常见错误**：

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `too many arguments for 'agent'` | 消息内容被当作位置参数 | 用 `-m "消息"` 明确指定 |
| `Delivering to Feishu requires target` | 缺少投递目标 | 添加 `--reply-account` 和 `--reply-to` |
| `gateway closed` | Gateway 未运行或连接断开 | `openclaw gateway restart` |
| `Session send visibility is restricted` | 跨 Agent 通信受限 | 用 `openclaw agent` 命令替代 |

---

### 5. 时间不对

**排查**：

```bash
# 检查系统时区
timedatectl

# 检查 OpenClaw 使用的时区
# cron 表达式默认用主机时区
# --at 时间不带时区默认 UTC

# 中国用户必须指定时区
--tz "Asia/Shanghai"           # cron 表达式
--at "2026-03-19T09:00:00+08:00"  # 一次性（带 +08:00）
```

**时区对照**：

| 写法 | 实际执行时间（北京） |
|------|-------------------|
| `--at "2026-03-19T09:00:00"` | 17:00（UTC 被当作北京时间差 8 小时） |
| `--at "2026-03-19T09:00:00Z"` | 17:00（UTC 明确标注） |
| `--at "2026-03-19T09:00:00+08:00"` | 09:00 ✅ |
| `--cron "0 9 * * *"` 无 --tz | 取决于主机时区 |
| `--cron "0 9 * * *" --tz "Asia/Shanghai"` | 09:00 ✅ |

---

### 6. 定时任务重试和失败

**OpenClaw Cron 重试机制**：

一次性任务（`--at`）：
- 临时错误（限流、网络）：最多重试 3 次（30s → 1m → 5m）
- 永久错误（认证、配置）：���即禁用

定期任务（`--cron`）：
- 任何错误：指数退避（30s → 1m → 5m → 15m → 60m）
- 成功后退避重置

**查看失败详情**：

```bash
openclaw cron runs --id <jobId> --limit 10
```

---

## 调试清单

创建定时任务后，按此清单验证：

- [ ] `openclaw cron list` 确认任务已创建
- [ ] 时区正确（`Asia/Shanghai`）
- [ ] `openclaw cron run <jobId>` 手动触发成功
- [ ] `openclaw cron runs --id <jobId>` 查看运行结果
- [ ] 飞书/目标渠道收到消息
- [ ] 日志无报错
