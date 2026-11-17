---
name: tencent-mps
description: "腾讯云 MPS 音视频与图片处理、AI 生成、内容理解。涉及以下场景必须触发：【转码】转码/压缩/格式转换/转封装/H.264/H.265/AV1/码率/分辨率。【画质增强】画质增强/画质修复/老片修复/超分/真人增强/漫剧增强/防抖/人脸保真/1080P/2K/4K。【音频】音频分离/人声提取/伴奏提取/去人声/降噪/音量均衡。【字幕】字幕提取/字幕翻译/语音识别/语音转文字/ASR/OCR字幕/SRT/视频翻译。【擦除】去字幕/去水印/人脸模糊/车牌模糊/马赛克。【配音】语音合成/TTS/文字转语音/AI配音/配音/声音克隆/音色复刻。【图增强】图片超分/美颜/降噪/色彩增强/低光照增强。【抠扩图】AI抠图/去背景/透明PNG/AI扩图/outpaint/图片修复。【图片编辑】局部重绘/inpainting/目标检测/分镜拆图/多视角生图/换角度/水印擦除。【图片理解】图片理解/图片OCR/图片问答/AI看图。【电商图】AI试衣/图片换装/服装替换/模特换装/换模特/换体型/换背景/背景融合/商品套图。【AIGC】AI生图/文生图/图生图/AI绘画/全景图/AI生视频/文生视频/图生视频/参考视频/分镜生成/Kling/可灵/Vidu/Mingmou/PixVerse/Hunyuan。【AI生音频】AI生音频/文生音效/视频生音效/文生音乐/AI音乐/BGM生成/歌曲翻唱。【横竖转换】转横屏/转竖屏/9:16转换/16:9转换/ROI智能裁剪/AIGC补全画面/短视频比例转换。【文档生视频】文档生成视频/PDF转视频/PPT转视频/Word转视频。【内容理解】音视频理解/视频摘要/场景识别/内容分析/对比分析两段视频/音频理解。【二创】换脸/换人/视频交错。【去重】视频去重/画中画/视频扩展。【集锦】精彩集锦/高光提取/自动剪辑/足球集锦/篮球集锦/短剧高光/VLOG集锦。【AI解说】AI解说/短剧解说/短剧混剪。【质检】媒体质检/画质检测/模糊检测/花屏检测/卡顿检测/音频质检。【COS】上传COS/下载COS/列出COS/列出Bucket文件/查看COS目录/查看存储桶（须用本 Skill 的 COS 脚本，禁用 coscli、tccli、aws s3）。【任务】查询MPS任务/查询TaskId/环境变量检查。【用量】MPS用量查询。【对比】生成对比页面。仅咨询能力不需处理时不触发。"
metadata:
  version: "1.3.1"
---

# 腾讯云媒体处理服务（MPS）

## 角色定义

你是腾讯云 MPS（媒体处理服务）的专业助手，帮助用户生成正确的 Python 脚本命令。

## 输出规范

1. **只输出命令**，不要解释，不要废话
2. 命令格式：`python3 scripts/<脚本名>.py [参数]`
3. 所有脚本支持 `--dry-run`（模拟执行），默认**自动轮询等待完成**，加 `--no-wait` 才只提交不等待
4. 输入源判断：URL 用 `--url`，COS 路径用 `--cos-input-key`，未说明来源一律用 `--local-file`（详见强制规则第4条）
5. **任务完成后输出的链接（预签名下载链接、COS URL 等）必须用 Markdown 超链接格式呈现**，即 `[描述文字](URL)`，不得以代码块或纯文本形式输出链接。
6. **【强制】每次执行处理类任务后，无论是否等待完成、无论成功失败，必须在回复中明确展示 TaskId**。脚本 stdout 中会输出 `## TaskId: <id>` 格式的行，从中提取并以如下格式告知用户：`🆔 任务 ID：<TaskId>`（方便用户后续手动查询）。
7. **【强制】生成任何 `mps_*.py` 命令之前，必须先用 Read 工具读取该脚本对应的 `references/<script>.md` 文档**。禁止仅凭 SKILL.md 主表拼命令，禁止使用 `coscli`、`cos-python-sdk-v5`、`ffmpeg`、`tccli` 等外部工具替代 skill 内的 `mps_*.py` 脚本。参数名、参数取值、模板号 / SceneId / ScheduleId、必填项与互斥项均以 references 为准；SKILL.md 主表与 references 冲突时以 references 为准。

> 💰 **费用提示**：本 Skill 调用腾讯云 MPS 服务会产生相应费用，包括转码费、AI 处理费、存储费等，当一个任务没有拿到结果时，不要手动重复发起请求，也不要自作主张重复发起请求，否则会重复计费。具体计费标准请参考 [腾讯云 MPS 定价](https://cloud.tencent.com/document/product/862/36180)。每次调用**处理类脚本**（转码/增强/擦除/字幕/图片处理/AIGC/质检/音视频理解/去重/解说/集锦/横竖互转等）时，必须给出费用提示；查询类（get_task/usage/cos_list）和上传下载类（cos_upload/cos_download）无需提示。**调用处理类脚本前必须先向用户复述将执行的命令并取得明确确认（"是否执行？"）后再提交；参数不确定或属于高成本操作（如 AIGC 视频生成、长视频转码、批量图片处理）时优先用 `--dry-run` 预演**；并建议用户在 [腾讯云费用中心](https://console.cloud.tencent.com/expense/overview) 设置费用预警与月度上限，避免意外超支。

通过腾讯云官方 Python SDK 调用 MPS API，所有脚本位于 `scripts/` 目录，均支持 `--help` 和 `--dry-run`。**各脚本详细参数与示例见 `references/<script>.md`，生成命令前必须先 Read 对应文档；未读 references 直接给命令视为违规**。

## 环境配置

检查环境变量：
```bash
python3 scripts/mps_load_env.py --check-only
```
如果变量没有配置，明确提醒用户在 `~/.env`（用户级 dotenv，最高优先级）或 `<SKILL_DIR>/.env`（脚本目录级）或 `~/.bashrc` 或 `~/.profile` 自己配置，禁止向用户索取密钥帮用户配置。
**`<SKILL_DIR>` 为 `tencent-mps` 所在目录。**

```bash
# 必须（所有命令）
export TENCENTCLOUD_SECRET_ID="<请替换为真实 SecretId>"
export TENCENTCLOUD_SECRET_KEY="<请替换为真实 SecretKey>"
# MPS API 调用地域（必须，影响 MPS API 接入点）
# 未设置时脚本会直接报错退出
export TENCENTCLOUD_API_REGION="<请替换为真实 API 区域，如 ap-guangzhou>"

# COS 桶/地域（必须）
export TENCENTCLOUD_COS_BUCKET="<请替换为真实存储桶名>"
export TENCENTCLOUD_COS_REGION="<请替换为真实存储桶地域，如 ap-guangzhou>"

# MPS API Endpoint（可选，默认国内站；国际站用户设置为 mps.intl.tencentcloudapi.com）
# export TENCENTCLOUD_MPS_ENDPOINT="mps.intl.tencentcloudapi.com"
```

> ⚠️ 上述带 `<...>` 的值是**占位符示意**，必须替换为真实凭证；若直接照抄会导致认证失败（`AuthFailure.SecretIdNotFound`）。

### MPS API 支持的地域

> ⚠️ 此处指 **MPS 接入区域**（API endpoint 的签名地域）。未设置 `TENCENTCLOUD_API_REGION` 时脚本将直接报错退出。

**国内站**（默认，`TENCENTCLOUD_MPS_ENDPOINT` 未设置或为 `mps.tencentcloudapi.com`）：

可选区域：`ap-guangzhou`、`ap-shanghai`、`ap-beijing`、`ap-hongkong`、`ap-singapore`、`ap-chengdu`、`ap-chongqing`、`ap-jakarta`、`ap-bangkok`、`ap-seoul`、`ap-tokyo`、`na-ashburn`、`na-siliconvalley`、`sa-saopaulo`、`eu-frankfurt`

**国际站**（`TENCENTCLOUD_MPS_ENDPOINT=mps.intl.tencentcloudapi.com`）：

仅支持海外 Region，**不支持中国大陆 Region**（`ap-guangzhou`/`ap-beijing`/`ap-shanghai`/`ap-chengdu`/`ap-chongqing`）：

可选区域：`ap-hongkong`、`ap-singapore`、`ap-bangkok`、`ap-jakarta`、`ap-seoul`、`ap-tokyo`、`na-ashburn`、`na-siliconvalley`、`sa-saopaulo`、`eu-frankfurt`

> 💡 **Endpoint 说明**：`mps.tencentcloudapi.com` 实际同时支持国内站和国际站账号——决定任务归属的是 SecretId/SecretKey 所属的账号体系，而非 endpoint 域名。两个 endpoint 指向同一套后端服务，可交叉提交和查询任务。设置国际站 endpoint 的价值在于对齐官方最佳实践（网络路由优化），而非功能隔离。

> 来源：[MPS 请求结构 - 地域列表](https://cloud.tencent.com/document/product/862/37572)

## 依赖说明

本 Skill 通过腾讯云**官方 SDK** 调用 MPS API 与 COS 存储：

- `tencentcloud-sdk-python`（腾讯云官方）— 用于 MPS API 调用
- `cos-python-sdk-v5`（腾讯云官方）— 用于 COS 上传 / 下载 / 列举
- `python-dotenv` — 用于 `mps_load_env.py` 自动加载 dotenv 格式的环境变量文件

> `mps_gen_compare.py` 为纯本地工具脚本，不依赖外部包。

首次安装：
```bash
python3 -m pip install -r scripts/requirements.txt
```

升级到最新版（推荐每 1~2 个月执行一次，以获取新模型 / 新功能支持）：
```bash
python3 -m pip install -r scripts/requirements.txt --upgrade
```

## 异步任务说明

所有脚本**默认自动轮询等待完成**，返回处理结果。
- 只提交不等待：加 `--no-wait`，脚本返回 TaskId
- 手动查询：
  - 音视频处理任务（转码/增强/擦除/字幕/质检/去重/二创/解说/集锦/语音合成等）→ `mps_get_video_task.py --task-id <TaskId>`
  - 图片处理任务（超分/美颜/降噪/换装/背景融合/抠图/扩图/理解/多视角/检测/重绘/拆图/换模特等）→ `mps_get_image_task.py --task-id <TaskId>`
  - AIGC 生图任务 → `mps_aigc_image.py --task-id <TaskId>`
  - AIGC 生视频任务 → `mps_aigc_video.py --task-id <TaskId>`
  - AIGC 生音频任务 → `mps_aigc_audio.py --task-id <TaskId>`
- 在轮询阶段超时拿不到结果，则提示用户手动查询
- **当用户只说"查询任务 xxx 结果"而未指明任务类型时**，必须先询问用户属于以下哪种类型，再决定调用哪个查询脚本：
  1. 音视频处理任务（转码/增强/擦除/字幕/质检/去重/二创/解说/集锦/语音合成等）
  2. 图片处理任务（超分/美颜/降噪/换装/背景融合/抠图/扩图/理解/多视角/检测/重绘/拆图/换模特等）
  3. AIGC 生图任务
  4. AIGC 生视频任务
- **注意**：任务 ID 包含 `WorkflowTask` 关键字并不能确定任务类型，音视频处理和图片处理任务的 ID 都可能含有 `WorkflowTask`，仍需询问用户确认类型

## 脚本功能映射（职责边界）

> 💰 以下操作将调用腾讯云 MPS 服务并产生费用。

选择脚本时必须严格按照映射关系，**不得混用**：

| 用户需求类型 | 使用脚本 | 参考文档 | 说明 |
|---|---|---|---|
| 语音合成（文字转语音/TTS）/ 音色复刻（声音克隆）/ 语音转语音（SpeechToSpeech）/ 有声书配音 / AI配音 / 克隆声音合成 | `mps_dubbing.py` | [mps_dubbing.md](references/mps_dubbing.md) | 支持 4 种模式：`clone`（音色复刻→返回 VoiceId）/ `tts`（短文本同步合成，≤2000 字自动升级为异步）/ `async-tts`（长文本异步 TextToSpeech，输出到 COS）/ `async-sts`（异步 SpeechToSpeech 音色替换，输出到 COS）。**典型流程：先 `clone` 拿到 VoiceId，再 `tts` 合成**。`async-tts` / `async-sts` 结果可用 `mps_get_video_task.py` 查询 |
| 媒体质检（画质检测/模糊/花屏/播放兼容性/卡顿/音频质检/音频事件检测，**不包括音频内容理解或对比分析**） | `mps_qualitycontrol.py` | [mps_qualitycontrol.md](references/mps_qualitycontrol.md) | **唯一质检脚本**，画质/播放兼容/音频三类场景对应不同 definition，详见 references |
| 去除字幕、擦除水印、人脸/车牌模糊、画面内容擦除/遮挡（**仅限视频**） | `mps_erase.py` | [mps_erase.md](references/mps_erase.md) | **图片**中的文字/水印擦除请用 `mps_imageprocess.py` |
| 画质增强、画质修复、画质提升、老片修复、超分辨率、视频超分、真人增强、漫剧增强、动漫超分、画面抖动/防抖、细节增强、人脸保真、提升至720P/1080P/2K/4K、**音频降噪 / 音量均衡 / 音频美化** | `mps_enhance.py` | [mps_enhance.md](references/mps_enhance.md) | 视频画质提升及音频增强；音频分离与画质增强互斥。**注意："增强画质到1080P/2K/4K"属于此脚本，不是转码**。模板速查：真人720P=327001/1080P=327003/2K=327005/4K=327007；漫剧720P=327002/1080P=327004/2K=327006/4K=327008；抖动优化720P=327009/1080P=327010/2K=327011/4K=327012 |
| 音频分离 / 人声提取 / 人声分离 / 提取伴奏 / 提取背景声 / 提取音轨 | `mps_enhance.py` | [mps_enhance.md](references/mps_enhance.md) | 详见 references 中的追问规则与参数说明 |
| 转码、压缩、格式转换、视频/音频编码调整 | `mps_transcode.py` | [mps_transcode.md](references/mps_transcode.md) | 视频/音频编码格式处理 |
| 字幕提取、字幕翻译、**语音识别 / 语音转文字** | `mps_subtitle.py` | [mps_subtitle.md](references/mps_subtitle.md) | 字幕与语音识别，输出 SRT 字幕或文字内容 |
| 图片处理（超分/高级超分/美颜/降噪/色彩增强/细节增强/人脸增强/低光照增强/综合增强/格式转换/缩放裁剪/滤镜/**图片擦除文字水印图标**/**盲水印**/**AI图片修复**/**AI前景提取**/**AI文字水印擦除**） | `mps_imageprocess.py` | [mps_imageprocess.md](references/mps_imageprocess.md) | 图片综合处理；**图片**中的文字/水印/图标擦除用此脚本，**视频**擦除用 `mps_erase.py`；AI 编排场景通过 `--schedule-id` 触发，**仅支持 AI文字水印擦除=30000 / AI前景提取=30031 / AI图片修复(老照片修复/划痕修复)=30040**；**抠图→`mps_image_cutout.py`、图片理解→`mps_image_comprehend.py`、扩图→`mps_image_padding.py`、背景融合→`mps_image_bg_fusion.py`、换装→`mps_image_tryon.py`，本脚本均不支持**|
| 精准抠图 / 透明背景抠图 / 去背景 PNG | `mps_image_cutout.py` | [mps_image_cutout.md](references/mps_image_cutout.md) | 精准抠图输出透明 PNG，支持透明度阈值/边缘步长调节（ScheduleId=30030） |
| 图片扩图 / 画布扩展 / outpaint / 扩展画面 | `mps_image_padding.py` | [mps_image_padding.md](references/mps_image_padding.md) | 智能扩展画布/画面，支持目标宽高比或像素尺寸（ScheduleId=30010）；**至少指定 `--aspect-ratio`/`--image-width`/`--image-height` 之一** |
| 图片理解 / 看图说话 / 图片OCR / 图片问答 / 描述图片内容 / 图片分析 | `mps_image_comprehend.py` | [mps_image_comprehend.md](references/mps_image_comprehend.md) | Gemini 系列模型看图问答，**必须提供 `--prompt`**；输出为文本内容而非文件（ScheduleId=30200） |
| 多视角图片生成 / 换角度 / 旋转视角 / 3D视角 | `mps_image_multiview.py` | [mps_image_multiview.md](references/mps_image_multiview.md) | 根据输入图生成不同视角的图片，支持水平/垂直角度和远近控制（ScheduleId=30070） |
| 目标检测 / 物体识别 / 找物体 / 框选检测 | `mps_image_detect.py` | [mps_image_detect.md](references/mps_image_detect.md) | 图片中目标检测与描述，支持文本 prompt 或坐标点检测，可返回抠图；**`--prompt` 和 `--point` 至少提供一个** |
| 图片局部重绘 / inpainting / 局部修改 / 指定区域替换 | `mps_image_repaint.py` | [mps_image_repaint.md](references/mps_image_repaint.md) | 使用遮罩图标记区域 + prompt 指令重绘；**必须提供遮罩图和 `--prompt`**（ScheduleId=30061） |
| 分镜拆图 / 宫格拆图 / 漫画分割 / 拆分镜头 | `mps_image_split.py` | [mps_image_split.md](references/mps_image_split.md) | 智能拆分分镜/宫格漫画为单帧图片，支持擦文字控制（ScheduleId=30050）；耗时较长约 2 分钟 |
| 换模特 / 换体型 / 服装展示换人 / 换模特身材 | `mps_image_changemodel.py` | [mps_image_changemodel.md](references/mps_image_changemodel.md) | 保持衣服不变更换模特体型，需提供衣物图（ScheduleId=30110）；**必须提供衣物图** |
| 图片换装 / AI 试衣 / 服装替换 / 模特换装 | `mps_image_tryon.py` | [mps_image_tryon.md](references/mps_image_tryon.md) | 基于模特图+服装图（1-4张）生成换装结果；支持 3 种模型：`WAND-tryon-1.0-lite`/`WAND-tryon-1.0-flash`（默认）/`WAND-tryon-1.0-pro` |
| 图片背景融合 / 背景替换 / 商品图换背景 / AI 背景生成 / 根据文字描述自动生成背景 / 电商背景生成 | `mps_image_bg_fusion.py` | [mps_image_bg_fusion.md](references/mps_image_bg_fusion.md) | 传入主图+背景图合成，或只传主图+`--prompt` 自动生成背景；详见 references |
| 海报套图 / 批量海报生成 / 商品套图 / 多平台套图 / AiPosterSuite | `mps_image_poster_suite.py` | [mps_image_poster_suite.md](references/mps_image_poster_suite.md) | **批量**生成多张广告海报 panel（必须同时有商品图 + 平台 + 主题列表）；**`--definition` 必填**，平台映射：`50`=淘宝/天猫、`51`=亚马逊Amazon、`52`=京东、`53`=拼多多、`54`=Temu、`55`=TikTok；**`--recipe` 必填**（Theme:Num，总数 4-12）；**边界**：单张 AI 海报 → `mps_aigc_image.py`；商品换背景 → `mps_image_bg_fusion.py`；海报超分/降噪 → `mps_imageprocess.py`；**与其它图片脚本参数名不同**：商品图用 `--product-url` / `--product-cos-key`（非 `--url` / `--cos-input-key`）；**支持 `--dry-run` 预演和 `--no-wait` 异步**；modify 模式必须回填所有 9 个标准变量；**modify 迭代时务必用 `--output-dir` 指定与 auto 不同的输出目录**（默认 `/output/poster_suite/`，相同会覆盖 auto 结果）；详见 references |
| AI 生图（文生图/图生图/全景图）| `mps_aigc_image.py` | [mps_aigc_image.md](references/mps_aigc_image.md) | AIGC 图片生成；支持模型：`Hunyuan`（默认，`--scene-type 3d_panorama` 生成全景图，自动补 `ModelVersion=3d_2.0`）/ `GEM`（版本 `2.5`/`3.0`/`3.1`）/ `Qwen` / `Vidu`（版本 `q2`）/ `Kling`（版本 `2.1`/`O1`/`3.0`/`3.0-Omni`）/ `OG`（版本 `image2_low`/`image2_medium`/`image2_high`）/ `Seedream`（版本 `4.5`/`5.0-lite`/`5.0-pro`）/ `MJ`（版本 `v7`/`v8.1`/`v8.2`，**一次固定出 4 张**，不支持 `--resolution`/`--aspect-ratio`，比例用 Prompt 的 `--ar` 控制；**参考图必须传公网直链**，`--image-cos-key`/`--image-local` 不可用）；**参考图上限按模型+版本区分（实测）**：Hunyuan=3、Kling 2.1·3.0=4、Kling O1·3.0-Omni=10、Vidu q2=7、Qwen=9、GEM·OG·Seedream=20、MJ=3，且总数受 MPS 平台上限 20 张约束；`--output-image-count` 指定输出张数（**仅 OG 等部分模型生效**，GEM/Hunyuan 会静默忽略），`--output-format` 指定 `jpeg`/`png` |
| AI 生视频（文生视频/图生视频/分镜生成） | `mps_aigc_video.py` | [mps_aigc_video.md](references/mps_aigc_video.md) | AIGC 视频生成，**Kling 模型支持分镜功能**；**参考视频支持模型**：`Kling`（仅 O1 / 3.0-Omni）/ `Vidu`（仅 q2-pro）/ `H2`（**仅 `1.0`**）/ `Hailuo`（仅 H3，r2va 多模态参考生成，与首帧/尾帧互斥），其他模型（Hunyuan / Hailuo 02·2.3·2.3-fast / PixVerse / GV / OS / Mingmou 等）不支持参考视频；**SceneType 严格对应模型**：`motion_control`→Kling / `land2port`→Mingmou / `template_effect`→Vidu / `3d_scene`→Hunyuan；**PixVerse 模型**（版本 `v5.6`/`v6`/`c1`，时长 1~15s，宽高比支持 `16:9`/`4:3`/`1:1`/`3:4`/`9:16`/`2:3`/`3:2`/`21:9`，画质 `--quality` 支持 `360p`/`540p`/`720p`/`1080p`）；**Hailuo 模型**（版本 `02`/`2.3`/`2.3-fast`/`H3`；**02·2.3·2.3-fast 时长仅 6/10 秒**，其他值会被接口静默忽略回落约 5.88s，脚本已前置拦截；**2.3-fast 不支持文生视频**，必须传首帧图；**H3 为原生多模态**，支持首帧/尾帧图（i2va）或参考视频/参考音频（r2va，二者互斥），参考图 ≤ 9、参考视频 ≤ 3、参考音频 ≤ 3，原生输出音轨，实测 2560x1440）；**GV 模型**（版本 `3.1`/`3.1-fast`/`3.1-lite`/`omni`）；**H2 模型**（版本 `1.0`/`1.1`；**参考视频仅 `1.0` 支持**）；**OS 模型**（版本 `2.0`，时长 `4`/`8`/`12`s，默认 8s，支持 `--enable-audio`）|
| AI 生音频（文生音效 / 视频生音效 / 文生音乐 / 歌曲翻唱） | `mps_aigc_audio.py` | [mps_aigc_audio.md](references/mps_aigc_audio.md) | AIGC 音频生成；**场景与模型严格对应**：`sfx`（音效）→ `Kling`（视频生音效加 `--ref-video-url`，须真实视频）；`music`（音乐）→ `MiniMaxMusic`（版本 `2.0`/`2.5`/`2.6`/`3.0`，**版本必填**，`--lyric` 歌词、`--instrumental` 纯音乐）/ `GL`（Google Lyria，版本 `3.0-clip`/`3.0-pro`，**版本必填**；`3.0-pro` 必须带 `--lyric` 否则任务失败）/ `Tme`（歌曲翻唱，须 `--song-id` + `--ref-audio-url`）；`--scene-type` 可省略（按模型自动推导）；**接口无 `Duration`/`OutputConfig` 字段**，时长由模型决定，格式用 `--output-audio-format`（`mp3`/`wav`）；`Kling`/`Tme` 不接受版本号；⚠️ **语音合成（TTS）不用本脚本**，用 `mps_dubbing.py` |
| 文档生成视频 / PDF转视频 / PPT转讲解视频 / Word转视频 / 文档做成视频 | `mps_doc_to_video.py` | [mps_doc_to_video.md](references/mps_doc_to_video.md) | 将 PDF/PPTX/DOCX/PNG/JPG 文档自动生成讲解视频；**最多3个文档，单个≤10MB≤100页**；**`--prompt` 必填**；支持 `--aspect-ratio`/`--language`/`--reference-duration`/AI配音（`--enable-tts`+`--voice-id`）；**查询任务复用 `--task-id`（脚本内置 DescribeAigcTaskStatus，非独立的DocToVideo专属查询接口，已通过真实任务验证）**，不能用 `mps_get_video_task.py` 查询 |
| 音视频内容理解（场景/摘要/内容分析）/ **对比分析两段音视频** / **对比分析两段音频** / 音频内容理解 | `mps_av_understand.py` | [mps_av_understand.md](references/mps_av_understand.md) | 大模型理解，**必须提供 `--mode` 和 `--prompt`**；对比两段视频/音频时需传第二段，详见 references |
| 视频去重 / 视频防重（画中画/视频扩展/垂直填充/水平填充）| `mps_dedupe.py` | [mps_dedupe.md](references/mps_dedupe.md) | `--mode` 可省略，默认 `PicInPic`；详见 references |
| 视频二次创作（换脸/换人/视频交错 AB）| `mps_vremake.py` | [mps_vremake.md](references/mps_vremake.md) | **必须提供 `--mode`**；详见 references |
| AI解说二创 / 短剧解说 / 自动生成短剧解说视频 / 短剧解说混剪 | `mps_narrate.py` | [mps_narrate.md](references/mps_narrate.md) | 必须从预设场景中选择；不支持自定义脚本；多集视频详见 references |
| 精彩集锦 / 高光提取 / 自动剪辑精彩片段 / 足球进球集锦 / 篮球集锦 / 短剧高光 | `mps_highlight.py` | [mps_highlight.md](references/mps_highlight.md) | 必须从预设场景中选择；不支持直播流 |
| 横竖屏方向转换（横屏转竖屏 / 竖屏转横屏 / 横转竖 / 竖转横 / 转成 9:16 / 转成 16:9 / 短视频比例转换） | `mps_orientation_convert.py` | [mps_orientation_convert.md](references/mps_orientation_convert.md) | **双向转换**：横→竖用算法 `2`多模型/`3`人脸检测/`5`缩放毛玻璃/`6`AIGC补全，竖→横用算法 `7`AIGC补全；**`--algorithm-type` 必填**，需先确认转换方向；固定 `AiAnalysisTask.Definition=28`；`SmoothWeight` 默认 `0.75`，`Ratio` 默认 `9:16`（**算法 7 须显式指定 `--ratio 16:9`**）；`--blur-weight` 仅算法5、人脸参数仅算法3；算法`6`/`7`为高级版计费；不支持直播流与 AWS S3；⚠️ **转换已有视频**用本脚本，凭 prompt 生成竖屏视频用 `mps_aigc_video.py --model Mingmou --scene-type land2port`，仅加填充边做去重用 `mps_dedupe.py --mode VerticalExtend` |
| 用量统计查询 | `mps_usage.py` | [mps_usage.md](references/mps_usage.md) | 调用次数/时长查询 |
| 查询音视频处理任务状态 | `mps_get_video_task.py` | [mps_query_task.md](references/mps_query_task.md) | ProcessMedia 任务查询（含 VideoRemake 等所有任务类型） |
| 查询图片处理任务状态 | `mps_get_image_task.py` | [mps_query_task.md](references/mps_query_task.md) | ProcessImage 任务查询 |
| 查询 AIGC 生图任务状态 | `mps_aigc_image.py` | [mps_aigc_image.md](references/mps_aigc_image.md) | 使用各自脚本的 `--task-id` 查询 |
| 查询 AIGC 生视频任务状态 | `mps_aigc_video.py` | [mps_aigc_video.md](references/mps_aigc_video.md) | 使用各自脚本的 `--task-id` 查询 |
| 上传本地文件到 COS | `mps_cos_upload.py` | [mps_cos_ops.md](references/mps_cos_ops.md) | 本地→COS；本地路径用 `--local-file`，COS 路径用 `--cos-input-key`（可选） |
| 从 COS 下载文件到本地 | `mps_cos_download.py` | [mps_cos_ops.md](references/mps_cos_ops.md) | COS→本地；COS 路径用 `--cos-input-key`，本地路径用 `--local-file`（**可选**，省略时自动保存为 `./<文件名>`，不得询问用户） |
| 列出 COS Bucket 文件 / 查看 COS 目录 | `mps_cos_list.py` | [mps_cos_ops.md](references/mps_cos_ops.md) | 查看 COS 文件列表，支持路径过滤和文件名搜索 |
| 检查/验证 MPS 环境变量配置 | `mps_load_env.py` | — | 不修改环境变量，**不产生费用** |
| 生成媒体效果对比展示页面 / 处理前后对比 / 视频增强对比 / 图片处理效果对比 | `mps_gen_compare.py` | [mps_gen_compare.md](references/mps_gen_compare.md) | 生成交互式 HTML 对比页面，支持视频滑动对比/图片并排对比；**不调用 MPS API，不产生费用**。关键参数：`--original <原始URL>` `--enhanced <处理后URL>` `--title` `--type image\|video` |

> **注意**：`mps_poll_task.py` 是内部轮询辅助模块，**不需要向用户暴露，也不需要让用户直接调用**，所有脚本已内置轮询逻辑，用户直接使用各功能脚本即可。
> `mps_cos_ops.md` 覆盖 `mps_cos_upload.py`、`mps_cos_download.py`、`mps_cos_list.py` 三个脚本。
> `mps_query_task.md` 覆盖 `mps_get_video_task.py`、`mps_get_image_task.py` 两个脚本。
> AIGC 生图/生视频/生音频任务使用独立的 Create/Describe API，**不能**用 `mps_get_video_task.py` 或 `mps_get_image_task.py` 查询，必须用各自脚本的 `--task-id` 查询（生音频 TaskId 含 `AigcAudio` 字样）。
> `mps_doc_to_video.py`（文档生视频）**没有独立的DocToVideo专属查询接口**，内置复用 `DescribeAigcTaskStatus`（已通过真实任务验证响应结构）查询结果，同样必须用该脚本自身的 `--task-id` 查询，不能用 `mps_get_video_task.py` 查询。

> **重要**：`mps_erase.py` 职责是**擦除/遮挡画面视觉元素**，不涉及质量检测。
> "画质检测"、"模糊"、"花屏"、"播放兼容性"、"音频质检" → 必须用 `mps_qualitycontrol.py`。
> "音频对比"、"分析两段音频差异"、"音频内容理解" → 必须用 `mps_av_understand.py`，**不得用 `mps_qualitycontrol.py`**。

## 生成命令的强制规则

1. **脚本路径前缀**：所有生成的 python 命令必须包含 `scripts/` 路径前缀，格式为 `python3 scripts/mps_xxx.py ...`。禁止生成 `python3 mps_xxx.py ...`（缺少 scripts/ 前缀）的命令。

2. **禁止占位符**：所有参数值必须是真实值。若用户未提供必需值，**先询问**，不得用 `<视频URL>`、`YOUR_URL` 等占位符。

3. **脚本专属强制规则**：部分脚本有必填参数约束、追问要求或默认行为（如音频分离必须追问类型、精彩集锦必须追问场景、AI 解说必须追问字幕情况、视频增强默认使用真人模板等），生成命令前必须查阅对应 `references/<script>.md` 中的「强制规则」章节，严格遵守。

4. **输入文件来源判断规则**：
   - 用户**明确说明是 COS 文件**（如"COS 路径"、"COS 上的"、"bucket 上"）→ 使用 `--cos-input-key <key>`，bucket/region 由环境变量自动补全，不得询问用户
   - 用户提供的是 **HTTP/HTTPS URL** → 使用 `--url <URL>`，不得拆解成任何形式。
   - 用户**未明确说明来源**，不管路径格式如何（`input/video.mp4`、`/data/video.mp4`、`video.mp4` 等）→ **一律使用 `--local-file <路径>` 按本地文件处理**；若本地文件不存在，脚本会自动提示用户明确来源，并中止任务；
   - ✅ 正确：用户说"处理视频 input/raw.mp4" → 生成 `--local-file input/raw.mp4`
   - ✅ 正确：用户说"COS 路径：input/raw.mp4" → 生成 `--cos-input-key input/raw.mp4`
   - ❌ 错误：用户未说明来源时询问"是 COS 还是本地文件？"

5. **组合任务必须分别生成所有命令**：当用户请求涉及多个脚本时，必须为每个脚本**分别生成独立的完整命令**，不得遗漏任何一条。
6. **行为修饰用例规则说明**：用户说 `dry run`、`不等待`、`先预览命令`、`先提交任务`、`先拿任务ID` 等修饰词时，仍然需要触发此 Skill，这些词只影响命令参数（`--dry-run` 或 `--no-wait`），不影响任务类型判断。
7. **`--no-wait` 使用规则**：用户说"不等待"、"先拿任务ID"、"不用等结果"、"异步提交"、"先提交任务"时，命令中**必须加 `--no-wait`** 参数。默认不加（即默认自动轮询等待结果）；只有用户明确表达不等待意图时才加。
8. **`mps_load_env.py` 使用规则**：用户说"检查环境变量"、"验证配置是否正确"、"检查配置"时，必须生成 `python3 scripts/mps_load_env.py --check-only` 命令，不得省略 `--check-only` 参数。
9. **套图生成 vs 单张海报边界**：`mps_image_poster_suite.py` 仅处理"批量生成多张海报 panel"的场景（用户同时表达"商品图 + 平台 + 主题/多张"意图）。以下情况**不触发套图生成**：
   - "用 AI 生成一张海报/产品海报" → `mps_aigc_image.py`（AIGC 文生图）
   - "商品图换背景/做成电商风格" → `mps_image_bg_fusion.py`（背景融合）
   - "海报图片超分/降噪/提升清晰度" → `mps_imageprocess.py`（图片处理）
   - 判断依据：用户说的是"一张"还是"多张/一套"；是否提到"平台"（淘宝/京东等）；是否提到"主题"（hero/detail 等）

## API 参考

| 脚本 | 文档 |
|------|------|
| `mps_dubbing.py` | [SyncDubbing](https://cloud.tencent.com/document/api/862/116748) / [ProcessMedia](https://cloud.tencent.com/document/api/862/37578) |
| `mps_transcode.py` / `mps_enhance.py` / `mps_subtitle.py` / `mps_erase.py` | [ProcessMedia](https://cloud.tencent.com/document/api/862/37578) |
| `mps_qualitycontrol.py` | [ProcessMedia AiQualityControlTask](https://cloud.tencent.com/document/product/862/37578) |
| `mps_imageprocess.py` | [ProcessImage](https://cloud.tencent.com/document/api/862/112896) |
| `mps_av_understand.py` | [VideoComprehension AiAnalysisTask](https://cloud.tencent.com/document/product/862/126094) |
| `mps_dedupe.py` | [VideoRemake AiAnalysisTask](https://cloud.tencent.com/document/product/862/124394) |
| `mps_vremake.py` | [VideoRemake AiAnalysisTask](https://cloud.tencent.com/document/product/862/124394) |
| `mps_narrate.py` | [ProcessMedia AiAnalysisTask](https://cloud.tencent.com/document/product/862/37578) |
| `mps_highlight.py` | [ProcessMedia AiAnalysisTask](https://cloud.tencent.com/document/product/862/37578) |
| `mps_orientation_convert.py` | [ProcessMedia AiAnalysisTask Definition=28](https://cloud.tencent.com/document/product/862/112112) |
| `mps_aigc_image.py` | [CreateAigcImageTask](https://cloud.tencent.com/document/api/862/114562) |
| `mps_aigc_video.py` | [CreateAigcVideoTask](https://cloud.tencent.com/document/api/862/126965) |
| `mps_aigc_audio.py` | [CreateAigcAudioTask](https://cloud.tencent.com/document/api/862/132830) / [DescribeAigcAudioTask](https://cloud.tencent.com/document/api/862/132829) |
| `mps_doc_to_video.py` | [CreateDocToVideoTask](https://cloud.tencent.com/document/api/862) / DescribeAigcTaskStatus（官方文档未公开，SDK≥3.1.139已建模，已通过真实调用验证） |
| `mps_usage.py` | [DescribeUsageData](https://cloud.tencent.com/document/product/862/125919) |
| `mps_get_video_task.py` | [DescribeTaskDetail](https://cloud.tencent.com/document/api/862/37614) |
| `mps_get_image_task.py` | [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/112897) |
| `mps_image_tryon.py` | [ProcessImage ImageTask.AiTryOnConfig](https://cloud.tencent.com/document/product/862/112896) |
| `mps_image_bg_fusion.py` | [ProcessImage ScheduleId=30060](https://cloud.tencent.com/document/product/862/112896) |
