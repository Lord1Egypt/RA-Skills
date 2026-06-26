---
name: nutrition
description: Nutrition analysis and supplement management including diet tracking, nutrient assessment, and food database queries
argument-hint: <操作类型，如：record breakfast 鸡蛋牛奶/food 燕麦/analyze/supplement 维生素D3/recommendations>
allowed-tools: Read, Write
schema: nutrition/schema.json
---

# Nutrition Analysis and Supplement Management Skill

Record diet, assess nutritional status, manage supplements, and provide nutritional recommendations.

## Medical Disclaimer

The nutritional assessment, supplement information, and recommendations provided by this system are for reference only and do not constitute medical diagnosis, treatment, or nutritional prescriptions.

**This System Can:**
- ✅ Record and track dietary intake
- ✅ Assess nutrient intake
- ✅ Identify nutrient deficiency risks
- ✅ Provide general nutritional recommendations
- ✅ Record supplement usage
- ✅ Check known supplement interactions

**This System Cannot:**
- ❌ Diagnose nutritional deficiencies or nutrition-related diseases
- ❌ Prescribe supplements or adjust dosages
- ❌ Replace professional advice from registered nutritionists or doctors
- ❌ Handle severe malnutrition or nutritional metabolic diseases

**When to Seek Medical Care or Consult a Nutritionist:**
- 🏥 Suspected severe nutritional deficiency
- 🏥 Preparing to take new supplements (with chronic disease or on medication)
- 🏥 Experiencing adverse reactions to supplements
- 🏥 Pregnancy or lactation
- 🏥 Chronic diseases

## 核心流程

```
用户输入 -> 识别操作类型 -> 解析信息 -> 检查完整性 -> 生成JSON -> 保存数据
```

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| record | Record meal |
| food | Query food nutrition info |
| compare | Compare foods |
| recommend | Food recommendations |
| analyze | Nutrition analysis |
| supplement | Supplement management |
| interaction | Interaction check |
| status | Nutrition status |
| recommendations | Nutrition recommendations |

## 步骤 2: 检查信息完整性

### Record Diet (record)
- **Required**: Meal type, food
- **Optional**: Time, calorie estimate

### Query Food (food)
- **Required**: Food name

### Supplement Management (supplement)
- **Required**: Supplement name
- **Recommended**: Dose, frequency

## 步骤 3: 生成 JSON

### 饮食记录数据结构

```json
{
  "date": "2025-06-20",
  "meal_type": "breakfast",
  "time": "07:30",
  "foods": ["鸡蛋", "牛奶", "全麦面包"],
  "calories": 450,
  "macronutrients": {
    "protein_g": 20,
    "carbs_g": 55,
    "fat_g": 15,
    "fiber_g": 5
  },
  "micronutrients": {
    "vitamin_a_mcg": 150,
    "vitamin_c_mg": 5,
    "calcium_mg": 250,
    "iron_mg": 2
  }
}
```

### 补充剂数据结构

```json
{
  "id": "supp_001",
  "name": "维生素D3",
  "dose": "2000 IU",
  "frequency": "daily",
  "timing": "breakfast",
  "indication": "vitamin_d_deficiency",
  "start_date": "2025-06-01",
  "monitoring": {
    "baseline_test": "2025-05-15",
    "current_level": 18,
    "target_level": "40-60",
    "next_test": "2025-09-01"
  }
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## 步骤 4: 食物数据库查询

### 查询输出格式

```markdown
# {{食物名称}} 营养信息

## 基本信息
- 名称: 燕麦 (Oats)
- 分类: 谷物类 > 全谷物
- 标准份量: 100克

## 宏量营养素 (每100克)
- 卡路里: 389 卡
- 蛋白质: 16.9g
- 碳水化合物: 66.3g
- 脂肪: 6.9g
- 膳食纤维: 10.6g ✅ 高纤维

## 微量营养素
### 维生素
- 维生素B1: 0.763 mg (66% RDA)
- 维生素B6: 0.165 mg (13% RDA)

### 矿物质
- 镁: 177 mg (44% RDA) ✅
- 磷: 523 mg (75% RDA)
- 锰: 4.916 mg (214% RDA) ✅✅

## 升糖指数
- GI值: 55 (低GI) ✅

## 健康标签
- ✅ 高纤维
- ✅ 低GI
- ✅ 无麸质选项
```

## 步骤 5: 营养分析

### 分析维度

**宏量营养素:**
- 蛋白质、碳水化合物、脂肪、膳食纤维、卡路里

**基础微量营养素:**
- 维生素: A、B族、C、D、E、K
- 矿物质: 钙、铁、镁、磷、钾、钠、锌、硒

**特殊营养素:**
- Omega-3脂肪酸、胆碱、辅酶Q10

## 营养安全原则

1. **不诊断营养缺乏症**
   - 不基于数据诊断疾病
   - 诊断需医生结合实验室检查

2. **不开具补充剂处方**
   - 不推荐具体品牌或剂量
   - 补充剂需医生或营养师指导

3. **不替代专业营养师**
   - 复杂营养管理需营养师
   - 系统仅提供记录和建议

4. **不处理严重营养问题**
   - 严重营养不良需就医
   - 营养代谢疾病需专业治疗

## 执行指令

```
1. 识别操作类型
2. 解析输入参数，提取所有可用信息
3. 检查必填字段，如有缺失则询问用户
4. 从食物数据库查询营养信息（如需要）
5. 计算营养素摄入和评估
6. 生成符合 schema.json 的 JSON
7. 保存到数据文件
8. 向用户确认保存成功，并显示摘要和建议
```

## 示例交互

### 示例 1: 记录饮食
```
用户: 记录早餐 燕麦粥 鸡蛋 牛奶
AI: ✅ 饮食已记录

    早餐 (2025-06-20 07:30):
    • 燕麦粥
    • 鸡蛋
    • 牛奶

    营养分析:
    卡路里: 约450卡
    蛋白质: 20g
    碳水化合物: 55g
    脂肪: 15g
    膳食纤维: 5g

    已保存至营养日志
```

### 示例 2: 查询食物
```
用户: 查询食物 燕麦
AI: # 燕麦 营养信息

    基本信息:
    名称: 燕麦 (Oats)
    分类: 谷物类 > 全谷物
    标准份量: 100克

    宏量营养素 (每100克):
    • 卡路里: 389 卡
    • 蛋白质: 16.9g
    • 碳水化合物: 66.3g
    • 脂肪: 6.9g
    • 膳食纤维: 10.6g ✅

    微量营养素:
    • 镁: 177 mg (44% RDA) ✅
    • 锰: 4.916 mg (214% RDA) ✅✅

    升糖指数:
    GI值: 55 (低GI) ✅

    健康标签:
    ✅ 高纤维、✅ 低GI、✅ 无麸质选项

    营养优势:
    1. 富含β-葡聚糖，有助于降低胆固醇
    2. 高纤维含量，促进肠道健康
    3. 低GI，有利于血糖控制
```

### 示例 3: 营养分析
```
用户: 营养分析
AI: 📊 营养摄入分析报告

    分析周期: 2025-06-14 至 2025-06-20（7天）

    宏量营养素摄入:
    蛋白质: 82g/天 ✅ (目标: 80g)
    碳水化合物: 240g/天 ✅ (目标: 250g)
    脂肪: 68g/天 ⚠️ (目标: 65g)
    膳食纤维: 22g/天 ❌ (目标: 30g)

    维生素状况:
    维生素D: 4 μg ❌ 缺乏
    维生素C: 85 mg ⚠️ 不足
    钙: 850 mg ⚠️ 不足

    洞察与建议:
    1. 📈 增加深海鱼类或鱼油补充剂以提高Omega-3摄入
    2. 📈 增加户外活动和维生素D补充剂
    3. 📈 增加蔬菜和水果种类以提高维生素和矿物质摄入

    [完整报告...]
```

## 重要提示

- 均衡饮食最重要
- 补充剂不能替代均衡饮食
- 过量补充有害
- 自然食物营养素吸收更好
- 孕期、哺乳期需要医生指导补充剂
- 慢性病患者补充剂需医生评估

## 食物数据来源

所有营养数据基于:
- 中国食物成分表
- 美国农业部(USDA)营养数据库
- 科学文献和权威机构数据
