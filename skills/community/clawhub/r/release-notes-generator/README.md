# release-notes

## 功能说明
这个 skill 旨在根据用户提供的纯文本 Commit 记录，自动提取、清洗并生成一份结构化、面向用户的发版说明（Release Notes / Changelog）。它可以：
- 将杂乱的 Commit 日志提炼并严格分类为：**💥 Breaking Changes (破坏性变更)**、**✨ Features (新特性)**、**🐛 Bug Fixes (问题修复)**。
- 自动过滤掉对最终用户无意义的噪音提交（如简单的 typo 修复、内部重构、测试用例更新等）。
- 支持中英双语输出，会根据用户的提问语言自动适配。
- **安全说明**：为了防止间接提示词注入（Indirect Prompt Injection）等安全风险，此 Skill 不会自动访问外部链接，用户需要直接提供 Commit 记录文本内容。

## 使用场景
在项目发版前，你需要撰写给用户或社区看的 Release Notes，但面对长串的 git log 感到无从下手时，使用这个 skill 可以一键生成排版精美的发版公告。

## 提问示例

**中文模式：**
```text
帮我根据以下 commit 记录生成一份中文的发版说明：
feat(auth): 新增企业微信登录
fix(db): 修复并发导致的数据死锁
chore: 更新 README.md
BREAKING CHANGE: 移除 v1 版本的 API 接口
```

**英文模式：**
```text
Generate a changelog for these commits:
feat: add dark mode support
fix: resolve memory leak in worker thread
docs: update installation guide
```