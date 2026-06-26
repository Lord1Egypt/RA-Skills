# Token Tracker 快速开始

## 功能

记录和追踪 OpenClaw 会话的 token 消耗，提供每日、每周和累计统计，并提出节省 token 的建议。

## 安装

```bash
cd ~/.openclaw/skills/token-tracker
npm install
```

## 使用

### 方式 1: 使用 npx tsx 运行

```bash
# 查看今日统计
npx tsx token-tracker-cli.ts today

# 查看本周统计
npx tsx token-tracker-cli.ts week

# 查看累计统计
npx tsx token-tracker-cli.ts total

# 查看历史记录
npx tsx token-tracker-cli.ts history

# 获取节省建议
npx tsx token-tracker-cli.ts save

# 清理历史数据（保留30天）
npx tsx token-tracker-cli.ts cleanup
```

### 方式 2: 在代码中使用

```typescript
import { tokenTracker } from './token-tracker';

// 记录 token 消耗
tokenTracker.record({
  model: 'zai/glm-4.7-flash',
  tokens: 1500,
  sessionKey: 'current-session'
});

// 获取今日统计
const todayStats = tokenTracker.getTodayStats();
console.log('今日消耗:', todayStats.total);

// 获取节省建议
const suggestions = tokenTracker.getSavingSuggestions();
suggestions.forEach(s => console.log(s));
```

## 节省 Token 的建议

### 1. 使用 Memory 优化
- 使用 `memory_search` 而不是重复搜索
- 使用 `memory_get` 获取特定部分
- 避免重复读取 MEMORY.md

### 2. 减少不必要的工具调用
- 合并多个工具调用
- 减少日志输出
- 避免不必要的检查

### 3. 优化查询
- 使用更精确的搜索词
- 限制结果数量
- 使用缓存

### 4. 会话管理
- 定期清理不必要的历史
- 使用会话重置
- 避免过度轮次

### 5. 使用更高效的模型
- 优先使用 `zai/glm-4.7-flash`
- 避免使用高 token 消耗的模型

## 数据存储

Token 历史数据存储在：
```
~/.openclaw/skills/token-tracker/data/token-history.json
```

## 测试

```bash
# 运行测试
npx tsx test.ts
```

## 更新日志

### v1.0.0 (2026-03-17)
- ✅ 初始版本
- ✅ 支持每日/每周/累计统计
- ✅ 支持历史记录查询
- ✅ 支持节省建议生成
- ✅ 支持数据清理
