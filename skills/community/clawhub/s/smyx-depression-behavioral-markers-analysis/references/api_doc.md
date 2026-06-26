# API 接口文档

此处用于存放抑郁症辅助行为标记（长时间不动、食欲改变） API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动抑郁症辅助行为标记分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取卧床时长 + 进食行为统计 + 行为变化报告
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史行为变化记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_DEPRESSION_BEHAVIORAL_MARKERS_ANALYSIS` - 抑郁症辅助行为标记（长时间不动、食欲改变）

## 输入约束

- 摄像头：**必须覆盖卧室区域（含床位）和餐厅区域（含餐桌）双视角**；可由两个摄像头分别覆盖
- 视频时长：**单次分析必须 ≥ 24 小时连续记录**（建议 24-72 小时滑动窗口），否则无法可靠统计每日总量
- 帧率 ≥ 1 FPS 即可（长时序统计无需高帧率）；分辨率 ≥ 480p；夜间需配合红外或低照度增强
- ROI 标定：床位 ROI（bed_region）+ 餐桌 ROI（dining_region）
- 必须有 **7-14 天历史基线数据**（个人均值与标准差），否则首次只输出"基线累积中"状态
- 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式

## 关键观测信号

### 卧床指标
- `lying_in_bed_duration_daily_min` - 当日卧床总时长（分钟）
- `out_of_bed_event_count_daily` - 当日离床事件次数
- `room_movement_minutes_daily` - 卧室外活动总时长（参考指标）

### 进食指标
- `eating_action_count_daily` - 当日进食动作次数（手部抓握餐具送入口中）
- `eating_total_duration_min_daily` - 当日进食总时长
- `meal_event_count_daily` - 当日完整餐次数（每餐 ≥ 1 分钟连续进食视为 1 餐）
- `food_remained_ratio_estimate` - 餐后剩余食物比例估计（参考指标）

### 基线对比
- `baseline_window_days` - 基线窗口（默认 7-14 天）
- `lying_delta_vs_baseline_min` - 当日卧床时长相对基线均值的偏差
- `eating_action_ratio_vs_baseline` - 当日进食动作次数相对基线的比例（0-1+）
- `consecutive_abnormal_days` - 连续异常天数

## 阈值与异常判定

- **卧床异常**：`lying_in_bed_duration_daily_min > 1200` (20 小时) 或相对基线 +6 小时及以上
- **进食异常**：`eating_action_ratio_vs_baseline < 0.5`（动作次数低于基线 50%）或 `meal_event_count_daily < 1`（24 小时内无完整餐次）
- **触发提醒**：上述异常**连续 ≥ 3 天**（默认）即输出"行为变化报告"
- **基线累积期**：前 7 天仅记录不报警

## 输出字段（参考）

- `subject_detected` / `baseline_ready`
- `daily_lying` / `daily_eating` - 当日两类指标
- `baseline_comparison` - 与基线对比
- `consecutive_abnormal_days`
- `abnormal_pattern` - 行为异常模式（hypersomnia_immobility / appetite_loss / both / none）
- `risk_signal_level` - 风险信号等级（none / mild_signal / notable_signal / strong_signal）
- `alert_type` - 提醒类型（behavioral_change_3day / behavioral_change_7day / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `alert_message` - 推送给家属/社区医生的友好文本（如"妈妈最近 3 天每天卧床 ≥ 21 小时、进食动作较平时少了 60%，建议尽快电话关心或安排居家探视"）
- `recommend_action` - 建议动作（push_family_notice / suggest_visit / suggest_consult_doctor / observe_only）
- `helpline_reference` - 当 strong_signal 时附**北京心理危机研究与干预中心 010-82951332 / 全国心理援助热线 400-161-9995**等参考资源

## 强制约束与红线

- ❌ **禁止**输出抑郁症诊断、抑郁量表评分（如 GDS-15、PHQ-9）、用药建议或处方
- ❌ **禁止**长期存储原始视频；仅保存匿名化的指标统计与时间戳
- ❌ **禁止**将"行为变化"等同于"确诊抑郁症"
- ✅ 出现 strong_signal 时附**心理援助热线**与就近社区精神卫生服务参考
- ✅ 建议由家属 / 社区医生 / 精神科医生联合解读，并配合患者本人自愿性谈话

> 仅输出基于视觉的客观行为统计与友好提醒，**不构成抑郁症诊断、量表评分或治疗方案**；任何抑郁症确诊与治疗必须由精神科医生评估制定；若老人出现明显自伤/自杀言语或行为，请立即联系心理援助热线或当地急救机构。
