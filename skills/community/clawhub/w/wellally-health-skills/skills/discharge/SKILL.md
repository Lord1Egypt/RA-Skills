---
name: discharge
description: Save and structure discharge summary information. Extract from images or process text descriptions of hospital discharge records including diagnosis, treatment, and follow-up instructions.
argument-hint: <出院小结来源（图片路径或文字描述）>
allowed-tools: Read, Write
schema: discharge/schema.json
---

# Discharge Summary Management Skill

Save and structure discharge summary information. Supports extraction from images or direct processing from text descriptions.

## 核心流程

```
用户输入 → 识别来源类型 → [图片]读取分析图片 → 提取信息 → 生成JSON → 保存
                              ↓
                         [文字]解析文本 → 提取信息 → 生成JSON → 保存
```

## 步骤 1: 解析用户输入

### Source Type Recognition

| Input Pattern | Source Type |
|---------------|-------------|
| Starts with @, .jpg/.png | Image path |
| Contains "hospitalization", "discharge" keywords | Text description |

### 日期识别
- 入院日期格式：`(\d{4}-\d{2}-\d{2})` 或 `(\d{4}年\d{1,2}月\d{1,2}日)`
- 出院日期格式：同上

## 步骤 2: 检查信息完整性

### 必填字段:
- `source` - 出院小结来源（图片或文字）

### 强烈建议有（可从图片/文字中提取）:
- `basic_info.hospital` - 医院名称
- `basic_info.admission_date` - 入院日期
- `basic_info.discharge_date` - 出院日期
- `diagnosis.discharge_diagnosis.main` - 主要诊断

## 步骤 3: 图片分析（图片来源）

使用 `mcp__4_5v_mcp__analyze_image` 工具分析出院小结图片：

**图片分析提示词模板：**
```
请详细识别这张出院小结的所有内容，包括：

1. 基础信息：患者姓名、性别、年龄、入院日期、出院日期、住院天数、住院科室、床号、医保类型

2. 诊断信息：入院诊断（主要诊断和其他诊断）、出院诊断（主要诊断和其他诊断）、诊断编码（ICD-10，如有）

3. 治疗经过：
   - 主要治疗措施
   - 药物治疗：药品名称、剂量、用法用量、用药起止日期、药物类别、适应症
   - 输液治疗：输液名称、添加药物、剂量、频率、起止日期
   - 非药物治疗：物理治疗、氧疗、雾化等
   - 肿瘤治疗（如适用）：
     * 放疗：放射部位、总剂量、次数、放疗技术、起止日期
     * 化疗：方案名称、周期、药物、剂量、不良反应
     * 靶向治疗：药物名称、靶点、剂量
     * 免疫治疗：药物名称、类型、剂量
   - 手术记录（如有）：手术名称、日期、麻醉方式
   - 检查结果摘要

4. 治疗效果评估：总体疗效（显效/有效/好转/无效）、症状改善、不良反应、实验室指标改善

5. 出院情况：出院时病情状态、症状改善情况、生命体征

6. 出院医嘱：用药指导、饮食指导、活动指导、伤口护理（如有）、复查计划和时间、注意事项

7. 其他信息：主治医生、医院名称、住院费用（如有）、随诊电话

请以结构化的方式列出所有信息，保持原文准确性。
```

## 步骤 4: 生成 JSON

### 出院小结数据结构

```json
{
  "id": "2024081500001",
  "basic_info": {
    "hospital": "某某医院",
    "department": "消化内科",
    "admission_date": "2024-08-10",
    "discharge_date": "2024-08-15",
    "hospitalization_days": 5,
    "bed_number": "23床",
    "insurance_type": "职工医保"
  },
  "diagnosis": {
    "admission_diagnosis": {
      "main": "急性胆囊炎",
      "secondary": ["胆囊结石", "高血压病（2级，中危组）"]
    },
    "discharge_diagnosis": {
      "main": "急性胆囊炎",
      "secondary": ["胆囊结石", "高血压病（2级，中危组）", "2型糖尿病"]
    }
  },
  "treatment_summary": {
    "main_treatments": ["禁食水、胃肠减压", "抗感染治疗", "解痉止痛治疗"],
    "medications": [
      {
        "drug_name": "阿莫西林胶囊",
        "dosage": "0.5g",
        "frequency": "每日3次",
        "route": "口服",
        "duration": "7天",
        "start_date": "2024-08-10",
        "end_date": "2024-08-15",
        "drug_category": "抗生素",
        "indication": "抗感染",
        "notes": "饭后服用"
      }
    ],
    "infusion_therapy": [
      {
        "solution_name": "0.9%氯化钠注射液",
        "additives": ["头孢哌酮钠舒巴坦钠 2g"],
        "dosage": "100ml",
        "frequency": "每日2次",
        "route": "静脉滴注",
        "duration": "5天",
        "start_date": "2024-08-10",
        "end_date": "2024-08-15"
      }
    ],
    "non_drug_treatments": [
      {
        "treatment_type": "氧疗",
        "treatment_name": "低流量吸氧",
        "parameters": "2L/min，每日2次，每次30分钟",
        "duration": "3天",
        "start_date": "2024-08-10",
        "end_date": "2024-08-12"
      }
    ],
    "treatment_effectiveness": {
      "overall_effect": "显效",
      "symptom_improvement": "腹痛完全缓解，体温恢复正常，无恶心呕吐",
      "adverse_reactions": [],
      "lab_improvements": "白细胞计数由15.2×10^9/L降至7.8×10^9/L，CRP正常"
    },
    "surgeries": [
      {
        "surgery_name": "腹腔镜下胆囊切除术",
        "surgery_date": "2024-08-12",
        "anesthesia": "全身麻醉",
        "surgeon": "张医生"
      }
    ]
  },
  "discharge_status": {
    "condition": "好转",
    "symptoms": "腹痛缓解，无发热，饮食恢复",
    "vital_signs": {
      "blood_pressure": "130/80 mmHg",
      "heart_rate": "78 次/分",
      "temperature": "36.5℃"
    }
  },
  "discharge_orders": {
    "medication_instructions": [...],
    "dietary_guidance": "低脂饮食，少食多餐，避免油腻食物",
    "follow_up_plan": [
      {
        "item": "术后复查",
        "timing": "术后2周",
        "location": "普通外科门诊"
      }
    ],
    "warnings": ["如出现发热、腹痛、黄疸等症状，请及时就医"]
  }
}
```

## 步骤 5: 保存数据

1. If image, copy to `data/discharge-summaries/YYYY-MM/images/`
2. Create month directory (if not exists)
3. Save JSON data file: `data/discharge-summaries/YYYY-MM/YYYY-MM-DD_main-diagnosis.json`
4. 更新全局索引 `data/index.json`

## 执行指令

```
1. 识别用户输入类型（图片或文字）
2. 图片来源：
   a. 使用 Read 工具读取图片
   b. 使用 mcp__4_5v_mcp__analyze_image 分析图片
   c. 提取结构化信息
3. 文字来源：
   a. 从文字中提取信息
   b. 按照数据结构分类
4. 如有缺失关键信息，询问用户补充
5. 生成 JSON 并保存
```

## 智能提取规则

### 诊断信息提取
- 主要诊断：通常排在第一位的诊断
- 次要诊断：合并症、并发症
- ICD-10编码：如有，自动提取

### 手术信息提取
- 识别"手术名称"、"手术日期"、"麻醉方式"
- 自动关联到手术记录（如果已存在）

### 药物信息提取
- 药品名称（通用名）
- 剂量（如 0.5g、10mg）
- 用法（每日3次、q8h、必要时）
- 给药途径（口服、静脉滴注、肌肉注射）
- 疗程（7天、遵医嘱）
- 用药起止日期（从住院记录中推断）
- 药物类别（抗生素、降压药、降糖药、止痛药等）
- 适应症（用于治疗什么症状或疾病）

### 输液治疗提取
- 输液名称（0.9%氯化钠、5%葡萄糖等）
- 添加药物（头孢XX、氯化钾等）
- 剂量（100ml、250ml、500ml）
- 频率（每日1次、q12h、q8h）
- 起止日期

### 非药物治疗提取
- 治疗类型（物理治疗、中医治疗、氧疗、雾化、透析等）
- 具体名称和参数
- 治疗频次和天数

### 治疗效果提取
- 总体疗效（显效/有效/好转/无效）
- 症状改善描述
- 有无不良反应
- 实验室指标变化

### 肿瘤治疗提取
#### 放疗信息
- 放射部位（胸部、头颈部、盆腔等）
- 总剂量和每次剂量
- 放疗次数
- 放疗技术（IMRT、VMAT等）
- 放疗目的（根治性/辅助性/姑息性）
- 放疗反应

#### 化疗信息
- 化疗方案名称（TP、AC-T、CHOP等）
- 周期数（第几周期/共几周期）
- 化疗药物及剂量
- 不良反应及毒性分级
- 下一周期计划时间

#### 靶向治疗
- 药物名称及靶点
- 剂量和用法
- 不良反应

#### 免疫治疗
- 药物名称及类型（PD-1/PD-L1等）
- 剂量和用法
- 免疫相关不良反应

更多示例参见 [examples.md](examples.md)。
