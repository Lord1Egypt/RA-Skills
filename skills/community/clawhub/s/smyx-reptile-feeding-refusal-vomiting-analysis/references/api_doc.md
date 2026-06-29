# API 接口文档

此处用于存放爬宠进食拒绝/呕吐识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动爬宠拒食/呕吐识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（攻击事件 / 吞食事件 / 反吐事件 / 拒食判定）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史拒食/呕吐事件记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出事件报告

## 场景代码

- `SMYX_REPTILE_FEEDING_REFUSAL_VOMITING_ANALYSIS` - 爬宠进食拒绝/呕吐识别

## 输入约束

- 摄像头：爬宠箱固定摄像头，**必须正对喂食区域**，无遮挡
- 分辨率 ≥ 720p；帧率 ≥ 20 FPS（攻击/吞食/反吐动作快，需较高帧率）
- 光照：喂食时段保持充足光照（避免漆黑环境无法识别）
- **核心采样窗口**：投喂瞬间为 t0 → 拒食判定窗口默认 t0+30 分钟 → 呕吐判定窗口默认 t0+2 小时（吞食后）
- 多箱场景按摄像头 ID 绑定到注册容器 ID
- **部署时必须录入**：宠物物种、猎物类型（乳鼠/成鼠/蟋蟀/面包虫/蔬果等）、猎物数量、投喂时间戳

## 关键观测信号

### 攻击行为
- `prey_present_in_view` - 猎物是否出现在视野中
- `attack_event_count` - 攻击次数（蛇：咬击+缠绕；蜥蜴/龟：扑咬）
- `attack_latency_seconds` - 从投喂到首次攻击的延迟（秒）
- `attack_confidence` - 攻击行为置信度

### 吞食行为
- `swallow_event_count` - **成功吞食次数**（核心指标）
- `swallow_completion_time_seconds` - 单次完整吞食时长
- `swallow_confidence` - 吞食置信度

### 反吐/呕吐行为（吞食后）
- `vomit_event_detected` - **是否检测到反吐事件**（核心指标）
- `vomit_latency_minutes_after_swallow` - 吞食后多少分钟反吐（< 120 分钟为短时呕吐）
- `vomit_appearance` - 反吐物外观（whole_prey / partial / liquid_only / mucus）
- `vomit_confidence` - 反吐置信度

### 拒食判定
- `refusal_judged` - **是否判定为拒食**（窗口内 attack_event_count = 0 且 swallow_event_count = 0）
- `ignore_duration_seconds` - 无视猎物总时长
- `avoidance_behavior_detected` - 是否检测到主动逃避（远离猎物移动）

### 上下文与排除信号
- `is_during_shedding_cycle` - 是否处于蜕皮期（蜕皮期拒食属正常）
- `is_during_brimation` - 是否处于冬化/冬眠期（冬化拒食属正常）
- `is_post_meal_within_72h` - 距上次成功喂食 < 72 小时（大型蛇类一次喂食后多日不再进食属正常）
- `is_breeding_season` - 是否繁殖期（雄性繁殖期可能拒食属正常）
- `is_gravid_or_pre_lay` - 是否抱卵/产前（产前拒食属正常）
- `enclosure_temperature_appropriate` - 环境温度是否在适宜范围（温度过低代谢下降可能拒食）
- `is_newly_introduced` - 是否新入缸适应期（应激拒食属正常）

## 综合判定

- `feeding_normal_attack_swallow` - 攻击+成功吞食，行为正常
- `feeding_normal_delayed_attack` - 攻击有延迟但成功吞食，可能轻度应激
- `refusal_in_physiological_context` - 拒食但属生理性正常上下文（蜕皮/冬化/72h 内喂过/繁殖/产前/新入缸）
- `refusal_abnormal` - **异常拒食**（无生理性上下文 + 30 分钟内无攻击无吞食）
- `vomiting_event` - **呕吐事件**（吞食后 2 小时内反吐）
- `vomiting_with_environmental_cause` - 呕吐 + 环境温度异常（疑似温度不适致代谢异常）
- `feeding_signal_unreliable` - 信号不可靠（视野遮挡 / 光照不足 / 跟踪率 < 80% / 投喂时间未录入）

## 4 级提醒策略递进

- Level 1（feeding_normal_attack_swallow）：仅入库 + 用户 APP 积极反馈"成功捕食并吞食"
- Level 2（feeding_normal_delayed_attack / refusal_in_physiological_context）：温和提示，记录生理性拒食属正常上下文，无需干预
- Level 3（refusal_abnormal）：重要提示，建议**检查环境温度/湿度/UVB/躲避区设置 + 检查猎物状态（活鼠是否健康/昆虫是否过冷）+ 评估猎物大小是否合适 + 7 天后再次尝试投喂；若连续 ≥ 2 次拒食则建议联系爬宠兽医**
- Level 4（vomiting_event / vomiting_with_environmental_cause）：紧急提示，建议**立即停止后续投喂 24-72 小时 + 检查环境温度（特别是消化温度梯度）+ 观察精神状态、排泄、体表 + 联系爬宠兽医（呕吐可能是肠道堵塞、寄生虫、传染病信号）**

## 单日提醒上限

- Level 1 不限 / Level 2 × 4 / Level 3 × 3 / Level 4 × 5（呕吐事件每次必报）

## 红线约束

- **🚨 禁止**做"隐孢子虫病 / 库道虫病 / OPMV / 蛇类传染性脑膜炎 / 肠道堵塞 / 代谢性骨病"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、给药方案、灌肠剂、催吐剂、止吐药
- **🚨 绝对禁止**输出"强制开口喂食""灌食""饥饿疗法多少天"等具体操作剂量（必须由兽医现场判断）
- **禁止**长期存储完整爬宠箱视频（≤ 14 天，仅入库喂食事件 + 异常事件片段；养殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户投喂 / 启停加热灯 / UVB / 加热垫 / 灯光参数；任何设备控制变更必须由用户确认（仅可建议）
- 攻击次数、吞食次数、反吐时间等指标必须基于真实视频帧分析；**禁止伪造或夸大指标**
- 物种特异性：**大型蛇类**（球蟒 / 红尾蚺 / 王蛇等）一次喂食可数日至两周不进食属正常；**冬化期物种**（部分龟类、玉米蛇）整季拒食属正常；**蜕皮期**所有爬宠均可能拒食；**繁殖期**雄性可能拒食 → **严禁通用阈值盲判生理性拒食为异常**
- 必须考虑生理性上下文：**蜕皮 / 冬化 / 距上次进食 < 72h / 繁殖期 / 抱卵期 / 新入缸应激 / 环境温度异常** → 不可直接告警
- 视野遮挡 / 光照不足 / 跟踪率 < 80% / 投喂时间未录入 → 必须返回 `feeding_signal_unreliable`
- 必须告知用户：AI 行为分析仅供参考，**呕吐/拒食根因诊断需结合现场观察并由专业爬宠兽医确认**

## 输出报告字段

- `report_date` - 报告日期
- `enclosure_id` - 爬宠箱 ID
- `species` - 宠物物种
- `prey_type` - 猎物类型
- `prey_count` - 猎物数量
- `feed_time` - 投喂时间戳
- `attack_event_count` - 攻击次数
- `swallow_event_count` - 吞食次数
- `vomit_event_detected` - 是否反吐
- `vomit_latency_minutes_after_swallow` - 吞食后反吐延迟（分钟）
- `refusal_judged` - 是否判定拒食
- `composite_scene` - 综合判定
- `alert_level` - 提醒等级
- `recommended_actions` - 建议动作（检查温度湿度 UVB / 检查猎物状态 / 评估猎物大小 / 停止后续投喂 / 观察精神排泄体表 / 联系爬宠兽医，**不含药物/剂量/灌食操作**）
- `disclaimer` - 免责声明
