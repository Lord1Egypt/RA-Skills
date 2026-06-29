# API 接口文档

此处用于存放爬宠排泄物形态识别（尿酸/粪便）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动爬宠排泄物分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（尿酸 / 粪便 / 肾脏肠道健康提示）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史排泄物评估记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出排泄物健康评估报告

## 场景代码

- `SMYX_REPTILE_EXCREMENT_ANALYSIS_ANALYSIS` - 爬宠排泄物形态识别（尿酸/粪便）

## 输入约束

- 摄像头：爬宠箱 / 饲养缸 / 蜥蜴/守宫/蛇类养殖场固定摄像头
- 分辨率 ≥ 1080p（尿酸结晶纹理与粪便形态需高清）；建议含已知尺寸参考物（硬币/标尺）用于像素-实际尺寸换算
- 拍摄角度：**俯拍**排泄物（需完整露出尿酸+粪便区域，避免遮挡）
- 光照：均匀白色光源（避免色温偏移影响粪便颜色判定）
- **核心采样窗口**：在发现排泄物后、清理前拍摄（**清理后无法回溯**）
- **必须排除背景干扰**：垫材颜色/纹理可能与尿酸/粪便混淆（深色垫材上白色尿酸较易识别，浅色/花纹垫材上可能误判）
- 多缸场景按摄像头 ID + 个体 ID 双重绑定
- **部署时必须录入**：物种（豹纹守宫/睫角守宫/鬃狮蜥/蓝舌石龙子/玉米蛇/球蟒/苏卡达/草龟等）、个体体长（用于尿酸面积归一化）、上次喂食时间/内容、上次排泄时间、当前温度、湿度

## 关键观测信号

### 尿酸检测
- `urate_detected` - **是否检测到尿酸**（核心指标，白色/乳白色区域）
- `urate_color_classification` - 尿酸颜色分类（**white_normal** / cream_yellow / orange_tinged / gritty_granular）
- `urate_pixel_area` - 尿酸像素面积
- `urate_area_normalized_by_body_length` - **尿酸面积归一化值**（核心指标，以个体体长为参考归一化，跨个体可比）
- `urate_area_vs_historical_baseline` - 与历史正常值对比（百分比变化，**增大 > 50% 提示肾脏负担或脱水**）
- `urate_texture` - 尿酸质地（smooth_paste_normal / gritty_granular / hard_chunky）
- `urate_count` - 尿酸团块数量（正常 1 团，多团可能多次排泄或异常）

### 粪便形态
- `feces_detected` - **是否检测到粪便**（核心指标）
- `feces_color_classification` - **粪便颜色分类**（核心指标：brown_normal / green / black_tarry / red_bloody / yellow / white_grey / undigested_insects_visible）
- `feces_consistency` - **粪便形态分类**（核心指标：formed_log_normal / soft_pasty / loose_watery / mucus_coated / bloody_streaked）
- `feces_pixel_area` - 粪便像素面积
- `feces_length_to_width_ratio` - 粪便长宽比（成形条状 > 2 / 稀软 ≈ 1）
- `undigested_content_visible` - 是否可见未消化内容（整只昆虫外骨骼 / 毛发 / 植物纤维）
- `feces_count` - 粪便团块数量

### 上下文与排除信号
- `is_post_feeding_within_72h` - 是否喂食后 72h 内（食物种类影响粪便颜色/形态：蟋蟀绿色便 / 粉鼠深色便 / 植物纤维便）
- `is_during_shedding_period` - 是否处于蜕皮期（蜕皮期食欲下降可能影响排泄）
- `is_gravid_female` - 是否抱蛋雌性（抱蛋期排泄间隔延长/尿酸增大属正常）
- `is_brumation_period` - 是否休眠/冬眠期（休眠期排泄频率大幅下降，尿酸可能浓缩增大）
- `substrate_type` - 垫材类型（reptile_carpet / paper_towel / coco_husk / bark / sand / tile）→ 影响排泄物识别难度
- `recent_diet_change` - 近期是否更换食物 < 7 天（食物变更可导致短期粪便异常）
- `image_quality_acceptable` - 图像质量是否合格

## 综合判定

- `excrement_healthy` - 排泄物健康（尿酸白色正常质地 + 粪便棕色成形条状）
- `urate_mildly_abnormal` - **尿酸轻度异常**（尿酸面积较基线增大 20-50% OR 质地粗糙颗粒 OR 颜色偏黄/橙）
- `urate_significantly_abnormal` - **尿酸显著异常**（尿酸面积较基线增大 > 50% OR 质地硬块 OR 颜色橙/红提示 → 脱水/肾脏负担风险）
- `feces_mildly_abnormal` - **粪便轻度异常**（粪便稀软糊状 OR 颜色偏绿/黄 OR 可见少量未消化内容）
- `feces_significantly_abnormal` - **粪便显著异常**（粪便水样 / 黑色柏油便 / 红色血便 / 大量黏液 / 大量未消化内容 → 肠炎/寄生虫/消化道出血风险）
- `excrement_context_diet_or_brumation` - 饮食变更/休眠期上下文，排泄物异常属临时
- `excrement_signal_unreliable` - 信号不可靠（排泄物被踩踏/被垫材遮挡/光照色温偏移/分辨率 < 1080p/无参考物无法归一化）

## 4 级提醒策略递进

- Level 1（excrement_healthy）：仅入库
- Level 2（urate_mildly_abnormal / feces_mildly_abnormal / context_diet_or_brumation）：温和提示，建议**观察下次排泄是否恢复正常 + 检查温度是否在物种适宜范围 + 确认喂食内容/频率是否合适**
- Level 3（urate_significantly_abnormal OR feces_significantly_abnormal）：紧急提示，建议**检查脱水迹象（皮肤皱褶/眼窝凹陷） + 提供充足饮水 + 检查温度梯度 + 收集新鲜粪便送检寄生虫 + 观察食欲精神 + 联系爬宠兽医（尿酸持续增大提示肾脏负担，血便/水样便提示肠炎或寄生虫感染）**
- Level 4（尿酸显著异常 + 粪便显著异常 同时出现）：最高紧急提示，建议**立即联系爬宠兽医（肾脏负担+肠道问题同时出现，可能为系统性感染/败血症前兆） + 保持环境稳定 + 保留排泄物样本供兽医检查**

## 单日提醒上限

- Level 1 不限 / Level 2 × 3 / Level 3 × 5 / **Level 4 不设上限（肾脏+肠道双重异常·败血症前兆风险）**

## 红线约束

- **🚨 禁止**做"肾衰竭 / 痛风 / 肠炎 / 寄生虫感染 / 沙门氏菌 / 阿米巴 / 消化道出血 / 败血症"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、驱虫药品牌、抗生素品牌、止泻药品牌、口服/注射剂量
- **🚨 绝对禁止**输出"用芬苯达唑 50mg/kg 驱虫""口服甲硝唑 25mg/kg""灌服益生菌 X 克""注射拜有利 5mg/kg"等具体处方
- **🚨 绝对禁止**输出"自行灌肠""自行催吐""自行挤压排泄口"等任何外科或医疗操作（必须由爬宠兽医现场判断）
- **禁止**长期存储排泄物图像（≤ 14 天，留关键帧 + 尿酸/粪便趋势；养殖场/医院按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户调整喂食内容/频率；任何饮食变更必须由用户确认（仅可建议）
- 所有指标必须基于真实图像分析；**禁止伪造或夸大尿酸面积、粪便稀软程度**
- 物种特异性：**蛇类**排泄频率低（7-14 天一次）、尿酸与粪便同时排出为"复合排泄" / **蜥蜴/守宫**排泄更频繁（1-3 天）、尿酸与粪便可能分开 / **草食性龟类**粪便量大含植物纤维 / **肉食性蛇类**粪便少含毛发 → 必须按物种排泄习性判定
- 必须考虑生理性上下文：**食物种类影响粪便颜色/形态**（蟋蟀绿便/粉鼠深色便） / **休眠/冬眠期排泄频率下降+尿酸浓缩** / **抱蛋期排泄间隔延长** / **近期换食 < 7 天** → 必须排除
- 排泄物被踩踏/被垫材遮挡/光照色温偏移/分辨率 < 1080p/无参考物 → 必须返回 `excrement_signal_unreliable`
- 必须告知用户：AI 排泄物评估仅供参考，**异常排泄物确诊需粪便镜检 + 寄生虫浮聚法 + 尿酸结晶分析 + 血液检查，联系专业爬宠兽医**

## 输出报告字段

- `report_date`、`enclosure_id`、`individual_id`、`species`、`urate_color_classification`、`urate_area_normalized_by_body_length`、`urate_area_vs_historical_baseline`、`urate_texture`、`feces_color_classification`、`feces_consistency`、`feces_length_to_width_ratio`、`undigested_content_visible`、`composite_scene`、`alert_level`、`recommended_actions`（观察下次排泄 / 检查温度 / 确认喂食内容 / 提供饮水 / 收集粪便送检 / 联系爬宠兽医，**不含具体药物/驱虫药品牌/剂量/外科操作**），`disclaimer`
