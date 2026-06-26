# n8n-integration

**n8n 工作流自动化集成** - 将 OpenClaw Agent 接入 n8n 工作流生态系统

## 描述

通过 Webhook 实现 n8n 与 OpenClaw Agent 的双向集成：

- **Webhook 触发** - n8n 工作流触发 Agent 执行
- **回调机制** - Agent 执行结果回调 n8n
- **Agent 集成** - 支持 ReAct/Multi-Agent 等执行器
- **可观测性** - 集成 Observability 系统
- **认证安全** - Token 验证保护

## 功能

- ✅ **Webhook 服务器** - Express.js 驱动，多端点支持
- ✅ **请求验证** - Token 认证，防止未授权访问
- ✅ **Agent 执行** - 包装 ReAct/Multi-Agent 执行器
- ✅ **超时控制** - 可配置执行超时
- ✅ **重试机制** - 指数退避重试
- ✅ **回调 n8n** - 执行结果自动回调
- ✅ **可观测性** - 集成日志/指标/追踪
- ⏳ **n8n 工作流示例** - 预置工作流模板

## 安装

```bash
# 从 ClawHub 安装（待发布）
clawhub install n8n-integration

# 或手动克隆
git clone https://github.com/YOUR_GITHUB/skills/n8n-integration
cd skills/n8n-integration
npm install
```

## 快速开始

### 1. 启动 Webhook 服务器

```bash
cd skills/n8n-integration
npm start

# 或
node src/webhook-server.js

# 环境变量
# N8N_PORT=3002
# N8N_AUTH_TOKEN=your-secret-token
# N8N_VERBOSE=true
```

### 2. 配置 n8n 工作流

**导入示例工作流**:
- 文件：`examples/workflow-example.json`
- Webhook URL: `http://localhost:3002/webhook/trigger`
- Token: `n8n-webhook-token`

### 3. 触发 Agent

```bash
curl -X POST http://localhost:3002/webhook/trigger \
  -H "Content-Type: application/json" \
  -H "X-N8N-Token: n8n-webhook-token" \
  -d '{
    "workflow": "ai-search",
    "action": "search",
    "params": {"query": "AI trends 2026"},
    "callbackUrl": "http://localhost:5678/webhook/result"
  }'
```

## 配置选项

### N8nIntegration 配置

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `port` | number | `3002` | Webhook 服务器端口 |
| `verbose` | boolean | `false` | 详细日志 |

### N8nWebhookServer 配置

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `port` | number | `3002` | 服务器端口 |
| `host` | string | `'localhost'` | 监听地址 |
| `authToken` | string | 环境变量 | 认证 Token |
| `callbackTimeout` | number | `30000` | 回调超时（毫秒） |
| `verbose` | boolean | `false` | 详细日志 |
| `executor` | object | `null` | Agent 执行器 |

### N8nAgentIntegration 配置

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `executor` | object | `null` | Agent 执行器 |
| `observability` | object | `null` | 可观测性系统 |
| `timeout` | number | `30000` | 执行超时（毫秒） |
| `retries` | number | `0` | 重试次数 |
| `verbose` | boolean | `false` | 详细日志 |

## API 参考

### N8nIntegration

#### `constructor(options)`
创建 n8n 集成实例。

#### `start()`
启动 Webhook 服务器。

#### `stop()`
停止服务。

#### `setExecutor(executor, type)`
设置 Agent 执行器：
- `executor` - ReAct/Multi-Agent 实例
- `type` - `'react'` 或 `'multi-agent'`

#### `setObservability(observability)`
设置可观测性系统。

#### `getWebhookServer()`
获取 Webhook 服务器实例。

#### `getAgentIntegration()`
获取 Agent 集成实例。

### N8nWebhookServer

#### `start()`
启动服务器。

#### `stop()`
停止服务器。

#### `setExecutor(executor)`
设置执行器。

#### `getResults(limit)`
获取执行结果历史。

### N8nAgentIntegration

#### `execute(workflow, action, params)`
执行 Agent：
- `workflow` - n8n 工作流名称
- `action` - 执行动作
- `params` - 执行参数
- 返回：`{ success, workflow, action, result, duration }`

#### `setExecutor(executor)`
设置执行器。

#### `setObservability(observability)`
设置可观测性。

## 使用场景

### 场景 1: AI 搜索自动化

```
n8n 定时触发 → OpenClaw Agent 搜索 → 结果处理 → 发送邮件
```

**n8n 工作流**:
1. Schedule Trigger (每天 9:00)
2. HTTP Request → OpenClaw Webhook
3. Process Result
4. Send Email

### 场景 2: CRM 数据增强

```
CRM 新客户 → n8n Webhook → Agent 调研公司 → 更新 CRM
```

**工作流**:
1. CRM Webhook (新客户)
2. HTTP Request → OpenClaw (调研公司)
3. Update CRM Record

### 场景 3: 社交媒体监控

```
RSS Feed → n8n → Agent 分析 → Slack 通知
```

**工作流**:
1. RSS Feed Read
2. Filter Keywords
3. HTTP Request → OpenClaw (分析重要性)
4. Slack Notification

## 与现有系统集成

### 集成 ReAct Orchestrator

```javascript
const { N8nIntegration } = require('./n8n-integration');
const { ReActOrchestrator } = require('../react-orchestrator');

const n8n = new N8nIntegration();

// 设置 ReAct 执行器
const orchestrator = new ReActOrchestrator();
n8n.setExecutor(orchestrator, 'react');

// 启动
await n8n.start();
```

### 集成 Observability

```javascript
const { ObservabilitySystem } = require('../observability');

const obs = new ObservabilitySystem();
n8n.setObservability(obs);
```

## 安全考虑

### 认证

**推荐方式**:
1. 使用环境变量存储 Token
2. 定期轮换 Token
3. 使用 HTTPS（生产环境）

```bash
export N8N_AUTH_TOKEN="your-secret-token"
```

### 请求验证

所有 Webhook 请求都验证 `X-N8N-Token` header：

```javascript
const token = req.headers['x-n8n-token'];
if (token !== process.env.N8N_AUTH_TOKEN) {
  return res.status(401).json({ error: 'Unauthorized' });
}
```

## 故障排查

### 问题 1: 401 Unauthorized

**原因**: Token 不匹配  
**解决**: 检查 `X-N8N-Token` header 和服务器配置

### 问题 2: 500 Internal Server Error

**原因**: Agent 执行失败  
**解决**: 检查日志，确认执行器配置正确

### 问题 3: 回调失败

**原因**: n8n 回调 URL 不可访问  
**解决**: 确保 n8n 公网可访问或使用 ngrok

## 依赖

- Node.js >= 18.0.0
- express ^4.18.2
- crypto ^1.0.1

## 版本历史

### v0.1.0 (2026-03-18)
- ✅ 初始版本
- ✅ Webhook 服务器
- ✅ Agent 集成
- ✅ 回调机制
- ✅ 可观测性集成

## 许可证

MIT

## 作者

小蒲萄 (Clawd) 🦞

## 贡献

欢迎提交 Issue 和 PR！

## 参考资料

- [n8n 官方文档](https://docs.n8n.io/)
- `RESEARCH.md` - 调研报告
- `examples/workflow-example.json` - 示例工作流
