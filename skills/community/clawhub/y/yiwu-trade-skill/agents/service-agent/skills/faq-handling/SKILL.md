---
name: faq-handling
description: 当用户询问常见问题、请求帮助文档或需要标准答案时触发
version: 1.0.0
tools_required:
  - faq_knowledge_base
  - semantic_search
  - answer_generator
---

# FAQ处理技能 (FAQ Handling)

## 触发条件

以下场景自动触发FAQ处理技能：
- 用户提问常见问题
- 用户请求帮助信息
- 意图识别为product_inquiry/offer_inquiry
- 新客户首次咨询

## 执行步骤

### Step 1: 问题解析
```
1. 提取问题核心:
   - 去除冗余信息
   - 识别问题类型(what/how/why/when)
   - 提取关键实体
   
2. 问题分类:
   - 产品FAQ
   - 订单FAQ
   - 支付FAQ
   - 物流FAQ
   - 服务FAQ
```

### Step 2: 知识库检索
```
检索策略:
1. 关键词精确匹配
2. 语义相似度匹配(embedding)
3. 问题模板匹配

检索参数:
- top_k: 5
- similarity_threshold: 0.75
- category_filter: 可选
```

### Step 3: 答案选择
```
选择策略:
1. 相似度 > 0.9 → 直接使用
2. 相似度 0.75-0.9 → 使用并标注
3. 相似度 < 0.75 → 组合多个答案 或 生成答案

答案组装:
- 优先使用原文
- 添加相关补充信息
- 多语言翻译(根据客户语言)
```

### Step 4: 答案优化
```
1. 个性化调整:
   - 替换占位符(商品名称、价格等)
   - 调整语气(正式/友好)
   
2. 格式优化:
   - 使用列表便于阅读
   - 重要信息加粗
   - 添加操作指引
   
3. 增强建议:
   - 添加相关问题推荐
   - 提供下一步操作
```

### Step 5: 满意度追踪
```
1. 记录FAQ命中
2. 追踪用户反馈
3. 标记未解决项
4. 优化知识库
```

## 输出格式

### FAQ命中响应
```json
{
  "success": true,
  "skill": "faq-handling",
  "data": {
    "query": {
      "original": "How long does shipping take?",
      "cleaned": "shipping time",
      "language": "en"
    },
    "match": {
      "faq_id": "FAQ_LOGISTICS_001",
      "question": "What is the estimated shipping time?",
      "similarity": 0.92,
      "category": "logistics"
    },
    "answer": {
      "content": "Shipping time varies by destination:\n\n**By Sea:**\n• Southeast Asia: 7-10 days\n• Middle East: 12-15 days\n• Europe: 25-30 days\n• Africa: 20-25 days\n• South America: 30-35 days\n\n**By Air:**\n• Most destinations: 5-7 days\n\n**Express (DHL/FedEx):**\n• 3-5 business days\n\nFor your order to UAE, sea freight typically takes 12-15 days.",
      "format": "markdown",
      "sources": ["logistics_policy_v2"],
      "confidence": 0.95
    },
    "metadata": {
      "helpful": true,
      "resolved": null,
      "feedback_requested": false
    },
    "suggestions": [
      {
        "question": "What are the shipping costs?",
        "faq_id": "FAQ_LOGISTICS_002"
      },
      {
        "question": "Can I track my shipment?",
        "faq_id": "FAQ_LOGISTICS_003"
      }
    ]
  },
  "confidence": 0.92
}
```

### 无匹配响应
```json
{
  "success": true,
  "skill": "faq-handling",
  "data": {
    "query": {
      "original": "Do you have certification for organic cotton?",
      "language": "en"
    },
    "match": {
      "found": false,
      "top_similarity": 0.45,
      "reason": "No matching FAQ found"
    },
    "answer": {
      "content": "Thank you for your inquiry! For certification details about specific products, I'll need to check with our supplier team.\n\nIn the meantime, could you please clarify:\n1. Which product are you interested in?\n2. What specific certification do you need (GOTS, Oeko-Tex, etc.)?\n\nI'll get back to you with the information shortly.",
      "generated": true,
      "confidence": 0.6
    },
    "action": {
      "type": "escalate",
      "reason": "Question outside knowledge base",
      "forward_to": "product_team"
    }
  },
  "confidence": 0.6
}
```

## 异常处理

### 异常1: 知识库检索超时
```
判断: 检索耗时 > 3秒
处理:
  1. 使用缓存结果
  2. 返回通用回复
  3. 记录待优化
```

### 异常2: 多答案冲突
```
判断: 多个答案相似度相近
处理:
  1. 选择最相关答案
  2. 标注"请参考具体产品"
  3. 提示可联系客服
```

### 异常3: 答案过期
```
判断: 答案更新日期 < today - 30天
处理:
  1. 标记"信息可能已更新"
  2. 提供最新查询入口
  3. 通知知识库管理员
```

## 示例

### 示例1: 标准FAQ查询
```
用户: "What is the minimum order quantity?"
系统:
  1. 识别为FAQ查询
  2. 检索知识库
  3. 返回标准答案
  4. 提供相关链接
```

### 示例2: 个性化FAQ
```
用户: "How long for 500 yoga mats to UAE?"
系统:
  1. 识别为物流FAQ
  2. 获取具体参数
  3. 生成个性化答案
  4. 包含具体数据
```

### 示例3: 多轮FAQ
```
用户: "Shipping time?"
系统: 返回通用物流时间

用户: "And cost?"
系统: 返回物流费用

用户: "Combined with 200 yoga balls?"
系统: 返回合并发货信息
```

### 示例4: FAQ+投诉
```
用户: "Product damaged when arrived!"
系统:
  1. 识别为投诉意图
  2. 切换到投诉处理
  3. 提供解决方案
```

## 知识库分类

### A. 产品类FAQ
- 产品规格
- 材质说明
- 颜色选择
- 包装方式
- 定制流程
- 认证信息

### B. 订单类FAQ
- 下单流程
- 订单修改
- 订单取消
- 合并发货

### C. 物流类FAQ
- 运输方式
- 运费计算
- 物流追踪
- 清关流程
- 收货注意

### D. 支付类FAQ
- 付款方式
- 付款账号
- 账期申请
- 发票开具

### E. 服务类FAQ
- 样品服务
- 验货服务
- 售后服务
- 合作洽谈
