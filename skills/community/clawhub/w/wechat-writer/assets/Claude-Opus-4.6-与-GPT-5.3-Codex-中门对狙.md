# Claude Opus 4.6 与 GPT-5.3 Codex：中门对狙的一天

在全网翘首以盼的等了两天之后，在凌晨 2 点，Anthropic 的新模型 Claude Opus 4.6 正式更新了。我说实话，我是真的最近因为 AI 圈这些模型和产品，熬夜熬的有点扛不住了。但其实最颠最绝望的是，20 分钟之后，OpenAI 也发了新模型。GPT 5.3 Codex 也来了。这尼玛，真的是中门对狙了。要了亲命了。

这两模型都还是得看，因为之前 GPT 和 Claude 几乎就是我最常用的两个主力模型：GPT-5.2 用来做各种各样的搜索和事实核查，还有研究还有编程改 bug；Opus 4.5 做创作和主力编程。现在两个都来了。太刺激了。一个一个说。

## 一. Claude Opus 4.6

这次 Anthropic 不止发了 Claude Opus 4.6，还有 Agent Teams，以及 Excel 和 PowerPoint 插件的更新。

每次有新模型发布，大家第一反应就是看跑分。这次 Opus 4.6 的跑分确实很漂亮：

- Terminal-Bench 2.0：65.4%
- OSWorld：72.7%
- BrowseComp：84.0%
- GDPval-AA：Elo 1606
- ARC AGI 2：68.8%

我对跑分一直有点复杂。一方面跑分确实能说明一些问题，但跑分和实际体验之间，往往有一道很深的鸿沟。所以我更关注的是产品层面的变化。

### 1）1M token 上下文窗口

普天同庆。Claude Opus 系列终于有 1M 上下文了。之前只有 200K，这次整整翻了 5 倍。做 coding 的朋友都知道上下文容量有多重要。

但上下文大，不等于能用好。很多模型长上下文会出现 context rot，用得越久越蠢。这里他们用 MRCR v2 做了“大海捞针”测试：100 万 token、藏 8 根针，Opus 4.6 拿了 76%。

### 2）输出上限提升到 128K

以前 Claude 输出上限是 64K，这次翻倍。听起来不起眼，但对实际交付物很重要。

### 3）Context Compaction（上下文压缩）

对话很长、任务很长时，Claude 可以自动把旧内容压缩成摘要，腾出空间给新内容，让长任务不因为上下文溢出而中断。

### 4）Adaptive Thinking 与 Effort 控制

以前 extended thinking 要么开要么关。现在：

- Adaptive Thinking：让 Claude 自己判断要不要深度思考
- Effort 控制：low / medium / high / max，默认 high

这样能在速度、成本、质量之间更灵活地平衡。

### 5）Agent Teams

以前是一个 Claude 干活，现在可以组队：一个会话当负责人，启动多个团队成员并行工作（比如前端 / 后端 / 数据库各看一遍），成员之间还可以相互沟通、相互质疑、共享发现。

### 6）Claude in Excel / PowerPoint

Claude 集成到 Excel，支持数据透视表、图表、条件格式、排序筛选等；也集成到 PowerPoint 侧边栏，能读取现有布局、字体和母版，按模板生成或编辑幻灯片。

价格方面，API 价格不变：输入/输出 $5/$25 每百万 token。超过 20 万 token 上下文有额外定价。

## 二. GPT-5.3 Codex

GPT-5.3 Codex 的更新我也很开心。我自己经常的工作流是：Claude Code 写一个大的，然后用 Codex 接手后续精准调整、改 bug。

这次最让我惊讶的，不是跑分，是他们博客里的一句话：GPT-5.3 Codex 是他们第一个在创造自己的过程中发挥重要作用的模型。用早期版本来 debug 训练过程、管理部署、诊断测试结果和评估。AI 参与了自己的开发。

老规矩看跑分。可比性很难完全对齐，但 Terminal-Bench 2.0 这个相同基准里：

- Claude Opus 4.6：65.4%
- GPT-5.3 Codex：77.3%

OSWorld 这块，两家的分数用的是不同版本（OSWorld vs OSWorld-Verified），不能直接拉通比较。SWE-bench 也是类似：Verified 与 Pro Public 难度与覆盖范围不一样，分数不能直接对比。

OpenAI 还展示了两个用 GPT-5.3 Codex 做的完整可玩游戏（赛车、潜水），不是简单 demo。并且 Codex 工作时你可以随时介入互动、调整方向，不用先停掉。

另外一个很关键的更新：在 Codex 上运行 GPT-5.3 Codex 直观感觉快了很多。奥特曼在 X 上提到：完成相同任务所需的令牌数不到 5.2-Codex 的一半，且单令牌速度快 25% 以上。

## 写在最后

这篇稿子又写了个通宵，基本把我对这两个模型的理解都写进去了。至于实际测试，这么一点时间实在测不出来。可能得正儿八经开发几个产品，才能感受到差异。

但有一点很明确：现在的模型几乎都是奔着 coding 和 agent 去的，用新不用旧。

直觉上我的工作流还是不太会变：Claude Opus 4.6 + Claude Code 打草稿，GPT-5.3 Codex + Codex 做后续精准开发。

原文：https://mp.weixin.qq.com/s/TUPekE8KbnefLdPfBtstlA
