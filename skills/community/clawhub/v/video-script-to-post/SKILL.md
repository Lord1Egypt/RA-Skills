---
name: video-script-to-post
version: 1.1.0
author: AI-Workflows
license: MIT
description: 短视频全链路编导引擎，从热点选题→分镜脚本→AI生成提示词→多平台排期，一站式输出可执行内容包
tags:
  - 短视频
  - 内容创作
  - AI编导
  - 多平台运营
  - AIGC
parameters:
  topic_or_product:
    type: string
    required: true
    description: 核心主题/产品名/活动名称
  target_platform:
    type: string
    required: true
    description: 发布平台（douyin/bilibili/video_account/xiaohongshu）
  video_duration:
    type: string
    required: false
    description: 目标时长（15s/30s/60s/3min）
  tone_style:
    type: string
    required: false
    description: 内容调性（专业科普/剧情反转/情绪共鸣/干货拆解/生活记录）
output_format: markdown
compatibility:
  - OpenClaw
  - Dify
  - Coze
  - SkillHub
---
# 🎬 短视频全链路编导

## 🎯 核心定位
将创意构思转化为可直接交付拍摄/AI生成的标准化内容工程包，深度适配主流短视频平台算法逻辑与用户停留习惯。

## 🔄 工作流指令
1. **结构规划**：根据 `target_platform` 与 `tone_style` 构建内容骨架（黄金3秒钩子→核心价值→行动号召）。
2. **分镜生成**：输出秒级分镜脚本表：画面描述/台词字幕/时长分配/音效BGM/AI视觉提示词。
3. **AI参数包**：生成适配 Midjourney/ComfyUI/Runway/Pika/Kling/Sora/Vidu/即梦 的精确提示词与参数配置（比例/风格/运动控制）。
4. **平台策略**：输出平台专属优化方案（封面标题/推荐标签/发布时间/评论区互动话术）。
5. **合规校验**：自动检测广告法敏感词、版权风险与平台社区公约红线。
6. **模板输出**：按标准 Markdown 结构生成工程包。

## 📤 输出模板
```markdown
# 🎥 短视频内容工程包

## 1. 分镜脚本表
| 秒数 | 画面描述 | 台词/字幕 | 音效/BGM | 视觉提示词(AI) |
|:---|:---|:---|:---|:---|
| 0-3s | ... | ... | ... | `prompt...` |
| ... | ... | ... | ... | ... |

## 2. AI生成参数包
- **Midjourney/ComfyUI（文生图/图生视频）**: `--v 6.0 --ar 9:16 --style raw --s 750 ...`
- **Runway/Pika/Kling（视频生成）**: `motion: 7, camera: pan_left, seed: 42, negative_prompt: ...`
- **Sora/Vidu/即梦（文生视频）**: `style: cinematic, duration: 5s, camera: orbit, lighting: moody`
- **可灵 Kling（中国区首选）**: `duration: 5, motion_bracket: [3,7], ratio: 9:16, negative: 面部扭曲`
- > 💡 提示词需根据实际模型版本微调参数。各模型最新 API 参数请参照对应官方文档。

## 3. 平台运营策略
| 维度 | 抖音 | B站 | 视频号 | 小红书 |
|:---|:---|:---|:---|:---|
| 封面标题 | ... | ... | ... | ... |
| 推荐标签 | `#...` | `#...` | `#...` | `#...` |
| 互动引导 | ... | ... | ... | ... |

## 4. 合规与版权提醒
- 字体/音乐版权状态：...
- 广告法敏感词检测：...
> 📌 本包需经编导/法务复核后进入制作流。AI提示词需根据实际模型版本微调参数。
