# red-team

> 对抗性方案审查工作流 · Adversarial Plan Review Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)]()

**在现实打你之前，让 AI 先打你一遍。**

三轮递进式对抗攻击：逻辑漏洞 → 执行风险 → 最坏情景。

---

## 和其他审查方式的区别

| | 普通 AI 反馈 | **red-team** |
|--|--|--|
| 立场 | 中立，帮你完善 | **专门站对立面攻击** |
| 深度 | 表面建议 | **三轮递进，逐层深挖** |
| 情景 | 正常情况 | **包含极端失败情景** |
| 输出 | 建议列表 | **韧性评级 + 必须解决 vs 可接受风险** |

---

## 快速安装

```bash
npx @skill-hub/cli install red-team --agent claude
clawhub install red-team
```

---

## 工作流程

```
方案摄入 → 选择攻击阵型 → 三轮攻击 → 防御建议（可选） → 综合评估
```

### 三轮攻击结构

**第一轮 · 逻辑漏洞**：前提假设是否成立？内部逻辑是否自洽？

**第二轮 · 执行风险**：资源、依赖、协调、时序——哪里最容易断？

**第三轮 · 最坏情景**：极端失败情景构建，测试方案有没有退出机制。

---

## 内置攻击者阵型

| 配对 | 适合方案类型 |
|------|-----------|
| 老股东 × 竞对 PM | 创业 / 商业计划 |
| 最挑剔用户 × 工程师 | 产品 / 功能设计 |
| 魔鬼代言人 × 悲观主义者 | 通用决策 |
| 安全专家 × 法务 | 技术 / 合规方案 |

---

## 与 critical-writing 的关系

两个 skill 是同一系列，互补使用：

- **critical-writing**：打磨文章表达，用辩论法庭提升写作质量
- **red-team**：检验方案实质，用对抗攻击暴露决策盲区

---

## 文件结构

```
red-team/
├── SKILL.md
├── README.md
├── references/
│   └── attackers.md       # 攻击者阵型手册
├── examples/
│   └── example-startup-plan.md
└── tests/
    └── test-cases.md
```

---

MIT License
