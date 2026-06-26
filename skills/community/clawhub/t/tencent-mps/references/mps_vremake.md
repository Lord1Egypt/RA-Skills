# 视频二次创作参数与示例 — `mps_vremake.py`

**功能**：视频二次创作（VideoRemake），支持换脸、换人、视频交错（AB）等创作模式。
> **核心机制**：`AiAnalysisTask.Definition=29` + `ExtendedParameter(vremake.mode + 模式参数)`。
> 脚本**默认自动轮询等待完成**，加 `--no-wait` 才只提交不等待。
> 官方文档：https://cloud.tencent.com/document/product/862/124394

> ⚠️ **视频去重**（画中画/视频扩展/垂直填充/水平填充）请使用 [`mps_dedupe.py`](mps_dedupe.md)，不要使用本脚本。

## 支持模式

| 模式 | 说明 |
|------|------|
| `AB` | 视频交错：AB 视频交错模式 |
| `SwapFace` | 换脸：视频人脸替换 |
| `SwapCharacter` | 换人：视频人物替换 |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL（HTTP/HTTPS）|
| `--cos-input-key` | COS 输入文件的 Key（如 `/input/video.mp4`，推荐使用）|
| `--cos-input-bucket` | 输入文件所在 COS Bucket 名称（默认使用环境变量）|
| `--cos-input-region` | 输入文件所在 COS Region（如 `ap-guangzhou`）|
| `--mode` | **必填**。二次创作模式（见上表）|
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量）|
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量）|
| `--output-cos-dir` | COS 输出目录（默认 `/output/vremake/`），以 `/` 开头和结尾 |
| `--no-wait` | 异步模式：只提交任务，返回 TaskId，不等待结果 |
| `--src-faces` | [SwapFace] 原视频中人脸 URL 列表（与 `--dst-faces` 一一对应，最多 6 张）|
| `--dst-faces` | [SwapFace] 目标人脸 URL 列表 |
| `--src-character` | [SwapCharacter] 原视频人物 URL（正面全身图）|
| `--dst-character` | [SwapCharacter] 目标人物 URL（正面全身图）|
| `--llm-prompt` | [AB] 大模型提示词 |
| `--llm-video-prompt` | [AB] 大模型提示词（生成背景**视频**，优先于 `--llm-prompt`）|
| `--random-cut` | [AB] 随机裁剪 |
| `--random-speed` | [AB] 随机加速 |
| `--random-flip` | [AB] 随机镜像（`true`/`false`，默认 `true`）|
| `--ext-mode` | [AB] 扩展模式 `1`/`2`/`3` |
| `--custom-json` | 自定义 vremake 扩展参数 JSON（与 `--mode` 自动合并）|
| `--json` | JSON 格式输出 |
| `--output-dir` | 将结果 JSON 保存到指定目录 |
| `--download-dir` | 任务完成后将输出视频下载到指定本地目录（默认仅打印预签名 URL）|
| `--definition` | AiAnalysisTask 模板 ID（默认 `29`）|
| `--region` | 处理地域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数预览，不调用 API |

**SwapFace 限制**：视频分辨率 ≤ 4K；单张图片 < 10MB（jpg/png）；人脸总数 ≤ 6 张。
**SwapCharacter 限制**：视频时长 ≤ 20 分钟；需正面全身图。

## 强制规则

- `--mode` **必填**，值必须是预设枚举之一：`AB` | `SwapFace` | `SwapCharacter`
  - 用户说"换脸"、"替换人脸" → 使用 `--mode SwapFace`，并提供 `--src-faces` 和 `--dst-faces`（一一对应）
  - 用户说"换人"、"替换人物" → 使用 `--mode SwapCharacter`，并提供 `--src-character` 和 `--dst-character`（正面全身图）
  - 用户说"视频交错"、"AB 混剪" → 使用 `--mode AB`
  - **用户未指明模式时，必须追问**，不得猜测
- **视频去重**（画中画/视频扩展/垂直填充/水平填充）必须使用 `mps_dedupe.py`，**禁止用本脚本**
- `SwapFace` 限制：视频分辨率 ≤ 4K；单张人脸图片 < 10MB（jpg/png）；人脸总数 ≤ 6 张
- `SwapCharacter` 限制：视频时长 ≤ 20 分钟；人物图必须是正面全身图

## 示例命令

```bash
# ===== 换脸 =====

# 换脸模式（--src-faces 和 --dst-faces 一一对应，自动等待完成）
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapFace \
    --src-faces https://example.com/src1.png https://example.com/src2.png \
    --dst-faces https://example.com/dst1.jpg https://example.com/dst2.jpg

# ===== 换人 =====

# 换人模式（正面全身图）
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapCharacter \
    --src-character https://example.com/src_fullbody.png \
    --dst-character https://example.com/dst_fullbody.png

# ===== 视频交错（AB） =====

python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode AB

# ===== 通用 =====

# 异步提交（加 --no-wait 只提交不等待）
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapFace \
    --src-faces https://example.com/src.png \
    --dst-faces https://example.com/dst.png \
    --no-wait

# 查询已有任务结果
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx

# dry-run 预览
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapFace \
    --src-faces https://example.com/src.png \
    --dst-faces https://example.com/dst.png \
    --dry-run
```
