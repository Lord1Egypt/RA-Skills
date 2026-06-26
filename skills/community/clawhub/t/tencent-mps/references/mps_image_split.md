# 分镜拆图参数与示例 — `mps_image_split.py`

**功能**：调用 MPS `ProcessImage` 接口发起分镜拆图/宫格拆图任务，
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径或下载到本地。

适用场景：AI 剧分镜拆分、漫画宫格分割、电商长图拆分、故事板提取等。

---

## 参数说明

### 输入参数

| 参数 | 说明 |
|------|------|
| `--url` | 输入图片 URL（与 `--cos-input-key`、`--local-file` **三选一**） |
| `--cos-input-key` | 输入图片 COS 对象 Key（如 `/input/storyboard.jpg`） |
| `--local-file` | 本地图片路径（自动上传至 COS 后处理） |
| `--cos-input-bucket` | 输入 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--cos-input-region` | 输入 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：必须指定 `--url`、`--cos-input-key`、`--local-file` 之一作为输入源。

### 专项参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--process-index` | — | 指定处理第几帧（int，0-based），不传则处理所有帧 |
| `--erase-text` / `--no-erase-text` | 开启 | 是否擦除分镜中的文字（默认开启擦除） |
| `--model-sampling` | `0.1` | 模型采样参数（float）：`0.1`=AI 剧分镜，`1.0`=漫画分镜，`0.85`=电商保留文字 |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/split/` | 输出目录 |
| `--output-path` | — | 自定义输出路径（需带文件后缀） |

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--poll-interval` | 轮询间隔秒数（默认 10） |
| `--timeout` | 最长等待时间秒数（默认 300） |
| `--dry-run` | 预览 API 请求参数，不实际调用 |
| `--download-dir` | 任务完成后将结果下载到指定本地目录 |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，未设则为 `ap-guangzhou`） |

---

## 强制规则

1. 分镜配置通过 `StdExtInfo.StoryboardConfig` 传入，`ScheduleId=30050`。
2. **任务耗时较长**（约 127 秒），请确保 `--timeout` 设置足够大，或使用 `--no-wait`。
3. **电商场景建议**：使用 `--no-erase-text --model-sampling 0.85` 以保留文字内容。
4. `--model-sampling` 取值含义：`0.1` 适合 AI 剧分镜（擦文字），`1.0` 适合漫画分镜（保留线条），`0.85` 适合电商图（保留文字）。
5. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
6. 手动查询分镜任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：AI 剧分镜拆图（默认参数）
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg"

# 漫画分镜拆图
python scripts/mps_image_split.py \
    --url "https://example.com/manga_page.jpg" \
    --model-sampling 1.0

# 电商场景：保留文字
python scripts/mps_image_split.py \
    --url "https://example.com/product_long.jpg" \
    --no-erase-text \
    --model-sampling 0.85

# 只处理指定帧（第 0 帧）
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --process-index 0

# 本地文件输入
python scripts/mps_image_split.py \
    --local-file /tmp/comic.jpg \
    --model-sampling 1.0

# COS 路径输入
python scripts/mps_image_split.py \
    --cos-input-key "/input/drama_board.jpg"

# 不擦除文字
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --no-erase-text

# 只提交任务，不等待结果（推荐用于耗时长的任务）
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --no-wait

# 完成后下载到本地目录
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --download-dir /tmp/results/

# 手动查询分镜任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-gHIJ7890KL1234",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:02:07Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/split/frame_0.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/split/frame_0.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/split/frame_0.jpeg"
    },
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/split/frame_1.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/split/frame_1.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/split/frame_1.jpeg"
    },
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/split/frame_2.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/split/frame_2.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/split/frame_2.jpeg"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交分镜拆图任务，`ScheduleId=30050`，通过 `StdExtInfo.StoryboardConfig` 配置参数 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
