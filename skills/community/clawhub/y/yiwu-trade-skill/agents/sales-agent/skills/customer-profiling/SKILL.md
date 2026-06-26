---
name: customer-profiling
description: 当需要分析客户特征、构建客户画像、打标签、追踪活跃度或进行客户分层时触发
version: 1.0.0
tools_required:
  - customer_database
  - tag_engine
  - activity_tracker
  - clv_calculator
---

# 客户画像技能 (Customer Profiling)

## 触发条件

以下场景自动触发客户画像技能：
- 新客户注册/导入
- 查看客户详情
- 客户分群筛选
- 活跃度分析
- 价值分层
- 个性化推荐依据
- 流失预警

## 执行步骤

### Step 1: 客户数据采集
```
1. 基础信息:
   - 姓名/公司名
   - 国家/地区
   - 联系方式(WhatsApp/Email)
   - 来源渠道
   
2. 行为数据:
   - 浏览记录
   - 询价记录
   - 订单历史
   - 沟通记录
   
3. 偏好数据:
   - 产品类目偏好
   - 价格敏感度
   - MOQ偏好
   - 质量要求
```

### Step 2: 标签体系构建
```
标签分类:

A. 来源标签:
   - facebook_lead
   - alibaba_inquiry
   - google_ad
   - referral
   - trade_show
   
B. 身份标签:
   - retailer (零售商)
   - wholesaler (批发商)
   - importer (进口商)
   - amazon_seller
   - ebay_seller
   - dropshipper
   
C. 产品标签:
   - category_home_decor
   - category_electronics
   - category_toys
   - category_fashion
   - ...
   
D. 行为标签:
   - price_sensitive (价格敏感)
   - quality_first (质量优先)
   - fast_decision (快速决策)
   - slow_responder (回复较慢)
   - high_moq_preferred
   
E. 状态标签:
   - hot_lead (热门线索)
   - active (活跃)
   - needs_followup (需跟进)
   - inactive (不活跃)
   - churned (流失)
```

### Step 3: 活跃度分析
```
活跃度评分计算:

浏览行为:
- 访问商品详情: +1分
- 发起询价: +5分
- 发起WhatsApp: +3分

转化行为:
- 收到报价: +2分
- 收到样品: +5分
- 下单: +10分
- 付款: +15分

活跃度等级:
- 超级活跃: 30天内得分 > 50
- 活跃: 30天内得分 20-50
- 一般: 30天内得分 5-20
- 不活跃: 30天内得分 < 5
- 流失: 90天无任何行为
```

### Step 4: 客户价值分层
```
CLV (Customer Lifetime Value) 计算:

基础指标:
- 历史订单总额 (GMV)
- 订单数量
- 平均订单价值
- 订单频率
- 客户时长

分层定义:
┌────────────────────────────────────────────────┐
│ 层级    │ 年均GMV   │ 特征                    │
├────────────────────────────────────────────────┤
│ VIP     │ >$50,000 │ 核心客户，全面服务      │
│ Premium │ $10-50K  │ 高价值，重点维护        │
│ Regular │ $1-10K    │ 成长客户，潜力挖掘      │
│ Small   │ <$1,000   │ 小客户，保持联系        │
│ Prospect│ 0        │ 潜在客户，转化为主      │
└────────────────────────────────────────────────┘
```

### Step 5: 画像更新与输出
```
1. 更新客户数据库
2. 生成/更新画像卡片
3. 触发个性化推荐
4. 记录关键事件
```

## 输出格式

### 客户画像响应
```json
{
  "success": true,
  "skill": "customer-profiling",
  "data": {
    "customer_id": "CUST202400123",
    "basic_info": {
      "name": "Ahmed Hassan",
      "company": "ABC Trading LLC",
      "country": "UAE",
      "city": "Dubai",
      "whatsapp": "+971501234567",
      "email": "ahmed@abctrading.ae",
      "language": "en",
      "source": "alibaba_inquiry",
      "created_at": "2024-01-15"
    },
    "identity_tags": ["importer", "wholesaler", "amazon_seller"],
    "product_preferences": {
      "categories": ["yoga_mat", "fitness_accessories"],
      "avg_moq": 300,
      "quality_expectation": "medium_high",
      "price_sensitivity": "medium"
    },
    "activity": {
      "last_active": "2024-03-15",
      "activity_score": 45,
      "level": "active",
      "recent_actions": [
        {"action": "viewed_product", "product": "LED Yoga Mat", "date": "2024-03-15"},
        {"action": "sent_inquiry", "product": "LED Yoga Mat", "date": "2024-03-14"},
        {"action": "received_quote", "quote": "QT20240314001", "date": "2024-03-14"}
      ]
    },
    "value_analysis": {
      "clv": 12500,
      "clv_level": "Premium",
      "total_orders": 8,
      "total_gmv": 12500,
      "avg_order_value": 1562.50,
      "first_order_date": "2024-01-20",
      "last_order_date": "2024-03-01"
    },
    "engagement_metrics": {
      "response_rate": 0.85,
      "avg_response_time_hours": 4,
      "conversion_rate": 0.25
    },
    "recommendations": [
      {
        "action": "send_followup",
        "reason": "Quoted 2 days ago, no response",
        "priority": "high"
      },
      {
        "action": "recommend_new_product",
        "product": "LED Yoga Ball",
        "reason": "Similar to recently viewed product"
      }
    ]
  },
  "confidence": 0.92
}
```

### 客户分群响应
```json
{
  "success": true,
  "skill": "customer-profiling",
  "data": {
    "segment_id": "seg_amazon_sellers_uae",
    "segment_name": "Amazon卖家-阿联酋",
    "criteria": {
      "identity_tags": ["amazon_seller"],
      "country": "UAE"
    },
    "stats": {
      "total_customers": 156,
      "total_gmv_90d": 450000,
      "avg_clv": 2880,
      "avg_activity_score": 35
    },
    "top_categories": [
      {"category": "yoga_mat", "percentage": 35},
      {"category": "fitness_accessories", "percentage": 28},
      {"category": "home_decor", "percentage": 22}
    ],
    "recommended_action": "批量发送健身类新品推广",
    "potential_customers": 45
  }
}
```

## 异常处理

### 异常1: 客户数据不足
```
判断: 客户记录<5条
处理:
  1. 标注"画像数据不足"
  2. 基于有限数据做初步推断
  3. 建议增加互动以完善画像
```

### 异常2: 客户流失预警
```
判断: 活跃度=inactive 且 CLV>0
处理:
  1. 发送唤醒消息
  2. 提供专属优惠
  3. 记录流失原因
```

### 异常3: 标签冲突
```
判断: 多个矛盾标签
处理:
  1. 以最新行为为准
  2. 标注需要人工确认
  3. 通知销售跟进
```

## 示例

### 示例1: 新客户自动打标
```
用户行为: 客户A在Alibaba发起瑜伽垫询价
系统:
  1. 创建客户档案
  2. 自动打标: alibaba_inquiry, yoga_mat_interest
  3. 识别身份: 初步判断为importer
  4. 分配销售跟进任务
```

### 示例2: 高价值客户识别
```
触发: 月末客户分层
系统:
  1. 计算所有客户CLV
  2. 按层级分组
  3. VIP客户: 发送专属问候
  4. 潜力客户: 触发培育流程
```

### 示例3: 流失预警
```
触发: 每日流失检测
系统:
  1. 扫描90天无活动客户
  2. 筛选高价值流失客户
  3. 发送挽留消息
  4. 记录挽留结果
```

### 示例4: 个性化推荐
```
用户: 打开与客户B的对话
系统:
  1. 加载客户画像
  2. 获取偏好类目
  3. 生成个性化产品推荐
  4. 显示"猜你喜欢"模块
```
