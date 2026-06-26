# 查询任务参数与示例 — `mps_get_video_task.py` / `mps_get_image_task.py`

## 查询音视频任务 — `mps_get_video_task.py`

适用于 `ProcessMedia` 提交的任务（TaskId 格式：`1234567890-WorkflowTask-xxxxxx`）

### 参数说明

| 参数 | 说明 |
|------|------|
| `--task-id` | 任务 ID（必填）|
| `--verbose` / `-v` | 输出完整 JSON 响应（含所有子任务详情）|
| `--json` | 只输出原始 JSON，不打印格式化摘要 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|

### 示例命令

```bash
# 查询任务状态（简洁输出）
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a

# 详细输出（含子任务信息）
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --verbose

# JSON 格式输出（便于程序解析）
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --json

# 指定地域
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --region ap-beijing
```

---

## 查询图片任务 — `mps_get_image_task.py`

适用于 `ProcessImage` 提交的任务

### 参数说明

| 参数 | 说明 |
|------|------|
| `--task-id` | 任务 ID（必填）|
| `--verbose` / `-v` | 输出完整 JSON 响应 |
| `--json` | 只输出原始 JSON |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|

### 示例命令

```bash
# 查询任务状态（简洁输出）
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a

# 详细输出（含子任务信息）
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --verbose

# JSON 格式输出
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --json

# 指定地域
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --region ap-beijing
```

## 强制规则

1. **任务类型未知时必须追问**：用户只说"查询任务 xxx"而未说明任务类型时，**必须先询问**任务类型（音视频/图片/AIGC生图/AIGC生视频），不得猜测直接调用。
2. **AIGC 任务不得用此脚本查询**：AIGC 生图/生视频任务有独立查询方式（`mps_aigc_image.py --task-id` / `mps_aigc_video.py --task-id`），**不得**用 `mps_get_video_task.py` 或 `mps_get_image_task.py` 查询。
3. **TaskId 含 WorkflowTask 不代表任务类型**：音视频处理和图片处理任务的 ID 都可能含 `WorkflowTask`，**不能**以此判断类型，仍需询问用户。
