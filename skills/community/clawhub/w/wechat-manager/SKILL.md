---
name: wechat-manager
description: "微信智能管家：自动回复、消息分类、聊天记录分析、联系人管理。Trigger on: 微信, WeChat, 群聊, 朋友圈, 公众号, 聊天记录, 联系人, 表情包, 小程序, 红包."
version: 1.0.0
license: MIT
---

# WeChat Manager 💬

微信智能管家 — 通过微信官方 API 实现消息管理、自动回复和数据洞察的 OpenClaw Skill。

## What it does

- **消息管理**: 收发消息、群聊管理、自动回复规则
- **联系人管理**: 搜索联系人、分组管理、标签系统
- **聊天分析**: 消息频率统计、情感分析、高频词云
- **内容提取**: 从聊天记录提取待办、地址、日期等结构化信息
- **朋友圈监控**: 特定好友动态追踪
- **文件助手**: 自动归档聊天中的图片、文件、链接

## Trigger Conditions

Activate when user asks about:
- 查看微信消息、回复某人
- 分析聊天记录、统计群活跃度
- 管理联系人或群组
- 设置自动回复规则
- 提取聊天中的信息
- 微信文件管理

## Prerequisites

- 微信官方 API 接入（企业微信或服务号）
- `curl`, `jq`, `python3`
- Access Token 管理

## Installation

```
clawhub install clawto/wechat-manager
```

## Configuration

```
# 微信 API 配置
export WECHAT_CORP_ID=your_corp_id
export WECHAT_CORP_SECRET=your_corp_secret
export WECHAT_AGENT_ID=your_agent_id
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/msg.py` | 消息收发与格式转换 |
| `scripts/contacts.py` | 联系人搜索与管理 |
| `scripts/stats.py` | 聊天统计分析 |
| `scripts/auto-reply.py` | 自动回复规则引擎 |
| `scripts/extract.py` | 聊天内容智能提取 |

## Usage

```
# 查看未读消息
> 我有多少未读微信？

📬 未读消息: 47条 | 来自 12 个对话
🔝 最多: 工作群(15), 小明(8), 家人群(6)

# 搜索联系人
> 帮我找一下小明的微信

👤 小明 (备注: 大学同学)
📱 微信号: xiaoming_2024
🏷️ 标签: 同学, 老友

# 聊天分析
> 分析一下工作群这个月谁最活跃

📊 本月活跃度 TOP5:
1. 🥇 张三: 847条 | 图片 23张
2. 🥈 李四: 632条 | 链接 12个
3. 🥉 王五: 501条 | @所有人 8次
```

## 🫶 Donation

| Coin | Address |
|------|---------|
| BTC | `bc1pdah8vmmuctw3cxz0lsryh5rpzqn8jv546jma3auxpgxeqplrd32s4m68cs` |

## License

MIT
