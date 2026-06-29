# API 接口文档

此处用于存放孵化箱内龟蛋/蛇蛋发育监测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动龟蛋/蛇蛋孵化监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（受精状态/发育阶段/蛋壳颜色/血管网络/胚胎黑影）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史孵化监测记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出孵化进度报告

## 场景代码

- `SMYX_EGG_INCUBATION_MONITORING_ANALYSIS` - 孵化箱内龟蛋/蛇蛋发育监测

## 输入约束

- 摄像头：孵化箱内固定**微距摄像头** OR **高分辨率摄像头 + 微距镜头**
- 分辨率 ≥ 1080p（**血管网络/血丝细节需高清**）；建议含已知尺寸参考物（毫米刻度）
- 拍摄角度：
  - **侧向透光照蛋**（关键照蛋技术 candling，从蛋下方/侧方用 LED 冷光源透射）OR
  - **微距俯拍蛋壳表面**（用于颜色/纹理/灰斑识别）
- 光照：**冷 LED 光源（< 300 lumen，<35°C）**，照蛋时间 < 10 秒（**严禁热光源长时间照射，胚胎对热敏感**）
- 不可移动蛋，**严禁翻转**（龟蛋/蛇蛋孵化中翻转 90° 以上会导致胚胎死亡）
- **核心采样窗口**：每日 1 次 OR 每两日 1 次（孵化周期长 45-120 天，无需频繁）
- 多蛋窝场景按摄像头 ID + 蛋编号双重绑定（每枚蛋必须独立编号）
- **部署时必须录入**：物种（陆龟/水龟/玉米蛇/球蟒/王蛇等）、产卵日期（用于计算孵化天数）、孵化温度方案、孵化湿度方案、蛋窝总数

## 关键观测信号

### 蛋壳形态
- `egg_shell_color_classification` - **蛋壳颜色分类**（核心指标：white_normal / pale_yellow_normal / **chalking_white_fertile_sign**（粉白受精征兆，蛋壳钙化）/ gray_spots_warning / **yellowed_discolored_warning** / mold_growth_severe）
- `egg_shell_calcification_zone_visible` - **钙化白带是否可见**（核心指标，受精后 7-14 天蛋壳中部出现的粉白色带，受精标志）
- `egg_shape_aspect_ratio` - 蛋形长宽比
- `egg_surface_texture` - 表面纹理（smooth_normal / sweating_water_droplets_warning / cracked / mold_visible）
- `mold_area_ratio` - 霉变面积占比（**> 5% 高警戒**）

### 血管与血丝
- `vascular_network_detected` - **血管网络是否可见**（核心指标，受精中早期 14-30 天，红色细线状网络）
- `vascular_network_complexity_score_0_10` - 血管网络复杂度评分（**< 3 早期 / 4-7 中期 / > 7 成熟**）
- `blood_ring_detected` - **血环是否检测到**（**死胎警告信号！血管退化形成红环**）
- `blood_streaks_visible` - 血丝可见度（首次发现血丝表示受精成功）
- `blood_color_classification` - 血色分类（bright_red_fresh / dark_red_aging / brown_dead_embryo）

### 胚胎与孵化进度
- `embryo_shadow_detected` - **胚胎黑影是否可见**（核心指标，后期 30 天+，照蛋时可见暗色团块）
- `embryo_shadow_size_relative` - 胚胎黑影相对蛋大小比例（早期 < 30% / 中期 30-60% / 即将孵化 > 70%）
- `embryo_movement_detected` - **胚胎运动是否检测到**（即将孵化前 7 天可见胚胎在蛋内活动）
- `embryo_position_normal` - 胚胎位置是否正常（**应靠上半部分**，朝下提示异常）
- `air_cell_position_normal` - 气室位置是否正常（蛋钝端，气室异常提示死胎）
- `incubation_days_estimated` - 估算孵化天数（基于产卵日期 + 当前日期）

### 上下文与排除信号
- `species_normal_incubation_days_range` - 物种正常孵化天数范围（陆龟 60-120 / 水龟 45-90 / 玉米蛇 55-65 / 球蟒 55-70）
- `temperature_stable_within_range` - 温度是否稳定在物种推荐范围
- `humidity_stable_within_range` - 湿度是否稳定在物种推荐范围
- `is_recently_flipped_or_moved` - 是否近期被翻转/移动（**翻转后必须警告蛋已损坏**）
- `candling_light_safe` - 照蛋光源是否安全（冷 LED < 300 lumen）
- `image_quality_acceptable` - 图像质量是否合格

## 综合判定

- `egg_unfertilized_yolker` - **未受精蛋**（候蛋黄蛋/无精蛋，超过 14 天仍无钙化白带、无血管，蛋液均匀黄色透光）
- `egg_fertile_early_stage` - **受精早期**（产卵后 7-21 天，钙化白带出现 + 血管网络初现）
- `egg_fertile_vascular_stage` - **血管发育期**（21-45 天，血管网络丰富，complexity_score 4-7）
- `egg_fertile_embryo_stage` - **胚胎成形期**（45 天-孵化前 7 天，胚胎黑影 30-70% + 气室扩大）
- `egg_pre_hatching` - **即将孵化**（孵化前 7 天，胚胎运动可见 + 胚胎黑影 > 70%）
- `egg_dead_embryo_blood_ring` - **死胎警告**（血环检测 / 胚胎运动消失 / 黑影颜色变暗均匀 / 蛋黄沉积底部）
- `egg_mold_contamination` - **霉变蛋**（霉变面积 > 5%，**必须立即移出隔离防止传染**）
- `egg_signal_unreliable` - 信号不可靠（照蛋角度差 / 蛋表凝水 / 蛋被堆叠遮挡 / 光源不当 / 分辨率 < 1080p）

## 4 级提醒策略递进

- Level 1（egg_fertile_*_stage / egg_pre_hatching）：仅入库 + 进度可视化（按蛋编号生成孵化时间线）
- Level 2（egg_unfertilized_yolker 持续 > 物种判定窗口）：温和提示，建议**继续观察至 21 天再做判定 + 检查温湿度是否在物种推荐范围 + 可考虑后期剔除（避免霉变影响其他蛋）**
- Level 3（egg_mold_contamination / 表面凝水/裂纹）：紧急提示，建议**立即将该蛋移至单独观察盒隔离 + 检查孵化箱整体湿度（凝水提示湿度过高） + 检查通风 + 观察其他蛋是否扩散**
- Level 4（egg_dead_embryo_blood_ring）：最高紧急提示 + 强烈建议**立即移出死胎避免发酵爆炸污染窝内其他蛋 + 检查温度是否曾过高/过低 + 评估孵化方案是否需要调整 + 联系爬宠繁殖兽医复盘原因**

## 单日提醒上限

- Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5

## 红线约束

- **🚨 严禁**伪造或夸大"已受精/血管发育/即将孵化"等关键阶段判定；**误判会让繁殖者错过最佳处理时机**
- **🚨 绝对禁止**输出"自行打开蛋壳查看""自行剥离胚胎""自行注射药物到蛋内""自行湿润蛋壳"等任何**侵入式操作**指令
- **🚨 严禁推荐具体温度/湿度数字**（如"调到 30.5℃""湿度调到 85%"）；仅可建议"按物种孵化手册推荐范围调整"
- **🚨 严禁推荐性别选择性温度操控**（TSD 温度性别决定虽然客观存在，但 AI 不应主动指导，避免性别比例失衡导致繁殖伦理问题）
- **🚨 严禁热光源照蛋**（白炽灯/卤素灯会快速升温杀死胚胎）；必须使用冷 LED < 300 lumen + 照射 < 10 秒
- **🚨 严禁建议翻蛋**（龟蛋/蛇蛋孵化中翻转 90° 以上会导致胚胎死亡，与鸟蛋孵化不同）
- **禁止**长期存储完整孵化箱视频（≤ 14 天，留每枚蛋每次照蛋关键帧 + 孵化时间线；繁殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户调整孵化箱温湿度；任何环境控制变更必须由用户确认（仅可建议）
- 必须考虑物种孵化周期差异：**陆龟 60-120 天 / 水龟 45-90 天 / 玉米蛇 55-65 天 / 球蟒 55-70 天 / 王蛇 60-75 天** → 严禁通用判定窗口
- 必须告知用户：AI 孵化监测仅供参考，**重要繁殖决策需结合温湿度日志和物种孵化手册综合判断**

## 输出报告字段

- `report_date`、`incubator_id`、`egg_id`、`species`、`egg_lay_date`、`incubation_days_estimated`、`egg_shell_color_classification`、`egg_shell_calcification_zone_visible`、`vascular_network_detected`、`vascular_network_complexity_score_0_10`、`blood_ring_detected`、`embryo_shadow_detected`、`embryo_shadow_size_relative`、`embryo_movement_detected`、`composite_scene`（受精状态+发育阶段）、`alert_level`、`recommended_actions`（继续观察 / 检查温湿度 / 隔离移出 / 联系爬宠繁殖兽医，**不含具体温度湿度数字、不含侵入式操作**），`disclaimer`
