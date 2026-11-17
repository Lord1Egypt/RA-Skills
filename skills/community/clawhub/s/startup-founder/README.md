# 独立开发者创业技能库

> AI Agent Skills for Startup Founders —— 从点子到产品到融资

## 定位

为独立开发者和小团队提供一套创业全流程 AI 技能，覆盖点子验证、MVP 构建、创始人销售和融资准备。

## 核心理念

> 创业失败的头号原因是做没人要的产品。本技能库教你：先验证再构建，先手动再自动化，先销售再规模化。

- **不写一行代码就能验证点子** — 人工卖服务，有人付钱再写代码
- **MVP 不是半成品** — 是能交付价值的最小单位
- **创始人是最好的销售** — 早期产品卖的是创始人的愿景和专业性
- **融资是放大器不是救命稻草** — 先有 traction，再谈估值

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 验证 | `idea-validator` | 创业点子验证：问题紧迫性、市场时机、商业数学 | [衍生](https://skills.sh/refoundai/lenny-skills/evaluating-startup-ideas) |
| 构建 | `mvp-builder` | MVP 三段式构建：手动 → 流程化 → 产品化 | [衍生](https://skills.sh/slavingia/skills/mvp) |
| 销售 | `founder-sales` | 创始人销售：信任建立、Pitch 打磨、心理突破 | [衍生](https://skills.sh/refoundai/lenny-skills/founder-sales) |
| 融资 | `fundraising-guide` | 融资指南：Pitch Deck、投资人关系、交割策略 | [衍生](https://skills.sh/refoundai/lenny-skills/fundraising) |

## 快速开始

```bash
# 安装全部创业技能
npx skills add skills-repo/startup-founder -g -y

# 或按需安装单个技能
npx skills add skills-repo/startup-founder@idea-validator -g -y
npx skills add skills-repo/startup-founder@mvp-builder -g -y
npx skills add skills-repo/startup-founder@founder-sales -g -y
npx skills add skills-repo/startup-founder@fundraising-guide -g -y
```

## 深层 Playbook（整库安装才带）

`references/` 里放的是子技能装不下的**判断层**内容——量化门槛、证据分级、止损判据：

| Playbook | 解决什么 |
|----------|---------|
| [references/validation-methodology.md](references/validation-methodology.md) | 三问前置、商业数学速算、证据强度 5 档与通过线、转向 vs 止损决策树 |
| [references/fundraising-readiness.md](references/fundraising-readiness.md) | 就绪五项、单位经济分档（LTV:CAC / 回收期 / 留存 / Burn Multiple）、Runway 决策线、轮次门槛 |

## 推荐工作流

```
点子验证 → MVP 构建 → 创始人销售 → 融资准备
idea-       mvp-        founder-     fundraising-
validator   builder     sales        guide
```

## 许可

MIT