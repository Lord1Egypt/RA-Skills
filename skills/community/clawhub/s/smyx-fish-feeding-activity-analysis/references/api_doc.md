# API 接口文档

此处用于存放鱼类摄食行为活跃度分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼类摄食行为活跃度分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取摄食活跃度结果（0-100 评分 + 食欲下降提示 + 剩余饲料评估）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史摄食活跃度报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出摄食活跃度报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 智能喂食器自动调整下次投喂量）

## 场景代码

- `SMYX_FISH_FEEDING_ACTIVITY_ANALYSIS` - 鱼类摄食行为活跃度分析

## 输入约束

- 摄像头：智能喂食器内置摄像头 / 鱼缸固定摄像头 / 养殖池上方摄像头，能完整覆盖投喂区域
- 分辨率 ≥ 720p；**帧率 ≥ 15 FPS**（鱼群抢食动作快，建议 ≥ 20 FPS）
- 光照：建议鱼缸/养殖池照明开启 + 无强反光；水质清澈
- **核心采样窗口**：**投喂后 1 分钟内**（关键约束），可选续采至 3 分钟用于剩余饲料评估
- 投喂触发：智能喂食器投喂动作触发 / 用户手动标记 / 视频自动检测饲料抛入水面
- 多鱼缸/池场景按摄像头 ID 绑定到注册容器 ID（每个容器独立鱼种 + 鱼群数量基线）
- 用户必须授权部署；公共水族馆/养殖场需公示告知

## 关键观测信号

### 鱼群聚集信号
- `fish_gathering_count` - 投喂区域内聚集鱼数（去重 ReID 跟踪）
- `total_fish_count_baseline` - 该容器注册总鱼数（基线，用户配置）
- `gathering_ratio` - 聚集比例 = gathering / baseline
- `gathering_response_latency_sec` - 从投喂到第一条鱼到达投喂区的响应时长（秒）

### 摄食强度信号
- `avg_swim_speed_pixel_per_sec` - 平均游动速度（像素/秒，校准后可换算体长/秒）
- `feeding_action_freq_per_min` - 摄食动作频率（次/分钟，张嘴啄食 / 转身咬颗粒）
- `attack_intensity_score` - 抢食激烈度评分（0-100，反映群体活力）
- `surface_feeding_event_count` - 水面摄食事件次数（浮性饲料）
- `mid_bottom_feeding_event_count` - 中层/底层摄食事件次数（沉性饲料）

### 剩余饲料信号
- `floating_pellet_count_after_60s` - 投喂 60 秒后水面残留颗粒数
- `sinking_pellet_count_after_180s` - 投喂 180 秒后缸底/池底残留颗粒数
- `residual_feed_ratio` - 剩余饲料比例（估算，0-1）

### 综合评分
- `feeding_activity_score` - 摄食活跃度评分（0-100，加权融合上述指标）

## 综合判定

- `feeding_excellent` - 摄食优秀（评分 ≥ 85）
- `feeding_normal` - 摄食正常（评分 70-85）
- `feeding_slightly_low` - 摄食略低（评分 60-70）
- `feeding_appetite_decline` - **食欲下降**（评分 40-60）
- `feeding_severe_appetite_loss` - 严重食欲不振（评分 20-40）
- `feeding_total_refusal` - 完全拒食（评分 < 20，聚集 < 10% 且无摄食动作）
- `feeding_signal_unreliable` - 信号不可靠（视频不在投喂窗口 / 投喂未发生 / 浑浊度过高）

## 4 级告警策略递进

- Level 1（slightly_low）：仅入库或用户 APP 轻提醒"摄食略低，请观察"
- Level 2（appetite_decline）：用户 APP 重要告警，建议**检查水温、溶氧、pH、氨氮、近期是否新增鱼/换水/换饲料**
- Level 3（severe_appetite_loss）：紧急告警，建议**隔离观察精神萎靡个体 + 检查体表症状 + 暂停下一次投喂**，并提示联系**当地观赏鱼兽医**
- Level 4（total_refusal / 连续 ≥ 3 餐 ≥ Level 2 / 同缸多条鱼同时拒食）：最高紧急告警 + 强烈建议**立即全面检查（水质 + 体表 + 游姿 + 呼吸）+ 联系专业人员**

## 单日告警上限

- Level 1 不限 / Level 2 × 4（按投喂次数）/ Level 3 × 2 / Level 4 不设上限

## 红线约束

- **禁止**做"肠炎 / 寄生虫 / 鳃病 / 细菌感染"等具体疾病诊断
- **禁止**输出具体药物名称、剂量、给药方案
- **禁止**长期存储完整鱼缸/养殖池视频（≤ 7 天，仅入库异常摄食事件片段；公共养殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停智能喂食器 / 投药 / 换水 / 加热 / 灯光；任何水族设备控制变更必须由用户确认（仅可建议或在用户明确授权的下次投喂量自动调整范围内执行）
- 评分、聚集比例、剩余饲料量等指标必须基于真实视频帧统计；**禁止伪造或夸大指标**
- 鱼种特异性：不同鱼种摄食习性差异极大（金鱼 / 锦鲤水面摄食、鼠鱼/异型底层摄食、神仙鱼立体抢食、夜行鱼日间不进食）→ 必须按**鱼种基线**判定；**禁止使用通用阈值盲判**
- 必须考虑"生理性低食欲"上下文：水温骤变、繁殖期、灯光开启/关闭过渡期、饲料品牌切换 → 评分降低属可解释，避免直接归因于疾病
- 视频不在投喂窗口、未检测到投喂动作、水浑浊度过高时，必须返回 `feeding_signal_unreliable`，**禁止给出不可靠的食欲下降告警**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸/养殖池 ID
- `species` - 鱼种
- `feeding_time` - 投喂时间戳
- `feeding_amount_g` - 本次投喂量（克，可选）
- `feeding_activity_score` - 0-100 摄食活跃度评分
- `gathering_ratio` / `attack_intensity_score` / `residual_feed_ratio` - 关键子指标
- `composite_scene` - 综合判定
- `alert_level` - 告警等级
- `recommended_actions` - 建议动作（观察 / 检查水质 / 暂停下次投喂 / 联系兽医，**不含药物**）
- `next_feeding_suggestion` - 下次投喂量建议（基于剩余饲料比例，仅建议）
- `disclaimer` - 免责声明
