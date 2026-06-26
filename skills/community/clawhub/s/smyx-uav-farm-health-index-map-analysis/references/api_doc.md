# API 接口文档

此处用于存放无人机农田健康指数图生成 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动农田健康指数图生成任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（指数图 + 异常区域）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史指数图记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_UAV_FARM_HEALTH_INDEX_MAP_ANALYSIS` - 无人机农田健康指数图生成

## 输入约束

- 推荐使用无人机正射影像或拼接图（GeoTIFF / JPG / PNG），含定位信息（EXIF/GeoTag）更佳
- 支持多光谱（包含 NIR / Red Edge 波段）或高分辨率 RGB 影像
- 飞行参数建议：飞行高度 80-120m、航向/旁向重叠 ≥ 70%、晴朗弱风时段拍摄
- 关键观测对象：作物冠层覆盖区域，避免大面积水体/建筑物干扰

## 支持的植被指数

- `NDVI` - 归一化植被指数（Normalized Difference Vegetation Index）
- `NDRE` - 归一化红边指数（Normalized Difference Red Edge）
- `OSAVI` - 优化土壤调整植被指数
- `GNDVI` - 绿光归一化植被指数
- 若为 RGB 影像，回退使用 `VARI` / `ExG` 等可见光植被指数

## 输出字段（参考）

- `health_index_map_url` - 农田健康指数热力图 URL（红/黄/绿三段色阶）
- `mean_ndvi` - 整体平均植被指数
- `low_health_zones` - 健康异常区域列表（坐标多边形 + 面积 ha）
- `coverage_ratio` - 作物覆盖率（%）
- `field_stats` - 分区统计（高/中/低健康占比）

> 仅输出基于植被指数的评估结果与异常区域，不输出具体农事操作建议（施肥量、农药品种等）。
