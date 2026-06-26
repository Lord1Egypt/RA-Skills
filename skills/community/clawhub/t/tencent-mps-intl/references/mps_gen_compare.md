# mps_gen_compare.py — Media Effect Comparison Tool

**Function**: Generates interactive HTML comparison pages, supporting before-and-after effect comparison for video and image processing.

**Features**: Local tool, **does not call MPS API and incurs no charges**.

## Parameter Reference

### Single Comparison (Most Common)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--original` | Yes | Original media URL or local file path |
| `--enhanced` | Yes | Processed media URL or local file path |

### Multiple Comparisons

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--pairs` | No | Multiple comparison pairs, each in format: `"originalURL,enhancedURL"`, supports multiple pairs |
| `--config` | No | JSON configuration file path |

### General Options

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--title` | No | `"Media Comparison"` | Page title |
| `--labels` | No | `"Original" "Enhanced"` | Custom left/right labels, format: `--labels "Left Label" "Right Label"` |
| `-o` / `--output` | No | `evals/test_result/compare_<timestamp>.html` | Output HTML file path |
| `--type` | No | Auto-detect | Force media type: `video` or `image` |
| `--dry-run` | No | — | Dry run, does not actually generate output |

## Comparison Capabilities

| Media Type | Comparison Method |
|------------|-------------------|
| **Video** | Slider divider + dual video synchronized playback + frame stepping (frame-by-frame forward/backward) + progress bar + speed control |
| **Image** | Slider divider / side-by-side comparison / overlay toggle (hover to switch) — three modes |

## Examples

### Video Enhancement Before/After Comparison

```bash
python scripts/mps_gen_compare.py \
    --original "https://example.cos.ap-guangzhou.myqcloud.com/input/video.mp4" \
    --enhanced "https://example.cos.ap-guangzhou.myqcloud.com/output/video_enhanced.mp4" \
    --title "4K Enhancement Effect Comparison" \
    --labels "Original" "4K Enhanced"
```

### Image Super-Resolution Before/After Comparison

```bash
python scripts/mps_gen_compare.py \
    --original "https://example.cos.ap-guangzhou.myqcloud.com/input/photo.jpg" \
    --enhanced "https://example.cos.ap-guangzhou.myqcloud.com/output/photo_sr.jpg" \
    --title "Image Super-Resolution Effect Comparison" \
    --labels "Original" "Super-Resolution" \
    --type image
```

### Watermark Removal Before/After Comparison

```bash
python scripts/mps_gen_compare.py \
    --original "https://example.cos.ap-guangzhou.myqcloud.com/input/video.mp4" \
    --enhanced "https://example.cos.ap-guangzhou.myqcloud.com/output/video_erased.mp4" \
    --title "Watermark Removal Effect Comparison" \
    --labels "Original (with watermark)" "Watermark Removed"
```

### Multiple Comparisons

```bash
python scripts/mps_gen_compare.py \
    --pairs \
    "https://xxx.cos/input1.mp4,https://xxx.cos/output1.mp4" \
    "https://xxx.cos/input2.jpg,https://xxx.cos/output2.jpg" \
    --title "Batch Processing Effect Comparison"
```

### Local File Comparison (Auto-uploads to COS and Generates Links)

```bash
python scripts/mps_gen_compare.py \
    --original /data/workspace/input.mp4 \
    --enhanced /data/workspace/output.mp4 \
    --title "Processing Effect Comparison"
```

## Mandatory Rules

1. **URL Source**: `--original` uses the original input URL provided by the user to the processing script; `--enhanced` uses the result URL output by the processing script (pre-signed download links or regular COS URLs are both acceptable)
2. **Title and Labels**: Set meaningful `--title` and `--labels` based on the processing type; do not use default values
3. **Image Type**: When comparing images (from `mps_imageprocess.py`, `mps_image_tryon.py`, `mps_image_bg_fusion.py`), it is recommended to explicitly specify `--type image`
4. **Display After Generation**: After the HTML is generated, use the `web_preview` tool to open the page and display it to the user
5. **No Cost Notice**: This script does not call MPS API and incurs no charges

## Applicable Scenarios

After the following processing scripts are executed, this script can be used to generate comparison effects:

| Processing Script | Comparison Scenario | Suggested Labels |
|-------------------|---------------------|------------------|
| `mps_enhance.py` | Quality enhancement / 4K enhancement / Old film restoration / Super-resolution | `"Original" "Enhanced"` |
| `mps_erase.py` | Subtitle removal / Watermark removal / Face blur | `"Original" "Erased"` |
| `mps_transcode.py` | Transcoding / Compression / Format conversion | `"Original" "Transcoded"` |
| `mps_imageprocess.py` | Image super-resolution / Beautification / Denoising | `"Original" "Processed"` |
| `mps_dedupe.py` | Video deduplication / Picture-in-picture / Video expansion / Vertical fill / Horizontal fill | `"Original" "Deduplicated"` |
| `mps_vremake.py` | Face swap / Person swap / Video interleaving | `"Original" "Remixed"` |
| `mps_narrate.py` | AI narration / Short drama narration / Narration remix | `"Original" "Narrated"` |
| `mps_highlight.py` | Highlight reel / Highlight extraction / Football highlights / Basketball highlights / VLOG highlights | `"Original" "Highlights"` |
| `mps_image_tryon.py` | Image try-on / AI fitting | `"Original" "Try-On"` |
| `mps_image_bg_fusion.py` | Background fusion / Background replacement | `"Original" "Background Changed"` |