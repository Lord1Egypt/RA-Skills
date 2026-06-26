# 目标检测与物体描述参数与示例 — `mps_image_detect.py`

**功能**：调用 MPS 图片任务接口发起目标检测与物体描述任务，
通过 `DescribeImageTaskDetail` 轮询等待结果，返回检测数据（边界框、描述、可选抠图）。

适用场景：商品定位、图片中物体识别与描述、自动标注、目标裁剪提取等。

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
| `--prompt` | — | 检测目标描述（可多次传入），与 `--point` 至少指定一个 |
| `--point` | — | 点选坐标 `"X,Y"`（可多次传入），与 `--prompt` 至少指定一个 |
| `--top-k` | `1` | 每个 prompt/point 返回的最大检测数量（1-20） |
| `--confidence-threshold` | `0.5` | 置信度阈值（0-1），低于此值的结果被过滤 |
| `--describe` | — | 启用物体描述（为每个检测结果生成文字描述） |
| `--return-cutout` | — | 启用抠图返回（为每个检测结果输出单独的抠图文件） |
| `--prompt-language` | — | 提示词语言：`zh`（中文）/ `en`（英文） |
| `--description-language` | — | 描述输出语言：`zh`（中文）/ `en`（英文） |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/object-detect/` | 输出目录 |
| `--output-path` | — | 自定义输出路径（需带文件后缀） |

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--poll-interval` | 轮询间隔秒数（默认 5） |
| `--timeout` | 最长等待时间秒数（默认 300） |
| `--dry-run` | 预览 API 请求参数，不实际调用 |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，未设则为 `ap-guangzhou`） |

---

## 强制规则

1. **`--prompt` 和 `--point` 至少指定一个**，两者都不传会报错退出。
2. 检测配置通过 `StdExtInfo.ObjectDetectDescribeConfig` 传入（无固定 ScheduleId，使用 ImageTask 方式）。
3. **输出 JSON 包含 Detections 数组**，每项包含边界框坐标、置信度、描述（若开启）和抠图路径（若开启）。
4. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
5. 手动查询检测任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：文本 prompt 检测
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "猫"

# 多目标检测（多个 prompt）
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "猫" \
    --prompt "狗"

# 点选检测
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --point "320,240"

# 多点选
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --point "100,200" \
    --point "500,300"

# 增加返回数量，降低置信度阈值
python scripts/mps_image_detect.py \
    --url "https://example.com/crowd.jpg" \
    --prompt "人" \
    --top-k 10 \
    --confidence-threshold 0.3

# 启用物体描述
python scripts/mps_image_detect.py \
    --url "https://example.com/product.jpg" \
    --prompt "商品" \
    --describe \
    --description-language zh

# 启用抠图返回
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "汽车" \
    --return-cutout

# 本地文件 + 完整参数
python scripts/mps_image_detect.py \
    --local-file /tmp/photo.jpg \
    --prompt "人脸" \
    --top-k 5 \
    --describe \
    --return-cutout \
    --prompt-language zh \
    --description-language zh

# 只提交任务，不等待结果
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "猫" \
    --no-wait

# 手动查询检测任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-eFGH5678IJ9012",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:06Z",
  "Detections": [
    {
      "Label": "猫",
      "Confidence": 0.92,
      "BoundingBox": {
        "X": 120,
        "Y": 80,
        "Width": 200,
        "Height": 180
      },
      "Description": "一只橘色的猫咪正趴在沙发上休息",
      "CutoutPath": "/output/object-detect/cutout_0.png"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交目标检测任务，通过 `StdExtInfo.ObjectDetectDescribeConfig` 配置参数 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
