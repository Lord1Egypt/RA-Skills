# API 接口文档

此处用于存放儿童接触危险物品识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童接触危险物品识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与紧急预警
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史预警记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_DANGEROUS_OBJECT_DETECTION_ANALYSIS` - 儿童接触危险物品识别

## 输入约束

- 摄像头建议覆盖客厅、儿童房、厨房等儿童常活动区域
- 视频帧率建议 ≥ 15 FPS，确保手部动作捕捉准确
- 24 小时全天候采集（含红外夜视）

## 预设危险物品类别

- `scissors` - 剪刀
- `knife` - 刀具（菜刀/水果刀）
- `medicine_bottle` - 药品瓶 / 药片
- `lighter` - 打火机 / 火柴
- `cleaning_agent` - 清洁剂 / 化学瓶罐
- `small_object` - 易吞咽小物件（纽扣/电池/硬币）
- `hot_appliance` - 热水壶 / 电热壶
- `socket_finger_insertion` - 手指/导电物体插入电源插座

## 关键检测行为

- `grab` - 抓握危险物品
- `hold_near_mouth` - 危险物品靠近口部（疑似误食）
- `point_at_socket` - 手指/物体指向插座
- `insert_socket` - 手指/导电物体插入插座

## 输出字段（参考）

- `child_detected` - 是否检测到儿童
- `dangerous_object` - 检测到的危险物品类别
- `risk_action` - 触发的危险行为（grab / hold_near_mouth / point_at_socket / insert_socket）
- `confidence` - 危险行为置信度
- `event_time` - 事件发生时间戳
- `snapshot_url` - 现场快照 URL（建议同步推送 APP / 智能音箱）
- `alert_level` - 预警等级（warning / critical / emergency）
- `alert_message` - 紧急预警文本（如"检测到儿童正在抓握剪刀，请立即制止"）

> 仅输出行为识别结果与预警信息，不提供其他安全建议或具体处置方案。
