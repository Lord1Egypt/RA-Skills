---
name: flink-monitor
description: Flink 实时监控技能，用于实时监控任务运行状态、查询指标、查看事件和日志。Use this skill when the user wants to view logs, metrics, events, or current runtime status for a specific Flink task/job. Always trigger only when the request contains a monitoring intent + a concrete task/job object/action.
required_binaries:
  - volc_flink
may_access_config_paths:
  - ~/.volc_flink
  - $VOLC_FLINK_CONFIG_DIR
credentials:
  primary: volc_flink_local_config
  optional_env_vars:
    - VOLCENGINE_ACCESS_KEY
    - VOLCENGINE_SECRET_KEY
    - VOLCENGINE_REGION
---

# Flink 实时监控技能

用于实时监控 Flink 任务运行状态、查询指标、查看事件和日志。

---

## 🎯 核心功能

### 0. 通用约定（必读）

本技能的基础约定与只读约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_READONLY.md`

本技能默认是只读流程，不执行任务启停、发布、扩缩容、删除等变更操作。
执行查询前，仍必须先完成 `COMMON.md` 中的 Scope & Identity（确认 project/job），并遵循 `COMMON_READONLY.md` 中的查询收敛与输出约定。

### 2. 实时任务监控

#### 2.1 查看任务详情
使用 `volc_flink jobs detail` 查看任务详情。

**命令格式**：
```bash
volc_flink jobs detail -i <任务ID>
```

**监控内容包括**：
- 任务状态（RUNNING、FAILED、STOPPED 等）
- 任务配置
- 运行时信息
- 资源使用情况
- 启动时间、运行时长

#### 2.2 查询任务指标
使用 `volc_flink jobs metrics` 查询任务指标。

**命令格式**：
```bash
volc_flink jobs metrics -i <任务ID>
```

**指标内容包括**：
- 吞吐量（Throughput）
- 延迟（Latency）
- 状态大小（State Size）
- Checkpoint 相关指标
- 反压（Backpressure）指标
- 等等...

#### 2.3 查询任务运行事件
使用 `volc_flink monitor events` 查询任务运行事件。

**命令格式**：
```bash
volc_flink monitor events -i <任务ID> --limit <数量>
```

**事件内容包括**：
- 任务状态变更事件
- Checkpoint 完成事件
- 异常事件
- 部署事件
- 等等...

#### 2.4 查询任务日志
使用 `volc_flink monitor logs` 查询任务日志。

**命令格式**：
```bash
# 查询最近的日志
volc_flink monitor logs -i <任务ID>

# 查询 ERROR 级别日志
volc_flink monitor logs -i <任务ID> --level ERROR

# 查询 WARNING 级别日志
volc_flink monitor logs -i <任务ID> --level WARN

# 查询 JobManager 日志
volc_flink monitor logs -i <任务ID> --component jobmanager

# 查询 TaskManager 日志
volc_flink monitor logs -i <任务ID> --component taskmanager

# 按时间范围查询
volc_flink monitor logs -i <任务ID> --since "<开始时间>" --until "<结束时间>"
```

#### 2.5 Flink UI 访问
使用 `volc_flink monitor flinkui` 访问 Flink UI。

**命令格式**：
```bash
# 获取 Flink UI 地址
volc_flink monitor flinkui url -i <任务ID>

# 获取作业概览
volc_flink monitor flinkui overview -i <任务ID>

# 获取作业异常信息
volc_flink monitor flinkui exceptions -i <任务ID>
```

---

### 3. 综合监控面板

整合以上信息，提供综合监控面板：

**监控面板内容**：
1. 任务基本信息（状态、运行时长等）
2. 关键指标（吞吐量、延迟、状态大小等）
3. 最近事件（状态变更、Checkpoint 等）
4. 最近告警（ERROR、WARNING 日志）
5. 访问链接（Flink UI、运维页面等）

---

## 工具调用顺序

### 综合监控流程
1. **检测登录状态** - 确认已登录
2. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
3. **获取任务详情** - `volc_flink jobs detail -i <任务ID>`
4. **查询任务指标** - `volc_flink jobs metrics -i <任务ID>`
5. **查询任务事件** - `volc_flink monitor events -i <任务ID>`
6. **查询 ERROR 日志** - `volc_flink monitor logs -i <任务ID> --level ERROR`
7. **获取 Flink UI 地址** - `volc_flink monitor flinkui url -i <任务ID>`
8. **展示综合监控面板** - 整合所有信息

### 专项监控流程
根据用户需求，只执行相应的监控操作：
- 查看状态 → 获取任务详情
- 查看指标 → 查询任务指标
- 查看事件 → 查询任务事件
- 查看日志 → 查询任务日志
- 访问 Flink UI → 获取 Flink UI 地址

---

## 常用 volc_flink monitor 命令速查

### 任务监控
```bash
# 获取任务详情
volc_flink jobs detail -i <任务ID>

# 查询任务指标
volc_flink jobs metrics -i <任务ID>

# 查询任务事件
volc_flink jobs events -i <任务ID>

# 获取任务日志（GAS）
volc_flink jobs logs -i <任务ID>

# 输出任务运维与 FlinkUI 地址
volc_flink jobs ui -i <任务ID>
```

### Monitor 子命令
```bash
# 查询任务运行事件
volc_flink monitor events -i <任务ID> --limit 50

# 查询任务日志
volc_flink monitor logs -i <任务ID> --level ERROR --lines 200

# 查询 JobManager 日志
volc_flink monitor logs -i <任务ID> --component jobmanager --level ERROR

# 查询 TaskManager 日志
volc_flink monitor logs -i <任务ID> --component taskmanager --level ERROR

# 按时间范围查询日志
volc_flink monitor logs -i <任务ID> --since "2026-03-19 20:00:00" --until "2026-03-19 22:00:00" --level ERROR

# 获取 Flink UI 地址
volc_flink monitor flinkui url -i <任务ID>

# 获取作业概览
volc_flink monitor flinkui overview -i <任务ID>

# 获取作业异常信息
volc_flink monitor flinkui exceptions -i <任务ID>
```

---

## 输出格式

### 综合监控面板
```
# 📊 Flink 任务实时监控面板

## 📋 基本信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **任务 ID**: [任务ID]
- **当前状态**: [状态] 🔴🟡🟢
- **运行时长**: [时长]
- **启动时间**: [时间]

## 📈 关键指标
- **吞吐量**: [值] records/s
- **延迟**: [值] ms
- **状态大小**: [值] MB
- **Checkpoint 间隔**: [值] s
- **最后 Checkpoint**: [时间]

## 📋 最近事件
1. [事件时间] - [事件类型] - [事件描述]
2. [事件时间] - [事件类型] - [事件描述]
3. [事件时间] - [事件类型] - [事件描述]

## ⚠️ 最近告警
1. [时间] - ERROR - [错误描述]
2. [时间] - WARN - [警告描述]

## 🌐 访问地址
- **运维页面**: [URL]
- **Flink UI**: [URL]

## 💡 后续建议
[根据监控情况给出建议]
```

### 指标查询反馈
```
# 📈 Flink 任务指标

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **查询时间**: [时间]

## 📊 指标详情

### 吞吐量
- **Source 吞吐量**: [值] records/s
- **Sink 吞吐量**: [值] records/s
- **各 Operator 吞吐量**: [详细数据]

### 延迟
- **端到端延迟**: [值] ms
- **各 Operator 延迟**: [详细数据]

### 状态
- **总状态大小**: [值] MB
- **各 Operator 状态大小**: [详细数据]

### Checkpoint
- **最后 Checkpoint 时间**: [时间]
- **Checkpoint 间隔**: [值] s
- **Checkpoint 状态**: [状态]

## 💡 分析
[根据指标给出分析和建议]
```

### 日志查询反馈
```
# 📝 Flink 任务日志

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **日志级别**: [级别]
- **查询时间**: [时间]

## 📄 日志内容
```
[日志内容]
```

## 💡 分析
[根据日志给出分析和建议]
```

---

## 错误处理

### 常见错误及处理

通用错误处理（未登录/未找到/超时网络）请遵循 `../../COMMON.md`。

监控查询失败时，优先缩小范围：
- 日志：缩短 `--since/--until` 时间窗口，减少 `--lines`
- 事件：降低 `--limit`

---

## 注意事项

### 重要：监控的实时性

⚠️ **监控数据的实时性**：
- 指标数据可能有一定延迟
- 日志查询可能需要时间
- 建议定期刷新监控数据
- 重要指标建议设置告警

### 重要：任务状态解读

⚠️ **任务状态说明**：
- 🟢 **RUNNING** - 正常运行
- 🟡 **STARTING** / **STOPPING** - 过渡状态
- 🔴 **FAILED** - 任务失败，需要处理
- ⚪ **STOPPED** - 任务已停止

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **智能任务选择**：如果用户没有提供任务，总是先列出任务供选择
3. **整合多维度信息**：提供综合监控面板，而不是单一信息
4. **关键指标高亮**：重要指标要突出显示
5. **异常及时告警**：发现异常要及时提醒用户
6. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案

---

## 🎯 技能总结

### 核心功能
1. ✅ **任务详情监控** - 查看任务状态、配置、运行时信息
2. ✅ **指标查询** - 查询吞吐量、延迟、状态大小等指标
3. ✅ **事件查询** - 查询任务运行事件
4. ✅ **日志查询** - 查询多级别、多组件的任务日志
5. ✅ **Flink UI 访问** - 获取 Flink UI 地址和信息
6. ✅ **综合监控面板** - 整合多维度监控信息

### 与其他技能的关系
- **依赖 flink-volc** - 需要先登录才能进行监控
- **配合 flink-diagnostic** - 发现异常后可以用 diagnostic 深入分析
- **配合 flink-sre** - 根据监控情况进行运维操作
- **配合 flink-performance** - 根据指标进行性能优化

这个技能是实时监控的核心，让用户可以随时了解任务的运行状态！
