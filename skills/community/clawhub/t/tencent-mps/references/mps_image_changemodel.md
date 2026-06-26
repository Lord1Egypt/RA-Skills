# 换模特参数与示例 — `mps_image_changemodel.py`

**功能**：基于**模特原图**与**衣物图**，调用 MPS `ProcessImage` 接口发起换模特/换体型任务，
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径或下载到本地。

适用场景：电商模特更换、不同体型展示、服装跨体型试穿效果、广告素材定制等。

---

## 参数说明

### 输入参数（原图）

| 参数 | 说明 |
|------|------|
| `--url` | 原图 URL（与 `--cos-input-key`、`--local-file` **三选一**） |
| `--cos-input-key` | 原图 COS 对象 Key（如 `/input/model.jpg`） |
| `--cos-input-bucket` | 原图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--cos-input-region` | 原图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |
| `--local-file` | 本地原图路径（自动上传至 COS 后处理） |

### 输入参数（衣物图）

| 参数 | 说明 |
|------|------|
| `--garment-url` | 衣物图 URL（与 `--garment-cos-key` **二选一**，必填） |
| `--garment-cos-key` | 衣物图 COS 对象 Key（与 `--garment-url` 二选一，必填） |
| `--garment-cos-bucket` | 衣物图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--garment-cos-region` | 衣物图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：原图必须指定 `--url`、`--cos-input-key`、`--local-file` 之一；衣物图必须指定 `--garment-url` 或 `--garment-cos-key` 之一。

### 专项参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--body-shape` | `hourglass` | 目标体型：`hourglass`（沙漏型）/ `rectangle`（矩形）/ `plus-size`（大码）/ `apple`（苹果型）/ `pear`（梨型） |
| `--precision-scale` | `1.0` | 精度系数（float，0.01-2.0），值越大精度越高但耗时越长 |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/changemodel/` | 输出目录 |
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

1. **衣物图必填**：必须指定 `--garment-url` 或 `--garment-cos-key` 之一，否则报错退出。
2. 换模特配置通过 `StdExtInfo.ChangeGarmentModelConfig` 传入，衣物图通过 `AddOnParameter.ImageSet`（Type="garment"）传入，`ScheduleId=30110`。
3. **`--precision-scale` 越大精度越高但处理越慢**：默认 1.0 适合大多数场景；对细节要求极高时可调到 1.5-2.0，但耗时可能翻倍。
4. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
5. 手动查询换模特任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：URL 原图 + URL 衣物图（默认沙漏型体型）
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg"

# 指定体型为梨型
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --body-shape pear

# 大码体型
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/coat.jpg" \
    --body-shape plus-size

# 提高精度（适合细节要求高的场景）
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --precision-scale 1.5

# 本地原图 + COS 衣物图
python scripts/mps_image_changemodel.py \
    --local-file /tmp/model.jpg \
    --garment-cos-key "/input/garment.jpg"

# COS 原图 + COS 衣物图
python scripts/mps_image_changemodel.py \
    --cos-input-key "/input/model.jpg" \
    --garment-cos-key "/input/garment.jpg"

# 衣物图使用非默认 Bucket
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-cos-key "/clothes/summer_dress.jpg" \
    --garment-cos-bucket mybucket-125xxx \
    --garment-cos-region ap-shanghai

# 只提交任务，不等待结果
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --no-wait

# 完成后下载到本地目录
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --download-dir /tmp/results/

# 手动查询换模特任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-hIJK8901LM2345",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:18Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/changemodel/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/changemodel/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/changemodel/result.jpeg"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交换模特任务，`ScheduleId=30110`，通过 `StdExtInfo.ChangeGarmentModelConfig` + `AddOnParameter.ImageSet`（Type="garment"）配置 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
