---
name: flink-cdc
description: Flink CDC 任务开发和部署工具，用于生成、创建、发布和调试 Flink CDC YAML 任务。Use this skill when the user wants to create/update/publish/debug a CDC draft/job, or asks for CDC pipeline YAML templates and parameter guidance for a concrete source/sink scenario.
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

# Flink CDC 开发和部署技能

基于 `volc_flink` 命令行工具，生成、创建、发布和调试 Flink CDC YAML 任务。

---

## 核心流程

### 0. 通用约定（必读）

本技能的基础约定与变更约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_MUTATION.md`

执行任何会改变草稿/任务状态的动作前，必须先完成 `COMMON.md` 的 Scope & Identity，并遵循 `COMMON_MUTATION.md` 中的 Risk Confirmation、变更前检查和操作后验证规则。

### 0.1 模板与参考（推荐入口）

CDC YAML 模板统一放在本技能的 `assets/` 下，参数说明与平台约束统一放在 `references/` 下：

- 模板：
  - `assets/kafka-print.yml`
  - `assets/kafka-paimon-las-route.yml`
  - `assets/mysql-paimon-filesystem.yml`
  - `assets/mysql-paimon-las.yml`
  - `assets/mysql-paimon-las-transform.yml`
  - `assets/mysql-starrocks.yml`
  - `assets/mysql-doris.yml`
  - `assets/mysql-kafka.yml`
  - `assets/mysql-bytehouse-cdw.yml`
- 参考：
  - `references/overview.md`
  - `references/mysql.md`
  - `references/paimon.md`
  - `references/starrocks.md`
  - `references/doris.md`
  - `references/kafka.md`
  - `references/bytehouse-cdw.md`
  - `references/route.md`
  - `references/transform.md`
  - `references/connectors.md`
  - `references/volc_flink_commands.md`

说明：模板用于快速生成 YAML；参数解释、限制、易错点统一查 `references/*.md`。

---

### 1. 信息提取与硬约束归一化

从用户提问中提取并显式确认以下信息：

- `project_name`：Flink 项目名
- `draft_name` / `job_name`：草稿或任务名称
- `directory` / `directory_id`：CDC 草稿目录
- `source_type`：如 `mysql` / `kafka`
- `sink_type`：如 `paimon` / `paimon-las` / `starrocks` / `doris` / `kafka` / `bytehouse-cdw`
- `engine_version`
- `cdc_version`
- 是否需要 `transform` / `route`
- 是否要直接创建草稿，还是先只生成模板

#### 1.1 JobType / 版本约束

CDC 任务统一按以下口径处理：

- `job_type` 固定为 `FLINK_CDC_JAR`
- `--type cdc` 等价于 `--job-type FLINK_CDC_JAR`
- 当前 CDC 任务仅支持 `FLINK_VERSION_1_16`
- 如果用户未指定引擎版本，默认使用 `FLINK_VERSION_1_16`
- 如果用户指定了非 1.16 版本，必须明确拦截并提示修改
- `cdc_version` 默认使用 `v3.4`

#### 1.2 MySQL CDC 前置条件

如果 source 使用 `mysql`：

- 需提醒用户：MySQL CDC 仅支持在 Flink 1.16-volcano 及以上引擎版本中使用
- 需提醒用户：基于合规要求，MySQL CDC 需要用户自行上传 MySQL Driver
- 建议口径：上传 MySQL `8.0.27` 驱动到作业开发依赖文件中

#### 1.3 YAML 结构约束

当前 `volc-flink-cli` 的 CDC YAML 与内置 `build_cdc_job_info()` 解析逻辑，建议统一使用以下结构：

```yaml
sources:
- source:
    type: mysql
    ...
sink:
  type: paimon
  ...
transform:
- source-table: db.table
  projection: "*"
route:
- source-table: db.table
  sink-table: ods_db.table
pipeline:
  name: my-cdc-job
  parallelism: 2
```

注意：

- 推荐使用 `sources:`（而不是文档中常见的 `source:` 单对象写法），以与当前 CLI 示例和 `CdcJobInfo` 解析逻辑保持一致
- `sink:` 使用单对象
- `transform:` / `route:` 使用列表

---

### 2. CDC YAML 生成规则

生成 YAML 时必须遵循以下规则：

- 默认输出“可直接保存为 `.yml/.yaml` 文件”的完整 YAML
- 优先使用参数占位符，例如 `${mysql_hostname}`、`${pipeline_name}`
- 如果用户未明确要求写死敏感信息，不要把真实密码、AK、SK 写进 YAML
- 对 `tables` 使用正则时，提醒用户转义点号，例如 `app_db\\.orders_.*`
- 对 `server-id`，增量快照场景优先给区间值，例如 `5401-5404`
- 如需表级映射，优先给 `route` 示例
- 如需字段裁剪、过滤、重命名，优先给 `transform` 示例

优先模板选择：

- Kafka -> Print / values 调试：`assets/kafka-print.yml`
- MySQL -> Paimon Filesystem：`assets/mysql-paimon-filesystem.yml`
- MySQL -> Paimon LAS：`assets/mysql-paimon-las.yml`
- MySQL -> StarRocks：`assets/mysql-starrocks.yml`
- MySQL -> Doris：`assets/mysql-doris.yml`
- MySQL -> Kafka：`assets/mysql-kafka.yml`
- MySQL -> ByteHouse CDW：`assets/mysql-bytehouse-cdw.yml`

---

### 3. 生成后静态检查

在建议用户创建草稿前，先检查 YAML 至少满足：

- 存在 `sources`、`sink`、`pipeline`
- `sources[*].source.type` 与 `sink.type` 明确
- `pipeline.name` 与 `pipeline.parallelism` 明确
- MySQL source 至少包含：
  - `hostname`
  - `port`
  - `username`
  - `password`
  - `tables`
  - `server-id`
- 如果使用 `route`：
  - 每条 route 至少包含 `source-table`
  - 建议明确 `sink-table`
- 如果使用 `transform`：
  - 至少包含 `source-table`
  - 根据需求补 `projection` / `filter`

如果用户只是要模板：

- 只输出 YAML 与关键参数说明
- 不创建草稿
- 不发布任务

---

### 4. 创建 CDC 草稿

在用户确认 YAML 后，使用 `volc_flink drafts create` 创建 CDC 草稿。

#### 4.0 目录前置条件（常见报错点）

`--directory` 必须是平台上已存在的草稿目录路径或目录名，否则会报错：

- `❌ 错误: 未找到目录路径，请使用 drafts dirs 查看可用目录`

建议流程：

```bash
volc_flink drafts dirs
volc_flink drafts mkdir --name "/数据开发文件夹/CDC"
```

推荐命令格式：

```bash
volc_flink drafts create \
  --type cdc \
  --directory <directory> \
  -n <draft-name> \
  --engine-version FLINK_VERSION_1_16 \
  --cdc-version v3.4 \
  --cdc "<inline-yaml>"
```

也可以使用（按优先级）：

- `--cdc-file <yaml-file>`：最稳妥（不受 shell 转义/变量展开/命令长度限制影响）
- `--cdc "<inline-yaml>"`：适合直接复制粘贴；建议配合 heredoc（见下文）避免转义与 `${...}` 展开问题
- `--cdc-dir <yaml-dir>`：递归读取 `*.yaml` / `*.yml`

关键参数说明：

- `--type cdc`：兼容参数，内部映射到 `FLINK_CDC_JAR`
- `--cdc`：CDC YAML 文本
- `--cdc-file`：CDC YAML 文件路径（当 YAML 很长、可能触发 shell 命令长度限制时再使用）
- `--cdc-dir`：递归读取 `*.yaml` / `*.yml`
- `--engine-version`：CDC 当前仅支持 `FLINK_VERSION_1_16`
- `--cdc-version`：默认 `v3.4`

#### 4.1 推荐的“内联 YAML”写法（避免转义与变量展开）

当 YAML 较长或包含 `${...}` 占位符时，直接 `--cdc "...."` 容易出现转义问题，且 `${...}` 可能被 shell 当作环境变量替换。

推荐用 heredoc 生成 `--cdc` 参数（不落盘）：

```bash
volc_flink drafts create \
  --type cdc \
  --directory "/数据开发文件夹" \
  -n "mysql-paimon-demo" \
  --engine-version FLINK_VERSION_1_16 \
  --cdc-version v3.4 \
  --cdc "$(cat <<'YAML'
sources:
- source:
    type: mysql
    hostname: ${mysql_hostname}
    port: ${mysql_port}
    username: ${mysql_username}
    password: ${mysql_password}
    tables: fin_db.*\\.balance.*
    server-id: ${mysql_server_id}
    schema-change.enabled: true
sink:
  type: paimon-las
  commit.user: ${paimon_las_commit_user}
pipeline:
  name: ${pipeline_name}
  parallelism: ${pipeline_parallelism}
YAML
)"
```

创建成功后应继续：

1. 记录 `draft_id`
2. 使用 `volc_flink drafts content -i <draft_id>` 回读 YAML
3. 向用户总结 `CdcJobInfo` 视角下的 source/sink/route/transform 结构

---

### 5. CDC 开发迭代

当前 CLI 对 CDC 的创建支持最完整；如果用户要迭代 CDC YAML，优先采用以下方式：

1. 先在文本中修改 YAML（推荐：内联 YAML，不落盘）
2. 再基于更新后的 YAML 重新创建草稿，或在明确具备对应能力时走平台更新流程
3. 不要假设 `drafts update` 已经稳定暴露 `--cdc/--cdc-file/--cdc-dir` 参数，除非先确认当前 CLI 版本支持

如果用户只是要“优化/重写 YAML”：

- 直接输出修订后的完整 YAML
- 明确指出需要替换的参数项

---

### 6. 发布与启动

如果用户明确要求发布/启动：

1. 先做风险确认
2. 发布草稿：

```bash
volc_flink drafts publish --draft-id <draft_id> --resource-pool <resource-pool>
```

3. 启动任务：

```bash
volc_flink jobs start --job-id <job_id>
```

4. 最小验证：
  - `volc_flink jobs detail --job-id <job_id>`
  - `volc_flink jobs events --job-id <job_id>`
  - `volc_flink monitor logs --job-id <job_id>`

---

### 7. 调试与排错

CDC 任务失败时，优先检查：

- 引擎版本是否误用非 1.16
- MySQL 驱动是否已上传
- MySQL `tables` 正则是否正确转义
- `server-id` 是否冲突
- sink 侧鉴权/endpoint/warehouse 参数是否完整
- `route` / `transform` 是否引用了不存在的源表

调试最小命令集：

```bash
volc_flink jobs detail --job-id <job_id>
volc_flink jobs events --job-id <job_id>
volc_flink monitor logs --job-id <job_id>
volc_flink jobs ui --job-id <job_id>
```

---

## 输出要求

### 模板模式

输出应包含：

- 使用的模板名
- 完整 YAML
- 关键参数说明
- 平台限制（如 Flink 1.16 / MySQL Driver）

### 变更模式

输出应包含：

- Scope：`project_name`、`draft_name/job_name`、`draft_id/job_id`
- 计划执行的动作
- 风险确认
- 执行结果
- 回读验证结果
