# tencent-mps Best-Practice Scenarios

> This document distills scenarios from the positive cases in `evals.json` and groups them by the 19 capability modules defined in SKILL.md. Each scenario is a natural-language description sourced from the diverse queries in real test cases, and can be used directly as:
>
> - Positive samples for skill-trigger-rate testing
> - A "capability-to-scenario" cheat sheet for product/operations/sales when introducing the skill to customers
> - A quick reference helping new users decide "which MPS capability does my requirement belong to"
>
> Each scenario is annotated with the corresponding **processing script** and key parameters, so you can cross-reference the script-routing table in SKILL.md when executing.

---

## Table of Contents

1. [Video Transcoding](#1-video-transcoding-mps_transcodepy)
2. [Quality Enhancement](#2-quality-enhancement-mps_enhancepy)
3. [Audio Processing (Audio Separation)](#3-audio-processing-audio-separation-mps_enhancepy)
4. [Subtitles & Speech](#4-subtitles--speech-mps_subtitlepy)
5. [Erase & Occlusion (Video)](#5-erase--occlusion-video-mps_erasepy)
6. [Image Processing](#6-image-processing-mps_imageprocesspy)
7. [Image Try-On](#7-image-try-on-mps_image_tryonpy)
8. [Image Background Fusion](#8-image-background-fusion-mps_image_bg_fusionpy)
9. [AIGC Image Generation](#9-aigc-image-generation-mps_aigc_imagepy)
10. [AIGC Video Generation](#10-aigc-video-generation-mps_aigc_videopy)
11. [Audio/Video Content Understanding](#11-audiovideo-content-understanding-mps_av_understandpy)
12. [Video Re-creation](#12-video-re-creation-mps_vremakepy)
13. [Video De-duplication](#13-video-de-duplication-mps_dedupepy)
14. [Highlight Reel](#14-highlight-reel-mps_highlightpy)
15. [AI Narration](#15-ai-narration-mps_narratepy)
16. [Media Quality Control](#16-media-quality-control-mps_qualitycontrolpy)
17. [Usage Statistics](#17-usage-statistics-mps_usagepy)
18. [COS & Task Management](#18-cos--task-management)
    - [18.1 Upload / Download / List](#181-upload--download--list)
    - [18.2 Task Status Query](#182-task-status-query)
    - [18.3 Environment-Variable Check](#183-environment-variable-check)
19. [Effect Comparison](#19-effect-comparison-mps_gen_comparepy)

---

## 1. Video Transcoding (`mps_transcode.py`)

**Core capabilities**: video/audio codec conversion; bitrate / resolution / frame-rate adjustment; container format conversion (MP4 / AVI / MKV / FLV / MOV / HLS, etc.); switching between H.264 / H.265 / AV1; compression and slimming; ultra-fast HD compression (`ultra_compress`).

**Typical scenarios**:

1. I have a 1.2 GB MOV video shot on my phone and want to compress it into MP4 to send to a colleague over WeChat — please handle it.
   → `python scripts/mps_transcode.py --url <video URL> --codec h264 --format MP4`
2. Compress the video `input/my_video.mp4` on COS, convert it to H.264 with a bitrate of 2000 kbps.
   → `python scripts/mps_transcode.py --cos-input-key input/my_video.mp4 --codec h264 --bitrate 2000`
3. I want to convert the video to MP4 but I don't want to wait for the result — just submit the task.
   → `python scripts/mps_transcode.py --url <video URL> --format MP4 --no-wait`
4. Transcode this video to H.265: `https://ie-mps-1258344699.cos.ap-nanjing.tencentcos.cn/evanxia/mps/vivienyao/test_video_01.mp4`
   → `python scripts/mps_transcode.py --url <URL> --codec h265`
5. Convert the video to H.264 at 1280x720 resolution and 30 fps.
   → `python scripts/mps_transcode.py --url <URL> --codec h264`
6. Local video `/home/user/video.mp4` needs H.265 transcoding (full pipeline: upload to COS first, then transcode, then download).
   → `python scripts/mps_transcode.py --local-file /home/user/video.mp4 --codec h265`
7. I have a local video `/data/my_video.mp4` — please transcode it to H.265 (full three-step pipeline).
   → `python scripts/mps_transcode.py --local-file /data/my_video.mp4 --codec h265`

---

## 2. Quality Enhancement (`mps_enhance.py`)

**Core capabilities**: video super-resolution, quality restoration, old-film restoration, super-resolution upscaling, quality boost, real-person enhancement, anime/animated-drama enhancement, anime super-resolution, shake stabilization, detail enhancement, face fidelity, sharpness boost to 720P / 1080P / 2K / 4K. Also includes audio-enhancement capabilities such as noise reduction, loudness leveling and audio beautification.

**Typical scenarios**:

1. Enhance the video quality to 1080P. The video is real-person footage.
   → `python scripts/mps_enhance.py --url <URL> --template 327003` (real-person 1080P template)
2. This is an old anime video — upscale it to 4K.
   → `python scripts/mps_enhance.py --url <URL> --template 327008` (anime 4K template)
3. The video is a bit shaky — apply shake stabilization and enhance to 2K.
   → `python scripts/mps_enhance.py --cos-input-key input/shaky.mp4 --template 327011` (shake-stabilization 2K template)
4. Enhance the animated-drama video to 2K.
   → `python scripts/mps_enhance.py --url <URL> --template 327006` (animated-drama 2K template)
5. Enhance the video to 720P, real-person scene.
   → `python scripts/mps_enhance.py --cos-input-key input/low_res.mp4 --template 327001` (real-person 720P template)
6. Face-fidelity enhancement to 1080P.
   → `python scripts/mps_enhance.py --url <URL> --template 327018` (face-fidelity 1080P template)
7. Strongest detail-enhancement mode, upscale to 4K.
   → `python scripts/mps_enhance.py --url <URL> --template 327016` (max-detail 4K template)
8. Shake-stabilization 720P enhancement.
   → `python scripts/mps_enhance.py --cos-input-key input/shaky720.mp4 --template 327009 --no-wait`
9. Real-person live-action video enhanced to 1080P.
   → `python scripts/mps_enhance.py --cos-input-key input/real_person.mp4 --template 327003`
10. Local video, enhance to 1080P real-person scene (must upload to COS first).
    → `python scripts/mps_enhance.py --local-file /home/user/input.mp4 --template 327003`

---

## 3. Audio Processing (Audio Separation) (`mps_enhance.py`)

**Core capabilities**: vocal extraction, vocal separation, accompaniment extraction, BGM separation, background-music extraction, vocal removal, accompaniment removal, audio-track extraction. **`--audio-separate vocal/background/accompaniment` must be specified (choose one)**.

**Typical scenarios**:

1. Extract the vocals (vocal separation) from this video: `https://vivien-1256342427.cos.ap-nanjing.myqcloud.com/MPS/QZ3jiuY4CrUA.mp4`
   → `python scripts/mps_enhance.py --url <URL> --audio-separate vocal`
2. I love the background music in this video — can you pull out the pure BGM and save it as a standalone MP3?
   → `python scripts/mps_enhance.py --url <URL> --audio-separate background`
3. For short-video re-creation, I need to remove the original vocals and keep only ambient sound + BGM.
   → `python scripts/mps_enhance.py --url <URL> --audio-separate accompaniment`
4. Give me a vocals-removed accompaniment of this interview video — I'll record a new voice-over.
   → `python scripts/mps_enhance.py --url <URL> --audio-separate accompaniment`
5. Make a karaoke version: remove the vocals from this live performance, keeping only the accompaniment.
   → `python scripts/mps_enhance.py --url <URL> --audio-separate accompaniment`
6. The video has both vocals and background music — extract the vocals (vocal separation).
   → `python scripts/mps_enhance.py --url <URL> --audio-separate vocal`
7. Separate the vocals and background music of the video, and at the same time transcode the video to H.264.
   → `python scripts/mps_enhance.py --cos-input-key input/music_video.mp4 --audio-separate vocal` + `mps_transcode.py --cos-input-key input/music_video.mp4 --codec h264`

---

## 4. Subtitles & Speech (`mps_subtitle.py`)

**Core capabilities**: speech recognition (ASR) for subtitle generation, hard-subtitle OCR extraction, subtitle translation, SRT output, speech-to-text, multilingual video subtitles, OCR region specification.

**Typical scenarios**:

1. Extract subtitles from this video: `https://vivien-1256342408.cos.ap-nanjing.myqcloud.com/DEMO/trailer.mp4`
   → `python scripts/mps_subtitle.py --url <URL>`
2. Translate the subtitles of this English video into Chinese.
   → `python scripts/mps_subtitle.py --url <URL> --translate`
3. I have a Chinese video — extract its subtitles and translate them into English.
   → `python scripts/mps_subtitle.py --cos-input-key input/chinese.mp4 --translate`
4. Run speech recognition on this video and output the text.
   → `python scripts/mps_subtitle.py --url <URL>`
5. This video has burned-in subtitles — use OCR to recognize and extract them.
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr`
6. Use OCR to recognize this video's subtitles and translate them into English.
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr --translate en`
7. The video has fancy subtitles at the bottom — use OCR but only on the bottom 30% of the frame.
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr --ocr-area`
8. Extract the on-screen text from the video; the video is bilingual Chinese/English.
   → `python scripts/mps_subtitle.py --url <URL> --process-type ocr --src-lang zh_en`
9. The video has burned-in hard subtitles — use OCR to extract them and translate into Japanese.
   → `python scripts/mps_subtitle.py --cos-input-key input/hardcoded_subtitle.mp4 --process-type ocr --translate ja`
10. Extract subtitles from the video without waiting for the task to finish.
    → `python scripts/mps_subtitle.py --url <URL> --no-wait`

---

## 5. Erase & Occlusion (Video) (`mps_erase.py`)

**Core capabilities**: subtitle removal in video frames, watermark removal, face blurring, license-plate blurring, privacy occlusion, mosaic. **Video only — for images, use `mps_imageprocess.py`**.

**Typical scenarios**:

1. Remove the subtitles from this video: `https://lily-1256342427.cos.ap-nanjing.myqcloud.com/mps_autotest/subtitle/subtitle.mkv`
   → `python scripts/mps_erase.py --url <URL> --template 101` (subtitle-removal template)
2. There's a watermark in the video — please apply the advanced watermark-removal template.
   → `python scripts/mps_erase.py --url <URL> --template 201` (advanced watermark-removal template)
3. There are faces in this video — apply face blurring.
   → `python scripts/mps_erase.py --cos-input-key input/faces.mp4 --template 301` (face-blur template)
4. The video contains both faces and license plates — both need to be blurred.
   → `python scripts/mps_erase.py --url <URL> --template 302` (face + license-plate blur template)
5. Remove the subtitles from the video and also extract the subtitle text via OCR.
   → `python scripts/mps_erase.py --url <URL> --template 102` (subtitle-removal + OCR template)
6. There's a watermark in the top-left of the video — please remove it.
   → `python scripts/mps_erase.py --cos-input-key input/watermark.mp4 --template 201`
7. Real-person live-action video has a watermark in the top-left — remove it and at the same time apply 1080P enhancement.
   → `python scripts/mps_erase.py --cos-input-key input/watermark.mp4 --template 201` + `mps_enhance.py --cos-input-key input/watermark.mp4 --template 327003`

---

## 6. Image Processing (`mps_imageprocess.py`)

**Core capabilities**: image super-resolution, advanced super-resolution, beautification, denoising, color enhancement, detail enhancement, face enhancement, low-light enhancement, comprehensive enhancement, format conversion, scaling/cropping, filters, **image text/watermark/icon erasure**, **invisible watermark**. **Image watermark removal belongs to this script, NOT the video erase script `mps_erase.py`**.

**Typical scenarios**:

1. Apply super-resolution to this image: `https://lily-1256342427.cos.ap-nanjing.myqcloud.com/mps_autotest/pic.jpeg`
   → `python scripts/mps_imageprocess.py --url <URL>` (default image super-resolution)
2. This portrait photo needs beautification (skin smoothing and whitening).
   → `python scripts/mps_imageprocess.py --cos-input-key input/portrait.jpg --process-type beautify`
3. The image is noisy — apply denoising.
   → `python scripts/mps_imageprocess.py --url <URL> --process-type denoise`
4. Image super-resolution, no wait, COS path: `input/lowres.jpg`.
   → `python scripts/mps_imageprocess.py --cos-input-key input/lowres.jpg --no-wait`
5. There's a logo watermark in the bottom-right of the image — erase it.
   → `python scripts/mps_imageprocess.py --cos-input-key input/logo.jpg --process-type erase` (use this script for image erasure)
6. I want to add invisible watermarks to a batch of images for copyright tracing.
   → `python scripts/mps_imageprocess.py --cos-input-key input/batch/ --process-type blind-watermark`
7. Convert this PNG to JPEG and resize it to 1920×1080.
   → `python scripts/mps_imageprocess.py --cos-input-key input/photo.png --process-type resize --target-format JPEG --width 1920 --height 1080`
8. A batch of source images is a bit blurry — run a comprehensive enhancement (super-resolution + denoising + color).
   → `python scripts/mps_imageprocess.py --cos-input-key input/batch/ --process-type enhance`

---

## 7. Image Try-On (`mps_image_tryon.py`)

**Core capabilities**: image try-on, AI clothing fitting, garment replacement, model dressing, virtual try-on. The general scenario supports 1–2 garment images; the lingerie scenario (`--schedule-id 30101`) supports only 1 garment image. Three input modes are supported: URL, COS key, and local file.

**Typical scenarios**:

1. Generate a model image with AI, then make her wear this T-shirt.
   → `python scripts/mps_image_tryon.py --model-url <model URL> --cloth-url <garment URL>`
2. We launched a batch of new dresses on our e-commerce site — instead of re-shooting model photos, can you put the new dresses on the original model?
   → `python scripts/mps_image_tryon.py --model-cos-key input/model.jpg --cloth-cos-key input/dress.jpg`
3. This is a flat-lay white-background image from the apparel supply chain — composite it onto a standard model to generate the main listing image.
   → `python scripts/mps_image_tryon.py --model-url <model URL> --cloth-url <flat-lay URL>`
4. We are a lingerie brand and want a virtual try-on; only the top lingerie piece needs to be replaced.
   → `python scripts/mps_image_tryon.py --model-url <model URL> --cloth-url <lingerie URL> --schedule-id 30101`
5. Limited budget for product photography — let's try AI try-on first to generate the main image for the detail page.
   → `python scripts/mps_image_tryon.py --model-cos-key input/model.jpg --cloth-cos-key input/cloth.jpg`
6. Same model pose — please try on 5 SKUs of clothing in batch and output 5 different model images.
   → `python scripts/mps_image_tryon.py --model-url <model URL> --cloth-url <garment 1 URL>` × 5 times
7. Local image try-on. Model image: `/data/model.jpg`, garment image: `/data/cloth.jpg`.
   → `python scripts/mps_image_tryon.py --local-file /data/model.jpg /data/cloth.jpg` (or upload to COS first, then try on)

---

## 8. Image Background Fusion (`mps_image_bg_fusion.py`)

**Core capabilities**: image background replacement, product-image background change, AI background generation, automatic background generation from a text prompt, e-commerce backgrounds. You can upload "subject + background" for compositing, or just the subject + `--prompt` to auto-generate. Three input modes: URL, COS key (with bucket/region).

**Typical scenarios**:

1. Run background fusion. Product image: `<URL>`, background image: `<URL>`.
   → `python scripts/mps_image_bg_fusion.py --subject-url <product URL> --bg-url <background URL>`
2. This is a white-background product image — replace it with a natural outdoor-grass background to create a spring/summer outdoor-style main image.
   → `python scripts/mps_image_bg_fusion.py --subject-url <product URL> --prompt "outdoor grass natural light spring/summer style"`
3. I only have a cut-out of the product and no suitable background asset — generate a background from a prompt.
   → `python scripts/mps_image_bg_fusion.py --subject-url <product URL> --prompt "Nordic-style living room with wooden floor and afternoon sunlight"`
4. AI background replacement. Subject is on COS at `input/product.jpg`, background image: `<URL>`.
   → `python scripts/mps_image_bg_fusion.py --subject-cos-key input/product.jpg --bg-url <background URL>`
5. Background fusion — both subject and background are on COS. Subject: `input/product.jpg`, background: `input/bg.jpg`.
   → `python scripts/mps_image_bg_fusion.py --subject-cos-key input/product.jpg --bg-cos-key input/bg.jpg`
6. Product-image background replacement. Subject: `<URL>`, background: `<URL>`. Fusion requirement: add warm-tone lighting.
   → `python scripts/mps_image_bg_fusion.py --subject-url <subject URL> --bg-url <background URL> --prompt "warm-tone lighting"`
7. E-commerce background generation. Product image: `<URL>`. Background description: outdoor lawn in bright sunshine, fixed random seed 42.
   → `python scripts/mps_image_bg_fusion.py --subject-url <product URL> --prompt "outdoor lawn bright sunshine" --random-seed 42`
8. Background generation. Product image: `<URL>`. Background description: modern minimalist living room. Output in PNG format at 4K size.
   → `python scripts/mps_image_bg_fusion.py --subject-url <product URL> --prompt "modern minimalist living room" --format PNG --image-size 4K`

---

## 9. AIGC Image Generation (`mps_aigc_image.py`)

**Core capabilities**: text-to-image, image-to-image, AI painting, 3D panoramic image. Supports 6 models: `Hunyuan` (default) / `GEM` (2.5/3.0/3.1, multi-image reference) / `Qwen` / `Vidu` (q2) / `Kling` (2.1/O1/3.0/3.0-Omni) / `OG` (image2_low/image2_medium/image2_high). Hunyuan supports `--scene-type 3d_panorama` to generate oversized panoramic images (~27MB).

**Typical scenarios**:

1. Generate an image with AI. Description: a golden retriever running on the grass in bright sunshine.
   → `python scripts/mps_aigc_image.py --prompt "a golden retriever running on the grass in bright sunshine"`
2. Use this image as a reference and generate a new image in a similar style. Description: seaside at sunset.
   → `python scripts/mps_aigc_image.py --prompt "seaside at sunset" --image-url <reference URL>`
3. AIGC image, reference image is on COS: bucket=`mps-test-1234567`, region=`ap-guangzhou`, key=`input/ref.jpg`. Prompt: city night view.
   → `python scripts/mps_aigc_image.py --prompt "city night view" --image-cos-bucket mps-test-1234567 --image-cos-region ap-guangzhou --image-cos-key input/ref.jpg`
4. Generate 4 poster images from the prompt "cyberpunk-style Hong Kong street, neon lights on a rainy night".
   → `python scripts/mps_aigc_image.py --prompt "cyberpunk-style Hong Kong street, neon lights on a rainy night"`
5. Use this cat photo as a reference and create a watercolor-style version via image-to-image.
   → `python scripts/mps_aigc_image.py --prompt "watercolor-style cat" --image-url <cat photo URL>`
6. AIGC image, dry-run the command first. Prompt: city night view with neon lights.
   → `python scripts/mps_aigc_image.py --prompt "city night view with neon lights" --dry-run`
7. Generate a "Spring-Festival red-themed gift-box packaging visual" for the e-commerce home banner.
   → `python scripts/mps_aigc_image.py --prompt "Spring-Festival red-themed gift-box packaging visual"`
8. Use Kling 3.0 to generate a realistic landscape painting.
   → `python scripts/mps_aigc_image.py --prompt "realistic landscape painting" --model Kling --model-version 3.0`
9. Use OG high-quality mode to generate a city night scene.
   → `python scripts/mps_aigc_image.py --prompt "city night view with neon lights" --model OG --model-version image2_high`
10. Use Hunyuan to generate a 3D panoramic image of a tropical rainforest.
    → `python scripts/mps_aigc_image.py --prompt "tropical rainforest panorama, lush and vibrant" --model Hunyuan --scene-type 3d_panorama`

---

## 10. AIGC Video Generation (`mps_aigc_video.py`)

**Core capabilities**: text-to-video, image-to-video, **Kling-model multi-shot storyboards** (1–6 shots, where the sum of shot durations equals the total duration). Supports pure-prompt text-to-video, image-to-video (URL or COS), Kling multi-shot, output-count control, random seed, dry-run, and no-wait.

**Typical scenarios**:

1. Generate a video with AI. Text description: a cat sunbathing by the window, lazily stretching.
   → `python scripts/mps_aigc_video.py --prompt "a cat sunbathing by the window, lazily stretching"`
2. Generate a video from this image. Image URL: `<URL>`. Description: a breeze rustling the leaves.
   → `python scripts/mps_aigc_video.py --prompt "a breeze rustling the leaves" --image-url <image URL>`
3. Use the Kling model to generate a multi-shot storyboard, total 10 seconds, 2 shots: first 5s sunrise, second 5s sunset.
   → `python scripts/mps_aigc_video.py --prompt "sunrise" --multi-shot --multi-prompts-json '[{"prompt":"sunrise","duration":5},{"prompt":"sunset","duration":5}]'`
4. AI video generation, no wait — just give me the task ID. Prompt: snow-mountain sunrise.
   → `python scripts/mps_aigc_video.py --prompt "snow-mountain sunrise" --no-wait`
5. Use Kling to generate a 5-second video from "seaside sunrise, waves crashing on rocks, slow push-in".
   → `python scripts/mps_aigc_video.py --prompt "seaside sunrise, waves crashing on rocks, slow push-in"`
6. I have a static product image — turn it into a 3-second camera-movement video pushing in from far to near.
   → `python scripts/mps_aigc_video.py --prompt "camera pushing in from far to near on the product" --image-url <product image URL>`
7. AIGC video dry-run. Prompt: stormy sea.
   → `python scripts/mps_aigc_video.py --prompt "stormy sea" --dry-run`

---

## 11. Audio/Video Content Understanding (`mps_av_understand.py`)

**Core capabilities**: video content analysis, video summarization, scene recognition, comparative analysis of two videos / two audio tracks, audio understanding. **Both `--mode` and `--prompt` are required**. Supports video URL and COS input.

**Typical scenarios**:

1. Analyze the content of this video — identify the main scenes and key information.
   → `python scripts/mps_av_understand.py --url <URL> --mode video --prompt "Analyze the video content and key information"`
2. Comparatively analyze the differences between these two audio tracks.
   → `python scripts/mps_av_understand.py --url <video 1 URL> --extend-url <video 2 URL> --mode compare --prompt "Compare the differences between the two audio tracks"`
3. Video content understanding, COS path `input/meeting.mp4` — summarize the key points of the meeting.
   → `python scripts/mps_av_understand.py --cos-input-key input/meeting.mp4 --mode video --prompt "Summarize the key points of the meeting"`
4. Run picture-quality QC on this video to check for blurring or screen artifacts (note: QC is handled by `mps_qualitycontrol.py`; here it is content understanding).
   → `python scripts/mps_av_understand.py --url <URL> --mode video --prompt "Describe the visual content of the video"`
5. Understand this video's content — give me a summary and key information; don't wait for the result.
   → `python scripts/mps_av_understand.py --url <URL> --mode video --prompt "Summary and key information" --no-wait`
6. Compare the narration differences between the two videos.
   → `python scripts/mps_av_understand.py --url <video 1 URL> --extend-url <video 2 URL> --mode compare --prompt "Compare narration differences"`
7. Video content understanding — describe the video content.
   → `python scripts/mps_av_understand.py --cos-input-key input/ocean.mp4 --mode video --prompt "Describe the video content"`

---

## 12. Video Re-creation (`mps_vremake.py`)

**Core capabilities**: face swap, character swap, video interleave (AB editing). **`--mode` is required** (SwapFace / SwapCharacter / VideoInterleave / AB).

**Typical scenarios**:

1. Do a video face swap. Source face: `<URL>`, target face: `<URL>`, video: `<URL>`.
   → `python scripts/mps_vremake.py --url <video URL> --mode SwapFace --src-faces <source face URL> --dst-faces <target face URL>`
2. Video character swap. Source character image: `<URL>`, target character image: `<URL>`, video: `<URL>`. Wait for the result.
   → `python scripts/mps_vremake.py --url <video URL> --mode SwapCharacter --src-character <source character URL> --dst-character <target character URL>`
3. Run AB-interleave video re-creation.
   → `python scripts/mps_vremake.py --url <video URL> --mode AB`
4. Face swap — replace the person in the video with the face from this image; no wait.
   → `python scripts/mps_vremake.py --url <video URL> --mode SwapFace --src-faces <face URL> --dst-faces <target face URL> --no-wait`
5. Video re-creation with face swap, but I haven't decided which mode to use — please introduce the available modes.
   → AI introduces `SwapFace` / `SwapCharacter` / `VideoInterleave` / `AB` modes and asks the user to choose.
6. Video re-creation with face swap — replace the host's face with the 2D cartoon mascot.
   → `python scripts/mps_vremake.py --url <video URL> --mode SwapFace --src-faces <host face URL> --dst-faces <mascot URL>`
7. The endorser in this old commercial needs to be swapped with a new endorser's face — keep the original lines and motion.
   → `python scripts/mps_vremake.py --url <video URL> --mode SwapFace --src-faces <old endorser URL> --dst-faces <new endorser URL>`

---

## 13. Video De-duplication (`mps_dedupe.py`)

**Core capabilities**: video de-duplication / anti-duplication, picture-in-picture (PicInPic, default), video extension, vertical filling, horizontal filling, background extension.

**Typical scenarios**:

1. Apply picture-in-picture de-duplication to the video.
   → `python scripts/mps_dedupe.py --url <URL>` (defaults to PicInPic)
2. The video needs video-extension de-duplication, horizontal-fill mode.
   → `python scripts/mps_dedupe.py --url <URL> --mode HorizontalExtend`
3. Video de-duplication, vertical-fill mode.
   → `python scripts/mps_dedupe.py --cos-input-key input/vertical.mp4 --mode VerticalExtend`
4. The same episode of a short drama is being distributed to multiple platforms with strict duplicate detection — please run de-duplication.
   → `python scripts/mps_dedupe.py --cos-input-key input/drama.mp4 --mode PicInPic`
5. Extend the video frame, filling top/bottom/left/right to the target resolution.
   → `python scripts/mps_dedupe.py --url <URL> --mode BackgroundExtend`
6. Video de-duplication, wait for the result, picture-in-picture mode.
   → `python scripts/mps_dedupe.py --url <URL> --mode PicInPic` (waiting is the default behavior)
7. I need to upload the same asset to 5 accounts — please de-duplicate so each version has a different hash.
   → `python scripts/mps_dedupe.py --url <URL> --mode PicInPic`

---

## 14. Highlight Reel (`mps_highlight.py`)

**Core capabilities**: highlight extraction, automatic editing of highlight clips. **A scene must be chosen from the preset list** (football / basketball / vlog / drama, etc.). Live streams are not supported. Supports COS input, custom prompt, top-clip count, and dry-run.

**Typical scenarios**:

1. Generate a football-match highlight reel. COS path: `input/football_game.mp4`.
   → `python scripts/mps_highlight.py --cos-input-key input/football_game.mp4 --scene football`
2. Basketball-game video — extract highlight clips.
   → `python scripts/mps_highlight.py --url <URL> --scene basketball`
3. Extract highlights from a vlog video shot with a 360 panoramic camera.
   → `python scripts/mps_highlight.py --url <URL> --scene vlog-panorama`
4. Extract highlights from a short drama.
   → `python scripts/mps_highlight.py --cos-input-key input/drama_highlight.mp4 --scene short-drama`
5. Skiing video — extract highlight clips, custom scene, focus on highlight actions of people.
   → `python scripts/mps_highlight.py --url <URL> --scene custom --prompt "Focus on highlight actions of people"`
6. Vlog highlight extraction — output the top 10 most-exciting clips.
   → `python scripts/mps_highlight.py --url <URL> --scene vlog --top-clip 10`
7. Highlight reel dry-run test, football scene.
   → `python scripts/mps_highlight.py --url <URL> --scene football --dry-run`

---

## 15. AI Narration (`mps_narrate.py`)

**Core capabilities**: AI narration, short-drama narration, short-drama remix, automatic generation of narrated videos, short-drama re-creation. **A scene must be chosen from the preset list — custom scripts are not supported**. Supports multi-episode merging, multi-version output, and no-wait.

**Typical scenarios**:

1. Generate AI narration for this short-drama video; the video has burned-in subtitles.
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama`
2. The video has no subtitles — generate AI narration for re-creation.
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama-no-erase`
3. I have three episodes of a short drama to be merged and narrated.
   → `python scripts/mps_narrate.py --url <episode 1 URL> --extra-urls <episode 2 URL>,<episode 3 URL> --scene short-drama`
4. Short-drama narration — output 3 different versions.
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama --output-count 3`
5. Transcode the short drama on COS to H.265 and at the same time generate AI narration; the video has burned-in subtitles.
   → `python scripts/mps_narrate.py --cos-input-key input/episode.mp4 --scene short-drama` + `mps_transcode.py --cos-input-key input/episode.mp4 --codec h265`
6. The short-drama video has burned-in subtitles — generate AI narration and at the same time extract the subtitles and translate them into English.
   → `python scripts/mps_narrate.py --cos-input-key input/drama_ep1.mp4 --scene short-drama` + `mps_subtitle.py --cos-input-key input/drama_ep1.mp4 --translate en`
7. AI narration dry-run, short-drama video with subtitles.
   → `python scripts/mps_narrate.py --url <URL> --scene short-drama --dry-run`

---

## 16. Media Quality Control (`mps_qualitycontrol.py`)

**Core capabilities**: picture-quality detection (blur / artifacts / black frames / green frames), playback-compatibility detection, stutter detection, audio QC, audio-event detection, video diagnostics. **Does NOT include audio content understanding or comparative analysis (those belong to `mps_av_understand.py`)**.

**Typical scenarios**:

1. Run picture-quality QC on the video — check for blur or screen artifacts.
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 60`
2. Detect this video's playback compatibility and check for stutter.
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 70`
3. Run audio QC on this audio file.
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 50`
4. Check the video's picture quality, no wait.
   → `python scripts/mps_qualitycontrol.py --cos-input-key input/video_check.mp4 --no-wait`
5. Video picture-quality detection — check for visual damage, no wait.
   → `python scripts/mps_qualitycontrol.py --cos-input-key input/damaged.mp4 --definition 60 --no-wait`
6. This batch of videos must pass QC before being ingested into the official media library.
   → `python scripts/mps_qualitycontrol.py --cos-input-key input/batch/ --definition 60`
7. The audio track looks problematic — please run audio QC to check for sustained silence, clipping, or abnormal bitrate.
   → `python scripts/mps_qualitycontrol.py --url <URL> --definition 50`

---

## 17. Usage Statistics (`mps_usage.py`)

**Core capabilities**: query MPS service call-count / duration usage statistics. Supports filtering by type, date range, and all-types query. **Read-only — does not incur charges**.

**Typical scenarios**:

1. Query my MPS usage statistics for the last 30 days.
   → `python scripts/mps_usage.py --days 30`
2. Query MPS usage for January 2026.
   → `python scripts/mps_usage.py --start 2026-01-01 --end 2026-01-31`
3. Query usage statistics for transcoding and quality enhancement, last 7 days.
   → `python scripts/mps_usage.py --type Transcode Enhance --days 7`
4. Query usage of all MPS types, last 30 days.
   → `python scripts/mps_usage.py --all-types --days 30`
5. Check whether MPS total call volume had any abnormal spikes last week.
   → `python scripts/mps_usage.py --days 7`
6. Query AIGC usage and image-processing usage, last 7 days.
   → `python scripts/mps_usage.py --type AIGC ImageProcess --days 7`
7. Query AI quality-control usage, last 30 days.
   → `python scripts/mps_usage.py --type AiQualityControl --days 30`

---

## 18. COS & Task Management

### 18.1 Upload / Download / List (`mps_cos_upload.py` / `mps_cos_download.py` / `mps_cos_list.py`)

1. Upload the local file `/home/user/video.mp4` to COS.
   → `python scripts/mps_cos_upload.py --local-file /home/user/video.mp4`
2. Download the file `output/result.mp4` on COS to local `/tmp/result.mp4`.
   → `python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --local-file /tmp/result.mp4`
3. List all files under the `input/` directory in the COS bucket.
   → `python scripts/mps_cos_list.py input/`
4. List all `.mp4` files on COS.
   → `python scripts/mps_cos_list.py .mp4`
5. List all files under `output/` on COS, showing file URLs.
   → `python scripts/mps_cos_list.py output/ --show-url`
6. Batch-upload all videos under the local `videos/` directory to the COS path `batch/`.
   → `python scripts/mps_cos_upload.py --local-file videos/ --cos-input-key batch/`

### 18.2 Task Status Query (`mps_get_video_task.py` / `mps_get_image_task.py`)

1. Query video-processing task status. Task ID: `2600011633-WorkflowTask-abc123`.
   → `python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-abc123`
2. Query image-processing task status. Task ID: `2600011633-ImageTask-xyz789`.
   → `python scripts/mps_get_image_task.py --task-id 2600011633-ImageTask-xyz789`
3. I submitted this transcoding task with `--no-wait` — please poll for the final result.
   → `python scripts/mps_get_video_task.py --task-id <TaskId>`
4. Query the status of a try-on task (try-on tasks use the image-task query API).
   → `python scripts/mps_get_image_task.py --task-id 2600011633-ImageTask-tryon001`
5. Query the status of a background-fusion task (do NOT use the video-task query API).
   → `python scripts/mps_get_image_task.py --task-id 2600007696-WorkflowTask-abc123`
6. Get image-task details in JSON format.
   → `python scripts/mps_get_image_task.py --task-id 2600011633-ImageTask-img001 --json`
7. Query AI-narration task status.
   → `python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-narrate001`

### 18.3 Environment-Variable Check (`mps_load_env.py`)

1. Check whether the environment-variable configuration is correct.
   → `python scripts/mps_load_env.py --check-only`
2. I rotated to a new key set — verify the current configuration can call MPS normally.
   → `python scripts/mps_load_env.py --check-only`
3. Check whether the COS configuration is complete before running a task.
   → `python scripts/mps_load_env.py --check-only`
4. New machine deployment is done — check that the MPS environment variables are in effect.
   → `python scripts/mps_load_env.py --check-only`
5. Suspect SecretKey has expired — please confirm with the env-check script.
   → `python scripts/mps_load_env.py --check-only`
6. Verify that the MPS configuration is correct.
   → `python scripts/mps_load_env.py --check-only`

---

## 19. Effect Comparison (`mps_gen_compare.py`)

**Core capabilities**: generate an interactive HTML comparison page that supports left/right slider comparison for video and side-by-side comparison for images. **Does NOT call any MPS API and does NOT incur charges**. Supports both video and image comparison types.

**Typical scenarios**:

1. Compare the before/after enhancement effect of the video. Original: `<URL>`, enhanced: `<URL>`.
   → `python scripts/mps_gen_compare.py --original <original URL> --enhanced <enhanced URL>`
2. Generate a before/after comparison page for image super-resolution. Original: `<URL>`, processed: `<URL>`.
   → `python scripts/mps_gen_compare.py --original <original URL> --enhanced <processed URL> --type image`
3. I want to see the watermark-removal effect — make a before/after comparison.
   → `python scripts/mps_gen_compare.py --original <original URL> --enhanced <processed URL> --title "Watermark-removal comparison"`
4. Quality enhancement is done — generate an HTML before/after comparison page with slider support.
   → `python scripts/mps_gen_compare.py --original <original URL> --enhanced <enhanced URL>`
5. Image super-resolution is done — make a side-by-side comparison page of the original and the upscaled image.
   → `python scripts/mps_gen_compare.py --original <original URL> --enhanced <upscaled URL> --type image`
6. Before/after effect of subtitle removal — generate an HTML comparison file.
   → `python scripts/mps_gen_compare.py --original <original URL> --enhanced <subtitle-removed URL>`
7. Two enhancement templates were applied to the same video (real-person vs. anime) — generate a 3-way comparison page.
   → `python scripts/mps_gen_compare.py --original <original URL> --enhanced <real-person enhanced URL> --enhanced2 <anime enhanced URL>`

---

## Appendix: Routing Quick Reference & Usage Tips

1. **"Video vs. image" is the first split**: for "watermark removal", video goes through `mps_erase.py` while image goes through `mps_imageprocess.py`.
2. **"Quality boost to 1080P / 2K / 4K" is enhancement** (`mps_enhance.py`), **not transcoding**. Transcoding only changes codec / bitrate / container format.
3. **"Audio comparative analysis / audio content understanding" goes through `mps_av_understand.py`** — **do NOT mistakenly use `mps_qualitycontrol.py`** (the latter is physical-layer QC: clipping, silence, peaking, etc.).
4. **The Kling model supports multi-shot storyboards** (1–6 shots, sum of durations = total duration); other AIGC video models do not.
5. **AIGC image / video tasks must be queried by the `--task-id` of their respective scripts** (`mps_aigc_image.py --task-id` / `mps_aigc_video.py --task-id`); you **cannot** use `mps_get_video_task.py` or `mps_get_image_task.py` to query them.
6. **Scripts that require follow-up parameters**: audio separation must specify vocal/background/accompaniment; highlight reel and AI narration must specify a preset scene; A/V understanding must provide both `--mode` and `--prompt`; video re-creation must provide `--mode`.
7. **A cost notice must be given before invoking processing scripts**; query-type scripts (usage / get_task / cos_list) and upload/download scripts (cos_upload / cos_download) do not require a notice.
8. **Input-source decision**: use `--url` for URLs; use `--cos-input-key` only when the user explicitly says it's on COS; otherwise default to `--local-file` — do not ask the user whether the file is on COS.
9. **Try-on task status query** uses `mps_get_image_task.py` (NOT `mps_get_video_task.py`).
10. **Background-fusion task status query** also uses `mps_get_image_task.py`.
11. **Dry-run / no-wait scenarios**: dry-run only previews and does not execute; no-wait submits without polling for the result, but the task is created and can be queried later via `mps_get_video_task.py` / `mps_get_image_task.py`.
12. **Multi-step requests**: when the user asks for two or more things at once (e.g. transcoding + subtitle extraction, QC + enhancement), generate the corresponding multiple script commands separately.
13. **When the user explicitly specifies ffmpeg, do NOT trigger MPS** — return the ffmpeg command directly.
14. **When the user is only asking for a tool recommendation or product comparison and no actual processing is needed, do NOT trigger MPS**.

---

> **Maintenance note**: This document is distilled from the positive cases in `evals.json`. The capability classification corresponds one-to-one with the "Script Capability Mapping (Responsibility Boundaries)" table in SKILL.md. Any change to script capabilities (new scripts, splits/merges, parameter changes) must be synchronized into this document to keep the scenarios authentic and executable.
