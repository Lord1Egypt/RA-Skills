# 图片换装参数与示例 — `mps_image_tryon.py`

**功能**：基于**模特图**与**服装图**，调用 MPS `ProcessImage` 接口发起 AI 换装任务，
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径。

适用场景：电商服饰试穿、商品展示图生成、广告创意素材生成、服装效果预览等。

---

## 参数说明

### 输入参数

| 参数 | 说明 |
|------|------|
| `--model-url` | 模特图 URL（与 `--model-cos-key` **二选一**） |
| `--model-cos-key` | 模特图 COS 对象 Key（如 `/input/model.jpg`），与 `--model-url` 二选一 |
| `--model-cos-bucket` | 模特图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--model-cos-region` | 模特图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |
| `--cloth-url` | 服装图 URL，可重复传入 1-2 次；与 `--cloth-cos-key` 可混用 |
| `--cloth-cos-key` | 服装图 COS 对象 Key，可重复传入 1-2 次；与 `--cloth-url` 可混用 |
| `--cloth-cos-bucket` | 服装图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--cloth-cos-region` | 服装图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：模特图必须指定 `--model-url` 或 `--model-cos-key` 之一；服装图必须至少指定一张（`--cloth-url` 或 `--cloth-cos-key`）。两者可混用，如模特图用 URL、服装图用 COS。

### 换装参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--schedule-id` | `30100` | 换装场景 ID：`30100`=普通衣物，`30101`=内衣 |
| `--ext-prompt` | — | 附加提示词，可重复传入多次（如 `"衬衫扣子打开"`） |
| `--random-seed` | — | 随机种子，固定种子可获得稳定风格 |
| `--resource-id` | — | 可选资源 ID（业务侧专属资源） |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/tryon/` | 输出目录 |
| `--output-path` | — | 自定义输出路径（需带文件后缀） |
| `--format` | `JPEG` | 输出格式：`JPEG` / `PNG` |
| `--image-size` | `2K` | 输出尺寸：`1K` / `2K` / `4K` |
| `--quality` | `85` | 输出质量 1-100 |

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--poll-interval` | 轮询间隔秒数（默认 10） |
| `--timeout` | 最长等待时间秒数（默认 600） |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，否则 `ap-guangzhou`） |

---

## 强制规则

1. **`--schedule-id 30101`（内衣场景）只能传 1 张服装图**，传入多张会报错退出。
2. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
3. 任务 `Status=FINISH` 不等于成功，需同时检查 `ErrMsg` 是否为空。
4. 脚本默认等待任务完成；若只需提交获取 TaskId，加 `--no-wait`。
5. 手动查询换装任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：模特图 + 1 张服装图（URL，等待结果）
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# 模特图使用 COS 路径输入
python scripts/mps_image_tryon.py \
    --model-cos-key "/input/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# 模特图 + 服装图均使用 COS 路径输入（使用环境变量中的默认 Bucket）
python scripts/mps_image_tryon.py \
    --model-cos-key "/input/model.jpg" \
    --cloth-cos-key "/input/cloth.jpg"

# 服装图使用 COS，指定非默认 Bucket
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-cos-key "/input/cloth.jpg" \
    --cloth-cos-bucket mybucket-125xxx --cloth-cos-region ap-shanghai

# 多张服装图（正面 + 背面，提升换装质量）
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth-front.jpg" \
    --cloth-url "https://example.com/cloth-back.jpg"

# 内衣场景（只支持 1 张服装图）
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/underwear.jpg" \
    --schedule-id 30101

# 附加提示词 + 固定随机种子
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --ext-prompt "衬衫扣子打开" \
    --random-seed 48

# 指定输出格式和尺寸
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --format PNG --image-size 4K

# 只提交任务，不等待结果（返回 TaskId）
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --no-wait

# 手动查询换装任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>

# 换装完成后下载结果到本地
# 第一步：执行换装任务（结果保存到 COS 输出路径）
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"
# 第二步：从 COS 下载结果到本地文件
python scripts/mps_cos_download.py \
    --cos-input-key /output/tryon/result.jpeg \
    --local-file /tmp/tryon_result.jpg
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-b8dac8f326214464acef88afef9002d4",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T01:02:51Z",
  "FinishTime": "2025-05-21T01:02:52Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/tryon/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/tryon/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/tryon/result.jpeg"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交换装任务，`ScheduleId=30100`（普通衣物）或 `30101`（内衣） |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
