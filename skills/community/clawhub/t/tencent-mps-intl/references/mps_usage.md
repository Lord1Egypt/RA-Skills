# Usage Statistics Parameters & Examples — `mps_usage.py`

**Function**: Query usage statistics (call count / duration) for various task types in Tencent Cloud MPS.

## Parameter Description

| Parameter | Description |
|------|------|
| `--days` | Query the last N days (default 7, max 90); mutually exclusive with `--start` |
| `--start` | Start date, format `YYYY-MM-DD` (used together with `--end`) |
| `--end` | End date, format `YYYY-MM-DD` (default today) |
| `--type` | Task type (multiple selections allowed), default `Transcode`. Available values: `Transcode` / `Enhance` / `AIAnalysis` (intelligent analysis, including audio/video understanding) / `AIRecognition` (intelligent recognition) / `AIReview` (content review) / `Snapshot` / `AnimatedGraphics` (animated image) / `AiQualityControl` (quality inspection) / `Evaluation` (video evaluation) / `ImageProcess` (image processing) / `AddBlindWatermark` (digital watermark) / `AddNagraWatermark` / `ExtractBlindWatermark` / `AIGC` (image/video generation) |
| `--all-types` | Query all task types (mutually exclusive with `--type`) |
| `--region` | MPS service region, multiple selections allowed (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--json` | Output results in JSON format |
| `--dry-run` | Only print request parameters without making actual calls |

## Example Commands

```bash
# Query usage for the last 7 days (default)
python scripts/mps_usage.py

# Query all types for the last 30 days
python scripts/mps_usage.py --days 30 --all-types

# Query a specific date range
python scripts/mps_usage.py --start 2026-01-01 --end 2026-01-31

# Query multiple task types
python scripts/mps_usage.py --type Transcode Enhance AIGC

# Query large model audio/video understanding usage (belongs to AIAnalysis type)
python scripts/mps_usage.py --days 30 --type AIAnalysis

# Query digital watermark related usage
python scripts/mps_usage.py --type AddBlindWatermark AddNagraWatermark ExtractBlindWatermark

# Query usage across multiple regions
python scripts/mps_usage.py --region ap-guangzhou ap-hongkong

# JSON format output
python scripts/mps_usage.py --days 7 --all-types --json
```

## Mandatory Rules

1. **Default Behavior**: When the user says "query usage" without specifying a type, default to `--type Transcode`, do not ask the user; if the user explicitly says "query all types", use `--all-types`.
2. **Date Range**: When the user does not specify a date, default to `--days 7` (last 7 days), do not ask the user.
3. **Audio/Video Understanding Usage**: The usage of audio/video understanding (`mps_av_understand.py`) belongs to the `AIAnalysis` type; use `--type AIAnalysis` when querying.