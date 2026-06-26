# Toutiao Draft Automation

本目录包含了用于辅助用户将生成的 Markdown 内容填入今日头条创作者平台的 Playwright 脚本说明和安全规则。

## 核心理念：Human-in-the-loop

由于平台风控、Cookie 时效以及账号安全要求，本自动化工具**绝对不是**自动发布机。

它的唯一功能是：**代替你的双手，在可见浏览器中把本地生成的草稿粘贴进浏览器文本框里。**

## 包含内容

- `playwright_draft_flow.md`: 脚本的执行逻辑和页面流转过程说明。
- `safety_rules.md`: 自动化脚本必须遵守的安全与合规边界。
