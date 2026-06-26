# API 接口文档

此处用于存放学生课堂情绪参与度分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动学生课堂情绪参与度分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取群体参与度评分 + 匿名低参与度提示
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史参与度报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告（含参与度热力图）

## 场景代码

- `SMYX_CLASSROOM_ENGAGEMENT_ANALYSIS_ANALYSIS` - 学生课堂情绪参与度分析

## 输入约束

- 摄像头：中小学教室 / 培训课堂 / 在线教育（需拍摄学生）固定摄像头，**讲台对面或斜侧高位**，画面应覆盖大部分学生脸部
- 帧率 ≥ 5 FPS（推荐 10-15 FPS）；分辨率 ≥ 720p；光照稳定避免逆光
- 视频时长建议 ≥ 5 分钟，匹配教学环节（导入 / 讲解 / 互动 / 练习）
- 初次部署需标定教室座位 ROI 网格（row × col，如 6×8，用于热力图坐标）
- **匿名约束**：不进行人脸识别 / 人脸比对 / 学生身份绑定；低参与度提醒仅返回座位坐标（如 row=3, col=2），不返回学生姓名

## 关键观测信号

- `student_count_detected` - 当前帧检测到的学生人数
- `emotion_distribution` - 班级情绪分布（focused / confused / happy / frustrated / bored / neutral 占比）
- `focus_ratio` - 专注比例（focused + 适度 happy + 适度 neutral）
- `confusion_ratio` - 困惑比例（confused / frustrated）
- `bored_ratio` - 无聊比例（bored + 走神：头部偏离讲台方向 + 长时间垂眼）
- `head_pose_toward_teacher_ratio` - 头部朝向讲台比例（参考指标）
- `hand_raise_event_count` - 举手互动次数（参考指标）
- `engagement_score` - 班级整体参与度评分（0-100）
- `low_engagement_seats` - 低参与度座位坐标数组（仅 row/col，不绑定身份）

## 阈值与等级

- `≥ 80` - 高参与度（excellent）
- `60-79` - 良好参与度（good）
- `40-59` - 中等参与度（fair）→ 建议教师调整节奏
- `< 40` - 低参与度（low）→ 触发实时提醒
- 教学环节切换（如从讲解 → 练习）时短暂下降视为正常

## 输出字段（参考）

- `time_window` - 采样时间窗口
- `teaching_phase_hint` - 推测教学环节（lecture / interaction / practice / unknown）
- `student_count_detected` / `emotion_distribution` / `focus_ratio` / `confusion_ratio` / `bored_ratio` / `head_pose_toward_teacher_ratio` / `hand_raise_event_count`
- `engagement_score` - 班级整体参与度评分
- `engagement_level` - 等级（excellent / good / fair / low）
- `low_engagement_seats` - 低参与度座位坐标数组（[{row, col}, ...]，**不含身份**）
- `confusion_hotspot_seats` - 困惑表情集中座位（[{row, col}, ...]）
- `trend_vs_last_window` - 相比上一时间窗变化（delta_pct）
- `alert_type` - 提醒类型（low_engagement / high_confusion / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `teacher_suggestion` - 教师建议（如"班级整体参与度 38（low），建议穿插一个 2 分钟小组讨论或提问环节；困惑集中在 row=3 col=2 附近，建议复述刚才的概念"）
- `engagement_heatmap_image_url` - 参与度热力图 URL（叠加在教室座位图上）

## 强制隐私约束

- ❌ **禁止**进行人脸识别 / 人脸比对 / 学生身份绑定
- ❌ **禁止**将"低参与度"用于学生绩效评估、家长沟通或公开排名
- ❌ **禁止**长期存储原始视频或可识别个人特征的数据
- ✅ 仅输出**班级群体聚合** + **座位坐标级别**的匿名提示，作为教师**实时**辅助参考
- ✅ 涉及未成年人，必须取得**学校 + 家长**双重知情同意，并明确告知用途与数据保存期限

> 仅输出基于视觉的群体行为聚合统计与教学辅助提示，**不构成对任何学生的能力评价、心理诊断或个人画像**；任何针对个体的关怀沟通应由教师 / 心理老师依据课堂观察与自愿性谈话进行。
