# 擦除/去水印参数与示例 — `mps_erase.py`

**功能**：去字幕、擦除水印、人脸模糊、车牌模糊等画面视觉元素擦除/遮挡。
> ⚠️ 职责是**擦除/遮挡画面视觉元素**，不涉及画质检测。画质检测请用 `mps_qualitycontrol.py`。

## 预设模板

| 模板 ID | 说明 |
|---------|------|
| `101` | 去字幕（默认）|
| `102` | 去字幕 + OCR 提取 |
| `201` | 去水印高级版 |
| `301` | 人脸模糊 |
| `302` | 人脸 + 车牌模糊 |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL 地址 |
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-region`/`--cos-input-key` 配合，推荐）|
| `--cos-input-region` | 输入 COS Bucket 区域（如 `ap-guangzhou`）|
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`，**推荐**）|
| `--template` | 模板 ID（优先级高于自定义参数）|
| `--method` | 擦除方式：`auto`（自动）/ `custom`（自定义区域）|
| `--model` | 擦除模型：`standard`（标准）/ `area`（区域，适合花体/阴影字幕）|
| `--position` | 预设位置：`fullscreen` / `top-half` / `bottom-half` / `center` / `left` / `right` |
| `--area` | 自动擦除区域（百分比坐标 `X1,Y1,X2,Y2`，0-1），可多次指定 |
| `--custom-area` | 自定义区域（`BEGIN,END,X1,Y1,X2,Y2`）|
| `--ocr` | 开启 OCR 字幕提取（布尔 flag，直接写 `--ocr`，**不是** `--type ocr`）|
| `--subtitle-lang` | 字幕语言：`zh_en`（中英，默认）/ `multi`（多语种）|
| `--subtitle-format` | 字幕文件格式：`vtt`（默认）/ `srt` |
| `--translate` | 字幕翻译目标语言（需同时具备 OCR 能力：使用 `--template 102` 或 `--ocr` 开启）。支持：`zh`、`en`、`ja`、`ko`、`fr`、`es`、`it`、`de`、`tr`、`ru`、`pt`、`vi`、`id`、`ms`、`th`、`ar`、`hi` 共 17 种 |
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量）|
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量）|
| `--output-dir` | 输出目录，默认 `/output/erase/` |
| `--output-object-path` | 输出文件路径，如 `/output/{inputName}_erase.{format}` |
| `--no-wait` | 仅提交任务，不等待结果（默认自动轮询）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800（30 分钟）|
| `--download-dir` | 任务完成后将输出文件下载到指定本地目录（默认仅打印预签名 URL）|
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--notify-url` | 任务完成回调 URL（可选）|
| `--dry-run` | 只打印参数，不调用 API |

## 区域预设（--position）说明

| 预设值 | 说明 | 坐标范围 |
|--------|------|----------|
| `fullscreen` | 全屏幕 | (0,0)-(0.9999,0.9999) |
| `top-half` | 上半屏幕 | (0,0)-(0.9999,0.5) |
| `bottom-half` | 下半屏幕 | (0,0.5)-(0.9999,0.9999) |
| `center` | 屏幕中间 | (0.1,0.3)-(0.9,0.7) |
| `left` | 屏幕左边 | (0,0)-(0.5,0.9999) |
| `right` | 屏幕右边 | (0.5,0)-(0.9999,0.9999) |

## 强制规则

> ⚠️ **优先级说明**：以下规则按优先级从高到低排列，遇到多条规则同时匹配时，**优先使用编号更靠前的规则**。

- **`mps_erase.py` 没有 `--type` 参数**：绝对禁止生成 `--type ocr` / `--type watermark` 等写法；OCR 功能用 `--ocr`（flag）或 `--template 102` 开启，不是 `--type` 参数。
- **【最高优先 - 判断入口】先判断用户是否同时需要"去字幕" AND "提取字幕文本/OCR/识别字幕"**：
  - ✅ 是 → **必须且只能用 `--template 102`**，命令中**绝对禁止**出现 `--template 101` 或 `--ocr` 参数（`--template 102` 已内置 OCR 功能，无需额外加 `--ocr`）
  - ✅ 否（只去字幕，不提取文本）→ 使用 `--template 101`，禁止省略
- **去字幕场景（仅去字幕，不提取文本）必须显式加 `--template 101`**，禁止省略（即使它是默认值，也必须在命令中写出）
- **人脸模糊场景必须加 `--template 301`**
- **人脸 + 车牌模糊场景必须加 `--template 302`**
- **去水印高级版必须加 `--template 201`**

## 示例命令

```bash
# 自动擦除中下部字幕（模板 101，必须显式指定）
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 101

# 去字幕并提取OCR字幕（模板 102）
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 102

# 去水印-高级版（模板 201）
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 201

# 人脸模糊（模板 301）
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 301

# 人脸和车牌模糊（模板 302）
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 302

# 强力擦除（区域模型，适合花体/阴影字幕）
python scripts/mps_erase.py --url https://example.com/video.mp4 --model area

# 使用区域预设 — 字幕在上半屏
python scripts/mps_erase.py --url https://example.com/video.mp4 --position top-half

# 使用区域预设 — 字幕在下半屏
python scripts/mps_erase.py --url https://example.com/video.mp4 --position bottom-half

# 自定义区域（画面顶部 0-25% 区域）
python scripts/mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.25

# 多区域擦除（顶部 + 底部都有字幕）
python scripts/mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.15 --area 0,0.75,1,1

# 去字幕 + OCR 提取 + 翻译为英文（必须用 --template 102）
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 102 --translate en

# 查询已有任务结果
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --verbose

# 查询任务并下载结果到本地
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --download-dir ./output/
