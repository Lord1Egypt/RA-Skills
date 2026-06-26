# 意图类型定义 (Intent Types)

## 一级意图分类 (8大类)

### 1. 产品咨询 (product_inquiry)
**定义**: 用户询问产品相关信息

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| product_inquiry.specification | 产品规格 | 材质、尺寸、规格、参数 |
| product_inquiry.price | 价格咨询 | 价格、报价、多少钱 |
| product_inquiry.moq | 最小起订量 | MOQ、最少、多少起订 |
| product_inquiry.sample | 样品相关 | 样品、拿样、sample |
| product_inquiry.customization | 定制需求 | 定制、logo、OEM |
| product_inquiry.availability | 库存/现货 | 有货吗、现货、库存 |
| product_inquiry.comparison | 产品对比 | 区别、不同、哪个好 |

### 2. 订单查询 (order_inquiry)
**定义**: 用户查询订单相关信息

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| order_inquiry.status | 订单状态 | 订单状态、发货了吗、什么时候发 |
| order_inquiry.tracking | 物流追踪 | 物流、快递、追踪、到哪了 |
| order_inquiry.delivery_time | 交期咨询 | 多久到、几天、发货时间 |
| order_inquiry.address | 地址修改 | 修改地址、地址错了 |
| order_inquiry.order_details | 订单详情 | 订单号、订单内容 |

### 3. 报价请求 (quote_request)
**定义**: 用户请求报价或询价

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| quote_request.price_inquiry | 询价 | 报个价、多少钱、给个价 |
| quote_request.negotiation | 价格谈判 | 便宜点、能便宜吗 |
| quote_request.proforma_invoice | PI请求 | PI、形式发票 |
| quote_request.bulk_discount | 批量折扣 | 量大优惠、折扣 |
| quote_request.renew_quote | 更新报价 | 重新报价、更新价格 |

### 4. 投诉反馈 (complaint)
**定义**: 用户表达不满或投诉

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| complaint.quality | 质量问题 | 质量差、坏了、有问题 |
| complaint.delivery_delay | 延迟投诉 | 延迟、太慢了、耽误 |
| complaint.wrong_item | 错发漏发 | 发错了、少了、没收到 |
| complaint.service | 服务投诉 | 服务态度、没人理 |
| complaint.packaging | 包装问题 | 包装破损、压坏了 |
| complaint.other | 其他投诉 | 不满意、太差了 |

### 5. 退换货 (return_exchange)
**定义**: 用户申请退换货

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| return_exchange.refund | 退款申请 | 退款、退钱、退回 |
| return_exchange.return | 退货申请 | 退货、退回、寄回 |
| return_exchange.exchange | 换货申请 | 换货、换颜色、换尺寸 |
| return_exchange.process | 退换流程 | 怎么退、流程、步骤 |

### 6. 支付问题 (payment)
**定义**: 支付相关问题

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| payment.method | 付款方式 | 怎么付、付款方式、能用XX吗 |
| payment.invoice | 发票问题 | 发票、增票、普票 |
| payment.terms | 付款条款 | 账期、月结、TT |
| payment.confirmation | 付款确认 | 已付款、付了、转了 |
| payment.discount | 支付优惠 | 折扣、优惠、减免 |

### 7. 合作咨询 (cooperation)
**定义**: 商务合作相关

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| cooperation.agency | 代理合作 | 代理、经销商 |
| cooperation.distribution | 分销合作 | 分销、合作 |
| cooperation.oem | OEM合作 | OEM、代工 |
| cooperation.brand | 品牌合作 | 品牌、授权 |
| cooperation.visiting | 实地考察 | 验厂、看厂、来义乌 |

### 8. 其他 (other)
**定义**: 无法归类或闲聊

| 二级意图 | 描述 | 关键词示例 |
|----------|------|------------|
| other.greeting | 问候 | 你好、hi、hello |
| other.thanks | 感谢 | 谢谢、感谢 |
| other.bye | 告别 | 拜拜、再见 |
| other.unclear | 不明确 | 说不清、不知道 |
| other.feedback_request | 反馈请求 | 评价、满意度 |

---

## 意图识别关键词库

### 中文关键词
```
【产品咨询】
材质: 什么材料、材质、原料、成分
尺寸: 尺寸、大小、规格、多长
价格: 价格、多少钱、报价、价位
MOQ: 起订量、最少、多少起订、MOQ
样品: 样品、sample、拿样、试卖
颜色: 颜色、什么色、有哪些颜色
包装: 包装、盒装、散装

【订单查询】
订单: 订单、订单号、单号
发货: 发货了没、什么时候发、发货时间
物流: 物流、快递、单号、追踪
收货: 收到了、收货、签收

【投诉】
差: 差、太差了、不行
慢: 慢、延迟、耽误
错: 发错了、错了、不对
损: 坏了、破了、损了、压坏

【退换】
退: 退货、退款、退回
换: 换货、换色、换款
```

### 英文关键词
```
【Product Inquiry】
material: material, what is it made of, ingredient
size: size, dimension, measurements, how big
price: price, cost, how much, quote
moq: moq, minimum order, at least
sample: sample, for testing, trial order
color: color, what colors, available colors

【Order Inquiry】
order: order, order number, PO
shipping: shipped, when ship, shipping time
tracking: tracking, logistics, delivery status
received: received, delivered, signed

【Complaint】
bad: bad, terrible, poor quality
late: late, delayed, taking too long
wrong: wrong, incorrect, mistake
damaged: damaged, broken, crushed
```

---

## 意图分类决策树

```
用户输入
    │
    ▼
语言检测 ──→ 文本预处理
    │
    ▼
关键词匹配
    │
    ├─── 命中关键词 ──→ 计算置信度 ──→ 意图分类
    │
    └─── 未命中 ──→ 语义理解 ──→ 向量相似度 ──→ 意图分类
    │
    ▼
置信度评估
    │
    ├─── ≥0.85 ──→ 直接输出
    │
    ├─── 0.6-0.84 ──→ 确认后执行
    │
    └─── <0.6 ──→ 澄清机制
```

---

## 意图切换规则

### 触发条件
1. 新消息意图与当前意图属于不同大类
2. 新意图置信度 > 当前意图 + 0.1
3. 用户明确表示新话题

### 切换处理
```python
def detect_intent_switch(current_intent, new_intent, confidence):
    if current_intent.category != new_intent.category:
        if confidence > current_intent.confidence + 0.1:
            return True  # 切换意图
    return False
```

### 特殊规则
- "还有..." 开头 → 保持当前意图，追加
- "顺便问一下..." → 意图切换
- "对了..." → 意图切换
- 追问类 → 保持当前意图
