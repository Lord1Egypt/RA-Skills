---
name: consult
description: Multi-disciplinary team consultation (MDT) coordinator for analyzing medical data and generating comprehensive reports
argument-hint: <数据范围，如：all/recent 5/date 2025-12-31>
allowed-tools: Read, Write
schema: consult/schema.json
---

# Multi-Disciplinary Team Consultation Skill

Coordinate MDT specialist team to analyze patient medical data and generate comprehensive diagnostic reports. |

## 核心流程

```
用户输入 -> 读取数据索引 -> 确定分析范围 -> 识别专科需求 -> 并行启动专科分析 -> 整合报告 -> 展示结果
```

## 步骤 1: 解析用户输入

### 数据范围识别

| Input | Analysis Range |
|------|----------|
| all | All available data |
| recent N | Last N records |
| date YYYY-MM-DD | Specified date data |
| date YYYY-MM-DD to YYYY-MM-DD | Date range data |
| no parameters | Last 3 records |

## 步骤 2: 读取数据索引

从 `data/index.json` 读取患者检查记录索引。

### 数据文件类型
- 检查报告: `data/检查报告/YYYY-MM/YYYY-MM-DD_检查名称.json`
- 症状记录: `data/health-feeling-logs.json`
- 慢性病管理: `data/*-tracker.json`

## 步骤 3: 确定会诊专科

### 自动识别规则

根据检查数据和异常指标，确定需要邀请的专科专家：

| 异常指标 | 专科 |
|---------|------|
| 血脂异常、心肌酶异常、BNP异常 | 心内科 |
| 血糖异常、甲状腺功能异常 | 内分泌科 |
| 肝功能异常、腹部超声异常 | 消化科 |
| 肾功能异常、尿常规异常 | 肾内科 |
| 血常规异常、凝血异常 | 血液科 |
| 胸部CT异常、感染指标异常 | 呼吸科 |
| 头颅影像异常 | 神经内科 |
| 肿瘤标志物异常 | 肿瘤科 |
| 多系统异常 | 全科 (协调员) |

### 专科列表

| 专科代码 | 专科名称 | Skill文件 |
|---------|---------|-----------|
| cardio | 心内科 | .claude/specialists/cardiology.md |
| endo | 内分泌科 | .claude/specialists/endocrinology.md |
| gastro | 消化科 | .claude/specialists/gastroenterology.md |
| nephro | 肾内科 | .claude/specialists/nephrology.md |
| heme | 血液科 | .claude/specialists/hematology.md |
| resp | 呼吸科 | .claude/specialists/respiratory.md |
| neuro | 神经内科 | .claude/specialists/neurology.md |
| onco | 肿瘤科 | .claude/specialists/oncology.md |
| general | 全科 | .claude/specialists/general.md |

## 步骤 4: 并行启动专科分析

使用 Task 工具并行启动相关专科的 subagent。

### Subagent Prompt 模板

```
您是{{专科名称}}专家。请按照以下 Skill 定义进行医疗数据分析：

## Skill 定义
{{读取对应的专科 skill 定义文件}}

## 患者医疗数据
{{加载相关的检查数据}}

## 分析要求
1. 严格按照 Skill 定义的格式输出分析报告
2. **优先分析慢性病管理情况**（如存在）
3. 结合检查报告数据综合分析
4. 严格遵守以下安全红线：
   - 不给出具体用药剂量
   - 不直接开具处方药名
   - 不判断生死预后
   - 不替代医生诊断
5. 提供具体可行的建议
```

## 步骤 5: 整合会诊报告

### 报告格式

```markdown
## 多学科会诊(MDT)报告

会诊日期: YYYY-MM-DD

━━━━━━━━━━━━━━━━━━━━━━━━━━

### 各专科分析

#### 1. {{专科名称}}
[专科分析内容...]

#### 2. {{专科名称}}
[专科分析内容...]

━━━━━━━━━━━━━━━━━━━━━━━━━━

### 综合评估

[综合分析...]

━━━━━━━━━━━━━━━━━━━━━━━━━━

### 优先级排序

1. [高优先级问题]
2. [中优先级问题]
3. [低优先级问题]

━━━━━━━━━━━━━━━━━━━━━━━━━━

### 综合建议

#### 生活方式调整
[具体建议...]

#### 就医建议
[具体建议...]

#### 随访计划
[具体计划...]

━━━━━━━━━━━━━━━━━━━━━━━━━━

### 重要声明

本报告仅供健康参考，不能替代专业医疗诊断和治疗。
所有医疗决策请遵从医生指导。
```

## 安全红线（严格遵守）

1. **不给出具体用药剂量**
   - 错误示例："服用阿托伐他汀 20mg 每日1次"
   - 正确做法："建议咨询医生调整降脂药物方案"

2. **不直接开具处方药名**
   - 错误示例："开具阿司匹林肠溶片"
   - 正确做法："建议咨询医生是否需要抗血小板治疗"

3. **不判断生死预后**
   - 错误示例："预后差，生存期不超过6个月"
   - 正确做法："建议积极治疗，定期复查评估疗效"

4. **不替代医生诊断**
   - 错误示例："确诊为冠心病"
   - 正确做法："提示可能存在冠心病风险，建议心内科进一步检查明确诊断"

## 执行指令

```
1. 识别数据范围参数
2. 读取 data/index.json 获取记录列表
3. 根据数据类型确定需要的专科
4. 并行启动相关专科 subagent 分析
5. 收集各专科分析报告
6. 整合生成综合会诊报告
7. 向用户展示完整报告
```

## 示例交互

### 示例 1: 分析所有数据
```
用户: /consult all
AI: 📊 正在启动多学科专家会诊...

    读取数据中...
    发现异常指标:
    • 血脂异常 → 心内科
    • 血糖偏高 → 内分泌科
    • 肝功能异常 → 消化科

    并行启动专科分析...

    [生成完整会诊报告...]
```

### 示例 2: 分析最近5条记录
```
用户: /consult recent 5
AI: 📊 分析最近5条检查记录...

    涉及专科: 心内科、内分泌科

    [生成会诊报告...]
```

### 示例 3: 分析指定日期数据
```
用户: /consult date 2025-12-31
AI: 📊 分析2025年12月31日的检查数据...

    [生成会诊报告...]
```

## 重要提示

- 本系统仅供健康参考，不能替代专业医疗诊断和治疗
- 所有医疗决策请遵从医生指导
- 会诊报告基于提供的检查数据，可能存在局限性
- 紧急情况请立即就医
