# 微信助手数据格式规范

## 目录
1. [聊天记录格式](#聊天记录格式)
2. [知识库格式](#知识库格式)
3. [分析结果格式](#分析结果格式)
4. [审核请求格式](#审核请求格式)

---

## 聊天记录格式

### 输入格式 (chat_records.json)
```json
{
  "status": "success",
  "contact": "联系人名称",
  "count": 100,
  "timestamp": "2024-01-01T12:00:00",
  "messages": [
    {
      "content": "消息内容",
      "time": "14:30",
      "is_from_me": false,
      "contact": "张三"
    }
  ]
}
```

### 字段说明
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| status | string | 是 | 状态: success/error |
| contact | string | 是 | 联系人名称 |
| count | integer | 是 | 消息数量 |
| timestamp | string | 是 | 抓取时间(ISO格式) |
| messages | array | 是 | 消息列表 |
| messages[].content | string | 是 | 消息文本内容 |
| messages[].time | string | 否 | 消息时间(HH:mm格式) |
| messages[].is_from_me | boolean | 是 | 是否为发送的消息 |

---

## 知识库格式

### 知识库文件 (kb_data.json)
```json
{
  "samples": [
    {
      "input": "用户输入示例",
      "output": "回复示例",
      "intent": "schedule",
      "tags": ["工作", "会议"],
      "added_at": "2024-01-01T12:00:00"
    }
  ],
  "intents": {
    "schedule": {
      "patterns": ["明天", "几点", "时间"],
      "responses": ["好的，记下了"]
    }
  },
  "templates": {
    "greeting": [
      {"content": "你好！", "added_at": "2024-01-01T12:00:00"}
    ]
  },
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| samples | array | 学习样本列表 |
| samples[].input | string | 用户输入 |
| samples[].output | string | 对应回复 |
| samples[].intent | string | 意图分类 |
| samples[].tags | array | 标签 |
| intents | object | 意图模式映射 |
| intents.{name}.patterns | array | 匹配模式关键词 |
| intents.{name}.responses | array | 回复列表 |
| templates | object | 回复模板 |
| templates.{type} | array | 指定类型的模板 |

---

## 分析结果格式

### 完整分析输出 (analysis_result.json)
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00",
  "total_messages": 100,
  "keywords": [
    {"word": "会议", "score": 2.5}
  ],
  "frequency": {
    "time_distribution": {
      "morning": 15,
      "afternoon": 30,
      "evening": 45,
      "night": 10
    },
    "contact_frequency": {
      "张三": 50,
      "李四": 30
    },
    "total_messages": 100
  },
  "intents": {
    "distribution": {
      "schedule": 20,
      "meeting": 15,
      "question": 25,
      "greeting": 10,
      "general": 30
    },
    "percentages": {
      "schedule": 20.0,
      "meeting": 15.0,
      "question": 25.0,
      "greeting": 10.0,
      "general": 30.0
    }
  },
  "sentiment": {
    "positive": 45,
    "negative": 10,
    "neutral": 45,
    "percentages": {
      "positive": 45.0,
      "negative": 10.0,
      "neutral": 45.0
    }
  },
  "requirements": [
    {
      "type": "schedule",
      "content": "明天上午10点",
      "source": "明天下午有空吗？我们明天上午10点...",
      "contact": "张三"
    }
  ],
  "interaction_pattern": {
    "total_exchanges": 25,
    "avg_exchange_length": 4.2,
    "longest_exchange": 12
  },
  "insights": [
    "主要沟通类型是question，占比25条消息",
    "整体沟通氛围偏积极正向"
  ]
}
```

### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| keywords | array | 关键词及重要性评分 |
| frequency | object | 聊天频率分析 |
| frequency.time_distribution | object | 时段分布 |
| frequency.contact_frequency | object | 各联系人消息数 |
| intents | object | 意图分布 |
| intents.distribution | object | 各意图消息数 |
| intents.percentages | object | 各意图百分比 |
| sentiment | object | 情感分析 |
| sentiment.positive/negative/neutral | integer | 各情感消息数 |
| requirements | array | 识别的需求 |
| requirements[].type | string | 需求类型 |
| interaction_pattern | object | 互动模式 |
| insights | array | 分析洞察 |

---

## 审核请求格式

### 自动回复审核 (reply_history.json)
```json
[
  {
    "id": "req_20240101120000",
    "timestamp": "2024-01-01T12:00:00",
    "contact": "张三",
    "input_message": "明天下午有空吗？",
    "candidates": [
      {
        "text": "好的，明天下午我有空",
        "source": "kb_generated",
        "confidence": 0.85,
        "type": "kb_generated"
      }
    ],
    "status": "pending_audit",
    "audit_result": {
      "request_id": "req_20240101120000",
      "decision": "approve",
      "selected_reply": "好的，明天下午我有空",
      "ready_to_send": true,
      "sent_at": "2024-01-01T12:05:00"
    }
  }
]
```

### 审核流程
1. **生成请求** → `auto_reply.py --action generate`
2. **审核决策** → `auto_reply.py --action audit --request_id xxx --decision approve/modify/reject`
3. **执行发送** → `auto_reply.py --action send --request_id xxx`

### 审核选项
| 选项 | 说明 | 参数 |
|------|------|------|
| approve | 批准最高置信度回复并发送 | 无 |
| modify | 使用修改后的文本发送 | --modified_text "新文本" |
| reject | 拒绝本次回复 | 无 |

---

## 示例数据

### 示例1: 聊天记录样本
```json
{
  "status": "success",
  "contact": "张三",
  "count": 5,
  "timestamp": "2024-01-15T14:30:00",
  "messages": [
    {"content": "你好", "time": "14:00", "is_from_me": false, "contact": "张三"},
    {"content": "你好，请问有什么事吗？", "time": "14:01", "is_from_me": true, "contact": "张三"},
    {"content": "明天下午有个会议，想确认下你有没有空", "time": "14:02", "is_from_me": false, "contact": "张三"},
    {"content": "明天下午可以的，几点？", "time": "14:03", "is_from_me": true, "contact": "张三"},
    {"content": "下午3点，在会议室A", "time": "14:05", "is_from_me": false, "contact": "张三"}
  ]
}
```

### 示例2: 知识库样本
```json
{
  "samples": [
    {
      "input": "明天下午有空吗",
      "output": "可以的，请问是什么事情？",
      "intent": "schedule",
      "tags": ["预约", "时间"]
    },
    {
      "input": "好的，明天见",
      "output": "好的，明天见！",
      "intent": "confirm",
      "tags": ["确认"]
    }
  ],
  "intents": {
    "schedule": {
      "patterns": ["明天", "后天", "几点", "时间", "有空"],
      "responses": ["好的，记下了", "没问题"]
    }
  }
}
```

---

## 验证规则

### 消息验证
- `content` 不能为空字符串
- `is_from_me` 必须为 boolean
- `time` 格式为 HH:mm 或空字符串

### 知识库验证
- `samples` 数组元素必须包含 `input` 字段
- `intent` 必须为已定义的意图类型
- `patterns` 数组不能为空

### 分析结果验证
- `total_messages` 必须为非负整数
- `keywords` 数组每项必须有 `word` 和 `score`
- `percentages` 总和应接近 100%
