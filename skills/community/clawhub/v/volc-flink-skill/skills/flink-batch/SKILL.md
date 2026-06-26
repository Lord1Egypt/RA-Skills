---
name: flink-batch
description: Flink 批处理任务管理技能，用于创建、调度、监控和管理批处理类型的 Flink 任务。Use this skill when the user wants to create, schedule, start, rerun, or inspect a concrete batch SQL/JAR draft or job. Always trigger only when the request contains a batch-task intent + a concrete draft/job object/action.
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

# Flink 批处理任务管理技能

用于创建、调度、监控和管理批处理类型的 Flink 任务。

---

## 通用约定（必读）

本技能的基础约定与变更约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_MUTATION.md`

本技能涉及草稿创建、发布、启动和批处理作业管理，必须遵循 `COMMON_MUTATION.md` 中的 Risk Confirmation、变更前检查和操作后验证规则。

---

## 🎯 核心功能

### 0. 登录状态检测（从 flink-volc 借鉴）
**在执行任何操作前，先检测登录状态！**

**检测步骤**：
1. 尝试执行一个简单的命令（如 `volc_flink config show`）
2. 如果提示"请先登录"，则提示用户需要登录
3. 引导用户使用 `flink-volc` 技能进行登录

**错误处理**：
- 如果检测到未登录，立即停止后续操作
- 友好提示用户需要先登录
- 引导使用 flink-volc 技能

---

### 1. 信息提取与智能选择

#### 1.1 信息提取
从用户提问中提取关键信息：
- **项目名** (project_name)
- **任务名** (job_name)
- **任务类型**：FLINK_BATCH_SQL 或 FLINK_BATCH_JAR
- **SQL 内容**（如果是 SQL 批处理）
- **JAR 包路径**（如果是 JAR 批处理）
- **主类名**（如果是 JAR 批处理）
- **程序参数**（可选）
- **Flink 引擎版本**：FLINK_VERSION_1_16、FLINK_VERSION_1_17、FLINK_VERSION_1_20
- **调度配置**：定时调度配置（可选）

如果用户没有明确提供，主动询问缺失的关键信息。

#### 1.2 智能项目和目录选择
**如果用户没有明确提供项目名或目录，按以下流程处理**：

**场景 A：用户只提供了任务名，没有提供项目名**
1. 列出所有项目：`volc_flink projects list`
2. 让用户选择项目
3. 列出该项目下的草稿目录：`volc_flink drafts dirs`
4. 让用户选择目录或使用默认目录

**场景 B：用户没有提供任何信息**
1. 先列出所有项目供用户选择
2. 用户选择项目后，列出该项目下的草稿目录供用户选择
3. 询问任务名、任务类型等信息

---

### 2. 批处理 SQL 任务

#### 2.1 SQL 代码生成或获取
根据用户的需求，生成或获取批处理 SQL 代码。

**批处理 SQL 特点**：
- 使用 `EXECUTION_MODE` = `BATCH`
- 通常有明确的开始和结束
- 处理有限数据集
- 处理完成后任务结束

**常用批处理 SQL 示例**：
```sql
-- 创建源表
CREATE TABLE source_table (
  id INT,
  name STRING,
  amount DECIMAL(10, 2)
) WITH (
  'connector' = 'paimon',
  'path' = 'tos://bucket/source-path',
  'scan.mode' = 'latest'
);

-- 创建目标表
CREATE TABLE sink_table (
  name STRING,
  total_amount DECIMAL(10, 2)
) WITH (
  'connector' = 'paimon',
  'path' = 'tos://bucket/sink-path',
  'auto-create' = 'true'
);

-- 批处理执行
INSERT INTO sink_table
SELECT name, SUM(amount) AS total_amount
FROM source_table
GROUP BY name;
```

#### 2.2 创建批处理 SQL 草稿
使用 `volc_flink drafts create` 创建批处理 SQL 草稿。

**命令格式**：
```bash
volc_flink drafts create \
  -n <草稿名称> \
  --directory <目录名称> \
  --job-type FLINK_BATCH_SQL \
  --engine-version FLINK_VERSION_1_17 \
  --sql "<SQL 代码>"
```

**参数说明**：
- `-n, --name`：草稿名称（必填）
- `--directory`：草稿目录名称或路径（可选）
- `--job-type`：作业类型
  - `FLINK_BATCH_SQL` - 批处理 SQL
  - `FLINK_BATCH_JAR` - 批处理 JAR
- `--engine-version`：Flink 引擎版本
  - `FLINK_VERSION_1_16`
  - `FLINK_VERSION_1_17`
  - `FLINK_VERSION_1_20`
- `--sql`：SQL 文本
- `--sql-file`：SQL 文件路径

---

### 3. 批处理 JAR 任务

#### 3.1 JAR 包准备
在创建批处理 JAR 任务前，确认 JAR 包的信息：

**需要确认的信息**：
1. **JAR 包路径** - 本地文件路径
2. **主类名** - Main Class 全限定名
3. **程序参数** - 传递给主类的参数（可选）
4. **依赖 JAR 包** - 是否需要其他依赖包（可选）

#### 3.2 前置条件检查
检查是否已配置 TOS Jar 存储路径：

**检查步骤**：
1. 查看当前配置：`volc_flink config show`
2. 如果未配置 TOS Jar 路径，提示用户配置
3. 引导使用 `flink-config` 技能进行配置

#### 3.3 创建批处理 JAR 草稿
使用 `volc_flink drafts create` 创建批处理 JAR 草稿。

**命令格式**：
```bash
volc_flink drafts create \
  -n <草稿名称> \
  --directory <目录名称> \
  --job-type FLINK_BATCH_JAR \
  --engine-version FLINK_VERSION_1_17 \
  --jar-path <JAR 包本地路径> \
  --main-class <主类名> \
  --args "<程序参数>"
```

---

### 4. 批处理任务配置

#### 4.1 获取草稿内容
使用 `volc_flink drafts content` 获取草稿内容，检查配置。

**命令格式**：
```bash
volc_flink drafts content -i <草稿ID>
```

#### 4.2 更新草稿内容（如需要）
如果需要修改 SQL 代码或 JAR 包，使用 `volc_flink drafts update` 更新草稿内容。

**命令格式**：
```bash
# 更新 SQL 代码
volc_flink drafts update -i <草稿ID> --sql "<新的 SQL 代码>"

# 更新 JAR 包
volc_flink drafts update -i <草稿ID> --jar-path <新的 JAR 包路径>
```

#### 4.3 设置草稿参数（可选）
如果需要设置动态参数，使用 `volc_flink drafts params set`。

**命令格式**：
```bash
volc_flink drafts params set -i <草稿ID> --kv parallelism.default=2
```

---

### 5. 批处理任务发布与执行

#### 5.1 发布草稿
使用 `volc_flink drafts publish` 发布草稿，创建任务。

**命令格式**：
```bash
volc_flink drafts publish -i <草稿ID> --resource-pool <资源池名称>
```

#### 5.2 启动任务
使用 `volc_flink jobs start` 启动批处理任务。

**命令格式**：
```bash
volc_flink jobs start -i <任务ID>
```

---

### 6. 批处理任务监控

#### 6.1 查看任务状态
使用 `volc_flink jobs detail` 查看批处理任务状态。

**命令格式**：
```bash
volc_flink jobs detail -i <任务ID>
```

**批处理任务状态**：
- `RUNNING` - 运行中
- `FINISHED` - 已完成（批处理特有）
- `FAILED` - 失败
- `CANCELED` - 已取消

#### 6.2 查询任务历史实例
使用 `volc_flink jobs instances` 查询批处理任务的历史执行记录。

**命令格式**：
```bash
volc_flink jobs instances -i <任务ID>
```

**历史实例信息**：
- 每次执行的开始时间
- 每次执行的结束时间
- 每次执行的状态
- 每次执行的持续时间

#### 6.3 获取任务日志
使用 `volc_flink monitor logs` 获取批处理任务日志。

**命令格式**：
```bash
volc_flink monitor logs -i <任务ID>
```

---

### 7. 批处理任务重新执行

#### 7.1 重新执行批处理任务
如果需要重新执行批处理任务：

1. **停止当前任务**（如果正在运行）
   ```bash
   volc_flink jobs stop -i <任务ID>
   ```

2. **重新启动任务**
   ```bash
   volc_flink jobs start -i <任务ID>
   ```

或者创建新的草稿和任务。

---

## 工具调用顺序（优化版）

### 批处理 SQL 任务完整流程

1. **检测登录状态** - 确认已登录
2. **信息提取** - 从用户提问中提取信息
3. **智能选择项目和目录** - 如果用户没有提供，列出项目和目录供选择
4. **SQL 代码准备** - 生成或获取批处理 SQL 代码
5. **用户确认 SQL** - 向用户展示 SQL，等待确认
6. **创建草稿** - `volc_flink drafts create`
7. **获取草稿内容** - `volc_flink drafts content` 验证配置
8. **设置草稿参数**（可选）- `volc_flink drafts params set`
9. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
10. **发布草稿** - `volc_flink drafts publish`
11. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
12. **启动任务** - `volc_flink jobs start`
13. **监控任务执行** - `volc_flink jobs detail`
14. **查看执行结果** - 等待任务完成，查看结果

---

## 常用命令速查

### 批处理草稿管理
```bash
# 创建批处理 SQL 草稿
volc_flink drafts create \
  -n <草稿名称> \
  --job-type FLINK_BATCH_SQL \
  --engine-version FLINK_VERSION_1_17 \
  --sql "<SQL 代码>"

# 创建批处理 JAR 草稿
volc_flink drafts create \
  -n <草稿名称> \
  --job-type FLINK_BATCH_JAR \
  --engine-version FLINK_VERSION_1_17 \
  --jar-path <JAR 包路径> \
  --main-class <主类名>

# 获取草稿内容
volc_flink drafts content -i <草稿ID>

# 更新草稿
volc_flink drafts update -i <草稿ID> --sql "<新 SQL 代码>"

# 发布草稿
volc_flink drafts publish -i <草稿ID>
```

### 批处理任务管理
```bash
# 启动批处理任务
volc_flink jobs start -i <任务ID>

# 停止批处理任务
volc_flink jobs stop -i <任务ID>

# 获取任务详情
volc_flink jobs detail -i <任务ID>

# 查询历史实例
volc_flink jobs instances -i <任务ID>

# 获取任务日志
volc_flink monitor logs -i <任务ID>
```

---

## 输出格式

### 批处理任务创建反馈
```
# 📦 Flink 批处理任务创建

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **任务类型**: [FLINK_BATCH_SQL / FLINK_BATCH_JAR]
- **Flink 版本**: [FLINK_VERSION_1_17]

## 💻 SQL 代码 / JAR 信息
[SQL 代码或 JAR 包信息]

## ❓ 确认问题
1. 配置是否正确？
2. 是否需要调整？
3. 确认后继续发布？(yes/no)
```

### 批处理任务执行结果反馈
```
# ✅ Flink 批处理任务执行完成

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **任务 ID**: [任务ID]
- **最终状态**: [FINISHED / FAILED / CANCELED]
- **开始时间**: [时间]
- **结束时间**: [时间]
- **执行时长**: [时长]

## 📊 执行结果
- **处理记录数**: [数量]
- **输出记录数**: [数量]
- **其他指标**: [指标]

## 💡 后续建议
[后续操作建议]
```

---

## 批处理 vs 流处理对比

| 特性 | 批处理 (Batch) | 流处理 (Streaming) |
|------|----------------|-------------------|
| **数据特点** | 有限数据集 | 无限数据流 |
| **执行模式** | 一次性执行 | 持续运行 |
| **任务结束** | 处理完成后结束 | 持续运行直到手动停止 |
| **状态** | FINISHED（完成） | RUNNING（运行中） |
| **典型场景** | 数据导入、报表生成、数据清洗 | 实时计算、实时监控、实时报表 |

---

## 注意事项

### 重要：批处理任务特点

⚠️ **批处理任务与流处理的区别**：
- 批处理任务处理有限数据集
- 批处理任务执行完成后会结束（FINISHED 状态）
- 流处理任务持续运行直到手动停止
- 根据业务需求选择合适的任务类型

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **明确任务类型**：确认是批处理还是流处理
3. **先确认任务范围**：在执行任何操作前，明确确认是哪个草稿/任务
4. **监控批处理执行**：批处理任务会执行完成，注意监控执行状态
5. **查看历史实例**：批处理任务可以查看历史执行记录
6. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案

---

## 🎯 技能总结

### 核心功能
1. ✅ **批处理 SQL 任务** - 创建、配置、发布 SQL 批处理任务
2. ✅ **批处理 JAR 任务** - 创建、配置、发布 JAR 批处理任务
3. ✅ **任务监控** - 查看批处理任务状态和执行结果
4. ✅ **历史实例** - 查询批处理任务的历史执行记录
5. ✅ **重新执行** - 重新执行批处理任务

### 与其他技能的关系
- **依赖 flink-volc** - 需要先登录才能创建批处理任务
- **配合 flink-sql** - 可以参考 SQL 开发的最佳实践
- **配合 flink-sre** - 可以进行运维操作
- **配合 flink-monitor** - 可以监控任务运行

这个技能可以完整地覆盖 Flink 批处理任务的管理！
