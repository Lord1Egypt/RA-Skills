# API 接口文档

此处用于存放老年人面部不对称/口角歪斜识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人面部不对称识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与不对称指数
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史面部对称性记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_FACIAL_ASYMMETRY_ANALYSIS` - 老年人面部不对称/口角歪斜识别

## 输入约束

- 推荐使用正面、平视、清晰、光照均匀的面部图像或短视频
- 单图像或 3-10 秒静止表情视频均可
- 拍摄距离建议 30-80 cm，五官区域清晰可见

## 关键观测指标

- 左右嘴角高度差（mouth_corner_height_diff）
- 鼻唇沟（法令纹）对称性（nasolabial_fold_symmetry）
- 左右眉毛抬高差异（eyebrow_lift_diff）
- 眼裂宽度对称性（eye_aperture_symmetry）
- 整体面部水平中线偏移（midline_offset）

## 不对称指数（0-100%）

- 0-15% - 正常对称范围
- 15-30% - 轻度不对称（建议复测）
- 30-50% - 中度不对称（建议关注）
- ≥ 50% - 重度不对称（强烈建议尽快就医）

## 输出字段（参考）

- `face_detected` - 是否检测到正面面部
- `asymmetry_index` - 面部不对称指数（0-100%）
- `mouth_corner_drop_side` - 口角下垂侧（left / right / none）
- `key_metrics` - 各关键观测指标数值（嘴角差 / 法令纹对称性 / 眉毛抬高差等）
- `risk_level` - 风险等级（normal / mild / moderate / severe）
- `alert_message` - 风险提示文本（如"检测到面部不对称指数偏高，建议关注是否存在面瘫或卒中前兆，必要时就医"）
- `medical_followup_hint` - 建议医疗复核提示（仅作建议，非诊断）

> 仅输出基于面部几何特征的客观指标与风险等级提示，不提供医学诊断；如出现疑似面瘫/口角歪斜伴随其他症状（如肢体无力、言语含糊），请按"中风急救"流程立即就医。
