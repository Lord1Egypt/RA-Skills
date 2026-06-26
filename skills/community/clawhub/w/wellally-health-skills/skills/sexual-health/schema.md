# SexualHealthTracker Schema

性健康管理的完整数据结构定义。

## Schema 文件

完整的JSON Schema定义：[schema.json](schema.json)

## 字段速查

### 根级别字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `created_at` | string | ISO 8601 创建时间 |
| `last_updated` | string | ISO 8601 最后更新时间 |
| `sexual_health_tracking` | object | 性健康追踪数据 |
| `statistics` | object | 统计数据 |
| `settings` | object | 设置 |

### male_assessment.iief5 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `last_assessed` | string/null | 最后评估日期 |
| `total_score` | int/null | IIEF-5总分（0-25） |
| `risk_level` | enum | ED风险等级 |
| `q1_confidence` | int/null | 问题1得分（0-5） |
| `q2_erection` | int/null | 问题2得分（0-5） |
| `q3_penetration` | int/null | 问题3得分（0-5） |
| `q4_maintenance` | int/null | 问题4得分（0-5） |
| `q5_satisfaction` | int/null | 问题5得分（0-5） |
| `score_history` | array | 评分历史 |

### female_assessment.fsfi 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `last_assessed` | string/null | 最后评估日期 |
| `total_score` | number/null | FSFI总分（2-36） |
| `desire_score` | number/null | 性欲得分（1.2-6） |
| `arousal_score` | number/null | 性兴奋得分（0-6） |
| `lubrication_score` | number/null | 阴道润滑得分（0-6） |
| `orgasm_score` | number/null | 性高潮得分（0-6） |
| `satisfaction_score` | number/null | 满意度得分（0.8-6） |
| `pain_score` | number/null | 疼痛得分（0-6） |

### std_screening.results 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `hiv` | object | HIV检测结果 |
| `syphilis` | object | 梅毒检测结果 |
| `chlamydia` | object | 衣原体检测结果 |
| `gonorrhea` | object | 淋病检测结果 |
| `hpv` | object | HPV检测结果 |
| `hepatitis_b` | object | 乙肝检测结果 |
| `herpes` | object | 疱疹检测结果 |

### std result 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `status` | enum | 结果：negative/positive/pending |
| `date` | string/null | 检测日期 |

### contraception 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `current_method` | enum | 当前避孕方法 |
| `start_date` | string/null | 开始日期 |
| `effectiveness` | enum | 有效性：high/moderate/low |
| `side_effects` | string[] | 副作用 |
| `satisfaction` | enum | 满意度 |
| `history` | array | 使用历史 |

## 枚举值

### iief5.risk_level
`normal` (正常22-25) | `mild` (轻度17-21) | `mild_moderate` (轻中度12-16) | `moderate` (中度8-11) | `moderate_severe` (中重度5-7) | `severe` (重度0-4)

### contraception.current_method
`condom` (避孕套) | `pill` (口服避孕药) | `IUD` (宫内节育器) | `implant` (皮下埋植) | `injection` (避孕针) | `withdrawal` (体外射精) | `rhythm` (安全期) | `sterilization` (结扎) | `none` (无)

### protection_usage
`always` (总是) | `usually` (通常) | `sometimes` (有时) | `rarely` (很少) | `never` (从不)

### std status
`negative` (阴性) | `positive` (阳性) | `pending` (待检测)

## IIEF-5评分标准

| 总分 | ED严重程度 | 建议 |
|------|-----------|------|
| 22-25 | 正常勃起功能 | 继续保持健康生活方式 |
| 17-21 | 轻度ED | 生活方式调整，如持续建议就医 |
| 12-16 | 轻中度ED | 建议咨询医生评估原因 |
| 8-11 | 中度ED | 建议就医，可能需要药物治疗 |
| 5-7 | 重度ED | 需要就医进行全面评估 |
| 0-4 | 极重度ED | 立即就医 |

## 避孕方法有效率

| 方法 | 典型使用 | 完美使用 | STD防护 |
|------|---------|---------|---------|
| 避孕套 | 85% | 98% | 是 |
| 口服避孕药 | 91% | 99.7% | 否 |
| 宫内节育器 | 99%+ | 99%+ | 否 |
| 皮下埋植 | 99%+ | 99%+ | 否 |
| 避孕针 | 94% | 99%+ | 否 |
| 体外射精 | 78% | 96% | 否 |
| 安全期法 | 76-88% | 95-99% | 否 |

## STD筛查频率建议

| 风险等级 | 建议频率 | 适用人群 |
|----------|----------|----------|
| 高风险 | 每3-6个月 | 多性伴侣、性工作者、MSM |
| 一般风险 | 每年1次 | 性活跃人群 |
| 低风险 | 每1-2年 | 单一稳定伴侣 |

## 数据存储

- 主文件: `data/sexual-health-tracker.json`
- 模式: 更新
