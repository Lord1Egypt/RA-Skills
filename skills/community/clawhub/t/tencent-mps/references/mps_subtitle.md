# 智能字幕参数与示例 — `mps_subtitle.py`

**功能**：字幕提取、翻译、语音识别（ASR）、OCR 硬字幕识别，支持 30+ 种语言互译。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL 地址 |
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-region`/`--cos-input-key` 配合，推荐）|
| `--cos-input-region` | 输入 COS Bucket 区域（如 `ap-guangzhou`）|
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`，**推荐**）|
| `--process-type` | 处理类型：`asr`（语音识别，默认）/ `ocr`（画面文字识别）/ `translate`（翻译）|
| `--src-lang` | 视频源语言。**ASR 模式**：`zh`、`en`、`ja`、`ko`、`zh-PY`、`yue`、`zh_dialect`、`prime_zh`、`vi`、`ms`、`id`、`th`、`fr`、`de`、`es`、`pt`、`ru`、`ar` 等；**OCR 模式**：`zh_en`（中英，默认）、`multi`（多语种）|
| `--subtitle-type` | 字幕类型：`0`=源语言、`1`=翻译语言、`2`=双语（有翻译时默认）|
| `--subtitle-format` | 字幕格式：`vtt` / `srt` / `original` |
| `--translate` | 翻译目标语言，支持多语言用 `/` 分隔，如 `en/ja`。支持 30+ 种语言：`zh`、`en`、`ja`、`ko`、`fr`、`es`、`de`、`it`、`ru`、`pt`、`ar`、`th`、`vi`、`id`、`ms`、`tr`、`nl`、`pl`、`sv` 等 |
| `--hotwords-id` | ASR 热词库 ID，提高专业术语识别准确率，如 `hwd-xxxxx` |
| `--ocr-area` | OCR 识别区域（百分比坐标 0-1），格式 `x1,y1,x2,y2`，可多次指定 |
| `--sample-width` | 示例视频/图片的宽度（像素），配合 `--ocr-area` 使用 |
| `--sample-height` | 示例视频/图片的高度（像素），配合 `--ocr-area` 使用 |
| `--template` | 智能字幕预设模板 ID（如 `110167`）|
| `--user-ext-para` | 用户自定义扩展参数（JSON 字符串，高级选项）|
| `--ext-info` | 扩展信息（JSON 字符串，高级选项）|
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量）|
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量）|
| `--output-dir` | 输出目录，默认 `/output/subtitle/` |
| `--output-object-path` | 输出字幕文件路径，如 `/output/{inputName}_subtitle.{format}` |
| `--no-wait` | 仅提交任务，不等待结果（默认自动轮询）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800（30 分钟）|
| `--download-dir` | 任务完成后将输出文件下载到指定本地目录（默认仅打印预签名 URL）|
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--notify-url` | 任务完成回调 URL（可选）|
| `--dry-run` | 只打印参数，不调用 API |

## 强制规则

- **`--process-type` 选择规则**：
  - 用户说"语音识别"、"识别说话内容"、"转文字"、"ASR" → 使用 `--process-type asr`（默认，可省略）
  - 用户说"OCR"、"识别画面文字"、"硬字幕识别"、"提取画面中的文字" → 使用 `--process-type ocr`，并根据语言设置 `--src-lang`（中英 `zh_en`，多语种 `multi`）
  - 用户说"翻译"、"字幕翻译"、"翻译成xx语言" → 使用 `--process-type translate`（或在 `asr`/`ocr` 基础上加 `--translate <目标语言>`）
- **`--src-lang` 规则**：OCR 模式下默认 `zh_en`；ASR 模式下若用户未指明语言，默认 `zh`
- **`--translate` 规则**：支持多目标语言用 `/` 分隔，如 `--translate en/ja`；翻译时字幕类型默认为双语（`--subtitle-type 2`）

## 示例命令

```bash
# ASR 识别字幕（默认）
python scripts/mps_subtitle.py --url https://example.com/video.mp4

# ASR + 翻译为英文（双语字幕）
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en

# OCR 识别硬字幕 + 翻译
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en --translate en

# 多语言翻译（英文+日文）
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en/ja

# COS 路径输入（推荐）
python scripts/mps_subtitle.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou \
    --cos-input-key /input/video.mp4 --src-lang zh --translate en

# 异步提交后查询任务状态
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --no-wait
python scripts/mps_get_video_task.py --task-id 1250017490-20260318152230-abcdef123456
```
