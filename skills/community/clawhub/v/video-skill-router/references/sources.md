# 外部渠道清单（sources.md）

## 1. GitHub 渠道

### 1.1 仓库搜索（search_anim.py 自动执行）

API：`https://api.github.com/search/repositories`

按类别选 topic（`--category` 触发，词表见 `categories.md` 第 2 节）：

| 类别 | topic 组 | 检索词模板 |
|---|---|---|
| 商业宣传类 | `motion-design`、`motion-graphics`、`lottie`、`lottiefiles`、`remotion`、`advertising` | `promo video skill`、`ad video generator`、`product demo animation` |
| 知识科普类 | `manim`、`manimgl`、`3blue1brown`、`data-visualization` | `manim animation skill`、`math animation agent`、`data visualization animation` |
| 其他类 | `video-editing`、`ffmpeg`、`subtitle`、`video` | `video editing skill`、`ffmpeg automation`、`subtitle generator` |

排序 `stars desc`，每类检索 ≤ 4 次（尊重 10 req/min 未认证限额），自动去重。

### 1.2 技能发现（搜别人写好的 SKILL.md）

API：`https://api.github.com/search/code`，查询式：

```
filename:SKILL.md animation in:file
filename:SKILL.md manim in:file
filename:SKILL.md video animation in:file
```

注意：code search **需要登录 token**，无 token 时静默降级为仓库搜索（不报错中断）。本机无 token，实际靠 1.1 + 关键词搜索发现技能包（2026-10-23 实测有效：`manim agent skill`、`video editing agent skills`、`remotion skill agent` 等关键词搜索直接命中了 manim_skill / herk-edit-kit / video-talkcraft）。

### 1.3 Awesome 列表（高信号源）

- `github.com/frankxai/awesome-motion-design-agent-skills`（动效 agent 技能精选，已入内置目录）
- `github.com/topics/manim`（Manim 生态合集）
- `github.com/airbnb/lottie`（Lottie 官方）

### 1.4 网络搜索通道（编排层执行，不走脚本）

用 WebSearch 工具补搜（三级渠道，仅在前两级零命中时用）：

- 「<类别典型场景> video skill github 2026」
- 「awesome <场景> animation」
- 「<场景> video generator AI agent」

**发现回落规则**：WebSearch 找到的仓库，必须再走 GitHub API 验证存在性与 SKILL.md 实体才能进候选（防幻觉链接）。

## 2. 代理探测规则（重要，本机环境）

本机 bash 环境注入的随机代理端口多为死端口，真实代理恒为 `http://127.0.0.1:7897`。脚本按以下顺序探测，全部失败才报网络错误：

1. 直连（无代理）
2. `http://127.0.0.1:7897`
3. 环境变量 `HTTPS_PROXY` / `https_proxy`

git clone 走子进程时同样剥离 `*_proxy` 环境变量（死端口会让 clone 假超时）。

## 3. 候选来源优先级

1. 已有一定 stars（>50）的活跃仓库
2. 明确含 SKILL.md 的技能包（可直接安装）
3. awesome 列表收录的工具库（通常需包装成技能后才可安装）
4. 个人仓库/新仓库：仅在无更优候选时纳入，报告中标注低置信度

## 4. GitHub 候选池（2026-10-23 三轮实测收录）

### 4.1 已入内置精选目录的技能包（一级渠道，优先用）

见 `catalog.md` 第 1 节，共 11 个：motion-design-skill / video-talkcraft / OpenMontage / ad-video-skills / ai-shorts-generator / awesome-motion-design-agent-skills / manim_skill / MathLens / herk-edit-kit / FireRed-OpenStoryline / baocut。

### 4.2 实证存在但不可直装（备查，不进目录）

| 仓库 | Stars | 核实结论 |
|---|---|---|
| https://github.com/Wing900/ManimCat | 476 | 无 SKILL.md，是「自然语言→Manim 动画」库，需包装成技能才能装 |
| https://github.com/iart-ai/motion-skills | 967 | 描述称「50 open-source skills」，但仓库内无 SKILL.md 实体，不可直装 |
| https://github.com/visser23/promo-video-generator | 30 | 工具集非技能包，无 SKILL.md |
| https://github.com/krillinai/OpenCreator | 13835 | 视频翻译配音工具（ KrillinAI ），非技能包 |
| https://github.com/GuanYixuan/pyJianYingDraft | 4642 | Python 库（剪映草稿），已入 catalog engines 区 |
| https://github.com/renezander030/capcut-cli | 936 | CLI 工具，已入 catalog engines 区 |

### 4.3 引擎库（需包装成技能后才能 install）

见 `catalog.md` 第 2 节，共 11 个（Manim 系 / Remotion / Vizzu / anichart / Lottie / yt-dlp / Whisper / 剪映系）。

### 4.4 本地已覆盖（Kyle 环境，不推荐重复安装）

ManimCommunity/manim、3b1b/manim、FFmpeg/FFmpeg、remotion-dev/remotion、openai/whisper、SYSTRAN/faster-whisper——本地技能已基于这些基座，见 `repos.md` 第 1 节。

## 5. 版本记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v1.0 | 2026-10-23 | 创建渠道清单：GitHub 搜索语法、topic 词表、代理探测规则 | 桂皮 |
| v1.1 | 2026-10-23 | 新增候选池：4 个可直装 skills 包 + 7 个引擎库 | 桂皮 |
| v2.0.0 | 2026-10-23 | 按类别重组渠道矩阵；候选池扩至 11 技能包 + 11 引擎（三轮实测）；补记 6 个实证不可直装仓库；修正 code search 需 token 的说明 | 桂皮 |
