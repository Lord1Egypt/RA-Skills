# Strategy Consultant Skill

> 战略顾问技能 - 外部洞察、战略分析、商业文档、专家库

## 一句话定位

**产品的"外部大脑"**，提供外部视角和战略高度，确保做正确的事。

## 核心能力

| 能力 | 说明 | 输出 |
|------|------|------|
| **外部洞察** | 客户访谈、市场研究、竞争分析 | 洞察报告 |
| **战略分析** | Benchmark、商业模式验证、战略规划 | 战略分析报告 |
| **商业文档** | BP撰写、财务预测、路演材料 | BP + PPT + 财务模型 |
| **专家支持** | 50+专家库，6大领域 | 专家意见 |

## 使用方式

### 方式一：独立使用

```bash
# 外部客户访谈
/strategy-consultant/interview

# 行业Benchmark分析
/strategy-consultant/benchmark

# 撰写商业计划书
/strategy-consultant/bp

# 财务预测
/strategy-consultant/finance

# 调用专家库
/strategy-consultant/expert list [领域]
/strategy-consultant/expert call [ID]
/strategy-consultant/expert topic [话题]
```

### 方式二：与 product-dev-ops 集成

**使用场景**：为产品研发运营体系的研讨会提供战略输入

**输出位置**：`00-work/interview/workshop/`

**标准输出文件**：
```
00-work/interview/workshop/
├── insights.md                    # 外部洞察汇总（必须）
├── benchmark-report.md            # 行业Benchmark报告（推荐）
├── business-model-canvas.md       # 商业模式画布（推荐）
├── financial-summary.md           # 财务预测摘要（推荐）
├── strategic-recommendations.md   # 战略建议（必须）
└── workshop-agenda.md             # 研讨会议程建议（可选）
```

**集成流程**：
```
product-dev-ops: /开工 项目名
    ↓
product-dev-ops: 产品经理访谈
    ↓
strategy-consultant: 外部访谈 + 战略分析
    ├── interview
    ├── benchmark
    └── bp
    ↓
输出到 00-work/interview/workshop/
    ↓
product-dev-ops: /研讨（自动检测并加载战略输入）
    ↓
product-dev-ops: /freeze
```

**自动检测机制**：
当 product-dev-ops 执行 `/研讨` 时，自动检测 `00-work/interview/workshop/` 目录：
- 如有战略顾问输入 → 自动加载到研讨会
- 如缺少必需文件 → 提示建议启用 strategy-consultant

详见：[product-dev-ops 战略顾问集成指南](https://github.com/openclaw/skills/product-dev-ops/docs/strategy-integration-guide.md)

## 何时使用？

| 场景 | 建议 |
|------|------|
| 全新业务方向 | ✅ 强烈建议 |
| 需要融资 | ✅ 强烈建议 |
| 复杂商业模式 | ✅ 强烈建议 |
| 高度竞争市场 | ✅ 强烈建议 |
| 内部工具/系统 | ⚠️ 可选 |
| 快速迭代试错 | ⚠️ 可选 |
| 技术重构 | ❌ 通常不需要 |

## 快速导航

| 文档 | 说明 |
|------|------|
| [SKILL.md](./SKILL.md) | 技能主文档 |
| [agents/strategy-consultant.md](./agents/strategy-consultant.md) | 角色完整定义 |
| [expert-library.md](./expert-library.md) | 专家库（50+专家） |

## 版本

v1.0.0 - 独立战略顾问技能包
