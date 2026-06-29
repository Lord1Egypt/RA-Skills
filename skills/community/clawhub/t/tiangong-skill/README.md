# 天工.skill

> 为 AI 智能体赋予专业灵魂。支持两种设计范式：**人物蒸馏**（由内而外，复刻真实人物的心智模型）与**岗位型专家**（由外而内，定义岗位职责与交付标准）。

## 两种范式

| | 人物蒸馏 (Persona Distillation) | 岗位型专家 (Job-oriented) |
|---|---|---|
| **方向** | 由内而外：心智模型 → 外部表达 | 由外而内：岗位职责 → 人格一致性 |
| **起点** | 真实人物的著作/访谈/表达DNA | 岗位描述/职责清单/交付标准 |
| **核心产出** | 3-7 个心智模型 + 决策启发式 + 表达DNA | 身份5字段 + DO/DON'T规则 + 可量化KPI |
| **模板** | `examples/persona-template.md` | `examples/job-template.md` |
| **验证脚本** | `scripts/verify-persona.py` | `scripts/verify-skill.py`（岗位型深度校验） |
| **端到端示例** | — | `examples/tax-advisor-example.md`（J1→J5 完整流程） |

**判断方法**：这个智能体是在模仿一个人（人物蒸馏），还是在承担一个岗位（岗位型）？

## 目录结构

```
tiangong-skill/
├── SKILL.md                      # 技能主文件（设计流程、CHECKPOINT、流水线定义）
├── README.md                     # 本文件
├── QUICKSTART.md                 # 30 秒快速上手
│
├── assets/                       # 静态资源（由设计流程按需引用）
│   ├── README.md                 # assets 目录说明
│   └── color-schemes.yaml        # 5 部门色标 + 人格蒸馏专属色
│
├── examples/                     # 模板与端到端示例
│   ├── persona-template.md       # 人格蒸馏空白启动模板（16 个必选章节）
│   ├── job-template.md           # 岗位型空白模板（身份5字段 + DO/DON'T + 极限行为）
│   └── tax-advisor-example.md    # 岗位型端到端示例（J1→J5 全流程）
│
├── references/                   # 详细参考文档（按需读取，不内联到 SKILL.md）
│   ├── persona-details.md        # 人物蒸馏详细模板与设计规范
│   ├── job-details.md            # 岗位型详细模板、触发词设计、范式融合路径
│   └── quality-system.md         # 质量体系：失败回退、反膨胀、规则冲突、回测验证
│
├── scripts/                      # 验证脚本（CHECKPOINT 门禁）
│   ├── verify-persona.py         # 人格蒸馏产物结构验证（16 项检查）
│   └── verify-skill.py           # 技能结构验证（通用 + 岗位型深度 11 项 + 规则冲突）
│
└── output/                       # 最终产出物写入目录
    └── .gitkeep
```

## 模板说明

### persona-template.md — 人格蒸馏模板

用于人物蒸馏范式。复制此模板，填入蒸馏结果即可生成完整的 SKILL.md。包含 **16 个必选章节**：

- 角色扮演规则、身份卡（5字段）、价值观与反模式、心智模型（3-7个）、决策启发式（5-10条）
- 回答工作流（Agentic Protocol）、表达DNA（7维度）、人物时间线、智识谱系
- 诚实边界（≥5条）、技术交付物（≥1）、工作流程（3-5步）、成功指标（≥3）、沟通风格、退化行为设计（4场景）、调研来源附录

完整设计规范见 `references/persona-details.md`。

### job-template.md — 岗位型模板

用于岗位型专家范式。包含 **12 个模块**：身份与记忆（5字段）、核心使命+反使命、专业回答工作流（3步骤）、领域流派与分歧、关键规则（DO/DON'T）、技术交付物、工作流程、沟通风格（3标签+拒绝方式）、成功指标（KPI ≥3）、知识库（3层）、极限行为设计（4场景）、诚实边界。

模板内置"快速启动"默认值推导规则——即使用户信息不足，也可自动填充关键字段。完整设计规范见 `references/job-details.md`。

## 验证脚本

两个脚本各司其职，分别对应两种范式的产出物。

### verify-persona.py — 人格蒸馏产物专用

```
python scripts/verify-persona.py <path/to/SKILL.md> [--json]
```

**校验 16 项**：YAML frontmatter（name/description/color）、16 个必选章节、身份卡5字段、心智模型数量 [3,7] 及三重验证痕迹、决策启发式 [5,10]、表达DNA 7维度、回答工作流3步、诚实边界 ≥5条及关键项、退化行为4场景、工作流程 [3,5]、成功指标 ≥3、技术交付物 ≥1、调研来源（一手+二手 ≥1）、人物时间线、沟通风格、智识谱系。额外检查一手来源占比（< 50% 警告）。

**退出码**：0 = PASS, 1 = FAIL。

### verify-skill.py — 技能结构通用验证（含岗位型深度校验）

```
python scripts/verify-skill.py [--skill path/to/SKILL.md] [--json] [--quiet]
```

**校验 7 大维度**：

| 维度 | 内容 |
|------|------|
| YAML frontmatter | name / description / version / domain / author |
| Gate 标记 | 3 个硬门禁（信息完备 / 提炼质量 / 交付就绪）统计 + 行号分布 |
| H2 标题 | 蒸馏流程 / 设计模式 / 工具类标题统计 |
| 规则冲突检测 | DO vs DON'T 语义交叉分析 |
| 反模式索引 | "不触发条件"（4条）+ "蒸馏红线"（5条）自动校验 |
| 引用文件 | references/ 和 examples/ 下 .md 文件的代码围栏配对、H2 重复、最小长度 |
| 岗位型深度结构 | **条件激活**：检测到"身份与记忆"章节时，自动校验 11 项（身份5字段、使命+反使命、回答工作流3步、流派共识、交付物、工作流程步骤 [3,5]、沟通风格3标签+拒绝方式、极限行为4场景、KPI ≥3、知识库3层、诚实边界 ≥5） |

> verify-skill.py 是**全流程通用门禁**——人格蒸馏在 Gate 3 调用，岗位型在 J4 质量内控调用。verify-persona.py 是**人物蒸馏专属补充**，提供更细粒度的心智模型/表达DNA/启发式等专属校验。

## 快速开始

1. **岗位型**（推荐入门）：阅读 `QUICKSTART.md`，30 秒了解从"创建一个税务顾问"到完整 SKILL.md 的全流程。
2. **人物蒸馏**：阅读 `SKILL.md` 中"人物蒸馏"章节，按照蒸馏 0→1→2→3→4→5 推进。
3. **类型判断拿不准**：阅读 `SKILL.md` 中"快速诊断"5 题，2 分钟确定走哪条路径。
4. **范式融合**：先定义岗位（岗位型），再注入某位行业人物的思维特征（蒸馏）——见 `references/job-details.md` §两种范式融合路径。

## 相关文档

| 文档 | 用途 |
|------|------|
| [完整设计流程](SKILL.md) | 完整设计流程、CHECKPOINT 定义、两种范式流水线 |
| [快速上手](QUICKSTART.md) | 30 秒快速上手 |
| [质量体系](references/quality-system.md) | 质量内控、规则冲突检测、反膨胀、回测验证 |
| [静态资源指引](assets/README.md) | 静态资源使用指引 |
