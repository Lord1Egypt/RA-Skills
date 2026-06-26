# API 接口文档

此处用于存放种子发芽率早期预测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动种子发芽率预测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（出土幼苗计数、发芽率）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史发芽率记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_SEED_GERMINATION_RATE_PREDICTION_ANALYSIS` - 种子发芽率早期预测

## 输入约束

- 推荐使用育苗盘正上方固定摄像头拍摄的高清俯视图像
- 拍摄环境建议光照均匀、相机角度稳定、覆盖整个育苗盘
- 关键观测特征：
  - 子叶刚突破土壤（嫩黄/嫩绿小点）
  - 子叶完全展开（明显绿色叶对）
  - 茎杆挺立

## 推荐附带参数

- `total_seeds` - 该批次播种总粒数
- `sown_date` - 播种日期
- `seed_type` - 种子品种（如生菜/番茄/罗勒）

## 输出字段（参考）

- `sprouted_count` - 已发芽（出土）幼苗数量
- `germination_rate` - 发芽率（%）= sprouted_count / total_seeds × 100
- `daily_curve` - 每日发芽数序列（可绘制发芽率曲线）
- `low_rate_alert` - 发芽率偏低提示（基于阈值，如 < 70%）

> 仅输出基于视觉的计数与发芽率估算，不输出农业建议、温度/湿度调控具体参数。
