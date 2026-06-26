# 电动车智能检测分析 API 文档

## 接口概述

本技能调用云端计算机视觉AI接口，自动识别禁行区域内的电动摩托车/电动车，统计车辆数量和违规情况，帮助园区、社区、单位进行违规停车/行驶管理，提升区域安全秩序。

## 支持检测车辆类型

| 车辆类型 | 描述 |
|----------|------|
| 电动摩托车 | 两轮电动摩托车 |
| 电动自行车 | 两轮电动自行车 |
| 电动轻便摩托车 | 轻便型电动车 |

## 支持禁行区域类型

| 区域类型 | 适用场景 |
|----------|----------|
| 停车场 | 禁停电动车停车场 |
| 社区园区 | 住宅小区、产业园区禁行区 |
| 校园单位 | 校园、机关单位禁行区 |
| 禁行道路 | 城市道路禁行电动车路段 |
| 其他 | 自定义禁行区域 |

## 违规等级划分

| 等级 | 描述 | 建议措施 |
|------|------|----------|
| 🟢 无违规 | 0辆电动车 | 无需处理 |
| 🟡 轻度违规 | 1-2辆电动车 | 记录提醒 |
| 🟠 中度违规 | 3-5辆电动车 | 需要清理 |
| 🔴 严重违规 | 5辆以上 | 立即清理整治 |

## API 响应字段说明

### 基础信息

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 分析记录ID |
| data.analysis_time | string | 分析时间 |
| data.area_detection.status | string | 区域检测状态 |
| data.area_detection.quality_score | int | 画面质量评分 0-100 |

### 诊断结果

| 字段 | 类型 | 说明 |
|------|------|------|
| data.diagnosis.risk_score | int | 整体风险评分 0-100 |
| data.diagnosis.violation_level | string | 违规等级：normal/mild/moderate/severe |
| data.diagnosis.total_ev_count | int | 检测到电动车总量 |
| data.diagnosis.illegal_parking_count | int | 违规停放数量 |
| data.diagnosis.illegal_driving_count | int | 违规行驶数量 |
| data.diagnosis.average_density_per_frame | float | 平均每帧车辆密度 |
| data.diagnosis.vehicle_counts | object | 各类车辆计数 |
| data.diagnosis.violation_assessment | object | 违规程度评估 |

### 警示与建议

| 字段 | 类型 | 说明 |
|------|------|------|
| data.management_warnings | array[string] | 管理警示信息列表 |
| data.management_suggestions | array[string] | 处理建议列表 |

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

## 使用提示

1. 本工具仅辅助管理使用，最终违规认定需要人工复核
2. 监控视角对识别准确率影响较大，请确保摄像头覆盖完整禁行区域
3. 请遵守相关法律法规，保护个人隐私
