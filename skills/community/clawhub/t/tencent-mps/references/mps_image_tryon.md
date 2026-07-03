# 图片换装参数与示例 — `mps_image_tryon.py`

**功能**：基于**模特图**与**服装图**，调用 MPS `ProcessImage` 接口发起 AI 换装任务（`ImageTask.AiTryOnConfig`），
通过 `DescribeImageTaskDetail` 轮询等待结果，返回输出路径或预签名下载链接。

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
| `--cloth-url` | 服装图 URL，可重复传入 1-4 次；与 `--cloth-cos-key` 可混用 |
| `--cloth-cos-key` | 服装图 COS 对象 Key，可重复传入 1-4 次；与 `--cloth-url` 可混用 |
| `--cloth-cos-bucket` | 服装图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--cloth-cos-region` | 服装图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：模特图必须指定 `--model-url` 或 `--model-cos-key` 之一；服装图 1-4 张（`--cloth-url` 或 `--cloth-cos-key`）。两者可混用，如模特图用 URL、服装图用 COS。

### 换装参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--model` | `WAND-tryon-1.0-flash` | 换装模型：`WAND-tryon-1.0-lite`（轻量）/ `WAND-tryon-1.0-flash`（快速）/ `WAND-tryon-1.0-pro`（专业） |
| `--prompt` | — | 换装指令（可选，为空时使用内置默认指令） |
| `--resource-id` | — | 可选资源 ID（业务侧专属资源） |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--resolution` | `1K` | 输出分辨率：`1K` / `2K` / `4K` |
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/tryon/` | 输出目录 |
| `--output-path` | — | 自定义输出路径（需带文件后缀） |

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--dry-run` | 仅打印请求参数，不实际调用 API |
| `--poll-interval` | 轮询间隔秒数（默认 10） |
| `--timeout` | 最长等待时间秒数（默认 600） |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，否则 `ap-guangzhou`） |

---

## 强制规则

1. **服装图 1-4 张**，超过 4 张会报错退出。
2. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
3. 任务 `Status=FINISH` 不等于成功，需同时检查 `ErrMsg` 是否为空。
4. 脚本默认等待任务完成；若只需提交获取 TaskId，加 `--no-wait`。
5. 手动查询换装任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。
6. 新 API 使用 `ImageTask.AiTryOnConfig`，不再使用 `ScheduleId` 区分场景。

---

## 示例命令

```bash
# 最简用法：模特图 + 1 张服装图（URL，默认 COS 输出）
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# 指定模型
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --model WAND-tryon-1.0-pro

# 模特图使用 COS 路径输入
python3 scripts/mps_image_tryon.py \
    --model-cos-key "/input/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# 多张服装图（1-4 张）
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth-front.jpg" \
    --cloth-url "https://example.com/cloth-back.jpg"

# 附加提示词
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --prompt "将衬衫换为红色"

# 指定分辨率 + 模型
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --model WAND-tryon-1.0-pro --resolution 4K

# 只提交任务，不等待结果
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --no-wait

# 指定 COS 输出 Bucket 和目录
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --output-bucket mybucket-125xxx --output-region ap-shanghai \
    --output-dir /custom/output/

# 预览请求参数（不实际提交）
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --dry-run

# 手动查询换装任务状态
python3 scripts/mps_get_image_task.py --task-id <TaskId>
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
| `ProcessImage` | 提交 AI 换装任务，`ImageTask.AiTryOnConfig` |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
- [AiTryOnConfig 参数说明](https://cloud.tencent.com/document/api/862/37615#AiTryOnConfig)
