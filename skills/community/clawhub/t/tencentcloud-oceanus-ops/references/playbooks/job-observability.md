# Playbook: Job Observability

作业可观测模块用于查询作业事件和运行日志，所有数据均按作业实例
（`RunningOrderId`，对应一次启动→停止的生命周期）归档。

涵盖的命令：

- `describe_job_events` — 查询作业事件（两阶段）
- `describe_job_running_log` — 查询作业日志（三阶段）
- `describe_job_log_cos_files` — 列出 COS 日志文件并生成预签名下载链接

## 1. Job Events (`describe_job_events`)

两阶段查询模式：

1. **Phase 1**：不传 `--running_order_ids` → 返回时间范围内的运行实例列表
2. **Phase 2**：传 `--running_order_ids` → 返回指定实例的事件详情

时间范围约束：默认最近 24 小时；最大跨度 7 天；起始时间距今不超过 90 天。

```bash
# Phase 1 — 默认最近 24 小时
python scripts/oceanus_ops.py describe_job_events \
  --job_id cql-xxx \
  --region ap-guangzhou \
  --workspace_id space-xxx

# Phase 1 — 指定时间范围（秒级时间戳）
python scripts/oceanus_ops.py describe_job_events \
  --job_id cql-xxx \
  --start_timestamp 1700000000 --end_timestamp 1700600000 \
  --region ap-guangzhou --workspace_id space-xxx

# Phase 2 — 查询指定实例的事件详情
python scripts/oceanus_ops.py describe_job_events \
  --job_id cql-xxx \
  --running_order_ids 1,2,3 \
  --region ap-guangzhou --workspace_id space-xxx
```

> Note: `DescribeJobEvents` 在内部要求 `WorkSpaceId`；不传时会返回
> `system error: reflect: ...`。请始终带上 `--workspace_id`。

## 2. Job Running Log (`describe_job_running_log`)

三阶段渐进式查询：

1. **Phase 1**：仅 `--job_id` → 实例列表（含 `log_collect_type`，参见
   `references/enum-reference.md → LogCollect (response)`）
2. **Phase 2**：`--running_order_id`，不传 `--container` → 容器列表
3. **Phase 3**：`--running_order_id` + `--container` → 日志内容

> Note: `DescribeJobRunningLog` **不接受** `WorkSpaceId` 参数；CLI 即使
> 收到 `--workspace_id` 也会显式忽略，不下发到该接口。

```bash
# Phase 1 — 实例列表，查看各实例的日志采集类型
python scripts/oceanus_ops.py describe_job_running_log \
  --job_id cql-xxx --region ap-guangzhou

# Phase 2 — 容器列表
python scripts/oceanus_ops.py describe_job_running_log \
  --job_id cql-xxx --running_order_id 1 \
  --region ap-guangzhou

# Phase 3 — 日志内容（支持关键字搜索 + 分页）
python scripts/oceanus_ops.py describe_job_running_log \
  --job_id cql-xxx --running_order_id 1 \
  --container jobmanager-0 \
  --keyword "ERROR" \
  --region ap-guangzhou
```

实例列表中各实例的 `log_collect_type`（响应侧枚举）决定后续查询路径：

| log_collect_type | 含义 | 后续查询 |
| ---------------- | ---- | -------- |
| 0 / 2 | 未采集 | — |
| 1 / 3 | 采集到 CLS | 走 Phase 2 / 3（CLS 后端） |
| 4     | 采集到 COS | **改用** `describe_job_log_cos_files` |
| 5     | 采集到 ES  | 走 Phase 2 / 3（ES 后端） |

## 3. COS Log Files (`describe_job_log_cos_files`)

当 `JobCollectType=4`（COS）时使用。流程：

1. `DescribeJobsExists` → 取作业绑定的 `ClusterId`
2. `DescribeClusters` → 取集群的 `LogCOSBucket` / `DefaultCOSBucket` / `CdcId`
3. 按 CDC / 普通集群规则拼 COS 路径：
   - 普通集群：`bucket = LogCOSBucket`，`region = {Region}`
   - CDC 集群：`bucket = DefaultCOSBucket`，`region = {CdcId}.cos-cdc.{Region}`
   - 路径前缀：`job-running-log/{ClusterId}/{JobId}/{RunningOrderId}/{component}/`
4. COS `ListObjects` → 拿到文件列表
5. 为每个文件生成预签名下载 URL（默认有效期 1 小时）

```bash
# 默认查 jobmanager 日志
python scripts/oceanus_ops.py describe_job_log_cos_files \
  --job_id cql-xxx --running_order_id 1 \
  --region ap-guangzhou

# 查 taskmanager 日志
python scripts/oceanus_ops.py describe_job_log_cos_files \
  --job_id cql-xxx --running_order_id 1 \
  --component taskmanager \
  --region ap-guangzhou
```

## Common Errors

| Error / Symptom | 原因 | 处理 |
| ---------------- | ---- | ---- |
| `system error: reflect: call of reflect.Value.FieldByName on zero Value` (DescribeJobEvents) | 没传 `WorkSpaceId` | 加 `--workspace_id <id>` |
| `UnknownParameter: The parameter WorkSpaceId is not recognized.` (DescribeJobRunningLog) | 该接口不支持 `WorkSpaceId` | CLI 已自动忽略；如直接调用 SDK，请去掉该字段 |
| `MissingParameter: EndTime` / `Limit` (DescribeJobRunningLog) | 该接口要求时间范围（毫秒）和 `Limit` | 用 `--start_time`/`--end_time`/`--limit` 显式指定 |
| `NoCOSBucket` (describe_job_log_cos_files) | 集群未配置 `LogCOSBucket` / `DefaultCOSBucket` | 集群侧未开启 COS 日志采集，请联系集群管理员或改查 CLS |

## 典型场景

### 场景 1：作业反复重启，定位原因

```bash
# 1. 看作业当前状态与 RestartCount
python scripts/oceanus_ops.py describe_job_detail --job_id cql-xxx --region ap-guangzhou

# 2. 看最近 24 小时的运行实例（重启次数 = 实例个数 - 1）
python scripts/oceanus_ops.py describe_job_events --job_id cql-xxx \
  --region ap-guangzhou --workspace_id space-xxx

# 3. 取最近一次 RunningOrderId，查看事件详情（异常事件会带 message / solution_link）
python scripts/oceanus_ops.py describe_job_events --job_id cql-xxx \
  --running_order_ids <latest_id> \
  --region ap-guangzhou --workspace_id space-xxx

# 4. 如有必要，进一步查 jobmanager 日志中的 ERROR
python scripts/oceanus_ops.py describe_job_running_log --job_id cql-xxx \
  --running_order_id <latest_id> --container jobmanager-0 \
  --keyword "ERROR" --region ap-guangzhou
```

### 场景 2：下载历史日志归档（COS）

```bash
# 1. Phase 1 看 log_collect_type，确认是 COS（值=4）
python scripts/oceanus_ops.py describe_job_running_log --job_id cql-xxx --region ap-guangzhou

# 2. 列出 COS 日志文件 + 预签名链接
python scripts/oceanus_ops.py describe_job_log_cos_files \
  --job_id cql-xxx --running_order_id <id> --component taskmanager \
  --region ap-guangzhou
```
