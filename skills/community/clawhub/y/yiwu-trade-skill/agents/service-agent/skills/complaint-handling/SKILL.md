---
name: complaint-handling
description: 当用户表达不满、提出投诉、要求赔偿或情绪激动时触发
version: 1.0.0
tools_required:
  - sentiment_analyzer
  - complaint_classifier
  - escalation_engine
  - ticket_manager
---

# 投诉处理技能 (Complaint Handling)

## 触发条件

以下场景自动触发投诉处理技能：
- 意图识别为complaint类
- 情绪分析为negative
- 用户明确表示不满
- 用户要求赔偿/退款
- 用户多次重复同一问题

## 执行步骤

### Step 1: 情绪感知与分析
```
情绪检测指标:
1. 负面词汇: "差/烂/bad/terrible"
2. 感叹号数量: 过多表示强烈不满
3. 问号数量: 反复追问表示不满
4. 表情符号: 😠😡💢 等
5. 语速/长度: 长篇抱怨通常情绪强烈

情绪等级:
- 😠 微怒: 正常处理
- 😡 不满: 优先处理
- 💢 愤怒: 立即安抚
- 😱 恐慌: 紧急升级
```

### Step 2: 投诉分级
```
投诉分级标准:

┌─────────────────────────────────────────────────────────────┐
│ 级别   │ 定义                    │ 响应时间  │ 处理方式   │
├─────────────────────────────────────────────────────────────┤
│ P3     │ 一般问题，服务/态度     │ 4小时     │ 客服处理   │
│ P2     │ 延迟，轻微损失          │ 2小时     │ 主管处理   │
│ P1     │ 严重损失，批量问题      │ 1小时     │ 经理处理   │
│ P0     │ 危机事件，法律风险      │ 即时      │ 高层介入   │
└─────────────────────────────────────────────────────────────┘

P3 普通投诉:
- 服务态度问题
- 一般延迟(3-5天)
- 轻微包装问题
- 信息回复慢

P2 升级投诉:
- 较大延迟(>10天)
- 部分产品损坏
- 错发漏发
- 多次未解决

P1 严重投诉:
- 大批量质量问题
- 严重延迟(>20天)
- 重要客户投诉
- 舆论风险

P0 紧急投诉:
- 人身安全问题
- 法律诉讼威胁
- 大规模召回
- 媒体曝光
```

### Step 3: 问题核实
```
核实清单:
1. 订单信息确认
   - 订单号
   - 购买日期
   - 订单金额
   
2. 问题描述确认
   - 问题类型
   - 发生时间
   - 影响范围
   - 相关证据

3. 责任归属判断
   - 供应商责任
   - 物流责任
   - 客户责任
   - 不可抗力

4. 损失评估
   - 直接损失
   - 间接损失
   - 预期利益损失
```

### Step 4: 解决方案制定
```
解决方案选项:

1. 退款类:
   - 全额退款
   - 部分退款
   - 折价退款
   
2. 补货类:
   - 补发全新
   - 补发同等价值其他产品
   - 折扣换货
   
3. 赔偿类:
   - 退款+赔偿
   - 额外补偿
   - 优惠券补偿
   
4. 服务补偿:
   - 免费升级服务
   - 免运费
   - 延长账期

决策原则:
- 优先保护客户利益
- 在授权范围内决策
- 考虑长期客户关系
- 避免开了先例
```

### Step 5: 升级规则
```
必须升级的情况:
1. 涉及金额 > $500
2. 客户威胁投诉媒体/监管
3. 客户要求高层道歉
4. 涉及法律条款争议
5. 同一问题超过3次未解决
6. 情绪失控无法沟通
7. VIP客户投诉

升级路径:
P3 → 客服组长
P2 → 客服主管
P1 → 客服经理
P0 → 总经理/法务
```

### Step 6: 闭环跟踪
```
工单系统:
1. 创建工单
   - 工单号
   - 问题类型
   - 优先级
   - 责任人
   
2. 处理记录
   - 每步操作记录
   - 沟通记录
   - 证据上传
   
3. 解决确认
   - 解决方案
   - 客户确认
   - 满意度评分
   
4. 事后分析
   - 问题根因
   - 改进措施
   - 预防计划
```

## 输出格式

### 投诉处理响应
```json
{
  "success": true,
  "skill": "complaint-handling",
  "data": {
    "complaint_id": "CMPT20240315001",
    "received_at": "2024-03-15T10:30:00+08:00",
    "customer": {
      "id": "CUST202400123",
      "name": "Ahmed Hassan",
      "company": "ABC Trading LLC",
      "tier": "Premium",
      "clv": 12500
    },
    "sentiment_analysis": {
      "emotion": "angry",
      "emotion_level": 3,
      "indicators": ["multiple_question_marks", "uppercase_words", "repeated_complaint"],
      "urgency": "high"
    },
    "complaint_classification": {
      "category": "quality_defect",
      "sub_category": "damaged_packaging",
      "severity": "P2",
      "responsibility": "logistics"
    },
    "issue_summary": {
      "order_id": "ORD20240228001",
      "product": "LED Yoga Mat",
      "quantity": 100,
      "problem": "30% of products have damaged packaging, 5 units are unusable",
      "evidence": ["photo_1.jpg", "photo_2.jpg"]
    },
    "resolution": {
      "status": "proposed",
      "options": [
        {
          "type": "full_replacement",
          "description": "Ship 30 replacement units immediately",
          "cost": 336,
          "timeline": "3-5 days",
          "accepted": null
        },
        {
          "type": "partial_refund",
          "description": "Refund $168 for damaged units",
          "cost": 168,
          "timeline": "3 days",
          "accepted": null
        }
      ],
      "recommended": "full_replacement",
      "decided_option": null
    },
    "escalation": {
      "required": false,
      "reason": null,
      "current_handler": "agent_wang"
    },
    "follow_up": {
      "next_action": "await_customer_response",
      "deadline": "2024-03-16T10:30:00+08:00",
      "reminder_set": true
    }
  },
  "confidence": 0.88
}
```

### 升级响应
```json
{
  "success": true,
  "skill": "complaint-handling",
  "data": {
    "escalation": {
      "required": true,
      "level": "P1",
      "reason": "VIP customer, loss > $500",
      "escalated_to": "manager_zhang",
      "escalated_at": "2024-03-15T10:35:00+08:00",
      "wait_time": "2 minutes",
      "original_handler": "agent_wang",
      "transfer_reason": "Case requires management approval for $500 compensation"
    },
    "customer_communication": {
      "message": "I understand your frustration, Mr. Hassan. I'm escalating this to my manager Mr. Zhang who will personally handle your case and get back to you within 1 hour. Your case number is CMPT20240315001.",
      "sentiment": "empathetic",
      "language": "en"
    }
  }
}
```

## 异常处理

### 异常1: 客户情绪失控
```
判断: 情绪等级 = 愤怒/恐慌
处理:
  1. 立即停止解释
  2. 表达理解和歉意
  3. 承诺尽快解决
  4. 主动升级处理
  5. 记录为高优先级
```

### 异常2: 责任归属争议
```
判断: 无法明确责任方
处理:
  1. 不推卸责任
  2. 先解决问题，后追责
  3. 内部协调处理
  4. 如需时间，向客户说明
```

### 异常3: 超出授权范围
```
判断: 赔偿金额 > 客服权限
处理:
  1. 说明需要申请
  2. 承诺回复时间
  3. 快速内部审批
  4. 优先满足客户合理诉求
```

## 补偿标准参考

| 问题类型 | 轻微 | 中等 | 严重 |
|----------|------|------|------|
| 质量问题 | 10%退款 | 30%退款/补发 | 全额退款+补偿 |
| 延迟发货 | 5%优惠券 | 10%退款 | 全额退款+补偿 |
| 错发漏发 | 补发+优惠券 | 退款+补发 | 全额退款 |
| 包装破损 | 5%退款 | 退款已损品 | 全额退款+补偿 |

---

## 示例

### 示例1: 情绪安抚优先
```
用户: "I'M SO TIRED OF WAITING!!! WHERE IS MY ORDER???"
系统:
  1. 识别为愤怒情绪
  2. 识别为P2投诉
  3. 首先安抚情绪
  4. 然后提供解决方案
  回复: "Mr. XX, I completely understand your frustration. I'm so sorry for the delay. Let me check your order right now and get back to you in 5 minutes."
```

### 示例2: 多选项方案
```
用户: "Product quality is not as described!"
系统:
  1. 核实订单和描述差异
  2. 提供三个方案:
     - 退货退款
     - 补发正确产品
     - 部分退款保留产品
  3. 让客户选择
```

### 示例3: 升级处理
```
用户: "This is unacceptable! I want to speak to your CEO!"
系统:
  1. 识别为P1投诉
  2. 立即升级
  3. 记录升级原因
  4. 告知客户已升级
```
