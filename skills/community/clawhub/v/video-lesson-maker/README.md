# 视频主题凝练及制作 (video-lesson-maker)

基于一篇文档（教材 / 课件 / 科普文章），凝练教学视频主题，并用**白板手绘动画 + 云希配音 + 同步字幕**批量制作科普 / 教学视频。

> 自包含：渲染 / 合并 / 配音 / 字幕脚本与手部素材全部内嵌，无需依赖其他技能即可独立运行。
> 已在本机 **10 部化妆品法规教学视频**上完整跑通。

## v1.4 更新：三道版式关卡，文字贴边与内容丢失都被机制拦下

上一版只做「渲染前体检」。用户第二次反馈「文字贴近边缘、显示不全」后复盘发现，问题有一半发生在**渲染之后**（字幕遮挡、libass 静默失败、合流丢幕），于是补齐成三道关卡：

| 关卡 | 脚本 | 时机 | 判据 |
|---|---|---|---|
| ① 绘制期钳制 | `enhance_toolkit` | 落笔时 | `SAFE_MARGIN=34` / `SAFE_TOP=36` / 字幕带 `y1≤756`，超出即平移回安全区 |
| ② 渲染前体检 | `check_layout.py` | 渲染前 | 贴边 / 入字幕带 / 永不被揭示，必须 0 问题；**支持底图对比模式** |
| ③ 成片复核 | `check_render.py` `NEW` | 烧字幕之后 | **内容覆盖率 ≥ 0.99**，并输出成片四边实际留白 |

关键改动：
- `check_layout.py` 重写为 v2：新增 `--base auto`（与 `-base.png` 做差，只量 PIL 新增墨迹，线稿本身不再误报）、解析 `maskPaddingPx` 参与归属判断（消除 6 处假阳性）、新增 `--json` 机器可读报告。
- `enhance_toolkit` 新增 `clamp_box` / `clamp_center` / `draw_text_center`，按**真实墨迹矩形**钳制（此前按文字原点钳，因字体 ascender 有 16px 偏差，仍会压进字幕带）。
- 新增 `check_render.py`：解成片末帧与增强图逐像素比对，列出「源图有、成片没有」的墨迹块并给出最近 region。
- 沉淀 7 条新教训（`lessons-learned.md` #24）：底图对比、maskPaddingPx、墨迹框 vs 原点框、成片像素倒推边距、ffmpeg `ass=` 不吃中文绝对路径、批量返工工程化（备份→脚本化→单片验证→放量）。

实测：项目1 十片 31 幕，修复前 22 幕有问题（99 处贴边 / 28 处压字幕带 / 3 处整块不显示），修复后 `--margin 32` 下 **0 问题**，成片覆盖率全部达标。

## v1.3 更新：文字不再贴边/被裁
- `enhance_toolkit`：`draw_label_card` / `draw_note` / `draw_title` / `safe_text` 按框宽**自动缩字号**（`fit_font`），超宽打印提示；`draw_note` 胶带改为框内绘制（原先越界 12px 永远不被揭示）。
- 新增 `scripts/check_layout.py`：渲染前体检，直接列出**永远不会被揭示的墨迹**与贴边图元；`--fix` 自动外扩 region。
- 新增 `scripts/make_spec.py` + `enhance_toolkit.LAYOUT`：spec 由绘制结果生成，坐标只有一份，杜绝漂移。

## 能力一览
- **主题凝练**：把一篇文档按「任务点 / 章节 / 知识点」拆成若干视频点，输出规划表与每点口播 SRT。
- **视频制作**：手绘线稿 → 去水印 → 匀纸 → 裁剪 1536×864 → PIL 增强 → 白板动画渲染 → 多幕合并。
- **配音**：edge-tts 云希（zh-CN-YunxiNeural）逐段合成，**先测真实时长再算锚点**，根除段间重叠。
- **字幕**：从真实音轨重建「意群完整 + 不超框」的同步字幕并烧录成片。

## 安装
```bash
# 方式一：openclaw（如已安装）
openclaw skill install ./video-lesson-maker

# 方式二：手动
unzip video-lesson-maker-v1.4.1.zip -d ~/.workbuddy/skills/
```

## 快速开始
1. 把源文档 / 教材拆成视频点，写每点的 `scripts/Vxx-主题.srt`（口播稿，参考 `references/srt-guidelines.md`）。
2. 用 ImageGen 生成每幕手绘线稿（1536×1024）。
3. 预处理：`remove_watermark.py` → `homogenize_paper.py` → 裁剪 `y55-919` 得 1536×864。
4. 写 `enhance_scenes.py`（PIL 在标注区内绘字 / 图元）→ 生成 `*-enh.png`。**保留 `-base.png`**，体检要用它做差。
5. **版式体检**：`check_layout.py --dir <目录> --margin 32` 必须 0 问题（见 `SKILL.md`「版式安全」）。
6. 写 `scene-xx.annotation.json`（推荐 `make_spec.py` 由 `layout-0N.json` 生成；**startMs 必须为幕内相对时间**）。
7. 渲染：`render_stream_whiteboard.py`；多幕用 `merge_scenes.py` 拼接为无声版。
8. 配音：`prepare_narration.py` 先合成并测真实时长 → 生成 `narration_plan.json` → `narrate_edge_tts.py`。
9. 字幕：`make_subtitle_plan.py` → `build_subtitles.py` 生成同步字幕 `.srt` → `srt_to_ass.py` 转 ASS。
10. 烧录：`cd` 进目录用 `-vf "ass=相对路径.ass"` 烧进配音版 → `*-完整版.mp4`（绝对路径 libass 打不开）。
11. **成片复核**：`check_render.py --dir <目录>`，内容覆盖率 ≥ 0.99 才算过。
12. 质检：抽帧看画面、听音画字对齐、查音峰 < 0 dBFS。

完整命令模板与 8 条避坑铁律见 `references/pipeline.md` 与 `references/lessons-learned.md`。

## 目录结构
```
video-lesson-maker/
├── SKILL.md              # 主文档（触发词 + 完整流水线）
├── manifest.json         # Clawhub 元数据（author / category / icon）
├── README.md             # 本文件
├── scripts/              # 渲染 / 合并 / 配音 / 字幕 / 辅助脚本
├── references/           # 主题凝练 / 流水线 / 标注 schema / 字幕规范 / 踩坑
└── assets/
    ├── drawing-hand-clean.png   # 手写动画手部素材
    └── icon.png                 # Clawhub 列表图标
```

## 依赖
- Python >= 3.10
- 系统：`ffmpeg`（推荐，或由环境变量 `FFMPEG_PATH` 指定）
- pip：`opencv-python numpy av Pillow soundfile edge-tts`

首次运行可调用 `scripts/prepare_env.py` 自动建 venv 并安装依赖。

## 许可证
MIT
