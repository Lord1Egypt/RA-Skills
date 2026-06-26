# API 接口文档

此处用于存放鱼苗生长速度测量（通过参照物）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼苗生长速度测量任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取测量结果（体长 mm + 生长速率 mm/day + 生长曲线）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史测量报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出生长曲线报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 智能鱼苗缸建议调整投喂量）

## 场景代码

- `SMYX_FISH_FRY_GROWTH_MEASUREMENT_ANALYSIS` - 鱼苗生长速度测量（通过参照物）

## 输入约束

- 摄像头：鱼苗缸固定摄像头 / 智能鱼苗缸内置摄像头 / 手机微距镜头（俯拍）
- 分辨率 ≥ 1080p（鱼苗 5-30mm 全长，需高清才能精确测量到亚毫米级）
- **关键硬件要求**：**视野内必须放置已知尺寸的参照物**（recognized reference object），三选一：
    - 防水刻度尺（最佳，建议金属/塑料防水尺，黑底白刻度对比强）
    - 标准硬币（1 元硬币 25.0mm / 5 角 20.5mm / 1 角 19.0mm；美元 quarter 24.26mm）
    - 标定板（黑白棋盘格 5mm/10mm 已知边长）
- 拍摄角度：**严格俯拍（垂直向下）**，参照物与鱼苗位于**同一水平面**（避免透视畸变导致换算误差）
- 鱼苗拍摄时应**短暂静止**或在透明计数槽中（移动模糊会让吻端/尾鳍末端定位失准）
- 多鱼苗缸场景按摄像头 ID 绑定到注册鱼苗缸 ID
- **部署时必须录入**：鱼种、孵化日期（用于换算日龄）、参照物类型 + 已知尺寸（mm）
- 用户必须授权部署；公共养殖场 / 实验室需公示告知

## 关键观测信号

### 参照物校准信号（核心）
- `reference_type` - 参照物类型（ruler / coin / calibration_board）
- `reference_known_length_mm` - 参照物已知尺寸（mm）
- `reference_detected_pixel_length` - 参照物检测到的像素长度
- `pixel_per_mm` - 校准比例（px/mm，核心换算系数）
- `reference_detection_confidence` - 参照物检测置信度（0-1）

### 鱼苗测量信号（每条 fry_id 独立）
- `fry_id` - 鱼苗唯一标识（ReID 输出，可选）
- `snout_xy` - 吻端 2D 像素坐标
- `tail_tip_xy` - 尾鳍末端 2D 像素坐标
- `body_length_px` - 吻端到尾鳍末端像素长度
- `body_length_mm` - **实际体长（mm，= body_length_px / pixel_per_mm）**
- `body_length_measurement_confidence` - 测量置信度（0-1，吻端/尾鳍末端定位质量）
- `posture_is_straight` - 鱼体姿态是否伸直（弯曲会导致体长低估）

### 群体统计
- `measured_fry_count` - 本次成功测量鱼苗数
- `body_length_mean_mm` - 平均体长
- `body_length_std_mm` - 体长标准差
- `body_length_cv_percent` - 变异系数（CV%，反映群体均匀度）
- `body_length_p10` / `body_length_p50` / `body_length_p90` - 体长 10/50/90 分位数

### 生长速率（结合历史数据）
- `last_measurement_date` - 上次测量日期
- `days_since_last_measurement` - 距上次测量天数
- `growth_rate_mm_per_day` - 平均日增长（mm/day）
- `growth_curve_points` - 生长曲线数据点列表（[{date, mean_mm}, ...]）

## 综合判定

- `growth_normal` - 生长正常（速率在鱼种基线区间内）
- `growth_fast` - 生长偏快（>基线 1.2 倍，可能投喂过量需关注水质）
- `growth_slow` - 生长偏慢（<基线 0.7 倍，疑似饲料质量/水质/温度问题）
- `growth_stagnant` - **生长停滞**（连续 ≥ 2 次测量速率 < 基线 0.3 倍）
- `growth_uneven_population` - 群体大小不均（CV% > 30%，需考虑分级饲养）
- `growth_measurement_unreliable` - 测量不可靠（参照物未检出 / 检测置信度 < 0.8 / 多数鱼姿态弯曲 / 视野遮挡）

## 4 级提醒策略递进（侧重养殖管理建议，非健康告警）

- Level 1（growth_normal / growth_fast）：仅入库 + 用户 APP 进度更新"本次平均体长 X mm，日增长 Y mm/day，生长正常"
- Level 2（growth_slow / growth_uneven_population）：重要提示，建议**检查投喂量与频次 / 检查水温与水质 / 评估饲料品牌或粒径是否匹配鱼苗口径 / 考虑分级饲养均匀群体**
- Level 3（growth_stagnant，单次）：紧急提示，建议**立即检查水质（溶氧/pH/氨氮/亚硝酸盐）+ 检查体表与游姿 + 检查投喂记录**，并联系**当地水产养殖技术员或观赏鱼繁育专家**
- Level 4（growth_stagnant 连续 ≥ 2 周 / 同缸多组鱼苗同时停滞）：最高紧急提示 + 推送所有管理人员 + 强烈建议**全面排查（饲料 + 水质 + 病害 + 密度 + 光照周期）+ 专业人员介入**

## 单日提醒上限

- Level 1 不限（建议默认每天/每周 1 次测量） / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限

## 红线约束

- **禁止**做"营养不良 / 肠炎 / 寄生虫 / 应激综合征 / 遗传缺陷"等具体疾病诊断
- **禁止**输出具体药物名称、剂量、给药方案
- **禁止**输出具体饲料品牌名称推荐（仅可指出"建议更换粒径"等中性建议）
- **禁止**长期存储完整鱼苗缸视频/图像（≤ 30 天，留生长曲线 + 关键测量帧；公共养殖场/实验室按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 喂食器 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
- 体长、生长速率、CV% 等指标必须基于真实图像测量；**禁止伪造或夸大指标**
- 鱼种特异性：不同鱼种生长基线差异极大（斑马鱼 0.3-0.5mm/d / 罗非鱼 0.8-1.5mm/d / 锦鲤幼苗 0.5-1.0mm/d / 神仙鱼 0.3-0.6mm/d）→ 必须按**鱼种 + 日龄 + 水温**联合判定基线；**禁止使用通用阈值盲判**
- 必须考虑透视畸变上下文：参照物与鱼苗不在同一水平面 / 摄像头不垂直俯拍 → 必须返回 `growth_measurement_unreliable` 并提示调整拍摄
- 参照物未检出 / 置信度 < 0.8 / 鱼苗姿态弯曲多数 / 视野遮挡严重 → 必须返回 `growth_measurement_unreliable`，**禁止给出不可靠的生长停滞告警**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼苗缸 ID
- `species` - 鱼种
- `fry_age_days` - 鱼苗日龄
- `reference_calibration` - 参照物校准信息（type / known_mm / pixel_per_mm / confidence）
- `population_statistics` - 群体统计（mean / std / CV% / p10 / p50 / p90）
- `growth_rate_mm_per_day` - 平均日增长
- `growth_curve_image_url` - 生长曲线图 URL
- `composite_scene` - 综合判定
- `alert_level` - 提醒等级
- `recommended_actions` - 建议动作（调整投喂 / 分级饲养 / 检查水质 / 联系技术员，**不含药物与品牌**）
- `disclaimer` - 免责声明
