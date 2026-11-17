# 开发资料入口

本目录面向**人类开发者**与 **AI 编程代理**。开始定制 skill 前，建议按以下顺序阅读：

1. [`REQUIREMENTS.md`](REQUIREMENTS.md) — 需求文档模板与验收标准
2. [`NAMING.md`](NAMING.md) — slug / 仓库名命名规范（复制模板前必读）
3. [`DEVELOPMENT.md`](DEVELOPMENT.md) — 完整开发步骤与目录规范
4. [`TESTING.md`](TESTING.md) — 测试分层、隔离数据根与档位开关
5. [`ADAPTER.md`](ADAPTER.md) — 涉及外部系统对接时
6. [`RPA.md`](RPA.md) — 涉及浏览器 / 桌面 / 手机自动化时
7. [`CONFIG.md`](CONFIG.md) — `.env` 规范与 bootstrap 机制
8. [`RUNTIME.md`](RUNTIME.md) — 共享 runtime、数据路径、发布打包与编码约定

脚手架与 Git 防串库：[`../tools/README.md`](../tools/README.md)（`scaffold_skill.ps1`）。

Agent 调用契约见 [`../references/CLI.md`](../references/CLI.md)、[`../references/SCHEMA.md`](../references/SCHEMA.md)。  
用户市场说明见根目录 [`README.md`](../README.md)，不要写进本目录。
