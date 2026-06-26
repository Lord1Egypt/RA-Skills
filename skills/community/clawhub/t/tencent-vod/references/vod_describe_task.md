# vod_describe_task — 详细参数与示例

> 此文件对应脚本：`scripts/vod_describe_task.py`
>
> 通过任务 ID 查询 VOD 异步任务的执行状态和结果详情（支持最近 3 天内提交的任务）。

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--task-id` | string | ✅ | 任务 ID（如 `1490013579-procedurev2-acd135`） |
| `--sub-app-id` | int | - | VOD 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | - | 仅查询当前状态，不等待完成（默认自动等待） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 600） |
| `--interval` | int | - | 轮询间隔（秒，默认 5） |
| `--json` | flag | - | JSON 格式输出完整 API 响应 |
| `--verbose` / `-v` | flag | - | 输出详细信息（含输出 URL 等） |

**任务状态说明**：

| 状态 | 含义 |
|------|------|
| `WAITING` | 等待中，尚未开始处理 |
| `PROCESSING` | 处理中 |
| `FINISH` | 已完成（成功） |
| `ABORTED` | 已终止（失败或被取消） |
| `FAIL` | 失败（子任务级别状态） |
| `SUCCESS` | 成功（子任务级别状态） |

---

## 支持的任务类型

| TaskType | 中文说明 |
|----------|---------|
| `Procedure` | 视频处理任务 |
| `EditMedia` | 视频编辑任务 |
| `SplitMedia` | 视频拆条任务 |
| `ComposeMedia` | 制作媒体文件任务 |
| `WechatPublish` | 微信发布任务 |
| `WechatMiniProgramPublish` | 微信小程序发布任务 |
| `PullUpload` | 拉取上传任务 |
| `FastClipMedia` | 快速剪辑任务（暂无详细解析，建议使用 `--json` 查看完整响应） |
| `RemoveWatermarkTask` | 智能去除水印任务 |
| `DescribeFileAttributesTask` | 获取文件属性任务 |
| `RebuildMedia` | 音画质重生任务（旧） |
| `ReviewAudioVideo` | 音视频审核任务 |
| `ExtractTraceWatermark` | 提取溯源水印任务 |
| `ExtractCopyRightWatermark` | 提取版权水印任务 |
| `QualityInspect` | 音画质检测任务 |
| `QualityEnhance` | 音画质重生任务 |
| `ComplexAdaptiveDynamicStreaming` | 复杂自适应码流任务 |
| `ProcessMediaByMPS` | MPS 视频处理任务 |
| `AigcImageTask` | AIGC 生图任务 |
| `SceneAigcImageTask` | 场景化 AIGC 生图任务 |
| `AigcVideoTask` | AIGC 生视频任务 |
| `SceneAigcVideoTask` | 场景化 AIGC 生视频任务 |
| `ImportMediaKnowledge` | 导入媒体知识任务 |
| `ExtractBlindWatermark` | 提取数字水印任务 |
| `CreateAigcAdvancedCustomElement` | 创建自定义主体任务 |
| `CreateAigcCustomVoiceTask` | 创建自定义音色任务 |
| `CreateAigcSubjectTask` | 创建主体任务 |

---

## 响应字段说明

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `TaskId` | string | 任务 ID |
| `TaskType` | string | 任务类型（见上方支持的任务类型表） |
| `Status` | string | 任务状态：`WAITING` / `PROCESSING` / `FINISH` / `ABORTED` / `FAIL` / `SUCCESS` |
| `CreateTime` | string | 任务创建时间（ISO 8601 格式） |
| `BeginProcessTime` | string | 任务开始处理时间（ISO 8601 格式） |
| `FinishTime` | string | 任务完成时间（ISO 8601 格式） |
| `RequestId` | string | 请求 ID |

> 根据 `TaskType` 不同，响应中还会包含对应的任务详情字段（如 `ProcedureTask`、`PullUploadTask`、`AigcImageTask` 等），使用 `--json` 可查看完整响应结构。

---

## 使用示例

### 基础查询

```bash
# 查询任务状态和摘要信息
python scripts/vod_describe_task.py --task-id 1490013579-procedurev2-acd135

# 指定子应用 ID
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
    --sub-app-id 1500046806
```

**输出示例**：
```
=== 任务详情 ===
TaskId: 1490013579-procedurev2-acd135
任务类型: 视频处理 (Procedure)
任务状态: 已完成
创建时间: 2024-03-01T10:00:00Z
开始时间: 2024-03-01T10:00:01Z
完成时间: 2024-03-01T10:05:30Z
文件 ID: 5145403721233902989
媒体处理子任务: 1 个
  - Transcode: 成功
```

### 等待任务完成

```bash
# 等待任务完成（默认最多等 600 秒，每 5 秒轮询一次）
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \


# 自定义超时和轮询间隔
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
 \
    --max-wait 300 \
    --interval 10
```

### 详细输出

```bash
# 详细模式：显示输出 URL、审核建议等结果信息
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
    --verbose

# JSON 格式输出完整 API 响应（便于脚本解析）
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
    --json

# 等待完成并以 JSON 输出
python scripts/vod_describe_task.py \
    --task-id 1490013579-procedurev2-acd135 \
 --json
```

### 典型使用场景

```bash
# 场景1：提交转码后分离查询（适合长时间任务）
TASK_ID=$(python scripts/vod_process_media.py transcode \
    --file-id 5145403721233902989 \
    --quality hd \
    --json | python3 -c "import sys,json; print(json.load(sys.stdin)['TaskId'])")

echo "任务已提交: $TASK_ID"
# 稍后查询
python scripts/vod_describe_task.py --task-id "$TASK_ID" --verbose

# 场景2：查询拉取上传任务结果
python scripts/vod_describe_task.py \
    --task-id 1490013579-pullupload-acd135 \
    --verbose

# 场景3：查询 AIGC 生图任务结果
python scripts/vod_describe_task.py \
    --task-id 1490013579-aigcimagetask-acd135 \
    --verbose --json
```

> 💡 **默认行为**：`vod_describe_task.py` 默认会自动等待任务完成；`vod_process_media.py` 等提交类脚本也默认等待。加 `--no-wait` 可仅查询/提交而不等待。

---

## API 接口

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 查询任务详情 | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |
