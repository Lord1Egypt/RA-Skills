# API 接口文档

此处用于存放老年人手部震颤（静止性）识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动手部震颤识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（震颤频率与幅度）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史震颤检测记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_HAND_TREMOR_DETECTION_ANALYSIS` - 老年人手部震颤（静止性）识别

## 输入约束

- 视频要求：手部置于桌面或扶手上保持自然静止，**无主动动作**
- 时长建议 ≥ 10 秒（推荐 15-30 秒），帧率 ≥ 30 FPS 以保证频率分析精度
- 拍摄距离建议 30-80 cm，手部完整入画，光照均匀，背景简洁
- 摄像头建议固定（避免镜头自身抖动干扰）

## 关键检测对象

- 手背 / 手指关键点（21 keypoints）
- 周期性位移轨迹（X/Y 方向）
- 频域峰值（FFT 主频）

## 关键观测指标

- `tremor_frequency_hz` - 震颤主频（Hz）
- `tremor_amplitude_pixel` - 震颤峰峰幅度（像素）
- `tremor_consistency` - 节律一致性（0-1）
- `affected_side` - 出现震颤的一侧（left / right / both / none）

## 参考分级（仅用作筛查提示，非临床诊断）

- 频率参考：
  - 4-6 Hz - 经典静止性震颤范围（常见于帕金森）
  - 6-12 Hz - 高频范围（可能为特发性震颤或生理性）
- 幅度参考：
  - small（< 阈值 A）→ 微小
  - medium（A - B）→ 中等
  - large（> 阈值 B）→ 明显

## 风险等级

- `none` - 未检测到明显周期性抖动
- `low` - 微小抖动（可能为正常生理抖动）
- `medium` - 中度可疑静止性震颤
- `high` - 明显静止性震颤（建议尽快神经内科就诊）

## 输出字段（参考）

- `hand_detected` - 是否检测到手部
- `is_resting` - 是否处于静止状态
- `tremor_frequency_hz` - 震颤主频（Hz）
- `tremor_amplitude_pixel` - 震颤幅度（像素）
- `tremor_consistency` - 节律一致性
- `affected_side` - 受累一侧
- `risk_level` - 风险等级（none / low / medium / high）
- `alert_message` - 提示文本（如"检测到右手存在约 5 Hz 周期性抖动，建议神经内科进一步评估"）
- `medical_followup_hint` - 医疗复核建议（仅作提示，非诊断）

> 仅输出基于视频运动分析的客观指标与风险提示，不提供医学诊断；疑似帕金森病或其他神经系统疾病请前往专业医疗机构评估。
