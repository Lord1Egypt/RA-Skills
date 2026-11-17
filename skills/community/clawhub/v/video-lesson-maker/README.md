# 视频主题凝练及制作 (video-lesson-maker)

基于一篇文档（教材 / 课件 / 科普文章），凝练教学视频主题，并用**白板手绘动画 + 云希配音 + 同步字幕**批量制作科普 / 教学视频。

> 自包含：渲染 / 合并 / 配音 / 字幕脚本与手部素材全部内嵌，无需依赖其他技能即可独立运行。
> 已在本机 **10 部化妆品法规教学视频**上完整跑通。

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
unzip video-lesson-maker-v1.0.0.zip -d ~/.workbuddy/skills/
```

## 快速开始
1. 把源文档 / 教材拆成视频点，写每点的 `scripts/Vxx-主题.srt`（口播稿，参考 `references/srt-guidelines.md`）。
2. 用 ImageGen 生成每幕手绘线稿（1536×1024）。
3. 预处理：`remove_watermark.py` → `homogenize_paper.py` → 裁剪 `y55-919` 得 1536×864。
4. 写 `enhance_scenes.py`（PIL 在标注区内绘字 / 图元）→ 生成 `*-enh.png`。
5. 写 `scene-xx.annotation.json`（**startMs 必须为幕内相对时间**，见 `references/lessons-learned.md`）。
6. 渲染：`render_stream_whiteboard.py`；多幕用 `merge_scenes.py` 拼接为无声版。
7. 配音：`prepare_narration.py` 先合成并测真实时长 → 生成 `narration_plan.json` → `narrate_edge_tts.py`。
8. 字幕：`make_subtitle_plan.py` → `build_subtitles.py` 生成同步字幕 `.srt`。
9. 烧录：`ffmpeg` 把字幕烧进配音版 → `*-完整版.mp4`。
10. 质检：抽帧看画面、听音画字对齐、查音峰 < 0.9 dBFS。

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
