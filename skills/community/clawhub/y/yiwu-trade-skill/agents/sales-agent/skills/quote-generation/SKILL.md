---
name: quote-generation
description: 当需要生成报价单、发送价格方案、创建PI或进行多语言报价时触发
version: 1.0.0
tools_required:
  - quote_template_engine
  - price_calculator
  - pdf_generator
  - multi_language_support
---

# 报价生成技能 (Quote Generation)

## 触发条件

以下场景自动触发报价生成技能：
- 客户询价，请求正式报价
- 生成Proforma Invoice (PI)
- 批量报价多个SKU
- 多语言报价单需求
- 报价单导出PDF/Excel
- 报价有效期管理

## 执行步骤

### Step 1: 信息收集与确认
```
1. 确认商品信息:
   - SKU列表
   - 数量
   - 规格/颜色要求
   
2. 确认价格条款:
   - 价格类型: FOB/CIF/EXW/DDP
   - 港口/目的地
   - 运输方式
   
3. 确认客户信息:
   - 公司名称
   - 联系人
   - 偏好语言
   - 付款方式
```

### Step 2: 价格计算
```
1. 获取基础单价
2. 应用阶梯价格:
   - if qty >= 1000: price × 0.85
   - if qty >= 500: price × 0.90
   - if qty >= 200: price × 0.95
   
3. 计算总价:
   line_total = unit_price × quantity
   
4. 计算附加费用:
   - 验货费: if required: +0.03/unit
   - 特殊包装: +cost
   - 样品费: +unit_price × 1.5
   
5. 计算总金额:
   grand_total = Σ(line_totals) + fees
```

### Step 3: 报价单生成
```
1. 选择报价单模板:
   - 标准模板 (Standard)
   - 简洁模板 (Compact)
   - 详细模板 (Detailed)
   
2. 填充内容:
   - Header: 公司信息、Logo
   - Quotation Details: 编号、日期、有效期
   - Client Info: 客户公司信息
   - Product Table: 商品明细
   - Pricing: 价格明细
   - Terms: 条款条件
   - Signature: 签名
      
3. 多语言适配:
   - 生成客户偏好语言版本
   - 保留英文对照(如需要)
```

### Step 4: 格式导出
```
支持导出格式:
- PDF: 正式文件，用于邮件发送
- Excel: 数据文件，便于客户修改
- HTML: 网页版本，用于即时通讯
```

### Step 5: 发送与跟踪
```
1. 生成下载链接/附件
2. 创建发送任务
3. 设置有效期提醒
4. 跟踪报价单状态:
   - created: 已创建
   - sent: 已发送
   - viewed: 客户已查看
   - replied: 客户已回复
   - expired: 已过期
   - converted: 已转订单
```

## 输出格式

### 报价单响应
```json
{
  "success": true,
  "skill": "quote-generation",
  "data": {
    "quote_info": {
      "quote_number": "QT20240315001",
      "created_at": "2024-03-15T10:00:00+08:00",
      "valid_until": "2024-03-22T10:00:00+08:00",
      "language": "en",
      "currency": "USD",
      "incoterms": "FOB",
      "loading_port": "Ningbo",
      "payment_terms": "T/T 30% deposit"
    },
    "supplier_info": {
      "company": "Yiwu Best Trading Co., Ltd.",
      "address": "Yiwu, Zhejiang, China",
      "contact": "John Wang",
      "email": "john@yiwubest.com",
      "whatsapp": "+86 139 1234 5678"
    },
    "client_info": {
      "company": "ABC Trading LLC",
      "contact": "Ahmed Hassan",
      "country": "UAE"
    },
    "products": [
      {
        "item_no": 1,
        "sku": "BB-001",
        "description": "Yoga Mat with LED Lights",
        "specifications": "8mm, Anti-slip, Rechargeable",
        "moq": 50,
        "quantity": 500,
        "unit": "pcs",
        "unit_price": 11.20,
        "line_total": 5600.00
      },
      {
        "item_no": 2,
        "sku": "BB-002",
        "description": "LED Controller",
        "specifications": "Remote control, USB charging",
        "moq": 50,
        "quantity": 500,
        "unit": "pcs",
        "unit_price": 2.50,
        "line_total": 1250.00
      }
    ],
    "pricing_summary": {
      "subtotal": 6850.00,
      "inspection_fee": 100.00,
      "subtotal_with_fees": 6950.00,
      "discount": 0,
      "grand_total": 6950.00
    },
    "shipping_estimate": {
      "20ft_container": "150 pcs",
      "estimated_freight": "USD 450",
      "notes": "Freight cost depends on final quantity and destination"
    },
    "terms_and_conditions": [
      "1. Price valid for 7 days",
      "2. 30% deposit required to start production",
      "3. Balance payable before shipment",
      "4. Lead time: 15-20 days after deposit",
      "5. Sample available at 1.5x unit price"
    ],
    "attachments": {
      "pdf_url": "https://cdn.example.com/quotes/QT20240315001.pdf",
      "excel_url": "https://cdn.example.com/quotes/QT20240315001.xlsx"
    }
  },
  "confidence": 0.98
}
```

### 多语言报价响应
```json
{
  "success": true,
  "skill": "quote-generation",
  "data": {
    "quote_number": "QT20240315001",
    "languages": {
      "en": {
        "url": "https://cdn.example.com/quotes/QT20240315001_en.pdf",
        "preview": "Proforma Invoice..."
      },
      "ar": {
        "url": "https://cdn.example.com/quotes/QT20240315001_ar.pdf",
        "preview": "فاتورةProforma..."
      },
      "es": {
        "url": "https://cdn.example.com/quotes/QT20240315001_es.pdf",
        "preview": "Factura Proforma..."
      }
    }
  }
}
```

## 异常处理

### 异常1: 商品信息缺失
```
判断: 缺少必填字段
处理:
  1. 列出缺失字段
  2. 使用引导式提问补全
  3. 常用默认值提示
```

### 异常2: 价格计算错误
```
判断: 计算结果与预期偏差>10%
处理:
  1. 重新校验基础数据
  2. 检查折扣/阶梯价格配置
  3. 人工复核确认
```

### 异常3: 导出格式不支持
```
判断: 客户要求格式系统不支持
处理:
  1. 说明支持的格式
  2. 建议最接近的替代格式
  3. 评估是否需要开发新格式支持
```

### 异常4: 报价单已过期
```
判断: 当前时间 > valid_until
处理:
  1. 提示报价已过期
  2. 询问是否重新生成
  3. 参考最新价格
```

## 示例

### 示例1: 标准报价
```
用户: "给我报500个LED瑜伽垫的价格"
系统:
  1. 获取商品信息和基础价格
  2. 计算阶梯价格(500件享9折)
  3. 生成完整报价单
  4. 输出PDF下载链接
```

### 示例2: 多SKU批量报价
```
用户: "我要报100个瑜伽垫、200个瑜伽砖、50个瑜伽球的价"
系统:
  1. 批量获取商品信息
  2. 分别计算各商品价格
  3. 汇总生成一张报价单
  4. 标注各商品MOQ
```

### 示例3: 阿拉伯语报价
```
用户: "Please send the quote in Arabic"
系统:
  1. 生成英文报价单
  2. 翻译所有内容为阿拉伯语
  3. 生成阿拉伯语PDF版本
  4. 右对齐排版
```

### 示例4: DDP报价(含税)
```
用户: "报DDP到迪拜的价格"
系统:
  1. 计算FOB价格
  2. 添加海运费
  3. 添加保险费
  4. 添加迪拜进口关税(5%)
  5. 生成DDP含税报价单
```
