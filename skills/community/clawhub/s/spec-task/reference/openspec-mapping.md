# OpenSpec 概念映射

spec-task 的设计借鉴了 OpenSpec 的 spec-driven 工作流，但做了大幅"去编码化"改造。本文档记录概念对照关系，帮助理解设计来源。

## 概念对照

| OpenSpec spec-driven | spec-task agent-task | 差异说明 |
|---|---|---|
| `proposal.md` | `brief.md` | 去掉 Capabilities 概念，改为 Intent + Scope + Success Criteria |
| `specs/**/*.md` | `spec.md`（任务根目录） | 保留 delta format（ADDED/MODIFIED/REMOVED），内容从"代码行为"改为"任务验收场景" |
| `design.md` | `plan.md` | 去掉代码架构决策，改为执行策略 + 工具清单 + 依赖 + 时间 |
| `tasks.md` | `checklist.md` | 格式相同（Markdown checkbox），增加产出物关联 |
| apply phase | apply phase | 增加 status.yaml 更新、outputs 写入 |
| — | `status.yaml` | 新增：运行时状态文件（OpenSpec 无对应概念） |
| — | `revisions[]` | 新增：任务变更追踪（OpenSpec 无对应概念） |
| — | `outputs/` | 新增：产出物目录（OpenSpec 无对应概念） |
| — | `verify` phase | 新增：验收阶段（OpenSpec 无对应概念） |
| — | archive to memory | 新增：经验归档到 agent memory（OpenSpec 归档到 .openspec/archive/） |
| — | Onboarding | 新增：配置初始化向导（OpenSpec 通过 CLI 交互配置） |

## OpenSpec 去除的部分

spec-task 不包含以下 OpenSpec 功能（这些是面向编码场景的）：

| 去除项 | 说明 |
|--------|------|
| Capabilities 概念 | New/Modified capabilities 面向代码 spec，agent 任务不需要 |
| RFC 2119 格式 | SHALL/MUST 面向代码行为，改为 GIVEN/WHEN/THEN 验收场景 |
| 代码架构决策 | 面向代码架构，改为执行策略 + 工具清单 |
| 20+ AI CLI 工具适配器 | agent 不通过 CLI 使用工具 |
| schema 配置字段 | 改为直接读取 schemas/ 目录下的模板 |
| agents 配置字段 | 任务分配由 agent 控制，spec-task 不管理 agent 注册表 |
| CLI 交互式命令 | 人驱动的 slash command，agent 不需要 |
| 人工确认流程 | agent 自主判断 |

## 概念复用的 OpenSpec 模块

以下 OpenSpec 的**设计概念**（非代码）被复用到 spec-task 中：

| OpenSpec 模块 | 源码位置 | 复用方式 |
|------|---------|---------|
| ArtifactGraph（DAG + 拓扑排序） | `artifact-graph/graph.ts` | **概念复用** — spec-task 的 schema.yaml 定义了 artifact 依赖 DAG，agent 按拓扑顺序生成构件 |
| 状态检测（文件存在性 + glob） | `artifact-graph/state.ts` | **概念复用** — agent 通过检查文件是否存在来判断 artifact 是否完成 |
| Schema 加载（三级解析） | `artifact-graph/resolver.ts` | **概念复用** — config 读取优先级：项目 > skill 内置默认 |
| Delta Spec 解析（ADDED/MODIFIED/REMOVED） | `specs-apply.ts` + `parsers/` | **概念复用** — spec.md 保留 delta format |
| Task Progress（checkbox 解析） | `utils/task-progress.ts` | **概念复用** — ProgressCalculator 读取 checklist.md 统计带步骤编号的 `- [x]` 计算进度 |
| Archive | `archive.ts` | **概念复用** — 任务完成后归档到 agent memory |

> **注意**：spec-task 是纯 Markdown + YAML 指令包，不导入 OpenSpec 的 TypeScript 代码。上述复用均为**设计概念层面**的借鉴。

> **历史遗留**：spec-task 的 `schema.yaml` 中引用了 `.py` 脚本名（如 `task_create.py`），这是早期设计遗留。实际执行的是对应的 TypeScript 工具，Python 脚本并不存在。
