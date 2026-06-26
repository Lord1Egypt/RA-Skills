# API 接口文档

此处用于存放婴幼儿趴睡窒息风险识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动婴儿趴睡窒息风险识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与风险等级
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史风险预警记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_INFANT_SUFFOCATION_RISK_DETECTION_ANALYSIS` - 婴幼儿趴睡窒息风险识别

## 输入约束

- 摄像头必须固定于婴儿床正上方，俯视拍摄婴儿全身
- 24 小时全天候采集（含红外夜视），帧率建议 ≥ 15 FPS
- 视野需覆盖头部、躯干及周边床面（可能遗留枕头/玩偶/被子）

## 睡姿分类

- `supine` - 仰卧（最安全）
- `side` - 侧卧（中性，需监测翻身）
- `prone` - 俯卧 / 趴睡（高风险）
- `unknown` - 姿态不明（可能被遮挡）

## 口鼻遮挡物类型

- `blanket` - 被子 / 毯子
- `pillow` - 枕头
- `plush_toy` - 毛绒玩具 / 玩偶
- `bedding_fold` - 床单褶皱压住口鼻
- `parent_arm` - 同床成人手臂压住口鼻

## 风险等级

- `low` - 仰卧，口鼻无遮挡
- `medium` - 侧卧或床上有危险物品靠近口鼻
- `high` - 俯卧（趴睡）或口鼻被遮挡
- `critical` - 俯卧 + 口鼻被遮挡 + 持续超过阈值

## 输出字段（参考）

- `infant_detected` - 是否检测到婴儿
- `sleep_posture` - 睡姿（supine / side / prone / unknown）
- `face_occlusion` - 是否检测到口鼻遮挡
- `occlusion_object` - 遮挡物类型
- `risk_level` - 风险等级（low / medium / high / critical）
- `risk_duration_sec` - 风险状态持续秒数
- `event_time` - 事件时间戳
- `snapshot_url` - 现场快照 URL（建议同步推送 APP）
- `alert_message` - 紧急预警文本（如"检测到婴儿趴睡且口鼻被被子遮挡，请立即查看"）

> 仅输出基于视觉的睡姿与遮挡判断结果，不提供医疗诊断或具体处置方案。
