---
name: skill-authoring-standard
description: 按六步规范编写、改造、审计 Agent Skill：定边界→配元信息→编 SOP→配资源→建评测→灰度迭代；附带 SKILL 模板、评测用例模板与自动审计脚本。触发词：编写 skill、设计 skill、新建 skill、改造 skill、审查 skill、skill 规范、skill 上线。不适用于：写业务代码、整理普通文档（走 knowledge-router）、只要一个 prompt 片段。
user-invocable: true
version: "1.0.0"
last_updated: "2026-10-26"
---

# Skill 编写标准（六步）

> 使用时机：每次新建、改造或审查 skill 都先走本 skill；`audit_skill.py` 是上线闸门，不通过不发版。

## 边界清单

| 能做 | 不做 |
|---|---|
| 新建 skill、改造已有 skill、审查 skill 是否符合上线标准 | 不写业务实现代码；不替用户决定业务边界 |
| 产出 SKILL.md、模板、参考、评测集、审计报告 | 不整理普通文档（→ `knowledge-router`）；不审查非 skill 文档 |
| 判断场景是否值得封装、粒度是否合适 | 不把多个独立业务塞进一个 skill；不拆到路由混乱 |

**粒度原则**：一个 skill 只解决一类闭环任务。做大而全 → 臃肿难维护；做碎而杂 → 频繁路由、逻辑混乱。

## 路由元信息

| 项 | 内容 |
|---|---|
| 正向触发 | 编写/设计/新建/改造/审查 skill、skill 规范、skill 上线、这个 skill 合格吗 |
| 反向不触发 | 写业务代码、写普通文章、只做内容压缩（→ `distill-onepager` / `docs-to-knowledge`） |
| 禁用场景 | 只要一段 prompt；非 Agent Skill 的普通脚本；业务边界尚未说清 |
| 优先级 | 用户明确“审 skill” > 本 skill；普通文档整理 > `knowledge-router` |

正/反用例见 `eval/cases.md`；审计脚本 `scripts/audit_skill.py`。

## 工作流（六步）

| 步 | 动作 | 交付物 | 通过门槛 |
|---|---|---|---|
| 1 | **定场景与边界**：重复高频、流程固定、目标独立、可闭环；四者缺一不封装 | 「能做 / 绝对不做」清单 + 粒度说明 | 边界能一句话说清 |
| 2 | **配元信息**：名称、用途、触发、禁用、优先级 | frontmatter + 正/反路由用例 | 路由准确率 ≥95% |
| 3 | **编 SOP**：目标与验收标准、固定流程、依赖、呈现格式、异常兜底 | 五模块齐全的 SKILL.md | 五模块无缺项 |
| 4 | **配资源**：few-shot、参考、模板、中间状态、权限 | `assets/`、`references/`、`scripts/`、状态约定 | 缺依赖有降级路径；高风险有二次确认 |
| 5 | **建评测**：路由准确率、任务完成率、抗幻觉 | `eval/cases.md` + 评分表 | 无评测不上线 |
| 6 | **灰度迭代**：MVP 先跑通核心，收集失败 case，反哺规则 | `version`、`last_updated`、`eval/failures.md` | 每条修正有回归用例 |

### 第 3 步的五个 SOP 模块（缺一不可）

| 模块 | 要写清什么 | 不管什么 |
|---|---|---|
| 目标与验收标准 | 交付什么、覆盖范围、什么算合格 | 排版、话术、模板 |
| 固定执行流程 | 分步顺序、每步输入输出 | 内容质量、排版 |
| 依赖 | 工具、接口、知识库、外部 skill | 流程顺序、输出格式 |
| 呈现格式与话术 | 排版、话术、模板、命名 | 内容是否完整正确 |
| 异常兜底 | 异常清单、降级路径、停止条件 | 正常路径与主流程 |

## 编辑质量门

写 SKILL.md 和它的产出文档时，必须过两道门（详见 `references/editorial-qa.md`）：

1. **章节契约 + 术语表**：每节先写“这一节回答什么问题、只收什么、不收什么”；两个标题共享未限定关键词（如“输出”）就加限定词。
2. **冷读者复审**：只读标题和每块首句，问“这句话在回答这个标题吗”“只看标题能分清这两节吗”。清单不为空就返回修改。

`scripts/audit_skill.py` 会自动检查必需章节、frontmatter、eval 文件和标题撞词。

## 交付物清单

| 产物 | 必需 | 说明 |
|---|---|---|
| `SKILL.md` | 是 | 边界、路由、SOP、依赖、异常、状态权限、评测、迭代 |
| `eval/cases.md` | 是 | 正/反/异常用例 + 评分表 |
| `eval/failures.md` | 是 | 失败回流表（可为空表） |
| `assets/` | 视需要 | 模板、few-shot、状态模板 |
| `references/` | 视需要 | 领域知识、长规则 |
| `scripts/` | 视需要 | 可执行检查/生成脚本 |

## 依赖与资源

| 类型 | 依赖 | 缺失/失败时 |
|---|---|---|
| 模板 | `assets/SKILL.template.md` | 按本 SKILL 的章节结构手写 |
| 用例模板 | `assets/eval-cases.template.md` | 至少写正向/反向/异常各 1 条 |
| 规范全文 | `references/six-step-standard.md` | 读本 SKILL 的六步表 |
| 编辑门 | `references/editorial-qa.md` | 至少执行章节契约与冷读复审 |
| 审计 | `scripts/audit_skill.py` | 人工逐项对照「交付物清单」 |

## 异常与兜底

| 场景 | 处理 |
|---|---|
| 场景不满足四条件 | 不建议封装成 skill；改用普通 prompt、脚本或文档 |
| 边界说不清 | 先做场景访谈/流程图，不写 SKILL.md |
| 粒度过大 | 拆成多个 skill + 一个 router |
| 粒度过细 | 合并；一个 skill 不服务单一按钮 |
| 两个 skill 路由冲突 | 在 description 写“不适用于”并定优先级 |
| 没有评测集 | 不许上线；先补 5 条正/反用例 |
| 依赖缺失 | 在 SKILL.md 标降级路径，不静默失败 |

## 状态与权限

- 多轮状态：`.skill-state/<skill-slug>.md`，字段：六步进度 / 关键决策 / 待确认 / 变更记录。
- 高风险操作需二次确认：覆盖已有 SKILL.md、删除 skill 目录、安装依赖、写到 skills 目录之外。
- 默认输出：`~/.zcode/skills/<skill-name>/`；用户指定则以其为准。

## 评测

| 指标 | 门槛 | 说明 |
|---|---|---|
| 审计通过率 | 100% | `audit_skill.py` 必需项全过 |
| 路由准确率 | ≥95% | 正反用例各 ≥10 条 |
| 任务完成率 | 100% | 正常场景可闭环 |
| 抗幻觉 | 100% | 不编造依赖、不虚构评测结果 |

运行：

```bash
python scripts/audit_skill.py <skill_dir>
python scripts/audit_skill.py --selftest
```

## 迭代

- 版本：`1.0.0`（2026-10-26 定稿）。
- 失败回流：`eval/failures.md`，四列「输入 / 期望 / 实际 / 修正」。
- 灰度：新 skill 先只在一个真实场景跑通，再扩触发词；每次改规则必须跑审计与回归。

## 快速开始

1. 复制 `assets/SKILL.template.md` 到 `~/.zcode/skills/<name>/SKILL.md`。
2. 按六步表逐项填，先写边界和路由，再写 SOP。
3. 复制 `assets/eval-cases.template.md` 到 `eval/cases.md`，补正/反/异常用例。
4. 跑 `python scripts/audit_skill.py <skill_dir>`，修到 PASS。
5. 用真实输入跑一次，把失败写入 `eval/failures.md`，再发版。

## 反模式

| 不要 | 要 |
|---|---|
| 大而全：一个 skill 包多个独立业务 | 一类闭环任务一个 skill |
| 碎而杂：拆到每个按钮一个 skill | 合并成有明确边界的流程 |
| 只写指令，不写“绝对不做” | 边界清单先行 |
| 触发词写得很宽 | 写“不适用于”和优先级 |
| 只写流程，不配资源/状态/权限 | 模板 + 状态 + 二次确认 |
| 无评测就上线 | 三指标 + 回归集 |
| 定义句放在流程/迭代节 | 定义进开头，动作进流程 |
| 两个模块名共享“输出/标准/格式” | 加限定词：内容验收 / 呈现格式 |
