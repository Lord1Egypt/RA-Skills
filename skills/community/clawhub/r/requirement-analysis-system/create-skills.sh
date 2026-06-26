#!/bin/bash

# 需求分析技能系统 - 批量创建脚本
# 创建 11 个独立技能 + 5 个工作流技能

set -e

BASE_DIR="/root/.openclaw/workspace/skills/requirement-analysis-system"
SKILLS_DIR="$BASE_DIR/skills"
WORKFLOWS_DIR="$BASE_DIR/workflows"

echo "=== 需求分析技能系统 - 批量创建 ==="
echo "基础目录：$BASE_DIR"

# 技能列表
declare -A SKILLS=(
    ["problem-statement"]="问题定义|Component|从用户视角清晰定义问题，使用同理心驱动的问题陈述框架"
    ["proto-persona"]="用户画像|Component|快速创建假设性用户画像，对齐目标用户特征"
    ["customer-journey-map"]="客户旅程地图|Component|可视化用户与品牌的完整互动过程，识别体验断点"
    ["jobs-to-be-done"]="JTBD 分析|Component|深度挖掘用户真实需求，探索功能/社会/情感工作"
    ["problem-framing-canvas"]="问题框架画布|Interactive|结构化问题探索，使用 MITRE 框架避免认知偏见"
    ["opportunity-solution-tree"]="机会方案树|Interactive|从目标到方案的系统拆解，Teresa Torres OST 方法"
    ["company-research"]="客户调研|Component|深度分析目标客户公司，B2B 售前支持"
    ["feature-investment-advisor"]="功能投资决策|Interactive|评估功能投资的 ROI，收益 - 成本 - 风险三维分析"
    ["finance-based-pricing-advisor"]="定价分析|Interactive|基于财务影响的定价决策，定价 - 财务模型联动"
    ["epic-hypothesis"]="史诗假设|Component|将大型需求转化为可验证假设，If/Then 结构"
    ["prd-development"]="PRD 开发|Workflow|端到端的 PRD 创建流程，多技能编排"
)

# 工作流列表
declare -A WORKFLOWS=(
    ["new-product-requirement"]="新产品需求分析|从 0 到 1 的新产品需求分析全流程"
    ["feature-iteration"]="功能迭代优化|已有功能的需求迭代和持续优化"
    ["customer-request-analysis"]="客户需求分析|B2B 场景的客户需求快速分析"
    ["sprint-planning"]="Sprint 需求规划|敏捷 Sprint 规划中的需求优先级和拆分"
    ["prd-full-workflow"]="完整 PRD 工作流|从问题定义到 PRD 输出的端到端流程"
)

echo ""
echo "📦 开始创建技能文件..."

for slug in "${!SKILLS[@]}"; do
    IFS='|' read -r name type desc <<< "${SKILLS[$slug]}"
    echo "  创建：$slug ($name)"
    
    # 创建 SKILL.md 模板
    cat > "$SKILLS_DIR/$slug/SKILL.md" << 'SKILL_TEMPLATE'
# {{NAME}} ({{SLUG}})

> 版本：v1.0.0  
> 创建：2026-03-09  
> 作者：Elatia 🌀 (基于 Product-Manager-Skills 提炼)  
> 许可：MIT  
> 类型：{{TYPE}} Skill

---

## 📋 技能描述

**面向场景**: [场景描述]  
**目标用户**: [用户群体]  
**核心价值**: [价值主张]

---

## 🎯 核心能力

### 1. [能力 1]
[能力描述]

### 2. [能力 2]
[能力描述]

### 3. [能力 3]
[能力描述]

---

## 🔧 使用方式

### 方式 1: 交互式引导

```markdown
/{{SLUG}}
```

**引导问题**:

**1. [问题 1]**
> [问题描述]

**2. [问题 2]**
> [问题描述]

**3. [问题 3]**
> [问题描述]

---

### 方式 2: 快速模式

```markdown
/{{SLUG}} quick \
  --param1 "值 1" \
  --param2 "值 2"
```

---

## 📝 输出模板

```markdown
# {{NAME}} 输出

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

### 好的 [技能名]
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
SKILL_TEMPLATE

    # 替换模板变量
    sed -i "s/{{SLUG}}/$slug/g" "$SKILLS_DIR/$slug/SKILL.md"
    sed -i "s/{{NAME}}/$name/g" "$SKILLS_DIR/$slug/SKILL.md"
    sed -i "s/{{TYPE}}/$type/g" "$SKILLS_DIR/$slug/SKILL.md"
    
    # 创建 _meta.json
    cat > "$SKILLS_DIR/$slug/_meta.json" << META_TEMPLATE
{
  "name": "$slug",
  "displayName": "$name",
  "version": "1.0.0",
  "description": "$desc",
  "author": "Elatia (基于 Product-Manager-Skills 提炼)",
  "license": "MIT",
  "tags": ["requirement-analysis", "$slug", "product-management", "${type,,}"],
  "category": "Product Management",
  "type": "${type,,}",
  "parentSkill": "requirement-analysis-system",
  "createdAt": "2026-03-09T15:15:00+08:00",
  "updatedAt": "2026-03-09T15:15:00+08:00"
}
META_TEMPLATE

done

echo ""
echo "🔄 开始创建工作流技能..."

for slug in "${!WORKFLOWS[@]}"; do
    IFS='|' read -r name desc <<< "${WORKFLOWS[$slug]}"
    echo "  创建：$slug ($name)"
    
    # 创建工作流 SKILL.md
    cat > "$WORKFLOWS_DIR/$slug/SKILL.md" << WORKFLOW_TEMPLATE
# $name ($slug)

> 版本：v1.0.0  
> 创建：2026-03-09  
> 作者：Elatia 🌀  
> 许可：MIT  
> 类型：Workflow Skill

---

## 📋 技能描述

**面向场景**: $desc  
**目标用户**: 产品经理、需求分析师、项目负责人  
**核心价值**: 端到端的工作流编排，自动化多技能协作

---

## 🎯 工作流阶段

### 阶段 1: [阶段名] (时间)
1. 运行 [技能 1]
2. 运行 [技能 2]
3. 输出：[产出物]

### 阶段 2: [阶段名] (时间)
1. 运行 [技能 3]
2. 运行 [技能 4]
3. 输出：[产出物]

### 阶段 3: [阶段名] (时间)
1. 运行 [技能 5]
2. 输出：[产出物]

---

## 🔧 使用方式

### 方式 1: 完整工作流

```markdown
/$slug
```

### 方式 2: 分阶段执行

```markdown
/$slug phase1 --params "..."
/$slug phase2 --params "..."
```

---

## 📝 输出模板

```markdown
# $name 输出

## 阶段 1 产出
[内容]

## 阶段 2 产出
[内容]

## 阶段 3 产出
[内容]
```

---

## 📚 示例

### 示例 1: [示例名称]

[示例内容]

---

## 🔗 依赖技能

| 技能 | 阶段 | 用途 |
|------|------|------|
| [技能 1] | 阶段 1 | [用途] |
| [技能 2] | 阶段 2 | [用途] |

---

## 📈 成功指标

| 指标 | 目标值 | 测量方式 |
|------|--------|----------|
| 执行效率 | 提升 50% | 时间对比 |
| 输出质量 | ≥4/5 | 评审打分 |

---

## 🔖 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-03-09 | 初始版本 |

---

## 📄 许可

MIT License

---

*创建者：Elatia 🌀*
WORKFLOW_TEMPLATE

    # 创建 _meta.json
    cat > "$WORKFLOWS_DIR/$slug/_meta.json" << META_TEMPLATE
{
  "name": "$slug",
  "displayName": "$name",
  "version": "1.0.0",
  "description": "$desc",
  "author": "Elatia",
  "license": "MIT",
  "tags": ["requirement-analysis", "workflow", "$slug", "product-management"],
  "category": "Product Management",
  "type": "workflow",
  "parentSkill": "requirement-analysis-system",
  "createdAt": "2026-03-09T15:15:00+08:00",
  "updatedAt": "2026-03-09T15:15:00+08:00"
}
META_TEMPLATE

done

echo ""
echo "✅ 技能系统创建完成！"
echo ""
echo "📁 目录结构:"
tree -L 3 "$BASE_DIR" || find "$BASE_DIR" -type f -name "*.md" -o -name "*.json" | head -30

echo ""
echo "📊 统计:"
echo "  技能数量：${#SKILLS[@]}"
echo "  工作流数量：${#WORKFLOWS[@]}"
echo "  总计：$((${#SKILLS[@]} + ${#WORKFLOWS[@]})) 个技能"
