---
name: websocket-reconnect
description: WebSocket connection management with exponential backoff + jitter retry, heartbeat detection, and circuit breaker pattern. Use when you need reliable WebSocket connections that automatically recover from network failures.
license: MIT
metadata: {"author":"custom","version":"1.0.0","openclaw":{"emoji":"🔌","requires":{"bins":["node"]}}}
---

# WebSocket Reconnect Skill

可靠的 WebSocket 连接管理，包含指数退避 + 抖动重连算法、心跳检测和断路器模式。

## 特性

- **指数退避重连**: 智能重试策略，延迟时间指数增长
- **随机抖动 (Jitter)**: 防止群震问题 (thundering herd)
- **心跳检测**: 自动检测僵死连接并触发重连
- **断路器模式**: 三次状态 (CLOSED, OPEN, HALF-OPEN) 防止级联故障
- **最大重试上限**: 避免无限重试消耗资源
- **事件驱动**: 完整的事件系统用于状态监控

## 安装依赖

```bash
npm install ws
```

## 快速开始

### 基础用法

```javascript
const { WebSocketReconnect } = require('./scripts/websocket-reconnect.js');

const ws = new WebSocketReconnect({
  url: 'wss://api.example.com/socket',
  maxRetries: 10,
  baseDelay: 1000,
  maxDelay: 30000
});

// 监听事件
ws.on('open', () => {
  console.log('✅ Connected');
});

ws.on('message', (event) => {
  console.log('📨 Message:', event.data);
});

ws.on('close', (event) => {
  console.log('❌ Closed:', event.code, event.reason);
});

ws.on('error', (error) => {
  console.error('⚠️ Error:', error.message);
});

ws.on('retry', (info) => {
  console.log(`🔄 Retry ${info.attempt}/${info.maxRetries} in ${info.delay}ms`);
});

// 连接
ws.connect();

// 发送消息
ws.send(JSON.stringify({ type: 'subscribe', channel: 'updates' }));

// 关闭连接
// ws.close();
```

### 完整配置示例

```javascript
const ws = new WebSocketReconnect({
  // 连接配置
  url: 'wss://api.example.com/socket',
  protocols: ['graphql-ws'],
  websocketOptions: {
    headers: {
      'Authorization': 'Bearer token123'
    }
  },
  
  // 重连配置
  maxRetries: 10,           // 最大重试次数
  baseDelay: 1000,          // 基础延迟 (ms)
  maxDelay: 30000,          // 最大延迟 (ms)
  multiplier: 2,            // 退避倍数
  jitter: 0.1,              // 抖动系数 (0-1)
  
  // 心跳配置
  heartbeatInterval: 30000,  // 心跳间隔 (ms)
  heartbeatTimeout: 5000,    // 心跳超时 (ms)
  heartbeatMessage: JSON.stringify({ type: 'ping' }),
  
  // 断路器配置
  circuitBreaker: {
    failureThreshold: 5,     // 失败阈值
    resetTimeout: 60000,     // 重置超时 (ms)
    halfOpenMaxRequests: 3   // 半开状态最大请求数
  }
});
```

## 重连策略

### 指数退避计算

重连延迟按指数增长，避免频繁重试：

```
延迟 = baseDelay × (multiplier ^ 尝试次数)
```

示例 (baseDelay=1000ms, multiplier=2):
- 第 1 次重试：1000ms (1 秒)
- 第 2 次重试：2000ms (2 秒)
- 第 3 次重试：4000ms (4 秒)
- 第 4 次重试：8000ms (8 秒)
- ...
- 达到 maxDelay 后不再增长

### 抖动 (Jitter)

添加随机抖动防止多个客户端同时重试：

```javascript
// jitter = 0.1 时，延迟在 ±10% 范围内随机
实际延迟 = 计算延迟 × (0.9 ~ 1.1)
```

## 心跳检测机制

### 工作原理

1. 连接成功后，每隔 `heartbeatInterval` 发送 ping 消息
2. 等待服务器在 `heartbeatTimeout` 内回复 pong
3. 如果超时，认为连接已僵死，自动关闭并触发重连

### 服务器端要求

服务器需要响应 ping 消息：

```javascript
// 服务器示例 (Node.js + ws)
wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    
    if (message.type === 'ping') {
      ws.send(JSON.stringify({ type: 'pong' }));
    }
    
    // ... 处理其他消息
  });
});
```

### 自定义心跳消息

如果服务器使用不同的心跳协议：

```javascript
const ws = new WebSocketReconnect({
  url: 'wss://api.example.com',
  heartbeatInterval: 30000,
  heartbeatMessage: 'PING',  // 字符串
  // 或者
  heartbeatMessage: { cmd: 'heartbeat' }  // 对象 (会自动 JSON.stringify)
});

// 监听 pong 响应
ws.on('message', (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'pong') {
    console.log('Heartbeat OK');
  }
});
```

## 断路器模式

### 三种状态

**CLOSED (正常)**
- 请求正常通过
- 跟踪失败次数
- 失败达到阈值时打开

**OPEN (熔断)**
- 请求立即失败，不尝试连接
- 防止对故障服务的过载
- 经过 `resetTimeout` 后自动转为 HALF-OPEN

**HALF-OPEN (测试)**
- 允许有限数量的请求通过
- 成功则转为 CLOSED
- 失败则转回 OPEN

### 状态监控

```javascript
ws.on('circuitChange', (state) => {
  console.log(`Circuit breaker state: ${state}`);
  
  if (state === 'OPEN') {
    console.log('⚠️ Service temporarily unavailable');
  }
});

// 手动查询状态
const circuitState = ws.getCircuitState(); // 'CLOSED', 'OPEN', or 'HALF-OPEN'
```

### 手动控制断路器

```javascript
// 手动打开断路器
ws.openCircuit();

// 手动关闭断路器 (重置)
ws.closeCircuit();
```

## 事件参考

| 事件 | 参数 | 描述 |
|------|------|------|
| `open` | 无 | 连接成功建立 |
| `message` | `event` | 收到消息 (原生 MessageEvent) |
| `close` | `{code, reason}` | 连接关闭 |
| `error` | `Error` | 发生错误 |
| `retry` | `{attempt, delay, maxRetries}` | 即将重试 |
| `stateChange` | `state` | 连接状态变化 |
| `circuitChange` | `state` | 断路器状态变化 |

## 状态监控

### 获取统计信息

```javascript
const stats = ws.getStats();
console.log(stats);
// {
//   state: 'OPEN',
//   circuitState: 'CLOSED',
//   retryCount: 2,
//   maxRetries: 10,
//   circuitFailures: 0,
//   failureThreshold: 5,
//   lastActivity: 1709532000000,
//   uptime: 15000
// }
```

### 连接状态

- `CLOSED`: 未连接
- `CONNECTING`: 正在连接
- `OPEN`: 已连接
- `CLOSING`: 正在关闭
- `BLOCKED`: 被断路器阻止
- `FAILED`: 超过最大重试次数

## 完整示例

### 实时聊天客户端

```javascript
const { WebSocketReconnect } = require('./scripts/websocket-reconnect.js');

class ChatClient {
  constructor(userId) {
    this.userId = userId;
    this.ws = new WebSocketReconnect({
      url: `wss://chat.example.com/socket?user=${userId}`,
      maxRetries: 10,
      baseDelay: 1000,
      maxDelay: 30000,
      heartbeatInterval: 30000,
      heartbeatTimeout: 5000,
      circuitBreaker: {
        failureThreshold: 5,
        resetTimeout: 60000
      }
    });
    
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    this.ws.on('open', () => {
      console.log('✅ Connected to chat server');
      // 发送上线通知
      this.ws.send(JSON.stringify({
        type: 'online',
        userId: this.userId
      }));
    });
    
    this.ws.on('message', (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    });
    
    this.ws.on('close', () => {
      console.log('❌ Disconnected from chat server');
    });
    
    this.ws.on('error', (error) => {
      console.error('⚠️ Chat error:', error.message);
    });
    
    this.ws.on('retry', (info) => {
      console.log(`🔄 Reconnecting... Attempt ${info.attempt}/${info.maxRetries}`);
    });
    
    this.ws.on('circuitChange', (state) => {
      if (state === 'OPEN') {
        console.log('⚠️ Chat service temporarily unavailable');
      }
    });
  }
  
  handleMessage(message) {
    switch (message.type) {
      case 'pong':
        // 心跳响应，忽略
        break;
      case 'chat':
        console.log(`[${message.from}]: ${message.content}`);
        break;
      case 'system':
        console.log(`[System]: ${message.content}`);
        break;
    }
  }
  
  sendMessage(content) {
    if (this.ws.state === 'OPEN') {
      this.ws.send(JSON.stringify({
        type: 'chat',
        content: content
      }));
    } else {
      console.log('⚠️ Cannot send message: not connected');
    }
  }
  
  connect() {
    return this.ws.connect();
  }
  
  disconnect() {
    this.ws.close();
  }
}

// 使用示例
const chat = new ChatClient('user123');
chat.connect();
chat.sendMessage('Hello, world!');
```

### GraphQL 订阅客户端

```javascript
const { WebSocketReconnect } = require('./scripts/websocket-reconnect.js');

class GraphQLSubscriptionClient {
  constructor(endpoint, options = {}) {
    this.ws = new WebSocketReconnect({
      url: endpoint,
      protocols: ['graphql-ws'],
      maxRetries: options.maxRetries || 10,
      heartbeatInterval: options.heartbeatInterval || 30000,
      heartbeatMessage: JSON.stringify({ type: 'connection_init' }),
      ...options
    });
    
    this.subscriptions = new Map();
    this.subscriptionId = 0;
    
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    this.ws.on('open', () => {
      console.log('✅ GraphQL WebSocket connected');
      // 重新订阅所有订阅
      this.resubscribeAll();
    });
    
    this.ws.on('message', (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    });
  }
  
  handleMessage(message) {
    switch (message.type) {
      case 'connection_ack':
        console.log('GraphQL connection acknowledged');
        break;
      case 'next':
        const subscription = this.subscriptions.get(message.id);
        if (subscription && subscription.onData) {
          subscription.onData(message.payload);
        }
        break;
      case 'complete':
        const sub = this.subscriptions.get(message.id);
        if (sub && sub.onComplete) {
          sub.onComplete();
        }
        this.subscriptions.delete(message.id);
        break;
      case 'error':
        const s = this.subscriptions.get(message.id);
        if (s && s.onError) {
          s.onError(message.payload);
        }
        break;
    }
  }
  
  subscribe(query, variables, callbacks) {
    const id = String(++this.subscriptionId);
    
    this.subscriptions.set(id, {
      query,
      variables,
      onData: callbacks.onData,
      onError: callbacks.onError,
      onComplete: callbacks.onComplete
    });
    
    if (this.ws.state === 'OPEN') {
      this.ws.send(JSON.stringify({
        id,
        type: 'subscribe',
        payload: { query, variables }
      }));
    }
    
    return () => this.unsubscribe(id);
  }
  
  unsubscribe(id) {
    this.subscriptions.delete(id);
    if (this.ws.state === 'OPEN') {
      this.ws.send(JSON.stringify({
        id,
        type: 'complete'
      }));
    }
  }
  
  resubscribeAll() {
    for (const [id, sub] of this.subscriptions) {
      this.ws.send(JSON.stringify({
        id,
        type: 'subscribe',
        payload: { query: sub.query, variables: sub.variables }
      }));
    }
  }
  
  connect() {
    return this.ws.connect();
  }
  
  disconnect() {
    this.ws.close();
  }
}
```

## 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `url` | string | 必填 | WebSocket 服务器 URL |
| `protocols` | array | `[]` | 子协议列表 |
| `websocketOptions` | object | `{}` | WebSocket 构造函数选项 (Node.js) |
| `maxRetries` | number | `10` | 最大重试次数 |
| `baseDelay` | number | `1000` | 基础延迟 (毫秒) |
| `maxDelay` | number | `30000` | 最大延迟 (毫秒) |
| `multiplier` | number | `2` | 退避倍数 |
| `jitter` | number | `0.1` | 抖动系数 (0-1) |
| `heartbeatInterval` | number | `30000` | 心跳间隔 (毫秒) |
| `heartbeatTimeout` | number | `5000` | 心跳超时 (毫秒) |
| `heartbeatMessage` | string | `{"type":"ping"}` | 心跳消息 |
| `circuitBreaker.failureThreshold` | number | `5` | 打开断路器的失败次数 |
| `circuitBreaker.resetTimeout` | number | `60000` | 断路器重置超时 (毫秒) |
| `circuitBreaker.halfOpenMaxRequests` | number | `3` | 半开状态最大请求数 |

## 最佳实践

### 1. 合理设置重试次数

```javascript
// 关键业务：更多重试
maxRetries: 20, baseDelay: 2000

// 非关键业务：较少重试
maxRetries: 5, baseDelay: 1000
```

### 2. 心跳间隔选择

```javascript
// 高频交易：短间隔
heartbeatInterval: 10000, heartbeatTimeout: 3000

// 普通应用：标准间隔
heartbeatInterval: 30000, heartbeatTimeout: 5000

// 低带宽场景：长间隔
heartbeatInterval: 60000, heartbeatTimeout: 10000
```

### 3. 断路器阈值

```javascript
// 敏感服务：低阈值快速熔断
circuitBreaker: { failureThreshold: 3, resetTimeout: 30000 }

// 稳定服务：高阈值避免误熔断
circuitBreaker: { failureThreshold: 10, resetTimeout: 120000 }
```

### 4. 优雅关闭

```javascript
// 应用退出前
ws.close(1001, 'Client shutting down');

// 而不是直接
process.exit();
```

## 故障排查

### 问题：频繁重连

**原因**: 服务器不稳定或网络问题

**解决**:
1. 增加 `baseDelay` 和 `maxDelay`
2. 降低 `maxRetries`
3. 检查服务器日志

### 问题：心跳超时

**原因**: 服务器未响应 ping 或网络延迟高

**解决**:
1. 增加 `heartbeatTimeout`
2. 确认服务器正确响应 ping
3. 检查网络质量

### 问题：断路器持续 OPEN

**原因**: 服务持续故障

**解决**:
1. 检查服务健康状态
2. 增加 `failureThreshold`
3. 减少 `resetTimeout` 更快尝试恢复

## 性能影响

### 内存占用

每个实例约 1-2MB (包括事件处理器和定时器)

### CPU 占用

- 空闲连接：几乎为零 (仅心跳定时器)
- 重连期间：低 (指数退避减少重试频率)

### 网络流量

- 心跳：每 30 秒约 100 字节
- 重连：根据网络状况动态调整

## 浏览器兼容性

支持所有现代浏览器 (Chrome, Firefox, Safari, Edge) 和 Node.js 14+

## 许可证

MIT
