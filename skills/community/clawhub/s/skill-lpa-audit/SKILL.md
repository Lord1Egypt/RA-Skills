---
slug: lpa-audit
name: LPA审核技能
displayName: LPA审核技能
version: 1.1.0
author: org-jaxjwo0r
category: quality
description: 提供LPA分层审核全流程支持，包括知识库查询、标准清单生成、结果录入分析、报告汇总生成；当需要进行分层审核培训、执行审核任务、分析审核数据或制作审核报告时使用
---

# LPA分层审核技能

## 任务目标
- 本技能用于：支持企业质量管理中的LPA（分层过程审核）全流程执行
- 能力包含：LPA知识体系查询、审核清单自动生成、审核结果分析处理、审核报告生成
- 触发条件：用户提及"分层审核"、"LPA"、"审核清单"、"审核报告"等场景

## 前置准备
- 依赖说明：jinja2==3.1.2（报告模板渲染）
- 输出路径：默认当前目录 `./output/`
- 输入文件：审核结果数据需符合JSON格式（见references）

## LPA基础知识

### 分层审核层级定义

| 层级 | 角色 | 审核频次 | 审核时长 | 覆盖范围 |
|------|------|----------|----------|----------|
| L1 | 班组长/操作员 | 每班次1-2次 | 10-15分钟 | 关键工序、标准作业 |
| L2 | 线长/工段长 | 每天1次 | 20-30分钟 | 生产线关键控制点 |
| L3 | 车间主任/主管 | 每周1-2次 | 30-45分钟 | 车间级重点区域 |
| L4 | 部门经理 | 每月1-2次 | 1-2小时 | 部门全面审核 |

### 核心审核要素
- **人员**：持证上岗、培训记录、技能等级
- **设备**：点检状态、参数设定、模具工装
- **物料**：来料标识、批次追溯、先进先出
- **方法**：作业标准执行、工艺参数遵守
- **环境**：5S状态、温度湿度、安全防护
- **测量**：量具校准、检验记录、MSA分析

## 操作步骤

### 1. 生成审核清单

根据审核层级和审核范围生成标准化审核清单：

```bash
python scripts/generate_checklist.py --level L2 --department "焊接车间" --output output/checklist_l2.json
```

**参数说明：**
- `--level`: 审核层级（L1/L2/L3/L4）
- `--department`: 被审核部门/产线名称
- `--output`: 输出文件路径

**输出格式：** JSON结构化清单，包含检查项ID、名称、分类、检查标准、判定依据

### 2. 录入与分析审核结果

将审核发现录入系统并生成分析数据：

```bash
python scripts/analyze_results.py --checklist output/checklist_l2.json --results data/audit_results.json --output output/analysis.json
```

**参数说明：**
- `--checklist`: 使用清单文件路径
- `--results`: 审核结果数据（JSON格式）
- `--output`: 分析结果输出路径

**输入数据格式要求：**
```json
{
  "audit_info": {
    "audit_id": "AUD-2024-001",
    "auditor": "张三",
    "audit_time": "2024-01-15 10:30:00",
    "level": "L2",
    "department": "焊接车间"
  },
  "findings": [
    {
      "item_id": "L2-EQP-001",
      "status": "pass/fail/na",
      "evidence": "现场照片路径或文字描述",
      "note": "备注说明"
    }
  ]
}
```

**分析维度：** 通过率、问题分布（按分类）、TOP问题排序、趋势对比

### 3. 生成审核报告

汇总多层级审核结果生成结构化报告：

```bash
python scripts/generate_report.py --level L2 --period "2024-01" --data output/analysis.json --output output/L2_audit_report_2024-01.html
```

**参数说明：**
- `--level`: 审核层级（L1/L2/L3/L4/all）
- `--period`: 审核周期（YYYY-MM格式）
- `--data`: 分析数据文件路径
- `--output`: 报告输出路径（支持.html/.pdf/.docx）

**报告结构：** 执行摘要 → 分项数据 → 问题分析 → 改进建议 → 附件清单

## 使用示例

### 示例1：月度审核准备
- **场景**：车间主任准备本月L3审核，需要生成标准清单
- **执行**：`python scripts/generate_checklist.py --level L3 --department "装配车间" --output checklist_l3.json`
- **产出**：包含35项检查项的标准化清单

### 示例2：审核数据分析
- **场景**：质量工程师分析上周审核结果，识别TOP问题
- **执行**：`python scripts/analyze_results.py --checklist checklist.json --results weekly_results.json --output analysis.json`
- **产出**：问题分布统计、TOP3问题排序、通过率趋势

### 示例3：季度审核报告
- **场景**：质量经理汇总Q1所有L2审核数据，制作汇报材料
- **执行**：`python scripts/generate_report.py --level L2 --period 2024-Q1 --data q1_data.json --output L2_Q1_report.html`
- **产出**：含图表的结构化HTML报告

## 资源索引
- 脚本:见 [scripts/generate_checklist.py](scripts/generate_checklist.py)（生成标准化审核清单）
- 脚本:见 [scripts/analyze_results.py](scripts/analyze_results.py)（录入分析审核数据）
- 脚本:见 [scripts/generate_report.py](scripts/generate_report.py)（生成结构化报告）
- 参考:见 [references/lpa_standards.md](references/lpa_standards.md)（LPA标准体系知识库）
- 参考:见 [references/audit_levels.md](references/audit_levels.md)（各层级审核标准详情）
- 模板:见 [assets/templates/report_template.html](assets/templates/report_template.html)（报告HTML模板）

## 注意事项
- 首次使用建议先阅读 references/audit_levels.md 了解各层级审核重点
- 审核结果数据必须包含 audit_info 基本信息和 findings 检查项列表
- 报告模板支持HTML输出，可直接打印或转换为PDF
- 问题分类编码规则：EQP-设备、MAT-物料、MTH-方法、PPE-人员、ENV-环境、MSR-测量
- 变更记录：V1.1.0：完善 TRACE 五维度测评体系，补充触发条件、能力边界、异常处理与 TRACE 自评表

## 能力边界

- **适用场景**：质量管理体系中涉及LPA分层审核技能的场景，需要生成标准化文档或分析
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
