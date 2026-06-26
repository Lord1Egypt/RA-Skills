---
name: shopping-intent-extractor
description: 从当前对话中提取用户的购物和支付意图，输出结构化 JSON 总结。提供两种方式：(1) 调用 `payment-intent summarize` 命令，或 (2) 由 AI 模型直接读取对话上下文分析总结。当用户要求总结购物意图、查看之前的购买计划、或提取支付相关信息时使用。
---

# Shopping Intent Extractor

从当前对话中提取用户的购物和支付意图，生成结构化 JSON 总结。

## 两种实现方式

| 方式 | 描述 | 适用场景 |
|------|------|----------|
| **方式 1** | 调用 `payment-intent summarize -s <sessionId>` 命令 | 有 sessionId 时，推荐方式 |
| **方式 2** | AI 模型直接分析对话上下文 | 无 sessionId 或快速响应 |

---

## 触发条件

当用户说以下类型的话时使用此 skill：

- "总结一下我之前的购物意图"
- "我之前想买什么来着？"
- "看看我之前的支付记录"
- "提取我的购物意图"
- "我从没说过要买什么吧"
- "我之前想支付什么？"
- "帮我看看上下文里有什么购物信息"

---

## 方式 1：调用 `payment-intent summarize` 命令

如果系统中有 `payment-intent` 命令行工具可用，优先使用此方式：

### 命令格式

```bash
payment-intent summarize -s <sessionId>
```

### 参数说明

| 参数 | 说明 | 是否必需 |
|------|------|----------|
| `-s <sessionId>` | 指定要分析的会话 ID | 必需 |

### 使用步骤

1. **获取 sessionId** —— 从当前会话元数据中获取
2. **执行命令** —— `payment-intent summarize -s <sessionId>`
3. **解析输出** —— 工具返回 JSON 格式的意图总结

**优点：** 准确、标准化、可复用

---

## 方式 2：AI 模型直接分析上下文

当 `payment-intent` 工具不可用或没有 sessionId 时，直接分析当前对话中的用户消息历史（OpenClaw 的上下文窗口内），**不需要读取外部 session 文件**。

**优点：** 快速、无需外部工具依赖

---

## AI 分析流程（方式 2）

### Step 1：扫描对话内容

读取当前对话中的用户消息历史。

### Step 2：识别关键信息

提取以下字段到 JSON：

| 字段 | 类型 | 说明 |
|------|------|------|
| `hasIntent` | boolean | 是否存在购物/支付意图 |
| `intentType` | `"shopping" \| "payment" \| "none"` | 意图类型 |
| `product` | string | 商品/服务名称（无则 `null`） |
| `amount` | string | 金额（无则 `null`） |
| `platform` | string | 平台（如"淘宝"、"支付宝"，无则 `null`） |
| `status` | `"pending" \| "paid" \| "cancelled" \| "unknown"` | 支付状态 |
| `summary` | string | 一句话总结（中文） |

### Step 3：识别关键词

**购物倾向：**
- "买"、"购买"、"下单"、"付款"、"支付"
- 商品名称、金额、平台名称
- "购物车"、"购物车里"、"淘宝"、"支付宝"

**支付状态：**
- "已支付"、"付款成功" → `paid`
- "待支付"、"还没付款"、"等会再付" → `pending`
- "不买了"、"取消了" → `cancelled`

---

## 输出格式

**纯 JSON，不使用 markdown 代码块包裹。**

### 示例 1：有明确购物意图

```json
{
  "hasIntent": true,
  "intentType": "shopping",
  "product": "手机高清壁纸",
  "amount": "¥0.01",
  "platform": "淘宝",
  "status": "pending",
  "summary": "用户计划在淘宝购买 1 分钱手机高清壁纸，待支付状态"
}
```

### 示例 2：无购物意图

```json
{
  "hasIntent": false,
  "intentType": "none",
  "product": null,
  "amount": null,
  "platform": null,
  "status": "unknown",
  "summary": "当前会话未检测到购物或支付意图"
}
```

### 示例 3：已支付

```json
{
  "hasIntent": true,
  "intentType": "payment",
  "product": "手机高清壁纸",
  "amount": "¥0.01",
  "platform": "支付宝",
  "status": "paid",
  "summary": "用户已通过支付宝完成 1 分钱壁纸支付"
}
```

---

## 规则

1. **优先使用 `payment-intent summarize -s <sessionId>` 命令** —— 有 sessionId 且工具可用时调用工具
2. **工具不可用时** —— AI 模型直接分析对话上下文
3. **只分析当前对话** —— 不读取外部 session 文件，不跨会话汇总
4. **仅识别购物/支付** —— 其他意图忽略
5. **输出纯 JSON** —— 不用 markdown 代码块包裹
6. **summary 字段用中文** —— 简洁直观
7. **金额统一格式** —— `¥X.XX` 或 `X 元`
8. **不确定时保守判断** —— `hasIntent: false`

---

## 决策流程

```
用户触发 skill
       ↓
有 sessionId 且 payment-intent 工具可用？
       ↓
   是 → payment-intent summarize -s <sessionId>
       ↓
   否 → AI 直接分析对话上下文
       ↓
输出 JSON 总结
```

---

## 下一步

分析完成后，直接输出 JSON 结果给用户。如果用户需要进一步操作（比如继续支付），根据结果提供建议。