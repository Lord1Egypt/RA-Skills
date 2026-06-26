---
name: steam-lowest-price-skill
description: Monitor Steam game prices and alert when a game hits historical low or a user target price. Use when users ask to track Steam discounts, watch specific games, check current price vs historical low, or send periodic price alerts.
---

# Steam Lowest Price Skill

追踪 Steam 游戏价格，并在触发条件时提醒：
- 达到历史低价
- 低于目标价

## Data source
- CheapShark public API（免费）
- 提供当前最低价（商店最低价）与历史最低价（cheapestPriceEver）

## Quick start

### 1) 添加关注
```bash
python3 {baseDir}/scripts/steam_watch.py add --query "Hades" --target 30
```

### 2) 查看关注列表
```bash
python3 {baseDir}/scripts/steam_watch.py list
```

### 3) 手动检查一次
```bash
python3 {baseDir}/scripts/steam_watch.py check
```

### 4) 删除关注
```bash
python3 {baseDir}/scripts/steam_watch.py remove --appid 1145360
```

## Alert format
触发提醒时输出：
- 游戏名
- 当前价
- 历史低价
- 差价（当前价 - 历史低价）
- 链接（Steam 商店页）

## Suggested cron message (OpenClaw)
```text
运行 python3 /home/lei/.openclaw/workspace/skills/steam-lowest-price-skill/scripts/steam_watch.py check 。
如果有命中项目，把每一条提醒结果发给用户；
若无命中，回复“Steam 史低监控：本轮无触发”。
```
