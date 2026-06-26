# HEARTBEAT.md — self-evolution-cognition

## 心跳检查清单（每次 heartbeat 执行）

- [ ] `VERIFICATION_LOG.md` 是否存在且最近 24h 内有更新？
- [ ] 已知/未知分离缓存文件 `known_unknown_cache.json` 是否正常？
- [ ] 上次 `evolve()` 调用的置信度是否 ≥ 90%？
- [ ] 红线监控进程是否存活？

## 异常触发条件

| 条件 | 动作 |
|------|------|
| VERIFICATION_LOG.md 超过 48h 未更新 | 发送告警，触发自检 |
| 置信度连续 3 次低于 80% | 暂停任务，等待人类介入 |
| 检测到 `rm -rf` 等危险命令 | 立即拦截，写入红线日志 |
| 私有数据外泄风险 | 中断执行，通知用户 |

## 心跳状态

```json
{
  "skill": "self-evolution-cognition",
  "version": "1.0.0",
  "last_heartbeat": null,
  "status": "initialized",
  "consecutive_low_confidence": 0
}
```
