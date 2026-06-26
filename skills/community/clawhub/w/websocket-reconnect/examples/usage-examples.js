/**
 * WebSocket Reconnect Skill - 使用示例
 */

const { WebSocketReconnect } = require('./scripts/websocket-reconnect.js');

// ============================================
// 示例 1: 基础用法
// ============================================
console.log('=== 示例 1: 基础用法 ===\n');

const ws1 = new WebSocketReconnect({
  url: 'wss://echo.websocket.org',
  maxRetries: 5,
  baseDelay: 1000
});

ws1.on('open', () => {
  console.log('✅ 连接成功');
  ws1.send('Hello WebSocket!');
});

ws1.on('message', (event) => {
  console.log('📨 收到消息:', event.data);
  ws1.close();
});

ws1.on('retry', (info) => {
  console.log(`🔄 重试 ${info.attempt}/${info.maxRetries}，延迟 ${info.delay}ms`);
});

ws1.on('close', () => {
  console.log('❌ 连接关闭\n');
});

// ============================================
// 示例 2: 完整配置
// ============================================
console.log('=== 示例 2: 完整配置 ===\n');

const ws2 = new WebSocketReconnect({
  // 连接配置
  url: 'wss://api.example.com/socket',
  protocols: ['graphql-ws'],
  
  // 重连配置
  maxRetries: 10,
  baseDelay: 1000,
  maxDelay: 30000,
  multiplier: 2,
  jitter: 0.1,
  
  // 心跳配置
  heartbeatInterval: 30000,
  heartbeatTimeout: 5000,
  heartbeatMessage: JSON.stringify({ type: 'ping' }),
  
  // 断路器配置
  circuitBreaker: {
    failureThreshold: 5,
    resetTimeout: 60000,
    halfOpenMaxRequests: 3
  }
});

ws2.on('open', () => console.log('✅ 连接成功'));
ws2.on('message', (event) => console.log('📨 消息:', event.data));
ws2.on('error', (error) => console.error('⚠️ 错误:', error.message));
ws2.on('retry', (info) => console.log(`🔄 重试：${info.attempt}/${info.maxRetries}`));
ws2.on('stateChange', (state) => console.log(`📊 状态变化：${state}`));
ws2.on('circuitChange', (state) => console.log(`🔌 断路器状态：${state}`));

// ============================================
// 示例 3: 状态监控
// ============================================
console.log('=== 示例 3: 状态监控 ===\n');

const ws3 = new WebSocketReconnect({
  url: 'wss://api.example.com/socket'
});

// 定期检查连接状态
setInterval(() => {
  const stats = ws3.getStats();
  console.log('📊 连接统计:', JSON.stringify(stats, null, 2));
}, 10000);

// ============================================
// 示例 4: 聊天客户端
// ============================================
console.log('=== 示例 4: 聊天客户端 ===\n');

class ChatClient {
  constructor(userId) {
    this.userId = userId;
    this.ws = new WebSocketReconnect({
      url: `wss://chat.example.com/socket?user=${userId}`,
      maxRetries: 10,
      baseDelay: 1000,
      heartbeatInterval: 30000
    });
    
    this.setupHandlers();
  }
  
  setupHandlers() {
    this.ws.on('open', () => {
      console.log('✅ 连接到聊天服务器');
      this.ws.send(JSON.stringify({ type: 'online', userId: this.userId }));
    });
    
    this.ws.on('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type !== 'pong') {
        console.log(`[${msg.from}]: ${msg.content}`);
      }
    });
    
    this.ws.on('retry', (info) => {
      console.log(`🔄 重连中... 尝试 ${info.attempt}/${info.maxRetries}`);
    });
  }
  
  send(content) {
    if (this.ws.state === 'OPEN') {
      this.ws.send(JSON.stringify({
        type: 'chat',
        content: content
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

// 使用示例
// const chat = new ChatClient('user123');
// chat.connect();
// chat.send('大家好！');

// ============================================
// 示例 5: GraphQL 订阅
// ============================================
console.log('=== 示例 5: GraphQL 订阅 ===\n');

class GraphQLSubscriptionClient {
  constructor(endpoint) {
    this.ws = new WebSocketReconnect({
      url: endpoint,
      protocols: ['graphql-ws'],
      heartbeatMessage: JSON.stringify({ type: 'connection_init' })
    });
    
    this.subscriptions = new Map();
    this.setupHandlers();
  }
  
  setupHandlers() {
    this.ws.on('open', () => {
      console.log('✅ GraphQL WebSocket 已连接');
      this.resubscribeAll();
    });
    
    this.ws.on('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'next' && msg.id) {
        const sub = this.subscriptions.get(msg.id);
        if (sub) sub.onData(msg.payload);
      }
    });
  }
  
  subscribe(query, variables, callbacks) {
    const id = String(Date.now());
    this.subscriptions.set(id, { query, variables, ...callbacks });
    
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
}

// 使用示例
// const gql = new GraphQLSubscriptionClient('wss://api.example.com/graphql');
// gql.subscribe(
//   'subscription { newPosts { id title } }',
//   {},
//   { onData: (data) => console.log('新帖子:', data) }
// );

console.log('\n💡 提示：取消注释示例代码以运行实际连接');
