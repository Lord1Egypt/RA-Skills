# API 接口文档

此处用于存放老年人服药动作确认（取药/入口/吞咽）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人服药动作依从性分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与依从性判断
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史用药依从性记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_MEDICATION_COMPLIANCE_ANALYSIS` - 老年人服药动作确认（取药/入口/吞咽）

## 输入约束

- 摄像头建议安装于药箱上方或侧方，能同时拍摄到药盒、双手及口部/颈部
- 24 小时全天候采集（建议覆盖每日服药时间窗口）
- 视频帧率建议 ≥ 15 FPS，确保手部 + 吞咽动作捕捉

## 三大关键步骤

- `step_1_pick_up` - 取药：手从药盒中取出药片/胶囊
- `step_2_to_mouth` - 送入口中：手部将药物送至嘴边（接触口唇区域）
- `step_3_swallow` - 吞咽：颈部喉结运动或下颌运动

## 依从性判定

- `completed` - 三步全部完成（按时按量服药）
- `partial_pickup_only` - 仅完成取药，未送入口中
- `partial_no_swallow` - 取药 + 入口完成，但未观察到吞咽
- `not_observed` - 在服药时间窗口内未检测到服药动作
- `unknown` - 关键步骤检测置信度偏低

## 输出字段（参考）

- `person_detected` - 是否检测到老人
- `step_1_pick_up_detected` - 是否检测到取药动作（+ 时间戳）
- `step_2_to_mouth_detected` - 是否检测到送入口中动作（+ 时间戳）
- `step_3_swallow_detected` - 是否检测到吞咽动作（+ 时间戳）
- `compliance_status` - 依从性状态（completed / partial_pickup_only / partial_no_swallow / not_observed / unknown）
- `missed_step` - 缺失的步骤（若有）
- `confidence` - 整体判定置信度
- `event_time` - 事件时间戳
- `snapshot_url` - 现场快照 URL
- `alert_message` - 提醒文本（如"宝奶奶在 08:00 取药后未观察到吞咽，请家人确认"）

> 仅输出基于视觉的服药动作步骤检测与依从性判断，不提供医疗建议（如药量调整、用药方案变更）。
