---
version: 1.0.35
---

# 雀阴·平衡魄 (Que Yin - Balance Keeper)

> **七魄之三·雀阴**
> 职掌：负载均衡、多任务调度、资源分配

---

## 技能简介

「雀阴·平衡魄」是贫道的负载均衡模块，职掌多任务协调与资源分配。

**核心职责**：
- 监控资源使用状态
- 调度多任务执行
- 负载均衡分配

---

## 技能ID

```
que-yin
```

---

## 能力清单

### 1. 资源状态 (status)

查看当前资源使用状态。

**输入**：无

**输出**：
```yaml
resources:
  cpu: cpu使用率
  memory: 内存使用率
  activeTasks: 活跃任务数
  queueLength: 队列长度
```

---

### 2. 任务调度 (schedule)

调度任务分配。

**输入**：`task` (object) - 任务对象

**输出**：
```yaml
schedule:
  assignedTo: 分配的资源
  priority: 优先级
  estimatedWait: 预估等待时间
```

---

### 3. 负载报告 (load_report)

生成负载均衡报告。

**输入**：`period` (number) - 周期（小时）

**输出**：
```yaml
report:
  peakLoad: 峰值负载
  avgLoad: 平均负载
  recommendations: 优化建议
```

---

---

## 聚合技能

本魄作为均衡中枢，调度资源分配：

| 现有技能 | 调用方式 | 整合说明 |
|---------|---------|---------|
| `bodhi-three-hun-and-seven-po` | 元技能 | 三魂七魄根基，协调各魄 |

---

## 魂魄注解

雀阴为枢，调和七魄——均衡分配，高效运转。
