# Vibe Coding 集成指南

**版本**: v3.0  
**创建日期**: 2026-04-06  
**状态**: ✅ 已完成

---

## 🎯 集成概览

### 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                可视化界面                                │
│           (vibe-dashboard.html)                          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ WebSocket 客户端                                  │   │
│  │ - 接收实时日志                                    │   │
│  │ - 接收 Agent 状态                                  │   │
│  │ - 接收进度更新                                    │   │
│  │ - 接收文件更新                                    │   │
│  │ - 接收质量评分                                    │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↕ WebSocket (ws://localhost:8765)
┌─────────────────────────────────────────────────────────┐
│                执行器                                    │
│        (vibe-executor-integrated.js)                     │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ WebSocket 服务器                                  │   │
│  │ - 推送日志                                        │   │
│  │ - 推送 Agent 状态                                  │   │
│  │ - 推送进度                                        │   │
│  │ - 推送文件                                        │   │
│  │ - 推送评分                                        │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Agent 调度器                                      │   │
│  │ - Analyst Agent                                   │   │
│  │ - Architect Agent                                 │   │
│  │ - Developer Agent                                 │   │
│  │ - Tester Agent                                    │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式 1: 使用开发服务器（推荐）

```bash
# 1. 启动服务器
cd /Users/lifan/.openclaw/workspace/skills/vibe-coding-cn
node server.js

# 2. 打开浏览器
http://localhost:3000/ui/vibe-dashboard.html

# 3. 点击"开始执行"或调用 API
curl -X POST http://localhost:3000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"requirement": "做一个个税计算器"}'
```

### 方式 2: 直接打开界面（演示模式）

```bash
# 直接打开界面（无 WebSocket 连接，使用演示模式）
open /Users/lifan/.openclaw/workspace/skills/vibe-coding-cn/ui/vibe-dashboard.html
```

### 方式 3: 在 OpenClaw 中执行

```javascript
// 在 OpenClaw 会话中
const { VibeExecutorIntegrated } = require('./executors/vibe-executor-integrated');

const executor = new VibeExecutorIntegrated('做一个个税计算器', {
  wsPort: 8765
});

// 启动 WebSocket 服务器和执行
executor.execute();

// 然后打开浏览器查看实时进度
```

---

## 📡 WebSocket 协议

### 连接

```javascript
const ws = new WebSocket('ws://localhost:8765');
```

### 消息格式

所有消息都是 JSON 格式：

```json
{
  "type": "message_type",
  "timestamp": "2026-04-06T10:30:00.000Z",
  ...data
}
```

### 消息类型

#### 1. connected（连接成功）

```json
{
  "type": "connected",
  "message": "已连接到 Vibe Coding 执行器",
  "timestamp": "2026-04-06T10:30:00.000Z"
}
```

#### 2. log（日志）

```json
{
  "type": "log",
  "logType": "phase|agent|output|complete|error",
  "message": "📊 Phase 1/5: 需求分析",
  "timestamp": "2026-04-06T10:30:00.000Z"
}
```

#### 3. agent_status（Agent 状态）

```json
{
  "type": "agent_status",
  "agent": "analyst|architect|developer|tester",
  "status": "waiting|running|completed|failed",
  "timestamp": "2026-04-06T10:30:00.000Z"
}
```

#### 4. phase_progress（阶段进度）

```json
{
  "type": "phase_progress",
  "phaseId": 1,
  "percent": 75,
  "status": "waiting|active|completed",
  "timestamp": "2026-04-06T10:30:00.000Z"
}
```

#### 5. file_added（文件添加）

```json
{
  "type": "file_added",
  "file": {
    "name": "docs/requirements.md",
    "size": "2.3 KB"
  },
  "timestamp": "2026-04-06T10:30:00.000Z"
}
```

#### 6. quality_score（质量评分）

```json
{
  "type": "quality_score",
  "role": "analyst|architect|developer|tester",
  "score": 85,
  "timestamp": "2026-04-06T10:30:00.000Z"
}
```

#### 7. execution_start（执行开始）

```json
{
  "type": "execution_start",
  "requirement": "做一个个税计算器",
  "projectName": "个税计算器",
  "timestamp": "2026-04-06T10:30:00.000Z"
}
```

#### 8. execution_complete（执行完成）

```json
{
  "type": "execution_complete",
  "stats": {
    "duration": 240,
    "avgQualityScore": 87,
    "filesGenerated": 5,
    "phasesCompleted": 5
  },
  "timestamp": "2026-04-06T10:34:00.000Z"
}
```

---

## 🔧 自定义配置

### 修改端口

```bash
# 修改 HTTP 端口
export PORT=8080

# 修改 WebSocket 端口
export WS_PORT=9000

# 启动服务器
node server.js
```

### 修改 WebSocket URL

在 `vibe-dashboard.html` 中修改：

```javascript
function connectWebSocket() {
  const wsUrl = 'ws://localhost:8765';  // 修改这里
  // ...
}
```

### 添加自定义日志类型

在 `vibe-dashboard.html` 中添加 CSS：

```css
.log-line.custom {
  border-left-color: #your-color;
  background: rgba(your-color, 0.05);
}
```

在 JavaScript 中处理：

```javascript
function handleWebSocketMessage(data) {
  switch (data.type) {
    case 'log':
      addLog(data.message, data.logType);
      break;
    case 'custom_type':  // 添加自定义类型
      // 处理自定义消息
      break;
  }
}
```

---

## 📊 API 接口

### POST /api/execute

启动执行任务

**请求**:
```json
{
  "requirement": "做一个个税计算器"
}
```

**响应**:
```json
{
  "status": "started",
  "requirement": "做一个个税计算器",
  "wsUrl": "ws://localhost:8765"
}
```

**错误**:
```json
{
  "error": "requirement is required"
}
```

---

## 🐛 故障排除

### 问题 1: WebSocket 连接失败

**症状**: 界面显示"未连接到执行器"

**原因**: 
- 服务器未启动
- 端口被占用
- 防火墙阻止

**解决**:
```bash
# 检查服务器是否运行
ps aux | grep node

# 检查端口是否被占用
lsof -i :8765

# 重启服务器
node server.js
```

### 问题 2: 界面不显示实时数据

**症状**: 界面正常，但数据不更新

**原因**: 
- WebSocket 连接断开
- 消息格式错误

**解决**:
1. 打开浏览器开发者工具
2. 查看 Console 日志
3. 检查 WebSocket 消息

### 问题 3: 执行器无法启动

**症状**: 调用 API 后无响应

**原因**: 
- sessions_spawn 不可用
- 模板文件缺失

**解决**:
```bash
# 检查模板文件
ls -la templates/

# 检查 OpenClaw 环境
node -e "console.log(typeof sessions_spawn)"
```

---

## 📈 性能优化

### 1. 减少消息频率

```javascript
// 优化前：每次更新都推送
this.wsServer.sendPhaseProgress(phaseId, percent, status);

// 优化后：每 10% 推送一次
if (percent % 10 === 0) {
  this.wsServer.sendPhaseProgress(phaseId, percent, status);
}
```

### 2. 消息批处理

```javascript
// 批量发送日志
const batchLogs = [];
batchLogs.push({ type: 'log', message: '...' });
batchLogs.push({ type: 'log', message: '...' });

this.wsServer.broadcast({
  type: 'batch',
  messages: batchLogs
});
```

### 3. 压缩消息

```javascript
// 使用 gzip 压缩
const zlib = require('zlib');

const compressed = zlib.gzipSync(JSON.stringify(data));
ws.send(compressed);
```

---

## 🎯 最佳实践

### 1. 开发模式

```bash
# 启动开发服务器（自动重载）
nodemon server.js

# 打开界面
open http://localhost:3000/ui/vibe-dashboard.html
```

### 2. 生产模式

```bash
# 设置生产环境变量
export NODE_ENV=production
export PORT=80

# 启动服务器
node server.js
```

### 3. 调试模式

```javascript
// 在 server.js 中添加调试日志
const DEBUG = true;

if (DEBUG) {
  console.log('[DEBUG] WebSocket 消息:', data);
}
```

---

## 📝 示例代码

### 前端集成示例

```html
<!DOCTYPE html>
<html>
<head>
  <title>Vibe Coding 集成示例</title>
</head>
<body>
  <div id="status">未连接</div>
  <div id="logs"></div>
  
  <script>
    const ws = new WebSocket('ws://localhost:8765');
    
    ws.onopen = () => {
      document.getElementById('status').textContent = '已连接';
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('收到消息:', data);
      
      if (data.type === 'log') {
        const logs = document.getElementById('logs');
        logs.innerHTML += `<div>${data.message}</div>`;
      }
    };
    
    // 启动执行
    fetch('http://localhost:3000/api/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        requirement: '做一个个税计算器'
      })
    });
  </script>
</body>
</html>
```

### 后端集成示例

```javascript
const { VibeExecutorIntegrated } = require('./vibe-executor-integrated');

async function runVibeCoding(requirement) {
  const executor = new VibeExecutorIntegrated(requirement, {
    wsPort: 8765,
    outputDir: './output'
  });
  
  try {
    const result = await executor.execute();
    console.log('执行完成:', result);
  } catch (error) {
    console.error('执行失败:', error);
  }
}

runVibeCoding('做一个个税计算器');
```

---

**集成状态**: ✅ 已完成  
**下一步**: 测试验证

**Vibe Coding v3.0** - 实时可视化执行！ 🎨
