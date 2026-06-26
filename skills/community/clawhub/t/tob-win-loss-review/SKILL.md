---
name: tob-win-loss-review
version: 2.0.0
description: ToB销售丢单复盘助手。输入行业/规模/阶段/竞品/关键事件，使用李宁原创销售经验规则引擎输出根因分析、风险信号和改进建议。
priority: high
source: lining-experience-rules
workers: Tech, Sales, Checker
created: 2026-05-15
tags: [tob, sales, win-loss, review, rules]
---

# tob-win-loss-review — 丢单复盘助手

## 何时使用

当用户需要复盘 ToB 销售丢单原因，并希望基于行业、销售阶段、关键事件快速得到可执行改进建议时使用。

本技能为**纯规则引擎**，规则来自李宁多年 ToB 销售与解决方案实践经验；不读取、不打包任何客户商业资产。

## 使用方式

### 交互模式

```bash
tob-win-loss-review
```

### 快速模式

```bash
tob-win-loss-review --industry 零售 --size 大型 --duration 4个月 --stage 报价谈判 --competitor 略 --event "客户说我们价格比竞品高30%，虽然我们功能更全但对方预算有限"
```

### JSON 调试

```bash
tob-win-loss-review ... --json
```

## 实现逻辑

1. 行业规则：识别不同行业的共性风险与价值包装重点
2. 阶段规则：按报价谈判、POC、方案、合同等阶段判断控制点缺口
3. 事件规则：从关键事件中触发价格、竞品、决策链、POC等风险模式
4. 概率排序：保留核心原因 / 辅助原因 / 潜在风险结构
5. 建议输出：短期动作 / 中期能力 / 长期体系化

## 输出约束

- 根因分析使用「规则依据」说明触发逻辑
- 风险信号对照基于行业 + 阶段 + 事件交叉匹配
- 中文输出，结构固定：项目画像 → 根因分析 → 风险信号 → 改进建议

## 注意事项

- 本技能不访问外部数据源，默认可离线运行
- 规则结论用于复盘和下一步行动设计，不替代真实客户访谈
