---
name: volcengine-image-studio
description: Practical image generation workflow for Volcengine/ARK-compatible APIs. Use when users need poster creation, text-to-image, reference-image generation, local image upload, multi-image runs, or automatic result downloads. 中文：适合火山引擎 / ARK 兼容接口的实战图片生成；适用于海报生成、文生图、参考图生图、本地图片上传、多图连续生成和结果自动下载。
---

# volcengine-image-studio

Use this skill to **actually generate images** through a Volcengine/ARK-compatible image endpoint.

## 中文说明

这是一个面向 **火山引擎 / ARK 兼容图片生成接口** 的实战型 skill，不只是帮你写提示词，而是直接把图片生成跑起来。

适用场景包括：

- 生成海报、宣传图、配图
- 文生图
- 单张或多张参考图生图
- 直接使用本地图片作为输入
- 一次生成多张结果图
- 自动下载生成结果到本地

## Default path

Run the bundled script:

```bash
python3 scripts/generate_image.py "<prompt>"
```

By default, URL results are **auto-downloaded to Desktop**. For multi-image runs, the script creates a **new folder per run** automatically and opens that folder in Finder.

## Required config

The script reads config from env vars:

- `VOLCENGINE_API_KEY` or `ARK_API_KEY`
- `VOLCENGINE_MODEL` or `ARK_MODEL`
- `VOLCENGINE_ENDPOINT` or `ARK_BASE_URL`

## Supported modes

### 1. Text to image

```bash
python3 scripts/generate_image.py "极简科技海报，深色背景，蓝紫色霓虹光效，高级感"
```

### 2. One local reference image → one new image

```bash
python3 scripts/generate_image.py "生成狗狗趴在草地上的近景画面" \
  --image ~/Desktop/dog-reference.png \
  --sequential-image-generation disabled
```

### 3. One reference image URL → one new image

```bash
python3 scripts/generate_image.py "生成狗狗趴在草地上的近景画面" \
  --image "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imageToimage.png" \
  --sequential-image-generation disabled
```

### 4. One reference image → multiple new images

```bash
python3 scripts/generate_image.py "参考这个LOGO，做一套户外运动品牌视觉设计，品牌名称为GREEN，包括包装袋、帽子、纸盒、手环、挂绳等。绿色视觉主色调，趣味、简约现代风格" \
  --image "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imageToimages.png" \
  --sequential-image-generation auto \
  --sequential-max-images 5 \
  --stream true
```

### 5. Multiple reference images → multiple new images

```bash
python3 scripts/generate_image.py "生成3张女孩和奶牛玩偶在游乐园开心地坐过山车的图片，涵盖早晨、中午、晚上" \
  --image "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_1.png" \
  --image "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_2.png" \
  --sequential-image-generation auto \
  --sequential-max-images 3 \
  --stream true
```

You can also pass a local text file of URLs/paths:

```bash
python3 scripts/generate_image.py "根据参考图生成多张变体" --image-file ./refs.txt
```

## Local image path support

- `--image ~/Desktop/ref.png` → automatically converted to a `data:` URL with base64
- `--image https://...` → sent as-is
- `--image data:image/png;base64,...` → sent as-is

This lets you use local files directly without manually converting them.

## Auto-download behavior

When the API returns image URLs, the script downloads them to Desktop by default.

Example download behavior:

- Single image: `~/Desktop/1710000000-my-prompt-1.jpeg`
- Multi-image run: `~/Desktop/1710000000-my-prompt/1710000000-my-prompt-1.jpeg`

Disable auto-download if needed:

```bash
python3 scripts/generate_image.py "极简科技海报" --download-results false
```

Custom download directory:

```bash
python3 scripts/generate_image.py "极简科技海报" --download-dir ~/Downloads/volcengine
```

Force a new folder even for single-image runs:

```bash
python3 scripts/generate_image.py "极简科技海报" --download-folder-per-run true
```

Disable per-run folders:

```bash
python3 scripts/generate_image.py "极简科技海报" --download-folder-per-run false
```

Disable auto-opening Finder:

```bash
python3 scripts/generate_image.py "极简科技海报" --open-download-folder false
```

## Optional env vars

- `VOLCENGINE_IMAGE_SIZE` (example: `2K`)
- `VOLCENGINE_IMAGE_COUNT` (default `1`)
- `VOLCENGINE_IMAGE_QUALITY` (default `standard`)
- `VOLCENGINE_RESPONSE_FORMAT` (default `url`)
- `VOLCENGINE_SEQUENTIAL_IMAGE_GENERATION` (`disabled` / `auto`)
- `VOLCENGINE_SEQUENTIAL_MAX_IMAGES` (example: `3`)
- `VOLCENGINE_STREAM` (`true` / `false`)
- `VOLCENGINE_WATERMARK` (`true` / `false`)
- `VOLCENGINE_OUTPUT_DIR` (default `generated-images`)
- `VOLCENGINE_DOWNLOAD_RESULTS` (default `true`)
- `VOLCENGINE_DOWNLOAD_DIR` (default `~/Desktop`)
- `VOLCENGINE_DOWNLOAD_FOLDER_PER_RUN` (`auto` / `true` / `false`, default `auto`)
- `VOLCENGINE_OPEN_DOWNLOAD_FOLDER` (`auto` / `true` / `false`, default `auto`)
- `VOLCENGINE_TIMEOUT` (default `120`)

## Execution checklist

1. Confirm prompt, target style, and whether reference images are needed.
2. Add `--image` once for single-reference generation, or repeat it for multi-reference generation.
3. For local images, pass the local path directly; the script converts it to base64 data URL automatically.
4. For single-image-to-multi-image and multi-reference sequences, set `--sequential-image-generation auto` and `--sequential-max-images <N>`.
5. Use `--stream true` when the API returns incremental image events.
6. By default, returned image URLs are downloaded to Desktop; multi-image runs go into a new folder automatically.
7. Mention the downloaded paths or folder path in the result.
8. For multi-image runs, let Finder open the created folder unless the user disabled it.
9. If it fails, surface the exact HTTP error or missing field.

## Release positioning

Compared with an earlier bare-bones generation flow, this version is packaged around the logic that proved usable in practice:

- supports Volcengine / ARK-compatible endpoint patterns
- supports reference-image workflows, including local files
- supports sequential multi-image generation
- supports automatic result download and run-based folder grouping
- better fits poster and commercial visual production

## Troubleshooting

- Missing key → set `VOLCENGINE_API_KEY`
- Missing model → set `VOLCENGINE_MODEL`
- Missing endpoint → set `VOLCENGINE_ENDPOINT`
- Local file not found → check the `--image` path
- 401/403 → key invalid or lacks permission
- 404/405 → endpoint wrong
- 400 → model/size/request body incompatible with the target API
- No returned files/URLs → inspect `raw` in the JSON output

## References

- `references/sources.md`
 found → check the `--image` path
- 401/403 → key invalid or lacks permission
- 404/405 → endpoint wrong
- 400 → model/size/request body incompatible with the target API
- No returned files/URLs → inspect `raw` in the JSON output

## References

- `references/sources.md`
 inspect `raw` in the JSON output

## References

- `references/sources.md`
