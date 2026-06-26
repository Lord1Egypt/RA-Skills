# 图片扩图参数与示例 — `mps_image_padding.py`

**功能**：调用 MPS `ProcessImage` 接口发起图片扩图/画布扩展任务，
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径或下载到本地。

适用场景：电商主图扩展、社交媒体封面适配、横竖屏转换、海报画布扩展等。

---

## 参数说明

### 输入参数

| 参数 | 说明 |
|------|------|
| `--url` | 输入图片 URL（与 `--cos-input-key`、`--local-file` **三选一**） |
| `--cos-input-key` | 输入图片 COS 对象 Key（如 `/input/photo.jpg`） |
| `--local-file` | 本地图片路径（自动上传至 COS 后处理） |
| `--cos-input-bucket` | 输入 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--cos-input-region` | 输入 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：必须指定 `--url`、`--cos-input-key`、`--local-file` 之一作为输入源。

### 专项参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--aspect-ratio` | — | 目标宽高比（str，如 `"16:9"`、`"1:1"`、`"9:16"`） |
| `--image-width` | — | 目标宽度（int，像素） |
| `--image-height` | — | 目标高度（int，像素） |

> **说明**：`--aspect-ratio`、`--image-width`、`--image-height` 至少指定一个。

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/padding/` | 输出目录 |
| `--output-path` | — | 自定义输出路径（需带文件后缀） |

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--poll-interval` | 轮询间隔秒数（默认 10） |
| `--timeout` | 最长等待时间秒数（默认 600） |
| `--dry-run` | 预览 API 请求参数，不实际调用 |
| `--download-dir` | 任务完成后将结果下载到指定本地目录 |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，未设则为 `ap-guangzhou`） |

---

## 强制规则

1. **至少指定一个扩图参数**：`--aspect-ratio`、`--image-width`、`--image-height` 不能全部为空。
2. **建议输出尺寸在 1K 级别**（如 1024×1024），不推荐 2K+ 以上分辨率，可能导致生成质量下降或超时。
3. 扩图配置通过 `AddOnParameter.OutputConfig` 传入，`ScheduleId=30010`。
4. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
5. 手动查询扩图任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：按宽高比扩展为 16:9
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --aspect-ratio "16:9"

# 竖屏转横屏
python scripts/mps_image_padding.py \
    --url "https://example.com/vertical.jpg" \
    --aspect-ratio "16:9"

# 指定目标宽高（像素）
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --image-width 1920 --image-height 1080

# 只指定目标宽度
python scripts/mps_image_padding.py \
    --local-file /tmp/product.jpg \
    --image-width 1024

# 本地文件输入，正方形画布
python scripts/mps_image_padding.py \
    --local-file /tmp/product.jpg \
    --aspect-ratio "1:1"

# COS 路径输入
python scripts/mps_image_padding.py \
    --cos-input-key "/input/banner.jpg" \
    --aspect-ratio "21:9"

# 只提交任务，不等待结果
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --aspect-ratio "16:9" \
    --no-wait

# 完成后下载到本地目录
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --aspect-ratio "16:9" \
    --download-dir /tmp/results/

# 手动查询扩图任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-bCDE2345FG6789",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:15Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/padding/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/padding/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/padding/result.jpeg"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交扩图任务，`ScheduleId=30010`，通过 `AddOnParameter.OutputConfig` 配置目标尺寸 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
