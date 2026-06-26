---
name: specialist
description: Consult specific medical specialists for targeted analysis based on medical data and symptoms
argument-hint: <专科代码> [数据范围]，如：cardio recent 3/endo all/pedia list>
allowed-tools: Read, Write
schema: specialist/schema.json
---

# Specialist Consultation Skill

Launch the appropriate specialist for in-depth analysis based on the user's specified specialty.

## 核心流程

```
用户输入 -> 验证专科代码 -> 读取专科Skill定义 -> 收集医疗数据 -> 启动专科分析 -> 展示报告
```

## 步骤 1: 解析用户输入

### 输入格式

```
/specialist <专科代码> [数据范围]
```

### 数据范围参数

| 参数 | 说明 |
|------|------|
| 无参数 | 最近3条记录 (默认) |
| all | 所有数据 |
| recent N | 最近N条记录 |
| date YYYY-MM-DD | 指定日期 |
| date YYYY-MM-DD to YYYY-MM-DD | 日期范围 |

## 步骤 2: 验证专科代码

### 支持的专科列表

| Specialty Code | Specialty Name | Skill File | Expertise |
|---------------|---------------|-----------|----------|
| cardio | Cardiology | cardiology.md | Heart disease, hypertension, lipid disorders |
| endo | Endocrinology | endocrinology.md | Diabetes, thyroid diseases |
| gastro | Gastroenterology | gastroenterology.md | Liver disease, gastrointestinal diseases |
| nephro | Nephrology | nephrology.md | Kidney disease, electrolyte disorders |
| heme | Hematology | hematology.md | Anemia, coagulation disorders |
| resp | Respiratory | respiratory.md | Lung infections, lung nodules |
| neuro | Neurology | neurology.md | Cerebrovascular disease, headache, dizziness |
| onco | Oncology | oncology.md | Tumor markers, cancer screening |
| ortho | Orthopedics | orthopedics.md | Fractures, arthritis, osteoporosis |
| derma | Dermatology | dermatology.md | Eczema, acne, skin tumors |
| pedia | Pediatrics | pediatrics.md | Child development, neonatal diseases |
| gyne | Gynecology | gynecology.md | Menstrual disorders, gynecological tumors |
| general | General Practice | general.md | Comprehensive assessment, chronic disease management |
| psych | Psychiatry | psychiatry.md | Mood disorders, mental health |

## 步骤 3: 慢性病数据读取

对于特定专科，还需读取相关的慢性病管理数据：

| 专科代码 | 慢性病数据文件 |
|---------|---------------|
| cardio | `data/hypertension-tracker.json` |
| endo | `data/diabetes-tracker.json` |
| resp | `data/copd-tracker.json` |
| nephro | `data/hypertension-tracker.json` + `data/diabetes-tracker.json` |

**数据读取优先级:**
1. 慢性病管理数据 (如存在)
2. 检查报告数据
3. 其他相关医疗记录

## 步骤 4: 启动专科分析

### Subagent Prompt 模板

```
您是{{专科名称}}专家。请按照以下 Skill 定义进行医疗数据分析：

## Skill 定义
{{读取对应的专科 skill 定义文件}}

## 患者医疗数据

### 慢性病管理情况（如有）
{{读取对应的慢性病数据文件}}

### 近期检查数据
{{读取相关的检查报告数据}}

## 分析要求
1. 严格按照 Skill 定义的格式输出分析报告
2. **优先分析慢性病管理情况**（如存在）:
   - 诊断时间和分类
   - 控制情况 (达标率、平均值等)
   - 靶器官损害/并发症状态
   - 风险评估
3. 结合检查报告数据综合分析
4. 严格遵守安全红线:
   - 不给出具体用药剂量
   - 不直接开具处方药名
   - 不判断生死预后
   - 不替代医生诊断
5. 提供具体可行的建议
```

## 步骤 5: 专科分析报告格式

```markdown
## {{专科名称}}分析报告

### 慢性病管理情况（如有）
**{{慢性病名称}}控制状态**: [基于慢性病管理数据]
- 诊断时间: YYYY-MM-DD
- 分级/分类: {{classification}}
- 近期控制指标: {{key metrics}}
- 达标情况: {{achievement status}}
- 靶器官损害/并发症: {{status}}
- 风险评估: {{risk level}}

### 近期检查数据
[其他检查数据分析...]

### 综合评估
[结合慢性病和检查数据的综合分析]

### 建议
- 生活方式: [具体建议]
- 饮食调整: [具体建议]
- 就医建议: [是否需要就医/复查]
```

## 错误处理

### 专科代码无效

```
❌ 未找到专科 "xyz"

可用的专科列表:

**内科系统**
- cardio: 心内科
- endo: 内分泌科
- gastro: 消化科
- nephro: 肾内科
- heme: 血液科
- resp: 呼吸科
- neuro: 神经内科
- onco: 肿瘤科

**外科及专科系统**
- ortho: 骨科
- derma: 皮肤科
- pedia: 儿科
- gyne: 妇科

**综合系统**
- general: 全科
- psych: 精神科

使用 /specialist list 查看详细信息
```

### 没有医疗数据

```
⚠️ 当前系统中没有医疗数据

请先使用 /save-report 保存医疗检查单，然后再进行专科咨询。
```

## 执行指令

```
1. 验证专科代码是否有效
2. 读取对应的专科 skill 定义文件
3. 根据数据范围参数收集医疗数据
4. 对于相关专科，读取慢性病管理数据
5. 启动专科 subagent 进行分析
6. 收集分析报告并展示给用户
```

## 示例交互

### 示例 1: 心内科分析
```
用户: /specialist cardio recent 5
AI: 🏥 心内科专家分析中...

    读取高血压管理数据...
    读取最近5条检查记录...

    [生成完整分析报告...]
```

### 示例 2: 内分泌科分析
```
用户: /specialist endo all
AI: 🏥 内分泌科专家分析中...

    读取糖尿病管理数据...
    读取所有检查记录...

    [生成完整分析报告...]
```

### 示例 3: 列出所有专科
```
用户: /specialist list
AI: 📋 可用专科列表

    **内科系统**
    - cardio: 心内科
    - endo: 内分泌科
    - gastro: 消化科
    ...

    [完整列表...]
```

## 安全红线

- ❌ 不给出具体用药剂量
- ❌ 不直接开具处方药名
- ❌ 不判断生死预后
- ❌ 不替代医生诊断

## 重要提示

- 专科分析仅供参考，不能替代专业医疗诊断
- 慢性病患者建议定期专科复查
- 所有医疗决策请遵从医生指导
- 紧急情况请立即就医
