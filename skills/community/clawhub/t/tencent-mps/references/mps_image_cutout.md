# 精准抠图参数与示例 — `mps_image_cutout.py`

**功能**：调用 MPS `ProcessImage` 接口发起精准抠图任务，输出透明背景 PNG 图片，
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径或下载到本地。

适用场景：商品抠图、人像抠图、证件照背景去除、素材制作、电商合成图制作等。

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
| `--transparency-threshold` | `30` | 透明度阈值（int），低于此值的像素视为透明 |
| `--opaque-threshold` | `127` | 不透明阈值（int），高于此值的像素视为不透明 |
| `--edge-sampling-step` | `5` | 边缘采样步长（int），值越小边缘越精细但计算越慢 |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/cutout/` | 输出目录 |
| `--output-path` | — | 自定义输出路径（需带文件后缀） |

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--poll-interval` | 轮询间隔秒数（默认 5） |
| `--timeout` | 最长等待时间秒数（默认 300） |
| `--dry-run` | 预览 API 请求参数，不实际调用 |
| `--download-dir` | 任务完成后将结果下载到指定本地目录 |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，未设则为 `ap-guangzhou`） |

---

## 强制规则

1. **输出为透明背景 PNG 格式**，不支持 JPEG 等非透明格式输出。
2. 抠图配置通过 `StdExtInfo.CutoutConfig` 传入，`ScheduleId=30030`。
3. **边缘较细的物体**（如头发丝、树叶缝隙）建议降低 `--edge-sampling-step`（如设为 2-3）以获得更精细的边缘效果。
4. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
5. 手动查询抠图任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：URL 输入，等待结果
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg"

# 本地文件输入
python scripts/mps_image_cutout.py \
    --local-file /tmp/photo.jpg

# COS 路径输入
python scripts/mps_image_cutout.py \
    --cos-input-key "/input/model.jpg"

# 精细边缘抠图（适合头发丝等细节）
python scripts/mps_image_cutout.py \
    --url "https://example.com/portrait.jpg" \
    --edge-sampling-step 2

# 调整透明度阈值
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg" \
    --transparency-threshold 20 \
    --opaque-threshold 150

# 只提交任务，不等待结果
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg" \
    --no-wait

# 完成后下载到本地目录
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg" \
    --download-dir /tmp/results/

# 手动查询抠图任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-aBCD1234EF5678",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:05Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/cutout/result.png",
      "cos_uri": "cos://mps-bucket-125xxx/output/cutout/result.png",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/cutout/result.png"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交抠图任务，`ScheduleId=30030`，通过 `StdExtInfo.CutoutConfig` 配置参数 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
