# 多视角图片生成参数与示例 — `mps_image_multiview.py`

**功能**：调用 MPS `ProcessImage` 接口发起多视角图片生成任务，
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径或下载到本地。

适用场景：3D 商品展示、多角度产品预览、电商详情页素材生成、虚拟展厅等。

---

## 参数说明

### 输入参数

| 参数 | 说明 |
|------|------|
| `--url` | 输入图片 URL（与 `--cos-input-key`、`--local-file` **三选一**） |
| `--cos-input-key` | 输入图片 COS 对象 Key（如 `/input/product.jpg`） |
| `--local-file` | 本地图片路径（自动上传至 COS 后处理） |
| `--cos-input-bucket` | 输入 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--cos-input-region` | 输入 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：必须指定 `--url`、`--cos-input-key`、`--local-file` 之一作为输入源。

### 专项参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--horizontal-angle` | `0` | 水平旋转角度（int，范围 -180 ~ 180） |
| `--vertical-angle` | `0` | 垂直旋转角度（int，范围 -30 ~ 60） |
| `--zoom` | `medium` | 缩放级别：`wide`（远景）/ `medium`（中景）/ `close`（近景） |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/multiview/` | 输出目录 |
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

1. 多视角配置通过 `StdExtInfo.MultiViewConfig` 传入，`ScheduleId=30070`。
2. **水平角度范围限制**：`--horizontal-angle` 必须在 -180 ~ 180 之间，超出范围会报错。
3. **垂直角度范围限制**：`--vertical-angle` 必须在 -30 ~ 60 之间，超出范围会报错。
4. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
5. 手动查询多视角任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：默认参数（正面视角）
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg"

# 水平旋转 45 度
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle 45

# 俯视角度（垂直旋转 30 度）
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --vertical-angle 30

# 组合旋转 + 近景
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle -90 \
    --vertical-angle 15 \
    --zoom close

# 远景视角
python scripts/mps_image_multiview.py \
    --local-file /tmp/shoe.jpg \
    --horizontal-angle 180 \
    --zoom wide

# COS 路径输入
python scripts/mps_image_multiview.py \
    --cos-input-key "/input/bag.jpg" \
    --horizontal-angle 60

# 只提交任务，不等待结果
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle 45 \
    --no-wait

# 完成后下载到本地目录
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle 90 \
    --download-dir /tmp/results/

# 手动查询多视角任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-dEFG4567HI8901",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:10Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/multiview/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/multiview/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/multiview/result.jpeg"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交多视角生成任务，`ScheduleId=30070`，通过 `StdExtInfo.MultiViewConfig` 配置角度和缩放 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
