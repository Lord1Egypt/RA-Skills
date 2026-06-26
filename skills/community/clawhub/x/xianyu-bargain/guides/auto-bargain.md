# 闲鱼全自动砍价 - 完整实现指南

## 概述

本文档详细说明如何实现完全自动化的闲鱼砍价流程，包括：
- 自动发送砍价消息
- 定时监控卖家回复
- 智能分析并自动跟进
- 关键节点通知用户

---

## 启动全自动砍价

### Step 1: 收集参数

```yaml
required:
  - item_url: 商品链接
  - target_price: 目标价格
  - max_price: 底价（最高可接受）

optional:
  - check_interval: 监控间隔（默认 5 分钟）
  - max_rounds: 最大轮次（默认 5 轮）
  - strategy: 策略（moderate/gentle）
```

### Step 2: 获取商品信息

```javascript
// 1. 打开商品页面
browser({ action: "open", url: itemUrl })

// 2. 获取快照，提取：
//    - 商品名称
//    - 卖家ID
//    - 当前价格
//    - 商品成色
//    - 卖家信息（评价、在线时间等）
```

### Step 3: 创建状态文件

```bash
mkdir -p ~/.openclaw/workspace/xianyu-bargain-state
```

```json
// ~/.openclaw/workspace/xianyu-bargain-state/{itemId}.json
{
  "itemId": "1030963177488",
  "itemUrl": "https://www.goofish.com/item?id=1030963177488",
  "chatUrl": "https://www.goofish.com/im?itemId=1030963177488&peerUserId=2009038787",
  "itemName": "iPhone 17 256G 紫色",
  "originalPrice": 4588,
  "sellerId": "2009038787",
  "sellerName": "北京十年数码人",
  
  "targetPrice": 4500,
  "maxPrice": 4550,
  "currentOffer": 4500,
  
  "round": 1,
  "maxRounds": 5,
  "checkInterval": 300000,
  
  "status": "active",
  "lastCheck": "2026-03-13T13:22:00+08:00",
  "lastMessageTime": "2026-03-13T13:22:00+08:00",
  "lastSellerMessageId": null,
  
  "history": [
    {
      "role": "buyer",
      "message": "你好～这台 iPhone 17 很喜欢...",
      "time": "2026-03-13T13:22:00+08:00"
    }
  ],
  
  "cronJobId": "xxxxxxxx-xxxx-xxxx-xxxx"
}
```

### Step 4: 生成首轮消息并等待用户确认

⚠️ **不得直接发送消息。必须先展示给用户审阅。**

```
Agent: 拟发送以下砍价消息，确认后我帮你发出：

---
{生成的砍价话术}
---

确认发送？
```

用户确认后：

```javascript
// 1. 导航到聊天页面
browser({ action: "navigate", url: chatUrl })

// 2. 输入砍价消息
browser({ 
  action: "act", 
  kind: "type", 
  ref: "inputRef",
  text: confirmedMessage
})

// 3. 点击发送
browser({ action: "act", kind: "click", ref: "sendButtonRef" })
```

### Step 5: 询问用户是否开启自动监控

⚠️ **此步骤必须等待用户明确同意，不得自动执行。**

完成首轮消息后，告知用户：
- 自动监控会每隔几分钟检查卖家回复并自动发送砍价消息
- 这会创建一个持续运行的定时任务
- 存在平台风控风险

**只有用户明确说"开启"、"自动跟进"、"帮我盯着"等同意用语后**，才执行以下操作：

```javascript
cron({
  action: "add",
  job: {
    name: `闲鱼砍价-${itemId}`,
    schedule: { kind: "every", everyMs: 300000 },  // 5分钟
    sessionTarget: "isolated",
    payload: {
      kind: "agentTurn",
      message: `
执行闲鱼砍价监控任务：
1. 读取状态文件 ~/.openclaw/workspace/xianyu-bargain-state/${itemId}.json
2. 打开聊天页面检查新消息
3. 如果有新的卖家回复，使用 LLM 分析卖家意图（参考 guides/llm-analyzer.md）
4. 根据分析结果执行相应动作
5. 更新状态文件
6. 如需通知用户，通过 announce 推送
`,
      timeoutSeconds: 120
    },
    delivery: { mode: "announce" }
  }
})
```

---

## 监控任务执行流程

### 每次监控执行的步骤

```
1. 读取状态文件
   ↓
2. 检查状态是否为 active
   ├─ 否 → 退出
   └─ 是 ↓
3. 打开聊天页面
   ↓
4. 获取消息列表快照
   ↓
5. 比对最新消息与上次记录
   ├─ 无新消息 → 检查是否需要跟进 → 更新状态 → 退出
   └─ 有新消息 ↓
6. 分析卖家回复（LLM 语义分析，参考 guides/llm-analyzer.md）
   ↓
7. 根据分析结果执行动作
   ├─ SUCCESS → 通知用户成交 → 更新状态为 success
   ├─ ACCEPT → 发送接受消息 → 通知用户 → 更新状态
   ├─ COUNTER → 检查是否达到底价上限
   │     ├─ 是 → 通知用户决策
   │     └─ 否 → 发送加价消息 → 更新状态
   ├─ RESPOND → 生成回复 → 发送 → 更新状态
   ├─ GIVE_UP → 发送放弃消息 → 通知用户 → 更新状态
   └─ FOLLOW_UP → 发送跟进消息 → 更新状态
   ↓
8. 保存更新后的状态文件
```

### 检查新消息的方法

```javascript
// 获取聊天页面快照
const snapshot = await browser({ action: "snapshot", targetId })

// 解析消息列表
// 查找最新的卖家消息（非当前用户发送的）
// 比对消息ID或时间戳与状态文件中的 lastSellerMessageId

// 如果有新消息，提取消息内容
```

### 超时跟进逻辑

⚠️ **自动跟进仅在用户开启 cron 监控且 maxFollowUps > 0 时生效。**
**手动模式下，Agent 应通知用户卖家未回复，由用户决定是否发送跟进消息。**

**Follow-up logic (LLM-driven, no script required):**

When monitoring detects no new seller reply:
- Calculate time since last message
- If over 30 minutes and follow-up count < maxFollowUps:
  → LLM generates a natural follow-up message and sends it
  → Increment follow-up count in state file
- If follow-up count >= maxFollowUps:
  → Notify user: "卖家长时间未回复，是否继续等待？"

---

## 停止监控

### 用户主动停止

```javascript
// 1. 获取 cron job ID
const state = read_state_file(itemId)
const cronJobId = state.cronJobId

// 2. 删除 cron job
cron({ action: "remove", jobId: cronJobId })

// 3. 更新状态
state.status = "cancelled"
save_state_file(state)

// 4. 通知用户
announce("已停止对 {itemName} 的砍价监控")
```

### 自动停止条件

- 砍价成功（status = success）
- 主动放弃（status = abandoned）
- 达到最大轮次且卖家仍拒绝
- 商品已下架或已被他人购买

---

## 通知模板

### 成交通知
```
🎉 砍价成功！

商品：{itemName}
成交价：¥{finalPrice}（原价 ¥{originalPrice}，省了 ¥{saved}）

请尽快前往闲鱼下单：
{itemUrl}
```

### 卖家还价（需决策）
```
💰 卖家还价通知

商品：{itemName}
卖家出价：¥{sellerPrice}
你的底价：¥{maxPrice}

卖家价格超出你的底价 ¥{diff}，请决定：
- 回复 "接受" 同意卖家价格
- 回复 "继续砍" 尝试继续压价
- 回复 "放弃" 结束砍价
```

### 卖家拒绝
```
❌ 砍价未成功

商品：{itemName}
卖家表示不议价

是否要：
- 回复 "加到{maxPrice}" 出底价
- 回复 "放弃" 结束砍价
```

### 超时无回复
```
⏰ 卖家暂未回复

商品：{itemName}
已等待：{waitTime}

已自动发送跟进消息，继续监控中...
如需停止，回复 "停止砍价"
```

---

## 文件结构

```
~/.agents/skills/xianyu-bargain/
├── SKILL.md                          # 主技能文件
├── guides/
│   ├── llm-analyzer.md               # LLM 分析指南
│   ├── auto-bargain.md               # 本文档
│   ├── batch-processing.md           # 批量处理指南
│   └── xianyu-browser.md             # 浏览器操作指南
└── references/
    ├── market-prices.md              # 市场参考价
    ├── advanced-strategies.md        # 高级策略
    ├── message-templates.md          # 话术模板
    └── config.md                     # 配置说明

~/.openclaw/workspace/xianyu-bargain-state/
└── {itemId}.json                     # 各商品的砍价状态
```

---

## 安全考虑

1. **频率限制**：监控间隔不低于 5 分钟
2. **同时任务数**：同时监控不超过 3 个商品
3. **消息确认**：首轮消息必须经用户确认后发送
4. **Cron 限制**：自动监控必须经用户明确同意后开启
5. **异常处理**：登录失效、页面变化等需要人工介入
6. **数据保护**：状态文件仅存储在本地
7. **平台合规**：遵守闲鱼平台使用规则，不使用反检测手段
