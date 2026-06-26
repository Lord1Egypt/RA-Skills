---
name: tiered-context-manager
description: 多Agent协作的智能会话上下文管理系统。当需要管理AI agent的长会话压缩、多层记忆分层、跨Agent知识共享时激活。支持L1/L2/L3分层压缩、实时监控、统计分析。用于OpenClaw agent的上下文管理优化。
---

# Tiered Context Manager

多Agent协作的智能会话上下文管理系统。

## 核心功能

### 1. 分层压缩 (Tiered Compression)

| 层级 | 触发 | 方法 | 成本 |
|------|------|------|------|
| **L1** | 75% | 截断最后N条工具结果 | $0 |
| **L2** | 90% | 摘要前半段 | $0 |
| **L3** | 95% | AI智能摘要 | Agent's AI |

### 2. 记忆分层 (Memory Tiering)

```
Persistent (365天) → Normal (30天) → Ephemeral (7天)
```

### 3. 跨Agent协作

- 共享记忆
- Inbox任务队列
- 防冲突机制

## 使用方式

### 扫描压缩
```bash
node skills/tiered-context-manager/scripts/tiered_standalone.js scan
```

### 查看统计
```bash
node skills/tiered-context-manager/scripts/tiered_standalone.js stats
```

### 生成报告
```bash
node skills/tiered-context-manager/scripts/tiered_standalone.js report
```

## API

```javascript
const { TieredContextEngine } = require('./tiered-engine.js');

const engine = new TieredContextEngine({
  openclawVersion: '1.0.0'
});

const result = await engine.compact({
  sessionFile: '/path/to/session.jsonl',
  tokenBudget: 100000,
  currentTokenCount: 85000
});
```

## 模块说明

| 模块 | 文件 | 功能 |
|------|------|------|
| 主引擎 | `tiered-engine.js` | L1/L2/L3压缩入口 |
| L3压缩 | `l3_ai_compressor.js` | AI摘要任务队列 |
| 记忆分层 | `memory_tiering.js` | 三层记忆管理 |
| 跨Agent | `cross_agent_context.js` | 知识共享 |
| 实时监控 | `realtime_monitor.js` | 阈值监控 |
| 统计分析 | `compression_stats.js` | 效果统计 |

## 配置

编辑 `config/default.json`:

```json
{
  "compression": {
    "L1_threshold": 0.75,
    "L2_threshold": 0.90,
    "L3_threshold": 0.95,
    "min_messages": 6
  }
}
```

## 测试

```bash
node skills/tiered-context-manager/scripts/run_tests.js
```

## 详细信息

详见 `references/architecture.md` - 完整架构文档
