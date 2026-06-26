---
name: smart-chatbot-builder
description: 智能聊天机器人构建器，快速创建客服/销售/内部助手聊天机器人，支持知识库、多轮对话、API 集成。
metadata:
  openclaw:
    requires:
      bins:
        - read
        - write
        - web_fetch
---

# AI 聊天机器人构建器 v1.0.0

快速构建 AI 聊天机器人，适用于客服、销售、内部助手等场景。

## 功能特性

### 1. 知识库集成
- 文档导入（PDF/Markdown/TXT）
- 网站内容抓取
- FAQ 配置
- RAG 检索增强

### 2. 对话管理
- 多轮对话流程
- 意图识别
- 上下文记忆
- 人工接管

### 3. 渠道集成
- Web 嵌入
- 微信/企业微信
- Slack/Discord
- API 接口

### 4. 数据分析
- 对话日志
- 用户行为分析
- 常见问题统计
- 满意度追踪

## 快速使用示例

```javascript
// 创建客服机器人
const bot = createChatbot({
  name: "客服助手",
  knowledgeBase: ["./docs/product.pdf", "./docs/faq.md"],
  channels: ["web", "wechat"],
  handoffThreshold: 0.6
})

// 配置对话流程
bot.addFlow("order_inquiry", {
  steps: [
    { ask: "请问您的订单号是？", save: "order_id" },
    { action: "query_order", use: "order_id" },
    { respond: "您的订单状态是：${order.status}" }
  ]
})

// 部署到 Web
bot.deploy({
  target: "web",
  container: "#chat-widget"
})
```

## 预置模板

### 模板 1：电商客服
- 订单查询
- 退换货政策
- 产品推荐
- 物流跟踪

### 模板 2：SaaS 产品助手
- 功能引导
- 故障排查
- 账户管理
- 技术支持

### 模板 3：内部知识库
- 员工问答
- 流程指引
- 文档检索
- IT 支持

## 定价参考

| 类型 | 复杂度 | 价格范围 |
|------|--------|----------|
| 基础客服 | 单渠道+FAQ | $5,000-$15,000 |
| 智能助手 | 多渠道+RAG | $15,000-$35,000 |
| 企业方案 | 全渠道+定制 | $35,000-$75,000+ |

## 定制开发

需要定制化 AI 聊天机器人、企业级集成方案？

📧 联系：careytian-ai@github

---

## 许可证

MIT-0
