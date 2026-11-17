---
name: 质量成本分析技能
slug: quality-cost-analysis
displayName: 质量成本分析技能
description: 自动化质量成本分析工具，支持Excel/CSV多Sheet数据读取、智能列识别、数据清洗、四大分类计算、自动图表选择和HTML报告输出；当用户需要质量成本分析、成本结构拆解、趋势分析或质量成本报告时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 质量成本分析 Skill

## 任务目标
- 本 Skill 用于：自动化质量成本分析全流程，从数据读取到报告生成
- 能力包含：多格式数据读取、智能数据清洗、四大分类计算、自动图表选择、HTML 报告生成
- 触发条件：用户需要分析质量成本、生成质量成本报告、识别质量成本结构或趋势时

## 前置准备
- 依赖说明：脚本所需的依赖包
  ```
  pandas>=2.0.0
  openpyxl>=3.1.0
  plotly>=5.14.0
  jinja2>=3.1.0
  ```

## 操作步骤
- 标准流程：
  1. **数据读取与预处理**
     - 调用 `scripts/data_processor.py` 读取 Excel/CSV 文件，自动扫描所有 sheet
     - 脚本将智能识别金额、日期、分类等关键列，并自动清洗空值和异常值
     - 返回清洗后的数据框和列类型标注

  2. **质量成本计算**
     - 调用 `scripts/calculator.py` 基于清洗后的数据计算质量成本四大分类
     - 脚本将智能识别预防成本、鉴定成本、内部损失成本、外部损失成本
     - 返回分类汇总、占比分析、趋势数据等计算结果

  3. **图表生成**
     - 调用 `scripts/chart_generator.py` 根据计算结果自动选择图表类型
     - 脚本将生成交互式图表（饼图、折线图、柱状图等）
     - 返回图表 HTML 代码

  4. **报告生成**
     - 调用 `scripts/report_generator.py` 生成 HTML 报告
     - 报告包含数据摘要、分类分析、趋势分析、图表展示
     - 返回报告文件路径

  5. **智能分析建议**
     - 根据 [references/quality_cost_framework.md](references/quality_cost_framework.md) 中的框架
     - 分析质量成本结构，识别异常点
     - 基于分析结果生成优化建议

- 可选分支：
  - 当数据为单时期：生成结构分析报告，重点展示四大分类占比
  - 当数据为多时期：生成趋势分析报告，展示质量成本变化趋势
  - 当数据异常值较多：在报告中标注异常数据并提供解读

## 资源索引
- 必要脚本：
  - [scripts/data_processor.py](scripts/data_processor.py) - 数据读取与智能清洗
  - [scripts/calculator.py](scripts/calculator.py) - 质量成本计算与分类
  - [scripts/chart_generator.py](scripts/chart_generator.py) - 自动图表生成
  - [scripts/report_generator.py](scripts/report_generator.py) - HTML 报告生成
- 领域参考：
  - [references/quality_cost_framework.md](references/quality_cost_framework.md) - 质量成本分析框架与四大分类定义
  - [references/chart_selection_rules.md](references/chart_selection_rules.md) - 图表类型选择规则
- 输出资产：
  - [assets/report_template.html](assets/report_template.html) - HTML 报告模板

## 注意事项
- 脚本会自动处理多 sheet Excel 文件，无需手动指定 sheet 名称
- 脚本会智能识别列类型，即使列名不规范也能处理
- 生成的 HTML 报告为单文件，内嵌 CSS 和图表代码，直接用浏览器打开即可
- 图表选择基于数据特征自动完成，无需手动指定图表类型

## 使用示例

### 示例 1：单时期质量成本分析
```bash
python scripts/data_processor.py --file ./data/quality_cost_2024.xlsx
python scripts/calculator.py --data ./output/cleaned_data.pkl
python scripts/chart_generator.py --result ./output/calculation_result.json
python scripts/report_generator.py --result ./output/calculation_result.json --charts ./output/charts.html --output ./reports/quality_cost_report.html
```

### 示例 2：多时期趋势分析
```bash
python scripts/data_processor.py --file ./data/quality_cost_multi_year.xlsx
python scripts/calculator.py --data ./output/cleaned_data.pkl --multi-period
python scripts/chart_generator.py --result ./output/calculation_result.json --type trend
python scripts/report_generator.py --result ./output/calculation_result.json --charts ./output/charts.html --output ./reports/trend_report.html
```

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
