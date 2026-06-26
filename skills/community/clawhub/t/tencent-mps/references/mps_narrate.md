# AI 解说二创参数与示例 — `mps_narrate.py`

**功能**：输入原始短剧视频，一站式自动完成解说脚本生成、AI 配音、去字幕，输出带解说的新视频。
> **核心机制**：`AiAnalysisTask.Definition=35` + `ExtendedParameter(reel.processType=narrate + 场景参数)`。
> 脚本**默认同步等待**任务完成，加 `--no-wait` 只提交任务返回 TaskId。

## 预设场景

| 场景值 | 说明 | 擦除设置 |
|--------|------|----------|
| `short-drama` | 短剧视频，画面上有字幕（默认）| 开启擦除 |
| `short-drama-no-erase` | 短剧视频，画面上没有字幕 | 关闭擦除 |

**场景选择规则**：
- 用户说"有字幕"/"带硬字幕" → 使用 `short-drama`
- 用户说"没有字幕"/"原片无字幕"/"不擦除" → 使用 `short-drama-no-erase`

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径（第一集视频），自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 输入视频 URL（HTTP/HTTPS），第一集视频 |
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-region`/`--cos-input-key` 配合，推荐）|
| `--cos-input-region` | 输入 COS Bucket 区域（如 `ap-guangzhou`）|
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`，**推荐**）|
| `--extra-urls` | 第2集及之后的视频 URL 列表（按顺序，分辨率须与第一集一致）|
| `--scene` | **必填**。预设场景：`short-drama` / `short-drama-no-erase` |
| `--output-count` | 输出视频数量，默认 1，最大 5 |
| `--output-bucket` | 输出 COS Bucket |
| `--output-region` | 输出 COS Region |
| `--output-dir` | 输出目录，默认 `/output/narrate/` |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`） |
| `--notify-url` | 任务完成回调 URL |
| `--no-wait` | 仅提交任务，不等待结果（返回 TaskId 后退出）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800 |
| `--download-dir` | 任务完成后将输出文件下载到指定本地目录（默认仅打印预签名 URL）|
| `--dry-run` | 只打印参数预览，不调用 API |
| `--verbose` / `-v` | 输出详细信息 |

> ⚠️ **不支持自定义脚本**：不支持输入自定义解说脚本（`scriptUrls`），仅支持 MPS 自动生成。
> ⚠️ **多集视频分辨率**：使用 `--extra-urls` 追加多集视频时，所有视频的分辨率须保持一致。

## 强制规则

- `--scene` **必填**，值必须是预设枚举之一：`short-drama` | `short-drama-no-erase`
  - 用户说"有字幕"/"带硬字幕"时 → 选 `short-drama`（含擦除）
  - 用户说"没有字幕"/"原片无字幕"/"不擦除"时 → 选 `short-drama-no-erase`
  - **用户未说明字幕情况时，必须先追问**："请问视频是否含有硬字幕？有字幕选 `short-drama`（自动擦除字幕），无字幕选 `short-drama-no-erase`。"，不得猜测直接执行
- 多集视频时，第一集用 `--url`/`--cos-input-key`，后续集用 `--extra-urls` 按顺序追加
- 禁止传入 `scriptUrls` 相关参数（不支持输入自定义脚本）

## 示例命令

```bash
# 短剧单集解说（默认含擦除）
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama

# COS 对象输入
python scripts/mps_narrate.py --cos-input-key /input/drama.mp4 --scene short-drama

# 原视频无字幕，关闭擦除
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama-no-erase

# 多集视频合并解说（第一集用 --url，后续集用 --extra-urls）
python scripts/mps_narrate.py \
    --url https://example.com/ep01.mp4 \
    --extra-urls https://example.com/ep02.mp4 https://example.com/ep03.mp4 \
    --scene short-drama

# 输出 3 个不同版本的视频
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --output-count 3

# 异步提交（不等待结果）
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --no-wait

# Dry Run（预览 ExtendedParameter）
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --dry-run

# 查询任务状态
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx
```
