---
name: reliable-api-client
description: Node.js API 客户端黄金标准 v3.0 - 多Endpoint + 多Key轮询 + 限流 + 熔断器
homepage: https://github.com/tvvshow/openclaw-evomap
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": {},
        "install": [],
      },
  }
---

# Node.js API 客户端黄金标准 v3.0

整合多Endpoint + 多Key轮询 + 限流 + 连接池 + 指数退避重试 + 熔断器

## 新功能 (v3.0)

| 功能 | 说明 |
|------|------|
| **多Endpoint** | 支持多个上游地址，自动故障转移 |
| **Endpoint熔断** | 每个Endpoint独立熔断器 |
| **优先级策略** | 支持 priority/least-used/round-robin |
| **延迟监控** | 跟踪每个Endpoint的响应时间 |

## 使用方法

```javascript
const ReliableAPIClient = require('./reliable-api-client');

const client = new ReliableAPIClient({
  // 多 Endpoint 支持
  endpoints: [
    { url: 'https://api.example.com', priority: 10 },  // 高优先级
    { url: 'https://backup.example.com', priority: 5 }
  ],
  endpointStrategy: 'priority',  // priority | round-robin | least-used
  endpointCooldown: 60000,      // 1分钟冷却
  
  // 多 Key 支持
  apiKeys: ['key1', 'key2', 'key3'],
  keyStrategy: 'round-robin',
  
  // 限流
  maxQPS: 10,
  
  // 重试
  maxRetries: 3,
  
  // 熔断
  circuitThreshold: 5,
  circuitReset: 30000,
  
  // 连接池
  poolSize: 20
});

// 添加更多 Endpoint
client.addEndpoint('https://new-endpoint.com', priority: 8);
client.addAPIKey('new-key');

// 请求
const data = await client.get('/users');
const result = await client.post('/orders', { item: 'test' });

// 统计
console.log('Endpoints:', client.getEndpointStats());
console.log('Keys:', client.getKeyStats());
console.log('Circuit:', client.getCircuitBreakerStatus(url));
```

## 架构

```
请求 → [限流器] → [Endpoint选择] → [Key选择] → [熔断器] → 发送
                                      ↓
                              [指数退避重试]
                                      ↓
                              [失败 → 切换Endpoint/Key]
```

## 故障转移逻辑

1. 优先选择健康的 Endpoint
2. 按策略选择（priority/least-used/round-robin）
3. 请求失败 → 标记 Endpoint 错误
4. 连续失败 → 熔断器打开
5. 熔断后 → 自动切换到下一个 Endpoint
6. 冷却后 → Endpoint 恢复健康

## 文件

- `reliable-api-client.js` - 主代码

## 相关文档

- `EVOMAP_STANDARD.md` - 胶囊发布规范
