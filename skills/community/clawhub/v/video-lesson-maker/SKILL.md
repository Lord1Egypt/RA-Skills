---
name: video-lesson-maker
description: >-
  基于一篇文档（教材/课件/科普文章）凝练教学视频主题，并用白板手绘动画 + 云希配音
  + 同步字幕，批量制作科普/教学视频。当用户需要从文档拆出视频点、写口播脚本、生成
  手绘线稿、做白板动画渲染、用 edge-tts 配音、重建同步字幕并烧录成片时使用。触发词：
  教学视频、科普视频、视频主题凝练、白板动画、配音字幕、课程视频制作、把文档做成视频。
version: 1.4.1
author: lengzheng2026
tags: [video, education, whiteboard-animation, tts, subtitle, courseware]
---

# 视频主题凝练及制作 skill

把「一篇文档 → 多部科普/教学成片」的全流程固化下来。已在本机 10 部化妆品法规教学视频上完整跑通。

## 能力范围

1. **主题凝练**：从文档拆出可独立成片的知识点（默认按教材「任务/章节」挂接，见 `references/theme-refinement.md`）。
2. **视频制作**：手绘线稿 → 去水印/匀纸/裁剪 → PIL 增强 → 白板动画渲染 → 多幕合并（自包含脚本在 `scripts/`，手部素材在 `assets/`）。
3. **配音**：edge-tts（云希）逐段合成、**先测真实时长再算锚点**，避免段间重叠（关键：见 `references/lessons-learned.md`）。
4. **字幕**：从真实音轨重建「意群完整 + 不超框」的同步字幕并烧录。

## 何时用

- 「帮我把这份教材做成一系列教学视频」
- 「给这个知识点做个 2 分钟科普视频」
- 「我有脚本了，帮我出白板动画 + 配音 + 字幕」
- 「视频主题怎么拆 / 字幕怎么和配音对齐」

## 工作流（十三步，详见 `references/pipeline.md`）

1. 主题凝练 → 规划表 + 每点 SRT（`theme-refinement.md`）
2. ImageGen 生成手绘线稿（1536×1024，分别生成避免同名覆盖）
3. `remove_watermark.py` 去水印
4. `fit_canvas.py` 尺寸守卫（ImageGen 可能返回 1024x1024 方图，crop 越界会填纯黑，必须先 pad 到 1536 宽）
5. `homogenize_paper.py` 匀纸
6. 裁剪到 1536×864
7. 增强：复制 `references/enhance_scenes_template.py`，按布局画标题/标签/便签（标题带先做「清字/底板」处理，见下节）。**文字一律走 `safe_text` / `draw_label_card` / `draw_note`，它们会按框宽自动缩字号**，不要用裸 `d.text()` 写长句。
8. **版式体检（渲染前必跑，v1.4 加严）**：`check_layout.py --dir <片子目录> --margin 32`。它拿「所有 region（含 maskPaddingPx 外扩）的并集」去比对墨迹，报出三类问题：**贴边**（墨迹距四边 <margin）、**入字幕带**（`y1 > 762`）、**永不被揭示**（墨迹落在所有 region 之外）。原图有底稿时必须走**底图对比模式**（自动找 `-base.png`），否则整张线稿都会被当成"新增文字"误报。必须 0 问题才进入渲染，可直接挂门禁：
   ```bash
   $VENV $SK/check_layout.py --dir "$d" --margin 32 || { echo "版式不合格，不要渲染"; exit 1; }
   ```
9. 标注：`make_annotation.py` + spec 生成 `annotation.json`（startMs 幕内相对！）。spec 优先用 `make_spec.py` 从 `layout-0N.json` 生成，避免手写坐标漂移。
10. 渲染：`render_stream_whiteboard.py`（默认即骨架随笔画法；传 `assets/drawing-hand-clean.png`）
11. 合并：`merge_scenes.py` → 无声.mp4
12. 配音+字幕+烧录：`prepare_narration.py` → `narrate_edge_tts.py` → `make_subtitle_plan.py` → `build_subtitles.py` → **`srt_to_ass.py`（显式 PlayRes，必做！）** → ffmpeg `ass=` 烧录 → 完整版.mp4
13. **成片复核（渲染后必跑，v1.4 新增）**：`check_render.py --dir <片子目录>`。它把「增强图 PNG」与「成片最后一帧」逐像素比对，算**内容覆盖率**并列出「源图里有、成片里没有」的墨迹块（带最接近的 region）——这是唯一能抓到"字幕带遮挡 / region 漂移 / 渲染丢层"的终局检查。同时报成片四边实际墨迹距离。覆盖率 < 0.99 即失败：
    ```bash
    $VENV $SK/check_render.py --dir "$d" --margin 12 --min-coverage 0.99 || echo "成片内容缺失"
    ```

## 环境准备（首次必跑）

```bash
ENV_PY=$(python <skill>/scripts/prepare_env.py)   # 建隔离 venv，末行输出 ENV_PY 路径
# 系统需有 ffmpeg（或运行前 export FFMPEG_PATH=...）
```

所有脚本都用该 `ENV_PY` 运行；`prepare_env.py` 已包含 cv2 / numpy / av / Pillow / soundfile / edge-tts。

## 关键铁律（新做视频前必读 `references/lessons-learned.md`）

- **字幕烧录必须走 `srt_to_ass.py` 转 ASS，禁用 ffmpeg `subtitles=` 滤镜**。`subtitles` 对 SRT 用 libass 默认 `PlayResY=288`，1080×600 画面上 `FontSize=32` 会被放大 ~2.08× 成 73px，字幕直接撑爆画面左右边缘（项目2 三片全部中招）。转 ASS 时显式写 `PlayResX/PlayResY = 画面宽高`，FontSize 即为画面像素，经验值 **26**。
- **`ass=` 滤镜遇到中文绝对路径会直接失败**：Windows 下报 `Could not create a libass track when reading file '/e/…/_subs.ass'`，即使路径存在。解法是 `cd` 进片子目录、用相对文件名：
  ```bash
  cd "$d" && ffmpeg -i "$src" -vf "ass=_subs.ass" -c:v libx264 -crf 18 -c:a copy "$out"
  ```
  别用 `subtitles=` 绕，也别给路径加引号转义——libass 只吃得了相对路径。
- **annotation.startMs 是幕内相对时间，不是成片绝对时间**（V05 大坑，写成绝对时间会虚高几十秒）。
- **配音时长用实测**，别手写估算；实测超画面就延长各幕 `sceneDurationMs` 重渲（V09 教训）。
- **字幕单行 ≤ 28 字**，且烧录样式放画面下方不压正文。
- **ImageGen 多图必须逐张串行生成**：并行调用时各 output_dir 会折叠——全部结果落进同一个目录，且秒级时间戳可能重复互覆盖（V11–V15 教训，详见 lessons-learned #22）。多幕分别生成、分别改名。
- **改 SRT 后重跑 TTS，必须先清空 narration/ 下 `seg*.mp3`/`seg*.wav`/`narration_plan.json`**：`prepare_narration.py` 的 synth 有缓存（mp3 存在即跳过合成），直接重跑会用旧文本音频、plan 时间戳全错；且 edge-tts 偶发短版音频会被缓存固化，重跑后量 1–2 段 wav 时长对照文本（约 5.2 字/秒）（lessons-learned #23）。
- **文字贴边/被遮罩裁掉 = 本 skill 的头号返工来源，必须靠 `check_layout.py` 在渲染前拦下**。白板渲染按 region 揭示墨迹（region 减去后续 region），所以：①任何图元画到 `x<24` / `x>W-24` / `y>H-24` 就会贴边；②文字压在 region 边界上，超出的部分**永远不被揭示**，但源图 PNG 是完整的，光看图查不出来。项目3 曾因「便签上移避字幕、spec 里的 y 没跟着改」在 13 幕里丢掉整块文字（成片里那块字根本不存在）。
- **region 坐标不要手写**：让 `enhance_scenes.py` 在每幕开头 `LAYOUT.begin(im)`、结尾 `LAYOUT.save("layout-0N.json")`，再用 `make_spec.py` 生成 spec。绘制与揭示用同一份坐标，从机制上不可能漂移。
- **定死字号 + 定死框宽 = 必然溢出**：`draw_label_card` / `draw_note` / `draw_title` / `safe_text` 已内置按框宽反算字号的 `fit_font`，会打印 `[fit] 字号 34→29`；自己写裸 `d.text()` 就绕过了这层保护，长句会直接冲出框外甚至画布外。
- **图元坐标不得超出画布边界**：`enhance_toolkit._check_bounds` 会打印 `[bounds!]`（出画布）与 `[edge!]`（贴边，距边 <8px）；`clamp_box`/`clamp_center` 会打印 `[clamp]` 告诉你哪个图元被推回安全区——**看到 `[clamp]` 就说明上游坐标写错了，别当它没事**，回去改坐标而不是依赖兜底。成片后仍要用 `check_render.py` 量一次四边实际距离。
- **底部图元不得画进字幕区**：1080×600 + MarginV=36 + FontSize=26 时，字幕块约占画面 y 529–567，折算回 1536×864 画布即 **y ≥ 762 是字幕区**；所有图元（尤其结论便签）的 `y1` 必须 ≤ 756（项目3 十二片质检发现，详见 lessons-learned #11）。
- **动过 SRT/分段/拆幕，合成前必须 `rebuild_track.py` 重建音轨**，混流加 `-af apad`；否则画面字幕按新 plan、声音按旧轨（lessons-learned #18）。合成后校验 `成片时长 ≈ 语音结束 + 凝视`。
- **卡片/便签填充用 `_page_rgb(im)` 全不透明**，同带并列图元的 x 区间不得相交（lessons-learned #19）。

## 动画观感：必须是「随笔画出来」（v3 核心，勿回退）

早期版本 `--ink-path grid --color-fill contour-wipe`（网格逐块填充 + 自上而下幕帘扫描）
被用户评价为「**擦写出来的，不是画出来的**」，且文字与绘画重叠。已根治并固化为默认值：

1. **渲染默认 `--ink-path skeleton --color-fill brush`**：骨架追踪出真实笔画，笔尖沿笔画
   滑行逐段落墨，添彩沿同一路径刷 → 观感即随笔画出来；凝视帧 0.4s 交叉淡入，杜绝硬切蹦变。
   除非用户点名，**不要**再传 grid/contour-wipe。
2. **标题带三选一**（先出 `crop y0-210` 对照图逐场景决策）：
   - 顶部带空白 → 直接 `draw_title`；
   - 顶部有自带字样（SCORECARD / Hands-on Operations / 金项目三角…）→
     `clear_area(im, box)` 软边清除后写（清除框要盖住全部笔画含下延部，y 从 0 起）；
   - 顶部有不可清的插画/深色底纹 → `draw_title(..., panel=True)` 纸板底板。
3. **文字底必须实心且取本图纸色**：`draw_note` / `draw_label_card` / `draw_title(panel=True)`
   的填充一律用 `_page_rgb(im)`（四角采样中位数）**全不透明**。半透明底会让线稿透过便签
   压住文字（「绘画与文字重叠看不见文字」）；而固定色 `PAPER_LIGHT` 与匀纸后的页面有色差，
   卡片会变成一块明显偏白的补丁（同样被用户指出）。
4. **增强内容对齐标注带、不得跨带**：标题 y40-170、主体 y180-600、结论便签 y600-742；
   一排标签卡整体放进一个带（跨带会被拆成两段揭示，笔「跳来跳去再回头」）。
5. **同带并列元素必须留缝**：便签与一排卡片同处 y600-742 时，x 区间**不得相交**
   （实测 V03-s3 便签 116-616 与「人」卡 520-688 重叠 96px，直接把「讲得清」压掉；
   V02-s5 便签 120-1416 横穿剪贴板插画）。写字前先算好这一带所有盒子的 x 边界。
6. 细节见 `references/lessons-learned.md` #16、#19。

## 题材专业相关性（STEM / 职教竞赛视频必看）

面向世界职业院校技能大赛等理工农医类竞赛时，**手绘线稿与口播案例必须与参赛专业强相关**，不要用医院/工厂/公文等泛化意象。优先从以下专业取材，按视频主题轮换：

- **生物**：无菌操作、PCR、发酵工程、生物反应器、菌种筛选、酶工程。
- **化工**：反应釜、精馏/吸收塔、催化燃烧、HPLC/气相色谱、危化品管理、GMP 规范。
- **环境**：污水处理厂（脱氮除磷、COD/氨氮监测）、VOCs 治理、在线监测、固废资源化。
- **材料**：复合材料、涂层附着力、拉伸/冲击试验、材料表征（SEM/XRD）、良品率提升。
- **轻工**：食品检测与感官评定、包装设计、质检漏检、工艺优化。

落实三处：① ImageGen 线稿 prompt 直接描述上述专业场景/仪器；② `enhance_scenes.py` 的 `draw_note` 结论条写具体专业案例；③ 口播 SRT 用专业痛点举例（如"某污水厂氨氮超标""药厂杂菌污染"），而非空泛口号。

## 音画同步（v3 核心，勿回退）

**问题**：早期视频的「配音时间轴」与「各幕绘画时间轴」是两套独立时钟，导致**讲 A 主题时画面仍是 B 主题**、且结尾约 30s 静默空画；节拍太粗（一拍覆盖五六句口播）又导致「讲到哪画不到哪」。

**解法（三层，全部固化在脚本里）**：

1. **逐句节拍（scenes.json v2 `beats` 格式）**——「讲到哪、画到哪」：
   ```json
   [
     {"lines": [1, 5], "beats": [
       {"lines": [1],    "rects": [[430, 40, 680, 135]]},
       {"lines": [2],    "rects": [[480, 180, 520, 420]]},
       {"lines": [3, 4], "rects": [[120, 610, 400, 132], [540, 610, 456, 132]]},
       {"lines": [5],    "point": [[440, 580], [760, 180], [440, 580]]}
     ]}
   ]
   ```
   - `lines` = 本节拍对应的口播段号（`Vxx.srt` 序号）；`rects` = 依次画哪些画面块
     （画布坐标 `[x,y,w,h]`，可带 `"dur"` 毫秒指定单块时长，未指定均分剩余）；
     `point` = 只移动笔尖不落墨的指点拍（总结/过渡句）。
   - **拍序 = 口播顺序**（顺序逻辑性第一来源）；块间动线按「从上到下、从左到右、
     相邻优先」规划（局部协调+整体阅读动线）。**一句最多配 2-3 个空间块**。
   - 内容多的幕**果断拆幕**（V02 29 句拆 5 幕，新幕用 ImageGen 补画对应意象线稿），
     不要硬塞。
2. **真实语音计时**：`build_sync_spec.py --narration-dir narration` 实测每个
   `segNN.wav` 真实语音长度（不再用 plan 的假间隔）。每拍窗口 =
   `[本拍首句起始, min(末句语音结束+tail, 下一拍首句起始-0.05)]`；幕时长 =
   下一幕首句起始（零漂移）；全片 = 最后一句语音结束 + 结尾凝视。
3. **笔顺 = 行带 + 带内严格左→右**（`stream_render._chain_strokes_logically`，v3）：
   笔画先按竖直重叠分成「行带」，带与带从上到下，**带内按 x 从小到大**逐笔接续。
   观感即真人板书：先画框线 → 从左到右写字 → 补右边框/折角。
   ⚠️ 别回退到两种旧做法：①「包围盒字典序」→ 同行部件被按 x 打散、笔乱跳；
   ②「最近邻接龙」→ 便签折角在右上，接龙就滑到文字右端、把"零失误·肌肉记忆"
   倒着写成"记忆…零失误"（本轮实测翻车）。
4. **四者同钟（画面/语音/字幕/plan）**：音轨是 `narrate_edge_tts.py` 一次生成后就
   固化在磁盘上的。**只要动过 SRT / 分段 / 拆幕，合成前必须重建音轨**，否则画面与
   字幕按新 plan、声音按旧轨，各走一只钟（实测 V03 末段 `seg29` 在旧轨里完全没声音，
   画面却为它画了 3 秒）：
   ```bash
   $VENV $SK/rebuild_track.py --plan $d/narration/narration_plan.json \
       --work $d/narration --out $d/narration/narration-track.wav
   # 输出 speech_end 必须满足：无声时长 ≈ speech_end + 结尾凝视(1.0~1.5s)
   ```
   混流再多加 `-af apad`（音频补齐到画面长度），避免音轨略短时把画面尾部凝视切掉。

```bash
# 生成同步标注 spec（须放在 prepare_narration 之后）
$VENV $SK/build_sync_spec.py --srt Vxx.srt --plan narration/narration_plan.json \
    --narration-dir narration --scenes scenes.json --out-dir . --gaze 1000 --tail 250
$VENV $SK/make_annotation.py --spec spec-01-1.json --out scene-01-1.annotation.json
# … 每幕各跑一次；make_annotation 自检「末元素结束 < sceneDuration」必须全过
```

> ⚠️ `lead` 与 `make_annotation` 全局 cursor 是**相加关系**：拍间空隙才用 lead
> （放在本拍第一块），拍内多块必须 `lead=0`，否则双重累加、末元素溢出 sceneDuration。

## 版式安全：文字不出框、不贴边（v1.3 起，v1.4 加严）

用户反馈「视频里文字处在边缘、显示不全」。根因有两层，都已从机制上堵住：

**① 绘制层：长句没有容身之处。** 定死字号 + 定死框宽，句子一长就冲出框外、甚至画到画布外。
现在 `enhance_toolkit` 提供自动收字能力，全部内置、无需额外调用：

| 用法 | 行为 |
|---|---|
| `draw_label_card(d, box, 文本, f_yahei(34))` | 按卡片内宽自动缩字号，最窄缩到 13px；打印 `[fit]` |
| `draw_note(d, im, box, 文本, f_kai(42))` | 同上；胶带/折角改为**画在框内**，不再越过上边界 12px |
| `draw_title(d, 文本, cx, y, 56, INK)` | 限宽 = 画布宽 − 2×24px，超宽自动缩；`y` 会被抬到 ≥36；**下沿要算到波浪线为止**（`y+size+12`），副标题从它下面 10px 起排 |
| `safe_text(d, None, "长句", f_kai(30), box=(x0,y0,x1,y1))` | 裸文字的安全版：先按框缩字号，再查边界 |

裸 `d.text((x,y), ...)` 仍然可用，但它不做任何保护——写长句时请改用 `safe_text`。

**② 揭示层：region 与绘制坐标漂移。** 渲染器只揭示「region 内、且不在后续 region 内」的墨迹，
所以坐标一漂，那块内容就**整块不出现**。两个新脚本配套使用：

```bash
# A. 渲染前体检（秒级，比渲染快两个数量级；必须 0 问题）
$VENV $SK/check_layout.py --dir ./V07-xxx
#   ✓ 通过 / [BAD] N 处墨迹落在所有 region 之外 → 成片里永远不显示
#   每行给出 bbox、面积、最接近的 region 与溢出方向（左/右/上/下 xx px）
#   「装饰线级溢出（≤6px）」会被单独归为可忽略，不计入失败

# B. 已写死 spec、只想补 region：自动外扩且不侵入相邻 region
$VENV $SK/check_layout.py --dir ./V07-xxx --fix ./specs-fixed/

# C. 从绘制结果直接生成 spec（推荐做法，坐标永不漂移）
#     enhance_scenes.py 内：LAYOUT.begin(im) …绘制… LAYOUT.save("layout-01.json")
$VENV $SK/make_spec.py --layout layout-01.json --out spec-01.json \
    --dur 4000 --title-dur 3000 --gaze 1200
```

`check_layout.py` 退出码 0/1，可直接挂到批量构建脚本里当门禁：

```bash
$VENV $SK/check_layout.py --dir "$d" --margin 32 || { echo "版式不合格，停在这里，不要渲染"; exit 1; }
```

### v1.4 安全区常量（写死在 `enhance_toolkit.py`，改一处全流程生效）

画布 1536×864，成片 1080×600，缩放比 **0.703**。所以画布 34px ≈ 成片 24px。

| 常量 | 值 | 含义 |
|---|---|---|
| `SAFE_MARGIN` | 34 | 左/右/下 最小墨迹距离（成片 ≈24px） |
| `SAFE_TOP` | 36 | 上 最小距离（标题带下压，避免顶天） |
| `SUB_BAND_TOP` | 756 | 字幕带上沿；所有图元 `y1 ≤ 756` |
| `EDGE_MARGIN` | 8 | 只打印 `[edge!]` 警告的软阈值 |

配套的 `clamp_box` / `clamp_center` / `draw_text_center` 已接进 `draw_title`、`draw_label_card`、`draw_note`、`safe_text`、`draw_stamp`、`draw_star`——**只平移不缩放**（除非图元本身比安全区还大）。所以哪怕上游坐标写飞了，落笔也会被推回安全区。

> ⚠️ **钳制必须按真实墨迹矩形，不能按文字原点**。PIL `textbbox((0,0),...)` 是相对原点的，字体 ascender 留白会让真实墨迹比原点低 10–18px。项目1 曾出现"日志记录钳到 756、实测却是 772"的 16px 偏差，根因就是钳了原点。`draw_text_center` 内部钳 `(ox+bb[0], oy+bb[1], ox+bb[2], oy+bb[3])`，`safe_text` 同理。

### 底图对比模式（`--base`，PIL 叠加文字时必用）

当增强图是在 ImageGen 线稿上叠加 PIL 文字（不是纯白纸重画）时，**整图墨迹边界量到的是线稿本身**，会把每一条画到边上的线都报成"文字贴边"。正确做法是只比对「新增像素」：

```python
diff = |enh - base|.max(axis=2);  added = (diff > 30) & ink_mask(enh, 55)
```

`check_layout.py` 默认 `--base auto`：同目录找 `<stem>-base.png`，找到就只量新增墨迹；没找到则退化为整图模式并打印 `[mode]`。**保留 `-base.png` 是硬要求**，删了它体检就失去意义。

### 三档检查的分工（v1.4）

| 脚本 | 时机 | 抓什么 | 失败判据 |
|---|---|---|---|
| `check_layout.py` | 渲染前 | 贴边 / 入字幕带 / 永不被揭示（region 漂移） | 任一 blob 越界，exit 1 |
| `make_annotation.py` 自检 | 标注后 | 末元素结束 > sceneDuration | 打印超时项，exit 1 |
| `check_render.py` | 渲染+烧字后 | **成片里内容是否真的全在**（覆盖率） | 覆盖率 < 0.99，exit 1 |

三者不可互相替代：`check_layout` 看的是源图与 region 的关系，`check_render` 看的是**解码后的成片像素**——字幕遮挡、libass 出错、合流丢帧只有它能发现。

## 目录结构

```
video-lesson-maker/
├── SKILL.md
├── manifest.json
├── scripts/        # 渲染/合并/配音/字幕 + 三个自研辅助脚本
│   ├── render_stream_whiteboard.py
│   ├── stream_render.py
│   ├── merge_scenes.py
│   ├── narrate_edge_tts.py
│   ├── build_subtitles.py
│   ├── enhance_toolkit.py
│   ├── homogenize_paper.py
│   ├── remove_watermark.py
│   ├── parse_srt.py
│   ├── prepare_env.py
│   ├── prepare_narration.py   # 自研：合成+测时长+算锚点
│   ├── make_subtitle_plan.py  # 自研：由 plan 生成字幕计划
│   ├── srt_to_ass.py          # 自研：SRT→ASS（显式 PlayRes，根治字幕缩放溢出）
│   ├── check_layout.py        # 自研：版式体检——贴边/字幕带/region 漂移，渲染前门禁（支持底图对比）
│   ├── check_render.py        # 自研：成片复核——增强图 vs 成片末帧，算内容覆盖率、抓丢失墨迹
│   ├── make_spec.py           # 自研：layout.json → spec（绘制与揭示共用一份坐标）
│   ├── make_annotation.py     # 自研：spec→annotation.json
│   ├── build_sync_spec.py     # 自研：音画同步——由 narration_plan+scenes 生成每幕 spec
│   ├── rebuild_track.py       # 自研：按 plan 重排 segNN.wav 重建音轨（四者同钟，不重调 TTS）
│   ├── fit_canvas.py          # 自研：尺寸守卫——宽<1536 居中 pad，防 crop 越界填黑
│   └── clear_area/panel       # enhance_toolkit 内：清线稿自带字样 / 标题纸板底板
├── references/
│   ├── theme-refinement.md    # 教材式主题凝练（默认）
│   ├── pipeline.md            # 十步流水线 + 命令模板
│   ├── annotation-schema.md
│   ├── srt-guidelines.md
│   ├── lessons-learned.md
│   ├── enhance_scenes_template.py
│   └── annotation_spec_example.json
└── assets/
    └── drawing-hand-clean.png
```
