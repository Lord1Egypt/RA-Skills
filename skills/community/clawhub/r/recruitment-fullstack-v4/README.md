# recruitment-fullstack-v4

> 招聘全流程 V4.0 — 结构化面试评估体系

## 快速开始

```
1. 安装 skill
2. 提供候选人简历
3. 按流程执行阶段0→4
```

## 核心功能

| 阶段 | 内容 | 文件 |
|------|------|------|
| 阶段0+1 | 需求确认 + 简历筛选 | `packages/02-intake-standards.md` |
| 阶段2 | 面试题目设计 | `packages/03-interview-design.md` |
| 阶段2附录 | 7大岗位题库 | `packages/04-questionbanks.md` |
| 阶段3 | BARS评估 | `packages/05-interview-evaluation.md` |
| 阶段3.5 | Calibration校准 | `packages/06-calibration.md` |
| 阶段4 | 最终决策 | `packages/07-final-decision.md` |

## 设计原则

- 证据驱动（无证据不结论）
- 可计算（评分必须带计算明细）
- 可校准（Calibration机制）
- 可复核（局限性声明）

## 与旧版差异

- 覆盖全流程（阶段0→4）
- BARS结构化评分
- A/B/C/D追问决策树
- 8项反偏见自检
- Calibration校准机制

## 文件结构

```
recruitment-fullstack-v4/
├── SKILL.md                    ← 主入口
├── README.md                   ← 本文件
└── packages/
    ├── 01-framework.md         ← 主框架
    ├── 02-intake-standards.md  ← 阶段0+1
    ├── 03-interview-design.md  ← 阶段2
    ├── 04-questionbanks.md     ← 题库
    ├── 05-interview-evaluation.md  ← 阶段3
    ├── 06-calibration.md       ← 阶段3.5
    └── 07-final-decision.md    ← 阶段4
```
