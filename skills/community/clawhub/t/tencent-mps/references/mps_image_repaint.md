# 图片局部重绘参数与示例 — `mps_image_repaint.py`

**功能**：调用 MPS `ProcessImage` 接口发起图片局部重绘（Inpainting）任务，
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径或下载到本地。

适用场景：商品图局部修改、广告素材修图、去除瑕疵并重绘、场景替换、创意编辑等。

---

## 参数说明

### 输入参数（原图）

| 参数 | 说明 |
|------|------|
| `--url` | 原图 URL（与 `--cos-input-key`、`--local-file` **三选一**） |
| `--cos-input-key` | 原图 COS 对象 Key（如 `/input/photo.jpg`） |
| `--local-file` | 本地原图路径（自动上传至 COS 后处理） |
| `--cos-input-bucket` | 输入 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--cos-input-region` | 输入 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

### 输入参数（遮罩图）

| 参数 | 说明 |
|------|------|
| `--mask-url` | 遮罩图 URL（与 `--mask-cos-key` **二选一**，必填） |
| `--mask-cos-key` | 遮罩图 COS 对象 Key（与 `--mask-url` 二选一，必填） |
| `--mask-cos-bucket` | 遮罩图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--mask-cos-region` | 遮罩图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：原图必须指定 `--url`、`--cos-input-key`、`--local-file` 之一；遮罩图必须指定 `--mask-url` 或 `--mask-cos-key` 之一。

### 专项参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt` | —（**必填**） | 编辑指令，描述重绘区域应生成的内容（如 `"蓝色天空"` 或 `"一朵红色玫瑰"`） |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/repaint/` | 输出目录 |
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

1. **遮罩图必须是 RGBA 格式（带 Alpha 通道）**，Alpha 通道标记需要重绘的区域（Alpha=255 表示重绘，Alpha=0 表示保留）。
2. **`--prompt` 必填**，描述重绘区域应生成的内容，不传会报错退出。
3. 遮罩图在 `AddOnParameter` 中通过 `ImageSet` 传入，其 `Type` 为 `"mask"`。
4. `ScheduleId=30061`。
5. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
6. 手动查询重绘任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：URL 原图 + URL 遮罩图
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "蓝色天空和白云"

# 本地原图 + URL 遮罩图
python scripts/mps_image_repaint.py \
    --local-file /tmp/room.jpg \
    --mask-url "https://example.com/mask.png" \
    --prompt "一盆绿色植物"

# COS 原图 + COS 遮罩图
python scripts/mps_image_repaint.py \
    --cos-input-key "/input/scene.jpg" \
    --mask-cos-key "/input/mask.png" \
    --prompt "一只白色的猫"

# 遮罩图使用非默认 Bucket
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-cos-key "/masks/area.png" \
    --mask-cos-bucket mybucket-125xxx \
    --mask-cos-region ap-shanghai \
    --prompt "红色花朵"

# 自定义输出路径
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "木质地板" \
    --output-path "/output/repaint/custom_result.jpg"

# 只提交任务，不等待结果
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "绿色草地" \
    --no-wait

# 完成后下载到本地目录
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "大理石纹理" \
    --download-dir /tmp/results/

# 手动查询重绘任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-fGHI6789JK0123",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:12Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/repaint/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/repaint/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/repaint/result.jpeg"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交局部重绘任务，`ScheduleId=30061`，遮罩通过 `AddOnParameter.ImageSet`（Type="mask"）传入 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
