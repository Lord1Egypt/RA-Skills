---
name: flink-jar
description: Flink JAR 任务管理技能，用于创建、部署、配置和调试 JAR 类型的 Flink 任务。Use this skill when the user wants to create, publish, start, configure, or debug a concrete JAR-based Flink draft/job, including jar path, main class, and runtime parameters. Always trigger only when the request contains a JAR-task intent + a concrete draft/job object/action.
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

# Flink JAR 任务管理技能

用于创建、部署、配置和调试 JAR 类型的 Flink 任务。

---

## 通用约定（必读）

本技能的基础约定与变更约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_MUTATION.md`

本技能涉及草稿创建、JAR 发布、任务启动和调试，必须遵循 `COMMON_MUTATION.md` 中的 Risk Confirmation、变更前检查和操作后验证规则。

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

### 0.5 前置条件检查

#### TOS Jar 路径配置
在上传 JAR 包前，检查是否已配置 TOS Jar 存储路径：

**检查步骤**：
1. 查看当前配置：`volc_flink config show`
2. 如果未配置 TOS Jar 路径，提示用户配置
3. 引导使用 `flink-config` 技能进行配置

**配置命令**：
```bash
volc_flink config set-tos-jar-prefix tos://<bucket-name>/<path>/
```

---

### 1. 信息提取与智能选择

#### 1.1 信息提取
从用户提问中提取关键信息：
- **项目名** (project_name)
- **任务名** (job_name)
- **JAR 包路径**（本地文件路径）
- **主类名** (Main Class)
- **程序参数**（传递给主类的参数）
- **作业类型**：FLINK_STREAMING_JAR 或 FLINK_BATCH_JAR
- **Flink 引擎版本**：FLINK_VERSION_1_16、FLINK_VERSION_1_17、FLINK_VERSION_1_20

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
3. 询问任务名、JAR 包信息等

---

### 2. JAR 包上传与管理

#### 2.1 JAR 包准备
在上传前，确认 JAR 包的信息：

**需要确认的信息**：
1. **JAR 包路径** - 本地文件路径
2. **主类名** - Main Class 全限定名
3. **程序参数** - 传递给主类的参数（可选）
4. **依赖 JAR 包** - 是否需要其他依赖包（可选）

#### 2.2 使用 flink-dependency 管理依赖
如果 JAR 任务有依赖的 JAR 包，先使用 `flink-dependency` 技能管理依赖：

1. 上传依赖 JAR 包
2. 将依赖添加到 Dependency.jars

#### 2.3 创建 JAR 任务草稿
使用 `volc_flink drafts create` 创建 JAR 任务草稿。

**命令格式**：
```bash
volc_flink drafts create \
  -n <草稿名称> \
  --directory <目录名称> \
  --job-type FLINK_STREAMING_JAR \
  --engine-version FLINK_VERSION_1_17 \
  --jar-path <JAR 包本地路径> \
  --main-class <主类名> \
  --args "<程序参数>"
```

**参数说明**：
- `-n, --name`：草稿名称（必填）
- `--directory`：草稿目录名称或路径（可选）
- `--job-type`：作业类型
  - `FLINK_STREAMING_JAR` - 流处理 JAR
  - `FLINK_BATCH_JAR` - 批处理 JAR
- `--engine-version`：Flink 引擎版本
  - `FLINK_VERSION_1_16`
  - `FLINK_VERSION_1_17`
  - `FLINK_VERSION_1_20`
- `--jar-path`：JAR 包本地路径（必填）
- `--main-class`：主类名（必填）
- `--args`：程序参数（可选）

---

### 3. JAR 任务配置

#### 3.1 获取草稿内容
使用 `volc_flink drafts content` 获取草稿内容，检查配置。

**命令格式**：
```bash
volc_flink drafts content -i <草稿ID>
```

#### 3.2 更新草稿内容（如需要）
如果需要修改 JAR 包或配置，使用 `volc_flink drafts update` 更新草稿内容。

**命令格式**：
```bash
# 更新 JAR 包
volc_flink drafts update -i <草稿ID> --jar-path <新的 JAR 包路径>

# 更新主类名
volc_flink drafts update -i <草稿ID> --main-class <新的主类名>

# 更新程序参数
volc_flink drafts update -i <草稿ID> --args "<新的程序参数>"
```

#### 3.3 设置草稿参数（可选）
如果需要设置动态参数（如并行度、TM 规格等），使用 `volc_flink drafts params set`。

**命令格式**：
```bash
volc_flink drafts params set -i <草稿ID> --kv parallelism.default=2
volc_flink drafts params set -i <草稿ID> --kv kubernetes.taskmanager.cpu=2
volc_flink drafts params set -i <草稿ID> --kv taskmanager.memory.process.size=8192mb
volc_flink drafts params set -i <草稿ID> --kv taskmanager.numberOfTaskSlots=2
```

---

### 4. JAR 任务发布与启动

#### 4.1 发布草稿
使用 `volc_flink drafts publish` 发布草稿，创建任务。

**命令格式**：
```bash
volc_flink drafts publish -i <草稿ID> --resource-pool <资源池名称>
```

**参数说明**：
- `--resource-pool`：资源池名称（可选，使用默认资源池）
- `--priority`：优先级 1-5，默认 3
- `--schedule-policy`：调度策略（GANG 或 DRF）

#### 4.2 启动任务
使用 `volc_flink jobs start` 启动任务。

**重要**：开发期间从全新启动，不要从 savepoint 恢复。

**命令格式**：
```bash
volc_flink jobs start -i <任务ID>
```

---

### 5. JAR 任务调试

#### 5.1 检查任务状态
使用 `volc_flink jobs detail` 检查任务状态。

**命令格式**：
```bash
volc_flink jobs detail -i <任务ID>
```

#### 5.2 获取任务日志
使用 `volc_flink monitor logs` 获取任务日志。

**日志查询策略**：
- 如果用户提供了故障时间，使用该时间范围
- 如果没有提供，查询最近 1 小时的日志
- 查询 ERROR 级别日志，同时查看 WARNING 级别

**命令格式**：
```bash
volc_flink monitor logs -i <任务ID>
```

#### 5.3 获取任务运行事件
使用 `volc_flink jobs events` 查询任务运行事件。

**命令格式**：
```bash
volc_flink jobs events -i <任务ID>
```

#### 5.4 分析错误
如果发现异常报错：

1. **停止任务**（仅停止当前正在调试的任务！）
   ```bash
   volc_flink jobs stop -i <任务ID>
   ```
   ⚠️ **重要**：只能停止用户明确要求调试的任务，绝对不能停止其他任务！

2. **根据报错信息更新草稿**
   ```bash
   volc_flink drafts update -i <草稿ID> --jar-path <修复后的 JAR 包>
   ```

3. **重新发布草稿**
   ```bash
   volc_flink drafts publish -i <草稿ID>
   ```

4. **重新启动任务**
   ```bash
   volc_flink jobs start -i <任务ID>
   ```

5. **重新检查日志，确认是否还有错误**

#### 5.5 重复调试循环
重复上述步骤，直到任务启动后没有报错。

---

## 工具调用顺序（优化版）

### JAR 任务完整开发流程

1. **检测登录状态** - 确认已登录
2. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
3. **信息提取** - 从用户提问中提取信息
4. **智能选择项目和目录** - 如果用户没有提供，列出项目和目录供选择
5. **JAR 包准备** - 确认 JAR 包路径、主类名、程序参数
6. **管理依赖**（可选）- 使用 flink-dependency 管理依赖 JAR
7. **创建草稿** - `volc_flink drafts create`
8. **获取草稿内容** - `volc_flink drafts content` 验证配置
9. **设置草稿参数**（可选）- `volc_flink drafts params set`
10. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
11. **发布草稿** - `volc_flink drafts publish`
12. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
13. **启动任务** - `volc_flink jobs start`
14. **检查任务状态** - `volc_flink jobs detail`
15. **获取日志** - `volc_flink monitor logs`
16. **分析错误** - 如果有错误，停止任务 → 更新草稿 → 重新发布 → 重新启动
17. **重复调试循环** - 直到没有错误
18. **验证正常运行** - 提供最终结果

---

## 常用命令速查

### JAR 草稿管理
```bash
# 创建 JAR 任务草稿（流处理）
volc_flink drafts create \
  -n <草稿名称> \
  --directory <目录名称> \
  --job-type FLINK_STREAMING_JAR \
  --engine-version FLINK_VERSION_1_17 \
  --jar-path <JAR 包路径> \
  --main-class <主类名> \
  --args "<程序参数>"

# 创建 JAR 任务草稿（批处理）
volc_flink drafts create \
  -n <草稿名称> \
  --job-type FLINK_BATCH_JAR \
  --engine-version FLINK_VERSION_1_17 \
  --jar-path <JAR 包路径> \
  --main-class <主类名>

# 获取草稿内容
volc_flink drafts content -i <草稿ID>

# 更新草稿（JAR 包）
volc_flink drafts update -i <草稿ID> --jar-path <新 JAR 包路径>

# 更新草稿（主类名）
volc_flink drafts update -i <草稿ID> --main-class <新主类名>

# 更新草稿（程序参数）
volc_flink drafts update -i <草稿ID> --args "<新参数>"

# 设置草稿参数
volc_flink drafts params set -i <草稿ID> --kv <key>=<value>

# 发布草稿
volc_flink drafts publish -i <草稿ID> --resource-pool <资源池名称>
```

### 任务管理
```bash
# 启动任务
volc_flink jobs start -i <任务ID>

# 停止任务
volc_flink jobs stop -i <任务ID>

# 获取任务详情
volc_flink jobs detail -i <任务ID>

# 获取任务日志
volc_flink monitor logs -i <任务ID>

# 获取任务事件
volc_flink jobs events -i <任务ID>
```

---

## 输出格式

### JAR 任务创建反馈
```
# 📦 Flink JAR 任务创建

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **JAR 包**: [JAR 包路径]
- **主类名**: [主类名]
- **程序参数**: [程序参数]
- **作业类型**: [FLINK_STREAMING_JAR / FLINK_BATCH_JAR]
- **Flink 版本**: [FLINK_VERSION_1_17]

## ✅ 创建结果
- **草稿 ID**: [草稿 ID]
- **状态**: 创建成功

## ❓ 确认问题
1. JAR 包配置是否正确？
2. 是否需要调整或优化？
3. 确认后继续发布？(yes/no)（发布前需先完成 `../../COMMON.md` 的风险确认）
```

### 调试流程反馈
```
# 🔍 Flink JAR 任务调试

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **当前状态**: [当前状态]

## 🐛 错误信息
[发现的错误信息]

## 🔧 修复方案
[修复方案描述]

## ❓ 确认问题
是否按照此方案修复？(yes/no)
```

---

## 注意事项

### 重要：TOS Jar 路径配置

⚠️ **在上传 JAR 包前，必须先配置 TOS Jar 存储路径！**

- 使用 `flink-config` 技能配置
- 命令：`volc_flink config set-tos-jar-prefix tos://<bucket-name>/<path>/`
- 确保 Bucket 存在且有读写权限

### 重要：调试时的安全规则

⚠️ **调试时必须遵守以下规则**：

1. **只能停止当前调试的任务** - 绝对不能停止其他任务
2. **明确确认任务范围** - 在停止任务前，明确确认是当前正在调试的任务
3. **如果有疑问，先询问用户** - 不要擅自停止任何任务

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **检查 TOS 配置**：在上传 JAR 包前，检查是否已配置 TOS Jar 路径
3. **先确认任务范围**：在执行任何操作前，明确确认是哪个草稿/任务
4. **绝不影响其他草稿/任务**：绝对不能停止、修改、发布不相关的草稿/任务
5. **风险确认**：在执行任何变更操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
6. **先获取信息**：在执行操作前，先获取草稿/任务的详细信息
7. **验证操作结果**：操作执行完成后，必须验证结果
8. **提供清晰的反馈**：向用户提供清晰的操作结果和后续建议

---

## 🎯 技能总结

### 核心功能
1. ✅ **JAR 包管理** - JAR 包上传、更新
2. ✅ **JAR 任务创建** - 创建 JAR 类型的草稿
3. ✅ **任务配置** - 主类名、程序参数、动态参数配置
4. ✅ **任务发布** - 发布草稿创建任务
5. ✅ **任务启动** - 启动 JAR 任务
6. ✅ **调试流程** - 日志查看、错误分析、修复循环

### 与其他技能的关系
- **依赖 flink-volc** - 需要先登录才能创建 JAR 任务
- **配合 flink-config** - 需要配置 TOS Jar 路径
- **配合 flink-dependency** - 可以管理依赖 JAR 包
- **配合 flink-sre** - 可以进行运维操作
- **配合 flink-monitor** - 可以监控任务运行
- **配合 flink-diagnostic** - 可以诊断故障

这个技能可以完整地覆盖 Flink JAR 任务从创建到部署到调试的全流程！
