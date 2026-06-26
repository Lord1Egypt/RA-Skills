# API 接口文档

此处用于存放驾驶员头部姿态异常（低头/侧视）检测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动驾驶员头部姿态异常检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取头部姿态分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史分心事件
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_DRIVER_HEAD_POSE_ABNORMALITY_ANALYSIS` - 驾驶员头部姿态异常（低头/侧视）检测

## 输入约束

- 摄像头：车载 DMS 摄像头（红外/IR-cut 优先）
- 安装位置：方向盘上方 / A 柱 / 仪表台上方，正对驾驶员面部
- 帧率：≥ 25 FPS；分辨率 ≥ 480p
- 必须能稳定看到面部及头部轮廓；夜间启用红外补光
- 戴帽子/口罩/墨镜可能影响关键点稳定性

## 头部姿态角定义

- `pitch_deg` - 俯仰角（° ， > 0 抬头 / < 0 低头）
- `yaw_deg` - 偏航角（° ， > 0 右转头 / < 0 左转头）
- `roll_deg` - 翻滚角（° ， 头部左右倾斜）

## 默认阈值（可由调用方覆盖）

- 低头判定：`pitch_deg < -30°`
- 侧视判定：`|yaw_deg| > 45°`
- 持续时间阈值：超过 2 秒触发预警（distraction_duration_threshold_sec）

## 预警类型

- `head_down_distraction` - 低头分心（疑似看手机/查物品）
- `head_side_distraction` - 侧视分心（疑似与乘客聊天/看窗外）
- `head_roll_abnormality` - 头部倾斜异常（参考）

## 输出字段（参考）

- `driver_detected` - 是否检测到驾驶员
- `head_pose_angles` - 当前/统计期内头部姿态角（pitch_deg / yaw_deg / roll_deg）
- `head_down_events` - 低头分心事件列表（含开始时间、持续秒数、最大角度）
- `head_side_events` - 侧视分心事件列表（含开始时间、持续秒数、最大角度、方向 left/right）
- `total_distraction_duration_sec` - 累计分心时长（秒）
- `distraction_event_count` - 分心事件总次数
- `warning_type` - 触发的预警类型
- `warning_message` - 预警提示文本（如"驾驶员低头 3.2 秒（最大 -38°），疑似看手机，请立即抬头注视前方"）
- `recommend_action` - 建议的座舱联动动作（voice_alert / fleet_upload / event_record）

> 仅输出基于头部姿态的检测结果与预警，不提供其他安全建议或医学诊断；预警仅供辅助提醒，驾驶员对车辆操作负全责。
