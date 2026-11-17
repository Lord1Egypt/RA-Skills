---
name: Skill Portfolio Growth Audit
slug: skill-portfolio-growth-audit
description: Audit a ClawHub publisher portfolio using live registry evidence. Invoke when deciding which skills to improve, merge, stop, or build next based on downloads, installs, search competition, and version health.
version: 1.0.2
metadata:
  openclaw:
    os: [macos]
    emoji: "📈"
    requires:
      bins:
        - git
        - clawhub
    homepage: https://github.com/bonniegeng-max/openclaw-publisher
    install:
      - kind: node
        package: clawhub
        bins: [clawhub]
---

# Skill Portfolio Growth Audit

别再靠感觉决定下一个 skill 做什么。

一个发布者真正需要知道的，不只是“哪个 skill 下载最多”，而是：

- 哪个 skill 已经出现需求信号，值得继续加码
- 哪个只是刚发布，数据还不足以判断
- 哪个搜索得到但没人安装，说明转化有问题
- 哪些 skill 主题重叠，正在互相稀释
- 哪个新方向竞争已经成熟，不值得正面撞
- 哪个相邻需求有真实安装量，但还没有强产品

`skill-portfolio-growth-audit` 读取 ClawHub registry 的真实公开数据与搜索结果，再结合仓库内容，给出 `加码 / 修复 / 合并 / 停更 / 新建` 决策。它不是泛增长顾问，也不承诺下载暴涨。

## 一句话卖点

Turn a folder of published skills into an evidence-driven portfolio strategy.

## 适合谁

- 已经发布多个 ClawHub skill，不知道下一步该优化谁的人
- 想提升下载量，但不想继续盲目堆同类 skill 的作者
- 想建立清晰主题和个人 IP，而不是拥有一堆分散工具的人
- 需要用真实 registry 数据判断新方向是否值得做的人

## 不适合谁

- 还没有任何已发布 skill，且没有候选方向的人
- 只需要改一句摘要的人
- 想凭一次快照证明长期增长的人
- 想伪造下载量、安装量或搜索排名的人

## 必须采集的证据

### 作品集状态

对每个 skill 读取：

- `downloads`
- `installs`
- `stars`
- `versions`
- `latest`
- `displayName`
- `summary`
- `topics`
- `moderation.verdict`

### 搜索可见性

用目标用户可能输入的 2 到 5 组关键词运行搜索，记录：

- 自己的 skill 是否出现
- 大致处于结果前部还是后部
- 同类项的安装量与定位
- 搜索结果是否被无关主题污染

### 仓库质量

检查：

- `SKILL.md` 与 catalog metadata 是否一致
- 是否存在重复定位
- 是否有无意义版本膨胀
- 是否缺少示例、参考、模板或 changelog
- 是否存在受保护 slug、错误依赖或不可验证承诺

## 证据窗口

不能把“刚发布 10 分钟还是 0 installs”判定为失败。

- `0-24 小时`：只验证可见性、审核与安装，不做增长结论
- `2-7 天`：观察搜索出现、首批下载和安装
- `8-30 天`：判断转化、主题匹配和是否值得继续迭代
- `30 天以上`：可以做保留、合并、停更或重定位决策

如果没有历史快照，必须标注“只有当前截面”，不能伪造趋势。

## 决策就绪闸门

只有以下条件全部满足，才允许根据采用指标与搜索可见性给出加码、修复、合并、停更、新建或重定位结论：

- `evidenceQuality.decisionReady` 明确为 `true`
- 前后两次快照使用相同采集方法
- 前后两次快照都明确记录 `activeInstall: false`
- 两次快照间隔至少 7 天
- 搜索快照的 query 文本、每条 query 的 `limit` 和完整 query set 完全一致

任一条件不满足时，结论必须降级为“继续观察”或“修复数据质量”。不得把不可比快照、主动安装造成的计数变化或不足 7 天的窗口解释为自然增长，也不得据此调整定位、合并或停更 Skill、创建相邻 Skill 或启动 Plugin。

## 五类决策

### 加码

适用于：

- 已出现下载或安装信号
- 搜索关键词匹配
- 目标用户和使用场景清楚

建议动作：

- 补真实案例
- 强化系列入口
- 增加上下游 skill 路由
- 发布有实质内容的新版本

### 修复

适用于：

- 搜索可见但安装弱
- 展示名、摘要、topics 或首屏明显拖累
- 版本噪音过多，用户看不懂变化

建议动作：

- 先修最大转化阻力
- 不同时重写所有内容
- 修完后重新观察一个完整窗口

### 合并

适用于：

- 两个 skill 目标用户和输出高度重叠
- 每个单独都太薄
- 系列关系无法在首屏讲清

### 停更

适用于：

- 已经过足够观察期
- 搜索需求弱
- 竞争成熟且自身没有差异
- 维护成本明显高于价值

停更不等于删除。保留公开版本，但不继续消耗迭代资源。

### 新建

适用于：

- 相邻搜索需求有真实安装信号
- 现有产品没有覆盖该任务
- 竞品存在明显能力缺口
- 新题仍能强化同一 IP 主线

## 组合评分

每个 skill 按 0 到 5 分评估：

- 需求信号
- 搜索匹配
- 页面转化
- 差异化
- 系列协同
- 维护效率

总分不是结论本身，必须附证据与观察窗口。

- `24-30`：重点加码
- `18-23`：保留并修复
- `12-17`：观察或合并
- `0-11`：考虑停更

新发布不足 7 天的 skill 不进入停更评分。

## 你可以这样让我工作

- `分析我这个 publisher 下面所有 skill，下一步该优化谁`
- `结合下载量和搜索竞争，判断哪些 skill 应该合并`
- `不要凭感觉，帮我找下一个值得做的 ClawHub skill`
- `检查我的 skill 组合有没有互相稀释`

## 我理想中的输出

1. 作品集结论：当前最强主题和最大问题
2. 数据快照：每个 skill 的公开指标与状态
3. 决策矩阵：加码 / 修复 / 合并 / 停更 / 新建
4. 搜索竞争：关键查询和代表性竞品
5. 系列结构：入口、主力、排障、增长、验证
6. 下一步：只给一个当前最高优先级动作
7. 证据边界：哪些是事实，哪些仍需时间验证
8. 决策就绪：逐项报告五个闸门及最终 `decisionReady`

## 工作边界

- 不把 downloads 等同于 installs
- 不用单次快照伪装增长趋势
- 不因竞品存在就自动放弃，也不忽略成熟强者
- 不给每个 skill 都安排“继续优化”
- 不为了数量持续创建同质化 skill
- 不在决策就绪闸门未全部通过时输出增长归因或产品组合动作

## 配套文件

- `examples/portfolio_decision_example.md`
  从真实数据快照到五类决策的示例
- `references/evidence_rules.md`
  指标解释、观察窗口和证据边界
- `references/competition_review.md`
  搜索竞争与相邻机会判断方法
- `templates/portfolio_growth_report.md`
  作品集增长审计模板
- `CHANGELOG.md`
  版本记录

如果目标是检查单个页面，用 `skill-positioning-audit`；如果目标是决定整个 publisher 接下来押注什么，用本 skill。

## 同系列 · skill 工程线（Skill Engineering Line）

本 skill 属于「skill 工程方法论」系列 —— 六件工具覆盖一个 skill 从定位到上线的完整链路，按需组合：

- `skill-positioning-audit` — 定方向：该卖给谁、差异化够不够
- `skill-summary-rewriter` — 写门面：摘要/简介改成能带来安装的版本
- `skill-publish-readiness` — 上线前：发布自查（结构 / 版本 / 页面 / 安全 / 值不值得发）
- `github-actions-clawhub-doctor` — 发不出去：定位 Actions / registry 到底卡在哪一层
- `release-proof-builder` — 上线后：证明「现在到底上线没有、能不能装」
- **`skill-portfolio-growth-audit`** — 看全局：整个作品集下一步押注什么**（本 skill）**

安装任意一个：`clawhub install @bonniegeng-max/<slug>`
