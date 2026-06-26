# API 接口文档

此处用于存放儿童分离焦虑识别（上学前哭闹）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童分离焦虑识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取哭闹表情/抓拽/抗拒行为统计 + 焦虑等级结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史分离焦虑事件
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_SEPARATION_ANXIETY_DETECTION_ANALYSIS` - 儿童分离焦虑识别（上学前哭闹）

## 输入约束

- 摄像头：家庭入户门口 / 幼儿园门口 / 晨间接待区固定摄像头，覆盖儿童与家长互动区域，**能看到儿童面部表情 + 双手 + 下肢**
- 帧率 ≥ 10 FPS（推荐 15-30 FPS，捕捉短促哭闹与抓拽动作）；分辨率 ≥ 480p；光照稳定
- 多儿童同时送学场景下需按区域跟踪，避免目标串扰
- 隐私敏感场景可启用人体轮廓 + 面部马赛克模式

## 关键观测信号

- `subject_detected` - 是否检测到儿童
- `parent_present` - 是否有家长在场（用于判断"分离"上下文）
- `crying_face_score` - 哭闹面部表情评分（皱眉 + 张嘴哭泣 + 流泪综合）
- `grab_event_count` - 肢体抓拽事件次数（抓家长衣服/抱腿/拉扯门框）
- `resistance_event_count` - 抗拒行为次数（后退、躺地、推开）
- `event_duration_sec` - 当次送别场景持续时长
- `peak_crying_intensity` - 哭闹强度峰值（0-1）
- `successful_separation` - 最终是否完成分离（家长离开后儿童是否平复）

## 阈值与分离焦虑等级

- `mild`（轻度）- 短暂皱眉/低声啜泣，无明显抓拽或抗拒，能在 1 分钟内完成分离
- `moderate`（中度）- 持续哭泣 + ≥ 1 次抓拽/抗拒，2-5 分钟内完成分离
- `severe`（重度）- 大声哭泣 + 多次抓拽/抗拒（≥ 3 次）+ 躺地等强烈抗拒 + 分离 ≥ 5 分钟仍未平复，或连续多日处于该状态

## 输出字段（参考）

- `subject_detected` / `parent_present` / `successful_separation`
- `behavior_metrics` - 当次行为统计（crying_face_score / grab_event_count / resistance_event_count / event_duration_sec / peak_crying_intensity）
- `consecutive_moderate_severe_days` - 连续中/重度天数（用于趋势预警）
- `separation_anxiety_level` - 分离焦虑等级（mild / moderate / severe）
- `alert_type` - 提醒类型（separation_anxiety_moderate / separation_anxiety_severe / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `alert_message` - 推送给家长/老师的友好文本（如"宝宝今早分离时哭泣约 4 分钟、抱腿 3 次，焦虑等级中度，建议家长今晚多陪伴或与老师沟通入园适应方案"）
- `recommend_action` - 建议动作（push_parent_notice / notify_teacher / suggest_gradual_separation / suggest_transition_object / observe_only）
- `tip_for_parent` - 家长安抚建议（如"明天提前 10 分钟到园，给孩子带一个安抚玩偶"）

> 仅输出基于视觉的客观行为统计与友好提醒，**不提供分离焦虑障碍（Separation Anxiety Disorder）等心理诊断或处方**；若儿童哭闹影响入园 ≥ 3-4 周或伴随躯体化症状（呕吐、入睡困难等）请咨询儿童心理医生。
