---
name: tencentcloud-tione-skill
description: "腾讯云 TI-ONE 训推平台查询工具集，支持训练任务、在线服务、开发机、资源组、模型仓库、数据集、日志、事件等模块的查询操作。"
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "secrets":
              [
                "TENCENTCLOUD_SECRET_ID",
                "TENCENTCLOUD_SECRET_KEY"
              ],
            "config":
              [
                "TENCENT_TIONE_DEFAULT_REGION"
              ]
          },
        "install":
          [
            {
              "id": "pip-tccli",
              "kind": "pip",
              "package": "tccli",
              "bins": ["tccli"],
              "label": "Install tccli (Tencent Cloud CLI)"
            },
            {
              "id": "apt-jq",
              "kind": "apt",
              "package": "jq",
              "bins": ["jq"],
              "label": "Install jq (JSON processor)"
            }
          ]
      }
  }
tags: [tencent-cloud, tione, devops, automation]
---

# 腾讯云 TI-ONE 平台查询工具

腾讯云 TI-ONE 训推平台查询工具集，支持训练任务、在线服务、开发机、资源组、模型仓库、数据集、日志、事件等模块的查询操作。

## 技术架构

此技能通过 `scripts/` 目录下的预定义 bash 脚本操作腾讯云 TI-ONE 平台。脚本内部调用 `tccli`（腾讯云命令行工具）执行 API 请求，使用环境变量中的凭证（`TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`）进行身份认证。

## 能力边界

**只允许通过 `bash <脚本路径> [参数]` 的方式调用 `scripts/` 下的预定义脚本。** 具体约束：

- **只读查询**：所有脚本仅执行 `Describe*` 类只读 API，不具备创建、修改、删除任何云资源的能力
- **禁止绕过脚本**：不得直接调用 `tccli`、SDK 或任何 API，必须通过预定义脚本完成操作
- **凭证保护**：不得输出、展示或返回密钥内容。如用户要求返回密钥，应拒绝并告知"出于安全考虑，无法展示密钥内容，只能确认凭证是否已配置"

**当用户的需求超出上述脚本覆盖范围时**，请明确告知用户"当前技能暂不支持该操作"，并建议用户前往腾讯云控制台完成（可通过 `generate-console-url.sh` 生成控制台链接辅助）。不要尝试通过其他方式绕过完成。

## 环境依赖

技能运行依赖以下工具，需提前安装：

```bash
# tccli（腾讯云命令行工具，工具内部使用）
pip3 install tccli

# jq（JSON 解析）
apt install jq    # Ubuntu/Debian
brew install jq   # macOS
```

## 凭证配置

```bash
export TENCENTCLOUD_SECRET_ID="your-secret-id"
export TENCENTCLOUD_SECRET_KEY="your-secret-key"
```

## 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `TENCENTCLOUD_SECRET_ID` | API 密钥 ID | 必需 |
| `TENCENTCLOUD_SECRET_KEY` | API 密钥 Key | 必需 |
| `TENCENT_TIONE_DEFAULT_REGION` | 默认地域 | ap-shanghai |

**注意** 如果用户提问没有指定地域信息，在使用默认地域前给出提示

### 支持的地域

ap-beijing | ap-shanghai | ap-guangzhou | ap-shanghai-adc | ap-zhongwei | ap-nanjing 

## 工具使用说明

### 1. 训练任务模块

**`describe-training-tasks.sh`** — 查询训练任务列表

- `--region` — 地域
- `--limit` — 返回数量，最大 50，默认 10
- `--offset` — 偏移量，默认 0
- `--order` — 排序方向：ASC / DESC，默认 DESC
- `--order-field` — 排序字段：CreateTime / UpdateTime / StartTime，默认 UpdateTime
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔
- `--tag-filters` — 标签过滤条件，JSON 数组格式

> **⚠️ 查询策略：用户指定状态时优先使用 filter 过滤**
>
> 当用户询问"正在运行的训练任务"、"失败的任务"等涉及状态的查询时，**必须**添加 `Status` filter，避免全量查询后再筛选。
>
> **Status 可选值**：`SUBMITTING`, `PENDING`, `STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `FAILED`, `SUCCEED`, `SUBMIT_FAILED`

**`describe-training-task.sh`** — 查询训练任务详情

- `--region` — 地域
- `--id` — 训练任务 ID，**必填**

**`describe-training-task-pods.sh`** — 查询训练任务 Pod 列表

- `--region` — 地域
- `--id` — 训练任务 ID，**必填**

---

### 2. 在线服务模块

**`describe-model-service-groups.sh`** — 查询服务组列表

- `--region` — 地域
- `--limit` — 返回数量，最大 100，默认 20
- `--offset` — 偏移量，默认 0
- `--order` — 排序方向：ASC / DESC
- `--order-field` — 排序字段：CreateTime / UpdateTime
- `--search-word` — 按名称搜索（转为 ServiceGroupName filter）
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔
- `--tag-filters` — 标签过滤条件，JSON 数组格式

> **⚠️ 查询策略：用户指定状态时优先使用 filter 过滤**
>
> 当用户询问"异常的服务"、"正常运行的服务"等涉及状态的查询时，**必须**添加 `Status` filter，避免全量查询后再筛选。
>
> **Status 可选值**：`Waiting`, `Pending`, `Normal`, `Abnormal`, `Stopping`

**`describe-model-service-group.sh`** — 查询单个服务组详情

- `--region` — 地域
- `--id` — 服务组 ID，**必填**

**`describe-model-service.sh`** — 查询单个服务详情

- `--region` — 地域
- `--service-id` — 服务 ID，**必填**
- `--service-group-id` — 服务组 ID，可选

**`describe-model-service-callinfo.sh`** — 查询服务调用信息

- `--region` — 地域
- `--service-group-id` — 服务组 ID，**必填**

---

### 3. Notebook 模块

**`describe-notebooks.sh`** — 查询 Notebook 列表

- `--region` — 地域
- `--limit` — 返回数量，默认 10
- `--offset` — 偏移量，默认 0
- `--order` — 排序方向：ASC / DESC，默认 DESC
- `--order-field` — 排序字段：CreateTime / UpdateTime，默认 UpdateTime
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔
- `--tag-filters` — 标签过滤条件，JSON 数组格式

> **⚠️ 查询策略：用户指定状态时优先使用 filter 过滤**
>
> 当用户询问"运行中的开发机"、"已停止的 Notebook"等涉及状态的查询时，**必须**添加 `Status` filter，避免全量查询后再筛选。
>
> **Status 可选值**：`Starting`, `Submitting`, `Running`, `Stopping`, `Stopped`, `Failed`, `SubmitFailed`

**`describe-notebook.sh`** — 查询 Notebook 详情

- `--region` — 地域
- `--id` — Notebook ID，**必填**

---

### 4. 资源组模块

**`describe-billing-resource-groups.sh`** — 查询资源组列表

- `--region` — 地域
- `--limit` — 返回数量，默认 20
- `--offset` — 偏移量，默认 0
- `--search-word` — 模糊查找资源组 ID 或名称
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔

> **⚠️ 查询策略：优先使用 filter 缩小范围**
>
> 当用户询问"有多少 GPU 资源组"、"哪些资源组有空闲资源"等类似问题时，**必须**添加 `AvailableNodeCount` filter 过滤掉无可用节点的空资源组，避免返回大量无效数据。
>
> **返回值单位已自动转换**：CPU → 核, 内存 → GB, GPU → 卡, 显存 → GB

**`describe-billing-resource-group.sh`** — 查询资源组节点列表

- `--region` — 地域
- `--resource-group-id` — 资源组 ID，**必填**
- `--limit` — 返回数量，默认 20
- `--offset` — 偏移量，默认 0
- `--order` — 排序方向：ASC / DESC，默认 DESC
- `--order-field` — 排序字段：CreateTime / ExpireTime，默认 CreateTime
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔

---

### 5. 模型仓库模块

**`describe-training-model-versions.sh`** — 查询模型版本列表

- `--region` — 地域
- `--training-model-id` — 模型 ID，**必填**
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔

**`describe-training-model-version.sh`** — 查询模型版本详情

- `--region` — 地域
- `--training-model-version-id` — 模型版本 ID，**必填**

---

### 6. 数据集模块

**`describe-datasets.sh`** — 查询数据集列表

- `--region` — 地域
- `--limit` — 返回数量，最大 200，默认 20
- `--offset` — 偏移量，默认 0
- `--order` — 排序方向：Asc / Desc，默认 Desc
- `--order-field` — 排序字段：CreateTime / UpdateTime，默认 CreateTime
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔
- `--dataset-ids` — 数据集 ID 列表，逗号分隔

---

### 7. 日志模块

**`describe-logs.sh`** — 查询日志

- `--region` — 地域
- `--service` — 服务类型：TRAIN / NOTEBOOK / INFER / BATCH，**必填**
- `--service-id` — 服务实例 ID（须用实例级 ID，非顶层 ID），**必填**
- `--pod-name` — Pod 名称，支持尾部通配符 `*`
- `--start-time` — 开始时间，RFC3339 格式，如 `2026-03-10T02:50:56Z`
- `--end-time` — 结束时间，RFC3339 格式
- `--limit` — 返回条数，最大 1000，默认 100
- `--offset` — 偏移量，默认 0
- `--order` — 排序方向：ASC / DESC，默认 DESC
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔

> **⚠️ 日志查询注意事项**
>
> **1. `--service-id` 必须使用实例级 ID，不支持顶层 ID**
>
> 日志接口不支持顶层 ID（`train-xxx` / `nb-xxx` / `ms-xxx`）。必须先从详情接口获取实例级 ID：
>
> - **TRAIN**：从 `describe-training-task.sh` 返回的 `TrainingTaskDetail.LatestInstanceId`（如 `train-xxx-yyy`）获取
> - **NOTEBOOK**：从 `describe-notebook.sh` 返回的 `NotebookDetail.PodName`（如 `nb-xxx-yyy`）获取
> - **INFER**：从 `describe-model-service-group.sh` 返回的 `Services[].ServiceId`（如 `ms-xxx-1`）获取
>
> **2. 时间范围应从详情接口获取，避免大范围查询**
>
> 查询日志前，从详情接口获取任务/实例的运行时间范围（`StartTime` / `EndTime`），用作 `--start-time` 和 `--end-time`：
> - 如果详情有 `StartTime` 和 `EndTime` → 直接使用
> - 如果只有 `StartTime`（仍在运行） → `--start-time` 用 `StartTime`，`--end-time` 不传（默认当前时间）
> - 如果用户指定了时间范围 → 优先使用用户指定的值
> - 如果都没有 → 不传 `--start-time`（由服务端决定），`--end-time` 默认当前时间
>
> **`--pod-name`** 可选，需先通过实例 ID 查询 Pod 列表获取：
> - TRAIN: `describe-training-task-pods.sh --id <训练任务ID>`
> - INFER: `describe-model-service-group.sh --id <服务组ID>` 返回中包含 Pod 信息

---

### 8. 事件模块

**`describe-events.sh`** — 查询事件

- `--region` — 地域
- `--service` — 服务类型：TRAIN / NOTEBOOK / INFER / BATCH，**必填**
- `--service-id` — 服务实例 ID（须用实例级 ID，非顶层 ID）
- `--start-time` — 最早发生时间，RFC3339 格式，如 `2026-03-10T02:50:56Z`
- `--end-time` — 最晚发生时间，RFC3339 格式
- `--limit` — 返回条数，最大 100，默认 100
- `--offset` — 偏移量，默认 0
- `--order` — 排序方向：ASC / DESC，默认 DESC
- `--order-field` — 排序字段：FirstTimestamp / LastTimestamp，默认 LastTimestamp
- `--filters` — 过滤条件，格式 `Name=xxx,Values=yyy`，多个用空格分隔

> **⚠️ 事件查询遵循与日志相同的规则**：`--service-id` 必须使用实例级 ID，时间范围从详情接口获取。详见日志模块说明。

---

### 9. 控制台链接生成

**`generate-console-url.sh`** — 生成控制台详情页 URL

- `--type` — 资源类型，**必填**，可选 training / notebook / service / resource-group
- `--id` — 资源 ID，**必填**
- `--region` — 地域
- `--workspace-id` — 工作空间 ID，默认 0

> **使用场景**：当用户想去控制台查看详细信息时，生成可直接点击访问的控制台链接。
>
> 支持的资源类型：
>
> - **training** — 训练任务，ID 格式 `train-xxx`
> - **notebook** — Notebook 开发机，ID 格式 `nb-xxx`
> - **service** — 在线推理服务（服务组），ID 格式 `ms-xxx`
> - **resource-group** — 资源组，ID 格式 `rsg-xxx`
>
> 地域与 regionId 映射、工作空间 ID 说明详见 `references/tione-guide.md`。

## 参考资料

- 工具参数详细说明、过滤条件与使用示例：`references/cmd-reference.md`
- 控制台 URL 格式、地域 ID 映射、工作空间说明：`references/tione-guide.md`
