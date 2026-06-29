# API 接口文档

此处用于存放龟类张嘴呼吸（肺炎征兆）识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动龟类肺炎征兆识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（口部开合频率 / 黏液检测 / 鼻腔分泌物 / 呼吸节律）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史肺炎风险预警记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出预警报告

## 场景代码

- `SMYX_TURTLE_PNEUMONIA_SYMPTOM_DETECTION_ANALYSIS` - 龟类张嘴呼吸（肺炎征兆）识别

## 输入约束

- 摄像头：龟缸固定摄像头 / 智能龟缸内置摄像头 / 养殖池水面摄像头 / 宠物医院诊查摄像头
- 分辨率 ≥ 1080p（**口鼻黏液为丝状/反光点细节，需高分辨率**）；帧率 ≥ 25 FPS（开合动作快，需高帧率）
- 拍摄角度：**正对头颈部**或侧前 30°，必须**清晰展示口鼻区域**（头部缩入壳内时无法分析）
- 光照：充足且均匀（避免反光过强误判为黏液 / 避免阴影遮挡口鼻）
- **核心采样窗口**：默认 ≥ 3 分钟连续观察
- **必须排除进食时段**（进食时口部开合属正常）
- 水栖龟需在**完全浮出水面或晒台上**时分析（水下口部开合为换气吐泡）
- 多缸场景按摄像头 ID + 个体 ID 双重绑定
- **部署时必须录入**：物种、龟类型（水栖/半水栖/陆栖）、水温（水栖必填）、气温、UVB 状态、上次投喂时间戳

## 关键观测信号

### 口部开合
- `mouth_opening_events_per_minute` - **每分钟口部开合次数**（核心指标，阈值 > 10 次/分钟触发风险）
- `mouth_opening_duration_ms_avg` - 单次开合平均时长
- `mouth_opening_amplitude_normalized` - 开合幅度归一化
- `mouth_opening_confidence` - 开合检测置信度
- `is_during_feeding_window` - 是否处于进食窗口
- `is_underwater_aquatic` - 水栖龟是否处于水下

### 口鼻黏液与分泌物
- `mucus_detected_in_mouth` - **口腔内是否检测到黏液**（反光点 + 丝状物）
- `mucus_strand_count` - 黏液丝状物数量
- `nasal_discharge_detected` - **鼻腔是否有分泌物**
- `nasal_discharge_color` - 分泌物颜色（clear_transparent / yellow_pus / blood_tinged）
- `bubble_at_nostril` - 鼻孔气泡（肺炎强信号）
- `mucus_nasal_confidence` - 综合置信度

### 呼吸节律与姿态
- `breathing_rate_per_minute` - 呼吸频率
- `neck_extension_persistent` - 头颈持续伸展不缩（呼吸困难强信号）
- `gaping_with_neck_extension` - **张嘴 + 头颈伸展**（典型肺炎姿态）
- `floating_tilted_aquatic` - 水栖龟漂浮倾斜（肺部积液浮力不平衡，肺炎晚期强信号）
- `lethargy_score_0_5` - 嗜睡/活动减少评分

### 上下文与排除信号
- `ambient_temperature_c` - 环境温度
- `water_temperature_appropriate` - 水温是否在物种适宜范围
- `is_post_feeding_within_30min` - 是否刚进食 30 分钟内
- `is_during_basking` - 是否处于晒背中
- `is_during_shedding` - 是否蜕皮期
- `is_breeding_season` - 是否繁殖期

## 综合判定

- `respiration_normal` - 呼吸行为正常
- `respiration_mild_anomaly` - 轻度异常（开合 6-10 次/分钟，无黏液）
- `pneumonia_risk_mild` - **肺炎风险轻度**（开合 > 10 次/分钟 OR 微量黏液）
- `pneumonia_risk_moderate` - **肺炎风险中度**（开合 > 10 次/分钟 + 黏液 + 鼻清涕）
- `pneumonia_risk_severe` - **肺炎风险严重**（张嘴+头颈持续伸展 / 黄脓血染鼻涕 / 鼻孔气泡 / 漂浮倾斜）
- `respiration_within_basking_context` - 晒背上下文正常
- `respiration_signal_unreliable` - 信号不可靠

## 4 级提醒策略递进

- Level 1：仅入库
- Level 2（mild_anomaly）：复测水温/气温 + 加强观察 24-48 小时
- Level 3（mild/moderate）：**立即将水温/气温调至物种推荐高线 + 隔离至温暖干燥养殖箱 + 观察食欲精神 + 立即联系爬宠兽医**
- Level 4（severe）：**立即干养 + 升温保暖 + 立即联系爬宠兽医**（肺炎急症可短期致死）

## 单日提醒上限

- Level 1 不限 / Level 2 × 3 / Level 3 × 5 / **Level 4 不设上限（肺炎急症）**

## 红线约束

- **🚨 禁止**做"细菌性肺炎 / 病毒性肺炎 / 真菌性肺炎 / 呼吸道支原体感染 / RNTV / 上呼吸道感染 URI"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、抗生素品牌、抗真菌药品牌、肌注剂量、口服剂量
- **🚨 绝对禁止**输出"打恩诺沙星 X mg/kg""口服阿莫西林""注射头孢拉定""灌服板蓝根"等具体处方
- **🚨 绝对禁止**输出"具体升温到 N℃ 持续 N 天"等精确温度疗法（仅可"水温/气温调至物种推荐高线"由用户根据物种手册）
- **禁止**长期存储完整龟缸视频（≤ 14 天）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热棒 / UVB / 干养/水养切换
- 所有指标必须基于真实视频帧分析；禁止伪造夸大
- 物种特异性：热带物种适温高、温带物种适温中等、深水龟 vs 浅水龟节律不同 → 按物种基线判定
- 生理性上下文：进食 / 水下换气 / 晒背蒸发 / 消化期短促 → 必须排除
- 头部缩入壳内 / 水栖全程水下 / 图像模糊 / 光照不足 / 进食未排除 / 分辨率 < 1080p → 必须返回 `respiration_signal_unreliable`
- 必须告知用户：AI 视觉仅供参考，**肺炎确诊需 X 光 + 肺部听诊 + 鼻分泌物镜检/培养，由专业爬宠兽医执行**

## 输出报告字段

- `report_date`、`enclosure_id`、`individual_id`、`species`、`turtle_type`、`water_temperature_c`、`ambient_temperature_c`、`mouth_opening_events_per_minute`、`mucus_detected_in_mouth`、`nasal_discharge_detected`、`nasal_discharge_color`、`bubble_at_nostril`、`gaping_with_neck_extension`、`floating_tilted_aquatic`、`composite_scene`、`alert_level`、`recommended_actions`（不含具体药物剂量、抗生素品牌、精确升温温度数值）、`disclaimer`
