# 科普教学视频制作流水线（十三步）

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
6. **增强**：基于 `enhance_toolkit.py` 写 `enhance_scenes.py`，用 PIL 在图上画标题 / 标签牌 / 便签 / 印章（见模板 `enhance_scenes_template.py`）。增强图尺寸须与标注画布一致（1536×864）。文字走带自动收字的图元或 `safe_text`，别用裸 `d.text()` 写长句。
7. **版式体检（渲染前门禁，v1.4 加严）**：`check_layout.py --dir . --margin 32`。三类判据：**贴边**（墨迹距四边 <32px）、**入字幕带**（`y1 > 762`）、**永不被揭示**（墨迹在所有 region+maskPaddingPx 之外）。原图有底稿时自动走**底图对比**，只量 PIL 新增的墨迹。必须 0 问题；有问题用 `--fix` 撑 region 或改绘制坐标。见下节。
8. **写标注**：优先 `make_spec.py` 从 `layout-0N.json` 生成 spec（绘制与揭示共用同一份坐标）；否则手写 spec 再用 `make_annotation.py` 生成 `annotation.json`。**startMs 必须是幕内相对时间**（见 `annotation-schema.md` 与 `lessons-learned.md`）。
9. **渲染**：`render_stream_whiteboard.py` 把 `*-enh.png` + `*.annotation.json` 渲染成单幕白板动画 mp4（传入手部素材 `assets/drawing-hand-clean.png`）。
10. **合并**：`merge_scenes.py` 把多幕白板 mp4 硬切拼成 `无声.mp4`。
11. **配音 + 字幕 + 烧录**：
    - `prepare_narration.py` 先合成每段、测真实时长、算锚点 → 写 `narration_plan.json`；
    - `narrate_edge_tts.py` 混音出 `配音版.mp4`；
    - `make_subtitle_plan.py` 由 plan 生成 `subtitle_plan.json`；
    - `build_subtitles.py` 从真实音轨重建同步字幕 `.srt`；
    - `srt_to_ass.py` 把 srt 转成**显式 PlayRes = 画面尺寸**的 `.ass`（必做，见下）；
    - ffmpeg 用 `ass=` 滤镜烧录 → `完整版.mp4`（**必须 cd 进目录用相对文件名**，见下）。
12. **成片复核（v1.4 新增，渲染后门禁）**：`check_render.py --dir .`。把增强图与成片末帧逐像素比对，算**内容覆盖率**、列出「源图有、成片没有」的墨迹块，并量成片四边实际留白。`check_layout` 查的是源图与 region，这一关查的是**解码后的真实像素**——字幕遮挡、libass 静默失败、合流丢帧只有它能抓。覆盖率 <0.99 判失败。见下节。

### 字幕烧录：为什么必须走 ASS（PlayRes 缩放坑）

ffmpeg 的 `subtitles=` 滤镜对 **SRT 输入**使用 libass 默认脚本分辨率 `PlayResX=384 / PlayResY=288`，
于是 `force_style` 里的 FontSize 会按 `frame_height / 288` 放大：

- 本项目出图 **1080×600**：缩放 ≈ 2.08×，`FontSize=32` 实际渲染成 **~73px**；
- 一条 28 字中文 ≈ 1850px，直接撑爆 1080 宽画面，左右被裁 —— 即"字体太大、超出视频界面"。

**解法**：`srt_to_ass.py` 显式写入 `PlayResX/PlayResY = 1080/600`，使 FontSize 恒等于**画面像素**，
再用 `ass=` 滤镜烧录。经验字号 **26**（28 字 ≈ 728px，左右各留 40px 边距仍余量充足）。
脚本内置宽度自检：估算宽 > 可用宽会打印 `!! 超宽`。

> ⚠️ **`ass=` 吃不了中文绝对路径**。Windows 上会报
> `Could not create a libass track when reading file '/e/…/narration/subs.ass'`，
> 哪怕文件确实存在、路径也确实对。必须先 `cd` 到该目录、只传相对文件名：
> ```bash
> cd "$d" && ffmpeg -y -i "配音版.mp4" -vf "ass=narration/subs.ass" ... "完整版.mp4"
> ```
> 不要试图用 `subtitles=` 或加引号转义绕过——libass 只认相对路径。

### 版式体检：为什么必须在渲染前跑（region 漂移坑）

渲染器按 region 揭示墨迹，**可见范围 = region 矩形 减去 后续 region**。由此有两个陷阱：

1. 图元画到 `x<24` / `x>W-24` / `y<24` / `y>H-24` → 缩到 1080×600 后贴边、字被画面边缘切掉。
2. 文字压在 region 边界上 → 超出部分**永远不被揭示**。源图 PNG 完整，光看 PNG 完全查不出，
   只有渲染完抽帧才会发现「那块字没了」。若 region 整体偏移（比如便签上移避字幕、spec 没跟着改），
   那块内容会**整块消失**。

`check_layout.py` 用「region 并集 vs 墨迹」直接回答「哪些内容永远不会显示」：

```bash
$ENV_PY $SK/check_layout.py --dir ./V07-主题 --margin 32         # 0 问题才继续
$ENV_PY $SK/check_layout.py --dir ./V07-主题 --fix ./specs-fixed/
$ENV_PY $SK/check_layout.py --image a-enh.png --spec spec.json --json r.json   # 单幕 + 机器可读
```

三个必知参数：

- `--margin 32`：画布侧安全边距。1536→1080 缩放比 0.703，32 画布 px ≈ 22.5 成片 px。
- `--subtop 762`：字幕带上沿。1080×600 + MarginV=36 + FontSize=26 → 字幕实占 y≈529–567，
  折算回画布即 y ≥ 762；所以任何图元 `y1` 必须 ≤ 756。
- `--base auto`：见下节。

输出示例（真实案例）：
```
[BAD] 18 处墨迹落在所有 region 之外 → 成片里永远不显示
      bbox=(1207,693,1240,717) 面积503
      bbox=(136,603,1399,626) 面积8121 → 应在 region#5（溢出 上 22px）
[ok ] 另有 5 处装饰线级溢出（≤6px，缩放后不足 4px，可忽略）
```

### 底图对比模式：`--base`（PIL 叠字场景必用）

若增强图是「ImageGen 线稿 + PIL 叠字」，整图墨迹边界量到的是**线稿本身**（线稿天然画到纸边），
会把上百条线报成"文字贴边"，报告直接失去可用性。

正确做法是把 `<stem>-base.png`（未叠字的裁剪图）一起给它，只量新增像素：

```python
diff  = |enh - base|.max(axis=2)
added = (diff > 30) & ink_mask(enh, 55)     # 只看"新画上去的"，且必须是墨
```

`--base auto` 默认行为：同目录找 `<stem>-base.png`，命中则打印 `[mode] 底图对比：…`；
未命中退化为整图模式。**`-base.png` 属于必留中间产物，别删**，删了体检就退回误报状态。

### `maskPaddingPx`：别把"其实显示了的"报成"永不显示"

渲染器揭示 region 时会把矩形**向外扩 `maskPaddingPx`**（老标注默认 22px）。
体检若只按纯 region 矩形判断，会把落在 padding 里的墨迹误报成"永不显示"（V07 曾一次误报 6 块）。
`check_layout.py` 已解析 `reveal.maskPaddingPx` 并外扩后再做归属判断，写标注时不要手改这个字段。

根治办法是**不让坐标有第二份**：`enhance_scenes.py` 里

```python
from enhance_toolkit import LAYOUT
LAYOUT.begin(im)                 # 每幕开头
...draw_title / draw_label_card / draw_note（自动登记 bbox）...
LAYOUT.save(f"layout-{idx}.json")
```

再 `make_spec.py --layout layout-01.json --out spec-01.json` 出 spec，region 顺序 = 绘制顺序。

### 成片复核：`check_render.py`（v1.4 新增，唯一能抓"成片真丢内容"的关）

`check_layout.py` 判的是**源图与 region 的关系**，它无法回答「烧完字之后，那块内容还在不在」。
渲染丢层、libass 静默失败、合流丢帧、字幕带压住底部便签——这些都只在**解码后的像素**里可见。

```bash
$ENV_PY $SK/check_render.py --dir ./V07-主题 --margin 12 --min-coverage 0.99
$ENV_PY $SK/check_render.py --dir ./V07-主题 --json render-report.json     # 机器可读
```

做法：解成片**最后一帧**（画面已完全揭示、字幕已烧上的状态）→ 与 `*-enh.png` 同尺寸对齐 →
算墨迹交集比例 = **内容覆盖率**；低于阈值时按连通块列出缺失区域，并给出最近的 region 与方向。
同时输出成片四边实际留白像素，便于直接判断"是否贴边"。

判据：覆盖率 ≥ 0.99 通过，exit 0；否则 exit 1。字幕带内的正常遮挡已从分母扣除，不会误判。
失败首先怀疑三件事：① 该幕 `annotation.json` 的 region 少于实际图元；② 烧录时 `ass=` 报错但被忽略；
③ `merge_scenes.py` 输入的幕数少了。

## 关键命令模板（可直接复用）

```bash
ENV_PY=<venv>/Scripts/python.exe
SK=<skill>/scripts
HAND=<skill>/assets/drawing-hand-clean.png

# 渲染单幕
$ENV_PY $SK/render_stream_whiteboard.py scene-01-xxx-enh.png scene-01-xxx.annotation.json \
    scene-01-xxx-whiteboard.mp4 "$HAND"
# v3 起默认 --ink-path skeleton --color-fill brush（随笔画出来的观感）；
# 勿回退 grid/contour-wipe（块状填充+幕帘扫描=「擦写感」，见 lessons-learned #16）。

# 合并
$ENV_PY $SK/merge_scenes.py --inputs s1.mp4 s2.mp4 s3.mp4 --output 无声.mp4

# 配音预演（先量真实时长）
$ENV_PY $SK/prepare_narration.py --srt ../scripts/Vxx.srt --work narration \
    --video 无声.mp4 --output 配音版.mp4 --total 130.7 --gap 0.4

# 混音
FFMPEG_PATH=ffmpeg $ENV_PY $SK/narrate_edge_tts.py --config narration/narration_plan.json

# ⚠️ 只要动过 SRT / 拆过幕 / 改过 plan，必须重建音轨（复用已有 segNN.wav，秒级）：
#    否则画面与字幕按新 plan、声音按旧轨，各走一只钟（lessons-learned #18）
$ENV_PY $SK/rebuild_track.py --plan narration/narration_plan.json \
    --work narration --out narration/narration-track.wav
# 输出核对：成片无声时长 ≈ speech_end + 结尾凝视(1.0~1.5s)

# 字幕计划 + 重建（narration_plan.json 是字典，务必先生成 subtitle_plan.json 列表）
$ENV_PY $SK/make_subtitle_plan.py --plan narration/narration_plan.json
FFMPEG_PATH=ffmpeg $ENV_PY $SK/build_subtitles.py --srt ../scripts/Vxx.srt \
    --track narration/narration-track.wav --plan narration/subtitle_plan.json \
    --work narration --out 同步字幕.srt --total 130.7

# 字幕转 ASS（显式 PlayRes，根治缩放溢出）
$ENV_PY $SK/srt_to_ass.py --srt 同步字幕.srt --out narration/subs.ass \
    --width 1080 --height 600 --font-size 26

# 混流：-af apad 把音频补齐到画面长度，避免音轨略短时把尾部凝视切掉
ffmpeg -y -i 无声.mp4 -i narration/narration-track.wav -af apad \
    -c:v copy -c:a aac -b:a 192k -shortest 配音版.mp4

# 烧录（用 ass 滤镜，不要用 subtitles 滤镜！）
ffmpeg -y -i 配音版.mp4 -vf "ass='narration/subs.ass'" \
    -c:v libx264 -crf 21 -preset medium -pix_fmt yuv420p -c:a copy 完整版.mp4
```

> ⚠️ 画面尺寸不同时，`--width/--height` 必须跟着改；FontSize 经验值按 `max_chars*FontSize + 2*40 <= width` 自检。

## 质检清单

- 音量峰值为负（约 −2.7 dB 为佳，避免破音）；用 `ffmpeg -i 完整版.mp4 -af volumedetect -f null -` 查 `max_volume`。
- 抽帧看关键时间点：标题、主体揭示、结尾凝视是否完整、字幕是否遮挡画布正文。
- **渲染前 `check_layout.py --dir --margin 32` 必须 0 问题**：否则成片里会有整块文字不出现，事后只能重渲。
- **渲染后 `check_render.py --dir` 覆盖率必须 ≥ 0.99**：这是"内容完整性"的终局判据，前面几关都替代不了。
- 绘制日志里不应出现 `[text-overflow!]`（最小字号仍超宽 → 必须缩短文案）、`[edge!]`（图元贴边）、`[bounds!]`（出画布）。
  出现 `[clamp]` 说明坐标写错但被兜底救回，**必须回改坐标**，不要依赖兜底。
- 字幕自检通过（`build_subtitles.py` 末行 `自检 通过`，最长 ≤ 28 字）。
- **字幕不溢画面**：抽帧量字幕带暗像素 bbox，需满足 `0 < x_min`、`x_max < width-1`、字幕底边距底 ≥ 30px。
  对照无声版可区分"字幕触边"与"持笔手素材自然延伸到底边"。
- **手绘内容不触边**：`check_render.py` 会直接报成片四边留白，四边均应有 > 0 的余量（建议 ≥ 20px）。
- 音画字三者时间轴一致（配音无重叠、字幕无越界、末条不超 `total`）。
