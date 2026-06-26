---
name: whatsapp-outreach
description: 当需要通过WhatsApp触达客户、发送营销消息、群发推广或进行一对一沟通时触发
version: 1.0.0
tools_required:
  - hugobsp_api
  - message_template_db
  - wa_status_tracker
---

# WhatsApp触达技能 (WhatsApp Outreach)

## 触发条件

以下场景自动触发WhatsApp触达技能：
- 批量发送营销推广消息
- 新客户首次触达
- 询盘回复跟进
- 产品上新通知
- 订单状态通知
- 节日/生日祝福
- 催单/付款提醒

## 执行步骤

### Step 1: 消息策略选择
```
1. 判断触达目的:
   - 首次开发 → 使用开发信模板
   - 询盘回复 → 使用回复模板
   - 营销推广 → 使用推广模板
   - 重要通知 → 使用通知模板

2. 选择消息类型:
   - 模板消息: 已审核的固定格式
   - 自由消息: 自由编辑内容
   - 图文消息: 包含图片/视频
   - 文档消息: PDF/Excel附件
```

### Step 2: 消息生成
```
1. 加载对应模板
2. 填充变量:
   - {customer_name}: 客户名称
   - {product_name}: 产品名称
   - {price}: 价格
   - {link}: 产品链接
   
3. 多语言适配:
   - 根据客户语言偏好选择模板版本
   - 自动翻译并校对

4. 个性化增强:
   - 引用上次对话内容
   - 提及客户关注的产品类目
```

### Step 3: BSP API调用
```
1. 认证授权
   - 获取Access Token
   - 验证账号状态

2. 构建请求
   - Phone Number: 客户手机号(含国家区号)
   - Message Template: 模板ID
   - Parameters: 变量值数组
   - Media URLs: 图片/视频链接

3. 发送请求
   - POST /v1/messages
   - 记录message_id用于追踪
```

### Step 4: 状态追踪
```
发送后自动追踪以下状态:
- queued: 消息排队中
- sent: 已发送到运营商
- delivered: 已送达客户手机
- read: 客户已读
- failed: 发送失败
- blocked: 被客户屏蔽

定期刷新状态并更新记录
```

## 输出格式

### 发送响应
```json
{
  "success": true,
  "skill": "whatsapp-outreach",
  "data": {
    "message_id": "wamsg_202403151234567890",
    "phone_number": "+60123456789",
    "message_type": "template",
    "template_id": "tmpl_new_product",
    "status": "sent",
    "sent_at": "2024-03-15T10:30:00+08:00",
    "estimated_delivery": "2024-03-15T10:30:30+08:00",
    "cost": {
      "currency": "CNY",
      "amount": 0.15
    }
  },
  "metadata": {
    "execution_time_ms": 850,
    "retry_count": 0
  },
  "confidence": 0.95
}
```

### 批量发送响应
```json
{
  "success": true,
  "skill": "whatsapp-outreach",
  "data": {
    "batch_id": "batch_20240315001",
    "total_recipients": 100,
    "sent": 98,
    "failed": 2,
    "results": [
      {
        "phone": "+60123456789",
        "status": "sent",
        "message_id": "wamsg_xxx"
      },
      {
        "phone": "+60123456790",
        "status": "failed",
        "error": "invalid_phone_number"
      }
    ],
    "summary": {
      "delivery_rate": 0.98,
      "estimated_reach": 95,
      "cost_total": 15.00
    }
  },
  "confidence": 0.92
}
```

### 状态追踪响应
```json
{
  "success": true,
  "skill": "whatsapp-outreach",
  "data": {
    "message_id": "wamsg_202403151234567890",
    "current_status": "delivered",
    "status_history": [
      {"status": "queued", "timestamp": "2024-03-15T10:30:00Z"},
      {"status": "sent", "timestamp": "2024-03-15T10:30:05Z"},
      {"status": "delivered", "timestamp": "2024-03-15T10:30:30Z"}
    ],
    "read_at": null,
    "replied_at": null
  }
}
```

## 异常处理

### 异常1: API认证失败
```
判断: HTTP 401 / token_invalid
处理:
  1. 重新获取Access Token
  2. 检查BSP账号状态
  3. 如持续失败，切换备用通道
  4. 记录错误并告警
```

### 异常2: 手机号无效
```
判断: HTTP 400 / invalid_phone
处理:
  1. 验证手机号格式(国家码+号码)
  2. 尝试格式修正
  3. 标记该客户联系方式异常
  4. 从当前批次移除，继续处理其他
```

### 异常3: 模板审核未通过
```
判断: template_status != approved
处理:
  1. 切换到已审核的相似模板
  2. 如无替代，自动改用自由消息
  3. 记录模板问题供后续优化
```

### 异常4: 发送频率超限
```
判断: HTTP 429 / rate_limit_exceeded
处理:
  1. 自动等待并重试(指数退避)
  2. 调整发送速率
  3. 分散到多个时间段
  4. 通知用户发送延迟
```

### 异常5: 客户已屏蔽
```
判断: delivery_status = blocked
处理:
  1. 停止向该号码发送消息
  2. 更新客户标签: blocked=true
  3. 不计入活跃客户池
  4. 记录屏蔽原因
```

## 消息模板示例

### 开发信模板
```
Hi {customer_name},

I found your business on {source} and noticed you're in {industry}.

As a Yiwu-based supplier specializing in {category}, I'd love to share our latest products:

🔥 {product_1} - {price_1}
🔥 {product_2} - {price_2}

Free samples available! Would you like to see?

Best regards,
{sales_name}
```

### 报价跟进模板
```
Hi {customer_name},

Following up on the quote I sent on {date}.

Here's a quick reminder:
📦 {product_name}
💰 Price: {price}
📅 Valid until: {validity_date}

Limited stock available! Let me know if you have any questions.

Best,
{sales_name}
```

### 新品推广模板
```
🆕 NEW ARRIVALS!

Hi {customer_name},

Just launched - {product_name}!

✨ Features: {features}
💰 MOQ: {moq} | Price: {price}
📦 Sample: Available

WhatsApp me for details! 👇
{sales_whatsapp}

-{sales_name}
```
