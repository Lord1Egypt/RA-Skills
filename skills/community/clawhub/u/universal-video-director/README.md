# universal-video-director

端到端的视频、AI 短剧、漫剧生产流水线：原著分析、剧本、资产锁定、站位、分镜、视频提示词、确认后生产、剪辑合成、评审、循环修复。每个阶段产出一份带 JSON Schema 的标准产物，由校验器检查并标出问题出在哪个阶段。

An end-to-end pipeline for videos, AI short dramas, and comic-motion production: source analysis, story, asset lock, staging, storyboard, video prompts, confirmed production, edit/compose, review, and repair loops. Each stage writes a schema-validated artifact; the validator flags which stage a problem comes from.

只要用户想做短视频、AI 短剧、漫剧、动态漫、宣传片、解说视频、分镜脚本，想把小说、剧本、创意或素材变成视频，或者想诊断、修复一个已有的视频项目（人物穿帮、跳轴、字幕错、时长不对），都应使用本技能。只剪一段现成素材、只转码、只写一段文案时不需要它。

需要 Python 3.9+（校验器仅用标准库）；剪辑合成需要 ffmpeg/ffprobe；可选 Remotion 或 HyperFrames；生图、生视频、配音、配乐需要用户自备平台账号。

## 目录结构

- `SKILL.md` — 总控流程
- `references/stages/` — 各阶段方法
- `references/sources.md` — 上游借鉴与许可说明
- `assets/schemas/` — 各阶段 JSON Schema
- `assets/examples/` — 示例项目产物
- `scripts/uvd_validate.py` — 校验器
- `evals/` — 评估用例

## Install / 安装

```bash
npx skills add linkxzhou/universal-video-director
```

Or clone:

```bash
git clone --depth 1 https://github.com/linkxzhou/universal-video-director.git ~/.claude/skills/universal-video-director
```

- GitHub: https://github.com/linkxzhou/universal-video-director

## License

MIT（上游借鉴项目各自许可见 `references/sources.md`）
