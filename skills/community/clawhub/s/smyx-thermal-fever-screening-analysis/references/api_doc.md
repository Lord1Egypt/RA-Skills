# API 接口文档

此处用于存放家庭多人聚集时体温相对异常检测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动多人聚集体温相对异常检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取相对体温分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史筛查记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_THERMAL_FEVER_SCREENING_ANALYSIS` - 家庭多人聚集时体温相对异常检测

## 输入约束

- 摄像头：**必须为热成像（红外测温）摄像头**，普通可见光摄像头无法支持
- 安装位置：家庭客厅、餐厅、会议室、活动室等公共区域，可同时覆盖 ≥ 2 人
- 帧率：≥ 5 FPS；分辨率：≥ 256×192（建议 384×288 或更高）
- 测温距离：1-3 m 之间为佳；测温目标头部需充分露出（避免帽子/口罩遮挡额头）
- 环境温度建议恒定，避免短时空调直吹、紧邻热源（炉灶/取暖器）

## 关键观测特征

- `persons_detected` - 当前场景检测到的人数
- `face_visible_count` - 头部/额头清晰可见的人数（参与温度比较的有效样本数）
- `per_person_temperature` - 每个人的额头体表温度（°C，已校正）
- `group_avg_temperature` - 群体平均体表温度（°C）
- `group_temperature_std` - 群体体表温度标准差（°C）
- `temperature_delta_per_person` - 每个人相对群体均值的差值（°C）

## 默认阈值（可由调用方覆盖）

- 相对异常阈值：`|temperature_delta| > 1.5 °C`（默认）
- 最小有效样本数：≥ 2 人（少于 2 人时不输出相对异常）
- 持续时间：相对异常持续 ≥ 3 秒触发提醒（防止偶发误报）

## 异常类型

- `relatively_hotter` - 个体体表温度显著高于群体均值（疑似发热）
- `relatively_colder` - 个体体表温度显著低于群体均值（多为环境因素，仅参考）
- `insufficient_sample` - 有效样本数不足，不进行相对比较

## 输出字段（参考）

- `persons_detected` / `face_visible_count` / `sample_sufficient`
- `group_metrics` - 群体统计（group_avg_temperature / group_temperature_std）
- `per_person_results` - 每个人的结果列表（含 person_id / forehead_temp_c / delta_c / is_relative_anomaly / anomaly_type）
- `anomaly_count` - 本次异常人数
- `alert_message` - 推送文本（如"客厅检测到 4 人，其中 1 人额头体表温度比群体均值高 1.8°C，建议使用额温枪复测体温"）
- `recommend_action` - 建议动作（recheck_with_thermometer / push_app_notice / observe_only）

> 仅输出基于热成像的相对温度差异与方向性提醒，不提供发热、流感、COVID 等具体医学诊断；正式体温判定请使用经过校准的医用红外/水银/电子额温枪/口腔体温计复测，并由专业医生评估。
