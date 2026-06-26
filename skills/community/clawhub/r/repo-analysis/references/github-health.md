# Lightweight GitHub health layer

仅作为仓库分析的补充层，不替代代码证据。

## 什么时候启用

满足以下条件再启用：
- 目标是公共 GitHub 仓库
- 用户在问项目是否值得关注、采用、参考、二开

如果只是单纯“读一下代码”，默认不启用。

## 看哪些信号

### 基础健康度
- stars
- forks
- license
- 最近一次 commit 时间
- 是否有 release，release 是否持续

### 维护信号
- issue 是否仍有近期活动
- PR 是否仍在流动
- maintainer 是否有明显参与

### 文档信号
- README 是否不只是 marketing
- 是否有 CONTRIBUTING / docs / examples

## 输出约束

- 保持简短
- 只补一个“GitHub 健康度补充”短块
- 不能把回答带偏成社区情报报告
- 不能让 stars / hype 压过代码和结构事实

## 推荐写法

### GitHub 健康度补充
- **基础信号**：stars / forks / license / 最近 commit / release 节奏
- **维护状态**：issue / PR 是否仍在流动，维护者是否在场
- **判断**：这些信号对采用或跟进意味着什么

## 不该做的事

- 不默认扩展到大量社区讨论
- 不默认做竞品大战
- 不用热度代替工程判断
- 不把这一段写得比 repo 本身的工程分析还长
