# 呼吸道症状智能识别分析 API 文档

## 接口概述

本技能调用云端视觉AI接口，自动识别视频中的咳嗽、咳痰、喘息等呼吸道症状，统计发作频次，评估严重程度，实现健康异常早期提醒。

## 支持识别的呼吸道症状

| 症状类型 | 描述 | 统计方式 |
|----------|------|----------|
| 咳嗽 | 胸部收缩+张口咳嗽动作识别 | 按发作次数统计 |
| 咳痰 | 咳嗽后清痰动作识别 | 按发作次数统计 |
| 喘息 | 呼吸急促、张口喘息识别 | 按发作次数统计 |
| 胸闷 | 胸部不适表情识别 | 按持续时间评估 |

## 监测场景

| 场景类型 | 适用场景 |
|----------|----------|
| 日常监测 | 居家日常健康监测 |
| 术后康复 | 手术后呼吸道康复监测 |
| 病房监测 | 医院病房持续监测 |
| 其他 | 自定义监测场景 |

## 风险等级划分

| 等级 | 描述 | 建议 |
|------|------|------|
| 🟢 正常 | 症状发作频次在正常范围 | 继续日常监测 |
| 🟡 轻度 | 轻度症状，偶发 | 注意休息，观察变化 |
| 🟠 中度 | 中度症状，频发 | 建议就医检查 |
| 🔴 重度 | 重度症状，频繁发作 | 立即就医 |

## API 响应字段说明

### 基础信息

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 分析记录ID |
| data.analysis_time | string | 分析时间 |
| data.person_detection.status | string | 对象检测状态 |
| data.person_detection.quality_score | int | 画面质量评分 0-100 |

### 诊断结果

| 字段 | 类型 | 说明 |
|------|------|------|
| data.diagnosis.risk_score | int | 整体风险评分 0-100 |
| data.diagnosis.risk_level | string | 风险等级：normal/mild/moderate/severe |
| data.diagnosis.total_cough_count | int | 咳嗽总次数 |
| data.diagnosis.total_sputum_count | int | 咳痰总次数 |
| data.diagnosis.total_wheeze_count | int | 喘息总次数 |
| data.diagnosis.average_freq_per_minute | float | 平均每分钟发作频次 |
| data.diagnosis.symptom_counts | object | 各症状详细计数 |
| data.diagnosis.severity_assessment | object | 各症状严重程度评估 |

### 警示与建议

| 字段 | 类型 | 说明 |
|------|------|------|
| data.health_warnings | array[string] | 健康风险警示信息列表 |
| data.medical_suggestions | array[string] | 就医护理建议列表 |

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | API 鉴权失败 |
| 413 | 文件大小超出限制 |
| 415 | 不支持的文件格式 |
| 500 | 服务器内部错误 |
| 503 | 服务繁忙，请稍后重试 |
| COMMON_AI_ANALYSIS_TIMEOUT | AI分析超时，请稍后重试 |

## 医学提示

1. 本工具仅用于辅助健康监测和早期异常提醒
2. 不能替代专业医师诊断、胸部X光、CT等医学检查
3. 分析结果仅供参考，确诊请遵医嘱进行相关检查
4. 如果出现严重呼吸困难，请立即就医，不要依赖工具监测
