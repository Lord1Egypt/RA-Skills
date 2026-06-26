---
name: tcm-constitution
description: TCM constitution assessment and wellness management including body constitution identification, dietary recommendations, exercise suggestions, acupoint therapy, and herbal medicine references. Use for TCM health tracking and constitution-based wellness planning.
argument-hint: <操作类型 问卷答案/体质类型，如：assess / diet 气虚质 / exercise 气虚质>
allowed-tools: Read, Write
schema: tcm-constitution/schema.json
---

# TCM Constitution Identification and Wellness Management Skill

TCM constitution identification, wellness recommendations, acupoint therapy, and trend analysis.

## Medical Safety Disclaimer

The TCM constitution identification, wellness recommendations, and herbal medicine information provided by this system are for reference only and do not constitute medical diagnosis or treatment recommendations.

**Cannot Do:**
- Do not diagnose TCM diseases
- Do not prescribe herbal medicine
- Do not replace TCM practitioner diagnosis and treatment
- Do not perform acupuncture or other treatments

**Can Do:**
- TCM constitution identification assessment
- Constitution characteristic analysis
- General wellness recommendations
- Acupoint health guidance
- Constitution trend tracking

## When to Seek Medical Care
- Suspected disease symptoms
- Severe constitution imbalance (>80 points)
- Ineffective or worsening after conditioning
- Need herbal medicine treatment
- Pregnancy or lactation
- Severe chronic diseases

## 核心流程

```
用户输入 → 识别操作类型 → [assess] 引导问卷 → 计算体质 → 保存结果
                              ↓
                         [diet/exercise/acupoint/herbal] 基于体质 → 提供建议
                              ↓
                         [status] 读取数据 → 显示体质状态
                              ↓
                         [trend] 读取历史 → 分析趋势
```

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| assess, 评估, 辨识 | assess - Constitution identification |
| diet, 饮食 | diet - Dietary recommendations |
| exercise, 运动 | exercise - Exercise recommendations |
| acupoint, 穴位 | acupoint - Acupoint therapy |
| herbal, 中药 | herbal - Herbal medicine recommendations |
| status, 状态 | status - View constitution status |
| trend, 趋势 | trend - Constitution trend analysis |
| recommendations, 建议 | recommendations - Comprehensive wellness recommendations |

## 步骤 2: 九种体质识别

### 平和质 (A型)
- 阴阳气血调和
- 体型健美
- 面色润泽
- 食欲良好
- 精力充沛

### 气虚质 (B型)
- 主项：疲乏、气短、自汗
- 舌质淡
- 脉弱

### 阳虚质 (C型)
- 主项：畏寒、怕冷、手脚发凉
- 喜热饮食
- 精神不振

### 阴虚质 (D型)
- 主项：盗汗、咽干、手足心热
- 喜冷饮
- 急躁易怒

### 痰湿质 (E型)
- 主项：体型肥胖、腹部肥满
- 面部油脂较多
- 舌苔腻

### 湿热质 (F型)
- 主项：面垢油光、易生痤疮
- 口苦口臭
- 大便黏滞

### 血瘀质 (G型)
- 主项：肤色晦暗、易有瘀斑
- 舌质紫暗
- 眼眶暗黑

### 气郁质 (H型)
- 主项：神情抑郁、多愁善感
- 胁郁不乐
- 乳房胀痛

### 特禀质 (I型)
- 主项：易过敏、喷嚏、鼻塞
| 输入 | 转换结果 |
|-----|---------|
| A. 没有 (1分) | 1 |
| B. 很少 (2分) | 2 |
| C. 有时 (3分) | 3 |
| D. 经常 (4分) | 4 |
| E. 总是 (5分) | 5 |

### 判定标准

| 体质类型 | 转化分 | 判定结果 |
|---------|-------|---------|
| 平和质 | <30分 且 其他8种<40分 | 是 |
| 偏颇质 | >=40分 | 是 |
| 兼夹质 | 2-3种>=40分 | 是 |

## 步骤 3: 生成 JSON

### 体质记录数据结构

```json
{
  "id": "assessment_20250620_001",
  "date": "2025-06-20",
  "primary_type": "气虚质",
  "secondary_types": ["阳虚质"],
  "scores": {
    "peaceful": 42.1,
    "qi_deficiency": 78.5,
    "yang_deficiency": 62.3,
    "yin_deficiency": 35.2,
    "phlegm_dampness": 28.5,
    "damp_heat": 25.3,
    "blood_stasis": 18.6,
    "qi_stagnation": 32.1,
    "special_constitution": 15.8
  }
}
```

## 步骤 4: 保存数据

1. 读取 `data/tcm-constitution-tracker.json`
2. 更新对应记录段
3. 写回文件

## 九种体质特征

### 1. 平和质 (A型)
- 体型匀称健美
- 面色润泽
- 头发稠密有光泽
- 目光有神
- 耐色良好
- 精力充沛
- 不易疲劳
- 睡眠良好

### 2. 气虚质 (B型)
- 主项：疲乏、气短、自汗
- 舌质淡
- 脉弱
- 面色萎黄
- 易出汗
- 易感冒
- 声低懒言
- 精神不振

### 3. 阳虚质 (C型)
- 主项：畏寒怕冷
- 手脚发凉
- 喜热饮食
- 精神不振
- 大便溏薄
- 夜尿清长

### 4. 阴虚质 (D型)
- 主项：盗汗
- 手足心热
- 口燥咽干
- 喜冷饮
- 急躁易怒
- 大便干燥

### 5. 痰湿质 (E型)
- 主项：体型肥胖
- 腹部肥满
- 面部油脂
| 体质 | 运动原则 |
|-----|---------|
| 气虚质 | 温和运动，避免剧烈 |
| 阳虚质 | 温和运动，避免寒冷环境 |
| 阴虚质 | 中等强度运动 |
| 痰湿质 | 中等强度，增加运动量 |
| 血瘀质 | 中等强度，促进血液循环 |
| 气郁质 | 中等强度，疏肝理气 |

## 推荐穴位

### 气虚质
- 足三里：健脾益气
- 气海：培补元气
- 关元：培元固本

### 阳虚质
- 关元：温补肾阳
| 问题 | 建议 |
|-----|------|
| 痰湿质 | • 清淡饮食，少食肥甘厚味<br>• 限制甜食<br>• 戒烟酒 |
| 湿热质 | • 清热利湿<br>• 忌食辛辣<br>• 多饮水 |
| 血瘀质 | • 活血化瘀<br>• 避免寒凉<br>• 少食酸涩 |

更多示例参见 [examples.md](examples.md)。
