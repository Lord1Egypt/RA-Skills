# 📊 Observability - 可观测性系统

**版本**: v0.1.0  
**状态**: ✅ 核心功能完成

---

## 🎯 快速开始

### 1. 安装依赖

```bash
cd skills/observability
npm install
```

### 2. 基础使用

```javascript
const { ObservabilitySystem } = require('./src/index');

const obs = new ObservabilitySystem();

// 记录日志
obs.logger.info('Agent started', { agentId: '001' });

// 链路追踪
const trace = obs.startTrace('agent.execute', { query: 'test' });
// ... 执行操作 ...
trace.end({ result: 'success' });

// 记录指标
obs.metrics.counter('calls.total').inc();
obs.metrics.histogram('calls.latency').observe(150);
```

### 3. 启动 Dashboard

```bash
npm start
# 访问 http://localhost:3001
```

---

## 📖 完整文档

- **SKILL.md** - 完整技能文档
- **src/logger.js** - 结构化日志
- **src/metrics.js** - 性能指标
- **src/index.js** - 主入口
- **src/dashboard.js** - 监控面板

---

## 🧪 测试

```bash
npm test
```

---

*最后更新：2026-03-18*
