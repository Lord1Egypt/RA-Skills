# API 接口文档

此处用于存放夫妻/家庭争吵强度识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动家庭争吵强度识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取声学/视觉指标 + 冲突强度等级结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史冲突事件
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_FAMILY_CONFLICT_INTENSITY_DETECT_ANALYSIS` - 夫妻/家庭争吵强度识别

## 输入约束

- 摄像头：家庭客厅/起居室固定摄像头，**必须含麦克风**（声学指标为核心），能看到家庭成员上半身
- 帧率 ≥ 10 FPS、分辨率 ≥ 480p；音频采样率 ≥ 16kHz、双声道更佳
- **声学校准**：建议在安装时录制 30 秒室内静音作为环境本底（baseline_db）
- 视频时长建议覆盖完整冲突过程（建议 ≥ 30 秒），过短样本无法稳定判定
- 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式

## 关键观测信号

### 声学
- `peak_db` - 峰值分贝
- `avg_db` - 平均分贝
- `db_delta_vs_baseline` - 与环境本底差值
- `shout_event_count` - 喊叫事件次数（短时高分贝 + 频谱特征）
- `aggressive_word_hit_count` - 攻击性/侮辱性关键词命中数（**仅本地推理，不上传原始语音**）
- `voice_speakers_estimate` - 说话人数估计（≥ 2 才视作"对话冲突"）

### 视觉
- `subject_count` - 画面中人数
- `wave_hand_event_count` - 快速挥手事件
- `finger_point_event_count` - 戳指事件
- `push_event_count` - 推搡事件（**关键升级信号**）
- `throw_object_event_count` - 摔砸物品事件（**关键升级信号**）
- `physical_proximity_invasion` - 是否存在面对面贴脸/逼近行为

## 冲突强度等级（综合声学 + 视觉）

- `low`（低）- 仅声音略升 + 偶尔挥手，无攻击性词汇与肢体接触
- `medium`（中）- 持续高分贝（≥ baseline + 15 dB）+ 多次戳指/挥手 + 攻击性词汇 ≥ 1 次，无推搡/摔物
- `high`（高）- 喊叫 + 推搡 / 摔砸物品 / 持续侮辱性词汇，**或** 出现儿童/老人在场（需立即提醒避免次生伤害）

## 输出字段（参考）

- `event_window` - 当次冲突时间窗
- `acoustic_metrics` - 声学指标
- `visual_metrics` - 视觉指标
- `child_or_elderly_present` - 是否有未成年人或老人在场（强升级触发位）
- `conflict_intensity_level` - 冲突强度等级（low / medium / high）
- `alert_type` - 提醒类型（conflict_low / conflict_medium / conflict_high / repeated_conflict / normal）
- `alert_level` - 提醒级别（info / notice / warning / urgent）
- `gentle_reminder_message` - 推送给当事人手机的**温和**文本（如"检测到中等强度对话冲突，建议双方暂停 10 分钟、各自深呼吸或喝口水后再继续"）
- `recommend_action` - 建议动作（push_gentle_reminder / suggest_cool_down / suggest_separate_rooms / notify_emergency_contact_if_consent / observe_only）
- `suggest_seek_help` - 建议寻求专业帮助的开关（高强度连续多次时为 true）

## 强制约束与红线

- ❌ **禁止**根据本工具结论给当事人贴"家暴施害者/受害者"标签
- ❌ **禁止**自动报警；最多在**事先取得用户同意**的前提下，提醒预设的紧急联系人
- ❌ **禁止**长期存储原始音视频；仅保存匿名化的指标统计与时间戳
- ❌ **禁止**输出法律意见、心理治疗方案或处方
- ✅ 出现 high 等级 + 推搡 / 摔物 / 儿童在场 时，应在友好提醒中附**全国反家庭暴力热线 12338**与就近社区调解资源参考
- ✅ 适合**双方知情同意**后部署；建议作为家庭咨询师辅助工具，由专业人员解读

> 仅输出基于声学和视觉的客观冲突强度指标与温和提醒，**不提供法律意见、心理治疗方案或人身安全判定**；若涉及人身安全或反复高强度冲突，请联系反家庭暴力热线 **12338** 或当地警方与心理援助机构。
