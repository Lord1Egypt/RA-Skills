---
name: polypharmacy
description: Polypharmacy management - medication list, Beers criteria screening, drug interaction checking, anticholinergic burden assessment, and deprescribing planning
argument-hint: <操作类型+信息，如：add 阿司匹林 100mg qd, beers, interaction check, deprescribe>
allowed-tools: Read, Write
schema: polypharmacy/schema.json
---

# Polypharmacy Management Skill

Manage polypharmacy in elderly patients, including medication list management, Beers criteria screening, drug interaction checking, and deprescribing planning.

## 核心流程

```
用户输入 -> 识别操作类型 -> 提取参数信息 -> 检查完整性 -> [需补充] 询问用户
                                                      |
                                                   [信息完整]
                                                      |
                                              生成JSON -> 保存数据 -> 输出确认
```

## 步骤 1: 解析用户输入

### Operation Type Recognition

| Input Keywords | Operation Type | Description |
|---------------|----------------|-------------|
| add | add_medication | Add medication |
| list | medication_list | View medication list |
| beers | beers_screening | Beers criteria screening |
| inappropriate | inappropriate_meds | View inappropriate medications |
| interaction | drug_interaction | Drug interaction check |
| anticholinergic | anticholinergic_burden | Anticholinergic burden assessment |
| acb-score | acb_score | ACB score |
| deprescribe | deprescribing_plan | Deprescribing plan |
| status | polypharmacy_status | View polypharmacy status |
| recommendations | management_recommendations | View management recommendations |

### 用药频次关键词

| Input Keywords | Frequency Value |
|---------------|----------------|
| qd | qd |
| bid | bid |
| tid | tid |
| qid | qid |
| qn | qn |
| prn | prn |

### 相互作用严重程度

| Input Keywords | Severity |
|---------------|----------|
| major | major |
| moderate | moderate |
| minor | minor |

### 精简行动类型

| Input Keywords | Action |
|---------------|--------|
| taper | taper |
| switch | switch |
| discontinue | discontinue |

## 步骤 2: 检查信息完整性

### Add Medication Required:
- Medication name
- Dose
- Frequency

### Interaction Check Required:
- Two medication names
- Severity

### Deprescribe Plan Recommended:
- Medication name (optional)
- Action type (optional)

## 步骤 3: 交互式询问（如需要）

### Scenario A: Adding Medication Incomplete Information
```
Please provide complete medication information:
- Medication name
- Dose (e.g.: 100mg)
- Frequency (qd/bid/tid/qid/qn/prn)
- Indication (optional)
```

### Scenario B: Interaction Information Missing
```
Please provide the following information:
- Medication 1 name
- Medication 2 name
- Severity (major/moderate/minor)
- Interaction description (optional)
```

### Scenario C: Deprescribing Medication Inquiry
```
The following medications may need deprescribing:
1. Diazepam - Beers criteria potentially inappropriate medication
2. Chlorpheniramine - High anticholinergic burden

Which medication would you like to create a deprescribing plan for?
Action options:
- taper (gradual dose reduction)
- switch (switch medication)
- discontinue (stop directly)

## 步骤 4: 生成 JSON

### 用药记录
```json
{
  "medication_id": "med_001",
  "name": "阿司匹林",
  "dosage": "100mg",
  "frequency": "qd",
  "indication": "心血管保护",
  "start_date": "2025-01-01",
  "is_appropriate": true,
  "beers_criteria": false
}
```

### Beers标准违规记录
```json
{
  "medication_id": "med_002",
  "medication_name": "地西泮",
  "violation_type": "potential_inappropriate",
  "severity": "moderate",
  "reason": "老年人使用苯二氮卓类增加跌倒和过度镇静风险",
  "recommendation": "考虑使用非苯二氮卓类替代",
  "alternative": "佐匹克隆、褪黑素"
}
```

### 药物相互作用记录
```json
{
  "drug_1": "华法林",
  "drug_2": "阿司匹林",
  "severity": "moderate",
  "interaction_type": "drug_drug",
  "description": "增加出血风险",
  "management": "密切监测出血迹象，考虑调整剂量",
  "clinical_significance": "需要监测"
}
```

### 抗胆碱能负荷记录
```json
{
  "total_score": 4,
  "risk_level": "显著风险",
  "contributing_medications": [
    {"name": "氯苯那敏", "score": 2},
    {"name": "阿米替林", "score": 2}
  ],
  "associated_risks": [
    "认知障碍",
    "便秘",
    "口干",
    "尿潴留",
    "跌倒风险增加"
  ]
}
```

### 精简计划记录
```json
{
  "medication_name": "地西泮",
  "action": "taper",
  "timeline": "4周逐渐减量",
  "schedule": [
    {"week": 1, "dosage": "5mg qn"},
    {"week": 2, "dosage": "2.5mg qn"},
    {"week": 3, "dosage": "2.5mg qod"},
    {"week": 4, "dosage": "停用"}
  ],
  "monitoring": ["睡眠质量", "焦虑症状", "撤药症状"],
  "alternative": "认知行为治疗"
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## 步骤 5: 保存数据

1. 读取 `data/polypharmacy-management.json`
2. 根据操作类型更新相应段
3. 更新统计数据
4. 写回文件

## 执行指令

```
1. 识别操作类型 (add/list/beers/inappropriate/interaction/anticholinergic/deprescribe/status/recommendations)
2. 提取参数信息
3. 检查必填字段完整性
4. 如有缺失，询问用户补充
5. 生成符合 schema.json 的 JSON
6. 保存到 data/polypharmacy-management.json
7. 输出确认信息和医学建议
```

## 示例交互

### 示例 1: 添加用药
```
用户: add 阿司匹林 100mg qd 心血管保护

AI: 已添加用药记录
药物: 阿司匹林
剂量: 100mg
用法: 每天1次
适应症: 心血管保护

Beers标准筛查: 适当
抗胆碱能负荷: 0

当前用药总数: 5种
```

### 示例 2: Beers标准筛查
```
用户: beers

AI: Beers标准筛查结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
发现2种潜在不适当用药：

1. 地西泮 5mg qn
   问题: 苯二氮卓类增加跌倒和过度镇静风险
   严重程度: 中度
   建议: 考虑使用非苯二氮卓类替代

2. 氯苯那敏 4mg prn
   问题: 第一代抗组胺药有抗胆碱能作用
   严重程度: 中度
   建议: 考虑使用第二代抗组胺药（氯雷他定）

建议与医生讨论用药调整
```

### 示例 3: 药物相互作用检查
```
用户: interaction check

AI: 药物相互作用检查结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
发现1个中等严重程度相互作用：

华法林 + 阿司匹林
- 严重程度: 中度
- 影响: 增加出血风险
- 管理: 密切监测出血迹象，定期检查INR
- 临床意义: 需要监测

建议: 告知医生正在同时使用这两种药物
```

### 示例 4: 抗胆碱能负荷评估
```
用户: anticholinergic

AI: 抗胆碱能负荷评估
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACB总分: 4分
风险等级: 显著风险

贡献药物:
- 氯苯那敏 (2分)
- 阿米替林 (2分)

相关风险:
- 认知障碍
- 便秘
- 口干
- 尿潴留
- 跌倒风险增加

建议: 与医生讨论精简高抗胆碱能负荷药物
```

### 示例 5: 精简计划
```
用户: deprescribe

AI: 用药精简建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
候选药物:

1. 地西泮 5mg qn
   原因: Beers标准不适当用药
   建议: 逐渐减量（4周）
   替代: 认知行为治疗、褪黑素

2. 氯苯那敏 4mg prn
   原因: 高抗胆碱能负荷
   建议: 替换为氯雷他定
   替代: 氯雷他定 10mg prn

精简原则:
- 逐步减量避免停药反应
- 监测减药反应
- 定期复查

重要: 任何用药调整前请咨询医生
```

更多示例参见 [examples.md](examples.md)。

## 医学安全边界

### 不能做的事:
- 调整药物剂量或停药
- 建议具体药物剂量调整
- 建议自行停药
- 推荐具体药物品牌
- 开处方药

### 能做的事:
- 用药清单管理
- 不适当用药筛查（Beers标准）
- 药物-药物相互作用检查
- 药物-疾病相互作用检查
- 抗胆碱能药物负荷评估
- 用药精简计划建议
- 用药依从性评估

### 重要提示:
- 调整用药需医生评估
- 系统仅提供筛查和建议
- 用药调整需医疗专业人员
- 定期用药审查（每6个月）
