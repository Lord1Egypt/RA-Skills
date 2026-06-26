---
name: sexual-health
description: Track sexual health checkups, manage STD screening, track contraception methods, and analyze sexual health trends with IIEF-5 and FSFI assessments
argument-hint: <操作类型+信息，如：checkup libido normal，iief5 score 18，std hiv negative，contraception condom>
allowed-tools: Read, Write
schema: sexual-health/schema.json
---

# 性健康管理技能

记录性健康检查、管理STD筛查、追踪避孕方式、分析性健康趋势。支持IIEF-5交互式问卷、FSFI评分、性活动日志等全面功能。

## 核心流程

```
用户输入 → 解析操作类型 → 执行对应操作 → 生成/更新数据 → 保存 → 输出结果
```

## 支持的操作类型

| 操作 | 说明 | 示例 |
|------|------|------|
| checkup | 健康检查 | /sexual checkup libido normal |
| iief5 | IIEF-5问卷 | /sexual iief5 score 18 |
| fsfi | 女性性功能指数 | /sexual fsfi score 28.5 |
| std | STD筛查 | /sexual std hiv negative |
| contraception | 避孕管理 | /sexual contraception condom |
| activity | 性活动日志 | /sexual activity satisfaction 7 |
| medication | 用药记录 | /sexual medication sildenafil 50mg |
| status | 状态查询 | /sexual status |
| trend | 趋势分析 | /sexual trend iief5 |
| reminder | 提醒设置 | /sexual reminder std 6 months |

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| checkup | checkup |
| iief5, IIEF | iief5 |
| fsfi | fsfi |
| std | std |
| contraception | contraception |
| activity | activity |
| medication | medication |
| status | status |
| trend | trend |
| reminder | reminder |

### IIEF-5评分识别

| 总分 | ED严重程度 | 建议 |
|------|-----------|------|
| 22-25 | 正常勃起功能 | 继续保持健康生活方式 |
| 17-21 | 轻度ED | 生活方式调整 |
| 12-16 | 轻中度ED | 建议咨询医生 |
| 8-11 | 中度ED | 建议就医，可能需要药物治疗 |
| 5-7 | 重度ED | 需要就医进行全面评估 |

### STD类型识别

| Disease | English | Screening Method |
|--------|-------|----------------|
| HIV | HIV | Blood test |
| Syphilis | Syphilis | Blood test |
| Chlamydia | Chlamydia | Urine/swab |
| Gonorrhea | Gonorrhea | Urine/swab |
| HPV | HPV | Swab/DNA test |
| Hepatitis B | Hepatitis B | Blood test |
| Herpes | Herpes | Swab/blood test |

### STD结果识别

| Normal | Abnormal |
|-------|---------|
| negative, clear | positive |

### 避孕方法识别

| Method | English | Typical Effectiveness |
|--------|-------|----------------------|
| Condom | condom | 85% |
| Pill | pill | 91% |
| IUD | IUD | 99% |
| Implant | implant | 99% |
| Withdrawal | withdrawal | 78% |
| Rhythm | rhythm | 76-88% |
| Sterilization | sterilization | 99% |

### 勃起困难频率识别

| Keyword | Frequency |
|--------|----------|
| always | always |
| usually | usually |
| sometimes | sometimes |
| rarely | rarely |
| almost never | almost_never |

### 性欲识别

| Keyword | Level |
|--------|-------|
| normal, good | normal |
| decreased, low | decreased |
| very low | very_low |
| absent | absent |

## 步骤 2: 检查信息完整性

### iief5 操作必填项
- 总分（0-25）或各题得分

### std 操作建议有
- 疾病类型
- 筛查结果

### contraception 操作建议有
- 避孕方法类型

### activity 操作建议有
- 频率或满意度

## 步骤 3: 交互式询问（如需要）

### 场景 A: IIEF-5问卷启动
```
国际勃起功能指数-5 (IIEF-5) 问卷

问题1：在过去6个月内，您有多少次对自己的勃起感到有信心？
• 0分 - 无性活动
• 1分 - 几乎没有/从不
• 2分 - 少数几次（远少于一半时候）
• 3分 - 有时（约一半时候）
• 4分 - 多数时候（远多于一半时候）
• 5分 - 几乎总是/总是

请选择0-5分：
```

### 场景 B: 缺少STD结果
```
请提供STD筛查结果：
• negative / 阴性 / 正常
• positive / 阳性 / 异常
```

### 场景 C: 缺少避孕方法
```
请选择避孕方法：
• condom - 避孕套
• pill - 口服避孕药
• IUD - 宫内节育器
• implant - 皮下埋植
• withdrawal - 体外射精
• rhythm - 安全期法
• none - 未使用
```

## 步骤 4: 生成 JSON

### 性健康数据结构

```json
{
  "sexual_health_tracking": {
    "last_updated": "2025-01-01T00:00:00.000Z",

    "male_assessment": {
      "iief5": {
        "last_assessed": null,
        "total_score": null,
        "risk_level": null,
        "q1_confidence": null,
        "q2_erection": null,
        "q3_penetration": null,
        "q4_maintenance": null,
        "q5_satisfaction": null,
        "score_history": []
      },
      "libido": {
        "level": null,
        "change": null,
        "notes": ""
      }
    },

    "female_assessment": {
      "fsfi": {
        "last_assessed": null,
        "total_score": null,
        "desire_score": null,
        "arousal_score": null,
        "lubrication_score": null,
        "orgasm_score": null,
        "satisfaction_score": null,
        "pain_score": null,
        "score_history": []
      }
    },

    "std_screening": {
      "last_screened": null,
      "next_due": null,
      "risk_level": "low",
      "results": {
        "hiv": {"status": null, "date": null},
        "syphilis": {"status": null, "date": null},
        "chlamydia": {"status": null, "date": null},
        "gonorrhea": {"status": null, "date": null},
        "hpv": {"status": null, "date": null},
        "hepatitis_b": {"status": null, "date": null},
        "herpes": {"status": null, "date": null}
      }
    },

    "contraception": {
      "current_method": null,
      "start_date": null,
      "effectiveness": null,
      "side_effects": [],
      "satisfaction": null,
      "history": []
    },

    "activity_log": {
      "frequency_weekly": null,
      "frequency_monthly": null,
      "satisfaction_average": null,
      "protection_usage": null,
      "last_activity": null,
      "logs": []
    },

    "medication": {
      "pde5_inhibitors": {
        "current_use": false,
        "medication": null,
        "dose": null,
        "frequency": null,
        "effectiveness": null,
        "side_effects": []
      },
      "other_medications": []
    },

    "notes": ""
  }
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## 步骤 5: 保存数据

1. 读取 `data/sexual-health-tracker.json`
2. 更新对应数据
3. 写回文件

## 执行指令

```
1. 解析用户输入，确定操作类型
2. 根据操作类型执行相应逻辑
3. 验证输入数据和状态
4. 生成符合 schema.json 的 JSON
5. 保存到 data/sexual-health-tracker.json
6. 向用户输出操作结果和摘要
```

## 示例交互

### 示例 1: IIEF-5评分
```
用户: /sexual iief5 score 18

系统:
IIEF-5评估完成

IIEF-5总分：18分

风险评估：轻度ED

建议：
• 生活方式调整（戒烟、限酒、运动）
• 减轻压力和焦虑
• 如持续或加重，建议咨询医生

ED可能是心血管健康的预警信号，
建议关注整体健康状况。
```

### 示例 2: STD筛查
```
用户: /sexual std screening all clear

系统:
STD筛查已记录

筛查日期：2025年1月1日

结果：
• HIV：阴性
• 梅毒：阴性
• 衣原体：阴性
• 淋病：阴性
• 乙肝：阴性
• 疱疹：阴性

下次筛查：
建议：1年后复查

风险等级：低
```

### 示例 3: 避孕记录
```
用户: /sexual contraception condom

系统:
避孕记录已更新

当前方法：避孕套

有效性：
• 典型使用有效率：85%
• 完美使用有效率：98%

优点：
• 预防性传播疾病
• 无激素副作用
• 易于获得

注意事项：
• 每次使用都要正确佩戴
• 注意保质期
• 储存在阴凉干燥处
```

### 示例 4: 查看状态
```
用户: /sexual status

系统:
性健康状态概览

男性性功能：
• IIEF-5评分：18分（轻度ED）
• 最后评估：2025年1月1日

STD筛查：
• 最后筛查：2025年1月1日
• 结果：全阴性
• 下次筛查：2026年1月

避孕：
• 当前方法：避孕套
• 满意度：良好

建议：
• 3个月后复评IIEF-5
• 继续使用保护措施
• 年度STD筛查
```

更多示例参见 [examples.md](examples.md)。
