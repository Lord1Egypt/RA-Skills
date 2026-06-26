# 定时任务设置

## 每日推荐推送

### 使用 OpenClaw Cron

```bash
# 添加每日 9:30 推送推荐股票的定时任务
openclaw cron add --name "daily-stock-picks" --schedule "0 30 9 * * *" --command "cd /root/.openclaw/workspace/skills/stock-portfolio/scripts && python3 daily_picks.py"
```

### 使用系统 crontab

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天 9:30 执行）
30 9 * * * cd /root/.openclaw/workspace/skills/stock-portfolio/scripts && python3 daily_picks.py | openclaw message send --target your-chat-id
```

## 预警检查

### 每 30 分钟检查一次预警

```bash
# OpenClaw Cron 格式（每 30 分钟）
openclaw cron add --name "stock-alerts-check" --schedule "0 */30 * * * *" --command "cd /root/.openclaw/workspace/skills/stock-portfolio/scripts && python3 portfolio_manager.py check-alerts"
```

### 系统 crontab 格式

```bash
# 每 30 分钟检查预警
*/30 * * * * cd /root/.openclaw/workspace/skills/stock-portfolio/scripts && python3 portfolio_manager.py check-alerts | grep -q "⚠️" && openclaw message send --target your-chat-id --message "$(cat)"
```

## 注意事项

1. **交易时间**: 建议在交易时间内设置检查（A 股：9:30-15:00）
2. **API 限流**: 避免过于频繁的请求（建议间隔 >= 30 秒）
3. **错误处理**: 添加适当的错误处理和重试机制
4. **通知渠道**: 配置正确的消息推送渠道

## 示例：完整的交易日监控

```bash
# 早上 9:25 - 发送开盘前推荐
25 9 * * 1-5 cd scripts && python3 daily_picks.py

# 每 30 分钟检查预警（9:30-15:00）
30,0 10-14 * * 1-5 cd scripts && python3 portfolio_manager.py check-alerts
0 15 * * 1-5 cd scripts && python3 portfolio_manager.py check-alerts

# 收盘后 15:05 - 发送当日总结
5 15 * * 1-5 cd scripts && python3 portfolio_manager.py summary
```

注意：以上 crontab 表达式假设工作日为周一到周五（1-5）。