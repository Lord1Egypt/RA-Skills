---
name: flink-performance
description: Flink 性能优化技能，用于分析和优化 Flink 任务的性能问题，包括反压检测、Checkpoint 优化、状态优化、并行度调优、内存配置优化等。Use this skill when the user wants to tune or analyze a specific Flink task for backpressure, checkpoint latency, state size, parallelism, memory, throughput, or latency issues. Always trigger only when the request contains a performance intent + a concrete task/job metric or tuning action.
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

# Flink 性能优化技能

基于 `volc_flink` 命令行工具，分析和优化 Flink 任务的性能问题，包括反压检测、Checkpoint 优化、状态优化、并行度调优、内存配置优化等。

---

## 通用约定（必读）

本技能的基础约定与只读约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_READONLY.md`

本技能当前按只读层管理，用于性能问题分析、指标解释和优化建议，不直接执行参数修改或任务变更。

---

## 指标查询前置规则（必须遵守）

在执行任何 `volc_flink jobs metrics` 之前，必须先确认这 3 件事：

1. 这条指标属于 `vcm_flink_metrics.md` 里的哪个一级标题
2. 把该一级标题原样作为 `--sub-namespace` 传入
3. 如果指标维度依赖 `task_name` / `operator_name` / `subtask_index`，补上对应的 `--group-by`

最重要的约束：

- 不允许先拍脑袋查指标，再补 `--sub-namespace`
- 不允许把不同一级标题下的指标混在同一条 `jobs metrics` 命令里
- 如果用户只说“查一下 checkpoint / Kafka lag / JVM / 资源”，你要先在脑中完成：
  - `Checkpoint` -> `--sub-namespace Checkpoint`
  - `Kafka` -> `--sub-namespace Kafka`
  - `JVM` -> `--sub-namespace JVM`
  - `OperatorInfo` -> `--sub-namespace OperatorInfo`
  - `overview` -> `--sub-namespace overview`
  - `resource` -> `--sub-namespace resource`

---

## 🎯 核心流程

### 0. 登录状态检测（从其他 flink 技能借鉴）
**在执行任何操作前，先检测登录状态！**

**检测步骤**：
1. 尝试执行一个简单的命令（如 `volc_flink config show`）
2. 如果提示"请先登录"，则提示用户需要登录
3. 提供登录指引：请使用交互式登录 `volc_flink login`（或企业内部安全方式），不要在对话/命令行参数中粘贴 AK/SK，详见 `../../COMMON.md`

**错误处理**：
- 如果检测到未登录，立即停止后续操作
- 友好提示用户需要先登录

---

### 1. 信息提取与智能选择（从其他 flink 技能借鉴）

#### 1.1 信息提取
从用户提问中提取关键信息：
- **Flink 项目名** (project_name)
- **任务名** (job_name)
- **性能问题描述**：延迟高、吞吐量低、反压、Checkpoint 失败等
- **问题发生时间** (用于日志查询)

如果用户没有明确提供，主动询问缺失的关键信息。

#### 1.2 智能项目和任务选择
**如果用户没有明确提供项目名或任务名，按以下流程处理**：

**场景 A：用户只提供了任务名，没有提供项目名**
1. 列出所有项目：`volc_flink projects list`
2. 在每个项目中搜索匹配的任务名
3. 展示所有匹配的任务供用户选择

**场景 B：用户没有提供任何信息**
1. 先列出所有项目供用户选择
2. 用户选择项目后，列出该项目下的所有任务供用户选择
3. 用户选择任务后，询问性能问题描述

**场景 C：用户提供的项目名或任务名不明确**
1. 使用模糊搜索：`volc_flink jobs list --search <关键词>`
2. 展示匹配结果供用户选择

---

### 2. 性能信息收集

#### 2.1 获取任务详细信息
```bash
volc_flink jobs detail -i <任务ID>
```

#### 2.2 获取任务指标（新增优化）

**步骤 1：先查看可用指标列表**
```bash
volc_flink jobs metrics list
```

**步骤 2：选择关键指标进行查询**

常用关键指标：

| 指标类别 | 指标名称 | `--sub-namespace` | 说明 |
|---------|---------|-------------------|------|
| **Checkpoint** | `flink_jobmanager_job_lastCheckpointDuration` | `Checkpoint` | 最近一次 Checkpoint 耗时 |
| **Checkpoint** | `flink_jobmanager_job_lastCheckpointSize` | `Checkpoint` | 最近一次 Checkpoint 大小 |
| **Checkpoint** | `flink_jobmanager_job_numberOfFailedCheckpoints` | `Checkpoint` | 失败的 Checkpoint 数量 |
| **反压** | `flink_taskmanager_job_task_backPressuredTimeMsPerSecond` | `OperatorInfo` | 反压时间百分比 |
| **反压** | `flink_taskmanager_job_task_busyTimeMsPerSecond_percent` | `OperatorInfo` | 忙时百分比 |
| **吞吐量** | `flink_taskmanager_job_task_operator_numRecordsInPerSecond` | `overview` | 每秒摄入记录数，建议 `--group-by operator_name` |
| **吞吐量** | `flink_taskmanager_job_task_operator_numRecordsOutPerSecond` | `overview` | 每秒输出记录数，建议 `--group-by operator_name` |
| **延迟** | `flink_taskmanager_job_task_operator_latency` | `overview` | 算子延迟（毫秒），建议 `--group-by operator_name` |
| **延迟** | `flink_taskmanager_job_task_operator_currentEmitEventTimeLag` | `overview` | 当前事件时间延迟，建议 `--group-by operator_name` |
| **JVM GC** | `flink_taskmanager_Status_JVM_GarbageCollector_G1_Young_Generation_Count` | `JVM` | Young GC 次数（示例） |
| **JVM GC** | `flink_taskmanager_Status_JVM_GarbageCollector_G1_Young_Generation_Time` | `JVM` | Young GC 耗时（示例） |
| **JVM 内存** | `flink_taskmanager_Status_JVM_Memory_Heap_Used` | `JVM` | 堆内存使用量 |
| **Kafka** | `flink_taskmanager_job_task_operator_KafkaConsumer_records_lag_max` | `Kafka` | Kafka 消费最大滞后 |
| **Kafka** | `flink_taskmanager_job_task_operator_KafkaSourceReader_KafkaConsumer_records_lag_max` | `Kafka` | 新版 KafkaSourceReader 最大滞后 |
| **资源使用** | `job_resource_usage_cpu_all` | `resource` | CPU 使用量 |
| **资源使用** | `job_resource_usage_memory_all` | `resource` | 内存使用量 |

**重要提示**：

- `vcm_flink_metrics.md` 中的指标维度大多基于 `ResourceID`
- `vcm_flink_metrics.md` 的一级标题就是 `jobs metrics` 的 `--sub-namespace` 值，例如：
  - `## Checkpoint` -> `--sub-namespace Checkpoint`
  - `## JVM` -> `--sub-namespace JVM`
  - `## Kafka` -> `--sub-namespace Kafka`
  - `## OperatorInfo` -> `--sub-namespace OperatorInfo`
  - `## overview` -> `--sub-namespace overview`
  - `## resource` -> `--sub-namespace resource`
- CLI 支持两种方式：
  - 直接传 `-u/--gtsjobuuid <ResourceID>`
  - 传 `-i/--job-id <任务ID>`，由 CLI 自动解析出 `ResourceID`
- 对于 `task_name` / `operator_name` / `subtask_index` 这类维度，必须配合 `--group-by`，否则无法稳定定位到具体瓶颈节点
- 一次 `jobs metrics` 调用应只查询同一个 `--sub-namespace` 下的指标，不要把 `JVM`、`resource`、`Checkpoint` 等不同分组的指标混在同一条命令里

**获取 GtsJobUuid**：
```bash
volc_flink jobs uuid -i <任务ID>
```

**查询关键指标的命令示例**：
```bash
# 先获取 GtsJobUuid
GTS_JOB_UUID=$(volc_flink jobs uuid -i <任务ID>)

# 查询 Checkpoint 相关指标
volc_flink jobs metrics -u $GTS_JOB_UUID \
  -m flink_jobmanager_job_lastCheckpointDuration \
  -m flink_jobmanager_job_lastCheckpointSize \
  -m flink_jobmanager_job_numberOfFailedCheckpoints \
  --sub-namespace Checkpoint

# 查询反压相关指标（按 task_name 聚合）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_backPressuredTimeMsPerSecond \
  -m flink_taskmanager_job_task_busyTimeMsPerSecond_percent \
  --group-by task_name \
  --sub-namespace OperatorInfo

# 查询吞吐量和延迟指标（按 operator_name 聚合，overview）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_numRecordsInPerSecond \
  -m flink_taskmanager_job_task_operator_numRecordsOutPerSecond \
  -m flink_taskmanager_job_task_operator_latency \
  -m flink_taskmanager_job_task_operator_currentEmitEventTimeLag \
  --group-by operator_name \
  --sub-namespace overview

# 查询 JVM GC 和内存指标
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_Status_JVM_GarbageCollector_G1_Young_Generation_Count \
  -m flink_taskmanager_Status_JVM_GarbageCollector_G1_Young_Generation_Time \
  -m flink_taskmanager_Status_JVM_Memory_Heap_Used \
  --sub-namespace JVM

# 查询 Kafka lag（按 task_name 聚合）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_KafkaConsumer_records_lag_max \
  -m flink_taskmanager_job_task_operator_KafkaSourceReader_KafkaConsumer_records_lag_max \
  --group-by task_name \
  --sub-namespace Kafka

# 查询资源使用指标
volc_flink jobs metrics -i <任务ID> \
  -m job_resource_usage_cpu_all \
  -m job_resource_usage_memory_all \
  --sub-namespace resource
```

**标准回退流程：metric not found / 无数据 / 查空**

当出现“metric not found”“empty series”“查不到数据”时，按以下顺序回退，不要直接判定“任务没问题”：

1. 先检查指标名是否来自 `vcm_flink_metrics.md`
2. 再检查 `--sub-namespace` 是否与 markdown 一级标题完全一致
3. 再检查是否缺少 `--group-by task_name/operator_name`
4. 对 Kafka 指标，优先同时尝试：
   - `flink_taskmanager_job_task_operator_KafkaConsumer_records_lag_max`
   - `flink_taskmanager_job_task_operator_KafkaSourceReader_KafkaConsumer_records_lag_max`
5. 如果仍然失败，先执行：
   - `volc_flink jobs metrics list --sub-namespace <对应标题>`
   然后从返回列表中重新选择合法指标名再查

**Kafka 指标查询示例（标准版）**

```bash
# Kafka lag：按 vcm_flink_metrics.md 的 Kafka 标题查询
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_KafkaConsumer_records_lag_max \
  -m flink_taskmanager_job_task_operator_KafkaSourceReader_KafkaConsumer_records_lag_max \
  --group-by task_name \
  --sub-namespace Kafka

# 如果用户要看 Kafka 导致的事件时间堆积，再补一个 overview/延迟视角
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_currentEmitEventTimeLag \
  --group-by operator_name \
  --sub-namespace overview
```

#### 2.3 获取任务日志
```bash
# 查询最近 1 小时的 WARNING 日志
volc_flink monitor logs -i <任务ID> --level WARN --lines 200

# 查询最近 1 小时的 ERROR 日志
volc_flink monitor logs -i <任务ID> --level ERROR --lines 200
```

#### 2.4 获取任务运行事件
```bash
volc_flink jobs events -i <任务ID> --limit 50
```

#### 2.5 获取 Flink UI 信息（如果可用）
```bash
# 获取 Flink UI 地址
volc_flink monitor flinkui url -i <任务ID>

# 获取作业概览
volc_flink monitor flinkui overview -i <任务ID>
```

---

### 3. 性能问题分析

#### 3.1 反压检测（Backpressure）

**反压信号**：
- 任务日志中出现反压相关警告
- 某个 Operator 的输出队列满
- Source 端消费速度下降
- Checkpoint 时间变长

**检测方法**：
1. 查看任务日志中的反压警告
2. 检查 Flink UI 中的反压指标
3. 分析任务的吞吐量变化

**优化建议**：
- 增加并行度
- 优化计算逻辑
- 增加缓冲区大小
- 考虑使用异步 IO

---

#### 3.2 Checkpoint 优化

**Checkpoint 问题信号**：
- Checkpoint 超时
- Checkpoint 失败
- Checkpoint 时间过长
- Checkpoint 状态过大

**检测方法**：
1. 查看任务事件中的 Checkpoint 记录
2. 检查 Checkpoint 大小和时间
3. 分析 Checkpoint 失败原因

**优化建议**：
- 增加 Checkpoint 间隔
- 优化状态后端配置
- 减少状态大小
- 启用增量 Checkpoint
- 调整 Checkpoint 超时时间

---

#### 3.3 状态大小优化

**状态问题信号**：
- 状态持续增长
- Checkpoint 状态过大
- 内存使用过高
- OOM 风险

**检测方法**：
1. 查看 Checkpoint 状态大小
2. 分析状态增长趋势
3. 检查内存使用情况

**优化建议**：
- 设置合理的 TTL
- 优化 Key 选择
- 使用 MapState 替代 ListState
- 考虑状态压缩
- 清理不需要的状态

---

#### 3.4 并行度调优

**并行度问题信号**：
- 资源利用率低
- 反压严重
- 吞吐量不达标
- 延迟过高

**检测方法**：
1. 查看当前并行度配置
2. 分析资源利用率
3. 检查反压情况
4. 评估吞吐量和延迟

**优化建议**：
- 根据数据量调整并行度
- 考虑数据倾斜问题
- 确保并行度与 slot 数匹配
- 逐步调整，避免大幅变动

---

#### 3.5 内存配置优化

**内存问题信号**：
- OOM 错误
- GC 频繁
- 内存使用过高
- TaskManager 丢失

**检测方法**：
1. 查看内存配置
2. 分析 GC 日志
3. 检查内存使用情况
4. 查看 OOM 错误

**优化建议**：
- 调整 TaskManager 内存大小
- 优化堆内存和堆外内存比例
- 调整网络缓冲区大小
- 考虑使用内存管理优化

---

#### 3.6 吞吐量和延迟优化

**吞吐量/延迟问题信号**：
- 吞吐量不达标
- 延迟过高
- 处理速度慢
- 数据积压

**检测方法**：
1. 查看吞吐量指标
2. 分析延迟指标
3. 检查数据处理速度
4. 查看数据积压情况

**优化建议**：
- 增加并行度
- 优化计算逻辑
- 使用微批处理
- 调整缓冲区大小
- 考虑异步操作

---

## 性能优化报告结构

**ALWAYS 使用以下格式输出性能优化报告：**

```
# ⚡ Flink 性能优化报告

## 📋 基本信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **任务 ID**: [任务 ID]
- **当前状态**: [状态]
- **分析时间**: [时间]

## 🔍 性能问题分析

### 问题类别
[类别 emoji] **[问题类别]**

### 严重程度
[优先级 emoji] **[严重程度]**

### 问题描述
[用通俗语言描述性能问题]

### 关键证据
- [证据 1]
- [证据 2]
- [证据 3]

## 💡 优化建议

### 1. 立即优化
[具体的优化步骤]

### 2. 中期优化
[中期可以进行的优化]

### 3. 长期优化
[长期的优化建议]

## 📊 性能指标
[附上关键的性能指标数据]

## 🌐 访问地址
- **运维页面**: [运维页面 URL]
- **Flink UI**: [Flink UI URL]
```

---

## 严重程度区分

根据问题严重程度，标记优先级：

🔴 **Critical** — 严重性能问题，需要立即优化。
- 任务频繁失败
- 严重的反压导致数据积压
- Checkpoint 持续失败
- OOM 导致 TaskManager 频繁重启

🟡 **Warning** — 性能下降，建议优化。
- 反压存在但不严重
- Checkpoint 时间较长但未超时
- 吞吐量低于预期
- 延迟较高但可接受

🟢 **Info** — 轻微的优化建议。
- 任务运行正常
- 有优化空间但不影响运行
- 配置可以优化但不是必须的

---

## 性能优化最佳实践

### 反压优化
- **先定位反压源**：找到导致反压的 Operator
- **优化计算逻辑**：简化复杂的计算
- **增加并行度**：如果资源允许
- **使用异步 IO**：对于外部系统访问

### Checkpoint 优化
- **合理设置间隔**：不要太频繁也不要太稀疏
- **使用增量 Checkpoint**：对于大状态任务
- **选择合适的状态后端**：根据状态大小选择
- **调整超时时间**：给足够的时间完成 Checkpoint

### 状态优化
- **设置 TTL**：自动清理过期数据
- **选择合适的 State 类型**：MapState vs ListState
- **优化 Key 分布**：避免数据倾斜
- **考虑状态压缩**：减少存储空间

### 并行度优化
- **根据数据量调整**：不是越大越好
- **考虑 slot 数量**：并行度 <= slot 总数
- **逐步调整**：避免大幅变动
- **监控效果**：调整后观察性能变化

### 内存优化
- **合理分配内存**：JM 和 TM 的内存比例
- **优化堆内存**：根据任务类型调整
- **监控 GC**：避免频繁 Full GC
- **考虑堆外内存**：对于大状态任务

---

## 常用 volc_flink 性能分析命令速查

### 任务信息
```bash
# 列举任务（支持搜索）
volc_flink jobs list --search <关键词>

# 获取任务详情（使用任务 ID）
volc_flink jobs detail -i <任务ID>

# 查询 Checkpoint 指标
volc_flink jobs metrics -i <任务ID> \
  -m flink_jobmanager_job_lastCheckpointDuration \
  -m flink_jobmanager_job_lastCheckpointSize \
  -m flink_jobmanager_job_numberOfFailedCheckpoints \
  --sub-namespace Checkpoint

# 查询反压指标（按 task_name 聚合）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_backPressuredTimeMsPerSecond \
  -m flink_taskmanager_job_task_busyTimeMsPerSecond_percent \
  --group-by task_name \
  --sub-namespace OperatorInfo

# 查询任务历史实例
volc_flink jobs instances -i <任务ID>

# 查询任务运行事件
volc_flink jobs events -i <任务ID>

# 输出任务运维与 FlinkUI 地址
volc_flink jobs ui -i <任务ID>
```

### 监控与日志
```bash
# 查询任务日志（WARNING 级别，最近 1 小时）
volc_flink monitor logs -i <任务ID> --level WARN --lines 200

# 查询任务日志（ERROR 级别，最近 1 小时）
volc_flink monitor logs -i <任务ID> --level ERROR --lines 200

# 按时间范围查询日志
volc_flink monitor logs -i <任务ID> --since "2026-03-19 20:00:00" --until "2026-03-19 22:00:00" --level WARN

# 查询任务运行事件
volc_flink monitor events -i <任务ID> --limit 50

# 获取 Flink UI 地址
volc_flink monitor flinkui url -i <任务ID>

# 获取作业概览
volc_flink monitor flinkui overview -i <任务ID>

# 获取作业异常信息
volc_flink monitor flinkui exceptions -i <任务ID>
```

### 项目管理
```bash
# 列举项目
volc_flink projects list

# 查看项目详情
volc_flink projects detail <项目名>
```

---

## 风险提示模板

注意：以下为风险要点汇总。执行任何会影响任务状态/配置的优化动作（重启、扩缩容、参数变更等）前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认。

### 性能优化风险
- 优化操作可能需要重启任务
- 可能导致数据处理短暂中断
- 优化效果需要时间验证
- 建议先在测试环境验证

### 并行度调整风险
- 任务会重启，导致短暂中断
- 可能导致数据延迟
- 调整后需要监控性能变化
- 资源使用可能增加

### 内存配置调整风险
- 任务会重启，导致短暂中断
- 配置错误可能导致任务启动失败
- 需要验证新配置的正确性
- 建议逐步调整，避免大幅变动

---

## 注意事项

### 重要：性能优化的特殊要求

⚠️ **性能优化时必须遵守以下规则**：

1. **先收集充分信息** - 优化前先收集足够的性能数据
2. **先分析后优化** - 不要盲目优化，先找到问题根因
3. **风险确认** - 执行任何优化操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
4. **逐步优化** - 不要一次性改变太多参数
5. **验证效果** - 优化后验证效果是否符合预期
6. **保留回滚方案** - 优化前确保有回滚方案（如快照）

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **先确认任务范围**：在执行任何操作前，明确确认是哪个任务
3. **先收集性能数据**：优化前先收集充分的性能数据
4. **始终先确认风险**：在执行任何优化操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **先获取任务信息**：在执行操作前，先获取任务的详细信息
6. **逐步优化**：不要一次性改变太多参数
7. **验证优化效果**：优化后验证效果是否符合预期
8. **提供清晰的反馈**：向用户提供清晰的优化建议和结果
9. **使用友好的语言**：用用户能理解的语言解释问题和建议
10. **避免过度技术化**：除非用户要求，否则避免过度技术化的解释

---

## 错误处理优化

### 常见错误及处理

#### 错误 1：未登录
**错误信息**：`❌ 请先登录`

**处理方式**：
- 友好提示："检测到未登录火山引擎账号，请先登录"
- 提供登录指引：请使用交互式登录 `volc_flink login`（或企业内部安全方式），详见 `../../COMMON.md`
- 停止后续操作，等待用户登录后重试

#### 错误 2：任务不存在
**错误信息**：任务 ID 或任务名不存在

**处理方式**：
- 提示："未找到任务，请检查任务名或任务 ID 是否正确"
- 提供帮助：列出该项目下的所有任务供用户选择
- 或者提供搜索功能：`volc_flink jobs list --search <关键词>`

#### 错误 3：日志查询失败
**错误信息**：日志查询超时或失败

**处理方式**：
- 提示："日志查询失败，请稍后重试"
- 建议检查任务状态，确认任务是否正在运行
- 建议尝试缩小时间范围查询

#### 错误 4：指标查询失败
**错误信息**：指标查询失败

**处理方式**：
- 提示："指标查询失败，请稍后重试"
- 建议检查任务状态，确认任务是否正在运行
- 可以尝试通过其他方式分析性能问题

---

## 工具调用顺序（优化版）

### 性能分析完整流程

1. **检测登录状态** - 确认已登录
2. **信息提取** - 从用户提问中提取信息
3. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
4. **获取任务详情** - `volc_flink jobs detail -i <任务ID>`
5. **获取任务指标** - 根据症状选择明确指标名；若要定位瓶颈，补充 `--group-by task_name/operator_name`
6. **获取 WARNING 级别日志** - `volc_flink monitor logs -i <任务ID> --level WARN`
7. **获取 ERROR 级别日志** - `volc_flink monitor logs -i <任务ID> --level ERROR`
8. **获取任务事件** - `volc_flink jobs events -i <任务ID>`
9. **如需要，获取 Flink UI 信息** - `volc_flink monitor flinkui overview -i <任务ID>`
10. **综合分析性能数据，识别问题类型**
11. **给出优化建议和报告**

---

## 🎯 技能总结

### 核心功能
1. ✅ **性能信息收集** - 任务详情、指标、日志、事件
2. ✅ **反压检测和优化** - 识别反压问题并提供优化建议
3. ✅ **Checkpoint 优化** - Checkpoint 问题分析和优化
4. ✅ **状态优化** - 状态大小分析和优化建议
5. ✅ **并行度调优** - 并行度分析和调优建议
6. ✅ **内存配置优化** - 内存配置分析和优化
7. ✅ **吞吐量和延迟优化** - 吞吐量和延迟分析优化
8. ✅ **登录状态检测** - 操作前检测登录状态
9. ✅ **智能项目和任务选择** - 交互式选择、模糊搜索
10. ✅ **性能优化报告** - 结构化的优化报告输出

这个技能可以完整地覆盖 Flink 任务的性能分析和优化流程！
