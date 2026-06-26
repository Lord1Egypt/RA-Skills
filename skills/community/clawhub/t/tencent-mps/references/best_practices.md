# tencent-mps 能力最佳实践场景

> 本文档从 `evals.json` 正向用例中提炼场景描述，按 SKILL.md 的 19 个能力模块归类。每条场景描述均为自然语言表达，来源于真实测试用例中的多样化 query，可直接用作：
>
> - Skill 触发率测试的正样本素材
> - 产品/运营/销售对客介绍的"能力-场景"对照清单
> - 帮助新用户快速判断"我的需求属于哪种 MPS 能力"
>
> 每条场景后面标注对应的**处理脚本**和关键参数，方便对照 SKILL.md 的脚本路由表执行。

---

## 目录

1. [视频转码](#1-视频转码-mps_transcodepy)
2. [画质增强](#2-画质增强-mps_enhancepy)
3. [音频处理（音频分离）](#3-音频处理音频分离-mps_enhancepy)
4. [字幕与语音](#4-字幕与语音-mps_subtitlepy)
5. [擦除与遮挡（视频）](#5-擦除与遮挡视频-mps_erasepy)
6. [图片处理](#6-图片处理-mps_imageprocesspy)
7. [图片换装](#7-图片换装-mps_image_tryonpy)
8. [图片背景融合](#8-图片背景融合-mps_image_bg_fusionpy)
9. [AIGC 生图](#9-aigc-生图-mps_aigc_imagepy)
10. [AIGC 生视频](#10-aigc-生视频-mps_aigc_videopy)
11. [音视频内容理解](#11-音视频内容理解-mps_av_understandpy)
12. [视频二创](#12-视频二创-mps_vremakepy)
13. [视频去重](#13-视频去重-mps_dedupepy)
14. [精彩集锦](#14-精彩集锦-mps_highlightpy)
15. [AI 解说](#15-ai-解说-mps_narratepy)
16. [媒体质检](#16-媒体质检-mps_qualitycontrolpy)
17. [用量统计](#17-用量统计-mps_usagepy)
18. [COS 与任务管理](#18-cos-与任务管理)
    - [18.1 上传/下载/列目录](#181-上传下载列目录)
    - [18.2 任务状态查询](#182-任务状态查询)
    - [18.3 环境变量检查](#183-环境变量检查)
19. [效果对比](#19-效果对比-mps_gen_comparepy)

---

## 1. 视频转码 (`mps_transcode.py`)

**核心能力**：视频/音频编码转换、码率/分辨率/帧率调整、格式转换（MP4/AVI/MKV/FLV/MOV/HLS 等）、H.264/H.265/AV1 编码切换、压缩瘦身、极速高清压缩（ultra_compress）。

**典型场景**：

1. 我有一个用手机拍的 1.2GB 的 MOV 格式视频，想把它压缩成 MP4 丢到微信发给同事看，帮我处理一下。
   → `python scripts/mps_transcode.py --url <视频URL> --codec h264 --container mp4`
2. 把 COS 上的视频 `input/my_video.mp4` 压缩一下，转成 H.264 格式，码率 2000kbps。
   → `python scripts/mps_transcode.py --cos-input-key input/my_video.mp4 --codec h264 --bitrate 2000`
3. 我想把视频转成 MP4 格式，不想等待结果，先提交任务就行。
   → `python scripts/mps_transcode.py --url <视频URL> --container mp4 --no-wait`
4. 帮我把视频转码成 H.265 格式：`https://ie-mps-1258344699.cos.ap-nanjing.tencentcos.cn/evanxia/mps/vivienyao/test_video_01.mp4`
   → `python scripts/mps_transcode.py --url <URL> --codec h265`
5. 把视频转成 H.264 格式，分辨率 1280x720，帧率 30fps。
   → `python scripts/mps_transcode.py --url <URL> --codec h264`
6. 本地视频 `/home/user/video.mp4` 要做 H.265 转码（需先上传 COS 再转码再下载完整流程）。
   → `python scripts/mps_transcode.py --local-file /home/user/video.mp4 --codec h265`
7. 我有一个本地视频 `/data/my_video.mp4`，帮我做 H.265 转码（完整三步流程）。
   → `python scripts/mps_transcode.py --local-file /data/my_video.mp4 --codec h265`

---

## 2. 画质增强 (`mps_enhance.py`)

**核心能力**：视频超分、画质修复、老片修复、超分辨率、画质提升、真人增强、漫剧增强、动漫超分、画面抖动/防抖、细节增强、人脸保真、清晰度提升至 720P/1080P/2K/4K；同时包含音频降噪、音量均衡、音频美化等音频增强能力。

**典型场景**：

1. 帮我对视频做画质增强，提升到 1080P，视频是真人拍摄的。
   → `python scripts/mps_enhance.py --url <URL> --template 327003`（真人 1080P 模板）
2. 这是一段老动漫视频，帮我超分辨率到 4K。
   → `python scripts/mps_enhance.py --url <URL> --template 327008`（漫剧 4K 模板）
3. 视频有点抖动，帮我做抖动优化增强到 2K。
   → `python scripts/mps_enhance.py --cos-input-key input/shaky.mp4 --template 327011`（抖动优化 2K 模板）
4. 漫剧视频增强到 2K。
   → `python scripts/mps_enhance.py --url <URL> --template 327006`（漫剧 2K 模板）
5. 视频增强到 720P，真人场景。
   → `python scripts/mps_enhance.py --cos-input-key input/low_res.mp4 --template 327001`（真人 720P 模板）
6. 人脸保真增强到 1080P。
   → `python scripts/mps_enhance.py --url <URL> --template 327018`（人脸保真 1080P 模板）
7. 细节最强增强模式，提升到 4K。
   → `python scripts/mps_enhance.py --url <URL> --template 327016`（细节最强 4K 模板）
8. 抖动优化 720P 增强。
   → `python scripts/mps_enhance.py --cos-input-key input/shaky720.mp4 --template 327009 --no-wait`
9. 真人实拍视频增强到 1080P。
   → `python scripts/mps_enhance.py --cos-input-key input/real_person.mp4 --template 327003`
10. 本地视频画质增强到 1080P 真人场景（需先上传 COS）。
    → `python scripts/mps_enhance.py --local-file /home/user/input.mp4 --template 327003`

---

## 3. 音频处理（音频分离） (`mps_enhance.py`)

**核心能力**：人声提取、人声分离、伴奏提取、BGM 分离、背景音乐提取、去人声、去伴奏、提取音轨。**必须指定 `--audio-separate vocal/background/accompaniment` 三选一**。

**典型场景**：

1. 帮我从这个视频里提取人声（人声分离）：`https://vivien-1256342427.cos.ap-nanjing.myqcloud.com/MPS/QZ3jiuY4CrUA.mp4`
   → `python scripts/mps_enhance.py --url <URL> --audio-separate vocal`
2. 这个视频的背景音乐我很喜欢，能不能把纯 BGM 扒出来单独存一个 MP3？
   → `python scripts/mps_enhance.py --url <URL> --audio-separate background`
3. 做短视频二创需要，把原视频的人声去掉只保留环境声 + BGM。
   → `python scripts/mps_enhance.py --url <URL> --audio-separate accompaniment`
4. 给我一份这段采访视频的纯伴奏（去掉人声），我要重新配一个旁白。
   → `python scripts/mps_enhance.py --url <URL> --audio-separate accompaniment`
5. 制作 KTV 消音版：请把这个现场演唱版本的人声去掉，只保留伴奏。
   → `python scripts/mps_enhance.py --url <URL> --audio-separate accompaniment`
6. 视频里有人声和背景音乐，帮我把人声提取出来（人声分离）。
   → `python scripts/mps_enhance.py --url <URL> --audio-separate vocal`
7. 帮我把视频的人声和背景音乐分离，同时把视频转码成 H.264。
   → `python scripts/mps_enhance.py --cos-input-key input/music_video.mp4 --audio-separate vocal` + `mps_transcode.py --cos-input-key input/music_video.mp4 --codec h264`

---

## 4. 字幕与语音 (`mps_subtitle.py`)

**核心能力**：语音识别（ASR）生成字幕、硬字幕 OCR 提取、字幕翻译、SRT 输出、语音转文字、视频多语字幕、OCR 识别区域指定。

**典型场景**：

1. 帮我提取这个视频的字幕：`https://vivien-1256342408.cos.ap-nanjing.myqcloud.com/DEMO/trailer.mp4`
   → `python scripts/mps_subtitle.py --url <URL>`
2. 把这个英文视频的字幕翻译成中文。
   → `python scripts/mps_subtitle.py --url <URL> --src-lang en --translate zh`
3. 我有一段中文视频，帮我提取字幕并翻译成英文。
   → `python scripts/mps_subtitle.py --cos-input-key input/chinese.mp4 --src-lang zh --translate en`
4. 帮我对这个视频做语音识别，输出文字内容。
   → `python scripts/mps_subtitle.py --url <URL>`
5. 这个视频有硬字幕，帮我用 OCR 识别提取出来。
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr`
6. 用 OCR 识别这个视频的字幕并翻译成英文。
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr --translate en`
7. 视频底部有花字字幕，帮我 OCR 识别，只识别底部 30% 区域。
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr --ocr-area`
8. 提取视频画面上的文字内容，视频是中英双语的。
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr --src-lang zh_en`
9. 视频里有烧录的硬字幕，帮我 OCR 提取后翻译成日文。
   → `python scripts/mps_subtitle.py --cos-input-key input/hardcoded_subtitle.mp4 --process-type ocr --translate ja`
10. 帮我对视频做字幕提取，不等待任务完成。
    → `python scripts/mps_subtitle.py --url <URL> --no-wait`

---

## 5. 擦除与遮挡（视频） (`mps_erase.py`)

**核心能力**：视频画面中的字幕擦除、水印擦除、人脸模糊、车牌模糊、隐私遮挡、马赛克。**仅限视频，图片请用 `mps_imageprocess.py`**。

**典型场景**：

1. 帮我把这个视频里的字幕去掉：`https://lily-1256342427.cos.ap-nanjing.myqcloud.com/mps_autotest/subtitle/subtitle.mkv`
   → `python scripts/mps_erase.py --url <URL> --template 101`（去字幕模板）
2. 视频里有水印，帮我用高级去水印处理一下。
   → `python scripts/mps_erase.py --url <URL> --template 201`（去水印高级版模板）
3. 这个视频里有人脸，帮我做人脸模糊处理。
   → `python scripts/mps_erase.py --cos-input-key input/faces.mp4 --template 301`（人脸模糊模板）
4. 视频里有人脸和车牌，都需要模糊处理。
   → `python scripts/mps_erase.py --url <URL> --template 302`（人脸+车牌模糊模板）
5. 帮我对视频做去字幕处理，同时提取字幕文本（OCR）。
   → `python scripts/mps_erase.py --url <URL> --template 102`（去字幕+OCR 模板）
6. 视频左上角有水印，帮我去掉。
   → `python scripts/mps_erase.py --cos-input-key input/watermark.mp4 --template 201`
7. 真人实拍视频左上角有水印，帮我去掉，同时做 1080P 增强。
   → `python scripts/mps_erase.py --cos-input-key input/watermark.mp4 --template 201` + `mps_enhance.py --cos-input-key input/watermark.mp4 --template 327003`

---

## 6. 图片处理 (`mps_imageprocess.py`)

**核心能力**：图片超分、高级超分、美颜、降噪、色彩增强、细节增强、人脸增强、低光照增强、综合增强、格式转换、缩放裁剪、滤镜、**图片文字/水印/图标擦除**、**盲水印**。**图片去水印属于此脚本，不是视频擦除脚本 `mps_erase.py`**。

**典型场景**：

1. 帮我对这张图片做超分辨率处理：`https://lily-1256342427.cos.ap-nanjing.myqcloud.com/mps_autotest/pic.jpeg`
   → `python scripts/mps_imageprocess.py --url <URL> --super-resolution`（普通 2 倍超分）
2. 这张人像照片需要美颜处理（磨皮和美白）。
   → `python scripts/mps_imageprocess.py --cos-input-key input/portrait.jpg --beauty Smooth:50 --beauty Whiten:50`
3. 图片噪点很多，帮我做降噪处理。
   → `python scripts/mps_imageprocess.py --url <URL> --denoise weak`
4. 图片超分辨率，不等待，COS 路径：`input/lowres.jpg`。
   → `python scripts/mps_imageprocess.py --cos-input-key input/lowres.jpg --super-resolution --no-wait`
5. 图片右下角有个 LOGO 水印，要擦掉。
   → `python scripts/mps_imageprocess.py --cos-input-key input/logo.jpg --erase-detect logo`（图片擦除用此脚本）
6. 我要给批量图片加盲水印，用于后续版权溯源。
   → `python scripts/mps_imageprocess.py --cos-input-key input/batch/ --add-watermark "版权"`
7. 把这张 PNG 转成 JPEG 并把宽高缩放到 1920×1080。
   → `python scripts/mps_imageprocess.py --cos-input-key input/photo.png --format JPEG --resize-mode fixed --resize-width 1920 --resize-height 1080`
8. 一组原图有点糊，走一下综合增强（超分+降噪+色彩）。
   → `python scripts/mps_imageprocess.py --cos-input-key input/batch/ --quality-enhance normal`

---

## 7. 图片换装 (`mps_image_tryon.py`)

**核心能力**：图片换装、AI 试衣、服装替换、模特换装、虚拟试穿。普通场景支持 1-2 张服装图；内衣场景（`--schedule-id 30101`）仅支持 1 张服装图。支持 URL、COS key、本地文件三种输入方式。

**典型场景**：

1. 帮我用 AI 生成一张模特图，然后让她换上这件 T 恤。
   → `python scripts/mps_image_tryon.py --model-url <模特图URL> --cloth-url <服装图URL>`
2. 电商上新一批连衣裙，不想重新拍模特图，能把原模特换上新款连衣裙吗？
   → `python scripts/mps_image_tryon.py --model-cos-key input/model.jpg --cloth-cos-key input/dress.jpg`
3. 这是服装供应链的平铺白底图，帮我合成到标准模特身上生成主图。
   → `python scripts/mps_image_tryon.py --model-url <模特图URL> --cloth-url <平铺图URL>`
4. 我们是内衣品牌，要做虚拟试穿，只替换上装内衣一件即可。
   → `python scripts/mps_image_tryon.py --model-url <模特图URL> --cloth-url <内衣图URL> --schedule-id 30101`
5. 产品拍摄预算不够，想先用 AI 换装生成详情页主图看看效果。
   → `python scripts/mps_image_tryon.py --model-cos-key input/model.jpg --cloth-cos-key input/cloth.jpg`
6. 同一个模特姿势，帮我批量换 5 款 SKU 的服装，输出 5 张不同款式的模特图。
   → `python scripts/mps_image_tryon.py --model-url <模特图URL> --cloth-url <服装1URL>` × 5 次
7. 本地图片换装，模特图：`/data/model.jpg`，服装图：`/data/cloth.jpg`。
   → `python scripts/mps_image_tryon.py --local-file /data/model.jpg /data/cloth.jpg`（或先上传到 COS 再换装）

---

## 8. 图片背景融合 (`mps_image_bg_fusion.py`)

**核心能力**：图片背景替换、商品图换背景、AI 背景生成、根据文字 prompt 自动生成背景、电商背景。可上传"主图+背景图"合成，或只传主图 + `--prompt` 自动生成。支持 URL、COS key（含 bucket/region）三种输入方式。

**典型场景**：

1. 帮我做背景融合，商品图：`<URL>`，背景图：`<URL>`。
   → `python scripts/mps_image_bg_fusion.py --subject-url <商品图URL> --bg-url <背景图URL>`
2. 这是白底商品图，帮我换成户外草地的自然背景，做成春夏户外风主图。
   → `python scripts/mps_image_bg_fusion.py --subject-url <商品图URL> --prompt "户外草地自然光春夏风格"`
3. 只有这个产品的抠图，没有合适的背景素材，请根据提示词自动生成背景。
   → `python scripts/mps_image_bg_fusion.py --subject-url <商品图URL> --prompt "北欧风客厅木地板午后阳光"`
4. AI 换背景，主图在 COS：`input/product.jpg`，背景图：`<URL>`。
   → `python scripts/mps_image_bg_fusion.py --subject-cos-key input/product.jpg --bg-url <背景图URL>`
5. 背景融合，主图和背景图都在 COS，主图：`input/product.jpg`，背景图：`input/bg.jpg`。
   → `python scripts/mps_image_bg_fusion.py --subject-cos-key input/product.jpg --bg-cos-key input/bg.jpg`
6. 商品图背景替换，主图：`<URL>`，背景图：`<URL>`，融合要求：增加暖色调光线。
   → `python scripts/mps_image_bg_fusion.py --subject-url <主图URL> --bg-url <背景图URL> --prompt "暖色调光线"`
7. 电商背景生成，商品图：`<URL>`，背景描述：户外草坪阳光明媚，固定随机种子 42。
   → `python scripts/mps_image_bg_fusion.py --subject-url <商品图URL> --prompt "户外草坪阳光明媚" --random-seed 42`
8. 背景生成，商品图：`<URL>`，背景描述：现代简约家居客厅，输出 PNG 格式，4K 尺寸。
   → `python scripts/mps_image_bg_fusion.py --subject-url <商品图URL> --prompt "现代简约家居客厅" --format PNG --image-size 4K`

---

## 9. AIGC 生图 (`mps_aigc_image.py`)

**核心能力**：文生图、图生图、AI 绘画、3D 全景图。支持 6 个模型：`Hunyuan`（默认）/ `GEM`（2.5/3.0/3.1，多图参考）/ `Qwen` / `Vidu`（q2）/ `Kling`（2.1/O1/3.0/3.0-Omni）/ `OG`（image2_low/image2_medium/image2_high）。Hunyuan 支持 `--scene-type 3d_panorama` 生成超宽全景图（~27MB）。

**典型场景**：

1. 帮我用 AI 生成一张图片，描述是：一只在草地上奔跑的金毛犬，阳光明媚。
   → `python scripts/mps_aigc_image.py --prompt "一只在草地上奔跑的金毛犬，阳光明媚"`
2. 用这张图片作为参考，生成一张类似风格的新图片，描述：夕阳西下的海边。
   → `python scripts/mps_aigc_image.py --prompt "夕阳西下的海边" --image-url <参考图URL>`
3. AI 生图，参考图在 COS 上：bucket=`mps-test-1234567`，region=`ap-guangzhou`，key=`input/ref.jpg`，提示词：城市夜景。
   → `python scripts/mps_aigc_image.py --prompt "城市夜景" --image-cos-bucket mps-test-1234567 --image-cos-region ap-guangzhou --image-cos-key input/ref.jpg`
4. 帮我根据"赛博朋克风格的香港街头，霓虹灯雨夜"这段 prompt 生成 4 张海报图。
   → `python scripts/mps_aigc_image.py --prompt "赛博朋克风格的香港街头，霓虹灯雨夜"`
5. 参考这张猫咪照片，用图生图生成它的水彩画版本。
   → `python scripts/mps_aigc_image.py --prompt "水彩画风格猫咪" --image-url <猫咪照片URL>`
6. AI 生图，先预览一下命令（dry run）：提示词是城市夜景霓虹灯。
   → `python scripts/mps_aigc_image.py --prompt "城市夜景霓虹灯" --dry-run`
7. 生成一张"春节红色主题的礼盒包装视觉图"用于电商首焦。
   → `python scripts/mps_aigc_image.py --prompt "春节红色主题的礼盒包装视觉图"`
8. 用 Kling 3.0 生成一张写实风格山水画。
   → `python scripts/mps_aigc_image.py --prompt "写实风格山水画" --model Kling --model-version 3.0`
9. 用 OG 高质量模式生成一张城市夜景。
   → `python scripts/mps_aigc_image.py --prompt "城市夜景霓虹灯" --model OG --model-version image2_high`
10. 用 Hunyuan 生成一张热带雨林 3D 全景图。
    → `python scripts/mps_aigc_image.py --prompt "热带雨林全景，郁郁葱葱" --model Hunyuan --scene-type 3d_panorama`

---

## 10. AIGC 生视频 (`mps_aigc_video.py`)

**核心能力**：文生视频、图生视频、**Kling 模型分镜生成**（1-6 个分镜，分镜时长之和 = 总时长）。支持纯 prompt 文生视频、图片生视频（URL 或 COS）、Kling 多分镜、输出数量控制、随机种子、dry-run、no-wait。

**典型场景**：

1. 帮我用 AI 生成一段视频，文字描述：一只猫咪在窗边晒太阳，慵懒地伸着懒腰。
   → `python scripts/mps_aigc_video.py --prompt "一只猫咪在窗边晒太阳，慵懒地伸着懒腰"`
2. 用这张图片生成一段视频，图片地址：`<URL>`，描述：微风吹动树叶。
   → `python scripts/mps_aigc_video.py --prompt "微风吹动树叶" --image-url <图片URL>`
3. 用 Kling 模型生成分镜视频，总时长 10 秒，分 2 个分镜：第一个 5 秒拍日出，第二个 5 秒拍日落。
   → `python scripts/mps_aigc_video.py --prompt "日出" --multi-shot --multi-prompts-json '[{"prompt":"日出","duration":5},{"prompt":"日落","duration":5}]'`
4. AI 生视频，不等待，先拿到任务ID：提示词是雪山日出。
   → `python scripts/mps_aigc_video.py --prompt "雪山日出" --no-wait`
5. 帮我根据"海边日出浪花拍打礁石，缓慢推镜"用 Kling 模型生成 5 秒视频。
   → `python scripts/mps_aigc_video.py --prompt "海边日出浪花拍打礁石，缓慢推镜"`
6. 我有一张静态产品图，请把它做成 3 秒的运镜视频，镜头从远到近推进。
   → `python scripts/mps_aigc_video.py --prompt "镜头从远到近推进产品" --image-url <产品图URL>`
7. AI 生视频 dry run，提示词：波涛汹涌的大海。
   → `python scripts/mps_aigc_video.py --prompt "波涛汹涌的大海" --dry-run`

---

## 11. 音视频内容理解 (`mps_av_understand.py`)

**核心能力**：视频内容分析、视频摘要、场景识别、对比分析两段视频/两段音频、音频理解。**必须提供 `--mode` 和 `--prompt`**。支持视频 URL、COS 输入。

**典型场景**：

1. 帮我分析这个视频的内容，了解主要场景和关键信息。
   → `python scripts/mps_av_understand.py --url <URL> --mode video --prompt "分析视频内容和关键信息"`
2. 对比分析这两段音频的差异。
   → `python scripts/mps_av_understand.py --url <视频1URL> --extend-url <视频2URL> --mode compare --prompt "对比分析两段音频的差异"`
3. 视频内容理解，COS 路径 `input/meeting.mp4`，帮我总结会议要点。
   → `python scripts/mps_av_understand.py --cos-input-key input/meeting.mp4 --mode video --prompt "总结会议要点"`
4. 帮我对这个视频做画面质检，检查是否有模糊或花屏（注意：质检走 `mps_qualitycontrol.py`，此处为内容理解）。
   → `python scripts/mps_av_understand.py --url <URL> --mode video --prompt "描述视频画面内容"`
5. 帮我理解这个视频内容，给出摘要和关键信息，不等待结果。
   → `python scripts/mps_av_understand.py --url <URL> --mode video --prompt "摘要和关键信息" --no-wait`
6. 对比两段视频的讲解差异。
   → `python scripts/mps_av_understand.py --url <视频1URL> --extend-url <视频2URL> --mode compare --prompt "对比讲解差异"`
7. 视频内容理解，描述一下视频内容。
   → `python scripts/mps_av_understand.py --cos-input-key input/ocean.mp4 --mode video --prompt "描述视频内容"`

---

## 12. 视频二创 (`mps_vremake.py`)

**核心能力**：换脸、换人、视频交错（AB 剪辑）。**必须提供 `--mode`**（SwapFace / SwapCharacter / VideoInterleave / AB）。

**典型场景**：

1. 帮我做视频换脸，原始脸：`<URL>`，目标脸：`<URL>`，视频：`<URL>`。
   → `python scripts/mps_vremake.py --url <视频URL> --mode SwapFace --src-faces <原始脸URL> --dst-faces <目标脸URL>`
2. 视频换人处理，原始人物图：`<URL>`，目标人物图：`<URL>`，视频：`<URL>`，等待结果。
   → `python scripts/mps_vremake.py --url <视频URL> --mode SwapCharacter --src-character <原始人物URL> --dst-character <目标人物URL>`
3. 视频 AB 交错二创处理。
   → `python scripts/mps_vremake.py --url <视频URL> --mode AB`
4. 换脸，把视频里的人换成这张图片的脸，不用等结果。
   → `python scripts/mps_vremake.py --url <视频URL> --mode SwapFace --src-faces <脸图URL> --dst-faces <目标脸URL> --no-wait`
5. 视频二创换脸，但我还没想好用哪个模式，请帮我介绍一下有哪些模式。
   → AI 介绍 `SwapFace`/`SwapCharacter`/`VideoInterleave`/`AB` 模式，并追问选择
6. 视频二创换脸，把主播的脸换成吉祥物的二维卡通形象。
   → `python scripts/mps_vremake.py --url <视频URL> --mode SwapFace --src-faces <主播脸URL> --dst-faces <吉祥物URL>`
7. 这个老广告里的代言人要换成新代言人的脸，请保留原台词和动作。
   → `python scripts/mps_vremake.py --url <视频URL> --mode SwapFace --src-faces <原代言人URL> --dst-faces <新代言人URL>`

---

## 13. 视频去重 (`mps_dedupe.py`)

**核心能力**：视频去重/防重、画中画（PicInPic 默认）、视频扩展、垂直填充、水平填充、背景扩展。

**典型场景**：

1. 帮我对视频做画中画去重处理。
   → `python scripts/mps_dedupe.py --url <URL>`（默认 PicInPic）
2. 视频需要做视频扩展去重，水平填充模式。
   → `python scripts/mps_dedupe.py --url <URL> --mode HorizontalExtend`
3. 视频去重，垂直填充模式。
   → `python scripts/mps_dedupe.py --cos-input-key input/vertical.mp4 --mode VerticalExtend`
4. 短剧同一集要在多个平台分发，每个平台判重严，请做一次视频去重处理。
   → `python scripts/mps_dedupe.py --cos-input-key input/drama.mp4 --mode PicInPic`
5. 把视频画面做扩展填充，上下左右扩展到目标分辨率。
   → `python scripts/mps_dedupe.py --url <URL> --mode BackgroundExtend`
6. 视频去重，等待结果完成，画中画模式。
   → `python scripts/mps_dedupe.py --url <URL> --mode PicInPic`（等待为默认行为）
7. 同一版素材我要上传 5 个账号，请帮我做去重处理，让每个版本哈希不一样。
   → `python scripts/mps_dedupe.py --url <URL> --mode PicInPic`

---

## 14. 精彩集锦 (`mps_highlight.py`)

**核心能力**：高光提取、自动剪辑精彩片段。**必须从预设场景中选择**（football/basketball/vlog/drama 等）。不支持直播流。支持 COS 输入、自定义 prompt、top-clip 数量控制、dry-run。

**典型场景**：

1. 帮我生成足球赛事精彩集锦，COS 路径：`input/football_game.mp4`。
   → `python scripts/mps_highlight.py --cos-input-key input/football_game.mp4 --scene football`
2. 篮球比赛视频，帮我提取精彩片段。
   → `python scripts/mps_highlight.py --url <URL> --scene basketball`
3. VLOG 视频提取高光片段，全景相机拍摄的。
   → `python scripts/mps_highlight.py --url <URL> --scene vlog-panorama`
4. 短剧视频提取高光。
   → `python scripts/mps_highlight.py --cos-input-key input/drama_highlight.mp4 --scene short-drama`
5. 滑雪视频提取精彩片段，自定义场景，关注人物高光动作。
   → `python scripts/mps_highlight.py --url <URL> --scene custom --prompt "关注人物高光动作"`
6. VLOG 集锦提取，要求输出前 10 个最精彩片段。
   → `python scripts/mps_highlight.py --url <URL> --scene vlog --top-clip 10`
7. 精彩集锦 dry run 测试，足球场景。
   → `python scripts/mps_highlight.py --url <URL> --scene football --dry-run`

---

## 15. AI 解说 (`mps_narrate.py`)

**核心能力**：AI 解说、短剧解说、短剧混剪、自动生成解说视频、短剧二创。**必须从预设场景中选择**，不支持自定义脚本。支持多集合并、多版本输出、no-wait。

**典型场景**：

1. 帮我对这个短剧视频做 AI 解说，视频有硬字幕。
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama`
2. 这个视频没有字幕，帮我做 AI 解说二创。
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama-no-erase`
3. 我有三集短剧需要合并解说。
   → `python scripts/mps_narrate.py --url <第一集URL> --extra-urls <第二集URL> <第三集URL> --scene short-drama`
4. 短剧解说，输出 3 个不同版本。
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama --output-count 3`
5. 帮我对 COS 上的短剧做 H.265 转码，同时生成 AI 解说，视频有硬字幕。
   → `python scripts/mps_narrate.py --cos-input-key input/episode.mp4 --scene short-drama` + `mps_transcode.py --cos-input-key input/episode.mp4 --codec h265`
6. 短剧视频有硬字幕，需要做 AI 解说，同时提取字幕翻译成英文。
   → `python scripts/mps_narrate.py --cos-input-key input/drama_ep1.mp4 --scene short-drama` + `mps_subtitle.py --cos-input-key input/drama_ep1.mp4 --translate en`
7. AI 解说 dry run，短剧视频，含字幕。
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama --dry-run`

---

## 16. 媒体质检 (`mps_qualitycontrol.py`)

**核心能力**：画质检测（模糊/花屏/黑场/绿屏）、播放兼容性检测、卡顿检测、音频质检、音频事件检测、视频诊断。**不包括音频内容理解或对比分析**（那是 `mps_av_understand.py`）。

**典型场景**：

1. 帮我对视频做画面质检，检查是否有模糊或花屏。
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 60`
2. 检测这个视频的播放兼容性，看看有没有卡顿问题。
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 70`
3. 对这个音频文件做音频质检。
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 50`
4. 帮我检查视频画质，不等待结果。
   → `python scripts/mps_qualitycontrol.py --cos-input-key input/video_check.mp4 --no-wait`
5. 视频画质检测，检查是否有画面受损问题，不等待。
   → `python scripts/mps_qualitycontrol.py --cos-input-key input/damaged.mp4 --definition 60 --no-wait`
6. 这批视频进入正式媒资库前必须先过质检。
   → `python scripts/mps_qualitycontrol.py --cos-input-key input/batch/ --definition 60`
7. 音轨看起来有问题：请用音频质检脚本检查是否有持续静音、爆音、码率异常。
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 50`

---

## 17. 用量统计 (`mps_usage.py`)

**核心能力**：MPS 服务调用次数/时长统计查询。支持按类型过滤、日期范围、全类型查询。**查询类，不产生费用**。

**典型场景**：

1. 查询我最近 30 天的 MPS 用量统计。
   → `python scripts/mps_usage.py --days 30`
2. 查询 2026 年 1 月份的 MPS 用量。
   → `python scripts/mps_usage.py --start 2026-01-01 --end 2026-01-31`
3. 查询转码和画质增强的用量统计，最近 7 天。
   → `python scripts/mps_usage.py --type Transcode Enhance --days 7`
4. 查询所有类型的 MPS 用量，最近 30 天。
   → `python scripts/mps_usage.py --all-types --days 30`
5. 帮我看看上周 MPS 的总调用量有没有异常波动。
   → `python scripts/mps_usage.py --days 7`
6. 查询 AIGC 用量和图片处理用量，最近 7 天。
   → `python scripts/mps_usage.py --type AIGC ImageProcess --days 7`
7. 查询 AI 质检用量，最近 30 天。
   → `python scripts/mps_usage.py --type AiQualityControl --days 30`

---

## 18. COS 与任务管理

### 18.1 上传/下载/列目录（`mps_cos_upload.py` / `mps_cos_download.py` / `mps_cos_list.py`）

1. 帮我把本地文件 `/home/user/video.mp4` 上传到 COS。
   → `python scripts/mps_cos_upload.py --local-file /home/user/video.mp4`
2. 把 COS 上的文件 `output/result.mp4` 下载到本地 `/tmp/result.mp4`。
   → `python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --local-file /tmp/result.mp4`
3. 列出 COS Bucket 里 `input/` 目录下的所有文件。
   → `python scripts/mps_cos_list.py --prefix input/`
4. 查看 COS 上所有 `.mp4` 文件。
   → `python scripts/mps_cos_list.py --search .mp4`
5. 列出 COS 上 `output/` 目录下的所有文件，显示文件 URL。
   → `python scripts/mps_cos_list.py --prefix output/ --show-url`
6. 批量把本地 `videos/` 目录下的视频都上传到 COS 的 `batch/` 路径下。
   → `python scripts/mps_cos_upload.py --local-file videos/ --cos-input-key batch/`

### 18.2 任务状态查询（`mps_get_video_task.py` / `mps_get_image_task.py`）

1. 查询视频处理任务状态，任务ID：`2600011633-WorkflowTask-abc123`。
   → `python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-abc123`
2. 查询图片处理任务状态，任务ID：`2600011633-ImageTask-xyz789`。
   → `python scripts/mps_get_image_task.py --task-id 2600011633-ImageTask-xyz789`
3. 这个转码任务我用 `--no-wait` 提交的，请帮我轮询查询最终结果。
   → `python scripts/mps_get_video_task.py --task-id <TaskId>`
4. 查询换装任务状态（换装任务用图片任务查询接口）。
   → `python scripts/mps_get_image_task.py --task-id 2600011633-ImageTask-tryon001`
5. 查询背景融合任务状态（不要使用视频任务查询接口）。
   → `python scripts/mps_get_image_task.py --task-id 2600007696-WorkflowTask-abc123`
6. 查询图片任务的详细信息，JSON 格式输出。
   → `python scripts/mps_get_image_task.py --task-id 2600011633-ImageTask-img001 --json`
7. 查询 AI 解说任务状态。
   → `python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-narrate001`

### 18.3 环境变量检查（`mps_load_env.py`）

1. 帮我检查一下环境变量配置是否正确。
   → `python scripts/mps_load_env.py --check-only`
2. 我换了一组新密钥，请验证当前配置是否能正常调用 MPS。
   → `python scripts/mps_load_env.py --check-only`
3. 检查一下 COS 配置是否完整，准备跑一次任务。
   → `python scripts/mps_load_env.py --check-only`
4. 新机器部署完成，帮我检查 MPS 环境变量是否已经生效。
   → `python scripts/mps_load_env.py --check-only`
5. 怀疑 SecretKey 失效了，请用环境变量检查脚本确认一下。
   → `python scripts/mps_load_env.py --check-only`
6. 验证一下 MPS 的配置是否正确。
   → `python scripts/mps_load_env.py --check-only`

---

## 19. 效果对比 (`mps_gen_compare.py`)

**核心能力**：生成交互式 HTML 对比页面，支持视频左右滑动对比、图片并排对比。**不调用 MPS API，不产生费用**。支持视频和图片两种对比类型。

**典型场景**：

1. 帮我把视频增强前后的效果对比一下，原始视频：`<URL>`，增强后的：`<URL>`。
   → `python scripts/mps_gen_compare.py --original <原始URL> --enhanced <增强后URL>`
2. 生成一个图片超分前后的对比页面，原图：`<URL>`，处理后：`<URL>`。
   → `python scripts/mps_gen_compare.py --original <原图URL> --enhanced <处理后URL> --type image`
3. 我想看看去水印的效果，帮我做个前后对比。
   → `python scripts/mps_gen_compare.py --original <原始URL> --enhanced <处理后URL> --title "去水印效果对比"`
4. 画质增强跑完了，帮我生成一个前后对比的 HTML 页面，可以滑动对比。
   → `python scripts/mps_gen_compare.py --original <原始URL> --enhanced <增强后URL>`
5. 图片超分完成后，做一个原图和超分后图片的并排对比页面。
   → `python scripts/mps_gen_compare.py --original <原图URL> --enhanced <超分后URL> --type image`
6. 视频去字幕前后的效果，要生成 HTML 对比文件。
   → `python scripts/mps_gen_compare.py --original <原始URL> --enhanced <去字幕后URL>`
7. 同一段视频跑了两种增强模板（真人 vs 漫剧），帮我生成 3 路对比页面。
   → `python scripts/mps_gen_compare.py --original <原始URL> --enhanced <真人增强URL> --enhanced2 <漫剧增强URL>`

---

## 附：路由速查 & 使用建议

1. **"视频 vs 图片"是第一分流**：同样是"擦除水印"，视频走 `mps_erase.py`，图片走 `mps_imageprocess.py`。
2. **"画质提升到 1080P/2K/4K"属于增强**（`mps_enhance.py`），**不是转码**。转码只做编码/码率/容器格式变换。
3. **"音频对比分析/音频内容理解"走 `mps_av_understand.py`**，**不要误用 `mps_qualitycontrol.py`**（后者是物理层质检：爆音、静音、削波等）。
4. **Kling 模型支持分镜视频**（1-6 个分镜，时长之和 = 总时长），其他 AIGC 视频模型不支持。
5. **AIGC 生图/生视频任务**必须用各自脚本的 `--task-id` 查询（`mps_aigc_image.py --task-id` / `mps_aigc_video.py --task-id`），**不能**用 `mps_get_video_task.py` 或 `mps_get_image_task.py` 查询。
6. **必须追问参数的脚本**：音频分离必须指定 vocal/background/accompaniment；精彩集锦和 AI 解说必须指定预设场景；音视频理解必须提供 `--mode` 和 `--prompt`；视频二创必须提供 `--mode`。
7. **处理类脚本调用前必须给费用提示**；查询类（usage / get_task / cos_list）和上传下载类（cos_upload / cos_download）无需提示。
8. **输入源判断**：URL 用 `--url`；用户明确说 COS 用 `--cos-input-key`；其余一律 `--local-file`，不要反问用户是不是 COS。
9. **换装任务状态查询**统一使用 `mps_get_image_task.py`（不用 `mps_get_video_task.py`）。
10. **背景融合任务状态查询**也使用 `mps_get_image_task.py`。
11. **dry-run / no-wait 场景**：dry-run 只预览不执行；no-wait 提交后不轮询等待结果但任务已创建，可通过 `mps_get_video_task.py` / `mps_get_image_task.py` 手动查询。
12. **多步骤请求**：当用户要求同时做两件或多件事（如转码+字幕提取、质检+增强），应分别生成对应的多条脚本命令。
13. **用户明确指定 ffmpeg 时不应触发 MPS**，直接给出 ffmpeg 命令。
14. **用户只是询问工具推荐或产品对比，不需要实际处理时不触发 MPS**。

---

> **维护说明**：本文档从 `evals.json` 正向用例中提炼，能力分类与 SKILL.md 的"脚本功能映射（职责边界）"表一一对应。任何脚本能力调整（新增脚本、拆分合并、参数变更）都应同步更新本文档，确保场景描述的真实性与可执行性。
