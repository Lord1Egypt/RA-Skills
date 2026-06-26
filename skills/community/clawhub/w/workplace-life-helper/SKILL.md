---
name: workplace-life-helper
description: 职场+生活全能助手：租房避坑、闲鱼卖货、职场赋能、内容合规检测20项服务（合同审查/押金计算/简历优化/周报生成/合规检测等），0.10元/次
version: 1.3.0
author: Workplace Life Helper Team
tags:
  - 职场
  - 生活
  - 租房
  - 闲鱼
  - 简历
  - 周报
  - 合规
  - 支付宝AI收
metadata:
  openclaw:
    skill_type: api-wrapper
    api_endpoint: https://w4h8ghmxcv.coze.site
    pricing:
      model: per_call
      price: 0.10
      currency: CNY
    payment:
      provider: alipay_a2m
      service_id: API_B954E805E6F0419A
---

# 职场+生活全能助手

## 任务目标
- 本 Skill 用于：解决打工人租房、卖货、职场、合规检测中的高频痛点
- 能力包含：租房避坑（4项）、闲鱼助手（4项）、职场赋能（6项）、内容合规（6项），共20项服务
- 触发条件：用户提到合同审查、押金计算、闲鱼卖货、简历优化、周报生成、合规检测等关键词

## 核心定价
- **统一价格**：0.10元/次
- **支付方式**：支付宝AI收（A2M自动付费）
- **服务地址**：https://w4h8ghmxcv.coze.site

## 服务目录

### 🏠 租房避坑（4项）

| 服务 | 端点 | 说明 |
|------|------|------|
| 合同审查 | `/api/v1/skill/zufang/contract` | 分析租房合同条款，识别风险点 |
| 押金计算 | `/api/v1/skill/zufang/deposit` | 计算押金退还方案 |
| 文书生成 | `/api/v1/skill/zufang/document` | 生成退租协议等法律文书 |
| 维权建议 | `/api/v1/skill/zufang/complaint` | 提供租房纠纷解决方案 |

### 🛒 闲鱼助手（4项）

| 服务 | 端点 | 说明 |
|------|------|------|
| 商品文案 | `/api/v1/skill/xianyu/describe` | 生成吸引买家的商品描述 |
| 定价建议 | `/api/v1/skill/xianyu/price` | 智能定价参考 |
| 谈判话术 | `/api/v1/skill/xianyu/negotiate` | 应对砍价、交易谈判 |
| 防骗识别 | `/api/v1/skill/xianyu/antiscam` | 识别交易风险和骗子套路 |

### 💼 职场赋能（6项）

| 服务 | 端点 | 说明 |
|------|------|------|
| 清醒搭子 | `/api/v1/skill/bahe/qingxing` | 职场困惑倾诉和建议 |
| 简历优化 | `/api/v1/skill/bahe/jianli` | 优化简历提高面试率 |
| 社媒文案 | `/api/v1/skill/bahe/shemei` | 小红书/抖音等平台文案 |
| 电商文案 | `/api/v1/skill/bahe/dianshang` | 产品卖点提炼和推广 |
| 周报神器 | `/api/v1/skill/bahe/zhoubao` | 自动生成周报/月报 |
| AI工具集 | `/api/v1/skill/bahe/aitools` | 推荐适合任务的AI工具 |

### ✅ 内容合规检测（6项）

| 服务 | 端点 | 说明 |
|------|------|------|
| 公众号合规 | `/api/v1/skill/comply/wechat` | 检测公众号文章违规词/广告法 |
| 抖音合规 | `/api/v1/skill/comply/douyin` | 检测抖音文案/直播带货合规 |
| 小红书合规 | `/api/v1/skill/comply/xiaohongshu` | 检测小红书种草/测评内容 |
| 电商合规 | `/api/v1/skill/comply/ecommerce` | 检测电商详情页价格/宣传 |
| 广告合规 | `/api/v1/skill/comply/ad` | 检测各类广告文案合规 |
| 通用合规 | `/api/v1/skill/comply/general` | 通用文本合规检测 |

## 操作步骤

### 步骤1：识别用户需求
根据用户输入判断属于哪类服务：
- 租房相关 → zufang 端点组
- 闲鱼卖货相关 → xianyu 端点组
- 职场相关 → bahe 端点组
- 内容合规相关 → comply 端点组

### 步骤2：调用 api_client.py
使用 scripts/api_client.py 发起请求：

```bash
python scripts/api_client.py <endpoint> <json_body>
```

**示例调用**：
```bash
# 简历优化
python scripts/api_client.py "bahe/jianli" '{"resume_text": "张三，3年经验...", "target_job": "产品经理"}'

# 合同审查
python scripts/api_client.py "zufang/contract" '{"contract_text": "甲方：... 乙方：..."}'

# 闲鱼定价
python scripts/api_client.py "xianyu/price" '{"item_name": "iPhone14", "condition": "9成新", "original_price": "5999"}'

# 公众号合规检测
python scripts/api_client.py "comply/wechat" '{"content": "文章内容...", "article_title": "标题", "industry": "食品"}'

# 抖音文案合规检测
python scripts/api_client.py "comply/douyin" '{"content": "视频文案...", "video_type": "带货"}'
```

### 步骤3：处理响应
- **402 Payment Needed**：告知用户价格（0.10元），引导支付宝AI收支付
- **200 OK**：返回服务结果，直接呈现给用户

### 步骤4：结果呈现
将API返回的JSON结果格式化输出，确保用户易读易懂。

## API统一响应格式

所有端点返回统一格式：
```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    "content": "生成的具体内容..." 或 "report": "合规检测报告..."
  },
  "credits_used": 10,
  "disclaimer": "本内容由AI生成，仅供参考。"
}
```

**注意**：未付费请求会收到HTTP 402响应：
```json
{
  "code": "Payment-Needed",
  "message": "需要支付",
  "out_trade_no": "ORDER_xxx",
  "amount": "10",
  "currency": "CNY",
  "goods_name": "简历优化"
}
```
此时需要通过支付宝AI收完成支付，携带Payment-Proof头重新请求即可获得200响应。

## API调用示例

### 简历优化示例
**输入**：
```json
{
  "resume_text": "张三\n3年产品经验\n负责过APP迭代\n熟练Axure",
  "target_job": "高级产品经理"
}
```

**输出（200）**：
```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    "content": "【优化后的简历内容】..."
  },
  "credits_used": 10,
  "disclaimer": "本内容由AI生成，仅供参考。"
}
```

### 公众号合规检测示例
**输入**：
```json
{
  "content": "这款产品是最好的，100%有效！",
  "article_title": "产品推荐",
  "industry": "化妆品"
}
```

**输出（200）**：
```json
{
  "success": true,
  "message": "公众号文章合规检测完成",
  "data": {
    "report": "{\"risk_level\": \"高\", \"total_issues\": 2, \"issues\": [...]}"
  },
  "credits_used": 10,
  "disclaimer": "⚠️ 本内容由AI生成，仅供法律信息参考..."
}
```

## 注意事项
- 所有端点统一收费：0.10元/次（共20个端点）
- 未付费用户会收到402响应，需通过支付宝AI收完成支付
- 合同审查仅供参考，不构成法律意见
- 合规检测结果仅供参考，不构成法律建议
- 闲鱼定价建议仅供参考，实际价格自行决定
- 支付宝AI收会自动处理付费流程，用户授权后即可使用


