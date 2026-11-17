# siluzan-tso — 文档目录

> 入口：`SKILL.md` → 按路由表 Read 列出的文件。改文档结构时对齐 `references/core/skill-authoring.md`。

## 怎么找文档

| 要做什么           | 读哪里                                      |
| ------------------ | ------------------------------------------- |
| 锁定工作流         | `SKILL.md` 路由表                           |
| 报告类话术模糊     | `references/core/intent-routing.md`         |
| 步骤与产物         | `playbooks.md`（P*）或 `workflows.md`（W*） |
| 命令参数 / 字段    | 路由表「必读文档」                          |
| 纪律与对用户怎么说 | `references/core/agent-conventions.md`      |
| 报告结构纲要       | `report-templates/*.md`（勿读 `*.html`）    |
| P10 下期规划怎么写 | `report-templates/google-quarterly-plan.md` |

## 启动顺序

1. Read `SKILL.md` 路由表，锁定唯一工作流
2. 报告类模糊 → Read `intent-routing.md`
3. Read「必读文档」+ 对应 playbook/workflow 卡片
4. 写操作 / 报告交付 / 批量 / 对用户写结论 → Read `agent-conventions.md` 相关节
5. P5/P6/P7 或长 CLI：可选 `subagent-orchestration.md`

## 按域

| 域         | 路径                               | 说明                                                                       |
| ---------- | ---------------------------------- | -------------------------------------------------------------------------- |
| Core       | `references/core/`                 | conventions、intent-routing、playbooks、workflows                          |
| Accounts   | `references/accounts/`             | 直接读 `accounts-list` / `accounts-balance-stats` / `accounts-permissions` |
| Google Ads | `references/google-ads/`           | `google-ads-read` / `write` / `batch`；`rules/` 先 README 再单文件         |
| Meta Ads   | `references/meta-ads/`             | Instant Form：`meta-ads` / `read` / `write` + `meta-lead-launch-plan-template` |
| Analytics  | `references/analytics/`            | 拉数、批处理、拓词                                                         |
| Operations | `references/operations/`           | 预警、线索；自动化仅用户问起时                                             |
| Templates  | `report-templates/*.md`、`assets/` | 报告纲要 / JSON 契约                                                       |

源码目录：`tso-cli/assets/siluzan-ads/`。DeerFlow 的 `skills/public/siluzan-tso` 是发版时从 CLI 包拉下来的副本，不要手改，也不要在改完源文档后把副本再同步一遍。
