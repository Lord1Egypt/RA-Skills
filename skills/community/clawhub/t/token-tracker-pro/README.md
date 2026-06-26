# Token Tracker 使用指南

## 安装

```bash
npm install -g tsx
```

## 快速开始

```bash
cd ~/.openclaw/skills/token-tracker

# 查看今日统计
npm run token:today

# 查看本周统计
npm run token:week

# 查看累计统计
npm run token:total

# 查看历史记录
npm run token:history

# 获取节省建议
npm run token:save
```

## 集成到 OpenClaw 主程序

### 方法 1: 使用 Hook（推荐）

详见 `INTEGRATION.md`

```typescript
// 会话开始时
import { recordSessionStart } from './token-tracker-hook';
recordSessionStart();

// agent 执行...

// 会话结束时
import { recordSessionEnd } from './token-tracker-hook';
recordSessionEnd();
```

### 方法 2: 手动记录

```typescript
// 会话开始时
import { recordSessionStart } from './token-tracker-hook';
recordSessionStart();

// 会话结束时
import { recordSessionEnd } from './token-tracker-hook';
recordSessionEnd();
```

## 数据文件

- 数据文件：`data/token-history.json`
- CLI入口：`token-tracker-entry.ts`
- Hook入口：`token-tracker-hook.ts`

## 修复进度

- ✅ CLI 工具参数传递问题 - 已修复
- ✅ 优化节省建议算法 - 已修复
- ✅ 添加自动记录功能 - 已完成
- ✅ 集成到 OpenClaw 主程序 - 已完成

## 当前状态

累计消耗：9,000 tokens
本周消耗：5,500 tokens
今日消耗：0 tokens
