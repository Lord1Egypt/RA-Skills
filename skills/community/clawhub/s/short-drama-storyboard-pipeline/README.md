# short-drama-storyboard-pipeline · 短剧分镜提示词流水线

> 🎬 Batch-generate first-frame image prompts and image-to-video prompts for AI short
> drama / comic drama — with character consistency anchors, 9:16 vertical shot
> vocabulary, and six model prompt dialects (Jimeng · Kling · Hailuo H3 · Seedance ·
> Vidu · Runway).
>
> 🎬 一条从剧本/分镜表到「可粘贴即用的提示词包」的批量流水线：首帧图提示词 + 图生视频
> 提示词（I2V 首帧驱动 / FL2V 首尾帧），角色一致性锚点逐字锁定，竖屏 9:16 镜头语言，
> 六类模型方言，CSV/JSON 批量清单导出。

**Install / 安装**

```bash
clawhub install @<your-handle>/short-drama-storyboard-pipeline
# or / 或
openclaw skills install @<your-handle>/short-drama-storyboard-pipeline
```

## Why / 为什么做这个

Cross-shot character face drift (跨镜头角色脸崩) and shot-by-shot prompt writing are
the two biggest time sinks in AI short-drama production. This skill turns one
standardized storyboard table into a complete prompt pack for a whole episode
(20–50 shots) in one pass:

1. **Character consistency anchors** — one verbatim-locked anchor string per
   character, reused word-for-word in every prompt (with a global negative-prompt
   library and character reference-sheet template)
2. **Six model dialects** — H3's structured 3-section format, Chinese natural
   language for Jimeng/Kling/Seedance, subject-reference workflow for Vidu,
   short English sentences + keyframes for Runway; never mixed in one session
3. **Cross-shot continuity** — FL2V tail frames chain to the next shot's first
   frame automatically
4. **Real batch export** — `scripts/export_prompts.py` validates the table
   (duration limits per model, missing anchors, frame modes) and emits per-shot
   prompt files + `manifest.csv` / `manifest.json` (Python 3.8+ stdlib only)

## Pipeline / 流水线

```
Script or rough shots  剧本片段/分镜表
   │  Step 1  Standardize storyboard table   分镜表标准化（11 列规范）
   ▼
   │  Step 2  Character consistency anchors  角色一致性锚点（逐字锁定）
   ▼
   │  Step 3  Prompt generation by dialect   按模型方言批量生成
   ▼
   │  Step 4  Batch export & validation      批量导出与校验（脚本可选）
   ▼
Prompt pack  提示词包：S01.image.txt · S01.video.i2v.txt · … · manifest.csv/json
```

## Quick start / 快速开始

Tell your agent / 对 Agent 说：

> 帮我把这段短剧剧本转成分镜表，目标模型海螺 H3，竖屏 9:16，然后批量导出提示词包。

Or run the batch exporter directly / 或直接跑批量导出：

```bash
python3 scripts/export_prompts.py \
  --input examples/sample_storyboard.csv \
  --anchors examples/sample_characters.csv \
  --outdir out/EP01 --mode both --model hailuo
```

## What's inside / 包内结构

```
short-drama-storyboard-pipeline/
  SKILL.md                      Trigger rules + 4-step pipeline / 触发与四步流水线
  references/
    storyboard-spec.md          11-column table spec & validation / 分镜表规范
    consistency-anchor.md       Anchor formula, reference sheets, negatives / 锚点系统
    shot-vocabulary.md          9:16 shot sizes, camera moves, drama pacing / 镜头语言
    model-dialects.md           Six-model prompt dialects / 六模型方言速查
  scripts/
    export_prompts.py           Batch exporter & validator / 批量导出脚本（可选）
  examples/                     Sample storyboard + anchor table / 样例数据
```

## Good fits / 适合谁

1. AI 短剧/漫剧工作室与个人创作者（竖屏 9:16 剧情向）
2. 网文 IP 改编团队需要批量分镜出图出视频
3. 用即梦/可灵/海螺/Seedance/Vidu/Runway 量产但要保角色一致的创作者

Not for / 不适合：单条独立视频、剪辑合成、完整成片流水线。

## FAQ

1. **Does it call any paid API?** No. Pure prompt engineering + a stdlib-only Python
   script; video/image generation happens in your own model accounts.
   不调用任何付费 API，生成动作全部发生在你自己的模型账号里。
2. **Can I add another model dialect?** Yes — add a section in
   `references/model-dialects.md` following the same checklist (language, structure,
   keyframe handling, references, negatives).
   可以，按方言自检清单在 model-dialects.md 追加一节即可。
3. **Free?** This skill is free on ClawHub (MIT-0) and keeps updating for free.
   Optional Pro add-on: final-cut assembly script, comic-grid template library
   (9/16/25 panels), quick-start script and video tutorial —
   https://afdian.com/item/2e33aad6ad3111f195dc52540025c377
   本技能在 ClawHub 永久免费且持续更新；Pro 版（成片合成脚本+漫剧宫格模板库+视频教程）
   为可选增值内容，见上方爱发电链接。

## Version / 版本

- **1.0.2** (2026-09-11): Added optional Pro add-on link. 新增可选 Pro 增值版入口
  （成片合成脚本 / 漫剧宫格模板库 / 视频教程 / 一键上手脚本），免费版功能不变。
- **1.0.1** (2026-09-06): Security hardening. 安全加固：`export_prompts.py` 增加
  shot_id 白名单校验（仅允许 `[A-Za-z0-9_-]+`），拒绝用 `../` 等片段拼路径造成的目录逃逸；
  生成文件名统一经 `safe_name()` 清洗兜底。修复 ClawHub 扫描 T09 警告。
  修复：脚本提示词文件名不再信任 CSV 原样 shot_id。
- **1.0.0** (2026-09-05): Initial release. 4-step pipeline, 6 model dialects,
  consistency anchor system, batch export script, sample data.
  首发：四步流水线、六模型方言、锚点系统、批量导出脚本、样例数据。

---

License: MIT-0 (per ClawHub policy). 许可：MIT-0（遵循 ClawHub 平台政策）。
