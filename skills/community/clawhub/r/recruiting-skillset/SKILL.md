---
name: recruiting-skillset
description: Use when starting any end-to-end hiring task — defining a role, writing/revising a JD, screening resumes, preparing interviews, writing interview evaluations, or calibrating hiring standards from feedback. Triggers include "招聘全流程"、"JD + 简历筛选 + 面试评价"、"统一招聘口径"、"批量评估候选人"、"复盘招聘标准"、"按 Superpowers 架构整合招聘 skill"。
license: MIT
---

# 招聘 Skill Set

## Overview

招聘全流程的总控 Skill。把 [[jd-writing]]、[[recruiting-resume-screening]]、[[interview-evaluation]] 串成一条用同一套标准的流水线。

**Core principle: 一套岗位标准，三次使用。**

- JD 阶段定义岗位本质、必备能力、加分项和验证标准。
- 简历筛选用同一套标准判断是否值得面试，并输出疑点、面试问题。
- 面试评价用同一套标准验证候选人真实能力、动机、风险与下一步。
- 用户、面试或入职反馈暴露标准错误时，回流更新 JD / 筛选 / 面评 Skill。

## When to Use

启用本 Skill 的触发词或场景：

- 用户要求从需求开始端到端做招聘：定义岗位、写 JD、筛简历、面试准备、写面评。
- 用户要求对同一岗位的 JD、筛选、面评做"统一口径校准"。
- 批量评估候选人并要求横向排序、面试问题、录用建议。
- 用户根据投递质量 / 面试结果 / 入职表现要求修正招聘标准。
- 用户在对话中出现"招聘 skill set / 招聘技能合集 / Superpowers 风格招聘 skill"等表达。

**NOT** for: 已经明确只在单一阶段（如只是写一份 JD），直接加载对应专项 Skill 即可。

## Stage Routing

| 用户意图 | 加载 | 产出 |
| --- | --- | --- |
| 写 JD / 改 JD / 岗位说明外发 | **REQUIRED:** [[jd-writing]] | 候选人外发 JD + 内部验证标准 |
| 评估简历 / 批量筛选 / 横向排序 | **REQUIRED:** [[recruiting-resume-screening]] | 个人评估卡 + 排序表 + 疑点 + 面试问题 |
| 准备面试 / 根据筛选生成追问 | [[recruiting-resume-screening]] + [[interview-evaluation]] | 面试卡、统一问题、专项追问 |
| 写面评 / 根据转写评估 | **REQUIRED:** [[interview-evaluation]] | 推进建议、优势、不足、风险、下一步 |
| 复盘招聘质量 / 调整标准 | 本 Skill + 相关专项 | 标准修正、Skill 更新、进化日志 |

## Architecture

```
[招聘需求/业务上下文]
        │
        ▼
┌────────────────────────────┐
│  recruiting-skillset 总控   │  ← 维护"岗位标准包"
└────────────────────────────┘
        │
        ▼
   [jd-writing] ───► 岗位标准包 ◄────┐
        │                            │
        ▼                            │
   [recruiting-resume-screening] ── 短名单 ───┤
        │                            │
        ▼                            │
   [interview-evaluation] ─── 面评 ──┘
        │
        ▼
   反馈回流：投递质量 / 面试发现 / 入职表现 → 修正标准
```

## The Role Standard Packet

每个岗位都应形成一个**岗位标准包**，贯穿三项专项 Skill。完整模板见 [role-standard-packet.md](role-standard-packet.md)。

最简形式：

- 岗位定位：行业通用岗位名 / 业务背景 / 核心问题 / 候选人层级。
- JD 核心结构：岗位职责 / 任职要求 / 加分项 / 反向筛选（可选）。
- 简历筛选标准：必备硬信号 / 加分信号 / 风险信号 / 一票否决。
- 面试验证标准：必问问题 / 强信号 / 弱信号 / 风险确认。
- 决策口径：⭐⭐⭐ 强推 / ⭐⭐ 推荐 / ⭐ 待定 / ❌ 不推荐。

## Workflow

### 1. Define Role Standard

加载 [[jd-writing]]。输出 JD 时同步沉淀岗位标准包：

- 岗位名称用行业通用叫法。
- JD 默认三段：岗位职责、任职要求、加分项；业务背景放进岗位职责开头，不单独立"岗位信息"章节。
- 任职要求必须可被简历和面试验证。
- 如有反向筛选，使用专业、克制的"我们不太适合这样的候选人"。

### 2. Screen Resumes Against the Same Standard

加载 [[recruiting-resume-screening]]。

1. 确认岗位标准包存在；没有则从 JD 中抽取。
2. 逐份提取简历文本，不凭记忆、不复用旧结论。
3. 每人输出五维评分、疑点、亮点、风险、Top 面试问题。
4. 批量候选人必须输出横向排序表。
5. 面试问题必须直接对应 JD 的必备能力、加分项、风险信号。

### 3. Prepare Interviews

同时使用 [[recruiting-resume-screening]] + [[interview-evaluation]]：

- 统一必问问题（横向比较）。
- 每人专项追问（来自简历疑点和岗位关键能力）。
- 强 / 弱信号现场判断卡。
- 速记模板供面试官使用。

### 4. Evaluate Interview Evidence

加载 [[interview-evaluation]]。面评必须：

- 用人单位视角直接给推进建议（不是顾问报告）。
- 先读完整转写 / 记录，再判断，不只根据简历印象。
- 优势 / 不足 / 风险都绑定具体证据。
- 区分"经验不匹配"和"能力不合适"；岗位不要求的能力不要当短板。
- 技术深度判断必须看核心基础问题，不被关键词光环带偏。
- AI Coding 经验区分"会用工具"和"有工程化方法论"。
- 批量面试转写有姓名误识别风险，必须先核对正式姓名再下结论。
- 下一步建议回到岗位标准包：进入下一轮 / 终面验证 / 不推荐 / 补充信息。

### 5. Feedback Loop

| 反馈 | 应更新 |
| --- | --- |
| 投递候选人整体不对 | [[jd-writing]] 岗位名、职责、反向筛选 |
| 筛选放过明显不合适候选人 | [[recruiting-resume-screening]] 硬信号 / 风险信号 / 一票否决 |
| 面试发现 JD 要求不可验证 | [[jd-writing]] 任职要求表达 |
| 面评归因不准 | [[interview-evaluation]] 归因规则和追问技巧 |
| 入职表现与评价偏差大 | 岗位标准包、筛选权重、面试验证标准 |

用户指出可复用问题时，立即 patch 对应 Skill，并在该 Skill 的 `EVOLUTION.md` 中记录。

## Output Contracts

### JD Output

```markdown
# [行业通用岗位名称]

## 岗位职责
...

## 任职要求
...

## 加分项
...

## 我们不太适合这样的候选人（可选）
...

## 面试重点（内部使用，外发可删除）
...
```

### Resume Screening Output

```markdown
# [岗位] 简历筛选报告

## 汇总排序
| 排名 | 姓名 | 评级 | 总分 | 核心理由 | 面试建议 |

## 个人评估卡
### [姓名]
- 综合评级：
- 五维评分：
- 核心亮点：
- 风险/疑点：
- 面试必问题：
```

### Interview Evaluation Output

```markdown
## 综合建议
> ⭐⭐⭐ 强推 / ⭐⭐ 推荐 / ⭐ 待定 / ❌ 不推荐 进入下一轮

## 综合评价

### 优势
...

### 不足
...

### 风险
...

## 下一步建议
...
```

正式交付给用户的报告只保留正式评价内容。姓名匹配、修订说明、材料定位、工具执行痕迹不要混入正式报告，除非用户明确要求。

## Common Pitfalls

| 反模式 | 后果 | 正确做法 |
| --- | --- | --- |
| 三段流程标准不一致 | 口径漂移，越筛越偏 | 强制使用同一份岗位标准包 |
| JD 像内部说明 | 候选人投递错位 | 写给候选人，业务背景放岗位职责开头 |
| 筛选凭关键词 | 关键词命中 ≠ 做过 ≠ 做深 | 看项目证据和个人贡献 |
| 面评复述经验 | 没判断只总结 | 判断能力和风险，绑定证据 |
| 全员都给推荐 | 排序失去意义 | 敢下不推荐 / 待定 |
| 把过程说明写进正式面评 | 报告变操作日志 | 过程信息只作内部材料 |
| 反馈不回流 | 同类错误反复出现 | 立即 patch 对应 Skill + EVOLUTION |

## Verification Checklist

输出前逐项确认：

- [ ] 当前任务属于 JD / 筛选 / 准备 / 面评 / 复盘中的哪一步？
- [ ] 已加载对应的专项 Skill？
- [ ] 形成或复用了岗位标准包？
- [ ] JD 包含 `岗位职责 / 任职要求 / 加分项`？
- [ ] 简历筛选逐人基于原始材料而非记忆？
- [ ] 面评基于转写 / 记录证据？
- [ ] 正式报告去除了姓名匹配、修订说明、工具执行痕迹？
- [ ] 最终建议能回溯到同一套岗位标准？
- [ ] 用户反馈已落到对应 Skill 的 `EVOLUTION.md`？

## See Also

- [role-standard-packet.md](role-standard-packet.md) — 完整岗位标准包模板。
- [EVOLUTION.md](EVOLUTION.md) — 本 Skill 的演化历史。
- [[jd-writing]] · [[recruiting-resume-screening]] · [[interview-evaluation]] — 三个专项 Skill。
