---
name: QMS环境因素技能
slug: qms-environment-analysis
displayName: QMS环境因素技能
description: 基于QMS框架的内外部环境因素分析与可视化；用于ISO 9001质量管理体系内审/管理评审时识别机遇与风险、制定改进计划、生成SWOT/PESTEL分析报告
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# QMS环境因素分析技能

## 任务目标
- 本 Skill 用于：组织内外部环境因素的系统性分析，支撑质量管理体系（QMS）的战略决策与持续改进
- 能力包含：环境因素识别、内外部因素分析、SWOT/PESTEL可视化、问题诊断与改进建议
- 触发条件：管理评审准备、内审问题整改、新年度质量目标制定、体系换版升级

## 前置准备
- 依赖说明：matplotlib>=3.8.0（图表生成）、reportlab>=4.0.7（PDF报告）
- 数据准备：按分析维度收集相关因素清单（JSON格式）

## 操作步骤

### 一、环境因素识别方法

#### 1.1 内部环境因素分类

| 维度 | 关键要素 | 分析要点 |
|------|---------|---------|
| 组织治理 | 战略目标、价值观、质量方针 | 是否与QMS有效整合 |
| 质量管理文化 | 质量意识、员工参与度、培训体系 | 质量文化成熟度评估 |
| 资源配置 | 人力资源、基础设施、监视测量设备 | 是否满足质量目标需求 |
| 流程体系 | 过程识别、风险管控、绩效评价 | 流程效率与合规性 |
| 组织架构 | 职责权限、接口关系、沟通机制 | 质量职能是否有效运行 |
| 技术能力 | 工艺水平、创新能力、数字化程度 | 质量保证的技术支撑 |

#### 1.2 外部环境因素分类（PESTEL框架）

| 维度 | 关键要素 | 分析要点 |
|------|---------|---------|
| 政治(Political) | 法规政策、行业监管、国际贸易 | 合规要求变化趋势 |
| 经济(Economic) | 市场需求、成本变化、融资环境 | 经营压力与机遇 |
| 社会(Social) | 消费者意识、人才供给、社会责任 | 市场需求的深层驱动 |
| 技术(Technological) | 技术变革、数字化转型、专利壁垒 | 技术领先或落后风险 |
| 环境(Environmental) | 绿色制造、碳排放、资源利用 | 可持续发展要求 |
| 法律(Legal) | 劳动法规、产品责任、知识产权 | 法律风险敞口 |

### 二、分析数据准备

将分析数据整理为以下JSON格式，保存为 `analysis_data.json`：

```json
{
  "org_name": "组织名称",
  "analysis_date": "2024-01-15",
  "swot": {
    "strengths": ["优势1", "优势2"],
    "weaknesses": ["劣势1", "劣势2"],
    "opportunities": ["机遇1", "机遇2"],
    "threats": ["威胁1", "威胁2"]
  },
  "pestel": {
    "political": ["政治因素1", "政治因素2"],
    "economic": ["经济因素1", "经济因素2"],
    "social": ["社会因素1", "社会因素2"],
    "technological": ["技术因素1", "技术因素2"],
    "environmental": ["环境因素1", "环境因素2"],
    "legal": ["法律因素1", "法律因素2"]
  },
  "internal_issues": [
    {"dimension": "质量管理文化", "issue": "质量问题描述", "severity": "高/中/低", "suggestion": "改进建议"}
  ],
  "external_issues": [
    {"dimension": "政策法规", "issue": "风险描述", "likelihood": "高/中/低", "impact": "高/中/低", "suggestion": "应对措施"}
  ]
}
```

### 三、脚本执行生成分析成果

#### 3.1 生成可视化图表

```bash
python scripts/generate_analysis.py visualize --data analysis_data.json --output ./output/
```

输出文件：
- `swot_matrix.png` - SWOT四象限矩阵图
- `pestel_radar.png` - PESTEL雷达图
- `risk_matrix.png` - 风险评估矩阵图

#### 3.2 生成分析报告

```bash
python scripts/generate_analysis.py report --data analysis_data.json --output ./output/
```

输出文件：
- `qms_environment_report.pdf` - 完整的QMS环境因素分析报告

## 使用示例

### 示例1：年度管理评审准备
- 场景：XX公司准备年度管理评审，需提交环境因素分析报告
- 输入：收集各部门环境因素输入，整理为analysis_data.json
- 执行：`python scripts/generate_analysis.py report --data analysis_data.json --output ./`
- 产出：完整的PDF报告，包含可视化图表和SWOT/PESTEL分析

### 示例2：内审问题整改验证
- 场景：针对上次内审发现的环境因素识别不充分问题，需补充分析
- 输入：重点补充内审不符合项相关的因素分析
- 执行：更新JSON后重新生成报告，重点关注新增维度
- 产出：整改验证报告，附带可视化对比

### 示例3：体系换版准备（ISO 9001:2024）
- 场景：应对新版标准对风险机遇识别的更高要求
- 输入：全面梳理内外部环境因素，特别关注战略背景相关内容
- 执行：生成完整分析报告，重点输出SWOT战略建议
- 产出：支撑管理评审的完整环境因素分析包

## 资源索引

- 脚本：见 [scripts/generate_analysis.py](scripts/generate_analysis.py)（用途：生成SWOT/PESTEL可视化图表和PDF分析报告；参数：visualize/report子命令）
- 参考：见 [references/analysis-templates.md](references/analysis-templates.md)（何时读取：准备分析数据时查阅模板格式；包含：JSON格式规范、分析维度说明、填写示例）

## 注意事项

- 分析数据应来源于实际调研，避免空洞表述
- SWOT/PESTEL每项因素建议控制在3-5条，突出重点
- 问题严重性/风险等级需结合组织实际情况判定
- 报告生成后可补充组织specific的案例和数据

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 10/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互；已声明安全注意事项 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **48/50** | 通过 |
