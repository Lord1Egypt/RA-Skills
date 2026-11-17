---
name: social-video-resizer
description: 把一条社媒视频快速变成多个平台可发的尺寸版本——在 9:16、1:1、4:5、16:9 之间选择 crop / pad / scale 最佳策略，保护人脸、产品与字幕安全区，输出各平台可直接使用的适配方案。
---

# Social Video Resizer

把一条社媒视频，快速变成多个平台可发的尺寸版本。

## Quick Reference

| 决策点 | Strong（推荐） | Acceptable（可接受） | Weak（避免） |
|---|---|---|---|
| 策略选择 | 按主体位置定：主体居中→crop；信息占满画面→pad | 统一 pad 加模糊背景 | 直接拉伸变形 |
| 主体保护 | 逐镜头确认人脸/产品/字幕在目标画幅内 | 按整片主要构图判断一次 | 只看首帧 |
| 字幕处理 | 压在安全区内或建议重新上字幕 | pad 保留原字幕 | crop 切掉半行字幕不提示 |
| 目标清单 | 每个平台给出确切分辨率+比例+时长上限 | 只给比例 | "适配一下各平台" |
| 竖转横 | 优先 pad（模糊/纯色底）或建议重构图 | 中心 crop 且主体确认安全 | 硬 crop 切掉主体 |
| 横转竖 | 找主体做跟踪式 crop 或上下 pad 加标题区 | 中心 crop | 拉伸填满 |
| 交付说明 | 每版本注明策略+取舍+风险 | 注明策略 | 只给文件不给说明 |

## Solves

1. **平台尺寸要求不一** —— TikTok/Reels/Shorts 要 9:16，Feed 要 1:1/4:5，YouTube 要 16:9，一条素材到处不能直接发。
2. **硬拉伸毁画面** —— 直接 scale 到目标比例，人物变形、品牌感尽失。
3. **裁切切掉关键信息** —— crop 后字幕少半行、人脸出画、产品被切边。
4. **广告位审核被拒** —— 尺寸、时长、文件大小不符合广告位规格，投放被打回。
5. **逐平台手工重做** —— 没有标准决策流程，每次适配都从头摸索。
6. **成片安全区意识缺失** —— 平台 UI（进度条、按钮、标题）盖住关键内容。

## Use when

- 一条视频要同时发 TikTok、Instagram、YouTube Shorts、Facebook、X 等平台
- 需要在 9:16、1:1、4:5、16:9 等比例之间切换
- 需要决定 pad、crop 还是 scale 的最佳策略

## Do not use when

- 需要高级主体追踪或复杂智能重构镜头
- 视频内容本身构图太差，需要重新剪辑而非单纯改尺寸（转 product-video-cutter）

## Inputs

- Source video file
- Target platforms or ratios
- Whether the priority is face, product, subtitles, or full-frame preservation
- Optional output dimensions, file size limit, or ad placement requirements
- Optional brand constraints such as background color or padding preference

## Workflow

### Step 1 — 确认目标清单

把"发到各平台"翻译成确切规格：平台 → 比例 → 分辨率 → 时长上限 → 文件大小限制。对照 references/platform-spec-sheet.md，广告位规格以投放后台为准。

### Step 2 — 识别保护对象

明确优先级：人脸 > 字幕/关键文字 > 产品 > 完整画面。逐个关键镜头检查主体位置（不能只看首帧），标出主体活动范围。

### Step 3 — 逐版本选策略

按 references/crop-pad-scale-guide.md 的决策树选 crop / pad / scale 组合。核心原则：宁 pad 不变形，宁 crop 不糊底，绝不拉伸。

### Step 4 — 检查安全区

每个目标平台有 UI 遮挡区（底部进度条、右侧按钮栏、顶部标题）。关键内容退到安全区内，字幕位置逐平台确认。

### Step 5 — 输出适配方案

按 references/output-template.md 输出：每个版本的尺寸、策略、构图取舍、风险提示，以及可选的 ffmpeg 命令。

### Step 6 — 自检

对照 assets/resize-checklist.md 逐项检查后交付。

## Worked Example 1 — 16:9 横版测评 → 9:16 + 1:1

**输入：** 1920×1080 横版产品测评（人物居左 1/3，产品特写居中，底部有烧录字幕），要发 TikTok（9:16）和 Instagram Feed（1:1），优先保护人脸和字幕。

**输出（核心部分）：**

> **版本 A — TikTok 9:16（1080×1920）：**
> 策略：以人物为锚点做偏左 crop（取源画面 x=0-607px 区域会切掉产品特写）→ 改用"上下 pad + 中间 16:9 原片"结构：原片 scale 到 1080×608 居中，上方加标题区（写视频主题），下方加品牌色底。
> 理由：人物和产品分布两侧，任何 9:16 crop 都会丢一个主体；pad 保全部信息。
> 风险：原片字幕在 pad 版中偏小，建议重新上竖版大字幕。
>
> **版本 B — IG Feed 1:1（1080×1080）：**
> 策略：中心偏左 crop（x=180-1260px），人物完整保留，产品特写镜头单独检查——第 42-48s 产品在画面右缘，该段改为轻微右移的动态 crop 或接受产品切边。
> 风险：底部烧录字幕两端各被切 90px，需确认无整行文字丢失；抽查 3 处字幕最长的镜头。

## Worked Example 2 — 9:16 竖版达人视频 → 16:9 YouTube + 4:5 Feed 广告

**输入：** 1080×1920 竖版口播带货视频，人脸居中偏上，字幕在下 1/3，要投 YouTube 插播广告（16:9，≤30s）和 Facebook Feed 广告（4:5，文件 ≤4GB, 实际 30MB 上限更稳）。

**输出（核心部分）：**

> **版本 A — YouTube 16:9（1920×1080）：**
> 策略：竖转横不 crop（会只剩一张脸）。用"两侧模糊 pad"：原片 scale 到 608×1080 居中，两侧用放大 20 倍+高斯模糊的本片做底。
> 备注：更优方案是重构图（左侧人物右侧上产品图+卖点字卡），如有设计资源建议采用。
> 时长：源片 45s 超广告位 30s 上限，需先剪（转 product-video-cutter）再适配。
>
> **版本 B — Facebook 4:5（1080×1350）：**
> 策略：crop：保留 y=285-1635px 区域，人脸完整，字幕上移前的位置检查——原字幕底部 60px 落在切除区，建议字幕整体上移或重烧。
> 压缩：H.264, ~8Mbps, 目标 <30MB。

## Common Mistakes

1. **拉伸填满** —— 任何情况下都不允许非等比 scale，人物变形是最显眼的低质信号。
2. **只看首帧定 crop** —— 主体会移动，必须检查关键镜头的主体活动范围。
3. **切掉半行字幕** —— crop 后字幕缺字比没字幕更糟；切到字幕必须提示重烧。
4. **忽略平台 UI 遮挡** —— 9:16 平台右侧按钮栏和底部进度条会盖住内容，关键信息要退进安全区。
5. **竖转横硬 crop** —— 9:16 crop 成 16:9 通常只剩鼻子以上，几乎总应该用 pad 或重构图。
6. **忘记时长和文件大小限制** —— 尺寸对了但超时长/超体积照样被拒，规格要一次对齐。
7. **所有平台共用一个 1:1 妥协版** —— 1:1 在 9:16 信息流里占屏小、完播差，能出竖版就出竖版。
8. **pad 底色随意** —— 模糊 pad 或品牌色 pad 都行，但要与品牌规范一致，纯黑底最显廉价。
9. **交付无说明** —— 每个版本必须写策略与取舍，否则运营不知道哪个版本能投哪个位。

## Resources

- `references/output-template.md` — 适配方案标准输出模板
- `references/platform-spec-sheet.md` — 主流平台尺寸/时长/体积规格表
- `references/crop-pad-scale-guide.md` — 策略决策树与 ffmpeg 命令参考
- `assets/resize-checklist.md` — 交付前自检清单
