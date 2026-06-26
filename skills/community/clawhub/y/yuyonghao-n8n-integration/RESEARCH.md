# 🔗 n8n 工作流集成调研

**日期**: 2026-03-18  
**阶段**: Week 3 P0 任务  
**状态**: 📋 调研中

---

## 📖 n8n 概述

**n8n** 是一个可扩展的工作流自动化工具，支持 200+ 集成，基于 Node.js。

**核心特性**:
- 可视化工作流编辑器
- Webhook 支持
- 自定义函数节点
- 自托管/云部署
- 200+ 预置集成

---

## 🎯 集成方案

### 方案 1: Webhook 触发（推荐）⭐⭐⭐

**架构**:
```
n8n WorkFlow → Webhook → OpenClaw Agent → 执行 → 回调 n8n
```

**优点**:
- ✅ 简单直接
- ✅ n8n 原生支持
- ✅ 实时响应
- ✅ 易于调试

**缺点**:
- ⚠️ 需要公网可访问（或用 ngrok）

**实施难度**: ⭐⭐ (简单)

---

### 方案 2: n8n Function 节点

**架构**:
```
n8n WorkFlow → Function 节点 → require('openclaw-sdk') → Agent
```

**优点**:
- ✅ 深度集成
- ✅ 直接调用

**缺点**:
- ⚠️ 需要 SDK
- ⚠️ 依赖管理复杂

**实施难度**: ⭐⭐⭐ (中等)

---

### 方案 3: REST API 轮询

**架构**:
```
n8n 定期调用 OpenClaw API → 检查任务 → 执行
```

**优点**:
- ✅ 简单
- ✅ 无需 Webhook

**缺点**:
- ⚠️ 延迟高
- ⚠️ 资源浪费

**实施难度**: ⭐ (简单)

---

## 🚀 推荐实施方案

### Webhook 触发 + 回调

**工作流程**:
```
1. n8n 触发 Webhook
   ↓
2. OpenClaw 接收请求
   ↓
3. Agent 执行任务（ReAct/Multi-Agent）
   ↓
4. 回调 n8n Webhook（结果）
   ↓
5. n8n 继续后续工作流
```

**技术栈**:
- Express.js (Webhook 服务器)
- WebSocket (实时通信)
- OpenClaw Agent (执行)

---

## 📋 实施计划

### Phase 1: Webhook 服务器（2h）

**任务**:
- [ ] 创建 `skills/n8n-integration/src/webhook-server.js`
- [ ] 实现 `/webhook/trigger` 端点
- [ ] 请求验证（签名/Token）
- [ ] 响应格式化

**代码框架**:
```javascript
const express = require('express');
const app = express();

app.post('/webhook/trigger', async (req, res) => {
  const { workflow, action, params } = req.body;
  
  // 验证签名
  if (!verifySignature(req)) {
    return res.status(401).json({ error: 'Invalid' });
  }
  
  // 执行 Agent
  const result = await agent.execute(action, params);
  
  // 回调 n8n
  await callbackToN8n(workflow, result);
  
  res.json({ success: true, result });
});
```

---

### Phase 2: Agent 集成（2h）

**任务**:
- [ ] 包装 Agent 执行函数
- [ ] 支持 n8n 数据格式
- [ ] 错误处理
- [ ] 超时控制

**集成示例**:
```javascript
const { ObservabilitySystem } = require('../observability');
const { ReActOrchestrator } = require('../react-orchestrator');

const obs = new ObservabilitySystem();
const orchestrator = new ReActOrchestrator();

// 包装执行
const executeWithN8n = obs.wrap(
  async (workflow, action, params) => {
    const trace = obs.startTrace('n8n.workflow', { workflow });
    
    try {
      const result = await orchestrator.execute(action, params);
      trace.end({ success: true });
      return result;
    } catch (error) {
      obs.recordError(error, { workflow });
      trace.end({ error: error.message });
      throw error;
    }
  },
  'n8n.execute'
);
```

---

### Phase 3: n8n 工作流示例（1h）

**任务**:
- [ ] 创建示例工作流 JSON
- [ ] 测试端到端流程
- [ ] 编写使用文档

**示例工作流**:
```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "trigger-agent"
      }
    },
    {
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:3000/webhook/trigger",
        "body": "={{ $json }}"
      }
    }
  ]
}
```

---

## 📊 预期收益

| 指标 | 当前 | 实施后 | 提升 |
|------|------|--------|------|
| **工作流自动化** | 无 | 有 | +100% ✅ |
| **集成应用数** | 0 | 200+ | 显著 ✅ |
| **响应延迟** | - | ~100ms | 实时 ✅ |

---

## 📚 参考资料

- [n8n 官方文档](https://docs.n8n.io/)
- [n8n Webhook 节点](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [n8n HTTP Request 节点](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)

---

*调研时间：2026-03-18 14:15*  
*状态：📋 调研完成，准备实施*
