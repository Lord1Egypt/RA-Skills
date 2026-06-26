# AIGC 生视频参数与示例 — `mps_aigc_video.py`

**功能**：AI 生成视频，支持文生视频、图生视频、分镜生成，支持 Hunyuan/Hailuo/Kling/Vidu/OS/GV/Mingmou/PixVerse 模型。
> ⚠️ 生成的视频默认存储 12 小时，请尽快下载使用。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt` | 视频描述文本（最多 2000 字符，未传图片时必填）|
| `--model` | 模型：`Hunyuan`（默认）/ `Hailuo` / `Kling` / `Vidu` / `OS` / `GV` / `Mingmou` / `PixVerse` |
| `--model-version` | 模型版本。Kling: `1.6`/`2.0`/`2.1`/`2.5`/`O1`/`2.6`/`3.0`/`3.0-Omni`；Hailuo: `02`/`2.3`/`2.3-fast`；Vidu: `q2`/`q2-pro`/`q2-turbo`/`q3`/`q3-pro`/`q3-turbo`/`q3-mix`；GV: `3.1`/`3.1-fast`；PixVerse: `v5.6`/`v6`/`c1` |
| `--scene-type` | 场景类型（严格模型映射）：`motion_control`（Kling 动作控制）/ `land2port`（Mingmou 横转竖）/ `template_effect`（Vidu 特效模板）/ `3d_scene`（Hunyuan 3D 场景，自动使用 ModelVersion=3d_2.0）|
| `--multi-shot` | **Kling 专属**。启用分镜功能 |
| `--multi-prompts-json` | **Kling 专属**。多分镜配置（JSON 数组），每个分镜含 `index`、`prompt`、`duration`。限制：1-6 个分镜，每个提示词最长 512 字符，所有时长之和必须等于总时长 |
| `--negative-prompt` | 负向提示词 |
| `--enhance-prompt` | 开启提示词增强 |
| `--image-url` | 参考图（首帧）URL（单张，图生视频时使用）|
| `--last-image-url` | 参考图（尾帧）URL（部分模型支持，需同时传 `--image-url`）|
| `--image-cos-bucket` | 首帧图片所在 COS Bucket（脚本自动生成预签名 URL 后以 ImageUrl 传入 API）|
| `--image-cos-region` | 首帧图片所在 COS Region |
| `--image-cos-key` | 首帧图片的 COS Key |
| `--image-local` | **首帧本地图片路径**，自动上传 COS 后以 ImageUrl 传入。需配置 `TENCENTCLOUD_COS_BUCKET` 或 `--cos-bucket-name` |
| `--last-image-cos-bucket` | 尾帧图片所在 COS Bucket（脚本自动生成预签名 URL 后以 LastImageUrl 传入 API）|
| `--last-image-cos-region` | 尾帧图片所在 COS Region |
| `--last-image-cos-key` | 尾帧图片的 COS Key |
| `--last-image-local` | **尾帧本地图片路径**，自动上传 COS 后以 LastImageUrl 传入。需配置 `TENCENTCLOUD_COS_BUCKET` 或 `--cos-bucket-name` |
| `--ref-image-url` | 多图参考 URL（可多次指定，GV/Vidu 支持，最多 3 张）|
| `--ref-image-type` | 多图参考类型（与所有来源参考图按顺序一一对应，依次覆盖 `--ref-image-url` / `--ref-image-cos-key` / `--ref-image-local`）：`asset`（内容参考）/ `style`（风格参考）|
| `--ref-image-cos-bucket` | 多图参考所在 COS Bucket（可多次指定，脚本自动生成预签名 URL 后传入 API）|
| `--ref-image-cos-region` | 多图参考所在 COS Region（可多次指定）|
| `--ref-image-cos-key` | 多图参考的 COS Key（可多次指定）|
| `--ref-image-local` | **多图参考本地图片路径**（可多次指定），自动上传 COS 后以 ImageUrl 传入。需配置 `TENCENTCLOUD_COS_BUCKET` 或 `--cos-bucket-name` |
| `--duration` | 视频时长（秒）。各模型支持范围：<br>- Hunyuan: 默认 5s<br>- Hailuo: 6s（默认）/ 10s<br>- Kling: 5s / 10s，默认 5s<br>- Vidu: 1~10s，默认 4s<br>- OS: 5s / 10s，默认 5s<br>- GV: 5s / 10s，默认 5s<br>- **PixVerse: 1~15s 任意整数，默认 5s** |
| `--resolution` | 分辨率：`720P` / `1080P` / `2K` / `4K` |
| `--aspect-ratio` | 宽高比（如 `16:9`, `9:16`, `1:1`, `4:3`, `3:4`）。**PixVerse 支持 8 种**：`16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `2:3` / `3:2` / `21:9` |
| `--quality` | 视频画质（**仅 PixVerse 支持**）：`360p` / `540p` / `720p` / `1080p`。底层走 `ExtraParameters.Quality` 传给 MPS（MPS 后端会映射到 PixVerse 原生字段）|
| `--generate-audio` | 是否生成音效（**仅 PixVerse 支持**）：`true` / `false`。底层走 `ExtraParameters.EnableAudio`（MPS 后端会映射到 PixVerse 的 `generate_audio_switch`）；开启后 PixVerse 会根据视频内容自动生成匹配的环境音/音效 |
| `--no-logo` | 去除水印（Hailuo/Kling/Vidu 支持）|
| `--enable-bgm` | 启用背景音乐（部分模型版本支持）|
| `--enable-audio` | 是否为视频生成音频（GV/OS 支持，可选值: `true`/`false`）|
| `--ref-video-url` | 参考视频 URL（仅 Kling 模型支持）|
| `--ref-video-type` | 参考视频类型：`feature`（特征参考）/ `base`（待编辑视频，默认）|
| `--keep-original-sound` | 保留原声：`yes` / `no` |
| `--ref-video-cos-bucket` | 参考视频所在 COS Bucket（可多次指定）|
| `--ref-video-cos-region` | 参考视频所在 COS Region（可多次指定）|
| `--ref-video-cos-key` | 参考视频的 COS Key（可多次指定，自动生成预签名 URL 填入 VideoUrl）|
| `--off-peak` | 错峰模式（仅 Vidu），任务 48 小时内生成 |
| `--additional-params` | JSON 格式附加参数，用于传递模型专属扩展参数（如 Kling 相机控制）|
| `--no-wait` | 只提交任务，不等待结果 |
| `--task-id` | 查询已有任务结果 |
| `--cos-bucket-name` | 结果存储 COS Bucket（不配置则使用 MPS 临时存储 12 小时）|
| `--cos-bucket-region` | 结果存储 COS 区域 |
| `--cos-bucket-path` | 结果存储 COS 路径前缀，默认 `/output/aigc-video/` |
| `--download-dir` | 任务完成后将生成视频下载到指定本地目录（默认仅打印预签名 URL）|
| `--operator` | 操作者名称（可选）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800 |
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## ⚠️ 强制规则（违反将导致命令执行失败）

- **🚫 参考视频仅 Kling 模型支持**：当用户请求使用参考视频（`--ref-video-url` 或 `--ref-video-cos-key`）时，**必须使用 `--model Kling`**，其他模型不支持参考视频。如果用户指定了其他模型 + 参考视频，**必须拒绝并提示**用户参考视频仅 Kling 模型支持，建议改用 Kling 模型。
- **🚫 SceneType 严格对应模型**：`--scene-type` 参数**必须**与模型严格对应，**禁止混用**：
  - `motion_control`（动作控制）→ ⚠️ **仅 Kling 模型**
  - `land2port`（横转竖）→ ⚠️ **仅 Mingmou 模型**
  - `template_effect`（特效模板）→ ⚠️ **仅 Vidu 模型**
  - `3d_scene`（3D 场景）→ ⚠️ **仅 Hunyuan 模型**（自动配合 ModelVersion=3d_2.0）
  如果用户指定了不匹配的组合（如"用 Vidu 模型做动作控制"），**必须拒绝并提示**用户该场景类型仅支持对应模型（如"motion_control 仅 Kling 支持，请改用 Kling 模型"）。
- **Mingmou 横转竖（land2port）不需要输入视频文件**：该场景通过 prompt 描述即可生成竖屏视频，**不要追问用户输入视频来源**，直接使用 `--prompt` 参数生成命令。
- **PixVerse 模型参数严格校验**：
  - `--model-version` 必须是 `v5.6` / `v6` / `c1` 三者之一（默认不传时由后端兜底）
  - `--aspect-ratio` 必须是 8 种之一：`16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `2:3` / `3:2` / `21:9`
  - `--duration` 必须是 1~15 秒之间的整数
  - `--quality` 必须是 `360p` / `540p` / `720p` / `1080p` 之一（走 `ExtraParameters.Quality`，仅 PixVerse 支持）
  - `--generate-audio` 必须是 `true` / `false`（走 `ExtraParameters.EnableAudio`，MPS 后端会映射到 PixVerse 的 `generate_audio_switch`，仅 PixVerse 支持，开启后自动生成与画面匹配的音效）
  如果用户要求 PixVerse 做分镜（`--multi-shot`）或参考视频（`--ref-video-url`），**必须拒绝**，该能力仅 Kling 支持。
- **AIGC 生视频 API 的图片参数只支持 URL**（`ImageUrl`/`LastImageUrl`），不支持 CosInputInfo。使用 `--image-cos-key` / `--last-image-cos-key` / `--ref-image-cos-key` 时，脚本会自动生成预签名 URL 后传入 API（需配置 `TENCENTCLOUD_SECRET_ID/KEY`）。
- 用户提供 bucket/region/key 时，必须完整传入这三个参数，不得省略。

```bash
# COS 图生视频（脚本自动将 COS Key 转为预签名 URL 后传入 API）
python scripts/mps_aigc_video.py --prompt "花朵随风摇曳" \
    --image-cos-bucket mps-test-1234567 \
    --image-cos-region ap-guangzhou \
    --image-cos-key input/scene.jpg
```

## 分镜功能说明（Kling 专属）

### 单分镜模式（系统自动拆分）
```bash
python scripts/mps_aigc_video.py --prompt "旅行日记，记录美好瞬间" --model Kling --multi-shot
```

### 多分镜模式（自定义每个分镜）
```bash
python scripts/mps_aigc_video.py --model Kling --multi-shot --duration 12 \
    --multi-prompts-json '[
      {"index": 1, "prompt": "日出时分，从酒店窗户看城市天际线", "duration": "3"},
      {"index": 2, "prompt": "在咖啡馆享用早餐，窗外街道行人", "duration": "4"},
      {"index": 3, "prompt": "公园里散步，阳光透过树叶", "duration": "5"}
    ]'
```

**校验规则**：分镜数量 1-6 个；每个提示词最长 512 字符；每个时长 ≥ 1 秒；所有时长之和必须等于总时长。

## 示例命令

```bash
# 文生视频（Hunyuan 默认）
python scripts/mps_aigc_video.py --prompt "一只猫在阳光下伸懒腰"

# Kling 2.5 + 10秒 + 1080P + 16:9 + 去水印 + BGM
python scripts/mps_aigc_video.py --prompt "赛博朋克城市" --model Kling --model-version 2.5 \
    --duration 10 --resolution 1080P --aspect-ratio 16:9 --no-logo --enable-bgm

# 图生视频（首帧图片 + 描述）
python scripts/mps_aigc_video.py --prompt "让画面动起来" \
    --image-url https://example.com/photo.jpg

# 首尾帧生视频（GV 模型）
python scripts/mps_aigc_video.py --prompt "过渡动画" --model GV \
    --image-url https://example.com/start.jpg --last-image-url https://example.com/end.jpg

# GV 多图参考生视频（支持 asset/style 参考类型）
python scripts/mps_aigc_video.py --prompt "融合风格生成视频" --model GV \
    --ref-image-url https://example.com/img1.jpg --ref-image-type asset \
    --ref-image-url https://example.com/img2.jpg --ref-image-type style

# Kling 参考视频 + 保留原声
python scripts/mps_aigc_video.py --prompt "将视频风格化" --model Kling --model-version O1 \
    --ref-video-url https://example.com/video.mp4 --ref-video-type base --keep-original-sound yes

# Mingmou 横转竖（land2port 场景不需要输入视频文件，只需 prompt 描述即可生成竖屏视频）
python scripts/mps_aigc_video.py --prompt "横屏转竖屏" --model Mingmou --scene-type land2port

# COS 参考视频（自动生成预签名 URL）
python scripts/mps_aigc_video.py --prompt "将视频风格化" --model Kling \
    --ref-video-cos-bucket mybucket-125xxx --ref-video-cos-region ap-guangzhou \
    --ref-video-cos-key /input/video.mp4 --ref-video-type base --keep-original-sound yes

# Vidu 错峰模式
python scripts/mps_aigc_video.py --prompt "自然风景" --model Vidu --off-peak

# === PixVerse 模型示例 ===
# PixVerse v6 文生视频（电影宽屏 21:9，10 秒，1080p 画质）
python scripts/mps_aigc_video.py --prompt "电影级城市天际线镜头" --model PixVerse --model-version v6 \
    --duration 10 --aspect-ratio 21:9 --quality 1080p

# PixVerse v6 文生视频 + 自动音效（雨夜氛围、环境音由模型生成）
python scripts/mps_aigc_video.py --prompt "雨夜霓虹街道，行人独自漫步" --model PixVerse --model-version v6 \
    --duration 15 --aspect-ratio 16:9 --quality 720p --generate-audio true

# PixVerse c1 图生视频（短视频 9:16，5 秒，540p 画质）
python scripts/mps_aigc_video.py --prompt "人物缓步前行，微风吹过发丝" \
    --model PixVerse --model-version c1 \
    --image-url https://example.com/first-frame.jpg --duration 5 --aspect-ratio 9:16 --quality 540p

# PixVerse c1 文生视频（正方形 1:1，3 秒，720p 画质）
python scripts/mps_aigc_video.py --prompt "咖啡拉花特写" --model PixVerse --model-version c1 \
    --duration 3 --aspect-ratio 1:1 --quality 720p

# 仅提交任务不等待
python scripts/mps_aigc_video.py --prompt "宣传片" --no-wait

# 查询任务结果
python scripts/mps_aigc_video.py --task-id abc123def456-aigc-video-20260328112000
```
