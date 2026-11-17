# Job Runtime Operations Playbook

作业运维操作 Playbook — 启动/停止/快照的完整操作指南。

## Prerequisites

- 已知作业 ID（格式：`cql-xxxxxxxxxxxx`）
- 已配置 region（默认 `ap-guangzhou`）
- 作业已创建并有已发布的配置版本

## Workflow: 查询作业详情

```bash
python scripts/oceanus_ops.py describe_job_detail \
  --job_id cql-xxx \
  --region ap-guangzhou
```

**返回字段说明**：
- `JobId`: 作业唯一标识
- `Name`: 作业名称
- `Status`: 作业状态码（1-7）
- `StatusDesc`: 状态描述
- `ClusterId`: 所属集群
- `RunningCuNum`: 当前运行 CU 数
- `PublishedJobConfigVersion`: 已发布配置版本号

## Workflow: 启动作业

### 前置条件
- 作业有已发布的配置版本（`PublishedJobConfigVersion > 0`）
- 作业不能处于运行中或操作中状态

### 交互式启动（推荐，不指定 run_type）

当不指定 `--run_type` 时，CLI 会自动查询作业快照并返回 `needs_selection` 响应，
agent 必须询问用户选择启动模式：

```bash
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --region ap-guangzhou \
  --confirm
```

**CLI 返回行为**：
- **有快照**：返回 `needs_selection: true`，列出两个选项：
  - **选项 A**：不使用快照，直接启动（`--run_type 1`）
  - **选项 B**：从历史快照恢复启动（`--run_type 3 --savepoint_id <id>`），并附带快照列表
- **无快照**：自动以 `run_type=1` 直接启动（无需额外确认）

**Agent 行为要求**：
1. 收到 `needs_selection` 响应后，必须向用户展示选项并等待选择
2. 用户选择后，以显式 `--run_type` 重新执行命令
3. 不要替用户做选择，不要静默跳过

### 标准启动（使用最新状态，显式指定 run_type）

```bash
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --region ap-guangzhou \
  --confirm
```

### 从 Savepoint 恢复

```bash
# 通过 Savepoint ID 恢复
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --run_type 3 \
  --savepoint_id sp-xxx \
  --region ap-guangzhou \
  --confirm

# 通过 Savepoint 路径恢复
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --run_type 2 \
  --savepoint_path "cosn://bucket/path/to/savepoint" \
  --region ap-guangzhou \
  --confirm
```

### 从指定时间戳启动

```bash
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --run_type 4 \
  --custom_timestamp 1700000000000 \
  --region ap-guangzhou \
  --confirm
```

### 指定配置版本启动

```bash
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --config_version 3 \
  --region ap-guangzhou \
  --confirm
```

### Run Type 说明

| run_type | 含义 | 附加参数 |
| -------- | ---- | -------- |
| 1 | 从最新状态启动（默认） | 无 |
| 2 | 从 Savepoint 路径恢复 | `--savepoint_path` |
| 3 | 从 Savepoint ID 恢复 | `--savepoint_id` |
| 4 | 从指定时间戳启动 | `--custom_timestamp` |

### 无快照场景处理

当用户指定 `--run_type 3`（从快照恢复）但作业没有任何可用快照时，CLI **不会静默回退**到无快照启动。
而是返回 `needs_selection: true` 响应，附带两个选项：

- **选项 A**：改为不使用快照直接启动（`--run_type 1`）
- **选项 B**：取消启动，暂不操作

**Agent 必须**将此结果展示给用户，等用户确认后再执行下一步。

## Workflow: 停止作业

### 前置条件
- 作业状态必须为**运行中(4)**或**操作中(3)**

### 交互式停止（推荐，不指定 stop_type）

当不指定 `--stop_type` 时，CLI 会返回 `needs_selection: true` 响应，
agent 必须询问用户选择停止方式：

```bash
python scripts/oceanus_ops.py stop_jobs \
  --job_id cql-xxx \
  --region ap-guangzhou \
  --confirm
```

**CLI 返回行为**：返回 `needs_selection: true`，列出两个选项：
- **选项 A**：直接停止（`--stop_type 1`，不生成快照，可能丢失未持久化的状态）
- **选项 B**：触发快照后停止（`--stop_type 2`，推荐，先保留作业状态再停止）

**Agent 行为要求**：
1. 收到 `needs_selection` 响应后，必须向用户展示选项并等待选择
2. 用户选择后，以显式 `--stop_type` 重新执行命令
3. 不要替用户做选择，不要静默使用默认值

### 直接停止（显式指定 stop_type）

```bash
python scripts/oceanus_ops.py stop_jobs \
  --job_id cql-xxx \
  --stop_type 1 \
  --region ap-guangzhou \
  --confirm
```

### 触发快照后停止

```bash
python scripts/oceanus_ops.py stop_jobs \
  --job_id cql-xxx \
  --stop_type 2 \
  --region ap-guangzhou \
  --confirm
```

### Stop Type 说明

| stop_type | 含义 |
| --------- | ---- |
| 1 | 直接停止（立即停止，不生成快照） |
| 2 | 触发快照后停止（推荐用于生产环境，先保留状态再停止） |

## Workflow: 触发作业快照

### 前置条件
- 作业状态必须为**运行中(4)**

### 触发快照

```bash
python scripts/oceanus_ops.py trigger_savepoint \
  --job_id cql-xxx \
  --region ap-guangzhou
```

### 带描述的快照

```bash
python scripts/oceanus_ops.py trigger_savepoint \
  --job_id cql-xxx \
  --description "上线前手动快照" \
  --region ap-guangzhou
```

**返回字段说明**：
- `savepoint_trigger`: 是否触发成功
- `savepoint_id`: 快照 ID
- `savepoint_path`: 快照存储路径

## 典型运维场景

### 场景 1: 更新作业并重启

```bash
# 1. 停止作业（触发快照后停止，保留状态）
python scripts/oceanus_ops.py stop_jobs --job_id cql-xxx --stop_type 2 --region ap-guangzhou --confirm

# 2. 修改草稿并发布新版本配置（必须显式指定 --job_type）
python scripts/oceanus_ops.py modify_draft --job_id cql-xxx --job_type 1 --sql "..." --region ap-guangzhou
python scripts/oceanus_ops.py create_job_config --job_id cql-xxx --job_type 1 --region ap-guangzhou --confirm

# 3. 从最新 Savepoint 恢复启动
python scripts/oceanus_ops.py run_jobs --job_id cql-xxx --run_type 3 --savepoint_id sp-xxx --region ap-guangzhou --confirm
```

### 场景 2: 定时手动快照（用于数据恢复点）

```bash
# 触发手动快照
python scripts/oceanus_ops.py trigger_savepoint --job_id cql-xxx --description "每日例行快照" --region ap-guangzhou
```

### 场景 3: 紧急停止

```bash
# 立即停止（不等待快照，显式指定 --stop_type 1）
python scripts/oceanus_ops.py stop_jobs --job_id cql-xxx --stop_type 1 --region ap-guangzhou --confirm
```

## Error Handling

| Error Code | 含义 | 处理建议 |
| ---------- | ---- | -------- |
| `JobNotFound` | 作业不存在或无权限 | 确认 job_id 和 workspace_id 是否正确 |
| `JobAlreadyRunning` | 作业已在运行中 | 无需重复启动 |
| `JobInProgress` | 作业处于操作中 | 等待操作完成后再执行 |
| `NoPublishedVersion` | 无已发布配置版本 | 先通过 modify_draft + create_job_config 发布配置 |
| `InvalidJobStatus` | 作业状态不满足前置条件 | 根据错误信息中的当前状态判断后续操作 |
| `SafetyCheckRequired` | 缺少 --confirm 参数 | 添加 --confirm 参数重新执行 |
| *(success)* `needs_selection` | CLI 需要用户选择启动模式 | 展示选项让用户选择，不要自动决策 |
