# Vibe Coding 执行流程说明

**版本**: v3.0  
**创建日期**: 2026-04-06  
**状态**: ✅ 逻辑已理顺

---

## 🎯 完整执行流程

### 用户操作流程

```
1. 打开界面
   http://localhost:3000/ui/vibe-dashboard.html
   
2. 输入需求
   "做一个个税计算器"
   
3. 点击"🚀 执行 Vibe Coding"
   
4. 等待执行完成（3-5 分钟）
   
5. 查看生成的文件
   output/个税计算器/
```

---

## 📊 技术流程

### 方式 1: 实时模式（WebSocket 连接）

```
用户操作                    界面                      服务器                   执行器
   │                        │                          │                        │
   │ 1. 输入需求             │                          │                        │
   │    点击执行            │                          │                        │
   │───────────────────────>│                          │                        │
   │                        │                          │                        │
   │                        │ 2. POST /api/execute     │                        │
   │                        │    {requirement}         │                        │
   │                        │─────────────────────────>│                        │
   │                        │                          │                        │
   │                        │                          │ 3. 启动 VibeExecutor   │
   │                        │                          │<───────────────────────│
   │                        │                          │                        │
   │                        │ 4. 返回 {status:started} │                        │
   │                        │<─────────────────────────│                        │
   │                        │                          │                        │
   │ 5. 显示"执行已启动"     │                          │                        │
   │<───────────────────────│                          │                        │
   │                        │                          │                        │
   │                        │                          │ 6. 执行 Phase 1        │
   │                        │                          │<───────────────────────│
   │                        │                          │                        │
   │                        │ 7. WebSocket 推送日志     │                        │
   │                        │<─────────────────────────│                        │
   │ 8. 显示日志             │                          │                        │
   │<───────────────────────│                          │                        │
   │                        │                          │                        │
   │                        │                          │ 9. 执行 Phase 2-5      │
   │                        │                          │<───────────────────────│
   │                        │                          │                        │
   │                        │ 10. WebSocket 推送进度    │                        │
   │                        │<─────────────────────────│                        │
   │ 11. 更新进度条          │                          │                        │
   │<───────────────────────│                          │                        │
   │                        │                          │                        │
   │                        │ 12. WebSocket 推送文件    │                        │
   │                        │<─────────────────────────│                        │
   │ 13. 显示文件树          │                          │                        │
   │<───────────────────────│                          │                        │
   │                        │                          │                        │
   │                        │ 14. WebSocket 推送评分    │                        │
   │                        │<─────────────────────────│                        │
   │ 15. 显示质量评分        │                          │                        │
   │<───────────────────────│                          │                        │
   │                        │                          │                        │
   │                        │ 16. WebSocket 推送完成    │                        │
   │                        │<─────────────────────────│                        │
   │ 17. 显示"执行完成"      │                          │                        │
   │<───────────────────────│                          │                        │
   │                        │                          │                        │
```

---

### 方式 2: 演示模式（无 WebSocket 连接）

```
用户操作                    界面
   │                        │
   │ 1. 输入需求             │
   │    点击执行            │
   │───────────────────────>│
   │                        │
   │                        │ 2. 检查 WebSocket 连接
   │                        │    → 未连接
   │                        │
   │                        │ 3. 启动演示模式
   │                        │    （模拟执行）
   │                        │
   │ 4. 显示"演示模式"       │
   │<───────────────────────│
   │                        │
   │                        │ 5. 模拟 Phase 1-5
   │                        │    （进度条、日志、文件）
   │                        │
   │ 6. 实时更新界面         │
   │<───────────────────────│
   │                        │
   │ 7. 显示"演示完成"       │
   │<───────────────────────│
   │                        │
```

---

## 🔧 关键代码

### 1. 用户点击执行

```javascript
async function executeRequirement() {
  const requirement = document.getElementById('requirementInput').value.trim();
  
  if (!requirement) {
    alert('请输入需求！');
    return;
  }
  
  // 检查 WebSocket 连接
  if (!wsConnected) {
    // 无连接 → 演示模式
    resetDashboard();
    addLog(`📝 用户需求：${requirement}`, 'info');
    addLog(`⚠️  未连接到执行器，使用演示模式`, 'warning');
    startExecutionDemo();
    return;
  }
  
  // 有连接 → 实时模式
  resetDashboard();
  addLog(`📝 用户需求：${requirement}`, 'info');
  
  // 调用 API
  const response = await fetch('http://localhost:3000/api/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ requirement })
  });
  
  const result = await response.json();
  
  if (result.status === 'started') {
    addLog(`🚀 执行已启动`, 'complete');
    isRunning = true;
    // 等待 WebSocket 推送真实数据
  }
}
```

### 2. API 接口

```javascript
// server.js
server.on('request', async (req, res) => {
  if (req.url === '/api/execute' && req.method === 'POST') {
    const { requirement } = JSON.parse(body);
    
    // 启动执行器
    const executor = new VibeExecutorIntegrated(requirement, {
      wsPort: WS_PORT
    });
    
    // 异步执行
    executor.execute().catch(console.error);
    
    res.end(JSON.stringify({
      status: 'started',
      requirement,
      wsUrl: `ws://localhost:${WS_PORT}`
    }));
  }
});
```

### 3. WebSocket 推送

```javascript
// vibe-executor-integrated.js
async function callAgent(role, prompt) {
  // 更新 Agent 状态
  this.wsServer.sendAgentStatus(role, 'running');
  
  // 执行...
  
  // 质量检查
  const quality = qualityCheck(role, output);
  
  // 发送质量评分
  this.wsServer.sendQualityScore(role, quality.score);
  
  // 更新 Agent 状态
  this.wsServer.sendAgentStatus(role, 'completed');
}
```

### 4. 界面接收数据

```javascript
// vibe-dashboard.html
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleWebSocketMessage(data);
};

function handleWebSocketMessage(data) {
  switch (data.type) {
    case 'log':
      addLog(data.message, data.logType);
      break;
    case 'agent_status':
      setAgentStatus(data.agent, data.status);
      break;
    case 'phase_progress':
      setPhaseProgress(data.phaseId, data.percent, data.status);
      break;
    case 'file_added':
      addFile(data.file.name, data.file.size);
      break;
    case 'quality_score':
      addQualityScore(data.role, data.score);
      break;
  }
}
```

---

## ✅ 逻辑验证

### 问题 1: 用户输入需求后，点击执行会发生什么？

**答案**:
1. 界面获取输入的需求
2. 检查 WebSocket 连接状态
3. **有连接** → 调用 API → 服务器启动执行器 → WebSocket 推送实时数据
4. **无连接** → 启动演示模式 → 模拟执行过程

### 问题 2: 执行器如何知道要执行什么？

**答案**:
- API 接收 `{ "requirement": "..." }`
- 创建 `VibeExecutorIntegrated(requirement)`
- 执行器调用 5 个 Agent

### 问题 3: 界面如何显示实时进度？

**答案**:
- 执行器通过 WebSocket 推送数据
- 界面监听 WebSocket 消息
- 根据消息类型更新界面

### 问题 4: 演示模式和实时模式有什么区别？

| 维度 | 实时模式 | 演示模式 |
|------|---------|---------|
| **WebSocket** | 需要连接 | 不需要 |
| **数据来源** | 真实执行 | 模拟数据 |
| **执行时间** | 3-5 分钟 | 30 秒 |
| **文件生成** | 真实文件 | 模拟文件 |
| **质量评分** | 真实评分 | 随机评分 |

---

## 🚀 使用方式总结

### 方式 1: 完整实时模式

```bash
# 1. 启动服务器
node server.js

# 2. 打开界面
open http://localhost:3000/ui/vibe-dashboard.html

# 3. 输入需求，点击执行
# 实时查看执行进度
```

### 方式 2: 演示模式

```bash
# 1. 直接打开界面（不启动服务器）
open /Users/lifan/.openclaw/workspace/skills/vibe-coding-cn/ui/vibe-dashboard.html

# 2. 输入需求，点击执行
# 观看演示动画
```

### 方式 3: 在 OpenClaw 中执行

```javascript
// 1. 在 OpenClaw 会话中
const { VibeExecutorIntegrated } = require('./executors/vibe-executor-integrated');

const executor = new VibeExecutorIntegrated('做一个个税计算器', {
  wsPort: 8765
});

// 2. 启动执行
executor.execute();

// 3. 打开界面查看进度
```

---

**逻辑状态**: ✅ 已理顺  
**下一步**: 测试验证

**Vibe Coding v3.0** - 逻辑完整，可以执行！ 🎨
