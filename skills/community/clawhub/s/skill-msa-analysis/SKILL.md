---
name: MSA分析技能
slug: msa-analysis
displayName: MSA分析技能
description: 辅助完成测量系统分析(MSA)，支持Gage R&R、偏倚、线性、稳定性分析；当用户需要进行测量系统评估、了解测量系统准确性、生成MSA分析报告时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# MSA测量系统分析

## 任务目标
- 本Skill用于：帮助用户完成完整的测量系统分析(MSA)流程，从需求识别到报告输出
- 能力包含：Gage R&R分析、偏倚分析、线性分析、稳定性分析、交互式需求引导、数据收集指导、HTML报告生成
- 触发条件：用户提到"MSA"、"测量系统分析"、"量具分析"、"R&R"等关键词，或需要评估测量系统准确性时

## 前置准备
- 依赖说明：以下Python包已预先安装
  ```
  pandas==2.0.3
  numpy==1.24.3
  matplotlib==3.7.2
  openpyxl==3.1.2
  ```

## 操作步骤

### 步骤1：识别用户场景（智能体处理）
通过交互式问答确定用户需求：

**问题清单**：
1. 您的测量系统是什么类型？（例如：卡尺、天平、显微镜、测试设备等）
2. 您需要进行哪种类型的MSA分析？
   - Gage R&R（重复性和再现性）
   - 偏倚分析
   - 线性分析
   - 稳定性分析
   - 综合分析
3. 您对MSA熟悉程度如何？
   - 不熟悉，需要完整指导
   - 了解基本概念，需要分析支持
   - 熟悉，直接开始分析

**根据用户响应分路径**：
- **路径A：用户不熟悉MSA** → 进入步骤2（方案设计和数据收集指导）
- **路径B：用户熟悉MSA** → 进入步骤3（直接数据确认和分析）

### 步骤2：方案设计和数据收集指导（智能体处理）

#### 2.1 推荐实验方案
根据测量类型和分析类型推荐参数：

**Gage R&R标准方案**：
- 样本数：10个
- 操作员数：3个
- 测量次数：3次
- 总测量点：10×3×3=90个

**偏倚分析方案**：
- 样本数：1个（已知参考值）
- 测量次数：≥15次
- 操作员数：1个

**线性分析方案**：
- 样本数：5个（覆盖测量范围）
- 测量次数：每个样本≥12次
- 操作员数：1个

**稳定性分析方案**：
- 样本数：1个
- 测量间隔：按天/周/月
- 测量次数：≥20次

提供详细的测量注意事项和随机化要求。

#### 2.2 提供数据收集模板
向用户说明数据格式要求：
- 参考 `references/data_template.md` 中的详细格式说明
- 提供Excel/CSV模板示例
- 说明必需字段：样本编号、操作员、测量次数、测量值

### 步骤3：数据确认和解析（脚本处理）

用户上传数据文件后：

#### 3.1 调用数据解析脚本
```python
python scripts/parse_data.py --data_file <文件路径> --analysis_type <分析类型>
```

该脚本将：
- 验证数据格式
- 提取基本信息（样本数、操作员数、测量次数）
- 返回解析后的数据结构

#### 3.2 确认参数
向用户确认：
- 分析类型
- 样本数量
- 操作员数量
- 测量次数
- 测量单位

### 步骤4：执行分析（脚本处理）

根据分析类型调用相应脚本：

**Gage R&R分析**：
```python
python scripts/gage_rr.py --data <解析数据> --alpha 0.05
```

**偏倚分析**：
```python
python scripts/bias_analysis.py --data <解析数据> --reference_values [值列表]
```

**线性分析**：
```python
python scripts/linearity_analysis.py --data <解析数据> --reference_values [值列表]
```

**稳定性分析**：
```python
python scripts/stability_analysis.py --data <解析数据> --time_points [时间点列表]
```

### 步骤5：生成图表（脚本处理）

```python
python scripts/generate_charts.py --analysis_results <分析结果> --chart_type <图表类型>
```

支持的图表类型：
- 均值图（mean_chart）
- 极差图（range_chart）
- 贡献占比图（contribution_pie）
- 偏倚线性图（bias_linearity）
- 稳定性控制图（stability_control）

### 步骤6：生成HTML报告（脚本处理）

```python
python scripts/generate_report.py --analysis_results <分析结果> --charts <图表> --metadata <元数据>
```

报告包含：
- 分析摘要和结论
- 详细统计指标
- 可视化图表（Base64内嵌）
- 判定标准和改进建议

### 步骤7：结果解读（智能体处理）

基于分析结果，向用户说明：
- 测量系统是否可接受
- 主要问题在哪里（重复性、再现性、偏倚等）
- 改进建议
- 下一步行动

## 资源索引
- **数据解析脚本**：见 `scripts/parse_data.py`（用途：解析Excel/CSV数据，验证格式）
- **Gage R&R分析**：见 `scripts/gage_rr.py`（用途：计算EV、AV、GRR、%GRR、ndc等指标）
- **偏倚分析**：见 `scripts/bias_analysis.py`（用途：计算偏倚及其显著性）
- **线性分析**：见 `scripts/linearity_analysis.py`（用途：分析偏倚与测量范围的关系）
- **稳定性分析**：见 `scripts/stability_analysis.py`（用途：分析测量系统随时间的变化）
- **图表生成**：见 `scripts/generate_charts.py`（用途：生成各类统计图表并返回Base64编码）
- **报告生成**：见 `scripts/generate_report.py`（用途：组装HTML报告，内嵌图表）
- **MSA概念**：见 `references/msa_concepts.md`（何时读取：需要向用户解释MSA概念时）
- **数据模板**：见 `references/data_template.md`（何时读取：指导用户准备数据时）
- **分析方法**：见 `references/analysis_methods.md`（何时读取：需要解释计算原理时）
- **报告模板**：见 `assets/report_template.html`（用途：HTML报告的基础模板）

## 注意事项
- 交互式引导时，保持友好的沟通风格，避免使用过多专业术语
- 数据格式验证严格，确保用户数据符合要求后再进行分析
- 分析结果要结合实际业务场景进行解读，避免仅给出数字
- HTML报告为单文件，可直接在浏览器中打开
- 所有图表均为内嵌Base64编码，无需外部文件

## 使用示例

### 示例1：用户不熟悉MSA
**用户**："我需要做MSA分析，但是不太清楚怎么做"

**流程**：
1. 智能体通过问答了解：测量卡尺、需要Gage R&R分析
2. 智能体推荐：10个样本、3个操作员、每个样本测3次
3. 提供Excel数据模板
4. 用户完成测量并上传数据
5. 调用 `parse_data.py` 解析数据
6. 调用 `gage_rr.py` 执行分析
7. 调用 `generate_charts.py` 生成图表
8. 调用 `generate_report.py` 生成HTML报告
9. 智能体解读结果：%GRR=8.2%，测量系统可接受，建议定期复查

### 示例2：用户熟悉MSA
**用户**："我有Gage R&R数据，直接帮我分析一下"（上传Excel文件）

**流程**：
1. 调用 `parse_data.py` 解析数据，确认参数
2. 调用 `gage_rr.py` 执行分析
3. 调用 `generate_charts.py` 生成图表
4. 调用 `generate_report.py` 生成HTML报告
5. 返回报告并简要说明关键结论

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
