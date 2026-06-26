# API 接口文档

此处用于存放驾驶员面部潮红/出汗异常检测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动驾驶员潮红/出汗异常检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取潮红/出汗分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史异常事件
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_DRIVER_FLUSHING_SWEAT_DETECTION_ANALYSIS` - 驾驶员面部潮红/出汗异常检测

## 输入约束

- 摄像头：车载 DMS 摄像头，**优先使用彩色（RGB）通道**；纯红外通道无法识别潮红
- 安装位置：方向盘上方 / A 柱 / 仪表台上方，正对驾驶员面部
- 帧率：≥ 15 FPS；分辨率 ≥ 480p
- 光照尽量稳定（白平衡固定），避免强逆光、车窗滤色片严重影响 RGB
- 戴口罩会显著降低潮红面积识别可靠性

## 关键观测特征

- `flush_index` - 面部潮红指数（基于 RGB 红色分量比 / 肤色模型偏移，0-1）
- `flush_area_ratio` - 潮红区域面积占面部 ROI 的比例
- `sweat_glare_area_ratio` - 汗珠/皮肤反光面积占面部 ROI 的比例
- `skin_texture_score` - 皮肤纹理粗糙度（受汗液/油脂反光影响）
- `baseline_flush_index` - 当次会话起始基线潮红值（用于变化幅度判定）
- `flush_index_delta` - 当前潮红指数相对基线的变化幅度

## 默认阈值（可由调用方覆盖）

- 潮红指数阈值：`flush_index > 0.6` 或 `flush_index_delta > 0.25`
- 出汗反光面积阈值：`sweat_glare_area_ratio > 0.15`（约 15% 面部 ROI）
- 持续时间阈值：异常状态持续超过 5 秒触发提醒

## 预警类型

- `facial_flushing` - 面部潮红显著升高（可能与血压升高 / 发热 / 情绪激动等相关）
- `excessive_sweating` - 大量出汗（可能与热应激 / 低血糖 / 心脏不适等相关）
- `combined_flush_sweat` - 潮红 + 出汗同时出现（更高优先级提醒）

## 输出字段（参考）

- `driver_detected` - 是否检测到驾驶员
- `face_visible` - 面部是否可见（戴口罩/严重遮挡时为 false）
- `flush_metrics` - 潮红相关指标（flush_index / flush_area_ratio / flush_index_delta）
- `sweat_metrics` - 出汗相关指标（sweat_glare_area_ratio / skin_texture_score）
- `warning_type` - 触发的预警类型
- `warning_message` - 预警提示文本（如"驾驶员面部潮红指数上升 0.32 且额头出汗反光面积 22%，请注意身体状态，建议就近停车休息"）
- `recommend_action` - 建议的座舱联动动作（voice_alert / fleet_upload / event_record）

> 仅输出基于视觉的面部潮红/出汗异常现象提示，不提供血压、心脏病、中暑、低血糖等具体医学诊断；如有不适请及时就医并由专业人员评估。
