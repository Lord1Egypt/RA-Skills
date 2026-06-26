# API 接口文档

此处用于存放员工情绪波动 HR 报告 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权（**仅向 HR 管理层角色开放**）
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动员工情绪波动监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取匿名 ID 级情绪基线对比 + 波动预警
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史 HR 关怀报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出 HR 内部完整报告

## 场景代码

- `SMYX_EMPLOYEE_EMOTION_FLUCTUATION_HR_ANALYSIS` - 员工情绪波动 HR 报告

## 输入约束

- 摄像头：企业开放式办公区 / 部门独立办公室固定摄像头，能看到工位上半身（含面部）
- 帧率 ≥ 5 FPS（推荐 10 FPS）；分辨率 ≥ 720p；光照稳定避免逆光
- 视频时长：日常工作时段连续采样（建议每个被分析人每日 ≥ 4 小时累计在画面中）
- 必须有**个人 30 天历史基线**，否则首次仅输出"基线累积中"状态
- 多人开放式办公需启用基于匿名 ID 的目标跟踪，不做姓名/工号绑定
- 工位 ROI 标定：每个工位作为一个匿名工位 ID（如 W-A12 / W-B07）

## 强制匿名约束（核心红线）

- ❌ **禁止**进行人脸识别 / 人脸比对到 HR 系统姓名/工号库
- ❌ **禁止**将"匿名 ID ↔ 实际员工"的映射表落地存储或对外暴露
- ✅ 仅维护**临时跟踪 ID**（仅用于会话内同一人跨帧追踪），跟踪 ID 周期性轮换（建议 ≤ 7 天）
- ✅ 所有预警结果输出**匿名 ID + 工位坐标**，不输出员工姓名或人脸图像
- ✅ HR 收到预警后由**直属管理者本人**根据工位坐标自行判断是谁，再以**自愿性、保密**方式发起关怀沟通

## 关键观测信号

### 面部表情
- `smile_count_per_day` - 每日笑容次数
- `smile_total_duration_sec` - 笑容总时长
- `frown_count_per_day` - 每日皱眉次数
- `sigh_visual_event_count` - 视觉叹气动作次数（耸肩 + 呼气长姿态）
- `neutral_ratio` - 中性面部比例

### 行为
- `solo_sit_total_minutes` - 独自静坐总时长
- `peer_interaction_event_count` - 与他人互动事件次数（同事接近、转身交谈）
- `desk_leave_event_count` - 离开工位次数（参考指标）
- `working_posture_hunch_ratio` - 工位姿态前倾/含胸比例（参考指标）

### 基线对比
- `baseline_window_days` - 基线窗口（默认 30 天）
- `smile_delta_pct` - 笑容频率相对基线变化（如 -45%）
- `sigh_delta_pct` - 叹气次数相对基线变化（如 +60%）
- `solo_sit_delta_pct` - 独自静坐相对基线变化
- `peer_interaction_delta_pct` - 社交互动相对基线变化
- `consecutive_abnormal_days` - 连续异常天数

## 阈值与等级（默认值，可由 HR 配置覆盖）

- `smile_delta_pct ≤ -40%` 或 `sigh_delta_pct ≥ +50%` → 单项异常
- 连续 **3 个工作日**任一组合（笑容降 ≥ 40% 或叹气增 ≥ 50% 或独自静坐增 ≥ 50%）→ 触发波动预警
- 同时出现 ≥ 2 项异常 → 升级为重点关怀
- 最小样本保护：当日累计可分析时长 < 2 小时 → 输出 `insufficient_sample`，不发布预警

## 输出字段（参考）

- `report_period` - 报告周期（weekly / monthly）
- `anonymized_subject_id` - 匿名跟踪 ID（如 ANON-2026W21-073，**仅本周期有效**）
- `workstation_id` - 匿名工位坐标（如 W-A12，**不绑定姓名**）
- `daily_metrics` - 每日 4 项面部 + 4 项行为指标
- `baseline_comparison` - 与个人 30 天基线对比
- `consecutive_abnormal_days`
- `fluctuation_pattern` - 波动模式（smile_drop / sigh_increase / withdrawal / mixed / improving / none）
- `concern_level` - 关怀等级（none / mild / notable / focus_care）
- `alert_type` - 提醒类型（emotion_fluctuation_notice / focus_care_needed / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `hr_care_suggestion` - 给 HR 的关怀建议（如"匿名 ID ANON-2026W21-073（工位 W-A12）近 5 个工作日笑容频率降 42%、独自静坐增 55%，建议其直属上级以工作支持/1-on-1 聊聊近况的方式自愿沟通，**禁止**当面提及监控数据"）
- `recommend_action` - 建议动作（suggest_one_on_one_chat / suggest_workload_review / suggest_eap_referral / observe_only）
- `eap_reference` - 当 focus_care_needed 时附**企业 EAP 服务 / 全国心理援助热线 400-161-9995** 参考

## 强制约束与红线

- ❌ **禁止**输出"焦虑症/抑郁症"等任何精神医学诊断或量表评分
- ❌ **禁止**将员工情绪监测数据用于绩效考核、晋升评估、解雇决策
- ❌ **禁止**长期存储原始视频或人脸特征；建议仅保存匿名 ID 级聚合指标，**保留期 ≤ 30 天**
- ❌ **禁止**未经员工本人同意将其数据共享给直属上级以外的第三方
- ❌ **禁止**在沟通中直接告知员工"你被摄像头分析为情绪低落"，必须以**自然工作支持**的方式进行
- ✅ **必须**事先在企业内部以**显著公告 + 员工代表大会/工会备案**方式公开告知监测范围、用途、保留期与员工反对/退出渠道
- ✅ 必须有**员工退出选项**（opt-out），退出员工的工位永久排除在分析之外
- ✅ 数据访问仅限 **HR 高级管理层（≥ 2 人共同审批）**，所有访问留日志

> 仅输出基于视觉的匿名行为聚合预警，**不构成精神医学诊断，不可作为绩效/晋升/解雇依据**；任何疑似心理健康问题应通过 EAP（员工援助计划）或专业心理咨询渠道，由员工本人自愿参与解决。
