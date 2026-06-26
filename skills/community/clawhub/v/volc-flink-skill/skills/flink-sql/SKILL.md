---
name: flink-sql
description: Flink SQL 任务开发和部署工具，用于创建、开发、部署和调试 Flink SQL 任务。Use this skill when the user wants to create, update, publish, start, or debug a concrete Flink SQL draft/job, or generate SQL for a clearly defined task. Always trigger only when the request contains a SQL-task intent + a concrete draft/job object/action.
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

# Flink SQL 开发和部署技能

基于 `volc_flink` 命令行工具，自动化创建、开发、部署和调试 Flink SQL 任务。

---

## 🎯 优化后的核心流程

### 0. 通用约定（必读）

本技能的基础约定与变更约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_MUTATION.md`

执行任何会改变草稿/任务状态的动作前，必须先完成 `COMMON.md` 的 Scope & Identity，并遵循 `COMMON_MUTATION.md` 中的 Risk Confirmation、变更前检查和操作后验证规则。

### 0.1 模板与参考（推荐入口）

Flink SQL 的连接器模板与最佳实践示例统一放在本技能的 `assets/` 下（从 `flink-template` 迁入），文档链接统一放在 `references/` 下：

- 模板：
  - `assets/kafka.md`
  - `assets/paimon.md`
  - `assets/tls.md`
  - `assets/tos.md`
  - `assets/bytehouse-cdw.md`
  - `assets/bytehouse-ce.md`
- 参考：
  - `references/kafka.md`
  - `references/paimon.md`
  - `references/tls.md`
  - `references/tos.md`
  - `references/bytehouse-cdw.md`
  - `references/bytehouse-ce.md`
  - `references/connectors.md`
  - `references/volc_flink_commands.md`

说明：`references/connectors.md` 汇总外部官方文档链接。

### 1. 信息提取与版本归一化（关键）

从用户提问中提取并**显式确认**以下信息（缺一不可时必须先问清楚）：

- `project_name`：Flink 项目名（缺失时先 `volc_flink projects list` 让用户选）
- `draft_name` / `job_name`：草稿/任务名称（用于后续创建或定位）
- `job_type`：通常为 `FLINK_STREAMING_SQL` 或 `FLINK_BATCH_SQL`
- `flink_version`：用户口径的 Flink 版本（如 `1.16/1.17/1.20`）
- `engine_version`：用于 `drafts create` 的 `--engine-version`（必须由 `flink_version` 归一化得到）

#### 1.1 Flink 版本 -> engine-version 映射规则

可接受的用户输入形式：

- `Flink 1.16` / `1.16`
- `Flink 1.17` / `1.17`
- `Flink 1.20` / `1.20`
- 或直接给 `FLINK_VERSION_1_16 / FLINK_VERSION_1_17 / FLINK_VERSION_1_20`

映射规则：

- Flink 1.16 -> `--engine-version FLINK_VERSION_1_16`
- Flink 1.17 -> `--engine-version FLINK_VERSION_1_17`
- Flink 1.20 -> `--engine-version FLINK_VERSION_1_20`

如果用户给了不在上述列表中的版本（如 1.18/1.19）：

1. 先澄清用户要用的目标版本
2. 让用户在受支持的版本（1.16/1.17/1.20）中选择一个
3. 不要擅自猜测或“就近替换”

如果用户未指定版本：

- 先问用户希望使用哪个版本（1.16/1.17/1.20）
- 只有在用户明确说“默认即可/你定”时，才可选择默认版本（建议默认 `FLINK_VERSION_1_17`），并在输出中标明“版本来源：默认”

---

### 2. SQL 代码生成
根据用户的逻辑描述，生成 Flink SQL 代码。

**生成 SQL 时需要考虑**：
- 数据源的连接配置（Kafka、Paimon、MySQL 等）
- 数据表的 schema 定义
- 业务逻辑的实现
- 水位线（Watermark）设置
- 窗口函数（如需要）
- 输出目标的配置

**向用户展示生成的 SQL 代码，并询问是否需要调整和优化。**

---

### 3. SQL 逻辑确认
在用户确认 SQL 逻辑后，再继续后续步骤。

**在执行任何变更操作前，必须向用户确认！**

---

### 4. 创建和部署流程

#### 步骤 1：创建草稿
使用 `volc_flink drafts create` 创建草稿。

**命令格式**：
```bash
volc_flink drafts create \
  -n <草稿名称> \
  --directory <目录名称> \
  --job-type FLINK_STREAMING_SQL \
  --engine-version <engine_version> \
  --sql "<SQL 代码>"
```

**参数说明**：
- `-n, --name`：草稿名称（必填）
- `--directory`：草稿目录名称或路径（可选）
- `--job-type`：作业类型
  - `FLINK_STREAMING_SQL` - 流处理 SQL
  - `FLINK_STREAMING_JAR` - 流处理 JAR
  - `FLINK_BATCH_SQL` - 批处理 SQL
  - `FLINK_BATCH_JAR` - 批处理 JAR
- `--engine-version`：Flink 引擎版本
  - `FLINK_VERSION_1_16` 代表 Flink 1.16 版本
  - `FLINK_VERSION_1_17` 代表 Flink 1.17 版本
  - `FLINK_VERSION_1_20` 代表 Flink 1.20 版本
- `--sql`：SQL 文本
- `--sql-file`：SQL 文件路径
- `--sql-dir`：SQL 文件目录（递归读取 *.sql）

#### 步骤 2：获取草稿内容
使用 `volc_flink drafts content` 获取草稿内容，检查 SQL 代码。

**命令格式**：
```bash
volc_flink drafts content -i <草稿ID>
```

#### 步骤 3：更新草稿内容（如需要）
如果需要修改 SQL 代码，使用 `volc_flink drafts update` 更新草稿内容。

**命令格式**：
```bash
volc_flink drafts update -i <草稿ID> --sql "<新的 SQL 代码>"
```

**参数说明**：
- `--sql`：新的 SQL 文本
- `--sql-file`：新的 SQL 文件路径
- `--sql-dir`：新的 SQL 文件目录

#### 步骤 4：设置草稿参数（可选）
如果需要设置动态参数（如并行度、TM 规格等），使用 `volc_flink drafts params set`。

**命令格式**：
```bash
volc_flink drafts params set -i <草稿ID> --kv parallelism.default=2
volc_flink drafts params set -i <草稿ID> --kv kubernetes.taskmanager.cpu=2
volc_flink drafts params set -i <草稿ID> --kv taskmanager.memory.process.size=8192mb
volc_flink drafts params set -i <草稿ID> --kv taskmanager.numberOfTaskSlots=2
```

#### 步骤 5：发布草稿
使用 `volc_flink drafts publish` 发布草稿，创建任务。

**命令格式**：
```bash
volc_flink drafts publish -i <草稿ID> --resource-pool <资源池名称>
```

**参数说明**：
- `--resource-pool`：资源池名称（可选，使用默认资源池）
- `--priority`：优先级 1-5，默认 3
- `--schedule-policy`：调度策略（GANG 或 DRF）

#### 步骤 6：启动任务
使用 `volc_flink jobs start` 启动任务。

**重要**：开发期间从全新启动，不要从 savepoint 恢复。

**命令格式**：
```bash
volc_flink jobs start -i <任务ID>
```

---

### 5. 调试流程

#### 步骤 1：检查任务状态
使用 `volc_flink jobs detail` 检查任务状态。

**命令格式**：
```bash
volc_flink jobs detail -i <任务ID>
```

#### 步骤 2：获取任务日志
使用 `volc_flink monitor logs` 获取任务日志。

**日志查询策略**：
- 如果用户提供了故障时间，使用该时间范围
- 如果没有提供，查询最近 1 小时的日志
- 查询 ERROR 级别日志，同时查看 WARNING 级别

**命令格式**：
```bash
volc_flink monitor logs -i <任务ID>
```

#### 步骤 3：获取任务运行事件
使用 `volc_flink jobs events` 查询任务运行事件。

**命令格式**：
```bash
volc_flink jobs events -i <任务ID>
```

#### 步骤 4：分析错误
如果发现异常报错：

1. **停止任务**（仅停止当前正在调试的任务！）
   ```bash
   volc_flink jobs stop -i <任务ID>
   ```
   ⚠️ **重要**：只能停止用户明确要求调试的任务，绝对不能停止其他任务！

2. **根据报错信息更新草稿**
   ```bash
   volc_flink drafts update -i <草稿ID> --sql "<修复后的 SQL 代码>"
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

#### 步骤 5：重复调试循环
重复上述步骤，直到任务启动后没有报错。

---

### 6. 验证正常运行
当任务启动后没有报错，才算正常运行。

向用户提供以下信息：
- 任务状态
- 任务配置信息
- 运行时信息
- Flink UI 地址
- 后续使用建议

---

## 安全与变更门禁

通用安全规则与变更门禁（禁止误停/误改/误发布、必须二次确认、操作后验证最小集合）请统一遵循 `../../COMMON.md`。

---

## 输出格式

### SQL 代码生成反馈

```
# 📝 Flink SQL 代码生成

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **业务逻辑**: [业务逻辑描述]
- **作业类型**: [FLINK_STREAMING_SQL / FLINK_BATCH_SQL]
- **Flink 版本**: [engine_version]
- **版本来源**: [用户指定/默认/澄清选择]

## 💻 生成的 SQL 代码
```sql
[生成的 SQL 代码]
```

## ❓ 确认问题
1. SQL 逻辑是否正确？
2. 是否需要调整或优化？
3. 确认后继续创建草稿？(yes/no)
```

### 操作风险确认

统一使用 `../../COMMON.md` 的 Risk Confirmation 模板。

### 调试流程反馈

```
# 🔍 Flink SQL 任务调试

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

### 成功完成反馈

```
# ✅ Flink SQL 任务开发完成

## 📋 任务信息
- **项目名**: [项目名]
- **任务名**: [任务名]
- **当前状态**: [当前状态]
- **完成时间**: [时间]

## 📊 任务配置
- **草稿 ID**: [草稿 ID]
- **任务 ID**: [任务 ID]
- **作业类型**: [作业类型]
- **Flink 版本**: [Flink 版本]
- **其他关键配置**: [其他信息]

## 🌐 访问地址
- **运维页面**: [运维页面 URL]
- **Flink UI**: [Flink UI URL]

## 💡 后续建议
[后续使用建议]
```

---

## 工具调用顺序（优化版）

### 创建 SQL 任务开发完整流程

1. **检测登录状态** - 确认已登录
2. **信息提取** - 从用户提问中提取信息（必须包含 Flink 版本并归一化出 `engine_version`）
3. **智能选择项目和目录** - 如果用户没有提供，列出项目和目录供选择
4. **SQL 代码生成** - 根据逻辑描述生成 SQL
5. **用户确认 SQL** - 向用户展示 SQL，等待确认
6. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板确认变更风险
7. **创建草稿** - `volc_flink drafts create`（命令必须显式带 `--engine-version <engine_version>`）
8. **获取草稿内容** - `volc_flink drafts content` 验证 SQL
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

### 调试循环（发现错误时）

1. **获取日志** - `volc_flink monitor logs`
2. **获取事件** - `volc_flink jobs events`
3. **分析错误**
4. **停止任务** - `volc_flink jobs stop`（⚠️ 仅停止当前调试的任务！）
5. **更新草稿** - `volc_flink drafts update`
6. **重新发布草稿** - `volc_flink drafts publish`
7. **重新启动任务** - `volc_flink jobs start`
8. **检查日志** - 确认是否还有错误
9. **重复** - 直到没有错误

---

## 注意事项

### 重要：草稿和任务的关系

⚠️ **草稿和任务的对应关系**：
- 一个草稿可以发布多次，每次发布创建一个新任务
- 草稿 ID 可以从 `drafts apps` 或任务详情中获取
- 任务 ID 可以从 `jobs list` 或发布返回结果中获取

### 重要：调试时的安全规则

⚠️ **调试时必须遵守以下规则**：

1. **只能停止当前调试的任务** - 绝对不能停止其他任务
2. **明确确认任务范围** - 在停止任务前，明确确认是当前正在调试的任务
3. **如果有疑问，先询问用户** - 不要擅自停止任何任务

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **先确认任务范围**：在执行任何操作前，明确确认是哪个草稿/任务
3. **绝不影响其他草稿/任务**：绝对不能停止、修改、发布不相关的草稿/任务
4. **风险确认**：在执行任何变更操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **先获取信息**：在执行操作前，先获取草稿/任务的详细信息
6. **验证操作结果**：操作执行完成后，必须验证结果
7. **提供清晰反馈**：向用户提供清晰的操作结果和后续建议
8. **使用友好语言**：用用户能理解的语言解释操作和风险
9. **避免过度技术化**：除非用户要求，否则避免过度技术化的解释
10. **错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案
11. **调试循环**：调试时，要有耐心，重复直到成功

---

## 错误处理

通用错误处理（未登录/未找到/超时网络）请遵循 `../../COMMON.md`。SQL 语法类问题建议优先使用 `flink-validate` 进行预校验。

---

## 🎯 技能总结

### 已集成的优化（从 flink-sre 借鉴）
1. ✅ **登录状态检测** - 操作前检测登录状态
2. ✅ **智能项目和目录选择** - 交互式选择、模糊搜索
3. ✅ **错误处理优化** - 友好的错误提示和解决方案

### 核心功能
1. ✅ **SQL 代码生成** - 根据业务逻辑生成 Flink SQL
2. ✅ **草稿管理** - 创建、获取、更新、发布草稿
3. ✅ **任务管理** - 启动、停止、重启任务
4. ✅ **调试流程** - 日志查看、错误分析、修复循环
5. ✅ **参数配置** - 设置并行度、TM 规格等动态参数

这个技能可以完整地覆盖 Flink SQL 任务从开发到部署到调试的全流程！
