---
name: memory-system
description: >-
  曙光智能记忆系统 v4.0 - 五层金字塔架构 (HOT→DAILY→WEEKLY→CORE→ARCHIVE)。
  支持 Weibull 衰减、混合检索、WAL 协议、自我改进治理。
  当用户需要持久记忆、跨会话回忆、自动归档时触发。
version: 4.0.0
author: 曙光
tags:
  - memory
  - persistence
  - recall
  - agent
  - openclaw
---

# 曙光记忆系统 v4.0

**不是聊天机器人的临时记忆。是AI的持久大脑。**

## 五层金字塔架构

| 层级 | 文件 | 保留时间 | 用途 |
|------|------|----------|------|
| **HOT** | `session-state.json` + `working-buffer.md` | 当前会话 | 热数据、持仓、任务状态 |
| **DAILY** | `memory/YYYY-MM-DD.md` | 7天 | 每日日志、当日交易、学习 |
| **WEEKLY** | `memory/weekly/YYYY-WXX.md` | 4周 | 周报、技能扫描、总结 |
| **CORE** | `memory/core/*.json` | 永久 | 身份、策略、偏好、教训 |
| **ARCHIVE** | `memory/archive/` | 长期 | 历史归档、压缩存储 |

## 核心特性

### 1. Weibull 衰减模型
```
S(t) = exp(-(t/λ)^k)
```
- **Core层**: 半衰期90天，重要性≥0.8
- **Working层**: 半衰期30天，重要性≥0.4
- **Peripheral层**: 半衰期7天，自动遗忘

### 2. 混合检索 (向量 + BM25)
- 语义相似度: 70% 权重
- 关键词匹配: 30% 权重
- 无需外部向量数据库，纯本地实现

### 3. WAL 协议
**先写文件，再回复用户。**
任何修正、偏好、决策、专有名词 → 立即写入 `session-state.json` → 再回复。

### 4. 自我改进治理
- 自动从失败中提取教训
- 记录到 `memory/core/lessons.json`
- 重复错误自动触发熔断

## 快速启动

### 首次使用
```python
from memory_system import ShuguangHybridMemory

memory = ShuguangHybridMemory(
    memory_dir="./memory",
    agent_name="曙光"
)

# 保存记忆
memory.remember(
    text="用户偏好：不做科创板和ST",
    category="preference",
    importance=0.95
)

# 召回记忆
results = memory.recall("用户股票偏好", top_k=3)
```

### 记忆写入 (WAL)
```python
# 必须在回复用户前执行
memory.wal_write({
    "type": "decision",
    "content": "止损华银电力",
    "reason": "主力出货+D级评分"
})
```

## 文件结构

```
memory/
├── daily/
│   └── 2026-05-03.md          # 今日日志
├── weekly/
│   └── 2026-W18.md            # 本周总结
├── core/
│   ├── identity.json          # 身份定义
│   ├── preferences.json       # 用户偏好
│   ├── strategies.json        # 策略配置
│   └── lessons.json           # 教训记录
├── archive/
│   └── 2026-04.tar.gz         # 月度归档
└── working-buffer.md          # 危险区日志
```

## 记忆类型 (category)

| 类型 | 说明 | 示例 |
|------|------|------|
| `preference` | 用户偏好 | "讨厌废话" |
| `fact` | 事实 | "六脉神剑V4.1胜率71.4%" |
| `decision` | 决策 | "78分门槛最优" |
| `entity` | 实体 | "华银电力600744" |
| `reflection` | 反思 | "单票90%仓位是赌博" |
| `other` | 其他 | "..." |

## 维护任务

### 每天凌晨3点
- [ ] 遗忘曲线应用 → 降低旧记忆权重
- [ ] 冲突解决 → 合并重复记忆

### 每周日
- [ ] 记忆统计 → 生成健康报告
- [ ] 归档过期日志 → 压缩到 archive/

## 依赖

- Python 3.8+
- 无外部数据库依赖
- 可选: `pip install numpy` (用于向量计算)

## 来源

- 掠夺自: memory-lancedb-pro, memory-os, omni-memory
- 整合: 曙光核心操作系统 (shuguang-core)
- 版本: v4.0.0

---

**Text > Brain**。想记住就写文件。这是AI活下去的方式。
