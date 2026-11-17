# 踩坑与铁律（本项目 10 部视频沉淀）

把白板动画流水线跑顺之前，踩过的坑都记在这里。**新做视频前通读一遍可省数小时。**

## 1. annotation 的 startMs 必须是「幕内相对时间」

- ❌ 写成成片绝对时间（如 105000ms）→ 这一幕被拉长到几十秒，合并后成片虚高、音画错位。
- ✅ 写成幕内从 0 起算的相对时间；合并总时长 = 各幕 `sceneDurationMs` 之和。
- 自检：写完 annotation 后断言「末元素 end < sceneDurationMs」。
- 用 `make_annotation.py` 自动生成可规避此坑。

## 2. ImageGen 并行生成会「同名覆盖」

- 一次并行生成多张线稿时，若 prompt 触发相同文件名，后发的会覆盖先发的（本项目 V06、V09 都中招）。
- ✅ 每张分别生成、生成后立即 `mv` 成唯一名（如 `scene-01-xxx.png`、`scene-02-yyy.png`）。

## 3. 配音时长要用「实测」，别用估

- 云希（zh-CN-YunxiNeural）常速约 **5.2 字/秒**。手写 `durations.json` 估算会系统性偏短（本项目 V09 每段短约 1.06s，22 段累计差 24s），导致段间重叠、配音塞不进画面。
- ✅ 用 `prepare_narration.py`：先 edge-tts 合成每段 → 裁静音 → 测真实时长 → 段间留 0.4s 间隙算锚点 → 写 `narration_plan.json`。再交给 `narrate_edge_tts.py`。
- 若实测配音 > 无声成片时长：**延长各幕 `sceneDurationMs` 并重渲**，或给慢段加正 rate（微加速），不要事后硬拉音频（会吞字）。

## 4. 字幕遮挡画布正文

- libass 实际渲染位置：video_y = canvas_y × 0.6944。字幕默认落在 y≈717–780，会盖住画布下半部正文。
- ✅ 用推荐烧录样式（FontSize=21，MarginV=28，白字黑描边），并把画布正文控制在上方 2/3 区域；线稿下半部留白给字幕。

## 5. 增强图元必须落在揭示区内

- `render_stream_whiteboard.py` 只在标注 `region` 内揭示墨迹（_allowed_mask）。PIL 用 `enhance_toolkit.py` 画的标题/标签/便签，如果画在区域框外，渲染时**不会显示**。
- ✅ 增强图上的每个文字块，都要在对应 `region` 框内；多块内容用多个 region 分别揭示。

## 6. 手部素材要显式传入

- 渲染命令必须带 `assets/drawing-hand-clean.png`，否则用内置 `drawing-hand.png`（可能不存在）或退化成程序化笔尖。自包含版已把素材放进 `assets/`，默认即指向它。

## 7. 环境：缺 soundfile / edge-tts 会中途崩

- `narrate_edge_tts.py` 与 `build_subtitles.py` 依赖 soundfile；`prepare_narration.py` 依赖 edge_tts。先跑 `prepare_env.py` 建好 venv（已把这两个加进依赖清单）。

## 8. 抽帧质检不可省

- 每部成片至少抽 5–7 帧（开头/各幕交界/结尾），核对：标题是否完整、主体是否揭示完毕、字幕是否压正文、音峰是否 < 0dB。本项目 V04 因字幕压住第五层文字返工过一次。
