# siluzan-tso — Agent 文档目录

> 单一 Skill 包（`name: siluzan-tso`）。运行时入口：`SKILL.md` → 按域 lazy-load `references/`。

## 启动顺序

1. Read `SKILL.md`（单一路由表：意图 → 工作流 → 必读文档）
2. **每个新任务** Read `references/core/agent-conventions.md`
3. 按路由表 Read「必读文档」与对应工作流卡片，再执行 `siluzan-tso …`：
   - 分析/报告类线性步骤 → `references/core/playbooks.md`（P1–P9）
   - 操作/管理类线性步骤 → `references/core/workflows.md`（W1–W12）
   - 命令参数/字段口径 → 各域 `references/*.md`
4. **P5 / P6 / P7** 或长 CLI 输出：可选 Read `references/core/subagent-orchestration.md`（主 Agent 自行决定是否委派 subagent）

## 文档域（gstack-style domains）

| 域             | 路径                                                                 | 何时 Read                                                      |
| -------------- | -------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Core**       | `references/core/`                                                   | 纪律、安装、tips、playbooks、workflows、subagent-orchestration |
| **Handoff**    | `snippets/`                                                          | P5/P6/P7 Task 派发模板（与 SKILL 同级）                        |
| **Accounts**   | `references/accounts/`                                               | 列表、余额、开户、财务、审计                                   |
| **Google Ads** | `references/google-ads/`                                             | CRUD、PMax、搜索系列流水线；`rules/` 为优化 SOP                |
| **Analytics**  | `references/analytics/`                                              | 拉数、批处理、拓词、RAG、TSO 报告                              |
| **Operations** | `references/operations/`                                             | 预警、线索、优化记录、宿主编排自动化                           |
| **Templates**  | `assets/`、`references/report-templates/`、`report-templates/*.html` | JSON 契约、报告纲要、HTML 样式                                 |

## 工作流目录

| 类别          | 文档                           | 编号   |
| ------------- | ------------------------------ | ------ |
| 分析 / 报告类 | `references/core/playbooks.md` | P1–P9  |
| 操作 / 管理类 | `references/core/workflows.md` | W1–W12 |

专用报告模板（被工作流卡片引用）：

| ID                | 文档                                                              |
| ----------------- | ----------------------------------------------------------------- |
| 网站诊断          | `references/report-templates/website-diagnosis-report.md`         |
| 战略市场分析      | `references/report-templates/market-analysis-report.md`           |
| Google 周期 Excel | `references/report-templates/google-period-report-excel.md`（P4） |
| OKKI 周报         | `references/report-templates/okki-weekly-google-client.md`        |
| 询盘分析          | `references/report-templates/google-inquiry-analysis.md`          |

## 维护

- 源码唯一真相：`tso-cli/assets/siluzan-ads/`（勿编辑 `skills/siluzan-tso/` 副本）
- 通用纪律唯一真相源：`references/core/agent-conventions.md`（其他文档只单行指向，不复制规则）

## CLI 代码域（与文档对齐）

| CLI 模块                                                           | 文档域                       |
| ------------------------------------------------------------------ | ---------------------------- |
| `src/commands/list-accounts/`、`accounts-digest/`、`balance-scan/` | accounts                     |
| `src/commands/open-account/`、`account-manage-register.ts`         | accounts                     |
| `src/commands/ad/`                                                 | google-ads                   |
| `src/commands/google-analysis/`、`google-analysis-batch.ts`        | analytics                    |
| `src/commands/website-diagnosis/`                                  | analytics（网站诊断）        |
| `src/commands/market-analysis/`                                    | analytics（战略市场分析）    |
| `src/commands/report/`                                             | analytics + report-templates |
| `src/commands/forewarning/`、`optimize/`、`clue.ts`                | operations                   |
