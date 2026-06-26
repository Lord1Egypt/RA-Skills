# 图片处理参数与示例 — `mps_imageprocess.py`

**功能**：图片超分辨率、美颜、降噪、色彩增强、滤镜、缩放、盲水印、自动擦除等。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 图片 URL 地址 |
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-region`/`--cos-input-key` 配合，推荐）|
| `--cos-input-region` | 输入 COS Bucket 区域（如 `ap-guangzhou`）|
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/image.jpg`，**推荐**）|
| `--format` | 输出格式：`JPEG` / `PNG` / `BMP` / `WebP` |
| `--quality` | 图片质量 [1-100] |
| `--super-resolution` | 启用超分辨率（2 倍）|
| `--sr-type` | 超分类型：`lq`（低清晰度有噪声，默认）/ `hq`（高清晰度）|
| `--advanced-sr` | 启用高级超分 |
| `--adv-sr-type` | 高级超分类型：`standard`（通用，默认）/ `super` / `ultra` |
| `--sr-mode` | 高级超分输出模式：`percent`（倍率）/ `aspect`（等比，默认）/ `fixed`（固定）|
| `--sr-percent` | 高级超分倍率（如 `3.0`）|
| `--sr-width` / `--sr-height` | 高级超分目标宽/高（不超过 4096）|
| `--sr-long-side` | 高级超分目标长边（不超过 4096）|
| `--sr-short-side` | 高级超分目标短边（不超过 4096）|
| `--denoise` | 降噪强度：`weak`（轻度）/ `strong`（强力）|
| `--quality-enhance` | 综合增强强度：`weak` / `normal` / `strong` |
| `--color-enhance` | 色彩增强：`weak` / `normal` / `strong` |
| `--sharp-enhance` | 细节增强（0.0-1.0）|
| `--face-enhance` | 人脸增强强度（0.0-1.0）|
| `--lowlight-enhance` | 启用低光照增强 |
| `--beauty` | 美颜效果，格式 `类型:强度`（强度 0-100），可多次指定。类型：`Whiten`（美白）、`Smooth`（磨皮）、`BeautyThinFace`（瘦脸）、`NatureFace`（自然脸型）、`VFace`（V脸）、`EnlargeEye`（大眼）、`EyeLighten`（亮眼）、`RemoveEyeBags`（祛眼袋）、`ThinNose`（瘦鼻）、`ToothWhiten`（牙齿美白）、`FaceFeatureLipsLut`（口红，可附加颜色：`FaceFeatureLipsLut:50:#ff0000`）等 20 种 |
| `--filter` | 滤镜效果，格式 `类型:强度`。类型：`Dongjing`（东京）、`Qingjiaopian`（轻胶片）、`Meiwei`（美味）|
| `--erase-detect` | 自动擦除类型（可多选）：`logo` / `text` / `watermark` |
| `--erase-area` | 指定擦除区域（像素坐标），格式 `x1,y1,x2,y2`，可多次指定 |
| `--erase-box` | 指定擦除区域（百分比坐标 0-1），格式 `x1,y1,x2,y2`，可多次指定 |
| `--erase-area-type` | 指定区域擦除的类型：`logo`（默认）/ `text` |
| `--add-watermark` | 添加盲水印，指定水印文字（最多 4 字节，约 1 个中文字或 4 个 ASCII 字符）|
| `--extract-watermark` | 提取盲水印 |
| `--remove-watermark` | 移除盲水印 |
| `--resize-percent` | 百分比缩放倍率（如 `2.0` 表示放大 2 倍）|
| `--resize-mode` | 缩放模式：`percent` / `mfit` / `lfit` / `fill` / `pad` / `fixed` |
| `--resize-width` / `--resize-height` | 目标宽/高（像素）|
| `--resize-long-side` | 目标长边（像素）|
| `--resize-short-side` | 目标短边（像素）|
| `--definition` | 图片处理模板 ID |
| `--schedule-id` | 编排场景 ID（控制台预置 AI 能力），见下方「编排场景一览」。**换装请用 `mps_image_tryon.py`，背景融合请用 `mps_image_bg_fusion.py`**|
| `--resource-id` | 资源 ID（高级选项，特定场景使用）|
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量）|
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量）|
| `--output-path` | 输出文件路径模板（如 `/output/{inputName}_processed.{format}`）|
| `--output-dir` | 输出目录（如 `/output/image/`），不指定则使用 MPS 默认路径 |
| `--no-wait` | 仅提交任务，不等待结果（默认自动轮询）|
| `--poll-interval` | 轮询间隔（秒），默认 5 |
| `--max-wait` | 最长等待时间（秒），默认 300（5 分钟）|
| `--download-dir` | 任务完成后将输出文件下载到指定本地目录（默认仅打印预签名 URL）|
| `--compare [路径]` | 任务完成后自动生成效果对比 HTML 页面；可选指定输出路径，省略则自动命名 |
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## 编排场景一览（`--schedule-id`）

> 下列 ScheduleId 为腾讯云 MPS **控制台预置 AI 能力**。使用时通常仅需提供输入图片和 `--schedule-id` 即可，不需要配合其他处理参数（编排内部已预设完整流程）。

| ScheduleId | 能力 | 典型触发词 |
|:---:|------|------|
| `30000` | **AI 文字水印擦除** | 擦除文字水印 / 去文字水印 / 去图片水印文字 |
| `30010` | **AI 扩图（图片扩展）** | 图片扩图 / AI 扩展 / 画面扩展 / outpaint |
| `30030` | **AI 抠图** | AI 抠图 / 智能抠图 / 抠人像 / 抠主体 / 去背景（保留主体）|
| `30031` | **AI 前景提取** | 前景提取 / 提取主体 / 抽取前景 |
| `30040` | **AI 图片修复** | 图片修复 / 老照片修复 / 坏损修复 / 划痕修复 / 人像修复 |
| `30200` | **AI 图片理解** | 图片理解 / 图片内容识别 / AI 看图 / 描述图片内容 |

> ⚠️ 其它业务 ScheduleId 走专属脚本：`30060` 背景融合用 `mps_image_bg_fusion.py`；`30100/30101` 图片换装用 `mps_image_tryon.py`。

## 强制规则

- **超分辨率选择规则**：
  - 用户说"放大到 4K"、"超高清"、"放大 3 倍及以上"、"高清修复" → 优先使用 `--advanced-sr`（高级超分），可配合 `--sr-width`/`--sr-height` 或 `--sr-long-side` 指定目标尺寸
  - 用户说"2 倍放大"、"超分"、"提升分辨率"（未指定倍数或目标尺寸）→ 使用 `--super-resolution`（普通 2 倍超分）
  - **两种超分互斥**，不可同时使用 `--super-resolution` 和 `--advanced-sr`
- **擦除职责边界**：图片中的文字/水印/图标擦除用 `--erase-detect` 或 `--erase-area`；**视频**擦除请用 `mps_erase.py`，不要混用
- **换装场景禁止用此脚本**：图片换装必须使用 `mps_image_tryon.py`，`mps_imageprocess.py` 不支持换装功能（即使使用 `--schedule-id 30100/30101` 也不正确）
- **编排场景（`--schedule-id`）使用规则**：
  - 以下 AI 能力**必须**通过 `--schedule-id` 触发，不要自行组合处理参数：
    - 用户说"图片理解 / 看图 / 描述图片内容" → `--schedule-id 30200`
    - 用户说"抠图 / 智能抠图 / 抠主体" → `--schedule-id 30030`
    - 用户说"图片修复 / 老照片修复 / 划痕修复" → `--schedule-id 30040`
    - 用户说"前景提取 / 提取主体" → `--schedule-id 30031`
    - 用户说"AI 扩图 / 图片扩展 / outpaint" → `--schedule-id 30010`
    - 用户说"擦除文字水印 / 去图片上的文字水印"（强调 AI 智能擦除时）→ `--schedule-id 30000`
  - `--schedule-id` 与图片增强/擦除/美颜等本地配置参数**不要混用**（控制台编排模板已定义好完整流程）
  - 不同业务编排走不同脚本：**背景融合** → `mps_image_bg_fusion.py`（30060）；**换装** → `mps_image_tryon.py`（30100/30101）

## 示例命令

```bash
# 超分辨率 2 倍放大
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --super-resolution

# 高级超分至 4K
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --advanced-sr --sr-width 3840 --sr-height 2160

# 降噪 + 色彩增强 + 细节增强
python scripts/mps_imageprocess.py --url https://example.com/image.jpg \
    --denoise weak --color-enhance normal --sharp-enhance 0.8

# 综合增强（画质整体提升）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --quality-enhance normal

# 综合增强 + 超分（强力修复低质量图片）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --quality-enhance strong --super-resolution

# 美颜（美白 + 瘦脸 + 大眼）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg \
    --beauty Whiten:50 --beauty BeautyThinFace:30 --beauty EnlargeEye:40

# 自动擦除水印
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --erase-detect watermark

# 添加盲水印
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --add-watermark "MPS"

# 转为 WebP 格式 + 质量 80
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --format WebP --quality 80

# 滤镜（轻胶片风格，强度 70）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --filter Qingjiaopian:70

# 缩放（等比缩放至宽 800 高 600 以内）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --resize-mode lfit --resize-width 800 --resize-height 600

# 缩放（指定长边为 1920，等比缩放）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --resize-long-side 1920

# === 编排场景（AI 控制台预置能力，仅需输入图片 + schedule-id） ===
# AI 图片理解（30200）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30200

# AI 抠图（30030）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30030

# AI 图片修复（30040，老照片/划痕修复）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30040

# AI 前景提取（30031）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30031

# AI 扩图（30010）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30010

# AI 文字水印擦除（30000）
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30000

# 查询图片处理任务状态
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a
```
