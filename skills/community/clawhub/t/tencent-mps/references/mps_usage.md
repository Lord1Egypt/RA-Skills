# 用量统计参数与示例 — `mps_usage.py`

**功能**：查询腾讯云 MPS 各类型任务的用量统计（调用次数/时长）。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--days` | 查询最近 N 天（默认 7 天，最大 90），与 `--start` 互斥 |
| `--start` | 开始日期，格式 `YYYY-MM-DD`（与 `--end` 配合使用）|
| `--end` | 结束日期，格式 `YYYY-MM-DD`（默认今天）|
| `--type` | 任务类型（可多选），默认 `Transcode`。可选值：`Transcode`（转码）/ `Enhance`（增强）/ `AIAnalysis`（智能分析，含音视频理解）/ `AIRecognition`（智能识别）/ `AIReview`（内容审核）/ `Snapshot`（截图）/ `AnimatedGraphics`（转动图）/ `AiQualityControl`（质检）/ `Evaluation`（视频评测）/ `ImageProcess`（图片处理）/ `AddBlindWatermark`（数字水印）/ `AddNagraWatermark` / `ExtractBlindWatermark` / `AIGC`（生图/生视频）|
| `--all-types` | 查询所有任务类型（与 `--type` 互斥）|
| `--region` | MPS 服务区域，可多选（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`） |
| `--json` | 以 JSON 格式输出结果 |
| `--dry-run` | 仅打印请求参数，不实际调用 |

## 示例命令

```bash
# 查询最近 7 天用量（默认）
python scripts/mps_usage.py

# 查询最近 30 天所有类型
python scripts/mps_usage.py --days 30 --all-types

# 查询指定日期范围
python scripts/mps_usage.py --start 2026-01-01 --end 2026-01-31

# 查询多个任务类型
python scripts/mps_usage.py --type Transcode Enhance AIGC

# 查询大模型音视频理解用量（属于 AIAnalysis 类型）
python scripts/mps_usage.py --days 30 --type AIAnalysis

# 查询数字水印相关用量
python scripts/mps_usage.py --type AddBlindWatermark AddNagraWatermark ExtractBlindWatermark

# 查询多地域用量
python scripts/mps_usage.py --region ap-guangzhou ap-hongkong

# JSON 格式输出
python scripts/mps_usage.py --days 7 --all-types --json
```

## 强制规则

1. **默认行为**：用户说"查询用量"而未指定类型时，默认使用 `--type Transcode`（转码），不得询问用户；若用户明确说"查询所有类型"，使用 `--all-types`。
2. **日期范围**：用户未指定日期时，默认 `--days 7`（最近 7 天），不得询问用户。
3. **音视频理解用量**：音视频理解（`mps_av_understand.py`）的用量属于 `AIAnalysis` 类型，查询时使用 `--type AIAnalysis`。
