# API 接口文档

此处用于存放老年人呼吸急促/困难识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人呼吸急促识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与呼吸频率
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史呼吸监测记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_TACHYPNEA_DETECTION_ANALYSIS` - 老年人呼吸急促/困难识别

## 输入约束

- 摄像头建议固定于卧室上方/侧方，覆盖胸腹部区域
- 老年人需处于**静息状态**（睡眠或静卧）下采集，避免剧烈活动
- 视频时长建议 ≥ 30 秒（推荐 60 秒）以稳定计算呼吸周期
- 帧率建议 ≥ 15 FPS；夜间启用红外/微光模式

## 关键检测对象

- 胸部 / 腹部起伏轮廓
- 呼吸周期（吸气 + 呼气）
- 微小位移信号（可结合视频放大技术）

## 呼吸频率参考范围（老年人静息）

- 正常：12-20 次/分
- 轻度增快：20-24 次/分
- 呼吸急促（tachypnea）：≥ 24 次/分（默认告警阈值）
- 严重急促：≥ 30 次/分（critical）

## 输出字段（参考）

- `person_detected` - 是否检测到躺卧人体
- `is_resting` - 是否处于静息状态
- `respiratory_rate_bpm` - 呼吸频率（次/分钟）
- `respiratory_pattern` - 呼吸节律描述（regular / irregular / paradoxical）
- `chest_amplitude_pixel` - 胸腹起伏幅度（像素，参考值）
- `signal_quality` - 信号质量（high / medium / low）
- `risk_level` - 风险等级（normal / mild / warning / critical）
- `alert_message` - 提示文本（如"检测到老人静息呼吸频率 26 次/分，超过 24 次/分阈值，建议关注是否有发热、肺炎或心衰等情况，必要时就医"）
- `medical_followup_hint` - 医疗复核提示（仅作建议，非诊断）

> 仅输出基于视觉的呼吸频率数值与异常提示，不提供医学诊断；如疑似肺炎、心衰、慢阻肺急性加重，请及时就医。
