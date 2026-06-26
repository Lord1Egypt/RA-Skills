# Cron Job Templates

Ready-to-use cron job definitions for post-restore rebuild. Adapt the message text to your setup.

## Memory Backup (every 6 hours)

```json
{
  "name": "Memory Backup",
  "schedule": { "kind": "cron", "expr": "0 */6 * * *", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "定时记忆备份。执行以下操作：\n1. cd 到 workspace 目录\n2. git add -A\n3. git status 检查是否有变更\n4. 如有变更，git commit 并 push 到 origin\n5. 记录备份结果到今天的日志\n如果 git remote 未配置，先配置 remote。",
    "timeoutSeconds": 180
  },
  "delivery": { "mode": "none" },
  "enabled": true
}
```

## Nightly Optimization (adjust schedule to your timezone)

```json
{
  "name": "Nightly Optimization",
  "schedule": { "kind": "cron", "expr": "0 19 * * *", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "夜间主动优化。执行以下任务：\n1. 记忆整理 — 回顾最近 3 天日志，更新 MEMORY.md\n2. 安全检查 — 检查 workspace 文件完整性\n3. Git 备份 — 确保最新文件已 commit\n4. 清理过期状态文件\n只做可逆的、低风险的优化。不发消息、不改生产配置。",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "announce" },
  "enabled": true
}
```

## Daily Community Scan (optional, adjust to your community)

```json
{
  "name": "Daily Community Scan",
  "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "每日社区热榜扫描。执行以下操作：\n1. 访问社区热门帖子\n2. 记录 Top 5 热帖（标题、作者、热度、核心观点）\n3. 写入今天的日志 memory/YYYY-MM-DD.md\n4. 如果有特别有价值的洞察，记录到 MEMORY.md",
    "timeoutSeconds": 180
  },
  "delivery": { "mode": "none" },
  "enabled": true
}
```
