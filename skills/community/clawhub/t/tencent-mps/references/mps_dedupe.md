# 视频去重参数与示例 — `mps_dedupe.py`

**功能**：视频去重（VideoRemake），通过修改视频画面规避平台重复内容检测。
> **核心机制**：`AiAnalysisTask.Definition=29` + `ExtendedParameter(vremake.mode)`。
> 脚本**默认自动轮询等待完成**，加 `--no-wait` 才只提交不等待。
> 官方文档：https://cloud.tencent.com/document/product/862/124394

## 支持模式

| 模式 | 说明 |
|------|------|
| `PicInPic` | 画中画：原视频缩小嵌入新背景 |
| `BackgroundExtend` | 视频扩展：在场景切换处插入扩展画面 |
| `VerticalExtend` | 垂直填充：上下方向添加填充内容 |
| `HorizontalExtend` | 水平填充：左右方向添加填充内容 |

> **默认模式**：未指定 `--mode` 时自动使用 `PicInPic`。
> **精细化控制**：每种模式均支持更多精细化参数，如有需要请[联系腾讯云](https://cloud.tencent.com/document/product/862/124394)线下对接确认具体配置。

## 强制规则

1. 用户说"视频去重"、"视频防重"、"规避重复检测"时，**必须使用本脚本**（`mps_dedupe.py`），不得使用 `mps_vremake.py`。
2. `--mode` 参数**可省略**，默认为 `PicInPic`（画中画）。如用户未指定模式，**直接使用默认值，不需要追问**。
3. 如用户明确要求其他模式（垂直填充/水平填充/视频扩展），则按用户要求选择。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL（HTTP/HTTPS）|
| `--cos-input-key` | COS 输入文件的 Key（如 `/input/video.mp4`，推荐使用）|
| `--cos-input-bucket` | 输入文件所在 COS Bucket 名称（默认使用环境变量）|
| `--cos-input-region` | 输入文件所在 COS Region（如 `ap-guangzhou`）|
| `--mode` | 去重模式（默认 `PicInPic`，见上表）|
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量）|
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量）|
| `--output-cos-dir` | COS 输出目录（默认 `/output/dedupe/`），以 `/` 开头和结尾 |
| `--no-wait` | 异步模式：只提交任务，返回 TaskId，不等待结果 |
| `--json` | JSON 格式输出 |
| `--output-dir` | 将结果 JSON 保存到指定目录 |
| `--download-dir` | 任务完成后将输出视频下载到指定本地目录（不指定则只打印输出路径和预签名 URL）|
| `--definition` | AiAnalysisTask 模板 ID（默认 `29`）|
| `--region` | 处理地域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数预览（含 ExtendedParameter），不调用 API |

## 示例命令

```bash
# 最简用法（默认 PicInPic 模式，自动等待完成）
python scripts/mps_dedupe.py --url https://example.com/video.mp4

# 垂直填充去重
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --mode VerticalExtend

# 水平填充去重
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --mode HorizontalExtend

# 视频扩展去重（COS 输入）
python scripts/mps_dedupe.py --cos-input-key /input/video.mp4 \
    --mode BackgroundExtend

# 本地文件（自动上传到 COS）
python scripts/mps_dedupe.py --local-file ./video.mp4

# 异步提交（不等待，获取 TaskId 后可用 mps_get_video_task.py 查询）
python scripts/mps_dedupe.py --url https://example.com/video.mp4 --no-wait

# 完成后自动下载结果到本地
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --download-dir /data/workspace/output/

# dry-run 预览
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --mode BackgroundExtend --dry-run
```
