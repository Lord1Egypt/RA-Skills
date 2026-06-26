# 视频增强参数与示例 — `mps_enhance.py`

**功能**：视频画质增强、老片修复、超分辨率、音频分离/人声提取/伴奏提取、HDR、插帧、音频降噪/音量均衡/音频美化等。

## 两种使用模式

> 1. **模板模式**（推荐）：使用 `--template` 参数指定大模型增强模板 ID（327001-327032），默认采用真人场景
> 2. **自定义参数模式**：通过 `--preset`、`--diffusion-type` 等参数自定义增强配置
>
> **注意**：两种模式互斥，使用 `--template` 时其他增强参数将被忽略。

## 模板 ID 速查表

| 场景 | 720P | 1080P | 2K | 4K |
|------|------|-------|----|----|
| 真人（Real，人脸与文字区域保护）**默认** | 327001 | 327003 | 327005 | 327007 |
| 漫剧（Anime，动漫线条色块增强） | 327002 | 327004 | 327006 | 327008 |
| 抖动优化（JitterOpt，减少帧间抖动） | 327009 | 327010 | 327011 | 327012 |
| 细节最强（DetailMax，最大化纹理细节） | 327013 | 327014 | 327015 | 327016 |
| 人脸保真（FaceFidelity，保留人脸五官） | 327017 | 327018 | 327019 | 327020 |
| 老片/低清修复（OldFilm，综合增强+人脸增强+去划痕） | 327021 | 327022 | 327023 | 327024 |
| 真人小脸优化（RealSmallFace，远景小脸优化） | 327025 | 327026 | 327027 | 327028 |
| 漫剧小脸优化（AnimeSmallFace，远景小脸优化） | 327029 | 327030 | 327031 | 327032 |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL 地址 |
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-region`/`--cos-input-key` 配合，推荐）|
| `--cos-input-region` | 输入 COS Bucket 区域（如 `ap-guangzhou`）|
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`，**推荐**）|
| `--template` | **大模型增强模板 ID**（模板模式）：`327001`-`327032` |
| `--preset` | 大模型增强预设（自定义模式）：`diffusion` / `comprehensive` / `artifact` |
| `--diffusion-type` | 扩散增强强度：`weak` / `normal` / `strong` |
| `--comprehensive-type` | 综合增强强度：`weak` / `normal` / `strong` |
| `--artifact-type` | 去伪影强度：`weak` / `strong` |
| `--scene-type` | 增强场景：`common` / `AIGC` / `short_play` / `short_video` / `game` / `HD_movie_series` / `LQ_material` / `lecture` |
| `--super-resolution` | 开启超分辨率（2倍，不可与大模型增强同时使用）|
| `--sr-type` | 超分类型：`lq`（低清有噪，默认）/ `hq`（高清）|
| `--sr-size` | 超分倍数，目前仅支持 `2`（默认 2）|
| `--denoise` | 开启视频降噪（不可与大模型增强同时使用）|
| `--denoise-type` | 降噪强度：`weak`（默认）/ `strong` |
| `--color-enhance` | 开启色彩增强 |
| `--color-enhance-type` | 色彩增强强度：`weak`（默认）/ `normal` / `strong` |
| `--low-light-enhance` | 开启低光照增强 |
| `--scratch-repair` | 划痕修复强度（浮点数 0.0-1.0），适合老片修复 |
| `--hdr` | 开启 HDR 增强，可选 `HDR10` / `HLG` |
| `--frame-rate` | 开启插帧，目标帧率（Hz），如 `60` |
| `--audio-denoise` | 开启音频降噪 |
| `--audio-separate` | 音频分离：`vocal`（提取人声）/ `background`（提取背景声）/ `accompaniment`（提取伴奏）。**无默认值，必须由用户明确指定，不得猜测**|
| `--volume-balance` | 开启音量均衡 |
| `--volume-balance-type` | 音量均衡类型：`loudNorm`（响度标准化，默认）/ `gainControl` |
| `--audio-beautify` | 开启音频美化（杂音去除 + 齿音压制）|
| `--codec` | 输出视频编码：`h264` / `h265`（默认）/ `h266` / `av1` / `vp9` |
| `--width` | 输出视频宽度/长边（像素）|
| `--height` | 输出视频高度/短边（像素），`0` 表示按比例缩放 |
| `--bitrate` | 输出视频码率（kbps），`0` 表示自动 |
| `--fps` | 输出视频帧率（Hz），`0` 表示保持原始 |
| `--container` | 输出封装格式：`mp4`（默认）/ `hls` / `flv` |
| `--audio-codec` | 输出音频编码：`aac`（默认）/ `mp3` / `copy` |
| `--audio-bitrate` | 输出音频码率（kbps），默认 `128` |
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量）|
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量）|
| `--output-dir` | 输出目录，默认 `/output/enhance/` |
| `--output-object-path` | 输出文件路径，如 `/output/{inputName}_enhance.{format}` |
| `--no-wait` | 仅提交任务，不等待结果（默认自动轮询）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800（30 分钟）|
| `--download-dir` | 任务完成后将输出文件下载到指定本地目录（默认仅打印预签名 URL）|
| `--compare [路径]` | 任务完成后自动生成效果对比 HTML 页面；可选指定输出路径，省略则自动命名 |
| `--notify-url` | 任务完成回调 URL（可选）|
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## 强制规则

- **音频分离追问规则**：只有当用户**完全没有指明**要分离哪种音轨（如只说"提取音轨"、"音频分离"）时，才追问："请问您需要提取哪种音轨？人声（vocal）、伴奏（accompaniment）还是背景声（background）？"
- **已有明确意图时直接生成命令**：若用户说"人声和背景音乐分离"，意图已明确（vocal + accompaniment），直接生成**两条独立命令**，分别加 `--audio-separate vocal` 和 `--audio-separate accompaniment`，不得追问。
- **视频增强默认使用真人模板**：使用模板模式时，若用户未说明视频类型，**默认选用真人模板**（720P→327001，1080P→327003，2K→327005，4K→327007），无需追问直接生成命令；若用户明确说明是漫剧/动画，再使用对应漫剧模板。
- 音频分离与画质增强互斥，不可同时使用 `--audio-separate` 和 `--template`/`--preset`。

## 示例命令

```bash
# ===== 大模型增强模板（推荐优先使用） =====

# 真人场景 - 升至 1080P（推荐用于真人实拍视频）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327003

# 真人场景 - 升至 4K（超高清修复）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327007

# 漫剧场景 - 升至 1080P
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327004

# 漫剧场景 - 升至 4K（推荐用于动漫视频超清修复）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327008

# 抖动优化 - 升至 1080P（减少帧间抖动与纹理跳变）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327010

# 细节最强 - 升至 4K（极致细节修复）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327016

# 人脸保真 - 升至 1080P（推荐用于人像/写真/访谈视频）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327018

# ===== 自定义参数模式 =====

# 大模型增强（效果最强）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --preset diffusion --diffusion-type strong

# 综合增强（平衡效果与效率）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --preset comprehensive --comprehensive-type normal

# 去伪影（针对压缩产生的伪影修复）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --preset artifact --artifact-type strong

# 超分 + 降噪 + 色彩增强
python scripts/mps_enhance.py --url https://example.com/video.mp4 --super-resolution --denoise --color-enhance

# HDR + 插帧 60fps
python scripts/mps_enhance.py --url https://example.com/video.mp4 --hdr HDR10 --frame-rate 60

# ===== 音频分离 =====

# 提取人声（去除背景音乐）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-separate vocal

# 提取背景声（去除人声）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-separate background

# 提取伴奏（去除人声，保留音乐）
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-separate accompaniment

# 音频增强：降噪 + 音量均衡 + 美化
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-denoise --volume-balance --audio-beautify

# ===== 输出编码控制 =====

# 增强后输出为 H265 + 1080P + 指定码率
python scripts/mps_enhance.py --url https://example.com/video.mp4 --super-resolution \
    --codec h265 --width 1920 --height 1080 --bitrate 4000

# 异步提交后查询任务状态
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327003 --no-wait
python scripts/mps_get_video_task.py --task-id 1250017490-20260318152230-abcdef123456
```
