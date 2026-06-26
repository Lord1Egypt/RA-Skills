---
name: flink-sre
description: Flink SRE 自动化运维工具，用于管理 Flink 任务的启动、停止、重启、扩容、缩容、配置修改等操作。Use this skill when the user wants to stop, restart, rescale, or update parameters for a specific running Flink job/application. Always trigger only when the request contains an operations intent + a concrete job/application object/action.
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

# Flink SRE 自动化运维技能

基于 `volc_flink` 命令行工具，自动化管理 Serverless Flink 应用的启动、停止、重启、扩容、缩容、配置修改等运维操作。

## 🎯 优化后的核心流程

### 0. 通用约定（必读）

本技能的基础约定与变更约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_MUTATION.md`

本技能只保留 SRE 差异化内容：参数验证、配置对比、rescale/restart 的执行与监控建议，并遵循 `COMMON_MUTATION.md` 中的 Risk Confirmation、变更前检查和操作后验证规则。

### 2. 参数验证（新增优化）
**在执行任何操作前，必须验证输入参数的合法性！**

#### 2.1 并行度验证
- **合法范围**：1 - 1000
- **验证逻辑**：
  ```
  if parallelism < 1:
      错误提示：并行度不能小于 1，建议值：1-100
  if parallelism > 1000:
      错误提示：并行度不能大于 1000，建议值：1-100
  ```

#### 2.2 TM 规格验证
- **合法规格**：
  - 1C4GB（1核CPU，4GB内存）
  - 2C8GB（2核CPU，8GB内存）
  - 4C16GB（4核CPU，16GB内存）
  - 8C32GB（8核CPU，32GB内存）
  - 16C64GB（16核CPU，64GB内存）

- **验证逻辑**：
  - CPU 必须是：1, 2, 4, 8, 16 之一
  - 内存配比必须是 1:4（1核对应4GB内存）
  - 如果规格不合法，提示合法的规格列表

#### 2.3 TM slot 数量验证
- **合法范围**：1 - 8
- **建议值**：1, 2, 4, 8
- **验证逻辑**：
  ```
  if tm_slots < 1:
      错误提示：TM slot 数量不能小于 1
  if tm_slots > 8:
      错误提示：TM slot 数量不能大于 8，建议值：1, 2, 4, 8
  ```

#### 2.4 验证失败处理
- 如果参数验证失败，**不执行任何操作**
- 明确告诉用户哪个参数不合法
- 提供合法的参数值建议
- 让用户重新输入

---

### 3. 获取当前配置与对比展示（新增优化）
**在执行扩容/缩容/修改配置前，必须获取并展示当前配置！**

#### 3.1 使用 rescale --dry-run 获取配置变更
对于扩容/缩容操作，使用 `--dry-run` 参数获取将要变更的配置：

```bash
volc_flink jobs rescale -i <任务ID> --parallelism <新并行度> --tm-cpu <新CPU> --tm-mem-ratio <配比> --tm-slots <新slot数> --dry-run
```

#### 3.2 配置对比展示（新增优化）
**必须以表格形式清晰展示当前配置 vs 新配置的对比！**

**展示格式**：
```
📊 当前配置 vs 新配置对比：
| 配置项 | 当前值 | 新值 | 变更 |
|--------|--------|------|------|
| parallelism.default | 20 | 2 | 🔽 降低 |
| kubernetes.taskmanager.cpu | 4 | 2 | 🔽 降低 |
| taskmanager.memory.process.size | 16384mb | 8192mb | 🔽 降低 |
| taskmanager.numberOfTaskSlots | 4 | 2 | 🔽 降低 |
```

**变更标记**：
- 🔽 降低：数值变小（缩容）
- 🔼 增加：数值变大（扩容）
- ➡️ 不变：数值保持不变

---

### 4. 风险确认
**在执行任何变更操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认！**

统一使用 `../../COMMON.md` 的 Risk Confirmation 模板；只有当用户明确确认后，才继续执行操作。

---

### 5. 执行操作

#### 启动任务
使用 `volc_flink jobs start -i <任务ID>` 启动任务。

**命令格式**：
```bash
volc_flink jobs start -i <任务ID>
```

#### 停止任务
使用 `volc_flink jobs stop -i <任务ID>` 停止任务。

**命令格式**：
```bash
volc_flink jobs stop -i <任务ID>
```

#### 重启任务
使用 `volc_flink jobs restart -i <任务ID> --inspect` 重启任务。

**命令格式**：
```bash
volc_flink jobs restart -i <任务ID> --inspect
```

#### 扩容/缩容任务（优化版 - 优先使用 rescale）
**⚠️ 重要：扩容/缩容优先使用 `volc_flink jobs rescale` 命令！**

**为什么使用 rescale 命令**：
- ✅ 自动更新草稿配置
- ✅ 自动发布草稿
- ✅ 自动重启任务
- ✅ 自动监控任务状态直到 RUNNING
- ✅ 支持 dry-run 预览
- ✅ 支持规格便捷参数（--tm-spec、--jm-spec）

**详细步骤**：
1. **参数验证** - 验证并行度、TM 规格、TM slot 等参数是否合法
2. **获取当前配置** - 使用 `volc_flink jobs detail` 获取当前配置
3. **Dry-run 预览变更** - 使用 `--dry-run` 获取将要变更的配置
4. **展示配置对比** - 以表格形式展示当前配置 vs 新配置
5. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
6. **执行 rescale** - 使用 `--inspect` 参数自动监控重启过程
7. **验证结果** - 确认任务成功恢复为 RUNNING 状态

**命令格式**：
```bash
# 方式 1: 使用 --tm-spec 和 --jm-spec（推荐，更便捷）
# Step 1: Dry-run 预览变更
volc_flink jobs rescale -i <任务ID> --parallelism <新并行度> --tm-spec <TM规格> --jm-spec <JM规格> --dry-run

# Step 2: 执行 rescale 并监控
volc_flink jobs rescale -i <任务ID> --parallelism <新并行度> --tm-spec <TM规格> --jm-spec <JM规格> --inspect

# 方式 2: 使用单独参数（更灵活）
# Step 1: Dry-run 预览变更
volc_flink jobs rescale -i <任务ID> --parallelism <新并行度> --tm-cpu <新CPU> --tm-mem-ratio <配比> --tm-slots <新slot数> --jm-cpu <新JM CPU> --jm-mem-ratio <JM配比> --dry-run

# Step 2: 执行 rescale 并监控
volc_flink jobs rescale -i <任务ID> --parallelism <新并行度> --tm-cpu <新CPU> --tm-mem-ratio <配比> --tm-slots <新slot数> --jm-cpu <新JM CPU> --jm-mem-ratio <JM配比> --inspect
```

**规格参数示例**：
- `--tm-spec 1C4GB` - TaskManager: 1核CPU, 4GB内存
- `--tm-spec 2C8GB` - TaskManager: 2核CPU, 8GB内存
- `--jm-spec 0.5C2GB` - JobManager: 0.5核CPU, 2GB内存
- `--jm-spec 1C4GB` - JobManager: 1核CPU, 4GB内存

**配比参数**：
- `--tm-mem-ratio 1:4` - TaskManager CPU:内存 = 1:4（推荐）
- `--jm-mem-ratio 1:4` - JobManager CPU:内存 = 1:4（推荐）

#### 修改配置参数
修改配置参数需要以下步骤：
1. **参数验证** - 验证要修改的配置参数是否合法
2. 获取草稿内容：`volc_flink drafts content -i <草稿ID>`
3. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
4. 更新草稿参数：`volc_flink drafts params set -i <草稿ID> --kv <key>=<value>`
5. 发布草稿：`volc_flink drafts publish -i <草稿ID>`
6. 重启任务：`volc_flink jobs restart -i <任务ID> --inspect`

---

### 6. 状态监控（新增优化）
**操作完成后，持续监控任务状态一段时间！**

#### 6.1 实时状态更新
使用 `--inspect` 参数让命令自动监控任务状态：
```bash
volc_flink jobs restart -i <任务ID> --inspect
volc_flink jobs rescale -i <任务ID> ... --inspect
```

#### 6.2 状态展示
在监控过程中，实时展示状态变化：
```
⏳ 任务状态更新中...
- 当前状态：STARTING
- 已等待：15秒
- 剩余超时：285秒

✅ 任务已进入 RUNNING 状态！
```

#### 6.3 异常处理
如果任务状态异常（如 FAILED），立即通知用户：
```
❌ 任务状态异常！
- 当前状态：FAILED
- 建议：检查任务日志，排查错误原因
```

---

### 7. 验证操作结果
操作执行完成后，使用以下工具验证结果：
- `volc_flink jobs detail -i <任务ID>` - 查看最新的任务详情
- `volc_flink jobs instances -i <任务ID>` - 查看历史实例
- `volc_flink monitor logs -i <任务ID>` - 查看任务日志

向用户报告操作结果。

---

## 错误处理

通用错误处理（未登录/未找到/超时网络）请遵循 `../../COMMON.md`。本技能特有错误主要来自参数验证失败与 rescale dry-run 对比异常，处理原则是：不执行变更、明确指出不合法参数/差异点并要求用户确认后再继续。

---

## 操作类型说明

| 操作类型 | 描述 | 需要确认 |
|---------|------|---------|
| **启动任务** | 启动已停止的 Flink 任务 | ✅ 是 |
| **停止任务** | 停止正在运行的 Flink 任务 | ✅ 是 |
| **重启任务** | 重启 Flink 任务（先停止再启动） | ✅ 是 |
| **扩容任务** | 增加任务的并行度 | ✅ 是 |
| **缩容任务** | 减少任务的并行度 | ✅ 是 |
| **修改配置** | 修改 Flink 任务的配置参数 | ✅ 是 |

---

## 风险提示模板

### 启动任务风险
- 任务启动可能需要较长时间
- 如果任务有积压数据，启动后可能需要时间追赶
- 启动失败可能需要手动干预

### 停止任务风险
- 任务停止后，数据处理将中断
- 可能导致数据延迟
- 停止失败可能需要手动干预

### 重启任务风险
- 任务会短暂中断
- 可能导致数据延迟
- 重启失败可能需要手动干预
- Checkpoint 可能需要重新开始

### 扩容/缩容风险
- 任务会重启，导致短暂中断
- 可能导致数据延迟
- 扩容后可能需要更多资源
- 缩容可能影响处理性能
- 重新部署可能失败

### 修改配置风险
- 任务会重启，导致短暂中断
- 可能导致数据延迟
- 配置错误可能导致任务启动失败
- 需要验证新配置的正确性

---

## 输出格式

**ALWAYS 使用以下格式输出操作结果：**

```
# ⚙️ Flink SRE 操作执行结果

## 📋 操作信息
- **操作类型**: [操作类型]
- **项目名**: [项目名]
- **任务名**: [任务名]
- **执行时间**: [时间]

## ✅ 操作结果
[描述操作是否成功]

## 📊 当前状态
- **任务状态**: [当前状态]
- **并行度**: [当前并行度]
- **其他关键信息**: [其他信息]

## 💡 后续建议
[给出后续操作建议]
```

---

## 常用 volc_flink 命令速查

### 项目管理
```bash
# 列举项目
volc_flink projects list

# 查看项目详情
volc_flink projects detail <项目名>
```

### 任务管理
```bash
# 列举任务（支持搜索）
volc_flink jobs list --search <关键词>

# 获取任务详情（使用任务 ID）
volc_flink jobs detail -i <任务ID>

# 启动任务
volc_flink jobs start -i <任务ID>

# 停止任务
volc_flink jobs stop -i <任务ID>

# 重启任务（带状态监控）
volc_flink jobs restart -i <任务ID> --inspect

# 扩容/缩容任务（推荐方式）
volc_flink jobs rescale -i <任务ID> --parallelism <并行度> --tm-cpu <CPU> --tm-mem-ratio 1:4 --tm-slots <slot数> --inspect

# 查询任务历史实例
volc_flink jobs instances -i <任务ID>

# 查询任务运行事件
volc_flink jobs events -i <任务ID>

# 获取任务日志
volc_flink jobs logs -i <任务ID>

# 查询任务指标
volc_flink jobs metrics -i <任务ID>

# 输出任务运维与 FlinkUI 地址
volc_flink jobs ui -i <任务ID>

# 快照操作
volc_flink jobs savepoint -i <任务ID>

# 查询快照列表
volc_flink jobs savepoints -i <任务ID>
```

### 草稿管理
```bash
# 列举草稿
volc_flink drafts apps

# 获取草稿内容
volc_flink drafts content -i <草稿ID>

# 设置草稿参数
volc_flink drafts params set -i <草稿ID> --kv <key>=<value>

# 发布草稿
volc_flink drafts publish -i <草稿ID>
```

### 监控与日志
```bash
# 查询任务运行事件
volc_flink monitor events -i <任务ID>

# 查询任务日志
volc_flink monitor logs -i <任务ID>

# FlinkUI 查询
volc_flink monitor flinkui -i <任务ID>
```

---

## 注意事项

### 重要：扩容/缩容的特殊要求

⚠️ **扩容/缩容时必须遵守以下规则**：

1. **使用 jobs rescale 命令** - 这是推荐方式，自动处理配置更新、发布和重启
2. **先使用 --dry-run 预览** - 确认配置变更是否正确
3. **展示配置对比** - 必须向用户展示当前配置 vs 新配置的对比
4. **使用 --inspect 监控** - 自动监控任务状态直到 RUNNING

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **先验证参数**：在执行任何操作前，必须验证输入参数的合法性
3. **展示配置对比**：在扩容/缩容前，必须展示当前配置 vs 新配置的对比
4. **始终先确认风险**：在执行任何变更操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **先获取应用信息**：在执行操作前，先获取应用的详细信息
6. **使用 --inspect 监控**：操作完成后，持续监控任务状态
7. **提供清晰的反馈**：向用户提供清晰的操作结果和后续建议
8. **使用友好的语言**：用用户能理解的语言解释操作和风险
9. **避免过度技术化**：除非用户要求，否则避免过度技术化的解释
10. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案

---

## 常用配置参数

以下是一些常用的 Flink 配置参数，可以通过修改配置来调整：

- `parallelism.default` - 默认并行度
- `taskmanager.memory.process.size` - TaskManager 内存大小
- `jobmanager.memory.process.size` - JobManager 内存大小
- `taskmanager.numberOfTaskSlots` - TaskManager slot 数量
- `execution.checkpointing.interval` - Checkpoint 间隔
- `execution.checkpointing.timeout` - Checkpoint 超时时间
- `restart-strategy` - 重启策略
- `state.backend.type` - 状态后端类型

---

## 工具调用顺序（优化版）

### 启动任务
1. **检测登录状态** - 确认已登录
2. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
3. **获取任务信息** - `volc_flink jobs detail -i <任务ID>`
4. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **启动任务** - `volc_flink jobs start -i <任务ID>`
6. **监控状态** - 可选：使用 --inspect 监控任务状态
7. **验证结果** - `volc_flink jobs detail -i <任务ID>`

### 停止任务
1. **检测登录状态** - 确认已登录
2. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
3. **获取任务信息** - `volc_flink jobs detail -i <任务ID>`
4. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **停止任务** - `volc_flink jobs stop -i <任务ID>`
6. **验证结果** - `volc_flink jobs detail -i <任务ID>`

### 重启任务
1. **检测登录状态** - 确认已登录
2. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
3. **获取任务信息** - `volc_flink jobs detail -i <任务ID>`
4. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **重启任务并监控** - `volc_flink jobs restart -i <任务ID> --inspect`
6. **验证结果** - `volc_flink jobs detail -i <任务ID>`

### 扩容/缩容任务（✅ 优先使用 rescale）
1. **检测登录状态** - 确认已登录
2. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
3. **获取当前配置** - `volc_flink jobs detail -i <任务ID>`
4. **参数验证** - 验证并行度、TM 规格、TM slot 等参数
5. **Dry-run 预览** - `volc_flink jobs rescale ... --dry-run`
6. **展示配置对比** - 以表格形式展示当前配置 vs 新配置
7. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
8. **执行 rescale 并监控** - `volc_flink jobs rescale ... --inspect`
9. **验证结果** - `volc_flink jobs detail -i <任务ID>`

### 修改配置
1. **检测登录状态** - 确认已登录
2. **智能选择任务** - 如果用户没有提供，列出项目和任务供选择
3. **参数验证** - 验证要修改的配置参数
4. **获取草稿内容** - `volc_flink drafts content -i <草稿ID>`
5. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
6. **更新草稿参数** - `volc_flink drafts params set -i <草稿ID> --kv <key>=<value>`
7. **发布草稿** - `volc_flink drafts publish -i <草稿ID>`
8. **重启任务并监控** - `volc_flink jobs restart -i <任务ID> --inspect`
9. **验证结果** - `volc_flink jobs detail -i <任务ID>`

---

## 🎯 优化总结

### 已实现的高优先级优化
1. ✅ **配置展示优化** - 当前配置 vs 新配置对比表格
2. ✅ **参数验证优化** - 并行度、TM 规格、TM slot 合法性验证
3. ✅ **错误处理优化** - 友好的错误提示和解决方案

### 已实现的中优先级优化
4. ✅ **项目和任务选择优化** - 智能选择、模糊搜索、交互式选择
5. ✅ **登录状态管理优化** - 操作前检测登录状态
6. ✅ **状态监控优化** - 使用 --inspect 自动监控任务状态

这些优化让 flink-sre 技能更加用户友好、更加健壮、更加高效！
