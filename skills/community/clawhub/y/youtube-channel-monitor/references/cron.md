# 定时任务设置

## 添加定时任务

```bash
openclaw cron add --name "YouTube 监控" \
  --schedule "every 1h" \
  --payload "agentTurn:运行 YouTube 频道检查脚本: python3 ~/.openclaw/workspace/skills/youtube-channel-monitor/scripts/youtube-monitor.py" \
  --delivery "announce:-1003899234137" \
  --session isolated
```

## 查看任务状态

```bash
openclaw cron list
```

## 手动触发

```bash
openclaw cron run <job-id>
```

## 注意事项

- 确保代理已开启（7897 端口）
- 首次运行需要安装依赖
- 无更新时不发送通知
