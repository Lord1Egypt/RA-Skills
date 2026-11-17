# references 索引

> 这是运行时的按需索引。先判断用户当前任务，再只加载一条最相关的参考链，不要全量阅读。

## 主链路

| 文件 | 何时加载 |
|------|----------|
| [quick-start.md](quick-start.md) | 用户第一次了解本 skill |
| [execution.md](execution.md) | 执行一次“选择 → 使用 → 验证”的真实任务 |
| [skill-usage-guide.md](skill-usage-guide.md) | 用户问怎么安装、调用、组合或维护 skill |
| [skill-ecosystem.md](skill-ecosystem.md) | 需要从已装 skill 和候选 skill 中选最小组合 |
| [skill-sources.md](skill-sources.md) | 需要从**外部**找优秀 skill（来源优先级 + 检索 + 安装适配） |
| [skill-taxonomy.md](skill-taxonomy.md) | 需要给 skill 归类、或按分类对齐任务域 |
| [best-practices/toolbox.md](best-practices/toolbox.md) | 需要查安装 prompt 或核心工具 |
| [retry-policy.md](retry-policy.md) | 进行 skillhub 或其他外部调用前 |

## 针对性诊断

| 文件 | 何时加载 |
|------|----------|
| [system-scan.md](system-scan.md) | 用户明确要求检查环境或解释 skill 为什么不生效 |
| [best-practices/checklist.md](best-practices/checklist.md) | 需要查看 12 条核心检查的唯一事实源 |
| [best-practices/checklist-details.md](best-practices/checklist-details.md) | 某条检查未达标，需要具体修复建议 |
| [report-format.md](report-format.md) | 生成或审阅诊断报告 |
| [state-schema.md](state-schema.md) | 读写 `state.md` 或处理状态迁移 |

## 维护与沉淀

| 文件 | 何时加载 |
|------|----------|
| [self-evolution.md](self-evolution.md) | 记录建议采纳、拒绝和可复用做法 |
| [self-evolution-log.md](self-evolution-log.md) | 追加用户确认后的经验事件 |
| [config-templates/automation-templates.md](config-templates/automation-templates.md) | 需要自动化、连接器或 SOUL 模板 |
| [token-management-checklist.md](token-management-checklist.md) | 用户明确询问 token、积分或成本 |

## Skill 目录

| 文件 | 何时加载 |
|------|----------|
| [skill-catalog/INDEX.md](skill-catalog/INDEX.md) | 需要浏览核心 skill、主题 skill 或画像映射 |
| [skill-catalog/core.md](skill-catalog/core.md) | 需要查看通用核心 skill |
| [skill-catalog/INDEX.md](skill-catalog/INDEX.md) | 已知用户主题，需要补齐最小候选（主题清单经 INDEX 索引） |

## 运行规则

1. 先理解真实目标，再选择最小方案；不要为了检查而先运行全量扫描。
2. 每次最多加载索引命中的 1–3 个文件；只有问题仍不清楚时才继续深入。
3. 安装、升级、停用、写记忆和创建自动化都必须在用户确认后执行。
4. 运行面只使用本索引中的资料；作者侧资料（发布、自测、经验编译、目录维护）不随发布包分发，仅保留在源仓库。

> 作者侧资料不参与运行时索引，包括架构说明、研究材料、案例、计划、wiki、skill 详细卡片和发布测试工具。
