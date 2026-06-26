---
name: intent-classification
description: 当需要识别用户意图、判断用户需求类别或进行对话路由时触发
version: 1.0.0
tools_required:
  - nlu_engine
  - intent_classifier
  - confidence_scorer
---

# 意图识别技能 (Intent Classification)

## 触发条件

以下场景自动触发意图识别技能：
- 用户发送新消息时
- 对话开始时
- 意图不明确需要澄清时
- 对话路由决策前

## 执行步骤

### Step 1: 文本预处理
```
1. 语言检测
   - zh: 中文
   - en: 英文
   - ar: 阿拉伯文
   - es: 西班牙文
   
2. 文本清洗
   - 去除多余空格
   - 标准化标点
   - 处理表情符号
   
3. 分词与词性标注
   - 中文: jieba分词
   - 英文: spaCy分词
```

### Step 2: 意图分类
```
8大类意图体系:

┌─────────────────────────────────────────────────────────────┐
│ 意图大类              │ 子意图示例                          │
├─────────────────────────────────────────────────────────────┤
│ 1. 产品咨询          │ 商品规格/价格/MOQ/定制              │
│ 2. 订单查询          │ 订单状态/物流/发货时间              │
│ 3. 报价请求          │ 询价/要约/价格谈判                  │
│ 4. 投诉反馈          │ 质量问题/延迟/服务不满              │
│ 5. 退换货            │ 退货/换货/退款                      │
│ 6. 支付问题          │ 付款方式/账期/发票                  │
│ 7. 合作咨询          │ 代理/分销/OEM合作                  │
│ 8. 闲聊/其他         │ 问候/感谢/无法归类                  │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: 置信度评估
```
置信度等级:
- 高置信度: ≥0.85 → 直接执行对应回复
- 中置信度: 0.6-0.84 → 确认后执行
- 低置信度: <0.6 → 澄清问题

置信度影响因素:
- 关键词匹配度
- 句式相似度
- 上下文关联度
- 历史意图一致性
```

### Step 4: 澄清机制
```
触发条件:
- 置信度 < 0.6
- 多个意图得分相近(差距<0.1)
- 缺失关键信息

澄清策略:
- 选项式澄清: "您是想问...还是..."
- 追问式澄清: "您能详细说明一下吗"
- 确认式澄清: "您是说...对吗"
```

### Step 5: 意图切换检测
```
检测意图变化:
- 新意图与上一轮不同类目
- 新意图置信度 > 上一意图
- 排除追问/确认类消息

意图切换处理:
- 记录意图切换事件
- 更新当前意图状态
- 保持上下文连贯性
```

## 输出格式

### 意图识别响应
```json
{
  "success": true,
  "skill": "intent-classification",
  "data": {
    "input": {
      "original_text": "I want to know the price for 500 yoga mats",
      "language": "en",
      "cleaned_text": "I want to know the price for 500 yoga mats"
    },
    "intent": {
      "primary": {
        "category": "quote_request",
        "sub_category": "price_inquiry",
        "confidence": 0.92,
        "keywords_matched": ["price", "500", "yoga mats"]
      },
      "secondary": {
        "category": "product_inquiry",
        "confidence": 0.45
      }
    },
    "entities": {
      "product": "yoga mat",
      "quantity": 500,
      "attribute": "price"
    },
    "sentiment": {
      "label": "neutral",
      "score": 0.3
    },
    "action": {
      "type": "direct_reply",
      "confidence_threshold_met": true,
      "clarification_needed": false
    }
  },
  "confidence": 0.92
}
```

### 澄清请求响应
```json
{
  "success": true,
  "skill": "intent-classification",
  "data": {
    "intent": {
      "possible_intents": [
        {"category": "order_inquiry", "confidence": 0.55},
        {"category": "complaint", "confidence": 0.48}
      ],
      "confidence": 0.55,
      "low_confidence": true
    },
    "clarification": {
      "needed": true,
      "strategy": "choice",
      "message": "I'm not sure I understand. Are you asking about:"
    },
    "options": [
      "Your order status and delivery",
      "A problem with your recent order",
      "Something else"
    ]
  }
}
```

## 异常处理

### 异常1: 意图完全无法识别
```
判断: 所有意图 < 0.3
处理:
  1. 归类为"闲聊/其他"
  2. 提供通用引导回复
  3. 记录为未知问题
  4. 考虑升级人工
```

### 异常2: 多意图冲突
```
判断: top1与top2差距<0.05
处理:
  1. 优先主意图处理
  2. 次意图作为补充
  3. 询问是否需要处理其他问题
```

### 异常3: 语言检测失败
```
判断: language_confidence < 0.7
处理:
  1. 尝试多语言解析
  2. 默认使用英文处理
  3. 请求用户确认语言
```

## 示例

### 示例1: 产品咨询
```
用户: "这个瑜伽垫是什么材质的？"
识别结果:
  - intent: product_inquiry.specification
  - confidence: 0.94
  - entities: {product: "瑜伽垫", attribute: "材质"}
  - action: faq_handling
```

### 示例2: 投诉
```
用户: "Order not received after 20 days, very disappointed!"
识别结果:
  - intent: complaint.delivery_delay
  - confidence: 0.89
  - entities: {order_status: "not_received", delay_days: 20}
  - sentiment: {label: "negative", score: -0.8}
  - action: complaint_handling
```

### 示例3: 需要澄清
```
用户: "有点问题"
识别结果:
  - intent: unclear
  - confidence: 0.35
  - action: clarification
  - clarification_message: "请问您遇到了什么问题？"
```

### 示例4: 复合意图
```
用户: "Price for 500 yoga mats? And how long for delivery?"
识别结果:
  - primary_intent: quote_request.price_inquiry
  - secondary_intent: order_inquiry.delivery_time
  - action: both_reply
```
