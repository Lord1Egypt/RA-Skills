# WebSocket Reconnect Skill

可靠的 WebSocket 连接管理技能，包含指数退避 + 抖动重连算法、心跳检测和断路器模式。

## 特性

- 🔁 **指数退避重连**: 智能重试策略，延迟时间指数增长
- 🎲 **随机抖动 (Jitter)**: 防止群震问题
- 💓 **心跳检测**: 自动检测僵死连接
- 🔌 **断路器模式**: 防止级联故障
- 📊 **状态监控**: 完整的事件系统和统计信息

## 安装

```bash
cd skills/websocket-reconnect
npm install
```

## 快速开始

```javascript
const { WebSocketReconnect } = require('./scripts/websocket-reconnect.js');

const ws = new WebSocketReconnect({
  url: 'wss://api.example.com/socket',
  maxRetries: 10,
  baseDelay: 1000,
  heartbeatInterval: 30000
});

ws.on('open', () => console.log('Connected'));
ws.on('message', (event) => console.log('Message:', event.data));
ws.on('retry', (info) => console.log(`Retry ${info.attempt}/${info.maxRetries}`));

ws.connect();
```

## 运行测试

```bash
npm test
```

## 文档

详细文档请参阅 [SKILL.md](SKILL.md)

## 许可证

MIT
