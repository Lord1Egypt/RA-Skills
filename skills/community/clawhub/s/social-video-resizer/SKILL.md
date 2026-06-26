---
name: social-video-resizer
description: Adapt one social video into platform-ready aspect ratios and dimensions for TikTok, Reels, Shorts, feeds, stories, and ads without awkward stretching or lost focal points. Use when teams need fast cross-platform resize decisions.
---

# Social Video Resizer

把一条社媒视频，快速变成多个平台可发的尺寸版本。

## Problem it solves
同一条内容发不同平台时，尺寸要求经常不一样：
- TikTok / Reels / Shorts 偏 9:16；
- Feed、广告位、封面预览可能要 1:1、4:5、16:9；
- 直接硬拉伸会让人物变形，直接裁切又容易切掉字幕、脸或产品。

这个 skill 的目标是：
**在不破坏主体和关键信息的前提下，把一条视频适配成多个社媒平台可直接使用的尺寸版本。**

## Use when
- 一条视频要同时发 TikTok、Instagram、YouTube Shorts、Facebook、X 等平台
- 需要在 9:16、1:1、4:5、16:9 等比例之间切换
- 需要决定 pad、crop 还是 scale 的最佳策略

## Do not use when
- 需要高级主体追踪或复杂智能重构镜头
- 视频内容本身构图太差，需要重新剪辑而非单纯改尺寸

## Inputs
- Source video file
- Target platforms or ratios
- Whether the priority is face, product, subtitles, or full-frame preservation
- Optional output dimensions, file size limit, or ad placement requirements
- Optional brand constraints such as background color or padding preference

## Workflow
1. 确认目标平台和尺寸要求。
2. 判断该用 crop、pad 还是 scale。
3. 优先保护人物、产品和字幕安全区域。
4. 输出一个或多个平台适配版本。
5. 说明每个版本的构图取舍和兼容性。

## Output
Return:
1. Target platform versions
2. Resize strategy per version
3. Output dimensions
4. Framing / subtitle safety notes
5. Additional recommended variants if useful

## Quality bar
- 绝不拉伸变形人物或产品
- 重要字幕和产品展示尽量不被切掉
- 优先使用平台安全尺寸
- 清楚说明 crop 与 pad 的取舍

## Resource
See `references/output-template.md`.
