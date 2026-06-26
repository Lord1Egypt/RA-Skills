# 图片理解参数与示例 — `mps_image_comprehend.py`

**功能**：调用 MPS `ProcessImage` 接口发起图片理解/OCR/看图问答任务（Gemini 系列模型），
通过 `DescribeImageTaskDetail` 轮询等待结果，返回文本内容（Content）。

适用场景：图片内容描述、OCR 文字识别、图片问答、商品信息提取、文档理解等。

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
| `--prompt` | —（**必填**） | 提问/指令内容，如 `"描述图片内容"` 或 `"提取图中所有文字"` |
| `--model-name` | `Google/gemini-2.5-flash` | 模型名称（与 `--definition` 互斥） |
| `--definition` | — | 模型预设 ID（与 `--model-name` 互斥），见下方映射表 |
| `--temperature` | — | 采样温度，控制输出随机性 |
| `--top-p` | — | Top-P 采样参数 |
| `--top-k` | — | Top-K 采样参数 |

**DEFINITION_MAP（`--definition` 取值）**：

| 值 | 对应模型 |
|------|------|
| `10000` | gemini-flash-lite |
| `10001` | gemini-flash |
| `10002` | gemini-flash-pro |
| `10003` | gemini-3-flash |
| `10004` | gemini-3-pro |

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/comprehend/` | 输出目录（若有文件输出时使用） |

> **说明**：图片理解任务返回的是文本 Content，而非图片文件。

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--poll-interval` | 轮询间隔秒数（默认 10） |
| `--timeout` | 最长等待时间秒数（默认 600） |
| `--dry-run` | 预览 API 请求参数，不实际调用 |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，未设则为 `ap-guangzhou`） |

---

## 强制规则

1. **`--prompt` 必填**，不传会报错退出。
2. **`--definition` 和 `--model-name` 互斥**，不能同时指定；若都不传则默认使用 `Google/gemini-2.5-flash`。
3. `ScheduleId=30200`，输出为文本 Content 而非图片文件。
4. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
5. 手动查询理解任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。

---

## 示例命令

```bash
# 最简用法：描述图片内容
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "描述这张图片的内容"

# OCR 文字提取
python scripts/mps_image_comprehend.py \
    --url "https://example.com/document.jpg" \
    --prompt "提取图片中所有文字"

# 图片问答
python scripts/mps_image_comprehend.py \
    --local-file /tmp/product.jpg \
    --prompt "这个商品的品牌和价格是什么？"

# 使用 definition 指定模型
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "描述图片内容" \
    --definition 10004

# 指定模型名称
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "描述图片内容" \
    --model-name "Google/gemini-2.5-flash"

# 调整采样参数
python scripts/mps_image_comprehend.py \
    --url "https://example.com/creative.jpg" \
    --prompt "用诗意的语言描述这张图" \
    --temperature 0.8 --top-p 0.9

# COS 路径输入
python scripts/mps_image_comprehend.py \
    --cos-input-key "/input/receipt.jpg" \
    --prompt "提取这张发票上的金额和日期"

# 只提交任务，不等待结果
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "描述图片内容" \
    --no-wait

# 手动查询理解任务状态
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-cDEF3456GH7890",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:12Z",
  "Content": "这张图片展示了一只橘色的猫咪躺在阳光下的窗台上，背景是一片绿色的花园。猫咪的眼睛半闭，看起来非常放松和惬意。"
}
```

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交图片理解任务，`ScheduleId=30200`，通过 Prompt 和模型参数配置 |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
