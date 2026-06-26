# API 接口文档

此处用于存放鱼类体表白点/充血/烂尾识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼类体表症状识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取症状检测结果（症状类型 + 置信度 + 部位 + 严重程度）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史体表健康报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出体表健康报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 智能鱼缸告警灯）

## 场景代码

- `SMYX_FISH_SURFACE_SYMPTOM_DETECTION_ANALYSIS` - 鱼类体表白点/充血/烂尾识别

## 输入约束

- 摄像头：鱼缸固定摄像头或水下摄像头，建议能近距离（≤ 30 cm）清晰拍摄鱼体侧面 / 尾部 / 鳃盖
- 分辨率 ≥ 1080p（白点直径 0.5-1mm，需高清才能可靠识别）；帧率 ≥ 10 FPS（图像模式 ≥ 2 张/小时）
- 光照：建议鱼缸照明开启 + 无强反光；水质清澈（浑浊度低）
- 拍摄角度：优先正侧面 + 尾部特写；体表完整可见
- 输入类型：支持高清图像（jpg/png）或视频；视频会自动抽帧进行体表分析
- 多鱼缸场景按摄像头 ID 绑定到注册鱼缸 ID（每个鱼缸独立鱼种清单）
- 用户必须授权部署；公共水族馆需公示告知

## 关键观测信号（按症状类型）

### 白点症状（white_spot）
- `white_spot_count` - 检测到的白点数量
- `white_spot_avg_diameter_mm` - 平均直径（mm，典型 0.5-1mm）
- `white_spot_location` - 分布部位（fin / gill_cover / body / tail，可多选）
- `white_spot_density_score` - 密度评分（0-100，覆盖比例）
- `white_spot_confidence` - 置信度（0-1）

### 充血症状（hyperemia）
- `hyperemia_area_ratio` - 充血面积占体表比例（0-1）
- `hyperemia_location` - 分布部位（fin_base / body_surface / gill / abdomen）
- `hyperemia_pattern` - 形态（blood_streak 血丝 / red_patch 片状红斑）
- `hyperemia_severity` - 严重程度（mild / moderate / severe）
- `hyperemia_confidence` - 置信度（0-1）

### 烂尾症状（fin_rot）
- `tail_edge_whiteness_score` - 尾鳍边缘发白评分（0-100）
- `tail_jagged_edge_detected` - 是否呈锯齿状边缘
- `tail_missing_area_ratio` - 尾鳍缺失面积比例（0-1）
- `tail_rot_severity` - 严重程度（mild / moderate / severe）
- `fin_rot_confidence` - 置信度（0-1）
- `other_fin_rot_detected` - 其他鳍是否也出现腐烂（背鳍 / 胸鳍 / 腹鳍）

## 综合判定

- `surface_healthy` - 体表健康
- `white_spot_early` - 白点早期（数量 ≤ 5 + 单部位）
- `white_spot_moderate` - 白点中期（数量 5-20 + 多部位）
- `white_spot_severe` - 白点重度（数量 > 20 / 密度 ≥ 30%）
- `hyperemia_local` - 局部充血
- `hyperemia_systemic` - 全身性充血
- `fin_rot_mild` - 烂尾轻度（仅边缘发白）
- `fin_rot_severe` - 烂尾重度（明显缺损 / 多鳍同时腐烂）
- `multi_symptom_concurrent` - 多症状并发（白点 + 充血 / 充血 + 烂尾等）

## 4 级告警策略递进

- Level 1（early / mild）：用户 APP 轻提醒，建议加强观察 + 检查水温/pH/氨氮
- Level 2（moderate / local）：用户 APP 重要告警，建议**隔离病鱼到独立缸**、检查水质并适当升温（针对白点）
- Level 3（severe / systemic / multi_symptom_concurrent）：紧急告警，建议**立即隔离 + 全缸检疫**，并提示联系**当地观赏鱼兽医或水族馆**
- Level 4（多日反复 / 同缸多条鱼同时发病）：紧急告警 + 强烈建议**全缸消毒处理**并咨询专业人员

## 单日告警上限

- Level 1 × 6 / Level 2 × 3 / Level 3 × 2 / Level 4 不设上限

## 红线约束

- **禁止**做"小瓜虫病 / 细菌性败血症 / 水霉病 / 柱状菌病"等具体疾病诊断
- **绝对禁止**输出具体药物名称、剂量、给药方案（如孔雀石绿 / 甲基蓝 / 黄粉 / 庆大霉素等）
- 禁止长期存储完整鱼缸图像 / 视频（≤ 7 天，仅入库症状事件帧）
- 禁止用于商业广告 / AI 训练；禁第三方共享
- 禁止越权代用户调整智能鱼缸的加热 / 换水 / 投药参数；任何水族设备控制变更必须由用户确认
- 置信度、白点数量、充血面积、烂尾比例等指标必须基于真实图像识别；**禁止伪造或夸大指标**
- 鱼种特异性：部分鱼种（如珍珠鳞、银河系神仙鱼）天然带白色斑点，**必须**按鱼种基线判定，禁止与白点病混淆
- 反射光、气泡、底砂颗粒可能造成假阳性 → 必须做去伪处理，并将"假阳风险标记"输出给用户
- 必须告知用户：AI 识别仅供参考，**最终诊断与治疗方案需专业水族兽医确认**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸 ID
- `species` - 鱼种
- `detected_symptoms` - 检测到的症状列表（含类型、置信度、部位、严重程度）
- `composite_scene` - 综合场景判定
- `alert_level` - 告警等级
- `recommended_actions` - 建议动作（隔离 / 升温 / 检查水质 / 联系兽医，**不含具体药物**）
- `disclaimer` - 免责声明（AI 仅辅助，最终诊断需专业兽医）
