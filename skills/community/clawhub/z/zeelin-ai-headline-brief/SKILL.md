---
name: ZeeLin AI头部简讯
description: "AI领域高质量信息聚合与过滤 skill。当用户要求获取AI领域最新动态、前沿论文、热门工具、行业趋势时触发。覆盖AIGC（文本/图像/视频生成）、虚拟数字人、AI短视频/短剧制作工具、智能传播/舆情/新闻学AI应用四大领域。自动从 arXiv、GitHub、Hacker News、Hugging Face 四大信息源抓取、过滤、评分并生成全球AI中文简报。支持每日快讯和每周深度总结两种输出模式。当用户说‘AI周报’‘本周AI有什么新进展’‘帮我追踪AI前沿信息简报’等类似表述时使用此 skill。"
---

# AI Breathing — 智能时代的信息呼吸术

## 核心理念

互联网上 80% 的 AI 资讯是噪音——标题党、重复包装、过度炒作。本 skill 的目标是：**只吸入有氧信息，过滤掉二氧化碳**。

## 工作流程

### Step 1：明确本次任务模式

用户触发时，先确认输出模式：

| 模式 | 触发词 | 输出 |
|------|--------|------|
| **每日快讯** | “今天AI有什么”“日报”“快讯” | 5-8 条精选，每条一句话摘要 + 链接 |
| **每周深度** | “周报”“本周总结”“AI breathing” | 分层结构化报告（见下方模板） |

### Step 2：按优先级采集四大信息源

按以下优先级依次采集，每个源使用 web_search 抓取最新内容：

#### 🥇 优先级 1：arXiv 论文（学术前沿）

**搜索策略：**
```
搜索关键词组合（每次选 2-3 组）：
- AIGC 方向：site:arxiv.org "video generation" OR "text-to-video" OR "image generation" [本周]
- 数字人方向：site:arxiv.org "digital human" OR "talking head" OR "avatar" [本周]
- 传播学方向：site:arxiv.org "AI narrative" OR "AI journalism" OR "computational propaganda" [本周]
- 短视频方向：site:arxiv.org "short video" OR "short-form video" OR "AI editing" [本周]
```

**筛选标准（满足 2 项即入选）：**
- 出自头部机构：OpenAI、Anthropic、Google DeepMind、Meta FAIR、清华、北大、中科院
- 有开源代码或在线 demo
- 被 3 个以上科技媒体/博主转发讨论
- 提出了新的 benchmark 或数据集
- 直接关联用户四大核心领域

**排除标准（命中 1 项即排除）：**
- 标题含 “A Survey of”“A Review of” 但无新见解的综述
- 纯理论证明、无实验验证
- 与用户四大领域无关的纯 NLP/CV 基础研究

#### 🥈 优先级 2：GitHub 热门仓库

**搜索策略：**
```
搜索关键词：
- github trending AI video generation [本周]
- github stars AIGC tools [本周]
- github "digital human" OR "avatar" new repo
- github AI short video editing tool
```

**筛选标准：**
- 本周 star 增量 > 500（或新仓库 3 天内 star > 200）
- 有完整 README 和可运行 demo
- 与用户四大核心领域直接相关
- 优先关注：视频生成工具、数字人框架、AI 剪辑工具、舆情分析工具

**评分公式：**
```
信息价值 = star增速权重(40%) + 实用性权重(30%) + 领域相关性权重(30%)
```

#### 🥉 优先级 3：Hacker News / Reddit

**搜索策略：**
```
搜索关键词：
- site:news.ycombinator.com AI video OR AIGC OR "digital human" [本周]
- site:reddit.com/r/MachineLearning AI video generation [本周]
- site:reddit.com/r/StableDiffusion [本周热门]
```

**筛选标准：**
- HN: points > 100 且 comments > 30（评论深度比点赞更重要）
- Reddit: upvotes > 500 或被多个子版块交叉讨论
- 排除：纯观点争论无信息增量的帖子、招聘帖、自我推广帖

#### 🏅 优先级 4：Hugging Face

**搜索策略：**
```
搜索关键词：
- site:huggingface.co new model video generation [本周]
- site:huggingface.co trending spaces AI
- huggingface "digital human" OR "avatar" model [最新]
```

**筛选标准：**
- 本周下载量增速 top 20 的模型（与领域相关的）
- 新上线的 Space 且试用人数快速增长
- 与用户研究方向直接相关的数据集发布

### Step 3：信噪比评估

对每条采集到的信息，进行三级信噪比评估：

| 等级 | 标准 | 处理 |
|------|------|------|
| 🔴 **噪音** | 标题党、旧闻重包装、无实质内容、"将改变世界"类空话 | 直接过滤，不出现在简报中 |
| 🟡 **背景** | 有一定信息量但非突破性、行业常规更新 | 仅在每周报告“背景扫描”中简要提及 |
| 🟢 **信号** | 真正的新工具/新方法/新数据、对用户研究或教学有直接价值 | 进入核心简报，附详细摘要 |

**噪音识别关键词黑名单：**
```
"will change everything", "mind-blowing", "game-changer", "天塌了",
"颠覆性", "史诗级", "重磅", "炸裂", "王炸", "刚刚",
"你还不知道？", "看完我沉默了", "XX已死"
```

遇到这些词汇时提高警惕，但不机械过滤——如果内容本身确实有干货，仍然保留。

### Step 4：生成输出

#### 每日快讯模板

```markdown
# 🫁 AI Breathing 每日快讯｜[日期]

## 今日信号（[N]条）

1. **[标题]** — [一句话摘要，说清楚"是什么+为什么重要"]
 - 来源：[arXiv/GitHub/HN/HF] ｜ 领域：[AIGC/数字人/短视频工具/智能传播]
 - 链接：[URL]

2. ...

## 背景扫描
- [一句话提及2-3条非核心但值得知道的动态]

---
> 信噪比：今日扫描[X]条信息，过滤[Y]条噪音，保留[Z]条信号。
```

#### 每周深度总结模板

```markdown
# 🫁 AI Breathing 周报｜[日期范围]

## 📌 本周必读（3-5条）
[真正的突破性进展，每条200-300字深度摘要]

### 1. [标题]
- **是什么**：[技术/工具/论文的核心内容]
- **为什么重要**：[对领域的影响，与用户研究方向的关联]
- **可行动项**：[用户可以做什么——试用、引用、关注后续]
- 来源 & 链接：[...]

### 2. ...

## 📋 值得关注（5-10条）
[有实用价值但非突破性的工具/论文/动态，每条1-2句]

## 📊 本周趋势洞察
[基于本周信息的1-2段趋势分析，关联用户的四大核心领域]

## 🔇 噪音过滤清单
[本周被过滤的3-5条热门但实际信息量低的内容，附过滤原因]
> 让用户知道自己没错过什么，同时理解为什么这些被过滤了

---
> 本周扫描：[X]条信息 → 过滤[Y]条噪音 → 保留[Z]条信号
> 信噪比：[Z/X * 100]%
```

## 用户四大核心领域定义

在采集和筛选时，用以下定义判断相关性：

| 领域 | 关键词 | 关注重点 |
|------|--------|----------|
| **AIGC/生成式AI** | text-to-video, image generation, Sora, Seedance, Kling, Runway, 可灵, 文生视频 | 新模型发布、生成质量突破、开源工具 |
| **虚拟数字人** | digital human, talking head, avatar, 数字人, 虚拟主播, 数字分身 | 驱动技术、表情/动作合成、实时交互 |
| **AI短视频/短剧工具** | AI editing, short video, 剪映AI, AI漫剧, AI短剧, AI动画 | 制作工具更新、工作流优化、产业数据 |
| **智能传播/舆情** | AI journalism, computational propaganda, 舆情分析, AI新闻, 算法推荐 | 学术论文、治理政策、平台算法变化 |

## 使用示例

**用户说**：“帮我看看这周AI领域有什么值得关注的”
**触发**：每周深度模式 → 执行完整 4 步流程 → 输出周报

**用户说**：“今天有什么AI新闻”
**触发**：每日快讯模式 → 快速扫描 4 个源 → 输出 5-8 条精选

**用户说**：“最近有没有新的视频生成模型”
**触发**：聚焦 AIGC 领域 → 重点搜索 arXiv 和 GitHub → 输出专题简报

## 注意事项

1. **中文输出为主**：所有摘要和分析用中文撰写，论文/仓库标题保留英文原文
2. **标注信息源**：每条信息必须标注来源和原始链接
3. **不编造信息**：如果某个源本周无相关高质量内容，如实说明，不凑数
4. **关联用户研究**：在每周报告的趋势洞察中，主动关联用户的学术研究方向（AIGC叙事理论、AI短视频传播、虚拟数字人应用等）
5. **累积记忆**：如果用户持续使用，注意追踪前几周提到的项目/论文的后续进展
