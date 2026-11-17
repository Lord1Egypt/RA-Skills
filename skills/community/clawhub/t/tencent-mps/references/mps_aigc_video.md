# AIGC 生视频参数与示例 — `mps_aigc_video.py`

**功能**：AI 生成视频，支持文生视频、图生视频、分镜生成，支持 Hunyuan/Hailuo/Kling/Vidu/OS/GV/Mingmou/PixVerse 模型。
> ⚠️ 生成的视频默认存储 12 小时，请尽快下载使用。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt` | 视频描述文本（最多 2000 字符，未传图片时必填）|
| `--model` | 模型：`Hunyuan`（默认）/ `Hailuo` / `Kling` / `Vidu` / `OS` / `GV` / `Mingmou` / `PixVerse` |
| `--model-version` | 模型版本。Kling: `1.6`/`2.0`/`2.1`/`2.5`/`O1`/`2.6`/`3.0`/`3.0-Omni`；Hailuo: `02`/`2.3`/`2.3-fast`/`H3`；Vidu: `q2`/`q2-pro`/`q2-turbo`/`q3`/`q3-pro`/`q3-turbo`/`q3-mix`；GV: `3.1`/`3.1-fast`；OS: `2.0`；PixVerse: `v5.6`/`v6`/`c1` |
| `--scene-type` | 场景类型（严格模型映射）：`motion_control`（Kling 动作控制）/ `land2port`（Mingmou 横转竖）/ `template_effect`（Vidu 特效模板）/ `3d_scene`（Hunyuan 3D 场景，自动使用 ModelVersion=3d_2.0）|
| `--multi-shot` | **Kling 专属**。启用分镜功能 |
| `--multi-prompts-json` | **Kling 专属**。多分镜配置（JSON 数组），每个分镜含 `index`、`prompt`、`duration`。限制：1-6 个分镜，每个提示词最长 512 字符，所有时长之和必须等于总时长 |
| `--negative-prompt` | 负向提示词 |
| `--enhance-prompt` | 开启提示词增强 |
| `--image-url` | 参考图（首帧）URL（单张，图生视频时使用）|
| `--last-image-url` | 参考图（尾帧）URL（部分模型支持，需同时传 `--image-url`；**Hailuo H3 例外，首帧/尾帧是彼此独立的上限，可单独指定尾帧**）|
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
| `--duration` | 视频时长（秒）。**详见下方「时长行为与本地校验策略」**——各模型对非法时长的反应不同（明确报错 / 静默忽略），脚本只在「静默忽略」的场景做本地拦截 |
| `--resolution` | 分辨率：`720P` / `1080P` / `2K` / `4K` |
| `--aspect-ratio` | 宽高比（如 `16:9`, `9:16`, `1:1`, `4:3`, `3:4`）。**PixVerse 支持 8 种**：`16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `2:3` / `3:2` / `21:9` |
| `--quality` | 视频画质（**仅 PixVerse 支持**）：`360p` / `540p` / `720p` / `1080p`。底层走 `ExtraParameters.Quality` 传给 MPS（MPS 后端会映射到 PixVerse 原生字段）|
| `--generate-audio` | 是否生成音效（**仅 PixVerse 支持**）：`true` / `false`。底层走 `ExtraParameters.EnableAudio`（MPS 后端会映射到 PixVerse 的 `generate_audio_switch`）；开启后 PixVerse 会根据视频内容自动生成匹配的环境音/音效 |
| `--no-logo` | 去除水印（Hailuo/Kling/Vidu 支持）|
| `--enable-bgm` | 启用背景音乐（部分模型版本支持）|
| `--enable-audio` | 是否为视频生成音频（GV/OS 支持，可选值: `true`/`false`）|
| `--ref-video-url` | 参考视频 URL（仅 Kling O1 / Kling 3.0-Omni / Vidu q2-pro / H2 **1.0** / Hailuo H3 支持）|
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

## Hailuo H3（MiniMax H3，2026-07-31 发布）

原生多模态理解与生成：支持文字、图片、音频、视频多种输入输出，覆盖影视、广告、游戏、品牌、电商等商用场景。

### 两种输入模式（互斥）

| 模式 | 含义 | 对应参数 |
|------|------|----------|
| i2va | 图生视频（首帧 / 尾帧） | `--image-url` / `--last-image-url` 及其 COS / local 变体 |
| r2va | 多模态参考生成（参考视频 / 参考音频） | `--ref-video-url` / `--ref-audio-url` 及其 COS / local 变体 |

> ⚠️ i2va 与 r2va **不可混用**，脚本会在提交前拦截并提示。参考图（`--ref-image-url`）不属于 i2va，可与参考音频/视频并存。

### 图片输入限制（首帧 / 尾帧 / 参考图）

| 项目 | 限制 |
|------|------|
| 支持格式 | JPG、JPEG、PNG、WEBP、HEIC、HEIF |
| 单文件大小 | ≤ 30 MB |
| 宽高范围 | [256, 5760] px |
| 宽高比 (w/h) | [0.4, 2.5] |
| 数量 | 首帧 ≤ 1，尾帧 ≤ 1，参考图 ≤ 9 |

> 三条数量限制彼此**独立**，不是一个总额。「9 张参考图 + 1 尾帧」是合法组合。
> 与其他模型不同，H3 的尾帧**无需**搭配首帧，可单独指定。

### 视频输入限制（参考生成场景）

| 项目 | 限制 |
|------|------|
| 容器/格式 | MP4 (.mp4)、MOV (.mov) |
| 编码 | 视频 H.264/AVC、H.265/HEVC；音频 AAC、MP3 |
| 单文件大小 | ≤ 50 MB |
| 数量 | ≤ 3 |
| 单片段时长 | [2, 15] 秒；总时长 ≤ 15 秒 |
| 宽高范围 | [256, 5760] px |
| 宽高比 (w/h) | [0.4, 2.5] |
| 帧率 | [23.976, 60] |

### 音频输入限制（参考生成场景）

| 项目 | 限制 |
|------|------|
| 支持格式 | WAV、MP3 |
| 单文件大小 | ≤ 15 MB |
| 数量 | ≤ 3 |
| 单片段时长 | [2, 15] 秒；总时长 ≤ 15 秒 |

> 脚本本地只校验**数量上限**与 **i2va/r2va 互斥**；格式、文件大小、宽高、时长、帧率由接口侧校验。

### 调用示例

```bash
# 纯文生视频
python3 scripts/mps_aigc_video.py --model Hailuo --model-version H3 \
    --prompt "生成一个小女孩，手中举着一个风筝，在操场上，面向镜头向前跑，环绕镜头，从正对角色，逐渐绕向身后。电影级画质"

# i2va：首帧
python3 scripts/mps_aigc_video.py --model Hailuo --model-version H3 \
    --prompt "缓慢推近" --image-url https://example.com/first.jpg

# i2va：首尾帧
python3 scripts/mps_aigc_video.py --model Hailuo --model-version H3 \
    --prompt "花朵绽放" --image-url https://example.com/a.jpg \
    --last-image-url https://example.com/b.jpg

# r2va：参考视频（最多 3 个）
python3 scripts/mps_aigc_video.py --model Hailuo --model-version H3 \
    --prompt "延续参考视频的镜头风格" \
    --ref-video-url https://example.com/ref1.mp4 \
    --ref-video-url https://example.com/ref2.mp4

# r2va：参考音频（最多 3 个，支持本地文件自动上传）
python3 scripts/mps_aigc_video.py --model Hailuo --model-version H3 \
    --prompt "画面节奏与参考音频匹配" --ref-audio-local ./bgm.mp3
```

### 实测输出规格

2026-08-02 实测（纯文生，未指定时长与分辨率）：

| 项目 | 实测值 |
|------|--------|
| 分辨率 | 2560x1440（与官方文档一致） |
| 时长 | 5.167 s（未指定 `--duration` 时由模型决定） |
| 视频编码 | H.264，24 fps，124 帧 |
| 音频 | AAC 32 kHz 立体声（**原生生成，未显式开启**） |
| 码率 / 体积 | 13.4 Mbps / 8.6 MB |

### 时长与分辨率（2026-08-02 逐值真接口实测）

| 参数 | 实测结论 |
|------|----------|
| `--duration` | **4~15 秒连续区间**，区间内任意整数均生效（4→4.46s、7→7.29s、12→12.25s、15→15.08s 等逐个验证）|
| `--duration` 越界 | 3 / 16 / 20 等被接口**静默忽略**，任务仍返回 `DONE` 但产物回落默认约 5.17s |
| `--resolution` | **仅 `4K` 生效**（3840x2160）；`720P` / `1080P` / `2K` 均输出原生 2560x1440 |
| `--resolution` 副作用 | 4K 档音频采样率为 44100Hz，其余档均为 32000Hz |
| 并发 | 连续提交约第 11 个起触发 `RequestLimitExceeded`，批量任务需间隔约 20s |

> ⚠️ 上述两个参数越界/无效时**接口不会报错**，只是悄悄丢弃参数。脚本已对 H3 做前置拦截并给出明确提示，避免误以为参数生效。

> H3 原生输出音轨，无需 `--generate-audio` 等开关；这与需要显式开启有声的模型不同。
> 产物会写回配置的 COS 桶永久保存，并附带 24 小时临时签名链接。

## 时长行为与本地校验策略

`--duration` 的取值约束**因模型而异**，且各模型对非法值的反应分两类，直接决定脚本是否做本地校验：

| 模型 | 实测有效时长 | 非法值的反应 | 脚本是否本地校验 |
|------|------|------|------|
| Hailuo 02 / 2.3 / 2.3-fast | **仅 6 / 10 秒** | ⚠️ **静默忽略**，回落默认约 5.88s，任务仍 `DONE` | ✅ **校验**（不拦用户会拿到错时长而不自知）|
| Hailuo H3 | 4~15 秒连续区间 | ⚠️ 静默忽略，回落约 5.17s | ✅ 校验（`h3_limits.duration_range`）|
| PixVerse | 1~15 秒任意整数 | ❌ 接口明确报错（16s 起）| ✅ 校验（与实测完全吻合）|
| Kling | 实测 3 / 5 / 7 / 10s 均**精确生效** | ❌ 接口明确报错（`duration value '20' is invalid`）| ❌ 不校验 |
| Vidu | 实测 5s 生效；12 / 16s 失败 | ❌ 接口明确报错（上游 Vidu 拒绝）| ❌ 不校验 |
| OS | 实测 4 / 8 / 12s 均精确生效 | ❌ 接口明确报错 | ❌ 不校验 |
| GV | 实测 **4s / 8s 均精确生效** | ❌ 接口明确报错 | ❌ 不校验 |

**为什么不对 Kling / Vidu / OS / GV 做本地白名单**（2026-08-08 实测结论）：

这些模型越界时接口会**明确报错**，用户能立即感知，接口报错比本地白名单更准确也不会过期。反之，硬编码白名单会**误拒合法值**——实测 Kling 的 3s / 7s、GV 的 4s 都能精确生效，但旧配置里 Kling 只写了 `[5,10]`、GV 只写了 `[8]`，一旦接上校验就会拦掉这些正常请求。

> ⚠️ **Hailuo 2.3-fast 不支持文生视频**：实测接口报 `model MiniMax-Hailuo-2.3-Fast does not support Text-to-Video mode`，必须传首帧图（`--image-url` / `--image-cos-key` / `--image-local`），脚本已前置拦截。纯文本生成请改用 02 / 2.3 / H3。

## ⚠️ 强制规则（违反将导致命令执行失败）

- **🚫 参考视频仅部分模型支持**：当用户请求使用参考视频（`--ref-video-url` 或 `--ref-video-cos-key`）时，**必须使用支持该能力的模型 + 版本组合**：
  - `--model Kling --model-version O1` 或 `--model Kling --model-version 3.0-Omni`（可作为特征参考视频或待编辑视频，支持保留原声）
  - `--model Vidu --model-version q2-pro`（支持视频参考；最多 1 个 8s 视频 或 2 个 5s 视频）
    实测：Vidu 参考视频**仅 q2-pro** 支持，`q2` / `q2-turbo` / `q3` / `q3-pro` 均返回 `FieldLacking`
  - `--model H2 --model-version 1.0`（**参考视频仅 1.0 支持**，实测 1.1 传参考视频报 `Model not exist`）
  - `--model Hailuo --model-version H3`（多模态参考生成 r2va，参考视频 ≤ 3；**与首帧/尾帧互斥**）
  其他模型或不匹配的版本（如 Kling 3.0、Vidu q2、PixVerse、Hunyuan，以及 **Hailuo 02 / 2.3 / 2.3-fast**）**不支持**参考视频；如果用户指定了不支持的组合，**必须拒绝并提示**用户改用上述支持组合之一。
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
  如果用户要求 PixVerse 做分镜（`--multi-shot`）或参考视频（`--ref-video-url`），**必须拒绝**：分镜功能仅 Kling 支持，参考视频仅 Kling O1 / 3.0-Omni / Vidu q2-pro / H2 1.0 / Hailuo H3 支持。
- **AIGC 生视频 API 的图片参数只支持 URL**（`ImageUrl`/`LastImageUrl`），不支持 CosInputInfo。使用 `--image-cos-key` / `--last-image-cos-key` / `--ref-image-cos-key` 时，脚本会自动生成预签名 URL 后传入 API（需配置 `TENCENTCLOUD_SECRET_ID/KEY`）。
- 用户提供 bucket/region/key 时，必须完整传入这三个参数，不得省略。

```bash
# COS 图生视频（脚本自动将 COS Key 转为预签名 URL 后传入 API）
python3 scripts/mps_aigc_video.py --prompt "花朵随风摇曳" \
    --image-cos-bucket mps-test-1234567 \
    --image-cos-region ap-guangzhou \
    --image-cos-key input/scene.jpg
```

## 分镜功能说明（Kling 专属）

### 单分镜模式（系统自动拆分）
```bash
python3 scripts/mps_aigc_video.py --prompt "旅行日记，记录美好瞬间" --model Kling --multi-shot
```

### 多分镜模式（自定义每个分镜）
```bash
python3 scripts/mps_aigc_video.py --model Kling --multi-shot --duration 12 \
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
python3 scripts/mps_aigc_video.py --prompt "一只猫在阳光下伸懒腰"

# Kling 2.5 + 10秒 + 1080P + 16:9 + 去水印 + BGM
python3 scripts/mps_aigc_video.py --prompt "赛博朋克城市" --model Kling --model-version 2.5 \
    --duration 10 --resolution 1080P --aspect-ratio 16:9 --no-logo --enable-bgm

# 图生视频（首帧图片 + 描述）
python3 scripts/mps_aigc_video.py --prompt "让画面动起来" \
    --image-url https://example.com/photo.jpg

# 首尾帧生视频（GV 模型）
python3 scripts/mps_aigc_video.py --prompt "过渡动画" --model GV \
    --image-url https://example.com/start.jpg --last-image-url https://example.com/end.jpg

# GV 多图参考生视频（支持 asset/style 参考类型）
python3 scripts/mps_aigc_video.py --prompt "融合风格生成视频" --model GV \
    --ref-image-url https://example.com/img1.jpg --ref-image-type asset \
    --ref-image-url https://example.com/img2.jpg --ref-image-type style

# OS 文生视频（默认 8s，支持 4/8/12s）
python3 scripts/mps_aigc_video.py --prompt "海边日落场景" --model OS --model-version 2.0

# OS 长视频 12s + 开启音频生成
python3 scripts/mps_aigc_video.py --prompt "夜市街头人流涌动" --model OS --duration 12 --enable-audio true

# Kling 参考视频 + 保留原声
python3 scripts/mps_aigc_video.py --prompt "将视频风格化" --model Kling --model-version O1 \
    --ref-video-url https://example.com/video.mp4 --ref-video-type base --keep-original-sound yes

# Mingmou 横转竖（land2port 场景不需要输入视频文件，只需 prompt 描述即可生成竖屏视频）
python3 scripts/mps_aigc_video.py --prompt "横屏转竖屏" --model Mingmou --scene-type land2port

# COS 参考视频（自动生成预签名 URL，Kling O1）
python3 scripts/mps_aigc_video.py --prompt "将视频风格化" --model Kling --model-version O1 \
    --ref-video-cos-bucket mybucket-125xxx --ref-video-cos-region ap-guangzhou \
    --ref-video-cos-key /input/video.mp4 --ref-video-type base --keep-original-sound yes

# Vidu q2-pro 参考视频（视频编辑 / 视频替换场景）
python3 scripts/mps_aigc_video.py --prompt "把画面变成赛博朋克风格" --model Vidu --model-version q2-pro \
    --ref-video-url https://example.com/video.mp4 --ref-video-type base

# Vidu 错峰模式
python3 scripts/mps_aigc_video.py --prompt "自然风景" --model Vidu --off-peak

# === PixVerse 模型示例 ===
# PixVerse v6 文生视频（电影宽屏 21:9，10 秒，1080p 画质）
python3 scripts/mps_aigc_video.py --prompt "电影级城市天际线镜头" --model PixVerse --model-version v6 \
    --duration 10 --aspect-ratio 21:9 --quality 1080p

# PixVerse v6 文生视频 + 自动音效（雨夜氛围、环境音由模型生成）
python3 scripts/mps_aigc_video.py --prompt "雨夜霓虹街道，行人独自漫步" --model PixVerse --model-version v6 \
    --duration 15 --aspect-ratio 16:9 --quality 720p --generate-audio true

# PixVerse c1 图生视频（短视频 9:16，5 秒，540p 画质）
python3 scripts/mps_aigc_video.py --prompt "人物缓步前行，微风吹过发丝" \
    --model PixVerse --model-version c1 \
    --image-url https://example.com/first-frame.jpg --duration 5 --aspect-ratio 9:16 --quality 540p

# PixVerse c1 文生视频（正方形 1:1，3 秒，720p 画质）
python3 scripts/mps_aigc_video.py --prompt "咖啡拉花特写" --model PixVerse --model-version c1 \
    --duration 3 --aspect-ratio 1:1 --quality 720p

# 仅提交任务不等待
python3 scripts/mps_aigc_video.py --prompt "宣传片" --no-wait

# 查询任务结果
python3 scripts/mps_aigc_video.py --task-id abc123def456-aigc-video-20260328112000
```
