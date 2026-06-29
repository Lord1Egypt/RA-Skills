# 告警阈值参考

## 系统资源阈值

| 指标 | 警告 (WARN) | 严重 (CRITICAL) | 说明 |
|------|------------|-----------------|------|
| CPU 负载 | > 1×核心数 | > 2×核心数 | 15min 平均负载 |
| 内存使用率 | > 75% | > 90% | used/total |
| 磁盘使用率 (/) | > 80% | > 90% | 根分区 |
| 磁盘使用率 (/home) | > 85% | > 95% | 数据分区 |
| SWAP 使用率 | > 50% | > 80% | 接近耗尽表示内存严重不足 |
| CPU 使用率 (单进程) | > 80% 持续 5min | > 95% 持续 2min | OpenClaw 进程自身 |

## OpenClaw 进程阈值

| 指标 | 正常 | 警告 | 严重 |
|------|------|------|------|
| Gateway 进程 | 存在 | — | 消失 |
| Gateway 内存 | < 500MB | 500-1000MB | > 1GB |
| Gateway 响应时间 | < 1s | 1-5s | > 5s 或无响应 |
| API 端口 (18792) | 通 | — | 不通 |
| OpenClaw 进程数 | ≥ 1 | — | 0 |

## 日志告警阈值

| 关键词 | 数量阈值 | 严重程度 | 说明 |
|--------|----------|----------|------|
| ERROR | ≥ 1 | CRITICAL | 任何 ERROR 都需关注 |
| FATAL | ≥ 1 | CRITICAL | 致命错误 |
| CRITICAL | ≥ 1 | CRITICAL | 严重错误 |
| WARN | > 5 | WARN | 5 个以下可忽略 |
| timeout | ≥ 1 | WARN | 超时可能影响响应 |
| reconnect | ≥ 3 | WARN | 频繁重连 |
| SIGSEGV | ≥ 1 | CRITICAL | 段错误/崩溃 |
| SIGABRT | ≥ 1 | CRITICAL | abort 信号 |
| OOM | ≥ 1 | CRITICAL | 内存耗尽 |

## 网络阈值

| 检查项 | 正常 | 警告 | 严重 |
|--------|------|------|------|
| Gateway HTTP /api/health | 200 OK | 超时 3s | 拒绝连接/5xx |
| 频道插件 ping | < 100ms | 100-500ms | > 500ms 或超时 |
| WebSocket 连接数 | < 50 | 50-200 | > 200 |

## 定时检查建议

建议配置 cron 定期检查，避免被动等待故障发生：

```cron
# 每 10 分钟健康检查，异常时发邮件通知
*/10 * * * * bash /root/.openclaw/workspace/skills/server-guardian/scripts/health_check.sh | tee -a /var/log/openclaw-health.log

# 每小时自动恢复（如有警告）
30 * * * * bash /root/.openclaw/workspace/skills/server-guardian/scripts/auto_recover.sh full >> /var/log/openclaw-recover.log 2>&1

# 每天凌晨 3 点整理日志
0 3 * * * bash /root/.openclaw/workspace/skills/server-guardian/scripts/auto_recover.sh logs
```
