---
name: solana-alerts
description: 创建和管理价格警报 — 当代币价格高于或低于目标值时通知用户。当用户想设置价格提醒、查看或删除警报时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: ["SOLANA_NETWORK"]
      bins: ["node"]
    emoji: "🔔"
---

# Solana 价格警报系统

## When to Use

- 用户想在代币达到某个价格时收到通知
- 用户想查看或删除已设置的警报
- 用户提到"提醒"、"通知"、"警报"、"到了xxxx通知我"

## Workflow

### 用户想设置价格警报

1. **确定代币** — 从用户消息中提取，或询问："监控哪个代币？"
2. **确定方向** — 判断用户是想在价格**上涨**还是**下跌**时通知
   - "SOL 到 200" → `above`（高于）
   - "SOL 跌到 100" → `below`（低于）
   - 如果不确定，询问："是价格高于还是低于这个值时通知你？"
3. **确定目标价** — 从用户消息中提取数字
4. **确认** — "好的，当 SOL 价格高于 $200 时通知你，确认吗？"
5. **执行** — `node skills/solana-alerts/scripts/create-alert.js <user_id> <token> <above|below> <price>`
6. **后续** — "警报已设置！你可以说'我的警报'来查看所有活跃警报"

### 用户想查看警报

1. `node skills/solana-alerts/scripts/list-alerts.js <user_id>`
2. 如果无警报，引导创建
3. 展示每个警报的代币、方向、目标价

### 用户想删除警报

1. 如果未指定 ID，先列出所有警报让用户选择
2. 确认："确定删除警报 #X 吗？"
3. `node skills/solana-alerts/scripts/delete-alert.js <user_id> <alert_id>`

### 手动检查价格触发

1. `node skills/solana-alerts/scripts/check-prices.js`
2. 将触发的警报信息通知用户

## Guardrails

- **最多 20 个警报** — 超出时提示用户清理旧警报
- **合理性检查** — 如果目标价偏离当前价格超过 50%，温和提醒用户确认
- **不预测价格** — 不说"SOL 很可能到 200"，只设置警报
- **不重复创建** — 如果已存在相同条件的警报，提醒用户

## Available Scripts

| 脚本 | 用途 | 参数 |
|------|------|------|
| `create-alert.js` | 创建警报 | `<user_id> <token> <above\|below> <price>` |
| `list-alerts.js` | 列出警报 | `<user_id> [--lang en]` |
| `delete-alert.js` | 删除警报 | `<user_id> <alert_id>` |
| `check-prices.js` | 手动检查 | （无参数） |
