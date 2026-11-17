# Agent 参考索引

本目录只是 Agent **运行、编排、调用** skill 时可渐进加载的资料索引，**不是**用户市场说明。

**边界规则：**

- 本文**不得**包含 YAML frontmatter，**不得**包含 `description` 字段。
- 技能市场详情与普通用户说明**必须**放在根目录 [`README.md`](../README.md)。
- 本目录只保留运行时引用资料（如 `CLI.md`、`SCHEMA.md`）；开发规范放在 [`../development/`](../development/)。

| 文档 | 用途 |
|------|------|
| 根目录 [`README.md`](../README.md) | 用户市场详情页说明 |
| [`SKILL.md`](../SKILL.md) | LLM / OpenClaw 平台技能入口 |
| [`CLI.md`](CLI.md) | 命令行入口、参数与调用契约 |
| [`SCHEMA.md`](SCHEMA.md) | 输入输出、数据库与字段说明 |
| [`../development/`](../development/) | 开发、测试、技术规范（给开发者 / AI 编程代理） |

按需阅读：编排任务时优先 `CLI.md`；解析结构化字段时读 `SCHEMA.md`；运行时环境细节见 `../development/RUNTIME.md`。
