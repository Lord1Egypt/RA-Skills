# API 接口文档

此处用于存放成人心率变异性（HRV）趋势监测（面部）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动 HRV 分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（含 SDNN/RMSSD 等指标）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整 HRV 趋势报告

## 场景代码

- `SMYX_FACIAL_HRV_TREND_MONITORING_ANALYSIS` - 成人心率变异性（HRV）趋势监测（面部）

## HRV 关键指标说明

- `SDNN`（ms）：全部正常窦性心搏间期（NN intervals）的标准差，反映总体 HRV
- `RMSSD`（ms）：相邻心搏间期差值的均方根，反映副交感神经活性
- `pNN50`（%）：相邻 NN 间期差值 > 50ms 的占比
- `LF/HF`：低频/高频功率比，反映自交感与副交感平衡
- `mean_HR`（bpm）：分析窗口内平均心率
- `trend`：相对历史基线的变化（rising/stable/declining）
- `stress_level`：基于 HRV 的压力水平估计（low/medium/high）

## 视频采集建议

- 时长：30 - 60 秒
- 光照：自然光或柔和稳定光源，避免强阴影
- 距离：人脸占画面 1/3 以上，正面、保持静止
- 帧率：≥ 25 fps，分辨率 ≥ 480p
