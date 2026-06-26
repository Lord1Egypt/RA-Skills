# API 接口文档

此处用于存放爬宠蜕皮进度识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动爬宠蜕皮进度识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（体表颜色 / 蓝眼 / 蜕皮阶段 / 卡皮风险）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史蜕皮进度记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出蜕皮护理建议报告

## 场景代码

- `SMYX_REPTILE_SHEDDING_PROGRESS_ANALYSIS` - 爬宠蜕皮进度识别

## 输入约束

- 摄像头：爬宠箱 / 饲养缸 / 养殖场固定摄像头
- 分辨率 ≥ 1080p（**蜕皮起翘细节 + 眼部蓝眼细节需高清**）
- 拍摄角度：**侧面 + 俯视双角度**（守宫/蜥蜴俯视看背部，蛇侧面看体表起翘）
- 光照：均匀白色光源（避免色温偏移影响体色发白判定）
- **核心采样窗口**：每日 1 次 OR 每半日 1 次（蜕皮全过程 7-14 天）
- 多缸场景按摄像头 ID + 个体 ID 双重绑定
- **部署时必须录入**：物种（蛇类/守宫/蜥蜴/水龟壳）、个体年龄（幼体蜕皮频繁 1-2 周一次 / 成体 1-2 月一次）、上次完整蜕皮日期、当前湿度、温度梯度、蜕皮辅助物（粗糙树皮/水盆/湿润箱）

## 关键观测信号

### 体表颜色与质地
- `body_color_classification` - **体表颜色分类**（核心指标：normal_vivid_color / **dull_faded_pre_shed**（暗淡褪色，蜕皮准备期）/ **whitish_milky_shed_ready**（发白乳白色，准备期晚期）/ **partial_old_skin_attached**（局部旧皮附着，进行期）/ recovered_post_shed_vivid（蜕皮后体色恢复鲜艳））
- `body_surface_lift_detected` - **体表旧皮起翘是否可见**（核心指标，进行期标志）
- `body_color_brightness_score_0_100` - 体色亮度评分（**蜕皮准备期 < 50 / 完成期回升至 > 70**）
- `body_surface_dryness_score_0_10` - 体表干燥度评分（**> 7 干燥可能加剧卡皮**）
- `old_skin_attachment_zones` - 旧皮附着区域（head / dorsal / ventral / **toes**（脚趾）/ **tail_tip**（尾尖）/ vent / **eye_caps**（蛇眼睑残留））

### 眼部状态（蓝眼 blue-phase 关键指标）
- `eye_state_classification` - **眼部状态分类**（核心指标：clear_normal / **opaque_milky_blue_phase**（蓝眼浑浊乳白，蜕皮准备期）/ clear_post_shed_recovered（蜕皮后恢复透明））
- `eye_opacity_score_0_10` - 眼部浑浊度评分（**> 6 蓝眼期 / < 2 透明期**）
- `eye_caps_residual_visible` - **蛇眼睑残留是否可见**（**蛇类卡皮高危区域，可能压迫眼球需兽医介入**）

### 蜕皮辅助物与环境
- `humid_box_or_substrate_visible` - 湿润箱/湿润底材是否可见
- `rough_surface_available` - 粗糙摩擦面（树皮/石板）是否可见
- `water_bowl_size_adequate` - 水盆大小是否充足（**蛇类蜕皮期需可整体浸泡的大水盆**）
- `current_humidity_within_species_range` - 当前湿度是否在物种推荐范围（**湿度不足 ≥ 卡皮主因**）

### 上下文与排除信号
- `last_complete_shed_days_ago` - 距上次完整蜕皮天数（用于判断蜕皮周期是否正常）
- `is_juvenile` - 是否幼体（**幼体蜕皮频繁 1-2 周一次** / 成体 1-2 月）
- `is_during_brumation` - 是否处于休眠/冬眠期（休眠期不蜕皮属正常）
- `recent_injury_or_burn` - 近期是否有烫伤/外伤（外伤区域可能影响蜕皮）
- `image_quality_acceptable` - 图像质量是否合格

## 综合判定

- `shed_phase_normal_state` - 正常体色，无蜕皮迹象
- `shed_phase_preparation` - **蜕皮准备期**（体色暗淡褪色 + 蓝眼浑浊 + 体表干燥度上升）
- `shed_phase_in_progress` - **蜕皮进行期**（局部旧皮起翘 + 头部首先蜕落 + 体色发白乳白）
- `shed_phase_completed_normal` - **蜕皮完成期**（旧皮完全脱离 + 体色恢复鲜艳 + 眼部透明）
- `shed_phase_dysecdysis_warning` - **🚨 卡皮警告**（蜕皮进行期 > 7 天未完成 / 脚趾尾尖眼睑残留旧皮 / 局部缠绕勒紧）
- `shed_phase_context_brumation_or_injury` - 休眠/外伤上下文，蜕皮异常属临时
- `shed_phase_signal_unreliable` - 信号不可靠（角度偏 / 光照色温偏移 / 个体藏匿 / 分辨率 < 1080p）

## 4 级提醒策略递进

- Level 1（shed_phase_normal_state / shed_phase_completed_normal）：仅入库
- Level 2（shed_phase_preparation）：温和提示，建议**适当增加环境湿度（按物种手册推荐范围调整） + 检查湿润箱/湿润底材是否到位 + 提供粗糙摩擦面 + 减少不必要的把玩**
- Level 3（shed_phase_in_progress 顺利）：进度跟踪提示，建议**继续保持湿度 + 持续观察至完成 + 避免强行剥落旧皮 + 检查水盆大小是否足够蛇类浸泡**
- Level 4（**shed_phase_dysecdysis_warning** 卡皮）：紧急提示，建议**立即提升环境湿度至物种推荐高线 + 提供温水浅盘浸泡（水位仅没腹部，时长 15-30 分钟）+ 让爬宠在粗糙树皮上自行摩擦 + 仍未脱落 → 联系爬宠兽医（脚趾/尾尖/眼睑卡皮可能导致缺血坏死/失明）**

## 单日提醒上限

- Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5

## 红线约束

- **🚨 严禁**做"蜕皮综合征 / 缺血坏死 / 眼睑感染 / 角膜溃疡 / 截肢"等**具体医学诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、抗生素品牌、眼药水品牌、剥皮油品牌
- **🚨 绝对禁止**输出"自行用镊子撕扯旧皮""自行剥离眼睑""自行涂抹凡士林到眼睛""自行切割脚趾断皮"等任何**侵入式操作或外科操作**指令
- **🚨 严禁推荐具体湿度/温度数字**（如"湿度调到 90%""温度升到 32℃"）；仅可建议"按物种手册推荐范围调整"
- **🚨 严禁强制干预蛇类完整蜕皮**：蛇类蜕皮应为**完整一条蛇皮（含眼睑）**，AI 不应建议中途人工干预（除非已发生 Level 4 卡皮）
- **🚨 严禁温水浸泡水位过高**：必须明确"水位仅没腹部，时长 15-30 分钟"，**禁止建议长时间或深水浸泡**（可能导致溺水/呼吸道感染）
- **禁止**长期存储爬宠箱视频（≤ 14 天，留每次蜕皮关键节点截图 + 蜕皮时间线；养殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户调整湿度/温度；任何环境控制变更必须由用户确认（仅可建议）
- 所有指标必须基于真实图像分析；**禁止伪造或夸大蜕皮阶段判定**
- 物种特异性：**蛇类蜕皮整张脱落（含眼睑）** / **守宫/蜥蜴蜕皮分片状脱落（守宫会自食蜕下的皮）** / **水龟蜕皮为甲壳鳞片单片脱落** → 严禁通用判定
- 必须考虑生理性上下文：**幼体蜕皮频繁 1-2 周一次** / **休眠期不蜕皮** / **外伤区域影响蜕皮** → 必须排除
- 个体藏匿 / 角度偏 / 光照色温偏移 / 分辨率 < 1080p → 必须返回 `shed_phase_signal_unreliable`
- 必须告知用户：AI 蜕皮评估仅供参考，**Level 4 卡皮持续 > 3 天 → 必须联系专业爬宠兽医（脚趾/尾尖/眼睑卡皮可致缺血坏死/失明）**

## 输出报告字段

- `report_date`、`enclosure_id`、`individual_id`、`species`、`body_color_classification`、`body_surface_lift_detected`、`body_color_brightness_score_0_100`、`body_surface_dryness_score_0_10`、`old_skin_attachment_zones`、`eye_state_classification`、`eye_opacity_score_0_10`、`eye_caps_residual_visible`、`humid_box_or_substrate_visible`、`current_humidity_within_species_range`、`last_complete_shed_days_ago`、`composite_scene`（蜕皮阶段）、`alert_level`、`recommended_actions`（增加湿度按物种范围 / 提供粗糙摩擦面 / 温水浅盘浸泡水位没腹部 15-30 分钟 / 联系爬宠兽医，**不含具体湿度温度数字、不含侵入式操作、不含具体药物**），`disclaimer`
