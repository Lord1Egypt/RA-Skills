# API 接口文档

此处用于存放守宫/蜥蜴尾巴断尾识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动守宫/蜥蜴断尾识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（尾长 / 缩短比例 / 断端伤口 / 结痂状态）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史断尾事件记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出断尾事件报告

## 场景代码

- `SMYX_REPTILE_TAIL_LOSS_DETECTION_ANALYSIS` - 守宫/蜥蜴尾巴断尾识别

## 输入约束

- 摄像头：爬宠箱固定摄像头 / 智能爬宠箱内置摄像头 / 手持高清相机
- 分辨率 ≥ 1080p（**像素测量精度要求高于其他爬宠技能**）；帧率 ≥ 5 FPS（静态测量为主，高帧率非必需）
- 拍摄角度：**侧位平拍**或**俯拍**，必须**完整展示从泄殖腔孔到尾尖的整条尾部**
- 光照：充足且均匀（避免阴影遮挡尾尖判断）
- **核心采样窗口**：每日 ≥ 1 张参考图像（建议早晚各 1 张），对比历史 7 天基线
- 多箱/多只场景按摄像头 ID + 个体 ID 双重绑定
- **部署时必须录入**：宠物物种、个体 ID（多只混养时唯一标识）、首次入缸基线照片、首次入缸 SVL（吻肛长，单位 mm）、是否已有历史断尾记录（已断尾个体新长尾巴 = 再生尾，形态颜色不同）

## 关键观测信号

### 尾长测量
- `tail_length_pixels` - 当前尾部像素长度（从泄殖腔到尾尖）
- `tail_length_mm_estimated` - 估算尾部实际长度（mm，需 SVL 参考或缸内已知尺寸物校准）
- `tail_to_svl_ratio` - **尾长/SVL 比值**（核心指标，物种基线差异大：豹纹守宫 ≈ 0.9-1.1，鬃狮蜥 ≈ 1.2-1.5，绿鬣蜥 ≈ 2.0-2.5）
- `tail_length_history_baseline` - 历史 7 天尾长基线
- `tail_shortening_ratio` - **尾长缩短比例**（核心指标，阈值 ≥ 20% 触发断尾事件）

### 断端形态
- `tail_tip_morphology` - 尾尖形态（intact_tapered_normal / blunt_amputated / scabbed / open_wound / regenerated_bulb）
- `wound_visible` - **断端是否可见开放伤口**（核心指标）
- `scab_present` - 是否结痂（结痂为后期，伤口为新鲜断尾）
- `redness_swelling_score_0_5` - 断端红肿评分（0-5，≥ 3 提示感染风险）
- `discharge_or_pus_detected` - 是否有渗液/脓液（感染强信号）

### 再生尾识别
- `is_regenerated_tail` - **是否为再生尾**（再生尾颜色与原尾不同，无原始鳞片纹路，球状钝端）
- `regenerated_tail_color_anomaly` - 再生尾颜色异常评分

### 上下文与排除信号
- `is_during_shedding_cycle` - 是否处于蜕皮期（蜕皮期尾尖可能呈白色脱皮态，易误判）
- `multi_individual_cohabitation` - 是否多只混养（争斗断尾高发场景）
- `recent_handling_stress` - 近期是否有人为操作（应激断尾）
- `previous_autotomy_recorded` - 历史断尾记录已存在
- `image_quality_acceptable` - 图像质量是否合格（清晰度 / 完整露出 / 无遮挡）

## 综合判定

- `tail_intact_normal` - 尾部完整正常
- `tail_shedding_artifact` - 蜕皮造成的尾尖白皮假象，非断尾
- `tail_regenerated_baseline` - 再生尾已存在基线，无新增断尾事件
- `tail_loss_event_fresh` - **新发断尾事件**（缩短 ≥ 20% + 断端可见伤口或新鲜创面）
- `tail_loss_event_with_infection_risk` - **断尾 + 感染风险**（伤口红肿 ≥ 3 / 有渗液脓液）
- `tail_loss_event_scabbed` - 断尾已结痂（事件已发生数日，进入恢复期）
- `tail_signal_unreliable` - 信号不可靠（图像模糊 / 尾尖未完整露出 / 光照不足 / 无 SVL 参考）

## 4 级提醒策略递进

- Level 1（tail_intact_normal / tail_regenerated_baseline / tail_shedding_artifact）：仅入库，不主动提示
- Level 2（tail_loss_event_scabbed）：温和提示，记录断尾已结痂进入恢复期，建议**继续保持环境清洁 + 评估是否需隔离**
- Level 3（tail_loss_event_fresh）：重要提示，建议**立即隔离受伤个体到单独养殖箱 + 用洁净水或宠物专用生理盐水冲洗伤口 + 保持环境湿度与温度稳定 + 减少应激源 + 观察食欲与精神状态**
- Level 4（tail_loss_event_with_infection_risk）：紧急提示，建议**立即隔离 + 保持伤口清洁 + 立即联系爬宠兽医（断尾感染可能引发败血症致死）**

## 单日提醒上限

- Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 不设上限（断尾感染急症）

## 红线约束

- **🚨 禁止**做"败血症 / 骨髓炎 / 蜂窝织炎 / 坏死性皮炎"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、给药方案、**消毒液品牌、抗生素品牌、外用药膏品牌**（仅可提"宠物专用生理盐水冲洗"等中性表述）
- **🚨 绝对禁止**输出"撒云南白药""涂红霉素软膏""用碘伏""口服阿莫西林"等具体处方剂量
- **🚨 绝对禁止**输出"自行缝合伤口""自行剪除坏死组织"等任何外科操作（必须由兽医现场判断）
- **禁止**长期存储完整爬宠箱视频/图像（≤ 30 天，留尾长时间序列 + 断尾事件关键图像；繁殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热灯 / UVB / 灯光参数；任何设备控制变更必须由用户确认（仅可建议隔离）
- 尾长测量、缩短比例、伤口评分等指标必须基于真实图像分析；**禁止伪造或夸大指标**
- 物种特异性：**豹纹守宫 / 肥尾守宫 / 蓝舌石龙子 / 部分石龙子 / 部分壁虎**具自割能力（autotomy），可主动断尾后再生；**鬃狮蜥 / 大多数 monitor / 鳄鱼**不能再生尾；**绿鬣蜥幼体**可再生但成体困难 → **必须按物种识别再生能力**；**严禁通用阈值盲判已断尾物种的再生尾基线为新发断尾**
- 必须考虑生理性上下文：**蜕皮期尾尖白皮假象 / 多只混养争斗高发 / 近期人为操作应激 / 已有历史断尾再生基线** → 不可直接告警
- 图像模糊 / 尾尖未完整露出 / 光照不足 / 无 SVL 参考 / 分辨率 < 1080p → 必须返回 `tail_signal_unreliable` 并建议重新拍摄
- 必须告知用户：AI 视觉识别仅供参考，**伤口处理与感染判断需用户结合现场观察并由专业爬宠兽医确认**

## 输出报告字段

- `report_date` - 报告日期
- `enclosure_id` - 爬宠箱 ID
- `individual_id` - 个体 ID（多只混养必填）
- `species` - 宠物物种
- `tail_length_mm_estimated` - 当前尾长估算
- `tail_to_svl_ratio` - 尾长/SVL 比值
- `tail_shortening_ratio` - 尾长缩短比例
- `tail_tip_morphology` - 尾尖形态
- `wound_visible` - 断端伤口
- `redness_swelling_score_0_5` - 红肿评分
- `is_regenerated_tail` - 是否再生尾
- `composite_scene` - 综合判定
- `alert_level` - 提醒等级
- `recommended_actions` - 建议动作（隔离 / 宠物专用生理盐水冲洗 / 保持环境清洁 / 观察食欲精神 / 联系爬宠兽医，**不含具体药物品牌、剂量、外科操作**）
- `disclaimer` - 免责声明
