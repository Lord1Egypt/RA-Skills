# Token Tracker 集成到 OpenClaw 主程序

## 方法 1: 使用 Hook（推荐）

### 步骤

1. **在 OpenClaw 主程序入口添加以下代码**：

```typescript
// 在会话开始时调用
import { recordSessionStart } from './token-tracker-hook';

// 在会话结束时调用
import { recordSessionEnd } from './token-tracker-hook';
```

2. **在 agent-runner-execution.ts 中添加 hook**：

```typescript
// 会话开始前
recordSessionStart();

// agent 执行...
// agent-runner-execution.ts 中的所有执行逻辑

// 会话结束后
recordSessionEnd();
```

### 优点

- 自动记录每次会话的 token 消耗
- 无需手动调用
- 可在任何地方调用统计功能

## 方法 2: 手动记录

### 在会话开始时

```typescript
import { recordSessionStart } from './token-tracker-hook';
recordSessionStart();
```

### 在会话结束时

```typescript
import { recordSessionEnd } from './token-tracker-hook';
recordSessionEnd();
```

### 获取统计信息

```typescript
import { getTodayStats, getWeekStats, getTotalStats, getSavingSuggestions } from './token-tracker-hook';

// 查看今日统计
const todayStats = getTodayStats();

// 查看本周统计
const weekStats = getWeekStats();

// 查看累计统计
const totalStats = getTotalStats();

// 获取节省建议
const suggestions = getSavingSuggestions();
```

## 数据存储

Token 数据存储在 `~/.openclaw/skills/token-tracker/data/token-history.json`

## 注意事项

1. 估算公式：`estimatedTokens = Math.round(duration * 0.5)`
   - 0.5 token/ms 是一个近似值，可能需要根据实际情况调整

2. 会话记录会在会话开始时记录 0 tokens，在会话结束时记录实际消耗

3. 数据文件会自动创建和更新

## 测试

```bash
cd ~/.openclaw/skills/token-tracker

# 测试 hook 功能
npx tsx token-tracker-hook.ts

# 查看统计
npm run token:today
npm run token:week
npm run token:total
npm run token:save
```
