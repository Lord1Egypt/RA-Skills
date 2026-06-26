# vod_describe_task — Detailed Parameters and Examples

> Corresponding script: `scripts/vod_describe_task.py`
>
> Query the execution status and result details of a VOD asynchronous task by task ID (supports tasks submitted within the last 3 days).

## Parameters

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--task-id` | string | ✅ | Task ID (e.g., `1490013579-procedurev2-acd135`) |
| `--sub-app-id` | int | - | VOD sub-application ID (required for accounts created after 2023-12-25; can also be set via environment variable `TENCENTCLOUD_VOD_SUB_APP_ID`) |
| `--region` | string | - | Region (default: `ap-guangzhou`) |
| `--no-wait` | flag | - | Query current status only, without waiting for completion (default: auto-wait) |
| `--max-wait` | int | - | Maximum wait time in seconds (default: 600) |
| `--interval` | int | - | Polling interval in seconds (default: 5) |
| `--json` | flag | - | Output full API response in JSON format |
| `--verbose` / `-v` | flag | - | Output detailed information (including output URLs, etc.) |

**Task Status Description**:

| Status | Meaning |
|------|------|
| `WAITING` | Waiting; processing has not yet started |
| `PROCESSING` | Processing in progress |
| `FINISH` | Completed (success) |
| `ABORTED` | Terminated (failed or cancelled) |
| `FAIL` | Failed (sub-task level status) |
| `SUCCESS` | Succeeded (sub-task level status) |

---

## Supported Task Types

| Task Type | Description |
|----------|---------|
| `Procedure` | Video processing task |
| `EditMedia` | Video editing task |
| `SplitMedia` | Video splitting task |
| `ComposeMedia` | Media composition task |
| `WechatPublish` | We Chat publishing task |
| `WechatMiniProgramPublish` | We Chat Mini Program publishing task |
| `PullUpload` | Pull upload task |
| `FastClipMedia` | Fast clip task (no detailed parsing available; use `--json` to view the full response) |
| `RemoveWatermarkTask` | Intelligent watermark removal task |
| `DescribeFileAttributesTask` | File attribute retrieval task |
| `RebuildMedia` | Audio/video quality restoration task (legacy) |
| `ReviewAudioVideo` | Audio/video review task |
| `ExtractTraceWatermark` | Trace watermark extraction task |
| `ExtractCopyRightWatermark` | Copyright watermark extraction task |
| `QualityInspect` | Audio/video quality inspection task |
| `QualityEnhance` | Audio/video quality enhancement task |
| `ComplexAdaptiveDynamicStreaming` | Complex adaptive bitrate streaming task |
| `ProcessMediaByMPS` | MPS video processing task |
| `AigcImageTask` | AIGC image generation task |
| `SceneAigcImageTask` | Scene-based AIGC image generation task |
| `AigcVideoTask` | AIGC video generation task |
| `SceneAigcVideoTask` | Scene-based AIGC video generation task |
| `ImportMediaKnowledge` | Media knowledge import task |
| `ExtractBlindWatermark` | Digital watermark extraction task |
| `CreateAigcAdvancedCustomElement` | Create custom subject task |
| `CreateAigcCustomVoiceTask` | Create custom voice task |
| `CreateAigcSubjectTask` | Create subject task |

---

## Response Fields

### Top-Level Fields

| Field | Type | Description |
|------|------|------|
| `TaskId` | string | Task ID |
| `TaskType` | string | Task type (see supported task types table above) |
| `Status` | string | Task status: `WAITING` / `PROCESSING` / `FINISH` / `ABORTED` / `FAIL` / `SUCCESS` |
| `CreateTime` | string | Task creation time (ISO 8601 format) |
| `BeginProcessTime` | string | Task processing start time (ISO 8601 format) |
| `FinishTime` | string | Task completion time (ISO 8601 format) |
| `RequestId` | string | Request ID |

> Depending on `TaskType`, the response will also include the corresponding task detail fields (e.g., `ProcedureTask`, `PullUploadTask`, `AigcImageTask`, etc.). Use `--json` to view the full response structure.

---

## Usage Examples

### Basic Query

```bash
# Query task status and summary information
python scripts/vod_describe_task.py --task-id 1490013579-procedurev2-acd135

# Specify sub-application ID
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
    --sub-app-id 1500046806
```

**Output Example**:
```
=== Task Details ===
TaskId: 1490013579-procedurev2-acd135
Task Type: Video Processing (Procedure)
Task Status: Completed
CreateTime: 2024-03-01T10:00:00Z
Start Time: 2024-03-01T10:00:01Z
Finish Time: 2024-03-01T10:05:30Z
File ID: 5145403721233902989
Media Processing Sub-tasks: 1
  - Transcode: Success
```

### Wait for Task Completion

```bash
# Wait for task completion (default: up to 600 seconds, polling every 5 seconds)
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \


# Custom timeout and polling interval
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
 \
    --max-wait 300 \
    --interval 10
```

### Verbose Output

```bash
# Verbose mode: display output URLs, review suggestions, and other result information
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
    --verbose

# JSON format output of full API response (useful for script parsing)
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
    --json

# Wait for completion and output as JSON
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
 --json
```

### Typical Use Cases

```bash
# Case 1: Submit transcoding then query separately (suitable for long-running tasks)
TASK_ID=$(python scripts/vod_process_media.py transcode \
    --file-id 5145403721233902989 \
    --quality hd \
    --json | python3 -c "import sys,json; print(json.load(sys.stdin)['TaskId'])")

echo "Task submitted: $TASK_ID"
# Query later
python scripts/vod_describe_task.py --task-id "$TASK_ID" --verbose

# Case 2: Query pull upload task result
python scripts/vod_describe_task.py \
    --task-id 1490013579-pullupload-acd135 \
    --verbose

# Case 3: Query AIGC image generation task result
python scripts/vod_describe_task.py \
    --task-id 1490013579-aigcimagetask-acd135 \
    --verbose --json
```

> 💡 **Default behavior**: `vod_describe_task.py` automatically waits for task completion by default; submission scripts such as `vod_process_media.py` also wait by default. Add `--no-wait` to only query/submit without waiting.

---

## API Reference

| Feature | API | Documentation |
|------|---------|---------|
| Query task details | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |