---
name: solution-research
description: Use when choosing solutions, including selecting open-source projects, working around issues, and comparing products.
---

## Solution-Research

_一言概之：工程师思维_

- ”找谁解决过“，而不是”我来做这个“
  - 不重复造轮子——方向比一味地努力更重要。无论干什么，你要干的事情别人肯定尝试过了
- 深度优先于速度，表面答案最危险
- 硬数据帮助我们辨别筛选。而”新鲜度（时效性）“和”可持续性“是两大巨擎，缺一不可
  - 十余star、百余下载，基本都是垃圾
- 新讨论>老公告、务实>哲学

## 流程

_加载这个 Skill，说明你 现在 就需要跟着这个 Skill 的工作流来走_

将以下三个阶段、以及每个项目的分析随时通过 todo list 进行记录，这样你不会迷失

### 阶段一：广泛调研

用英文多轮并发搜：不同关键词、不同深度（最新 vs 全面）、精确短语与宽泛术语混用

深入所有信息源以获得最全面的图景
- Reddit
- Github Issue
- 官方 Blog
- 官方论坛

### 阶段二：捕获 Vibe

基于阶段一的发现，**追加**深度 fetch 和搜索，逐个考虑以下信息：

1. 数据
  - GitHub stars
  - 下载量安装量
  - 涉及的讨论数量、Comment 的 reaction 数量

2. 已经被 Track？某人已经 working on it？
  - 具体的场景、边界，或者报错信息
    - 和我们的场景有何区别？
  - 讨论的态势
    - 在何处被 Track，是否真的有跟进
    - 最早的 Issue，多个 Issue 之间的关系
    - 每条 Comment 的 reaction、like/dislike
    - Git Commits History 变化趋势
    - 特定英雄个体的影响
    - 是否有随时间、情况的变化“故事”？

3. 新鲜度（时效性）
    - issue/threads 最新更新时间
    - 搜索索引，页面明确标注的时间

> 特定版本会有特定问题。不同版本的软件，配置使用完全迥异
> 例如在 LLM/AI 领域，超过 12 小时的信息可能就已过时

4. 代码真实质量
- 默认 README 吹的天花乱坠全是假的
- git clone 下源码，找它落地、release、ship 在哪，是不是堆满 ai slop 的空架子
- 什么语言、什么框架、多轻便多务实才是硬道理
- 证据
  - Issue、PR 列表
  - V2EX、Hacker News 趋势

5. Workaround 与兼容性检查
- 集成成本：采用它还需连带改动什么
- 已知 bug、blocker
- 如相关，检查 Atomic Linux 是否适用

6. 可持续性
  - 历来的长期活跃度（Commits History）
  - 维护者是谁，钱从哪来
    - CNCF、Linux Foundation、Red Hat 大厂是完美
    - 抑或是印度高中生？还是正规融资企业？
    - 要用户付费？如果是这样，那免费配额怎么算？
  - 谁在生产环境用它

> 一个项目，能解决问题，但是上周刚出，12 stars。那就没有用它的意义了
> 若确有意义，那宁可提取方案中的精髓，自己集成自己维护

记住只做 web search 不完整，扫搜索摘要，断章取义不能当真相
关键是深入：
命中即 fetch 全文爬整楼，读 PDF，用 gh cli 追 issue/PR threads, yt-dlp skill 分析任何视频内容等
不要担心上下文大小
- 每条评论全部加载遍历就是美
- 搜集范围又大又全就是美

### 阶段三：下一步

#### 如果进行汇报

上述所输出的信息，仅为研究过程的副产物
**不 是**能交付的汇报：可交付的汇报是给人看的

### 认真对待

> ”这问题很简单直接，用户给的情景不相干，不必跟随此流程走，现在足以得出结论“
> “当前信息已经非常丰富，如果有更多时间，可以再进行后续研究”

这样想法是完全错误的，你需要 one-shot 给出 deepest 的交付

因此：
1. 以上全部流程，全部信息获取： **必须**一个不落逐个完成
2. **汇报必须可交付，必须完整呈现**
3. 附上证据：链接、来源、原文
