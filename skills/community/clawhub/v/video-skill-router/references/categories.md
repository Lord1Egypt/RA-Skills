# 视频类别 → 渠道矩阵（categories.md）

本文件是「按视频类别去不同渠道下载技能」的决策依据。类别判定在 SKILL.md Step 1 完成，本文件给出每个类别的完整渠道矩阵与典型链路。

## 1. 类别判定关键词（完整版）

### 商业宣传类（commercial）

产品、宣传、广告、电商、带货、促销、品牌、发布会、演示、营销、推广、商品、种草、带货视频、企业宣传、promo、product、ad、advertising、marketing、brand、launch、testimonial

### 知识科普类（education）

知识、科普、教学、课程、数学、公式、数据、图表、讲解、科学、历史、地理、教程、学习、题、课件、math、science、education、tutorial、explain、data-visualization

### 其他类（general）

vlog、日常、创意、短片、口播、混剪、旅拍、毕业、纪念、婚礼、活动、字幕、配音、剪辑、切片、vlog、daily、edit、editing、subtitle

**判定规则**：命中数多者胜；并列时 商业 > 科普 > 其他（取更具体的）；用户显式指定类别时以用户为准。无法判定时归「其他类」并在报告中说明。

## 2. 完整渠道矩阵

### 2.1 商业宣传类

| 渠道级 | 渠道 | 具体内容 | 成本 |
|---|---|---|---|
| 一级 | 内置精选目录 | category=commercial 技能包：motion-design-skill（Lottie 官方动效）、video-talkcraft（动效工作室）、OpenMontage（agentic 视频生产系统，含 ai-video-gen）、ad-video-skills（广告模板 A/B）、ai-shorts-generator（促销短视频）、awesome-motion-design-agent-skills（精选清单） | 零网络 |
| 二级 | GitHub 实时搜索 | topic: `motion-design`、`motion-graphics`、`lottie`、`lottiefiles`、`remotion`、`advertising`；检索词模板：`promo video skill`、`ad video generator`、`product demo animation` | 1 次 API/渠道 |
| 三级 | 网络搜索 | 「product promo video generator github」「ad video template AI agent 2026」「awesome motion design」 | WebSearch |

已装剪映/CapCut：可加搜「剪映 模板 自动化」方向（pyJianYingDraft / capcut-cli 在 catalog engines 区）。

### 2.2 知识科普类

| 渠道级 | 渠道 | 具体内容 | 成本 |
|---|---|---|---|
| 一级 | 内置精选目录 | category=education 技能包：manim_skill（三技能：composer + CE/GL 最佳实践）、MathLens（数学题讲解） | 零网络 |
| 二级 | GitHub 实时搜索 | topic: `manim`、`manimgl`、`3blue1brown`、`data-visualization`；检索词模板：`manim animation skill`、`math animation agent`、`data visualization animation` | 1 次 API/渠道 |
| 三级 | 网络搜索 | 「manim animation tutorial」「awesome manim」「math video generator AI」 | WebSearch |

### 2.3 其他类

| 渠道级 | 渠道 | 具体内容 | 成本 |
|---|---|---|---|
| 一级 | 内置精选目录 | category=general 技能包：herk-edit-kit（15 个剪辑技能）、FireRed-OpenStoryline（文字出片）、baocut（时间轴剪辑 agent） | 零网络 |
| 二级 | GitHub 实时搜索 | topic: `video-editing`、`ffmpeg`、`subtitle`、`video`；检索词模板：`video editing skill`、`ffmpeg automation`、`subtitle generator` | 1 次 API/渠道 |
| 三级 | 网络搜索 | 「ai video editing skill」「ffmpeg video automation 2026」 | WebSearch |

## 3. 各类别典型链路（需求 → 技能 → 输出）

### 商业宣传类

```
用户：「给我的 APP 做个 30 秒产品演示」
→ 类别：commercial
→ 一级目录命中 video-talkcraft / motion-design-skill
→ 安装 → 执行（截图/文案 → Remotion/Lottie 动效 → mp4）
→ 输出：video-output/2026-10-23-app-demo/app-demo-30s.mp4
```

素材缺失时的降级：无截图 → 用技能自带占位模板；无文案 → 让用户补三句话（卖点/人群/行动号召）。

### 知识科普类

```
用户：「把勾股定理的证明做成讲解动画」
→ 类别：education
→ 一级目录命中 manim_skill（manim-composer）
→ 安装 → 执行（讲稿 → Scene 代码 → 渲染 mp4）
→ 输出：video-output/2026-10-23-pythagoras/pythagoras-proof.mp4
```

数学公式刚需：LaTeX + ManimCE；只要 3B1B 风格视觉 → ManimGL 分支。manim_skill 包内三个技能按需取（--subdir）。

### 其他类

```
用户：「这段口播素材帮我剪掉口误和静音」
→ 类别：general
→ 一级目录命中 herk-edit-kit（cut-mistakes + cut-silences）
→ 安装（--subdir 或 --all-skills）→ 执行（转写 → 定位 → 剪切 → mp4）
→ 输出：video-output/2026-10-23-koubo-edit/koubo-clean.mp4
```

已装剪映的用户：优先 pyJianYingDraft 方向（草稿级自动化，保留剪映后期空间）。

## 4. 渠道选择规则

1. **一级目录永远先查**：11 个技能包全部经过 2026-10-23 实证（仓库存在 + SKILL.md 实体 + stars 实测），命中即装，不等网络
2. **二级搜索按类别走**：不同类别的 topic 与检索词不同，不混用（商业类去 motion-design 淘，科普类去 manim 淘）
3. **三级网络兜底**：只在前两级零命中时用，且结果必须回落二级复核（WebSearch 发现的仓库仍要过 GitHub API 验证存在性与 SKILL.md）
4. **每级至少 2 候选**：首选失败（校验拒/执行挂）时能立刻降级，不回到起点

## 5. 版本记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v2.0.0 | 2026-10-23 | 创建类别渠道矩阵：三类别 × 三级渠道，含完整关键词表、topic 词表、检索词模板与典型链路 | 桂皮 |
