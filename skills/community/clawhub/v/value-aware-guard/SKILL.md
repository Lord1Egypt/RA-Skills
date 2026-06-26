---
name: value-aware-guard
description: 价值守护系统：监控价值漂移，检查边界违规，执行渐进式干预，支持独立CLI和proactive-engine协作。触发条件：价值偏离检测、边界违规、能量低警报、用户模式发现。
---

# Value Aware Guard - 价值守护系统

## 使用方法

### 直接调用
```bash
node scripts/guard.js <命令> [选项]
```

### 信号处理模式
```bash
node scripts/guard.js --process-signal <signal>
```

## 命令

- `monitor [选项]` - 监控价值状态
- `check [选项]` - 检查边界
- `intervene` - 执行干预
- `report [选项]` - 生成报告

## 示例

```bash
# 监控边界
node scripts/guard.js monitor --check-boundaries

# 检查价值对齐
node scripts/guard.js check --alignment

# 信号处理
node scripts/guard.js --process-signal value_drift_detected
```

## 与proactive-engine集成

该skill通过`--process-signal`参数与proactive-engine信号系统集成，支持自动价值监控和干预。