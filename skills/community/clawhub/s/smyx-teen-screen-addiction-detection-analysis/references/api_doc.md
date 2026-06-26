# API 接口文档

此处用于存放青少年沉迷手机/游戏行为识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动青少年沉迷手机/游戏行为识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取低头时长统计 + 沉迷等级 + 健康提醒
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史沉迷行为记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_TEEN_SCREEN_ADDICTION_DETECTION_ANALYSIS` - 青少年沉迷手机/游戏行为识别

## 输入约束

- 摄像头：家庭书房 / 青少年卧室 / 自习室 / 学校教室固定摄像头，能拍到**侧面或斜侧上半身**（便于计算头部俯仰角与手臂姿态）
- 帧率 ≥ 5 FPS（推荐 10 FPS）；分辨率 ≥ 480p；光照稳定（含夜间偷玩场景需红外补光）
- 视频时长建议 ≥ 30 分钟，过短样本无法统计"单次连续低头"
- 多人场景需按目标跟踪，避免身份串扰（家庭成员/同学）
- 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式

## 关键观测信号

### 姿态识别
- `head_pitch_angle_deg` - 头部俯仰角（向下为正，> 45° 视为"低头看屏幕"姿态）
- `hand_holding_device_detected` - 是否检测到手部抓握设备（手机/平板/掌机）+ 手臂弯曲姿态
- `device_in_view_box` - 设备在视野中的边界框（参考指标）
- `posture_state` - 当前姿态状态（looking_at_screen / normal_reading / writing / lifting_head / other）

### 时长统计
- `current_continuous_screen_min` - 当前连续低头看屏幕时长（分钟）
- `daily_total_screen_min` - 当日累计看屏幕总时长（分钟）
- `session_count_today` - 当日累计独立看屏幕段次数（≥ 5 分钟视为 1 段）
- `longest_session_today_min` - 当日最长单段时长
- `night_screen_minutes` - 夜间（22:00-06:00）看屏幕时长（参考指标，潜在熬夜）

## 阈值与等级（默认值，可在配置中覆盖）

- 单次连续 ≥ **30 分钟** → 建议起身休息（looking_too_long_session）
- 单次连续 ≥ **60 分钟** → 强烈建议起身休息（looking_too_long_critical）
- 日累计 ≥ **2 小时** → 沉迷预警（addiction_warning）
- 日累计 ≥ **4 小时** → 沉迷重度预警（addiction_critical）
- 夜间（22:00-06:00）≥ **30 分钟** → 熬夜玩屏幕提醒（late_night_warning）
- 写作业 / 看书 / 网课（前方有书本 + 头部朝下但角度 < 45°）应识别为 `normal_reading` 或 `writing`，**不计入沉迷时长**

## 输出字段（参考）

- `time_window` / `subject_count`（仅本场景，**禁止跨场景身份关联**）
- `current_posture` / `head_pitch_angle_deg` / `hand_holding_device_detected`
- `current_continuous_screen_min` / `daily_total_screen_min` / `session_count_today` / `longest_session_today_min` / `night_screen_minutes`
- `addiction_level` - 沉迷等级（normal / mild / notable / heavy）
- `dominant_device_guess` - 设备类型猜测（phone / tablet / handheld_console / unknown，**仅用于提示文案，不做识别留存**）
- `alert_type` - 提醒类型（looking_too_long_session / looking_too_long_critical / addiction_warning / addiction_critical / late_night_warning / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `friendly_reminder` - 友好提醒文本（如"宝贝，你已经连续看屏幕 45 分钟了，眼睛该休息啦~ 起来走 3 分钟、看看 6 米外的窗外吧"）
- `parent_summary` - 给家长的日报摘要（如"今日累计看屏幕 2 小时 35 分（已超 2 小时阈值），最长单段 52 分钟，建议在饭后约定 30 分钟亲子户外散步"）
- `recommend_action` - 建议动作（push_eye_break / push_parent_notice / suggest_outdoor_activity / suggest_bedtime / observe_only）

## 强制约束与红线

- ❌ **禁止**输出"游戏成瘾症"等精神医学诊断或量表评分
- ❌ **禁止**长期存储青少年原始视频
- ❌ **禁止**未经监护人同意便将数据提供给学校、机构或第三方
- ❌ **禁止**使用强惩罚性语言（如"再玩就没饭吃"），统一使用**温和、尊重、可执行**的建议
- ✅ 涉及未成年人，必须取得**监护人 + 青少年本人**双重知情同意；建议提前与孩子沟通用途与边界
- ✅ 写作业 / 看书 / 网课场景必须正确归类，**不得**将正常学习行为误报为"沉迷"

> 仅输出基于视觉的客观姿态与时长统计与温和家庭提醒，**不构成游戏成瘾的精神医学诊断**；任何疑似行为成瘾的判定与干预必须由专业心理医生评估制定。
