# RiskForge - AI代码风险审查与测试策略生成器

RiskForge 面向研发、测试和技术负责人，用 AI 对代码变更做上线前白盒风险审查。它会结合 Git Diff、源码上下文、依赖影响、运行时异常、安全与性能风险，输出可直接执行的测试策略、风险清单、修复建议和标准化报告。

> 适合在 Code Review、提测前、上线前质量门禁、回归测试规划、缺陷复盘时使用。

## 为什么值得收藏

- **定位准**：每个风险必须关联到具体文件和代码行，避免“泛泛而谈”的测试建议。
- **可执行**：输出测试清单、单测建议、回归范围、风险优先级和修复方向。
- **覆盖全**：同时检查功能正确性、运行时异常、依赖影响、安全、性能、兼容性和边界场景。
- **适合团队复用**：生成 Markdown/HTML 报告，可沉淀到评审、测试和发布流程中。
- **降低漏测**：把经验型 QA 的风险识别方法固化成可重复执行的 Skill。

## 典型使用场景

| 场景 | RiskForge 能做什么 |
| --- | --- |
| 上线前 Code Review | 从代码变更中识别缺陷、异常路径、兼容性和回归风险 |
| 测试策略设计 | 根据变更范围生成单测、集成测试、E2E 和探索性测试建议 |
| 质量门禁 | 输出风险等级、阻塞项、放行条件和必要验证项 |
| 缺陷预防 | 回溯风险依据，给出可验证的修复建议 |
| 覆盖率提升 | 找出未覆盖分支、边界条件和高风险依赖链路 |

## 快速开始

在支持 ClawHub/OpenClaw Skill 的环境中安装后，直接用自然语言触发：

```text
使用 riskforge 分析这次 Git Diff 的上线风险，并给出测试策略和高优先级风险清单。
```

```text
用 RiskForge 检查 src/services/order.ts 的运行时异常、安全风险和需要补充的单测。
```

如果在本地 skill 目录中运行报告脚本：

```bash
cd .joycode/skills/riskforge
npm install
```

## 输出内容

- 风险摘要：阻塞项、高风险项、中低风险项
- 代码定位：文件、函数、行号、触发条件
- 回溯校验：风险依据、置信度、误报检查
- 测试策略：单测、集成测试、E2E、回归测试建议
- 修复建议：优先级、验证方式、影响范围
- 标准报告：Markdown/HTML 格式，便于归档和分享

## 关键词

`AI Testing` `Code Review` `Risk Analysis` `Git Diff` `QA Automation` `Regression Testing` `Unit Test` `Security Test` `Performance Test` `Quality Gate`

## 文件结构

```text
.joycode/skills/riskforge/
├── SKILL.md
├── README.md
├── package.json
├── scripts/
│   └── generate-test-report.js
└── references/
    ├── dependency-impact-analyzer.md
    ├── runtime-exception-detector.md
    ├── risk-backtracking-validator.md
    └── unit-testing.md
```

## 使用建议

1. 在提交 PR 或提测前运行，风险发现最及时。
2. 给出具体范围，例如文件、分支、Git Diff 或业务功能名。
3. 对高风险项要求补充验证命令、单测或回归用例。
4. 将报告沉淀到发布记录中，形成可追溯质量资产。
## ClawHub 搜索词覆盖

RiskForge 覆盖这些高意图场景：`Code Review`、`Git Diff`、`代码风险分析`、`质量门禁`、`上线前检查`、`回归测试`、`单元测试建议`、`运行时异常`、`依赖影响分析`、`安全测试`、`性能测试`、`测试覆盖率`、`QA 自动化`。

## 30秒价值说明

如果你正在准备发布、提测或合并 PR，RiskForge 会把“这次代码改动可能哪里出问题、应该测什么、哪些风险会阻塞上线”整理成可执行报告。它不是泛用聊天提示词，而是面向研发和 QA 的代码风险审查工作流。

## 金融AI增强方向

RiskForge 会持续增强金融 AI 场景：LLM/Agent/RAG 风险、模型输出约束、金融数据泄漏、KYC/AML 审计证据、支付与风控链路、提示注入、工具调用滥用、模型降级与人工复核。
