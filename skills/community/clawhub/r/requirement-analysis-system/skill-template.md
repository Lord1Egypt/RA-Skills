# 需求分析技能系统 - 技能模板

> 版本：v1.0.0  
> 用途：批量创建技能时的模板参考

---

## 技能元数据模板 (_meta.json)

```json
{
  "name": "{{slug}}",
  "displayName": "{{name}}",
  "version": "1.0.0",
  "description": "{{description}}",
  "author": "Elatia (基于 Product-Manager-Skills 提炼)",
  "license": "MIT",
  "tags": ["requirement-analysis", "{{slug}}", "product-management", "{{type}}"],
  "category": "Product Management",
  "type": "{{type}}",
  "parentSkill": "requirement-analysis-system",
  "createdAt": "2026-03-09T15:15:00+08:00",
  "updatedAt": "2026-03-09T15:15:00+08:00"
}
```

---

## 技能文件模板 (SKILL.md)

```markdown
# {{name}} ({{slug}})

> 版本：v1.0.0  
> 创建：2026-03-09  
> 作者：Elatia 🌀 (基于 Product-Manager-Skills 提炼)  
> 许可：MIT  
> 类型：{{type}} Skill

---

## 📋 技能描述

**面向场景**: {{scenario}}  
**目标用户**: {{users}}  
**核心价值**: {{value}}

---

## 🎯 核心能力

### 1. {{capacity1}}
{{description1}}

### 2. {{capacity2}}
{{description2}}

### 3. {{capacity3}}
{{description3}}

---

## 🔧 使用方式

### 方式 1: 交互式引导

```markdown
/{{slug}}
```

**引导问题**:

**1. [问题 1]**
> [描述]

**2. [问题 2]**
> [描述]

**3. [问题 3]**
> [描述]

---

### 方式 2: 快速模式

```markdown
/{{slug}} quick \
  --param1 "值 1" \
  --param2 "值 2"
```

---

## 📝 输出模板

```markdown
# {{name}} 输出

## [章节 1]
[内容]

## [章节 2]
[内容]

## [章节 3]
[内容]
```

---

## 📚 示例

### 示例 1: [示例名称]

```markdown
[示例内容]
```

---

## 🎯 质量标准

### 好的 {{name}}
- ✅ [标准 1]
- ✅ [标准 2]
- ✅ [标准 3]

### 常见陷阱
- ❌ [陷阱 1]
- ❌ [陷阱 2]
- ❌ [陷阱 3]

---

## 🔗 与其他技能的关系

| 技能 | 关系 | 使用时机 |
|------|------|----------|
| [技能 1] | 前置/后置 | [时机] |
| [技能 2] | 前置/后置 | [时机] |

---

## 📈 成功指标

| 指标 | 目标值 | 测量方式 |
|------|--------|----------|
| [指标 1] | ≥90% | [方式] |
| [指标 2] | ≥4/5 | [方式] |

---

## 🔖 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-03-09 | 初始版本，基于 Product-Manager-Skills 提炼 |

---

## 📄 许可

MIT License

---

*基于 Product-Manager-Skills by Dean Peters · CC BY-NC-SA 4.0*  
*适配 OpenClaw 标准：Elatia 🌀*
```

---

## 技能配置清单

| Slug | 名称 | 类型 | 场景 | 用户 | 价值 |
|------|------|------|------|------|------|
| problem-statement | 问题定义 | component | 新项目启动/需求模糊 | PM/需求分析师 | 确保团队对问题达成共识 |
| proto-persona | 用户画像 | component | 缺乏研究数据/早期阶段 | PM/设计师 | 快速对齐目标用户 |
| customer-journey-map | 客户旅程地图 | component | 优化体验/识别断点 | PM/设计师 | 可视化完整互动过程 |
| jobs-to-be-done | JTBD 分析 | component | 需求表面化/创新探索 | PM/研究员 | 深度挖掘真实需求 |
| problem-framing-canvas | 问题框架画布 | interactive | 复杂问题/多方利益相关者 | PM/项目负责人 | 结构化探索避免偏见 |
| opportunity-solution-tree | 机会方案树 | interactive | 多需求优先级/方案探索 | PM/设计师 | 目标到方案系统拆解 |
| company-research | 客户调研 | component | B2B 售前/大客户开发 | 售前/PM | 深度分析客户公司 |
| feature-investment-advisor | 功能投资决策 | interactive | 大功能立项/资源取舍 | PM/负责人 | 评估 ROI |
| finance-based-pricing-advisor | 定价分析 | interactive | 新功能定价/价格调整 | PM/定价负责人 | 财务影响分析 |
| epic-hypothesis | 史诗假设 | component | 大型功能/项目立项 | PM/产品负责人 | 转化为可验证假设 |
| prd-development | PRD 开发 | workflow | 正式立项/跨团队对齐 | PM/产品负责人 | 端到端 PRD 创建 |

---

## 工作流配置清单

| Slug | 名称 | 场景 | 阶段 | 依赖技能 |
|------|------|------|------|----------|
| new-product-requirement | 新产品需求分析 | 从 0 到 1 新产品 | 问题定义→需求探索→方案设计→PRD | problem-statement, proto-persona, OST, prd-development |
| feature-iteration | 功能迭代优化 | 已有功能优化 | 数据分析→用户反馈→优先级→迭代 | user-story, prioritization-advisor, feature-investment |
| customer-request-analysis | 客户需求分析 | B2B 客户需求 | 客户调研→问题定义→方案匹配 | company-research, problem-statement, user-story |
| sprint-planning | Sprint 需求规划 | 敏捷 Sprint 规划 | 需求池→优先级→拆分→承诺 | prioritization-advisor, user-story, epic-hypothesis |
| prd-full-workflow | 完整 PRD 工作流 | 端到端 PRD | 问题定义→需求探索→方案设计→输出→整合 | 全部 11 个技能 |

---

*模板创建：Elatia 🌀 | 2026-03-09*
