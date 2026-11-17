---
slug: esg-report-compiler
name: ESG报告技能
displayName: ESG报告技能
version: 1.1.0
author: org-jaxjwo0r
category: quality
description: 协助企业完成ESG报告全流程编制；支持ESG数据收集整理、GRI/TCFD标准框架映射、数据验证、多维度可视化及PDF/HTML报告导出；当用户需要编制/生成ESG报告、分析ESG绩效数据或准备可持续发展披露文件时使用
---

# ESG报告编制技能

## 任务目标

- 本Skill用于：企业ESG（环境、社会、治理）可持续发展报告的全流程编制
- 核心能力：
  1. ESG数据收集与结构化整理
  2. 国际标准框架映射（GRI、TCFD）
  3. 数据完整性验证与合规检查
  4. 多维度可视化图表生成
  5. PDF/HTML格式报告导出
- 触发条件：用户要求编制ESG报告、分析ESG数据、准备GRI/TCFD披露文件

## 前置准备

- 依赖说明：pandas（数据处理）、matplotlib（图表生成）、reportlab（PDF生成）
- 非标准文件准备：企业ESG数据（CSV/Excel格式），参考references/esg_data_template.csv获取数据模板

## 操作步骤

### 完整工作流程

```
1. 数据收集 → 2. 数据验证 → 3. 可视化生成 → 4. 报告导出
```

### 步骤1：ESG数据收集与整理

使用数据采集脚本将分散的ESG数据整合为结构化JSON格式。

- 脚本调用：`python scripts/esg_data_collector.py --input <数据文件>`
- 支持格式：CSV、Excel
- 输出：JSON格式的结构化数据

**生成数据模板（首次使用）：**
```bash
python scripts/esg_data_collector.py --generate-template --output esg_data_template.csv
```

### 步骤2：数据核对与验证

按照GRI标准对数据进行完整性检查与合规性校验。

- 脚本调用：`python scripts/esg_validator.py --input <收集后的JSON文件> --standard GRI`
- 支持标准：GRI（默认）、TCFD、SASB
- 输出：验证报告（包含错误、警告、完整性得分）

**验证项包括：**
- 必需指标完整性检查
- 数值范围合理性验证
- 跨指标一致性检查

### 步骤3：多维度数据可视化

生成直观的ESG绩效图表。

- 脚本调用：`python scripts/esg_visualizer.py --input <数据文件> --output-dir <图表目录>`
- 输出图表类型：
  - 各维度柱状图
  - 维度构成饼图
  - ESG综合雷达图
  - 指标趋势图
  - 与行业基准对比图

### 步骤4：报告导出

生成符合格式要求的最终报告。

- 脚本调用：`python scripts/esg_exporter.py --input <数据文件> --output <报告文件> --format <pdf|html> --company <公司名称>`
- 支持格式：PDF（正式报告）、HTML（网页版）

## 使用示例

### 示例1：首次编制ESG报告

- 场景/输入：企业首次编制年度ESG报告，需要收集并整理全年ESG数据
- 预期产出：结构化ESG数据集、验证报告、可视化图表、最终PDF报告
- 关键要点：
  1. 先使用`--generate-template`生成标准数据模板
  2. 按模板格式填写企业实际数据
  3. 按流程依次执行：收集→验证→可视化→导出

### 示例2：季度ESG数据分析

- 场景/输入：分析Q2季度ESG绩效，与行业基准对比
- 预期产出：数据可视化图表、对比分析报告
- 关键要点：
  - 只需执行可视化步骤
  - 使用HTML格式便于内部分享

### 示例3：GRI标准合规检查

- 场景/输入：核查现有ESG数据是否符合GRI Standards要求
- 预期产出：验证报告，指出缺失的必需指标
- 关键要点：
  - 使用`--standard GRI`参数
  - 关注验证报告中的errors和warnings

## 资源索引

- 数据收集脚本：见 [scripts/esg_data_collector.py](scripts/esg_data_collector.py)（用途：数据收集整理、模板生成；参数：--input/--output/--generate-template）
- 数据验证脚本：见 [scripts/esg_validator.py](scripts/esg_validator.py)（用途：数据完整性验证、GRI合规检查；参数：--input/--standard）
- 可视化脚本：见 [scripts/esg_visualizer.py](scripts/esg_visualizer.py)（用途：生成ESG图表；参数：--input/--output-dir/--type）
- 报告导出脚本：见 [scripts/esg_exporter.py](scripts/esg_exporter.py)（用途：生成PDF/HTML报告；参数：--input/--output/--format/--company）
- GRI标准参考：见 [references/gri_standards.md](references/gri_standards.md)（何时读取：编制GRI标准报告时）
- TCFD框架参考：见 [references/tcfd_framework.md](references/tcfd_framework.md)（何时读取：气候相关披露时）
- 数据模板：见 [references/esg_data_template.csv](references/esg_data_template.csv)（何时读取：首次录入数据或了解指标定义时）

## 注意事项

- 数据模板中的指标ID不可修改，脚本依赖这些ID进行数据映射
- PDF报告生成依赖reportlab库，确保已正确安装
- 可视化脚本默认生成中文字体，如遇字体问题检查matplotlib配置
- 验证步骤建议在可视化前执行，确保数据质量后再生成图表
- 报告导出时需指定公司名称，否则使用默认名称"示例企业"
- 变更记录：V1.1.0：完善 TRACE 五维度测评体系，补充触发条件、能力边界、异常处理与 TRACE 自评表

## 能力边界

- **适用场景**：质量管理体系中涉及ESG报告编制技能的场景，需要生成标准化文档或分析
- **不适配场景**：法律法规正式解释、专业认证替代、涉及人身安全的紧急决策
- **输入要求**：需提供明确的参数和要求，脚本依赖需预先安装，Python 3.9+


## 异常处理

- **输入不完整**：提示用户补充缺失的关键信息，列出必需字段，引导用户逐步完善输入
- **依赖缺失**：检测依赖环境（Python库、系统工具），给出明确的安装指令和验证方法
- **执行失败**：输出清晰的错误信息和可能的原因，提供降级方案（如无法生成 PNG 则输出 SVG）
- **结果验证**：输出完成后提供校验方法，建议用户确认关键内容的准确性


## TRACE 五维度自评

| 维度 | 得分 | 自评说明 |
|------|------|----------|
| **Trust 信任度** | 8/10 | SKILL.md 结构化清晰，描述完整，触发条件明确，使用者可信任输出质量 |
| **Reliability 可靠性** | 8/10 | 包含使用示例和注意事项，输出格式统一，有脚本支撑的可复现能力 |
| **Adaptability 适配性** | 7/10 | 适应多种相关输入场景，提供参数化配置和脚本 支持 |
| **Convention 惯例性** | 8/10 | 遵循 SKILL.md 标准结构，frontmatter 完整，资源索引清晰 |
| **Effectiveness 有效性** | 8/10 | 端到端完成任务，脚本自动化提升执行效率 |
| **总分** | **39/50** | 基本合格 |
