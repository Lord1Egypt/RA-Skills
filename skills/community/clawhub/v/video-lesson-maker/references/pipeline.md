# 科普教学视频制作流水线（十步）

把一份 SRT 脚本 + 一张（或几张）手绘线稿，做成「白板手绘动画 + 云希配音 + 同步字幕」的成片。本流水线已在 10 部教学视频上完整跑通。

环境：先跑 `scripts/prepare_env.py` 建好隔离 venv（含 cv2 / numpy / av / Pillow / soundfile / edge-tts）。所有脚本都用该 venv 的解释器 `ENV_PY` 运行。系统需有 `ffmpeg`（或设 `FFMPEG_PATH`）。

约定目录（以某个视频 Vxx 为例）：
```
Vxx-主题/
  scripts/Vxx-主题.srt        # 口播脚本（第一步产出）
  scene-01-xxx-base.png       # ImageGen 生成的线稿（1536x1024）
  scene-01-xxx.png            # 去水印后
  scene-01-xxx-flat.png       # 匀纸后
  scene-01-xxx-crop.png       # 裁剪到 1536x864
  scene-01-xxx-enh.png        # 增强（PIL 画字/图元）后
  scene-01-xxx.annotation.json
  scene-01-xxx-whiteboard.mp4 # 单幕渲染
  Vxx-主题-无声.mp4           # 合并三幕后
  narration/                  # 配音工作目录
  Vxx-主题-配音版.mp4
  Vxx-主题-同步字幕.srt
  Vxx-主题-完整版.mp4         # 烧录字幕 = 最终交付
```

## 步骤

1. **主题凝练**：见 `theme-refinement.md`，产出规划表 + 每点 SRT。
2. **生成线稿**：用 ImageGen 对每个视频点生成手绘线稿（1536x1024，`line art` 风格，米色纸底）。**多幕务必分别生成、分别改名**，避免同名覆盖（见 `lessons-learned.md`）。
3. **去水印**：`remove_watermark.py` 清掉 ImageGen 右下角水印。
4. **匀纸**：`homogenize_paper.py` 抹平纸纹，避免渲染斑驳边界。
5. **裁剪**：把 1536x1024 裁到 **1536×864**（16:9，裁掉上下多余纸边，y 从 55 到 919）。
6. **增强**：基于 `enhance_toolkit.py` 写 `enhance_scenes.py`，用 PIL 在图上画**必须在揭示区内的**标题 / 标签牌 / 便签 / 印章（见模板 `enhance_scenes_template.py`）。增强图尺寸须与标注画布一致（1536×864）。
7. **写标注**：用 `make_annotation.py` + spec JSON 生成 `annotation.json`。**startMs 必须是幕内相对时间**（见 `annotation-schema.md` 与 `lessons-learned.md`）。
8. **渲染**：`render_stream_whiteboard.py` 把 `*-enh.png` + `*.annotation.json` 渲染成单幕白板动画 mp4（传入手部素材 `assets/drawing-hand-clean.png`）。
9. **合并**：`merge_scenes.py` 把多幕白板 mp4 硬切拼成 `无声.mp4`。
10. **配音 + 字幕 + 烧录**：
    - `prepare_narration.py` 先合成每段、测真实时长、算锚点 → 写 `narration_plan.json`；
    - `narrate_edge_tts.py` 混音出 `配音版.mp4`；
    - `make_subtitle_plan.py` 由 plan 生成 `subtitle_plan.json`；
    - `build_subtitles.py` 从真实音轨重建同步字幕 `.srt`；
    - ffmpeg 烧录字幕 → `完整版.mp4`。

## 关键命令模板（可直接复用）

```bash
ENV_PY=<venv>/Scripts/python.exe
SK=<skill>/scripts
HAND=<skill>/assets/drawing-hand-clean.png

# 渲染单幕
$ENV_PY $SK/render_stream_whiteboard.py scene-01-xxx-enh.png scene-01-xxx.annotation.json \
    scene-01-xxx-whiteboard.mp4 "$HAND" --ink-path grid --color-fill contour-wipe

# 合并
$ENV_PY $SK/merge_scenes.py --inputs s1.mp4 s2.mp4 s3.mp4 --output 无声.mp4

# 配音预演（先量真实时长）
$ENV_PY $SK/prepare_narration.py --srt ../scripts/Vxx.srt --work narration \
    --video 无声.mp4 --output 配音版.mp4 --total 130.7 --gap 0.4

# 混音
FFMPEG_PATH=ffmpeg $ENV_PY $SK/narrate_edge_tts.py --config narration/narration_plan.json

# 字幕计划 + 重建
$ENV_PY $SK/make_subtitle_plan.py --plan narration/narration_plan.json
FFMPEG_PATH=ffmpeg $ENV_PY $SK/build_subtitles.py --srt ../scripts/Vxx.srt \
    --track narration/narration-track.wav --plan narration/subtitle_plan.json \
    --work narration --out 同步字幕.srt --total 130.7

# 烧录
ffmpeg -y -i 配音版.mp4 -vf "subtitles=同步字幕.srt:force_style='FontName=Microsoft YaHei,FontSize=21,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,MarginV=28,Bold=1'" -c:v libx264 -crf 18 -preset medium -c:a copy 完整版.mp4
```

## 质检清单

- 音量峰值为负（约 −2.7 dB 为佳，避免破音）；用 `ffmpeg -i 完整版.mp4 -af volumedetect -f null -` 查 `max_volume`。
- 抽帧看关键时间点：标题、主体揭示、结尾凝视是否完整、字幕是否遮挡画布正文。
- 字幕自检通过（`build_subtitles.py` 末行 `自检 通过`，最长 ≤ 28 字）。
- 音画字三者时间轴一致（配音无重叠、字幕无越界、末条不超 `total`）。
