# Tiered Context Manager - 架构文档

## 系统架构

```
┌─────────────────────────────────────────────────┐
│           TieredContextEngine v1.0              │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │
│  │   L1    │→ │   L2    │→ │     L3      │   │
│  │ Micro   │  │ Partial │  │ AI(Agent)   │   │
│  └─────────┘  └─────────┘  └─────────────┘   │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │
│  │ Memory  │  │ Cross   │  │  Realtime   │   │
│  │ Tiering │  │ Agent   │  │   Monitor   │   │
│  └─────────┘  └─────────┘  └─────────────┘   │
└─────────────────────────────────────────────────┘
```

## 核心模块

### tiered-engine.js

主压缩引擎，处理L1/L2/L3分层压缩逻辑。

**主要函数：**
- `compact()` - 压缩入口
- `estimateTokens()` - Token计数
- `shouldCompress()` - 判断是否需要压缩

### l3_ai_compressor.js

L3级AI压缩，生成智能摘要。

**主要函数：**
- `createL3Task()` - 创建L3压缩任务
- `processCompletedL3Tasks()` - 处理已完成任务
- `getL3Stats()` - 获取L3统计

### memory_tiering.js

三层记忆生命周期管理。

**主要函数：**
- `getMemoryStats()` - 获取层级统计
- `migrateMemoriesToTiered()` - 迁移未分类记忆
- `cleanupExpiredMemories()` - 清理过期记忆
- `listCleanupCandidates()` - 列出待清理记忆

### cross_agent_context.js

跨Agent知识共享。

**主要函数：**
- `extractAndPublish()` - 提取并发布知识
- `createContextPackage()` - 创建Agent交接包
- `getRecentKnowledge()` - 获取最近共享知识

### realtime_monitor.js

实时会话监控。

**主要函数：**
- `monitorSession()` - 监控单个会话
- `analyzeHistory()` - 分析历史模式
- `adjustThresholds()` - 自适应阈值调整
- `getDashboard()` - 获取监控仪表板

### compression_stats.js

压缩统计与报告。

**主要函数：**
- `recordCompression()` - 记录压缩事件
- `getStats()` - 获取统计
- `generateTextReport()` - 生成文本报告
- `generateMarkdownReport()` - 生成Markdown报告
- `getEfficiencyScore()` - 计算效率评分

## 压缩算法

### L1 微压缩

触发条件：token使用率 > 75%

方法：截断最后N条工具结果消息

```javascript
// 示例
const truncated = messages.slice(0, -TRUNCATE_COUNT);
```

### L2 部分压缩

触发条件：token使用率 > 90%

方法：保留系统消息和最后M条，摘要中间部分

### L3 AI压缩

触发条件：token使用率 > 95%

方法：调用Agent自身的AI能力生成智能摘要

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| L1_threshold | 0.75 | L1触发阈值 |
| L2_threshold | 0.90 | L2触发阈值 |
| L3_threshold | 0.95 | L3触发阈值 |
| min_messages | 6 | 最少保留消息数 |
| l1_truncate_count | 4 | L1截断消息数 |

## 测试

```bash
# 运行所有测试
node scripts/run_tests.js

# 单元测试
node scripts/unit.test.js

# 集成测试
node scripts/integration.test.js

# 压力测试
node scripts/stress.test.js
```

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| 1.0.0 | 2026-04-04 | 初始版本 |
