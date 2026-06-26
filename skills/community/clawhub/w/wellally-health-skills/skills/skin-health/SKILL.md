---
name: skin-health
description: Manage skin health tracking including skin problems, mole monitoring with ABCDE rule, skincare routines, sun exposure tracking, and skin cancer screening. Use for mole monitoring, acne tracking, and dermatology visit records.
argument-hint: <操作类型 皮肤问题/痣描述，如：mole back 4mm 棕色，扁平>
allowed-tools: Read, Write
schema: skin-health/schema.json
---

# 皮肤健康管理技能

记录皮肤问题、监测痣的变化、管理护肤程序、跟踪皮肤健康状态、分析皮肤健康趋势。

## 医学免责声明

本系统仅用于健康追踪和教育目的，不提供医学诊断或治疗建议。

**不能做到:**
- 所有皮肤问题应咨询专业皮肤科医生
- 痣的异常变化应立即就医检查
- 不能替代专业皮肤科检查和治疗

**能做到:**
- 记录和追踪皮肤健康数据
- 提供皮肤检查记录和提醒
- 提供ABCDE法则自查指导
- 提供一般性护肤建议

## 核心流程

```
用户输入 → 识别操作类型 → [concern] 解析皮肤问题 → 保存记录
                              ↓
                         [mole] 解析痣信息 → ABCDE评估 → 保存
                              ↓
                         [routine] 解析护肤程序 → 保存
                              ↓
                         [exam] 记录检查结果 → 保存
                              ↓
                         [sun] 记录日晒信息 → 保存
                              ↓
                         [status/trend] 读取数据 → 显示报告
```

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| concern | concern - Skin problem record |
| mole | mole - Mole monitoring |
| routine | routine - Skincare routine |
| exam | exam - Skin exam record |
| sun | sun - Sun exposure record |
| status | status - View status |
| trend | trend - Trend analysis |
| reminder | reminder - Exam reminder |
| screening | screening - Disease screening |

## 步骤 2: 参数解析规则

### 皮肤问题类型

| Input Keywords | Type |
|---------------|------|
| acne | acne |
| eczema | eczema |
| psoriasis | psoriasis |
| pigmentation | pigmentation |
| rosacea | rosacea |
| dermatitis | dermatitis |
| dryness | dryness |
| oiliness | oiliness |
| sensitivity | sensitivity |
| scars | scars |

### 严重程度

| Input | Severity |
|-------|----------|
| mild | mild |
| moderate | moderate |
| severe | severe |

### 常见部位

| 面部 | 身体 |
|-----|------|
| forehead（额头）、cheeks（脸颊） | arms（手臂） |
| chin（下巴）、nose（鼻子） | legs（腿部） |
| around_eyes（眼周） | back（背部） |
| neck（颈部） | chest（胸部） |

## ABCDE法则详解

### A - Asymmetry（不对称性）
- 正常：痣从中间对折，两边基本对称
- 异常：痣的两半不对称，形状不规则

### B - Border（边缘）
- 正常：边缘清晰、平滑、规则
- 异常：边缘模糊、不规则、锯齿状、扇贝状

### C - Color（颜色）
- 正常：颜色均匀，通常是棕色、黑色或肤色
- 异常：颜色不均匀，包含多种颜色

### D - Diameter（直径）
- 正常：直径通常小于6mm
- 异常：直径大于6mm，或近期明显增大

### E - Evolution（变化/进展）
- 正常：长期稳定，无明显变化
- 异常：近期大小、形状、颜色、厚度、感觉发生变化

## 步骤 3: 生成 JSON

### 皮肤问题记录

```json
{
  "id": "concern_20250610_001",
  "date": "2025-06-10",
  "issue_type": "acne",
  "severity": "moderate",
  "location": "face",
  "specific_areas": ["forehead", "cheeks"],
  "description": "额头和脸颊有痤疮，中度严重",
  "triggers": ["hormonal", "stress"],
  "notes": ""
}
```

### 痣的监测记录

```json
{
  "id": "mole_20250610_001",
  "date": "2025-06-10",
  "location": "back",
  "size_mm": 4,
  "color": "brown",
  "shape": "flat",
  "abcde_assessment": {
    "asymmetry": false,
    "border": "regular",
    "color": "uniform",
    "diameter": false,
    "evolution": false
  },
  "risk_level": "low",
  "notes": ""
}
```

### 护肤程序记录

```json
{
  "date": "2025-06-10",
  "routine_type": "morning",
  "steps": ["cleanser", "toner", "moisturizer", "spf30"],
  "products_used": {
    "cleanser": "温和洁面乳",
    "toner": "爽肤水",
    "moisturizer": "保湿霜",
    "sunscreen": "SPF30防晒霜"
  }
}
```

## 步骤 4: 保存数据

1. 读取 `data/skin-health-tracker.json`
2. 更新对应记录段
3. 写回文件

## 皮肤类型识别

| 类型 | 特征 | 护肤重点 |
|-----|------|---------|
| 干性皮肤 | 皮肤紧绷、粗糙、可能有皮屑 | 保湿、补水、避免过度清洁 |
| 油性皮肤 | 油光明显、毛孔粗大、易长痘 | 控油、清洁、水油平衡 |
| 混合性皮肤 | T区油、两颊干 | 分区护理、平衡水油 |
| 中性皮肤 | 水油平衡、毛孔细小 | 维持现状、基础护理 |
| 敏感性皮肤 | 易泛红、刺痛、瘙痒、过敏 | 温和、舒缓、避免刺激 |

## 紧急情况指南

### 需要紧急处理（24小时内）
- 痣突然出血、溃疡
- 痣快速增大或颜色改变
- 新出现的可疑痣
- 大面积皮疹伴发热
- 严重过敏反应

### 需要尽快就诊（1周内）
- 痣出现ABCDE异常
- 伤口或溃疡超过2周未愈合
- 持续性瘙痒影响睡眠

## 健康建议

### 预防皮肤癌
- 每天使用广谱防晒霜（SPF 30或更高）
- 避免上午10点至下午4点的强烈日晒
- 穿戴防护衣物（帽子、长袖、太阳镜）
- 定期进行皮肤自我检查（每月一次）

### 管理痤疮
- 保持皮肤清洁，但不过度清洁
- 使用非致痘性护肤品
- 避免挤压或挑破痘痘
- 保持健康饮食，减少高糖食物

更多示例参见 [examples.md](examples.md)。
