---
name: video-deconstruct
version: 2.0.0
description: 把一段抖音/小红书短视频拆成「故事 + 心理学」式爆款拆解报告——选题/一句话总结/内容描述/视频结构(开头-中间-结尾)/事件推进/落幕文案/受众启示/核心爆点/节奏/BGM。给运营拍同款、写脚本、做分镜时直接当弹药。当用户说"拆解视频""分析这条视频""帮我看这段抖音""短视频结构""卡点在哪""这条爆款怎么火的"时触发。输入：本地 mp4 文件路径。输出：output/ 目录下一份 markdown 报告 + 一份原始 JSON。
author: 立瑄@StepFun
license: CC BY-SA 4.0
runtime: python3.10+
framework: StepClaw
models:
  - step-1o-turbo-vision      # 主拆解（视频原生输入）
  - stepaudio-2.5-asr         # v2.1 可选：把人声对白转为字幕辅助拆解
  - step-3.5-flash            # v2.1 可选：低成本快速合并/重写
requires:
  - openai (Python SDK)
  - httpx
  - jinja2
  - ffmpeg (system, ≥ 4.4) — 超过 128MB 时自动压缩兜底 + 抽音轨给 ASR
env:
  - STEP_API_KEY
inputs:
  - name: video
    type: path
    description: 本地 mp4 文件路径，长度建议 ≤ 3 分钟
    required: true
  - name: --with-asr
    type: flag
    description: 启用 stepaudio-2.5-asr 抽取对白文本一同投喂（强烈推荐）
    required: false
  - name: --comments-file
    type: path
    description: (v2 占位) 评论 txt 文件，启用后会做评论区聚类
    required: false
  - name: --keep-upload
    type: flag
    description: 分析完后保留云端文件，默认自动删除
    required: false
outputs:
  - path: output/{video_stem}-report.md
    description: 渲染好的爆款拆解 markdown 报告
  - path: output/{video_stem}-analysis.json
    description: 原始 JSON 分析结果（便于二次加工）
triggers:
  - 拆解视频
  - 分析这条视频
  - 帮我看这段抖音
  - 短视频结构
  - 卡点在哪
  - 这条爆款怎么火的
  - 视频拆解
  - 爆款拆解
tags:
  - video
  - 短视频
  - 抖音
  - 小红书
  - 拆解
  - 爆款分析
  - 运营
  - vision
  - asr
  - stepfun
  - stepclaw
---

# video-deconstruct (v2.0)

## 这个 skill 干啥

扔一段 mp4，吐一份**叙事式爆款拆解报告**。覆盖 10 个章节：

1. **选题介绍** — 一句话主题（≤ 12 字，可直接进选题库）
2. **一句话总结** — 主角关系 + 核心冲突 + 结局（≤ 100 字）
3. **内容描述** — 按时间线复述剧情，含转场+心理动机+元注释（300–600 字）
4. **视频结构分析** — 开头/中间/结尾各自的"设计点 + 效果分析"
5. **中间事件推进过程** — 3–8 条具体事件，每条"动作 + 隐含矛盾"
6. **视频结尾 + 落幕文案** — 收尾设计 + 字幕原文 + 受众启示
7. **核心爆点** — 为什么会火，必须涉及底层心理机制（120–250 字）
8. **节奏**（辅助）— 时间轴段落表，钩子/铺垫/转折/高潮/收尾
9. **BGM**（辅助）— 卡点位置、换歌点（纯视觉推断）
10. **评论区** — v1 跳过，v2 接入

## 快速开始

```bash
export STEP_API_KEY=sk-xxx
python scripts/analyze.py /path/to/your-video.mp4
# 报告生成在 ./output/your-video-report.md

# 强烈推荐：启用 ASR 把对白也喂进去
python scripts/analyze.py /path/to/your-video.mp4 --with-asr
```

详细步骤见 [`guides/01-quickstart.md`](guides/01-quickstart.md)。

## 想改输出风格？

- 改 `prompts/analysis_rubric.txt` 的字段定义/写作风格指引
- 改 `prompts/system.txt` 改 AI 的角色设定（默认是"资深拆解师"）
- 改 `templates/report.md.j2` 调整报告版式
- 详见 [`guides/03-prompt-engineering.md`](guides/03-prompt-engineering.md)

## 与 StepClaw Agent 框架的衔接

- `manifest.json` 已声明 `entry / inputs / outputs / triggers / models`，可被 StepClaw Agent 直接 dispatch
- 默认 `STEP_API_KEY` 走环境变量或 skill 根目录的 `.env`
- 输出路径 `output/{video_stem}-{report.md, analysis.json}` 是固定 schema，下游 Agent 可直接读取
- ASR 与 vision 模型都走 `https://api.stepfun.com/v1`，不需要额外 endpoint

## 限制

- 输入必须是 mp4。默认 **128MB 以内直传 StepFun 文件 API**；只有超过 128MB 才会自动两遍 ffmpeg 压缩（长视频可能降到 240p/低帧率，但 rubric 仍能分析节奏/卡点/事件；详见 `scripts/compress.py`）
- 没有对视频长度的硬限制，但超过 128MB 后会进入压缩兜底：3 分钟内通常可保 480p+，超长视频可能退化到近似 240p 幻灯片
- 运行时会先把（必要时压缩后的）文件上传到 StepFun 云端（临时），分析完后自动删除（除非加 `--keep-upload`）；压缩产物也会在处理完后清理
- BGM 维度仍以视觉线索为主（详见 `guides/02-叙事式拆解说明.md`）。`--with-asr` 启用后**对白文本**会作为辅助上下文喂给视觉模型，但不会直接做识曲
- 真识曲不做（要的话改成 ACRCloud / Audd.io，见 v3 路线）
