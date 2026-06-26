# 职场玩手机行为监测分析 API 文档

## 接口概述

本技能调用云端视觉AI接口，自动识别办公区域员工玩手机行为，支持视频流动态统计和图片静态检测。

## 支持检测的行为类型

| 行为类型 | 描述 | 统计方式 |
|----------|------|----------|
| 手持手机 | 员工手持智能手机，屏幕朝向面部 | 按次数/时长统计 |
| 低头看手机 | 员工低头注视手机屏幕 | 按时长分段统计 |
| 持续使用 | 连续使用手机超过设定时长（默认3分钟） | 记为违规行为 |
| 桌面放置 | 手机放置在桌面但未使用 | 不计数 |

## 支持检测区域

| 区域类型 | 特点 |
|----------|------|
| 开放办公区 | 多人员工同时监测 |
| 独立工位 | 单人固定工位监测 |
| 会议室 | 会议场景监测 |
| 其他区域 | 自定义区域 |

## API 响应字段说明

### 基础信息

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 分析记录ID |
| data.analysis_time | string | 分析时间 |
| data.person_detection.status | string | 人员检测状态 |
| data.person_detection.quality_score | int | 画面质量评分 0-100 |

### 诊断结果

| 字段 | 类型 | 说明 |
|------|------|------|
| data.diagnosis.compliance_score | int | 整体合规评分 0-100（分数越高越合规）|
| data.diagnosis.overall_compliance | string | 整体合规状况：合规/轻度违规/中度违规/严重违规 |
| data.diagnosis.total_phone_usage_count | int | 检测到玩手机行为总次数 |
| data.diagnosis.total_phone_usage_duration | int | 累计玩手机总时长（秒）|
| data.diagnosis.phone_usage_behavior | object | 各行为识别结果 |
| data.diagnosis.usage_duration | object | 时长分段统计结果 |
| data.diagnosis.area_compliance | object | 各区域合规评估 |

### 预警与建议

| 字段 | 类型 | 说明 |
|------|------|------|
| data.efficiency_warnings | array[string] | 效率风险警示信息列表 |
| data.improvement_suggestions | array[string] | 效率提升建议列表 |

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

## 合规提示

1. 使用本工具应当遵守国家相关劳动法律法规
2. 需要提前告知员工监控范围和目的，保护员工个人隐私
3. 本工具仅辅助办公管理，不建议作为唯一奖惩依据
4. 建议合理设定允许使用手机的休息时段，平衡工作与休息
