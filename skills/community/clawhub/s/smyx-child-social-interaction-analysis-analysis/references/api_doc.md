# API 接口文档

此处用于存放儿童社交互动频次与时长分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童社交互动分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（互动统计 + 热力图）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史社交互动记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_SOCIAL_INTERACTION_ANALYSIS_ANALYSIS` - 儿童社交互动频次与时长分析

## 输入约束

- 摄像头建议固定俯视/广角，覆盖完整活动区域（教室、游戏区、操场）
- 视频时长建议 ≥ 1 分钟，帧率 ≥ 10 FPS
- 可选附带：班级名单（用于稳定的多目标 ID 关联）、地面/场地标定（用于像素 → 米的距离换算）

## 关键检测对象

- 多儿童目标检测 + 跨帧 ID 跟踪
- 面对面朝向（face-to-face orientation）
- 嘴部运动（疑似对话）
- 群体行为（合作玩耍 / 追逐 / 共享玩具）
- 儿童间距离（结合标定换算米）

## 社交互动事件类型

- `approach` - 接近（距离 < 1 m）
- `conversation` - 对话（面对面且嘴部运动）
- `cooperative_play` - 共同游戏（合作玩耍 / 追逐 / 共享道具）
- `physical_contact` - 身体接触（拥抱 / 牵手）

## 输出字段（参考）

- `children_detected_count` - 检测到的儿童数量
- `child_ids` - 儿童 ID 列表（视频内稳定 ID）
- `interaction_pairs` - 每对儿童的互动统计（pair_id / interaction_count / total_duration_sec / 各事件类型分项）
- `initiator_stats` - 主动发起方统计（每个儿童作为 initiator 的次数）
- `loner_candidates` - 互动量显著偏低的儿童候选列表（疑似孤僻 / 被排斥）
- `social_heatmap_url` - 社交互动热力图 URL（pair-pair 互动强度矩阵或场地热力图）
- `summary` - 班级整体社交活跃度概览
- `alert_hint` - 异常提示（如"3 号儿童 30 分钟内互动 0 次，建议教师关注"）

> 仅输出基于视觉的社交行为统计数据与热力图，不提供心理诊断或孤独症诊断；如怀疑发育异常，请前往专业儿童医疗机构评估。
