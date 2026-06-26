# 媒体质检参数与示例 — `mps_qualitycontrol.py`

**功能**：音视频质量检测，支持画面质检、播放兼容性检测、音频质检三种模式。
> ⚠️ "画质检测"、"模糊"、"花屏"、"播放兼容性"、"音频质检" → 必须用此脚本，不要用 `mps_erase.py`。

## 质检模板

| 模板 ID | 名称 | 适用场景 |
|---------|------|---------|
| `50` | Audio Detection | 音频质量/音频事件检测 |
| `60` | 格式质检-Pro版（**默认**） | 画面模糊、花屏、画面受损等内容问题 |
| `70` | 内容质检-Pro版 | 播放卡顿、播放异常、播放兼容性问题 |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL 地址 |
| `--cos-input-key` | COS 输入文件的 Key（如 `/input/video.mp4`，推荐使用）|
| `--cos-input-bucket` | 输入文件所在 COS Bucket 名称（默认使用环境变量）|
| `--cos-input-region` | 输入文件所在 COS Region（如 `ap-guangzhou`）|
| `--definition` | 质检模板 ID（默认 `60`）。`50`：音频质检；`60`：格式质检（画面模糊/花屏等）；`70`：内容质检（播放兼容性）|
| `--no-wait` | 仅提交任务，不等待结果（返回 TaskId 后退出）|
| `--json` | 以 JSON 格式输出结果 |
| `--output-bucket` | 输出 COS Bucket 名称（默认从环境变量读取）|
| `--output-region` | 输出 COS Region（默认从环境变量读取）|
| `--output-dir` | 输出目录路径（如 `/output/quality_control/`）|
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--notify-url` | 任务完成回调 URL（可选）|
| `--dry-run` | 只打印参数，不调用 API |

## 强制规则

- **必须根据用户描述的场景选择对应模板**，不得随意使用默认值：
  - 用户说"音频质检"、"噪音检测"、"静音检测"、"音频事件" → **必须用 `--definition 50`**
  - 用户说"画质检测"、"模糊"、"花屏"、"画面受损"、"视频质量" → **必须用 `--definition 60`**（默认）
  - 用户说"播放兼容性"、"卡顿"、"播放异常"、"播放失败" → **必须用 `--definition 70`**
- 若用户描述模糊、无法判断场景，才使用默认值 `60`，并向用户说明

## 示例命令

```bash
# 画面质检（默认，模板 60）
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4

# 指定画面质检模板
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 60

# 播放兼容性质检（模板 70）
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 70

# 音频质检（模板 50）
python scripts/mps_qualitycontrol.py --url https://example.com/audio.mp3 --definition 50

# COS 输入（推荐写法）
python scripts/mps_qualitycontrol.py --cos-input-key /input/video.mp4

# 异步提交
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --no-wait

# 查询已有任务结果（JSON 格式）
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx

# dry-run 预览
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 70 --dry-run
```

