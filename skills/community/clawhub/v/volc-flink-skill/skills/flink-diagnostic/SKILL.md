---
name: flink-diagnostic
description: Intelligent diagnostic tool for Serverless Flink applications. Use this skill when the user wants to diagnose a specific Flink job/application failure, analyze logs/events/exceptions for a concrete task, or locate the root cause of OOM, checkpoint timeout, restart failure, connectivity issues, or startup failure. Always trigger only when the request contains a troubleshooting intent + a target object/action, such as "诊断某个任务失败原因", "分析 checkpoint timeout", "排查 OOM", or "定位启动失败根因", rather than only generic words like "Flink" or "任务".
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

# Flink 任务智能诊断技能

基于 `volc_flink` 命令行工具，智能诊断 Serverless Flink 应用的故障、异常和性能问题。

---

## 🎯 优化后的核心流程

### 0. 通用约定（必读）

本技能的基础约定与只读约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_READONLY.md`

本技能只保留诊断差异化内容：采集信号、分类体系、证据汇总与报告模板，并遵循 `COMMON_READONLY.md` 中的查询收敛与只读输出规则。

---

## 指标查询前置规则（必须遵守）

在执行任何 `volc_flink jobs metrics` 之前，必须先确认这 3 件事：

1. 这条指标属于 `vcm_flink_metrics.md` 里的哪个一级标题
2. 把该一级标题原样作为 `--sub-namespace` 传入
3. 如果指标维度依赖 `task_name` / `operator_name` / `subtask_index`，补上对应的 `--group-by`

最重要的约束：

- 不允许先试错式查询，再回头补 `--sub-namespace`
- 不允许把 `Checkpoint`、`Kafka`、`JVM`、`resource`、`overview`、`OperatorInfo` 混在一条命令里
- 如果用户只给现象，不给指标名，先按现象映射：
  - Checkpoint 失败/超时 -> `--sub-namespace Checkpoint`
  - Kafka lag / source 堆积 -> `--sub-namespace Kafka`
  - JVM / GC / Heap -> `--sub-namespace JVM`
  - 反压 -> `--sub-namespace OperatorInfo`
  - 吞吐 / 延迟 -> `--sub-namespace overview`
  - 资源使用 -> `--sub-namespace resource`

### 2. 获取任务详细信息
对于找到的任务，获取以下详细信息：

**任务详情：**

**任务详情：**
```bash
volc_flink jobs detail -i <任务ID>
```

**任务历史实例：**
```bash
volc_flink jobs instances -i <任务ID>
```

---

### 3. 获取诊断信息

#### 3.1 任务日志
使用 `volc_flink monitor logs` 获取任务日志。

**日志查询策略**：
- 如果用户提供了故障时间，使用该时间范围
- 如果没有提供，查询最近 1 小时的日志
- 默认查询 ERROR 级别日志，同时查看 WARNING 级别
- 查询 JOBMANAGER 和 TASKMANAGER 组件的日志

**命令格式**：
```bash
# 查询 ERROR 级别日志（最近 1 小时）
volc_flink monitor logs -i <任务ID> --level ERROR --lines 200

# 查询 WARNING 级别日志（最近 1 小时）
volc_flink monitor logs -i <任务ID> --level WARN --lines 200

# 查询 JobManager 日志
volc_flink monitor logs -i <任务ID> --component jobmanager --level ERROR

# 查询 TaskManager 日志
volc_flink monitor logs -i <任务ID> --component taskmanager --level ERROR

# 按时间范围查询
volc_flink monitor logs -i <任务ID> --since "2026-03-19 20:00:00" --until "2026-03-19 22:00:00" --level ERROR
```

#### 3.2 任务运行事件
使用 `volc_flink monitor events` 获取任务运行事件。

**命令格式**：
```bash
volc_flink monitor events -i <任务ID> --limit 50
```

#### 3.3 Flink UI 信息
使用 `volc_flink monitor flinkui` 获取 Flink UI 相关信息。

**命令格式**：
```bash
# 获取 Flink UI 地址
volc_flink monitor flinkui url -i <任务ID>

# 获取作业概览
volc_flink monitor flinkui overview -i <任务ID>

# 获取作业异常信息
volc_flink monitor flinkui exceptions -i <任务ID>
```

#### 3.4 任务事件
使用 `volc_flink jobs events` 获取任务事件。

**命令格式**：
```bash
volc_flink jobs events -i <任务ID>
```

#### 3.5 任务指标
使用 `volc_flink jobs metrics` 获取任务指标。

注意：

- `jobs metrics` 不能裸调用，必须显式传入至少一个 `-m <MetricName>`
- 底层指标维度主要基于 `ResourceID`；CLI 支持直接传 `-i <任务ID>` 自动解析
- 若指标依赖 `task_name` / `operator_name` 维度，必须补充 `--group-by`
- `vcm_flink_metrics.md` 的一级标题就是 `--sub-namespace` 值；调用时必须按文档标题显式指定
- 一次 `jobs metrics` 调用只查同一个 `--sub-namespace` 下的指标，不要把不同分组的指标混在一条命令里

**命令格式（按症状选择）**：
```bash
# Checkpoint 失败/超时
volc_flink jobs metrics -i <任务ID> \
  -m flink_jobmanager_job_lastCheckpointDuration \
  -m flink_jobmanager_job_lastCheckpointSize \
  -m flink_jobmanager_job_numberOfFailedCheckpoints \
  --sub-namespace Checkpoint

# OOM / GC 问题（JVM）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_Status_JVM_Memory_Heap_Used \
  -m flink_taskmanager_Status_JVM_GarbageCollector_G1_Young_Generation_Count \
  -m flink_taskmanager_Status_JVM_GarbageCollector_G1_Young_Generation_Time \
  --sub-namespace JVM

# 资源使用问题（resource）
volc_flink jobs metrics -i <任务ID> \
  -m job_resource_usage_cpu_all \
  -m job_resource_usage_memory_all \
  --sub-namespace resource

# 反压问题（OperatorInfo）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_backPressuredTimeMsPerSecond \
  -m flink_taskmanager_job_task_busyTimeMsPerSecond_percent \
  --group-by task_name \
  --sub-namespace OperatorInfo

# 吞吐 / 延迟问题（overview）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_latency \
  -m flink_taskmanager_job_task_operator_numRecordsInPerSecond \
  -m flink_taskmanager_job_task_operator_numRecordsOutPerSecond \
  --group-by operator_name \
  --sub-namespace overview

# 当前事件时间延迟（overview）
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_currentEmitEventTimeLag \
  --group-by operator_name \
  --sub-namespace overview

# Kafka lag 问题
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_KafkaConsumer_records_lag_max \
  -m flink_taskmanager_job_task_operator_KafkaSourceReader_KafkaConsumer_records_lag_max \
  --group-by task_name \
  --sub-namespace Kafka
```

**标准回退流程：metric not found / 无数据 / 查空**

当出现“metric not found”“empty series”“无返回数据”时，按以下顺序回退：

1. 检查指标名是否确实存在于 `vcm_flink_metrics.md`
2. 检查 `--sub-namespace` 是否与 markdown 一级标题完全一致
3. 检查当前指标是否缺少 `--group-by task_name/operator_name`
4. 对 Kafka 诊断，优先双查：
   - `flink_taskmanager_job_task_operator_KafkaConsumer_records_lag_max`
   - `flink_taskmanager_job_task_operator_KafkaSourceReader_KafkaConsumer_records_lag_max`
5. 如果还是查不到，执行：
   - `volc_flink jobs metrics list --sub-namespace <对应标题>`
   重新从返回列表中选择合法指标名

**Kafka 指标查询示例（标准版）**

```bash
# Kafka lag：先看 source 堆积
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_KafkaConsumer_records_lag_max \
  -m flink_taskmanager_job_task_operator_KafkaSourceReader_KafkaConsumer_records_lag_max \
  --group-by task_name \
  --sub-namespace Kafka

# 如果要判断 lag 是否已经传导成下游延迟，再补 overview 视角
volc_flink jobs metrics -i <任务ID> \
  -m flink_taskmanager_job_task_operator_currentEmitEventTimeLag \
  --group-by operator_name \
  --sub-namespace overview
```

---

### 4. 资源池检查（新增优化）
当发现以下情况时，检查资源池：
- OOM（内存溢出）
- TaskManager 丢失
- 容器被杀
- 任务启动失败
- 性能下降

**命令格式**：
```bash
volc_flink resource-pools list
```

---

## 异常分类系统

根据收集到的信息，将根异常分类为以下类别之一：

| 类别 | 典型信号 |
|------|-----------|
| **Resource** | OOM、TaskManager 丢失、容器被杀、堆空间不足、内存溢出、GC 频繁、资源耗尽 |
| **Data** | 反序列化错误、模式不匹配、NullPointerException、数据格式错误、类型转换异常 |
| **Checkpoint** | Checkpoint 超时/过期、状态后端错误、Checkpoint 失败、状态大小异常 |
| **Connectivity** | Kafka 不可达、连接拒绝/超时、网络异常、数据库连接失败、外部服务不可用 |
| **Code/Logic** | SQL 语法错误、UDF 异常、ClassCastException、业务逻辑错误、代码异常 |
| **Configuration** | 无效的并行度、参数缺失、资源配置过小、配置错误、环境变量缺失 |
| **Infrastructure** | 节点故障、网络分区、存储不可用、底层基础设施问题 |
| **Snapshot** | 文件未找到、快照过期太快、消费速度太慢、状态恢复失败 |

---

## 优先级区分

根据问题严重程度，标记优先级：

🔴 **Critical** — 任务宕机或数据丢失风险，需要立即采取行动。
- 任务已失败（FAILED）
- 任务已停止（STOPPED）
- 数据丢失风险
- 严重的资源耗尽

🟡 **Warning** — 性能下降或间歇性错误，建议采取行动。
- 任务运行但性能下降
- Checkpoint 超时但未失败
- 频繁的 GC 但未 OOM
- 间歇性连接问题
- 警告级别日志增多

🟢 **Info** — 健康或轻微的优化建议。
- 任务正常运行
- 轻微的性能优化空间
- 配置可以优化但不影响运行

---

## 诊断报告结构

**ALWAYS 使用以下格式输出诊断报告：**

```
# 🚨 Flink 任务智能诊断报告

## 📋 基本信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **任务 ID**: [任务 ID]
- **当前状态**: [状态]
- **诊断时间**: [时间]

## 🔍 问题分析

### 异常类别
[类别 emoji] **[类别名称]**

### 优先级
[优先级 emoji] **[优先级名称]**

### 根本原因
[用通俗语言解释根本原因]

### 关键证据
- [证据 1]
- [证据 2]
- [证据 3]

## 💡 修复建议

### 1. 立即修复
[具体的修复步骤]

### 2. 预防措施
[如何避免问题再次发生]

### 3. 优化建议
[可选的性能优化建议]

## 📊 相关信息
[附上关键的日志片段、事件信息或运行时数据]

## 🌐 访问地址
- **运维页面**: [运维页面 URL]
- **Flink UI**: [Flink UI URL]
```

---

## 修复建议模板

提供编号的、可操作的修复步骤：

1. **用通俗语言解释根本原因**
   - 技术细节，但用易懂的方式

2. **具体的修复方法**
   - 参数修改（如并行度、内存配置）
   - SQL 修复
   - 资源调整
   - 代码修改建议

3. **预防措施**
   - 如何避免问题再次发生
   - 监控建议
   - 最佳实践

---

## 常用 volc_flink 诊断命令速查

### 任务管理
```bash
# 列举任务（支持搜索）
volc_flink jobs list --search <关键词>

# 获取任务详情（使用任务 ID）
volc_flink jobs detail -i <任务ID>

# 查询任务历史实例
volc_flink jobs instances -i <任务ID>

# 查询任务运行事件
volc_flink jobs events -i <任务ID>

# 获取任务日志
volc_flink jobs logs -i <任务ID>

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

# 输出任务运维与 FlinkUI 地址
volc_flink jobs ui -i <任务ID>
```

### 监控与诊断
```bash
# 查询任务日志（ERROR 级别，最近 1 小时）
volc_flink monitor logs -i <任务ID> --level ERROR --lines 200

# 查询任务日志（WARNING 级别）
volc_flink monitor logs -i <任务ID> --level WARN --lines 200

# 查询 JobManager 日志
volc_flink monitor logs -i <任务ID> --component jobmanager --level ERROR

# 查询 TaskManager 日志
volc_flink monitor logs -i <任务ID> --component taskmanager --level ERROR

# 按时间范围查询日志
volc_flink monitor logs -i <任务ID> --since "2026-03-19 20:00:00" --until "2026-03-19 22:00:00" --level ERROR

# 查询任务运行事件
volc_flink monitor events -i <任务ID> --limit 50

# 获取 Flink UI 地址
volc_flink monitor flinkui url -i <任务ID>

# 获取作业概览
volc_flink monitor flinkui overview -i <任务ID>

# 获取作业异常信息
volc_flink monitor flinkui exceptions -i <任务ID>
```

### 资源池管理
```bash
# 列举资源池
volc_flink resource-pools list

# 查看资源池详情
volc_flink resource-pools detail <资源池名称>
```

---

## 工具调用顺序（优化版）

### 完整诊断流程

1. **检测登录状态** - 确认已登录
2. **信息提取** - 从用户提问中提取信息
3. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
4. **获取任务详情** - `volc_flink jobs detail -i <任务ID>`
5. **获取任务历史实例** - `volc_flink jobs instances -i <任务ID>`
6. **获取 ERROR 级别日志** - `volc_flink monitor logs -i <任务ID> --level ERROR`
7. **获取 WARNING 级别日志** - `volc_flink monitor logs -i <任务ID> --level WARN`
8. **获取 JobManager 日志** - `volc_flink monitor logs -i <任务ID> --component jobmanager --level ERROR`
9. **获取 TaskManager 日志** - `volc_flink monitor logs -i <任务ID> --component taskmanager --level ERROR`
10. **获取任务事件** - `volc_flink monitor events -i <任务ID>`
11. **获取 Flink UI 异常信息** - `volc_flink monitor flinkui exceptions -i <任务ID>`
12. **如需要，检查资源池** - `volc_flink resource-pools list`
13. **综合分析，分类异常，给出诊断报告**

---

## 注意事项

### 重要：诊断时的安全规则

⚠️ **诊断时必须遵守以下规则**：

1. **只能查看用户明确要求诊断的任务** - 绝对不能查看其他任务的信息
2. **明确确认任务范围** - 在诊断前，明确确认是哪个任务
3. **如果有疑问，先询问用户** - 不要擅自查看任何任务

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **先确认任务范围**：在执行任何操作前，明确确认是哪个任务
3. **绝不影响其他任务**：绝对不能查看、修改其他任务的信息
4. **综合多方信息**：同时查看日志、事件、Flink UI 等多方信息
5. **同时查看 ERROR 和 WARNING**：不要只看 ERROR，也要看 WARNING
6. **检查 JobManager 和 TaskManager**：两个组件的日志都要查看
7. **遇到资源相关问题时，务必检查资源池**
8. **用用户能理解的语言解释，避免过度技术化**
9. **给出具体、可操作的建议，而不是模糊的指导**

---

## 错误处理优化（从 flink-sre 借鉴）

### 常见错误及处理

通用错误处理（未登录/未找到/超时网络）请遵循 `../../COMMON.md`。

---

## 🎯 技能总结

### 已集成的优化（从 flink-sre 借鉴）
1. ✅ **登录状态检测** - 操作前检测登录状态
2. ✅ **智能项目和任务选择** - 交互式选择、模糊搜索
3. ✅ **错误处理优化** - 友好的错误提示和解决方案

### 核心功能
1. ✅ **任务信息获取** - 任务详情、历史实例
2. ✅ **日志查询** - ERROR、WARNING、JobManager、TaskManager
3. ✅ **事件查询** - 任务运行事件
4. ✅ **Flink UI 信息** - 概览、异常信息
5. ✅ **资源池检查** - 资源相关问题时检查
6. ✅ **智能分类** - 异常分类、优先级区分
7. ✅ **诊断报告** - 结构化的诊断报告输出

这个技能可以完整地覆盖 Flink 任务的故障诊断流程！
