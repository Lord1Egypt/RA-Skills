---
name: sentiment-analyzer
description: 客服场景文本情绪分析工具。当需要对客户消息进行情绪识别（愤怒/焦虑/中性/满意/热情）、敏感词检测、情绪波动告警时使用。适用于：自动调整回复语气、触发紧急转接、投诉分级处理、NPS情绪追踪。触发词：情绪分析、情感检测、客户情绪、愤怒检测、情绪告警、sentiment。
---

# 情感分析器 (Sentiment Analyzer)

客服销售总监卡耐基的专用情绪分析工具，基于本地规则引擎，无需外部 API。

## 快速使用

运行分析脚本，传入客户文本：

```bash
python3 scripts/analyze.py "客户的消息内容"
```

输出结构化 JSON，包含情绪分类、敏感词列表、告警标记。

## 输出格式

```json
{
  "sentiment": "angry|anxious|neutral|satisfied|enthusiastic",
  "score": -1.0 到 1.0,
  "keywords": ["检测到的负面关键词"],
  "sensitive_words": ["敏感词列表"],
  "alert": true|false,
  "alert_reason": "触发告警的原因",
  "reply_tone": "apologetic|calm|neutral|positive|enthusiastic"
}
```

## 情绪分类规则

| 情绪 | 触发条件 | 回复语气 |
|:--|:--|:--|
| `angry` | 负面词≥2 或含敏感词 或含强烈否定 | `apologetic` |
| `anxious` | 含担忧/急切词汇 | `calm` |
| `neutral` | 无明显情绪信号 | `neutral` |
| `satisfied` | 含正面词汇 | `positive` |
| `enthusiastic` | 含热情/赞叹词汇 | `enthusiastic` |

## 告警触发条件

满足以下任一条件时 `alert: true`：
1. 情绪为 `angry` 且 score < -0.5
2. 检测到敏感词
3. 情绪波动：连续 3 条消息 score 持续下降

## 回复语气映射

根据情绪自动推荐回复语气，详见 [references/reply_tone.md](references/reply_tone.md)。

## 集成指引

### 在对话流程中使用

当收到客户消息时，调用 `analyze.py` 获取情绪分析结果，据此调整回复策略：

- `apologetic`：立即道歉，表达理解，承诺解决
- `calm`：温和安抚，确认问题，给出时间表
- `neutral`：专业中性，提供解决方案
- `positive`：积极回应，强调价值
- `enthusiastic`：热情回应，感谢信任

### 情绪追踪

使用 `track.py` 记录对话中连续的情绪变化，用于判断是否需要人工介入：

```bash
python3 scripts/track.py "客户消息" --session-id "会话ID"
```

详见 [references/emotion_tracking.md](references/emotion_tracking.md)。