# API 接口文档

此处用于存放蛙类皮肤湿润度评估 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动蛙类皮肤湿润度评估任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（光泽度 / 皱褶 / 白膜 / 脱水等级）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史皮肤湿润度记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出脱水风险评估报告

## 场景代码

- `SMYX_FROG_SKIN_MOISTURE_ASSESSMENT_ANALYSIS` - 蛙类皮肤湿润度评估

## 输入约束

- 摄像头：雨林缸 / 蛙类饲养箱 / 两栖养殖场 / 宠物医院诊查摄像头
- 分辨率 ≥ 1080p（皮肤光泽度量化与皱褶细节需高清）；帧率 ≥ 10 FPS（静态拍照为主）
- 拍摄角度：**俯拍背部**或**侧拍侧身**（必须完整露出大块皮肤区域）
- 光照：**5000-6500K 中性白光源**，均匀光照（**严禁强点光源直射造成眩光误判为光泽**）
- **核心采样窗口**：每日定时拍照 1-3 次，建议**早晚各一次**（早晨喷雾前 + 夜间活动期）
- **必须排除水中浸泡帧**（蛙类全身浸水时光泽来自水膜而非皮肤分泌物）
- 多缸场景按摄像头 ID + 个体 ID 双重绑定
- **部署时必须录入**：物种（树蛇/角蛙/箭毒蛙/红眼蛙/番茄蛙/钟角蛙/猫眼珍珠蛙等）、品系颜色基线、缸内湿度、温度、上次喷雾时间、健康基线照片

## 关键观测信号

### 光泽度量化
- `skin_specular_reflection_score_0_100` - **皮肤镜面反射光泽度评分 0-100**（核心指标，HSV-V 亮度 + 反射高光占比联合计算）
- `glossiness_compared_to_baseline` - 与健康基线对比（百分比变化，**下降 > 30% 触发脱水预警**）
- `glossiness_compared_to_species_norm` - 与物种健康基线对比（物种差异大：箭毒蛇皮肤亮泽 vs 角蛙皮肤稍哑光）
- `light_source_temperature_estimated` - 估算光源色温（用于校准）
- `eyeshine_excluded` - 是否已排除眼睛反光区域（眼睛反光极强会污染光泽度评分）

### 皱褶与失水形态
- `skin_wrinkle_score_0_5` - **皮肤皱褶评分 0-5**（核心指标，≥ 2 提示中度脱水，≥ 4 提示重度脱水）
- `wrinkle_area_ratio` - 皱褶面积占可见皮肤比例
- `skin_tenting_visible` - 皮肤帐篷征是否可见（轻捏后恢复慢，重度脱水征兆，但本技能不主动捏，仅识别自发皱起）
- `body_emaciation_score_0_5` - 体型消瘦评分（脱水严重者皮包骨）

### 白膜与异常分泌
- `white_film_detected` - **是否检测到白膜**（核心指标，皮肤表面白色雾状膜，重度脱水或代谢应激征兆）
- `white_film_area_ratio` - 白膜面积占比
- `skin_color_dulling` - 皮肤颜色暗淡度（正常品系颜色 vs 暗淡）
- `skin_color_anomaly_patches` - 皮肤色块异常（不属于品系花纹的暗斑）

### 蜕皮上下文与排除信号
- `is_during_natural_shedding` - **是否处于自然蜕皮中**（蛙类自食蜕皮，蜕皮中白膜属正常生理过程，必须排除）
- `is_immersed_in_water` - 是否浸水中（光泽来自水膜非分泌物，需返回 unreliable 或上下文标注）
- `is_recently_misted` - 是否刚喷雾 < 15 分钟（水珠附着光泽虚高）
- `is_estivating_or_burrowing` - 是否处于蛰伏/钻土状态（角蛙蛰伏期皮肤会形成保护性蜕膜）
- `humidity_environment` - 缸内湿度（< 70% 大多树栖物种警戒线）
- `temperature_environment` - 缸内温度
- `image_quality_acceptable` - 图像质量是否合格

## 综合判定

- `skin_hydrated_excellent` - 皮肤湿润优良（光泽度 ≥ 80，无皱褶，无白膜）
- `skin_hydrated_good` - 皮肤湿润良好（光泽度 60-79，无皱褶，无白膜）
- `skin_hydrated_acceptable` - 皮肤湿润尚可（光泽度 45-59，轻微皱褶 ≤ 1，无白膜）
- `dehydration_risk_mild` - **轻度脱水风险**（光泽度 30-44 OR 较基线下降 30-50% OR 皱褶评分 2-3）
- `dehydration_risk_severe` - **重度脱水风险**（光泽度 < 30 OR 较基线下降 > 50% OR 皱褶 ≥ 4 OR 检测到白膜 OR 体型消瘦 ≥ 4）
- `skin_context_natural_shedding` - 自然蜕皮中，白膜属正常上下文
- `skin_context_post_misting` - 刚喷雾后水珠虚高，需稍后复测
- `skin_signal_unreliable` - 信号不可靠（浸水中 / 强眩光 / 钻土 / 图像模糊 / 光照不均 / 分辨率 < 1080p）

## 4 级提醒策略递进

- Level 1（hydrated_excellent / good）：仅入库
- Level 2（hydrated_acceptable / context_post_misting / context_natural_shedding）：温和提示，建议**正常关注 + 蜕皮中保持环境稳定**
- Level 3（dehydration_risk_mild）：紧急提示，建议**立即增加喷雾频率（具体值由用户根据物种适宜湿度手册设定） + 检查湿度计是否在物种推荐范围 + 提供浅水盆 / 湿润躲避屋 + 观察食欲精神 + 12-24 小时内复测**
- Level 4（dehydration_risk_severe）：最高紧急提示 + 强烈建议**立即提供浅水盆让蛙浸泡补水 + 增加喷雾至湿度推荐高线 + 立即联系两栖动物兽医（脱水可短期导致肾衰竭/电解质紊乱致死）**

## 单日提醒上限

- Level 1 不限 / Level 2 × 3 / Level 3 × 5 / **Level 4 不设上限（脱水急症·肾衰竭风险）**

## 红线约束

- **🚨 禁止**做"肾衰竭 / 急性脱水休克 / 电解质紊乱 / Chytrid 真菌病 / Saprolegnia 水霉病 / 红腿病"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、抗真菌药品牌、补液品牌、电解质溶液品牌、口服/外用剂量
- **🚨 绝对禁止**输出"用 Holtfreter 氏液浸泡 X 分钟""涂硝酸银""用 0.6% 盐水浴""口服恩诺沙星 5mg/kg""使用米尔伯霉素"等具体处方
- **🚨 绝对禁止**输出"自行注射皮下补液""自行切开水肿放液""自行剥离白膜"等任何外科或医疗操作（必须由两栖动物兽医现场判断）
- **🚨 严禁推荐自来水直接浸泡**（自来水含氯/氯胺会损伤蛙类皮肤），仅可中性提示"使用爬两栖宠物专用脱氯/曝气除氯水"
- **禁止**长期存储完整雨林缸视频/图像（≤ 14 天，留每日皮肤抓拍 + 脱水关键事件；养殖场/医院按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停喷雾系统 / 加热垫 / UVB / 灯光参数；任何环境控制变更必须由用户确认（仅可建议）
- 所有指标必须基于真实图像分析；**禁止伪造或夸大光泽度评分、皱褶评分、白膜面积**
- 物种特异性：**树栖物种**（红眼蛙/树蛙）适宜湿度 70-90% / **陆栖物种**（角蛙/番茄蛙）适宜湿度 60-80% / **水栖物种**（爪蟾）几乎全水浸泡 / **箭毒蛙**对干燥极度敏感 → 必须按物种适宜湿度判定；**严禁通用阈值**
- 必须考虑生理性上下文：**自然蜕皮中白膜属正常 / 浸水中光泽虚高 / 刚喷雾后水珠虚高 / 角蛙蛰伏期保护性蜕膜** → 必须排除
- **严禁误判蜕皮中的白膜为脱水重度白膜**
- 浸水中 / 强眩光 / 钻土 / 图像模糊 / 光照不均 / 分辨率 < 1080p → 必须返回 `skin_signal_unreliable`
- 必须告知用户：AI 视觉评估仅供参考，**重度脱水恢复与并发症需立即联系专业两栖动物兽医**

## 输出报告字段

- `report_date`、`enclosure_id`、`individual_id`、`species`、`skin_specular_reflection_score_0_100`、`glossiness_compared_to_baseline`、`skin_wrinkle_score_0_5`、`white_film_detected`、`white_film_area_ratio`、`skin_color_dulling`、`humidity_environment`、`is_during_natural_shedding`、`composite_scene`、`alert_level`、`recommended_actions`（增加喷雾频率 / 检查湿度计 / 提供浅水盆 / 湿润躲避屋 / 联系两栖动物兽医，**不含具体药物/剂量/精确湿度温度数值/具体浸泡液配方**），`disclaimer`
