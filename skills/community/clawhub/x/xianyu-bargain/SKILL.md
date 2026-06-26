---
name: xianyu-bargain
license: MIT
description: >
  闲鱼全自动砍价助手：帮助用户在闲鱼平台与卖家自动砍价。
  支持：生成讲价话术、分析商品价值、多轮砍价策略、自动监控回复、智能跟进、批量砍价。
  触发场景：闲鱼砍价、讲价、还价、二手交易谈价、"帮我砍价"、"自动砍价"、"批量砍价"、
  "这个价格合理吗"、"怎么跟卖家讲价"、发送闲鱼商品链接询问价格。
  全自动模式：设置目标价和底价后，自动监控卖家回复并智能跟进砍价。
  批量模式：同时对多个商品进行自动砍价，统一监控管理。
  ⚠️安全：绝不自动下单，只通知用户。
---

# 闲鱼全自动砍价助手

> 💡 **This is an instruction-only skill.** All analysis, decision-making, and reply generation are performed by the LLM directly using the platform's built-in `browser()` and `cron()` tools. No external scripts, Python files, or additional dependencies are required.

## 核心功能

| 功能 | 说明 |
|------|------|
| 💰 价格分析 | 评估商品定价是否合理 |
| 💬 多样话术 | 4种风格随机变化，不重复 |
| 🔄 多轮策略 | 试探 → 加价 → 最终出价 |
| 🤖 自动监控 | 定时检查卖家回复 |
| 🧠 智能分析 | 理解卖家意图，自动决策 |
| 📢 实时通知 | 重要进展推送通知 |
| 📦 批量处理 | 同时砍多个商品 |
| ⚙️ 可配置 | 最大回复数、话术风格等 |
| 🔒 安全保障 | 绝不自动下单 |

---

## 快速开始

### 手动模式
```
帮我砍价：
商品链接：https://www.goofish.com/item?id=XXX
目标价：4500
```

> ⚠️ 所有模式下，Agent 必须先将拟发送的砍价消息展示给用户确认，用户同意后再发送。不得跳过确认直接发送。

### 全自动模式
```
自动砍价：
商品链接：https://www.goofish.com/item?id=XXX
目标价：4500
底价：4550
```

### 批量模式
```
批量砍价：
https://www.goofish.com/item?id=111 目标4500 底价4800
https://www.goofish.com/item?id=222 目标6200 底价6500
https://www.goofish.com/item?id=333 目标3000 底价3200
```

### 批量管理命令
```
砍价进度      → 查看所有任务状态
停止砍价 17Pro → 停止单个任务
停止全部砍价   → 停止所有任务
```

---

## ⚙️ 配置选项

### 方式1: 自然语言（推荐）

```
砍价配置                     → 查看当前配置

设置砍价：最多回复3次         → maxReplies=3
设置砍价：最多回复5次         
设置砍价：监控间隔5分钟       → checkIntervalMin=5
设置砍价：话术风格=幽默       → messageStyle=humorous
设置砍价：话术风格=专业
设置砍价：话术风格=随性
设置砍价：话术风格=友好

重置砍价配置                  → 恢复默认
```

### 方式2: 启动时指定

```
自动砍价：
链接：https://...?id=xxx
目标价：4500
底价：4800
最多回复：3
话术：幽默
```

### 方式3: 编辑配置文件

位置: `~/.openclaw/workspace/xianyu-bargain-state/config.json`

```json
{
  "cronEnabled": false,
  "maxReplies": 5,
  "checkIntervalMin": 5,
  "maxFollowUps": 2,
  "messageStyle": "friendly"
}
```

### 配置项说明

| 配置项 | 默认 | 可选值 | 说明 |
|--------|------|--------|------|
| `maxReplies` | 5 | 1-10 | 每个商品最多自动回复次数，超过后通知用户 |
| `checkIntervalMin` | 5 | 5-30 | 监控检查间隔（分钟） |
| `maxFollowUps` | 2 | 0-5 | 卖家无回复时最多跟进次数 |
| `messageStyle` | friendly | friendly/professional/casual/humorous | 话术风格 |

### 话术风格对比

| 风格 | 中文 | 适用场景 | 示例 |
|------|------|----------|------|
| `friendly` | 友好 | 通用，大多数卖家 | 你好～很喜欢！🙏 |
| `professional` | 专业 | 高价商品、商家 | 您好，请问可否... |
| `casual` | 随性 | 年轻卖家、低价 | 老板，出不？ |
| `humorous` | 幽默 | 活跃气氛 | 钱包蠢蠢欲动！ |

---

## 全自动砍价流程

### 配置参数

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| 商品链接 | ✅ | 闲鱼商品 URL | `https://www.goofish.com/item?id=XXX` |
| 目标价 | ✅ | 理想成交价 | 4500 |
| 底价 | ✅ | 最高可接受价格 | 4550 |
| 监控间隔 | 可选 | 检查频率（分钟） | 5 (默认) |
| 最大轮次 | 可选 | 最多砍价几轮 | 5 (默认) |
| 自动发送 | 可选 | 是否无需确认 | true/false |

### 状态机

```
[配置] → [首轮砍价] → [等待回复] → [分析回复] → [决策]
              ↑                           ↓
              └────── [发送跟进] ←────────┘
                           ↓
                  [成交/放弃/通知用户]
```

### ⚠️ 自动监控（Cron Job）— 默认关闭，需用户明确开启

**自动监控默认不启动。** Agent 在完成首轮砍价消息后，必须：
1. 明确告知用户：自动监控会创建定时任务（cron job），每隔几分钟自动检查卖家回复并代你发送消息
2. 说明风险：持续自动消息可能触发平台风控、违反闲鱼规则
3. **等待用户明确同意**（如"开启自动监控"、"帮我自动跟进"）后才创建 cron job
4. 如果用户没有明确要求自动监控，则仅执行单次砍价，后续由用户手动触发

**禁止行为：**
- ❌ 不得在用户未明确同意的情况下创建 cron job
- ❌ 不得将 cron 监控作为默认流程的一部分自动启动
- ❌ 不得用模糊措辞暗示已开启监控（如"已为您设置"）

用户明确同意后，使用 cron 工具创建监控任务：

```javascript
cron({
  action: "add",
  job: {
    name: "闲鱼砍价监控-{商品ID}",
    schedule: { kind: "every", everyMs: 300000 },  // 5分钟（默认）
    sessionTarget: "isolated",
    payload: {
      kind: "agentTurn",
      message: "检查闲鱼砍价进度：商品ID={id}, 目标价={target}, 底价={max}",
      timeoutSeconds: 120
    },
    delivery: { mode: "announce" }
  }
})
```

---

## 🧠 LLM 智能分析（无硬编码）

**不使用关键词匹配**，完全依赖 LLM 语义理解来分析卖家回复并生成自然回复。

详细指南: `guides/llm-analyzer.md`

### 分析流程

每次检测到新的卖家消息时，将以下上下文交给 LLM 分析：

```
【商品】{itemName} ¥{originalPrice}
【目标价】¥{targetPrice}  【底价】¥{maxPrice}
【当前出价】¥{currentOffer}  【轮次】{round}/{maxRounds}
【话术风格】{messageStyle}
【对话历史】
{history}
【卖家最新回复】{latestMessage}

请分析卖家意图并决定下一步：
1. intent: agree/counter/reject/question/other
2. sellerPrice: 卖家提到的价格（如有）
3. action: accept/raise/respond/wait/notify/giveup
4. nextMessage: 要发送的回复
5. notifyUser: 是否通知用户
6. reason: 决策理由

规则：
- 卖家同意或还价≤底价 → accept，通知用户去下单（⚠️绝不自动下单）
- 卖家还价>底价 → notify，让用户决策
- 卖家拒绝且有轮次 → raise，适当加价
- 卖家询问 → respond，自然回答+重申出价
- 回复要像真人，简短2-3句，符合选定的话术风格
- 绝不暴露底价
- 如果卖家直接询问是否为 AI/自动化，应如实回答
```

### 决策矩阵

| 卖家意图 | 条件 | 行动 |
|----------|------|------|
| 同意 | 价格 ≤ 底价 | ✅ 通知用户下单 |
| 还价 | ≤ 底价 | ✅ 接受，通知用户 |
| 还价 | > 底价 | ⚠️ 通知用户决策 |
| 拒绝 | 有剩余轮次 | 🔄 LLM 生成加价回复 |
| 拒绝 | 轮次用完 | 🛑 礼貌结束 |
| 询问 | - | 💬 LLM 回答+重申 |
| 自动回复 | - | ⏳ 继续等待 |

### 回复生成原则

- **自然多变** — LLM 每次生成不同表达，不使用模板
- **风格一致** — 遵循 config 中的 messageStyle
- **简短** — 闲鱼聊天风格，2-3句话
- **有策略** — 表达真实购买诚意
- **不暴露底价** — 不主动透露最高可接受价格
- **诚实** — 如被卖家直接询问是否为AI，应如实告知

### 超时跟进

```
你好，还在吗？
之前问的{商品}，{当前出价}能出吗？
我挺喜欢的，可以的话今天就拍～
```

---

## 浏览器自动化

### 检查新消息

```javascript
// 1. 打开聊天页面
browser({ action: "navigate", url: chatUrl })

// 2. 获取页面快照
browser({ action: "snapshot" })

// 3. 解析消息列表，找到最新卖家消息
// 4. 与上次记录对比，判断是否有新回复
```

### 发送消息

```javascript
// 1. 定位输入框
browser({ action: "act", kind: "type", ref: "inputRef", text: message })

// 2. 点击发送
browser({ action: "act", kind: "click", ref: "sendButtonRef" })
```

### 状态持久化

在 workspace 中保存砍价状态：

```json
// ~/.openclaw/workspace/xianyu-bargain-state/{商品ID}.json
{
  "itemId": "1030963177488",
  "itemName": "iPhone 17 256G 紫色",
  "sellerId": "2009038787",
  "sellerName": "北京十年数码人",
  "targetPrice": 4500,
  "maxPrice": 4550,
  "currentOffer": 4500,
  "round": 1,
  "status": "waiting",  // waiting/success/failed/abandoned
  "lastCheck": "2026-03-13T13:22:00+08:00",
  "lastSellerMessage": null,
  "history": [
    {"role": "buyer", "message": "...", "time": "..."},
    {"role": "seller", "message": "...", "time": "..."}
  ]
}
```

---

## 通知机制

### 需要通知用户的情况

| 事件 | 通知内容 |
|------|----------|
| 🎉 成交 | "砍价成功！卖家同意{价格}，请尽快下单" |
| 💰 还价超底价 | "卖家还价{价格}，超出底价{底价}，是否接受？" |
| ❌ 明确拒绝 | "卖家表示不议价，是否放弃或调整策略？" |
| ⏰ 长时间无回复 | "已等待{时间}无回复，是否继续等待？" |
| ⚠️ 异常 | "砍价遇到问题：{错误信息}" |

### 通知方式

通过 cron job 的 delivery.mode = "announce" 自动推送到当前聊天。

---

## 使用示例

### 启动全自动砍价

用户说：
```
帮我全自动砍价这个 iPhone：
链接：https://www.goofish.com/item?id=1030963177488
目标价：4500
底价：4550
```

Agent 执行：
1. 获取商品信息，分析市场价
2. 打开聊天，发送首轮砍价消息
3. 保存状态到 workspace
4. 询问用户是否开启自动监控（cron job）
5. **仅当用户明确同意后**，创建 cron 监控任务

### 监控任务执行（用户开启后，每5分钟）

1. 读取状态文件
2. 打开聊天页面
3. 检查是否有新消息
4. 如果有 → 分析回复 → 执行策略 → 更新状态
5. 如果需要通知用户 → 通过 announce 推送

### 停止监控

用户说：`停止砍价监控` 或 `取消自动砍价`

Agent 执行：
1. 删除对应的 cron job
2. 更新状态为 abandoned
3. 确认已停止

---

## 注意事项

### ✅ 推荐

- 设置合理的目标价和底价
- 目标价和底价差距建议 50-100 元
- 监控间隔建议 3-5 分钟，避免过于频繁

### ⚠️ 风险提示

- 闲鱼可能检测自动化行为
- 建议同时只监控 1-2 个商品
- 重要交易建议人工确认最终成交

### ❌ 避免

- 不要设置过低的不合理目标价
- 不要同时监控太多商品
- 不要对同一卖家反复砍价

---

## 相关文件

- [market-prices.md](references/market-prices.md) — 热门品类市场参考价
- [advanced-strategies.md](references/advanced-strategies.md) — 高级砍价策略
- [auto-bargain.md](guides/auto-bargain.md) — 自动砍价流程详解
