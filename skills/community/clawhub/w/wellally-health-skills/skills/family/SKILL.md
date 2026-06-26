---
name: family
description: Family health management including member records, medical history tracking, genetic risk assessment, and health reports
argument-hint: <操作类型，如：add-member 父亲 张三 1960-05-15/add-history 父亲 高血压/risk/report>
allowed-tools: Read, Write
schema: family/schema.json
---

# Family Health Management Skill

Comprehensive family health record management, helping track family medical history, assess genetic risks, and maintain family health.

## 核心流程

```
用户输入 -> 识别操作类型 -> 解析信息 -> 检查完整性 -> [询问补充] -> 生成JSON -> 保存数据
```

## 步骤 1: 解析用户输入

### 操作类型识别

| 输入关键词 | 操作类型 |
|-----------|----------|
| add-member, 添加成员 | 添加家庭成员 |
| add-history, 记录病史, 记录家族史 | 记录家族病史 |
| track, 追踪 | 追踪成员健康 |
| list, 列表 | 列出家庭成员 |
| risk, 风险 | 遗传风险评估 |
| report, 报告 | 生成家庭健康报告 |

### Relationship Type Recognition

| Relationship | Code |
|-------------|------|
| Self | self |
| Father | father |
| Mother | mother |
| Spouse | spouse |
| Son | son |
| Daughter | daughter |
| Brother | brother |
| Sister | sister |
| Paternal grandfather | paternal_grandfather |
| Paternal grandmother | paternal_grandmother |
| Maternal grandfather | maternal_grandfather |
| Maternal grandmother | maternal_grandmother |

### Disease Category Recognition

| Category | Disease Keywords |
|----------|-----------------|
| Cardiovascular | Hypertension, coronary heart disease, cardiomyopathy, stroke |
| Metabolic | Diabetes, hyperlipidemia, gout, metabolic syndrome |
| Cancer | Lung cancer, breast cancer, colorectal cancer, gastric cancer, liver cancer |
| Respiratory | Asthma, COPD, pulmonary fibrosis |
| Other | Glaucoma, mental illness, autoimmune diseases |

## 步骤 2: 检查信息完整性

### Add Member (add-member)
- **Required**: Relationship, name, birth date or age
- **Optional**: Blood type, gender

### Record History (add-history)
- **Required**: Member, disease name
- **Recommended**: Age at onset
- **Optional**: Severity, notes

### Track Health (track)
- **Required**: Member, data type, value
- **Optional**: Date, unit

## 步骤 3: 交互式询问（如需要）

### Question Scenarios

#### Scenario A: Adding Member Missing Information
```
Please provide the following information:
• Member relationship (father/mother/spouse/child, etc.)
• Member name
• Birth date (format: YYYY-MM-DD)
• Blood type (optional)
```

#### Scenario B: Recording History Missing Age
```
Please provide the following information:
• When was this member diagnosed? (age or year)
• Current condition? (stable/controlled/needs treatment)

## 步骤 4: 生成 JSON

### 成员数据结构

```json
{
  "member_id": "mem_20250108_001",
  "name": "张三",
  "relationship": "father",
  "gender": "male",
  "birth_date": "1960-05-15",
  "blood_type": "A",
  "status": "living",
  "created_at": "2025-01-08T10:00:00.000Z"
}
```

### 家族病史数据结构

```json
{
  "history_id": "hist_20250108_001",
  "disease_name": "高血压",
  "disease_category": "cardiovascular",
  "affected_member_id": "mem_20250108_001",
  "age_at_onset": 50,
  "severity": "moderate",
  "notes": "药物控制良好",
  "reported_date": "2025-01-08"
}
```

### 风险评估数据结构

```json
{
  "disease": "高血压",
  "risk_level": "high",
  "confidence": "medium",
  "affected_members": ["父亲"],
  "risk_factors": ["一级亲属患病", "早发(<50岁)"],
  "recommendations": [
    {
      "category": "screening",
      "action": "定期血压监测",
      "frequency": "每周3次",
      "start_age": 35,
      "priority": "high"
    }
  ]
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## 步骤 5: 保存数据

1. 生成唯一ID
2. 保存到 `data/family-health-tracker.json`
3. 更新索引

## 遗传风险计算

```
遗传风险评分 = (一级亲属患病数 × 0.4) +
              (早发病例数 × 0.3) +
              (家族聚集度 × 0.3)

风险等级:
- 高风险: >= 70%
- 中风险: 40%-69%
- 低风险: < 40%
```

## 风险特征分类

### 高风险特征
- 多名一级亲属患病
- 早发病例 (<50岁)
- 家族聚集明显
- 遗传模式明确

### 中风险特征
- 1-2名一级亲属患病
- 中年发病 (50-65岁)
- 轻度家族聚集

### 低风险特征
- 仅有远亲患病
- 晚发病例 (>65岁)
- 散发病例

## 执行指令

```
1. 识别操作类型
2. 解析输入参数，提取所有可用信息
3. 检查必填字段，如有缺失则询问用户
4. 计算遗传风险
5. 生成符合 schema.json 的 JSON
6. 保存到数据文件
7. 向用户确认保存成功，并显示摘要和建议
```

## 示例交互

### 示例 1: 添加家庭成员
```
用户: 添加家庭成员 父亲 张三 1960-05-15 A型血
AI: ✅ 家庭成员已添加

    成员信息:
    关系: 父亲
    姓名: 张三
    出生日期: 1960年5月15日
    血型: A型
    年龄: 65岁

    已保存至家庭健康档案

    提示: 您可以继续添加其他成员或记录家族病史
```

### 示例 2: 记录家族病史
```
用户: 记录家族病史 父亲 高血压 50岁确诊
AI: ✅ 家族病史已记录

    病史信息:
    成员: 父亲 (张三)
    疾病: 高血压
    发病年龄: 50岁
    疾病类别: 心血管疾病

    风险评估: 高风险
    (一级亲属患病 + 早发病例)

    预防建议:
    • 35岁开始定期血压监测
    • 每周测量3次
    • 限制钠盐摄入
    • 规律有氧运动
    • 控制体重

    已保存至家族病史记录
```

### 示例 3: 遗传风险评估
```
用户: 遗传风险 高血压
AI: 📊 高血压遗传风险评估

    风险等级: 高 ⚠️

    受影响家庭成员:
    • 父亲: 50岁确诊

    风险因素:
    ✓ 一级亲属患病
    ✓ 早发病例 (<50岁)

    风险评分: 75/100

    预防建议:
    1. 定期血压监测 (35岁开始，每周3次)
    2. 限制钠盐摄入 (<5g/天)
    3. 规律有氧运动 (每周150分钟)
    4. 体重管理 (BMI < 24)
    5. 戒烟限酒

    筛查建议:
    • 每年健康体检
    • 监测血压、血脂、血糖

    [生成完整报告...]
```

## 重要提示

- 本系统仅供家庭健康记录和家族病史管理
- 遗传风险评估结果仅供参考，不预测个体发病
- 具体风险请咨询专业医师或遗传咨询师
- 高风险人群应提前开始筛查
- 所有数据仅保存在本地
