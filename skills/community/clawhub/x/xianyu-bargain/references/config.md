# 砍价配置指南

## 配置文件位置

`~/.openclaw/workspace/xianyu-bargain-state/config.json`

## 默认配置

```json
{
  "cronEnabled": false,
  "maxReplies": 5,
  "checkIntervalMin": 5,
  "maxFollowUps": 2,
  "followUpDelayMin": 30,
  "autoAcceptWithinMax": false,
  "notifyOnEveryReply": false,
  "messageStyle": "friendly"
}
```

## 配置项详解

### cronEnabled (自动监控开关)
- **默认**: false
- **说明**: 是否允许创建 cron job 自动监控卖家回复
- **设为true**: 仅在用户明确要求自动监控时设置
- **注意**: Agent 不得自行开启此选项，必须由用户明确同意

### maxReplies (最大回复次数)
- **默认**: 5
- **范围**: 1-10
- **说明**: 每个商品自动回复的最大次数，超过后停止自动回复并通知用户
- **建议**: 3-5次足够，太多可能引起卖家反感

### checkIntervalMin (检查间隔)
- **默认**: 5分钟
- **范围**: 5-30分钟
- **说明**: 多久检查一次卖家是否回复
- **建议**: 5-10分钟，太频繁可能触发风控

### maxFollowUps (最大跟进次数)
- **默认**: 2
- **范围**: 0-5
- **说明**: 卖家无回复时，最多发送几条跟进消息
- **建议**: 1-2次，不要太骚扰

### followUpDelayMin (跟进延迟)
- **默认**: 30分钟
- **说明**: 卖家无回复多久后发送跟进消息

### autoAcceptWithinMax (自动接受底价内还价)
- **默认**: false
- **说明**: 卖家还价在底价范围内时是否自动接受
- **设为true**: 自动接受底价范围内的还价（注意：会自动代你回复卖家，请确认了解风险）
- **设为false**: 所有还价都通知用户确认（推荐）

### notifyOnEveryReply (每次回复都通知)
- **默认**: false
- **说明**: 是否每次卖家回复都发通知
- **设为true**: 实时跟踪每条对话

### messageStyle (话术风格)
- **默认**: "friendly"
- **选项**: friendly / professional / casual / humorous

## 用户命令映射

| 用户说 | 配置变更 |
|--------|----------|
| 最多回复3次 | maxReplies = 3 |
| 监控间隔5分钟 | checkIntervalMin = 5 |
| 话术风格=幽默 | messageStyle = "humorous" |
| 话术=专业 | messageStyle = "professional" |
| 话术=随性 | messageStyle = "casual" |
| 话术=友好 | messageStyle = "friendly" |
| 每次都通知我 | notifyOnEveryReply = true |
| 还价都要确认 | autoAcceptWithinMax = false |

## 启动时配置示例

```
自动砍价：
链接：https://www.goofish.com/item?id=xxx
目标价：4500
底价：4800
最多回复：3        ← maxReplies
话术：幽默          ← messageStyle
间隔：5分钟        ← checkIntervalMin
```
