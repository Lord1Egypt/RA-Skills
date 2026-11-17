# 本地技能溯源表（repos.md）

> 适用范围：Kyle 本机环境（346 个本地技能中的 34 个动画/视频技能）。对普通用户本表通常为空——那是正常的，路由器会走内置精选目录。本表的价值：本地命中技能时报告上游仓库、识别共享基座、指导联动升级。

本文件是 video-skill-router 的「技能 → 上游仓库」映射基准。用途：

1. 本地命中某技能时，向用户报告其上游仓库（便于追踪更新、找替代品）
2. 外部发现时，优先推荐已有本地技能上游生态的仓库（版本一致性）
3. 维护本地技能体系时，识别哪些技能共享同一基座（基座升级需联动冒烟）

## 1. A 类：基于开源项目的技能（可追踪原仓库）

| 本地技能 | 上游项目 | 仓库 | 说明 |
|---|---|---|---|
| ManimCE最佳实践 | Manim Community | https://github.com/ManimCommunity/manim | 数学动画主力引擎，41k+ stars |
| ManimGL最佳实践 | ManimGL (3b1b) | https://github.com/3b1b/manim | 3b1b 原版，ManimCE 的上游起源 |
| 数学动画 | Manim（写 Scene） | https://github.com/ManimCommunity/manim | 自研 13 步 SOP 跑在 ManimCE 上 |
| 口播动画编排（主） | Manim + FFmpeg + LaTeX | https://github.com/FFmpeg/FFmpeg | 编排层，底座为 Manim 系 |
| 图形动画 | Remotion | https://github.com/remotion-dev/remotion | React 写视频；注意商业许可（>3 人收费） |
| 信息图素材 | Remotion | https://github.com/remotion-dev/remotion | 口播动画素材分支 1 |
| 视频动效卡片 | Remotion | https://github.com/remotion-dev/remotion | 108 张动效配方卡 |
| 口播素材规划 | Remotion + Manim | 见上两行 | 素材决策层 |
| 内容生产编排器 | Remotion + 剪映 | 见上 + 剪映（商业） | 门控流程编排 |
| 真人出镜口播视频剪辑 | Remotion | https://github.com/remotion-dev/remotion | 真人出镜成片 |
| Whisper语音识别 | OpenAI Whisper | https://github.com/openai/whisper | 本地语音转文字（marketplace 来源） |
| 视频文案提取 | Whisper | https://github.com/openai/whisper | 离线转写，模型缓存 ~/.whisper-models |
| 视频分析（字幕链路） | whisper.cpp | https://github.com/ggerganov/whisper.cpp | C++ 推理版 |
| 通用视频下载器 | faster-whisper + yt-dlp | https://github.com/SYSTRAN/faster-whisper ; https://github.com/yt-dlp/yt-dlp | 多平台下载统一入口 |
| la-pian | ffmpeg + faster-whisper + ocrmac | 见上 | 拉片分析（marketplace 来源） |
| TTS音频生成 | edge-tts + Whisper | https://github.com/rany2/edge-tts | 微软 Edge 朗读接口 |
| 爆款视频封面 | ffmpeg + rembg | https://github.com/danielgatis/rembg | 抽帧 + 抠图 + 提示词工程 |
| Kimi浏览器录制 | Playwright + FFmpeg | https://github.com/microsoft/playwright | 浏览器录屏 |
| 个性化播客生成 | FFmpeg + pydub | https://github.com/jiaaro/pydub | 文本转播客 |
| 音视频同步渲染 | Playwright + FFmpeg | 见上 | 口播字幕视频合成步 |
| 口播字幕视频 | FFmpeg + Whisper + Playwright | 见上 | 编排器（父） |

基座共享关系（升级需联动）：

- **Remotion 系**：图形动画 / 信息图素材 / 视频动效卡片 / 口播素材规划 / 真人出镜口播视频剪辑 / 内容生产编排器——共享 `remotion/node_modules`，Remotion 升版必须全家冒烟
- **Manim 系**：ManimCE / ManimGL / 数学动画 / 口播动画编排（主）——共享 manim 包 + FFmpeg + LaTeX
- **Whisper 系**：Whisper语音识别 / 视频文案提取 / 视频分析 / 通用视频下载器 / la-pian / TTS音频生成——三套实现（whisper / whisper.cpp / faster-whisper）并存，按场景选用
- **FFmpeg 系**：几乎所有视频技能的公共底座

## 2. B 类：商业 API / 产品（官网溯源，无开源仓库）

| 本地技能 | 商业产品 | 入口 |
|---|---|---|
| AI视频生成 | 可灵 Kling 3.0（快手） | https://klingai.com |
| 数字人对口型 | QCAPI pic-video-v12 | 商业 API（卡密计费） |
| 声音复刻配音 | MiniMax 音色复刻 | https://www.minimax.com |
| 开拍AI视频处理 | 开拍（videoscreenclear / hdvideoallinone） | 商业 API |
| VectCut剪辑 | VectCut | https://www.vectcut.com/ |
| 剪映编辑器 | 剪映 JyWrapper | 剪映客户端自动化 |
| 智灵视频分析 | 腾讯智灵 | 云端 API |

## 3. C 类：桂皮自研技能（本地沉淀，无上游仓库）

口播动画素材（父）、口播字幕视频、HTML字幕舞台、动画网页PPT、杂志风网页PPT、overlay-fx-generator、ai-promo-video-maker、nuwa-skill、视频创作、视频分析、百度视频文稿提取、长视频学习工具、视频拉片节奏分析、内容生产编排器。

这些技能的「源头」即桂皮本人的工作流沉淀，外部发现时**不要**找同类仓库替换，只在能力缺口出现时才扩展。

## 4. D 类：marketplace 来源技能

以下技能带 `_skillhub_meta.json`（source: marketplace），升级走市场通道，不要手动改：

- Whisper语音识别、la-pian、杂志风网页PPT

## 5. 维护规则

1. 新增动画/视频技能时，在此表登记一行（含来源分类）
2. 基座项目（Manim/Remotion/FFmpeg/Whisper）发布大版本时，检查对应共享基座技能是否需联动升级
3. 每季度核对一次开源仓库活跃度（stars/最近 commit），僵死项目在 catalog.md 标注替代候选

## 6. 版本记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v1.0 | 2026-10-23 | 创建溯源表：34 个本地动画/视频技能映射到上游仓库/商业产品/自研，识别 4 大共享基座 | 桂皮 |
| v1.1 | 2026-10-23 | 随技能更名为 video-skill-router，内容不变，补充普通用户适用说明 | 桂皮 |
