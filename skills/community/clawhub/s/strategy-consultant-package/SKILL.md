# Strategy Consultant Skill

> 战略顾问技能 - 外部洞察、战略分析、商业文档、专家库

## 版本

v2.0.0 - 新增 Brave 搜索集成

## 新增：Brave 搜索引擎集成

战略顾问现已集成 Brave 搜索引擎，支持实时市场情报获取：

| 场景 | 搜索类型 | 输出 |
|------|----------|------|
| **市场调研** | 行业报告、市场规模 | `market-analysis.md` |
| **竞品分析** | 竞品动态、融资新闻 | `competitor-report.md` |
| **专家背景** | 专家观点、近期动态 | `expert-brief.md` |
| **商业模式** | 对标案例、最佳实践 | `business-cases.md` |
| **Benchmark** | 行业数据、标杆对比 | `benchmark-data.md` |

### 搜索指令

```
/search market [行业]      # 市场规模分析
/search compete [公司]     # 竞品分析
/search expert [姓名]      # 专家背景调研
/search trend [话题]       # 行业趋势
```

## 包含内容

| 模块 | 说明 |
|------|------|
| **角色定义** | 战略顾问完整SOUL + TOOL |
| **专家库** | 50+专家，6大领域 |
| **模板库** | 访谈提纲、Benchmark报告、财务模型等 |

## 使用方式

### 方式一：独立使用

```
/strategy-consultant/interview    # 启动外部访谈
/strategy-consultant/benchmark    # 行业Benchmark分析
/strategy-consultant/bp           # 撰写商业计划书
/strategy-consultant/finance      # 财务预测
```

### 方式二：与产品研发运营体系集成

在产品研讨会前，战略顾问提供：
- `insights.md` - 外部洞察汇总
- `benchmark-report.md` - 行业Benchmark报告
- `business-model-canvas.md` - 商业模式画布
- `financial-summary.md` - 财务预测摘要
- `strategic-recommendations.md` - 战略建议

## 文档结构

```
strategy-consultant/
├── SKILL.md                    # 本文件
├── README.md                   # 说明文档
├── package.json                # 技能配置
├── agents/
│   └── strategy-consultant.md  # 角色完整定义
├── templates/
│   ├── external-interview-template.md
│   ├── benchmark-template.md
│   ├── bp-template.md
│   └── financial-model-template.xlsx
└── expert-library.md           # 专家库（50+专家）
```

## 核心能力

1. **外部洞察**：客户访谈、市场研究、竞争分析
2. **战略分析**：Benchmark、商业模式验证、战略规划
3. **商业文档**：BP撰写、财务预测、路演材料
4. **专家网络**：50+跨领域专家库

## 快捷指令

| 指令 | 功能 |
|------|------|
| `/interview` | 创建外部客户访谈计划 |
| `/insights` | 查看/更新外部洞察汇总 |
| `/market` | 市场规模分析 |
| `/compete` | 竞争格局分析 |
| `/business` | 商业模式验证 |
| `/benchmark` | 行业Benchmark分析 |
| `/bp` | 撰写/更新商业计划书 |
| `/finance` | 财务预测模型 |
| `/expert list` | 列出专家库专家 |
| `/expert call [ID]` | 调用指定专家 |
| `/expert topic [话题]` | 按话题调用专家 |
