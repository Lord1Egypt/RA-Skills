# rfc-writer

## 功能说明
这个 skill 旨在扮演一位资深的架构师或 Staff Engineer。当你有一个模糊的技术想法、或者面临一个需要向团队证明的架构重构时，你只需要提供简单的几句话描述，它就能为你扩写、润色并生成一份标准、专业的 **技术提案 (RFC, Request for Comments)**。

它会自动帮你补全：
- 系统的**背景 (Background)** 和 核心的**问题陈述 (Problem Statement)**。
- 详细的**技术方案 (Proposed Solution)** 及其优缺点分析。
- 极具说服力的**替代方案考量 (Alternatives Considered)**（如果你没想好，Agent 会自动帮你发散思维提出替代方案并给出为何不用的理由）。
- 需要团队进一步讨论的**未决问题 (Unresolved Questions)**。
- 支持中英双语输出，会根据用户的提问语言自动适配。

## 使用场景
当你准备在团队内部推动一项技术改造（如：从 Webpack 迁移到 Vite、引入 Redis 缓存、更改数据库表结构），或者在开源社区提交一个重大的 Feature Proposal 时。

## 提问示例

**中文模式：**
```text
写一个 RFC：我们现在的发验证码接口太容易被刷了，我打算加一个 Redis 限流，同一个 IP 1分钟只能发1次
```

**英文模式：**
```text
Draft a technical proposal to migrate our frontend from Webpack to Vite to speed up the dev server.
```