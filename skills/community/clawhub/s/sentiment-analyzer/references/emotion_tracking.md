# 情绪追踪机制

## 什么是情绪追踪

情绪追踪用于监控一次客服会话中，客户情绪随时间的变化趋势。当检测到持续恶化时，自动告警并建议人工介入。

## 数据存储

追踪数据保存在 `/tmp/sentiment_tracking/{session_id}.json`

```json
[
  {"index": 1, "text": "客户消息...", "sentiment": "neutral", "score": 0.0, "timestamp": "..."},
  {"index": 2, "text": "客户消息...", "sentiment": "angry", "score": -0.5, "timestamp": "..."}
]
```

## 告警规则

### 规则1：情绪连续恶化
连续3条消息 score 持续下降，触发 escalation_alert

```
score_3 < score_2 < score_1 < 0
```

### 规则2：极端情绪
任何单条消息 score ≤ -0.8，触发紧急告警

### 规则3：高敏感词
检测到任意敏感词，立即触发 alert

## 集成到客服流程

```
1. 客户发消息
2. 调用: python3 scripts/track.py "消息" --session-id "会话ID"
3. 检查返回结果:
   - alert == true → 优先处理，使用 apologetic 语气
   - escalation_alert == true → 通知人工介入
   - reply_tone → 选择对应语气回复
4. 记录到对话历史
```

## 清除会话数据

会话结束后，删除追踪文件：
```bash
rm /tmp/sentiment_tracking/{session_id}.json
```