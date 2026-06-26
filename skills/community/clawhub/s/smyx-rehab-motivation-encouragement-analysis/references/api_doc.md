# API 接口文档

此处用于存放康复患者沮丧/放弃倾向激励 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动康复患者沮丧/放弃倾向检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取沮丧事件 + 激励动作清单
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史激励记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出康复激励日志报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动激励动作（智能音箱鼓励语 / 屏幕进步对比 / 康复师 APP 推送）
6. （可选）`/web/rehab/v2/get-historical-progress` - 获取患者历史训练完成度（用于进步对比和长期无进展判定）

## 场景代码

- `SMYX_REHAB_MOTIVATION_ENCOURAGEMENT_ANALYSIS` - 康复患者沮丧/放弃倾向激励

## 输入约束

- 摄像头：康复中心训练区 / 作业治疗室 / 家庭康复区固定摄像头，能完整看到患者上半身和训练动作
- 帧率 ≥ 15 FPS；分辨率 ≥ 720p；优先正面或 45° 侧前方
- 音频可选：采样率 ≥ 16kHz（用于叹气声 / 言语沉默 / 自言自语检测）
- 时段：仅在患者训练时段内启用（默认按训练计划，可配置）
- 多患者场景按目标跟踪 + 人脸识别绑定到注册患者 ID（每位患者独立基线 + 训练计划）
- 患者本人必须授权部署，康复机构需公示告知；居家场景需家属或患者本人同意
- 训练前需录入：训练项目清单、每项预设次数/时长/关节活动度基线、康复阶段（早期/中期/后期）

## 关键观测信号

### 视频（核心）
- `sigh_event_count` - 叹气事件次数（胸腹快速隆起-收缩伴呼气节律）
- `training_interrupt_event` - 中断训练事件（未达预设次数/时长前主动停止）
- `head_down_silent_sec` - 低头不语持续时间（头部低垂 + 无言语交流）
- `eye_contact_avoidance_score` - 眼神接触回避评分（0-100）
- `joint_rom_shrink_ratio` - 关节活动范围相对训练初期的收缩比例（如 0.6 表示当前 ROM 仅为基线 60%）
- `movement_perfunctory_score` - 动作敷衍评分（0-100，速度慢 + 幅度小 + 节律乱）
- `facial_frustration_score` - 面部沮丧评分（0-100，皱眉 + 嘴角下拉 + 目光呆滞）

### 音频（可选）
- `sigh_audio_event_count` - 叹气声音事件
- `negative_self_talk_count` - 消极自言自语次数（"我做不到 / 没用 / 不练了"等）
- `silent_duration_min` - 训练期间累计沉默时长

### 进展信号（基于历史数据）
- `today_vs_yesterday_delta` - 今日 vs 昨日完成度差值（按训练项目）
- `recent_3day_trend` - 近 3 日训练完成度趋势（rising / flat / falling）
- `no_progress_days` - 连续无进展天数

## 场景判定

- `rehab_motivation_none` - 训练状态良好
- `rehab_motivation_mild` - 轻度沮丧（偶发叹气 + 短暂低头）
- `rehab_motivation_sigh_cluster` - 短时间内多次叹气
- `rehab_motivation_interrupt` - 提前中断训练
- `rehab_motivation_perfunctory` - 动作迟缓敷衍 + ROM 显著缩小
- `rehab_motivation_no_progress` - 连续 ≥ 3 日同一项目停滞或下降
- `rehab_motivation_strong` - 显著放弃倾向（多项叠加）

## 4 级激励策略递进

- Level 1（mild）：智能音箱低音量播放温和鼓励语（"您今天的状态不错，再来一组试试"）
- Level 2（sigh_cluster / interrupt）：在 Level 1 基础上，屏幕/语音展示与昨日（或最近一次）的具体进步对比（"您今天比昨天多做 2 次抬腿"）
- Level 3（perfunctory / no_progress）：在 Level 2 基础上向康复师 APP 推送提醒"患者出现放弃倾向，请关注或介入指导"
- Level 4（strong / 持续不缓解 / 出现强烈负向自语）：紧急推送康复师 + 家属，并建议暂停当前训练项目、切换轻松项目或休息

## 单训练日动作上限

- mild × 6 / moderate × 4 / strong × 2 / Level 4 不设上限

## 红线约束

- 禁止做"康复无效 / 抑郁症 / 适应障碍"等医学诊断
- 禁止长期存储患者隐私视频（≤ 7 天，仅入库沮丧事件片段；机构按伦理审查 ≤ 72 小时）
- 禁止用于商业广告 / AI 训练；禁第三方共享
- 禁止激励音量 > 50 dB
- 严禁使用 AI 克隆 / 合成家属或康复师声音；必须使用本人提前授权的预录音或标准 TTS
- 禁止使用"加油坚持就是胜利 / 别人都能你怎么不行 / 你这样不行"等压力型或对比型激励语
- 激励语必须个性化、具体、肯定（基于真实进步数据），优先采用 SMART 反馈
- 禁止越权代康复师调整训练强度 / 项目；任何强度变更必须由康复师确认
- 进步对比数据必须基于真实历史记录，**禁止伪造或夸大进步数值**
