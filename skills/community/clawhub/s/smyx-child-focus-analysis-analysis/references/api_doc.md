# API 接口文档

此处用于存放儿童专注度与走神时段分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童专注度分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（专注得分 + 走神时段）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史专注度记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_FOCUS_ANALYSIS_ANALYSIS` - 儿童专注度与走神时段分析

## 输入约束

- 摄像头建议为智能台灯内置摄像头或桌面摄像头，正对儿童面部 + 书本/屏幕区域
- 视频时长可短可长，按整段或每分钟切片输出
- 帧率建议 ≥ 15 FPS；光照均匀

## 关键观测指标

- 面部朝向（face_orientation）：是否偏离书本/屏幕
- 视线方向（gaze_direction）：是否注视学习区域
- 头部抬起/低下频次
- 手部小动作（玩笔 / 摸脸 / 摆弄物品 / 玩手机）
- 是否离开座位

## 专注得分（每分钟，0-100）

- 视线在学习区域比例（gaze_on_task_ratio）
- 面部朝向稳定度（face_stability）
- 手部小动作频次（罚分项）
- 离座时长（罚分项）

## 走神/分心事件类型

- `gaze_away` - 视线长时间偏离
- `head_lift` - 频繁抬头/转头
- `hand_fidget` - 玩笔/摸脸等小动作
- `off_seat` - 离开座位
- `phone_use` - 玩手机/平板

## 输出字段（参考）

- `child_detected` - 是否检测到儿童
- `session_duration_min` - 当次会话时长（分钟）
- `focus_score_overall` - 整体专注度（0-100）
- `focus_score_per_minute` - 每分钟专注得分序列
- `distraction_events` - 走神事件列表（类型 + 起止时间 + 持续秒数）
- `total_distraction_min` - 累计走神分钟数
- `focus_grade` - 整体等级（excellent / good / fair / poor）
- `alert_message` - 持续专注度偏低时的提醒（如"近 10 分钟专注度持续低于 40 分，建议短暂休息"）

> 仅输出基于视觉的专注度客观指标与走神事件统计，不提供教学建议或学习方案。
