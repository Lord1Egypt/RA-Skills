# API 接口文档

此处用于存放蛇类口腔腐肉识别（口炎）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动蛇类口炎识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（黏膜颜色 / 脓点 / 溃疡 / 腐肉 / 风险等级）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史口炎评估记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出口炎评估报告

## 场景代码

- `SMYX_SNAKE_STOMATITIS_DETECTION_ANALYSIS` - 蛇类口腔腐肉识别（口炎）

## 输入约束

- 摄像头：蛇箱固定摄像头 / 智能蛇箱内置摄像头 / 爬宠医院诊查摄像头 / 手持高清相机
- 分辨率 ≥ 1080p（**口腔黏膜颜色渐变、脓点、微小溃疡均需高清**）；帧率 ≥ 25 FPS（张口瞬间短暂，需高帧率抓拍）
- 拍摄角度：**正对蛇头部口腔**（侧面或斜角无法完整观察口腔内壁），必须在蛇**张口瞬间**抓拍（打哈欠 / 进食后 / 口腔检查时）
- 光照：充足且均匀（**口腔内部较暗，需补光或环形灯**；避免反光过强误判为脓点）
- **核心采样窗口**：蛇张口时自动抓拍单帧或多帧（需 ≥ 3 帧清晰口腔图像取最佳帧）
- **必须排除进食中帧**（吞食猎物时口腔被猎物遮挡，非口腔检查窗口）
- 多箱场景按摄像头 ID + 个体 ID 双重绑定
- **部署时必须录入**：物种（球蟒 / 玉米蛇 / 王蛇 / 红尾蚺 / 缅蟒 / 眼镜蛇 / 响尾蛇等）、上次脱皮日期、上次喂食日期、环境温度、湿度

## 关键观测信号

### 口腔黏膜颜色
- `mucosa_color_classification` - **黏膜颜色分类**（核心指标：healthy_pink_normal / mild_erythema_red / severe_erythema_dark_red / pale_anemic / cyanotic_bluish）
- `mucosa_redness_score_0_10` - **黏膜红肿评分 0-10**（核心指标，≤ 2 正常 / 3-5 轻度 / 6-8 中度 / ≥ 9 重度）
- `mucosa_color_patchy` - 是否斑块状红肿（非均匀，局部炎症特征）
- `mucosa_pale_areas` - 是否有苍白区域（贫血或坏死前兆）

### 脓点与分泌物
- `pus_points_detected` - **是否检测到脓点**（核心指标，白色或黄色点状隆起）
- `pus_point_count` - 脓点数量
- `pus_point_location` - 脓点位置（anterior_gum / posterior_gum / palate / inner_lip / throat_entrance）
- `caseous_plaques_detected` - **是否检测到干酪样斑块**（核心指标，灰白/黄色膜状物，口炎典型征兆）
- `mucus_or_foam_detected` - 口腔是否有异常黏液或泡沫（非进食时）
- `discharge_color` - 分泌物颜色（clear / white_purulent / yellow_purulent / blood_tinged）

### 溃疡与腐肉
- `ulcer_detected` - **是否检测到溃疡**（核心指标，黏膜表面不规则凹陷）
- `ulcer_count` - 溃疡数量
- `ulcer_depth_assessment` - 溃疡深度评估（superficial / moderate / deep_to_underlying_tissue）
- `necrotic_tissue_detected` - **是否检测到腐肉/坏死组织**（核心指标，暗色/黑褐色不规则组织，口炎晚期征兆）
- `necrotic_tissue_area_estimated` - 坏死组织面积估算（占口腔可视面积百分比）
- `gum_recession_or_hemorrhage` - 牙龈退缩或出血

### 上下文与排除信号
- `mouth_opening_trigger` - 张口触发原因（yawn_normal / post_feeding / threat_display / examination / unknown）
- `is_during_shedding_cycle` - 是否处于蜕皮期（蜕皮期口腔黏膜可能轻微异常）
- `is_post_feeding_within_24h` - 是否进食后 24h 内（进食后可能短暂口腔充血）
- `is_during_breeding_season` - 是否繁殖期（雄性争斗可致口腔外伤）
- `ambient_temperature_appropriate` - 温度是否适宜（低温应激是口炎主因之一）
- `humidity_appropriate` - 湿度是否适宜（过低湿度损伤黏膜）
- `image_quality_acceptable` - 图像质量是否合格（清晰度 / 口腔完整露出 / 光照充足 / 无唾液反光干扰）

## 综合判定

- `oral_cavity_healthy` - 口腔健康（黏膜粉红正常，无脓点/溃疡/腐肉）
- `stomatitis_risk_low` - **口炎风险低**（黏膜轻度红肿 ≤ 5 分，无脓点/溃疡/腐肉，可能为蜕皮或进食后短暂充血）
- `stomatitis_risk_moderate` - **口炎风险中**（黏膜红肿 6-8 分 OR 少量脓点 1-3 个 OR 浅表溃疡 OR 干酪样斑块初现）
- `stomatitis_risk_high` - **口炎风险高**（黏膜暗红/苍白/发绀 + 多量脓点 ≥ 4 个 + 深溃疡 + 腐肉/坏死组织 + 牙龈出血）
- `oral_injury_non_infectious` - 非感染性口腔外伤（繁殖期争斗/猎物刮伤，局部创伤而非弥漫性炎症）
- `oral_context_shedding_artifact` - 蜕皮期口腔黏膜轻微假象
- `oral_signal_unreliable` - 信号不可靠（口腔未完整露出 / 图像模糊 / 光照不足 / 唾液反光干扰 / 分辨率 < 1080p / 进食中帧未排除）

## 4 级提醒策略递进

- Level 1（oral_cavity_healthy / oral_context_shedding_artifact）：仅入库
- Level 2（stomatitis_risk_low / oral_injury_non_infectious）：温和提示，建议**加强观察 3-5 天 + 检查环境温湿度是否在物种适宜范围 + 确认饲养箱清洁度**
- Level 3（stomatitis_risk_moderate）：紧急提示，建议**检查并调整温湿度至物种适宜范围 + 保持饲养箱清洁干燥 + 隔离至单独观察箱 + 观察食欲精神 + 尽快联系爬宠兽医（口炎中期可快速恶化为败血症）**
- Level 4（stomatitis_risk_high）：最高紧急提示，建议**立即隔离 + 保持环境温湿度稳定 + 立即联系爬宠兽医（腐肉/坏死组织 + 深溃疡提示口炎已进入急症阶段，败血症风险极高，可短期致死）**

## 单日提醒上限

- Level 1 不限 / Level 2 × 3 / Level 3 × 5 / **Level 4 不设上限（口炎急症·败血症风险）**

## 红线约束

- **🚨 禁止**做"传染性口炎 / 偏肺衣原体感染 / OPMV / 包含体病 IBD / 细菌性败血症 / 真菌性口炎"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、抗生素品牌、抗真菌药品牌、口腔消毒液品牌、肌注/口服剂量
- **🚨 绝对禁止**输出"用聚维酮碘稀释液冲洗""涂抹制霉菌素""肌注恩诺沙星 5mg/kg""口服甲硝唑""涂云南白药"等具体处方
- **🚨 绝对禁止**输出"自行刮除腐肉""自行清创""自行拔除松动牙齿"等任何外科操作（必须由兽医现场判断）
- **禁止**长期存储完整蛇箱视频/图像（≤ 14 天，留张口抓拍关键帧 + 口炎进展对比图像；繁殖场/医院按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热灯 / UVB / 湿度控制；任何环境控制变更必须由用户确认（仅可建议）
- 所有指标必须基于真实图像分析；**禁止伪造或夸大黏膜红肿评分、脓点数量、溃疡深度等**
- 物种特异性：**毒蛇**口腔结构与无毒蛇不同（毒牙/毒腺开口），**蟒蚺**口腔较大易于观察 → 必须按物种口腔解剖基线判定
- 必须考虑生理性上下文：**蜕皮期口腔黏膜可能轻微异常 / 进食后短暂充血 / 繁殖期争斗外伤 / 低温应激** → 不可直接告警
- 口腔未完整露出 / 图像模糊 / 光照不足 / 唾液反光干扰 / 进食中帧 / 分辨率 < 1080p → 必须返回 `oral_signal_unreliable`
- 必须告知用户：AI 视觉识别仅供参考，**口炎确诊与治疗需立即联系专业爬宠兽医（建议口腔拭子培养 + 血液检查 + X 光排除呼吸道蔓延）**

## 输出报告字段

- `report_date`、`enclosure_id`、`individual_id`、`species`、`mucosa_color_classification`、`mucosa_redness_score_0_10`、`pus_points_detected`、`pus_point_count`、`caseous_plaques_detected`、`ulcer_detected`、`ulcer_depth_assessment`、`necrotic_tissue_detected`、`necrotic_tissue_area_estimated`、`gum_recession_or_hemorrhage`、`composite_scene`、`alert_level`、`recommended_actions`（检查温湿度 / 隔离观察 / 保持清洁 / 联系爬宠兽医，**不含具体药物品牌、剂量、外科操作**）、`disclaimer`
