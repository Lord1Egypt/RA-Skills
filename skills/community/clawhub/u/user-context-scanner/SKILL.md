---
name: user-context-scanner
description: 用户画像扫描器v4：自动挖掘用户偏好、行为模式、兴趣图谱，支持实时上下文更新。触发条件：用户表达偏好、检测到行为模式、上下文更新请求。
---

# User Context Scanner - 用户上下文扫描器

## 使用方法

### 直接调用
```bash
node scripts/scanner.js <命令> [选项]
```

### 信号处理模式
```bash
node scripts/scanner.js --process-signal <signal>
```

## 命令

- `scan [选项]` - 扫描并更新用户上下文
- `profile` - 显示当前用户画像
- `stats` - 显示统计信息

## 示例

```bash
# 扫描上下文
node scripts/scanner.js scan

# 显示画像
node scripts/scanner.js profile

# 信号处理
node scripts/scanner.js --process-signal context_update
```

## 与proactive-engine集成

该skill通过`--process-signal`参数与proactive-engine信号系统集成，支持自动更新用户画像。