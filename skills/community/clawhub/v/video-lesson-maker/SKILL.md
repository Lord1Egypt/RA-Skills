---
name: video-lesson-maker
description: >-
  基于一篇文档（教材/课件/科普文章）凝练教学视频主题，并用白板手绘动画 + 云希配音
  + 同步字幕，批量制作科普/教学视频。当用户需要从文档拆出视频点、写口播脚本、生成
  手绘线稿、做白板动画渲染、用 edge-tts 配音、重建同步字幕并烧录成片时使用。触发词：
  教学视频、科普视频、视频主题凝练、白板动画、配音字幕、课程视频制作、把文档做成视频。
version: 1.0.0
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

## 工作流（十步，详见 `references/pipeline.md`）

1. 主题凝练 → 规划表 + 每点 SRT（`theme-refinement.md`）
2. ImageGen 生成手绘线稿（1536×1024，分别生成避免同名覆盖）
3. `remove_watermark.py` 去水印
4. `homogenize_paper.py` 匀纸
5. 裁剪到 1536×864
6. 增强：复制 `references/enhance_scenes_template.py`，按布局画标题/标签/便签（必须落在 region 内）
7. 标注：`make_annotation.py` + spec 生成 `annotation.json`（startMs 幕内相对！）
8. 渲染：`render_stream_whiteboard.py`（传 `assets/drawing-hand-clean.png`）
9. 合并：`merge_scenes.py` → 无声.mp4
10. 配音+字幕+烧录：`prepare_narration.py` → `narrate_edge_tts.py` → `make_subtitle_plan.py` → `build_subtitles.py` → ffmpeg 烧录 → 完整版.mp4

## 环境准备（首次必跑）

```bash
ENV_PY=$(python <skill>/scripts/prepare_env.py)   # 建隔离 venv，末行输出 ENV_PY 路径
# 系统需有 ffmpeg（或运行前 export FFMPEG_PATH=...）
```

所有脚本都用该 `ENV_PY` 运行；`prepare_env.py` 已包含 cv2 / numpy / av / Pillow / soundfile / edge-tts。

## 关键铁律（新做视频前必读 `references/lessons-learned.md`）

- **annotation.startMs 是幕内相对时间，不是成片绝对时间**（V05 大坑，写成绝对时间会虚高几十秒）。
- **配音时长用实测**，别手写估算；实测超画面就延长各幕 `sceneDurationMs` 重渲（V09 教训）。
- **字幕单行 ≤ 28 字**，且烧录样式放画面下方不压正文。
- **ImageGen 多幕分别生成、分别改名**，避免同名覆盖。
- **增强图元必须落在标注 region 内**，否则渲染不显示。

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
│   └── make_annotation.py     # 自研：spec→annotation.json
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
