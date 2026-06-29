---
name: saas-decision
description: SaaS产品辅助决策助手。用户输入SaaS产品行业与定位，自动从市场需求、用户画像、需求痛点、竞品格局、变现定价(MRR/ARR/LTV)、获客增长(CAC/PLG)、推广营销、成本结构、技术可行性9大维度进行综合分析，生成专业交互式HTML可行性决策报告。涵盖SaaS定价模型对比、MRR预估、LTV/CAC分析、多租户架构选型等SaaS专属议题。触发词：SaaS决策, SaaS可行性, SaaS评估, SaaS能不能做, 开发SaaS, SaaS分析报告, SaaS调研, 软件即服务决策, saas decision, SaaS选型, SaaS创业评估, 做SaaS产品。
version: 1.0.0
agent_created: true
metadata:
  openclaw:
    requires:
      bins:
        - python
      env: {}
      tools:
        - Read
        - Write
        - Bash
        - WebSearch
        - WebFetch
        - Edit
---

# SaaS 产品辅助决策助手

## 概述

本技能为 SaaS 产品开发提供专业的多维度可行性决策分析。用户只需提供 SaaS 产品行业和定位描述，系统自动完成市场调研、竞品分析、用户需求验证、SaaS 商业模式评估，生成专业的可视化 HTML 决策报告。

## 核心能力

1. **市场需求分析** - SaaS 市场规模、增长率、TAM/SAM 估算
2. **用户画像分析** - 目标用户特征、决策链、付费意愿
3. **需求痛点诊断** - 核心痛点强度、替代方案、需求迫切度
4. **竞品格局分析** - 直接/间接竞品、差异化空间、护城河潜力
5. **变现定价策略** - SaaS 定价模型（订阅制/用量制/Freemium/混合）、MRR/ARR 预估、LTV 估算
6. **获客增长分析** - CAC 估算、获客渠道效率、PLG 增长潜力
7. **推广营销策略** - 内容策略、品牌定位、分阶段推广规划
8. **成本结构分析** - 云成本、研发、第三方工具、营销预算
9. **技术可行性评估** - SaaS 架构选型（多租户/隔离策略）、技术栈、合规要求

## 使用方式

```
触发词 + SaaS产品行业 + 定位描述
```

示例：
- "SaaS决策：做一个面向中小电商的AI客服SaaS"
- "帮我评估做企业知识管理SaaS可行吗"
- "分析HR SaaS招聘模块的市场可行性"

## 工作流程

### 第一阶段：数据采集（并行搜索）

使用 WebSearch 工具并行搜索以下维度（每批次 3-4 个搜索）：

**批次1 — 市场与竞品：**
1. `{产品方向} SaaS 市场规模 2025 2026 增长趋势`
2. `{产品方向} SaaS 竞品 头部玩家 排行`
3. `{产品方向} SaaS 融资 行业报告`

**批次2 — 用户与需求：**
4. `{目标用户群体} {痛点关键词} 数字化 软件需求`
5. `{产品方向} SaaS 用户画像 使用场景`
6. `{产品方向} 定价模式 订阅 SaaS 价格`

**批次3 — 增长与竞争：**
7. `{产品方向} SaaS 获客 增长 PLG 策略`
8. `{产品方向} SaaS 推广 营销 案例`
9. `SaaS {产品方向} 开发 技术栈 架构`

### 第二阶段：深度分析（WebFetch）

对搜索结果中数据丰富的页面进行 WebFetch 获取详细信息：
- 行业报告页面（提取市场规模、增长率数据）
- 竞品官网（提取定价、功能、目标客户）
- 技术博客/案例（提取架构方案）

### 第三阶段：报告生成

基于搜索和 fetch 的数据，构建 JSON 数据并调用报告生成脚本：

```bash
python {baseDir}/scripts/report_generator.py \
  --name "产品名称" \
  --category "行业/方向" \
  --output "output_path.html" \
  --scores '{"market_demand": 80, "user_profile": 70, ...}' \
  --market-demand '{"score": 80, "market_size": "500亿", ...}' \
  --user-profile '{"score": 70, "target": "...", ...}' \
  --pain-points '{"score": 75, "items": [...], ...}' \
  --competition '{"score": 65, "direct_count": "15+", ...}' \
  --monetization '{"score": 75, "pricing_model": "...", ...}' \
  --acquisition '{"score": 70, "cac_estimate": "...", ...}' \
  --marketing '{"score": 72, "strategies": [...], ...}' \
  --cost-structure '{"score": 68, "cloud": "...", ...}' \
  --tech-feasibility '{"score": 75, "recommended_stack": "...", ...}' \
  --risks '{"items": [{"name": "...", "level": "高", "desc": "..."}]}'
```

或者直接在 Python 中调用：

```python
import json, sys
sys.path.insert(0, '{baseDir}/scripts')
from report_generator import generate_report

data = {
    "name": "产品名称",
    "category": "行业方向",
    "scores": {"market_demand": 80, "user_profile": 70, ...},
    "market_demand": {...},
    "user_profile": {...},
    "pain_points": {...},
    "competition": {...},
    "monetization": {...},
    "acquisition": {...},
    "marketing": {...},
    "cost_structure": {...},
    "tech_feasibility": {...},
    "risks": {...},
}

html = generate_report(data)
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## 报告结构

生成的 HTML 报告包含以下章节：

1. **封面页** - 产品名称、SaaS行业定位、报告时间
2. **综合评分卡** - 加权总分 + 决策建议
3. **多维度评分矩阵** - 9维度评分卡片可视化
4. **市场需求分析** - SaaS市场规模、TAM/SAM、增长趋势
5. **用户画像分析** - 目标用户、决策链、付费意愿
6. **需求痛点分析** - 痛点矩阵、替代方案、迫切度
7. **竞品格局分析** - 直接/间接竞品、头部对比表、差异机会
8. **变现定价策略** - SaaS定价模式对比、MRR/ARPU/LTV预估、定价梯度建议
9. **获客增长分析** - CAC估算、渠道效率对比、PLG评估
10. **推广营销策略** - 品牌定位、内容策略、分阶段规划时间线
11. **成本结构分析** - 云/研发/工具/营销成本、SaaS成本结构参考
12. **技术可行性评估** - 架构选型、多租户策略、合规、开发周期
13. **风险提示** - SaaS特有的PMF/流失/定价/获客风险
14. **综合决策建议** - SaaS核心优劣势、MVP行动路线图(P0/P1/P2)

## 评分模型

基于以下 9 个 SaaS 专属维度加权评分（满分 100）：

| 维度 | 权重 | 核心评估标准 |
|------|------|-------------|
| 📊 市场需求 | 15% | SaaS细分市场规模、年增长率、TAM/SAM、数字化渗透率 |
| 👥 用户画像 | 10% | 目标用户清晰度、B2B/B2C决策链、付费能力与意愿 |
| 🎯 需求痛点 | 10% | 痛点强度与频率、替代方案成熟度、需求迫切度 |
| ⚔️ 竞品格局 | 15% | 直接/间接竞品数量、市场饱和度、差异化空间、护城河潜力 |
| 💰 变现能力 | 15% | SaaS定价模式清晰度、ARPU预估、LTV潜力、客户付费习惯 |
| 📈 获客增长 | 10% | CAC合理性、PLG增长飞轮潜力、获客渠道多样性 |
| 📢 推广营销 | 15% | 内容营销空间、品牌定位差异化、SEO/社交传播潜力 |
| 💸 成本结构 | 5% | 云成本可控性、研发成本效率、盈利周期预估 |
| 🔧 技术可行性 | 5% | SaaS架构成熟度、多租户方案、安全合规、团队能力 |

评分等级：
- ≥80分：✅ **强烈建议做** — 市场需求强劲，竞争格局有利，SaaS商业模式清晰
- 65-79分：🟡 **谨慎推进** — 有机会但需差异化定位，建议先做用户验证
- 50-64分：⚠️ **暂缓观望** — 风险较高，需先验证核心假设后再决定
- <50分：❌ **不建议做** — 市场条件不利，建议调整方向或等待时机

## 注意事项

1. 所有数据基于公开信息搜索，时效性可能有限，建议结合一手调研
2. MRR/ARR/LTV等指标为基于行业benchmark的预估值，实际数据需上线后验证
3. 竞品分析基于公开可见信息，可能存在未公开的竞品
4. 最终决策需结合团队实际资源、行业经验和执行能力综合判断
5. SaaS创业核心风险：PMF不匹配、CAC过高、客户流失——这三个问题在报告中均有专项分析
