# 图片背景融合/生成参数与示例 — `mps_image_bg_fusion.py`

**功能**：基于**主图（前景/商品/主体图）**与**背景图**，调用 MPS `ProcessImage` 接口发起 AI 背景融合任务，
或仅传入主图 + Prompt 描述，自动生成全新背景（背景生成模式）。
通过 `DescribeImageTaskDetail` 轮询等待结果，最终返回输出 COS 路径。

适用场景：电商商品图背景替换、广告素材背景生成、商品展示场景定制、营销创意图制作等。

---

## 两种使用模式

| 模式 | 是否传背景图 | `--prompt` 作用 | 典型场景 |
|------|------------|----------------|---------|
| **背景融合** | 是（`--bg-url` 或 `--bg-cos-key`） | 对融合结果的额外需求描述（如"将背景中的树叶替换为黄色"），可不传 | 商品图融合到指定场景 |
| **背景生成** | 否（不传背景图） | 生成背景的完整描述（如"简约白色大理石桌面，柔和自然光"），**必填** | 根据文字生成全新背景 |

---

## 参数说明

### 输入参数

| 参数 | 说明 |
|------|------|
| `--subject-url` | 主图（前景/商品/主体）URL（与 `--subject-cos-key` **二选一**） |
| `--subject-cos-key` | 主图 COS 对象 Key（如 `/input/product.jpg`），与 `--subject-url` 二选一 |
| `--subject-cos-bucket` | 主图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--subject-cos-region` | 主图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |
| `--bg-url` | 背景图 URL；不传则为背景生成模式（与 `--bg-cos-key` **二选一**） |
| `--bg-cos-key` | 背景图 COS 对象 Key（如 `/input/bg.jpg`），与 `--bg-url` 二选一 |
| `--bg-cos-bucket` | 背景图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--bg-cos-region` | 背景图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：主图必须指定 `--subject-url` 或 `--subject-cos-key` 之一；背景图可选，不传时为背景生成模式。

### 融合/生成参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt` | — | 背景描述或融合需求提示词，可重复传入多次；**背景生成模式下必填** |
| `--random-seed` | — | 随机种子，固定种子可获得稳定风格 |
| `--resource-id` | — | 可选资源 ID（业务侧专属资源） |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/bgfusion/` | 输出目录 |
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

1. **背景生成模式（不传背景图）下 `--prompt` 必填**，不传会报错退出。
2. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
3. 任务 `Status=FINISH` 不等于成功，需同时检查 `ErrMsg` 是否为空。
4. 脚本默认等待任务完成；若只需提交获取 TaskId，加 `--no-wait`。
5. 手动查询背景融合/生成任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。
6. 背景图只能传 **1 张**（`--bg-url` 或 `--bg-cos-key` 二选一，不支持多张背景图）。

---

## 示例命令

```bash
# 背景融合：主图 + 背景图（URL，等待结果）
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --bg-url "https://example.com/background.jpg"

# 背景融合 + 附加 Prompt（对融合结果的额外需求）
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --bg-url "https://example.com/background.jpg" \
    --prompt "将背景中的树叶替换为黄色"

# 背景生成：只有主图 + Prompt（无背景图）
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "简约白色大理石桌面，柔和自然光"

# 主图使用 COS 路径输入
python scripts/mps_image_bg_fusion.py \
    --subject-cos-key "/input/product.jpg" \
    --bg-url "https://example.com/background.jpg"

# 主图 + 背景图均使用 COS 路径输入（使用环境变量中的默认 Bucket）
python scripts/mps_image_bg_fusion.py \
    --subject-cos-key "/input/product.jpg" \
    --bg-cos-key "/input/background.jpg"

# 背景图 COS 输入，指定非默认 Bucket
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --bg-cos-key "/input/bg.jpg" \
    --bg-cos-bucket mybucket-125xxx --bg-cos-region ap-shanghai

# 背景生成 + 固定随机种子（可复现结果）
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "现代简约家居客厅背景" \
    --random-seed 42

# 指定输出格式和尺寸
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "户外草坪，阳光明媚" \
    --format PNG --image-size 4K

# 只提交任务，不等待结果（返回 TaskId）
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "简约白色大理石桌面" \
    --no-wait

# 手动查询背景融合/生成任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>

# 背景融合完成后下载结果到本地
# 第一步：执行背景融合任务（结果保存到 COS 输出路径）
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "简约白色大理石桌面"
# 第二步：从 COS 下载结果到本地文件
python scripts/mps_cos_download.py \
    --cos-input-key /output/bgfusion/result.jpeg \
    --local-file /tmp/bgfusion_result.jpg
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
      "path": "/output/bgfusion/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/bgfusion/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/bgfusion/result.jpeg"
    }
  ]
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交背景融合/生成任务，`ScheduleId=30060` |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
