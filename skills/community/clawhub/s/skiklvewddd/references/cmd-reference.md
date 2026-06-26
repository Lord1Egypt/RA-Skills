# TI-ONE 工具参数参考

本文档列出各工具支持的详细参数、过滤条件与使用示例。

## 训练任务模块

### describe-training-tasks.sh

查询训练任务列表。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 地域 | 环境变量配置值 |
| `--limit` | 返回数量，最大 50 | 10 |
| `--offset` | 偏移量 | 0 |
| `--order` | 排序方向：ASC / DESC | DESC |
| `--order-field` | 排序字段：CreateTime / UpdateTime / StartTime | UpdateTime |
| `--filters` | 过滤条件 | - |
| `--tag-filters` | 标签过滤条件（JSON 数组） | - |

**Filters 支持的 Name 值：**

| Name | 说明 | 可选 Values |
|------|------|------------|
| Name | 按任务名称模糊匹配 | 任意字符串 |
| Id | 按任务 ID 过滤 | `train-xxx` |
| Status | 按状态过滤 | `SUBMITTING`, `PENDING`, `STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `FAILED`, `SUCCEED`, `SUBMIT_FAILED` |
| ResourceGroupId | 按资源组 ID 过滤 | `trsg-xxx` |
| Creator | 按创建者 uin 过滤 | UIN 数字 |
| ChargeType | 按计费类型过滤 | `PREPAID`(预付费), `POSTPAID_BY_HOUR`(后付费) |
| CHARGE_STATUS | 按计费状态过滤 | `NOT_BILLING`, `BILLING`, `ARREARS_STOP` |

### describe-training-task.sh

查询训练任务详情。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--id` | 训练任务 ID | 是 |

### describe-training-task-pods.sh

查询训练任务 Pod 列表。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--id` | 训练任务 ID | 是 |

## 在线服务模块

### describe-model-service-groups.sh

查询服务组列表。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 地域 | 环境变量配置值 |
| `--limit` | 返回数量，最大 100 | 20 |
| `--offset` | 偏移量 | 0 |
| `--order` | 排序方向：ASC / DESC | - |
| `--order-field` | 排序字段：CreateTime / UpdateTime | - |
| `--search-word` | 按名称搜索（转为 ServiceGroupName filter） | - |
| `--filters` | 过滤条件 | - |
| `--tag-filters` | 标签过滤条件（JSON 数组） | - |

**Filters 支持的 Name 值：**

| Name | 说明 |
|------|------|
| ClusterId | 按集群 ID 过滤 |
| ServiceId | 按服务 ID 过滤 |
| ServiceGroupName | 按服务组名称过滤 |
| ServiceGroupId | 按服务组 ID 过滤 |
| Status | 按状态过滤：`Waiting`, `Pending`, `Normal`, `Abnormal`, `Stopping` |
| CreatedBy | 按创建者 uin 过滤 |
| ModelVersionId | 按模型版本 ID 过滤 |

### describe-model-service-group.sh

查询单个服务组详情。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--id` | 服务组 ID | 是 |

### describe-model-service.sh

查询单个服务详情。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--service-id` | 服务 ID | 是 |
| `--service-group-id` | 服务组 ID | 否 |

### describe-model-service-callinfo.sh

查询服务调用信息。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--service-group-id` | 服务组 ID | 是 |

## Notebook 模块

### describe-notebooks.sh

查询 Notebook 列表。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 地域 | 环境变量配置值 |
| `--limit` | 返回数量 | 10 |
| `--offset` | 偏移量 | 0 |
| `--order` | 排序方向：ASC / DESC | DESC |
| `--order-field` | 排序字段：CreateTime / UpdateTime | UpdateTime |
| `--filters` | 过滤条件 | - |
| `--tag-filters` | 标签过滤条件（JSON 数组） | - |

**Filters 支持的 Name 值：**

| Name | 说明 | 可选 Values |
|------|------|------------|
| Name | 按名称模糊匹配 | 任意字符串 |
| Id | 按 Notebook ID 过滤 | `nb-xxx` |
| Status | 按状态过滤 | `Starting`, `Submitting`, `Running`, `Stopping`, `Stopped`, `Failed`, `SubmitFailed` |
| Creator | 按创建者 uin 过滤 | UIN 数字 |
| ChargeType | 按计费类型过滤 | `PREPAID`, `POSTPAID_BY_HOUR` |
| ChargeStatus | 按计费状态过滤 | `NOT_BILLING`, `BILLING`, `BILLING_STORAGE`, `ARREARS_STOP` |
| DefaultCodeRepoId | 按默认代码仓库 ID 过滤 | `cr-xxx` |
| AdditionalCodeRepoId | 按关联代码仓库 ID 过滤 | `cr-xxx` |
| LifecycleScriptId | 按生命周期脚本 ID 过滤 | `ls-xxx` |

### describe-notebook.sh

查询 Notebook 详情。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--id` | Notebook ID | 是 |

## 资源组模块

### describe-billing-resource-groups.sh

查询资源组列表。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 地域 | 环境变量配置值 |
| `--limit` | 返回数量 | 20 |
| `--offset` | 偏移量 | 0 |
| `--search-word` | 模糊查找资源组 ID 或名称 | - |
| `--filters` | 过滤条件 | - |

**Filters 支持的 Name 值：**

| Name | 说明 |
|------|------|
| ResourceGroupId | 按资源组 ID 过滤（Fuzzy=true 时支持模糊查询） |
| ResourceGroupName | 按资源组名称过滤（Fuzzy=true 时支持模糊查询） |
| AvailableNodeCount | 按可用节点数量过滤 |

### describe-billing-resource-group.sh

查询资源组节点列表。

| 参数 | 说明 | 必填/默认值 |
|------|------|------------|
| `--region` | 地域 | 否 |
| `--resource-group-id` | 资源组 ID | 是 |
| `--limit` | 返回数量 | 20 |
| `--offset` | 偏移量 | 0 |
| `--order` | 排序方向：ASC / DESC | DESC |
| `--order-field` | 排序字段：CreateTime / ExpireTime | CreateTime |
| `--filters` | 过滤条件 | - |

**Filters 支持的 Name 值：**

| Name | 说明 |
|------|------|
| InstanceId | 按节点 ID 过滤（Fuzzy=true 时支持模糊查询） |
| InstanceStatus | 按节点状态过滤（如 `RUNNING`） |

## 模型仓库模块

### describe-training-model-versions.sh

查询模型版本列表。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--training-model-id` | 模型 ID | 是 |
| `--filters` | 过滤条件 | 否 |

**Filters 支持的 Name 值：**

| Name | 说明 | 可选 Values |
|------|------|------------|
| TrainingModelVersionId | 按模型版本 ID 过滤 | `mv-xxx` |
| ModelVersionType | 按版本类型过滤 | `NORMAL`(通用), `ACCELERATE`(加速) |
| ModelFormat | 按模型格式过滤 | `TORCH_SCRIPT`, `PYTORCH`, `DETECTRON2`, `SAVED_MODEL`, `FROZEN_GRAPH`, `PMML` |
| AlgorithmFramework | 按算法框架过滤 | `TENSORFLOW`, `PYTORCH`, `DETECTRON2` |

### describe-training-model-version.sh

查询模型版本详情。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--region` | 地域 | 否 |
| `--training-model-version-id` | 模型版本 ID | 是 |

## 数据集模块

### describe-datasets.sh

查询数据集列表。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 地域 | 环境变量配置值 |
| `--limit` | 返回数量，最大 200 | 20 |
| `--offset` | 偏移量 | 0 |
| `--order` | 排序值：Asc / Desc | Desc |
| `--order-field` | 排序字段：CreateTime / UpdateTime | CreateTime |
| `--filters` | 过滤条件 | - |
| `--dataset-ids` | 数据集 ID 列表 | - |

**Filters 支持的 Name 值：**

| Name | 说明 | 可选 Values |
|------|------|------------|
| DatasetName | 按数据集名称过滤 | 任意字符串 |
| DatasetScope | 按范围过滤 | `SCOPE_DATASET_PRIVATE`(私有), `SCOPE_DATASET_PUBLIC`(公共) |

## 日志模块

### describe-logs.sh

查询日志。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 地域 | 环境变量配置值 |
| `--service` | 服务类型：TRAIN / NOTEBOOK / INFER / BATCH | 必填 |
| `--service-id` | 服务实例 ID（注意：须用实例级 ID） | 必填 |
| `--pod-name` | Pod 名称（支持尾部通配符 *） | - |
| `--start-time` | 开始时间（RFC3339 格式） | 当前时间前一小时 |
| `--end-time` | 结束时间（RFC3339 格式） | 当前时间 |
| `--limit` | 返回条数，最大 1000 | 100 |
| `--offset` | 偏移量 | 0 |
| `--order` | 排序方向：ASC / DESC | DESC |
| `--filters` | 过滤条件 | - |

**Filters 支持的 Name 值：**

| Name | 说明 |
|------|------|
| Key | 按关键字过滤日志（多值时表示同时满足） |

## 事件模块

### describe-events.sh

查询事件。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 地域 | 环境变量配置值 |
| `--service` | 服务类型：TRAIN / NOTEBOOK / INFER / BATCH | 必填 |
| `--service-id` | 服务实例 ID | - |
| `--start-time` | 最早发生时间（RFC3339 格式） | 前一天 |
| `--end-time` | 最晚发生时间（RFC3339 格式） | 当前时间 |
| `--limit` | 返回条数，最大 100 | 100 |
| `--offset` | 偏移量 | 0 |
| `--order` | 排序方向：ASC / DESC | DESC |
| `--order-field` | 排序字段：FirstTimestamp / LastTimestamp | LastTimestamp |
| `--filters` | 过滤条件 | - |

**Filters 支持的 Name 值：**

| Name | 说明 | 可选 Values |
|------|------|------------|
| ResourceKind | 按资源类型过滤 | `Deployment`, `Replicaset`, `Pod` 等 |
| Type | 按事件类型过滤 | `Normal`, `Warning` |

## 控制台链接工具

### generate-console-url.sh

生成控制台详情页 URL。

| 参数 | 说明 | 必填/默认值 |
|------|------|------------|
| `--type` | 资源类型：training / notebook / service / resource-group | 是 |
| `--id` | 资源 ID | 是 |
| `--region` | 地域 | 默认值 |
| `--workspace-id` | 工作空间 ID | 0 |

## 典型使用示例

### 1. 排查训练任务问题（标准流程：指定训练任务 ID train-xxx 时）

```bash
# 步骤 1: 查看训练任务详情，获取 LatestInstanceId 和 StartTime/EndTime
./scripts/training/describe-training-task.sh --region ap-shanghai --id train-xxx
# 从返回中获取:
#   LatestInstanceId (如 train-xxx-yyy) — 日志/事件查询必需
#   StartTime / EndTime — 用作日志时间范围

# 步骤 2: 使用 LatestInstanceId + 时间范围查询日志
./scripts/log/describe-logs.sh --region ap-shanghai --service TRAIN \
  --service-id train-xxx-yyy \
  --start-time "2026-03-10T02:50:56Z" --end-time "2026-03-10T03:30:00Z" --limit 50

# 步骤 3: 如需查看指定 Pod 日志，先获取 Pod 列表
./scripts/training/describe-training-task-pods.sh --region ap-shanghai --id train-xxx
# 从返回结果获取 Pod 名称

# 步骤 4: 使用 Pod 名称查询指定 Pod 日志
./scripts/log/describe-logs.sh --region ap-shanghai --service TRAIN \
  --service-id train-xxx-yyy --pod-name <pod-name> --limit 50

# 查看训练事件
./scripts/event/describe-events.sh --region ap-shanghai --service TRAIN \
  --service-id train-xxx-yyy --start-time "2026-03-10T02:50:56Z"
```

### 1.1 按状态查询训练任务

```bash
# 查询运行中的训练任务 → 优先用 Status filter
./scripts/training/describe-training-tasks.sh --region ap-shanghai --filters "Name=Status,Values=RUNNING"

# 查询失败的任务
./scripts/training/describe-training-tasks.sh --region ap-shanghai --filters "Name=Status,Values=FAILED"

# 查询活跃状态的任务（运行中+启动中+停止中）
./scripts/training/describe-training-tasks.sh --region ap-shanghai --filters "Name=Status,Values=RUNNING;STARTING;STOPPING"
```

### 2. 排查在线服务问题（标准流程：指定服务组 ID ms-xxx 时）

```bash
# 步骤 1: 查看服务组详情，获取服务实例 ID 和 Pod 名称
./scripts/service/describe-model-service-group.sh --region ap-shanghai --id ms-xxx
# 从 Services[].ServiceId 获取实例 ID，如 ms-xxx-1, ms-xxx-2

# 步骤 2: 使用服务实例 ID 查询日志
./scripts/log/describe-logs.sh --region ap-shanghai --service INFER --service-id ms-xxx-1 --limit 100

# 步骤 3: 如需指定 Pod，从步骤 1 返回中获取 Pod 名称
./scripts/log/describe-logs.sh --region ap-shanghai --service INFER --service-id ms-xxx-1 --pod-name <pod-name>

# 查看单个服务实例详情
./scripts/service/describe-model-service.sh --region ap-shanghai --service-id ms-xxx-1

# 查看服务调用信息
./scripts/service/describe-model-service-callinfo.sh --region ap-shanghai --service-group-id ms-xxx

# 查看推理事件
./scripts/event/describe-events.sh --region ap-shanghai --service INFER --service-id ms-xxx-1
```

### 2.1 按状态查询在线服务

```bash
# 查询异常服务 → 优先用 Status filter
./scripts/service/describe-model-service-groups.sh --region ap-shanghai --filters "Name=Status,Values=Abnormal"

# 查询正常运行的服务
./scripts/service/describe-model-service-groups.sh --region ap-shanghai --filters "Name=Status,Values=Normal"

# 查询活跃状态的服务
./scripts/service/describe-model-service-groups.sh --region ap-shanghai --filters "Name=Status,Values=Normal;Waiting;Pending"
```

### 3. 查看 Notebook 状态

```bash
# 查看 Notebook 列表
./scripts/notebook/describe-notebooks.sh --region ap-shanghai

# 查看某个 Notebook 详情
./scripts/notebook/describe-notebook.sh --region ap-shanghai --id nb-xxx
```

### 3.1 排查 Notebook 日志（标准流程）

```bash
# 步骤 1: 查看 Notebook 详情，获取 PodName 和 StartTime
./scripts/notebook/describe-notebook.sh --region ap-shanghai --id nb-xxx
# 从 NotebookDetail 获取:
#   PodName (如 nb-xxx-yyy) — 日志查询必需
#   StartTime — 用作日志时间范围起点

# 步骤 2: 使用 PodName + 时间范围查询日志
./scripts/log/describe-logs.sh --region ap-shanghai --service NOTEBOOK \
  --service-id nb-xxx-yyy --start-time "2026-03-17T19:23:21Z" --limit 50

# 查看 Notebook 事件
./scripts/event/describe-events.sh --region ap-shanghai --service NOTEBOOK \
  --service-id nb-xxx-yyy --start-time "2026-03-17T19:23:21Z"
```

### 3.2 按状态查询开发机

```bash
# 查询运行中的开发机 → 优先用 Status filter
./scripts/notebook/describe-notebooks.sh --region ap-shanghai --filters "Name=Status,Values=Running"

# 查询已停止的开发机
./scripts/notebook/describe-notebooks.sh --region ap-shanghai --filters "Name=Status,Values=Stopped"

# 查询活跃状态的开发机（运行中+启动中+停止中）
./scripts/notebook/describe-notebooks.sh --region ap-shanghai --filters "Name=Status,Values=Running;Starting;Stopping"
```

### 4. 查看资源与计费

```bash
# 查看所有资源组
./scripts/resource/describe-billing-resource-groups.sh --region ap-shanghai

# 查询有可用节点的资源组 → 优先用 filter 排除空组
./scripts/resource/describe-billing-resource-groups.sh --region ap-shanghai --filters "Name=AvailableNodeCount,Values=1;2;3;4;5;6;7;8;9;10"

# 按名称模糊搜索资源组
./scripts/resource/describe-billing-resource-groups.sh --region ap-shanghai --filters "Name=ResourceGroupName,Values=test,Fuzzy=true"

# 查看资源组节点
./scripts/resource/describe-billing-resource-group.sh --region ap-shanghai --resource-group-id rg-xxx
```

### 5. 生成控制台链接

```bash
# 生成训练任务控制台链接
./scripts/utils/generate-console-url.sh --type training --id train-xxx

# 生成 Notebook 控制台链接
./scripts/utils/generate-console-url.sh --type notebook --id nb-xxx --region ap-beijing

# 生成推理服务控制台链接（指定工作空间）
./scripts/utils/generate-console-url.sh --type service --id ms-xxx --workspace-id 12345

# 生成资源组控制台链接
./scripts/utils/generate-console-url.sh --type resource-group --id rsg-xxx
```
