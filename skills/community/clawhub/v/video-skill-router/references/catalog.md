# 内置精选目录（catalog.md）

本目录是 video-skill-router 的**一级渠道**：随技能分发，零网络成本，全部条目经过实证。机器可读版在 `data/curated-catalog.json`（match_skill.py 直接读它）。

## 实证标准（2026-10-23）

每个条目都通过了：仓库存在 ✓ / 含 SKILL.md 实体（路径已核实）✓ / stars 与 description 为 GitHub API 实测值 ✓。

**未通过实证不进本目录**：ManimCat（无 SKILL.md，是库不是技能包）与 iart-ai/motion-skills（描述称 50 个 skills 但仓库内无 SKILL.md 实体）已排除，仅登记在 `sources.md` 备查。

## 1. 技能包（可直接安装执行）

### 商业宣传类

| 技能包 | 仓库 | Stars | 装哪个 | 能干嘛 |
|---|---|---|---|---|
| motion-design-skill | LottieFiles/motion-design-skill | 2441 | `skills/motion-design` | Lottie 官方动效设计：AE 导出规范、播放调试、Web/产品演示动画 |
| video-talkcraft | Vincentwei1021/video-talkcraft | 1713 | 根目录 | 把 AI 代理变成动效设计工作室，Remotion/Motion 宣传短片一条龙 |
| OpenMontage | calesthio/OpenMontage | 70908 | `.agents/skills/<子技能>` | agentic 视频生产系统，ai-video-gen / 3d-asset-generation 等 12+ 技能 |
| ad-video-skills | iart-ai/ad-video-skills | 18 | `skills/<子技能>` | 广告三模板：创意广告 / 发布视频 / 证言，批量出 A/B 成片 |
| ai-shorts-generator | hueanmy/ai-shorts-generator | 28 | `.claude/skills/<子技能>` | 科技资讯/促销短视频，news + promo，含 ElevenLabs 配音 |
| awesome-motion-design-agent-skills | frankxai/awesome-motion-design-agent-skills | 76 | `skills/<子技能>` | 动效 agent 技能精选：GSAP/Motion/Remotion/Lottie/Rive，按需取用 |

### 知识科普类

| 技能包 | 仓库 | Stars | 装哪个 | 能干嘛 |
|---|---|---|---|---|
| manim_skill | adithya-s-k/manim_skill | 1201 | `skills/<子技能>` | Manim 三技能：composer 创作编排 + CE/GL 双版本最佳实践，3B1B 风格 |
| MathLens | shuyicc/MathLens | 362 | 根目录 | 数学题视频讲解：贴题目（图/文）→ 分析 → 可视化 → 成片 |

### 其他类

| 技能包 | 仓库 | Stars | 装哪个 | 能干嘛 |
|---|---|---|---|---|
| herk-edit-kit | nateherkai/herk-edit-kit | 2017 | `.agents/skills/<子技能>` 或 `--all-skills` | 15 个剪辑技能：剪口误、静音剪切、粗剪精剪，转写驱动 |
| FireRed-OpenStoryline | FireRedTeam/FireRed-OpenStoryline | 3553 | `.claude/skills` | AI 剪辑 agent：自然语言描述直接出片，附转场/风格化技能 |
| baocut | JimLiu/baocut | 1208 | `.agents/skills/bcut-release` | AI 视频 agent：可编辑时间轴，转写+字幕+剪辑一体 |

安装命令模板：

```
python scripts/manage_skill.py install --repo <owner/name> --subdir <上表「装哪个」列> --reason "<匹配理由>"
# 整包安装（技能包内多技能都有用时）：
python scripts/manage_skill.py install --repo <owner/name> --all-skills --reason "<匹配理由>"
```

## 2. 引擎库（不可直装，作能力源参考）

这些是底座项目，本身不含 SKILL.md。用途：① 用户需求超出技能包能力时，指引用户/agent 基于引擎自建技能；② 溯源与版本追踪。

| 引擎 | 仓库 | Stars | 能力 | 类别 |
|---|---|---|---|---|
| ManimGL | 3b1b/manim | 95528 | 3b1b 原版数学动画引擎 | 科普 |
| ManimCE | ManimCommunity/manim | 41786 | 社区版 Manim，文档全 | 科普 |
| Remotion | remotion-dev/remotion | 66390 | React 编程化视频（注意商业许可） | 商业 |
| Vizzu | vizzuhq/vizzu-lib | 2043 | 动画数据可视化 | 科普 |
| anichart.js | Jannchie/anichart.js | 1131 | 动态排名数据视频 | 科普 |
| Lottie | airbnb/lottie | 4959 | AE 动画跨平台渲染标准 | 商业 |
| yt-dlp | yt-dlp/yt-dlp | 200470 | 多平台视频下载 | 其他 |
| Whisper | openai/whisper | 111088 | 语音识别/字幕转写 | 其他 |
| pyJianYingDraft | GuanYixuan/pyJianYingDraft | 4642 | Python 剪映草稿自动化 | 其他 |
| capcut-cli | renezander030/capcut-cli | 936 | 剪映/CapCut CLI | 其他 |

## 3. 维护规则

1. **新增条目必须实证**：GitHub API 确认仓库存在 + SKILL.md 实体 + 记录 stars，三个都过才进 `data/curated-catalog.json`，并在本表同步一行
2. **季度复核**：每季度核对 stars/最近 commit，僵死项目（≥12 个月无推送）标注替代候选后下架
3. **本地命中优先于目录**：本地技能得分 ≥ 25 即判本地命中，不装目录技能（避免重复安装）；低于 25 才走目录/外部发现。此规则由 match_skill.py 的双阈值逻辑（本地 25 / 外部 35）保证
4. **目录不追星**：收录看「能不能直接出片」，不追新追热；stars 仅作参考权重

## 4. 版本记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v2.0.0 | 2026-10-23 | 创建内置精选目录：11 个实证技能包（3 类别）+ 11 个引擎库；明确实证标准与维护规则 | 桂皮 |
