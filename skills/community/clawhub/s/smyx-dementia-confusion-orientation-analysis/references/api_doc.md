# API 接口文档

此处用于存放失智老人困惑/迷惘识别与定向安抚 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动失智老人困惑/迷惘检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取困惑事件 + 定向安抚动作清单
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史定向安抚记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出定向安抚日志报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动安抚（智能音箱播放家庭成员介绍 / 时间地点提示 / 照护者 APP 推送）

## 场景代码

- `SMYX_DEMENTIA_CONFUSION_ORIENTATION_ANALYSIS` - 失智老人困惑/迷惘识别与定向安抚

## 输入约束

- 摄像头：失智照护机构（认知症单元 / 公共活动区 / 走廊）或居家失智老人常驻活动区域固定摄像头
- 帧率 ≥ 10 FPS；分辨率 ≥ 720p；优先正面或 30° 内侧脸（便于眼神/头部姿态识别）
- 音频可选：采样率 ≥ 16kHz（用于"这里是哪 / 你是谁 / 现在几点"等定向问题语音识别 + 声纹绑定）
- 时段：默认全天 06:00 - 22:00 启用，夜间睡眠时段切换为低敏告警模式
- 多老人场景按目标跟踪 + 人脸识别 / 声纹绑定到注册老人 ID（每位老人独立基线）
- 家属或机构必须授权部署，机构场景需公示告知，家属同意书归档

## 关键观测信号

### 视频（核心）
- `sudden_activity_stop_sec` - 突然停止活动持续时间（动作中断 ≥ 5s）
- `gaze_drifting_score` - 眼神游离评分（0-100，视线无聚焦 / 漫无目的漂移）
- `head_scanning_event_count` - 四处张望次数（头部扫描周围环境）
- `facial_confusion_score` - 面部困惑评分（0-100，眉头紧锁 + 嘴唇微张 + 目光呆滞）
- `wandering_event_detected` - 游荡事件（无目的来回走动）
- `agitation_visual_detected` - 激越视觉信号（搓手 / 拉扯衣物 / 反复站起坐下）

### 音频（可选）
- `orientation_question_count` - 定向问题计数（"这是哪 / 你是谁 / 现在几点 / 我在哪 / 几点了"等）
- `orientation_question_repeat_count` - 5 分钟内重复同一问题次数
- `voice_anxiety_score` - 语音焦虑评分（0-100，颤抖 / 急促 / 提高音量）
- `calling_family_event_count` - 呼喊家人姓名次数（"老伴 / 儿子 / 女儿"等）

## 场景判定

- `dementia_orientation_none` - 状态平稳
- `dementia_orientation_mild` - 轻度迷惘（短暂停顿 + 偶发张望）
- `dementia_orientation_question` - 反复定向问题（5 分钟内同类问题 ≥ 2 次）
- `dementia_orientation_gaze_drift` - 眼神游离 + 活动中断
- `dementia_orientation_wandering` - 困惑伴游荡
- `dementia_orientation_agitation` - 困惑伴激越（焦虑动作 + 高音）
- `dementia_orientation_strong` - 显著困惑（多项叠加）

## 4 级定向安抚策略递进

- Level 1（mild）：智能音箱低音量播放当前时间地点温和提示（"今天是 2026 年 5 月 19 日，星期四，您在客厅"）
- Level 2（question / gaze_drift）：在 Level 1 基础上播放家庭成员介绍录音（"您儿子叫李明，他中午会来看您"）+ 柔和环境光辅助
- Level 3（wandering / agitation）：在 Level 2 基础上向主照护者 APP 推送提醒"老人出现困惑/游荡，请协助"，提示就近工作人员
- Level 4（strong / 持续不缓解 / 走出安全区）：紧急推送主照护者 + 机构值班护士，并触发本地温和提示音引导老人原地等待

## 单日动作上限

- mild × 12 / moderate × 8 / strong × 4 / Level 4 不设上限

## 红线约束

- 禁止做"阿尔茨海默病 / 血管性痴呆 / 路易体痴呆"等医学诊断
- 禁止长期存储老人隐私音视频（≤ 7 天，仅入库困惑事件片段；机构按伦理审查规范缩短至 ≤ 72 小时）
- 禁止用于商业广告 / AI 训练；禁第三方共享
- 禁止冷白光（≥ 4000K）或亮度 > 30 lux 的环境灯（避免黄昏综合征加重）
- 禁止安抚音量 > 55 dB（老人听力衰退需略高，但不可造成惊吓）
- 严禁使用 AI 克隆 / 合成家庭成员声音冒充本人录音；必须使用家属本人提前授权的预录音
- 禁止使用"您不是说过/您忘了吗/又问一遍了"等否定 / 矫正语；定向安抚语必须温和、当下、具体
- 机构场景必须公示告知，提供家属退出机制
