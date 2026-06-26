# API 接口文档

此处用于存放植物卷叶/焦边识别（干旱/病害）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动卷叶/焦边诊断任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与原因诊断
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史诊断记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_LEAF_CURLING_MARGIN_SCORCH_DIAGNOSIS_ANALYSIS` - 植物卷叶/焦边识别（干旱/病害）

## 输入约束

- 推荐拍摄叶片整体形态（区分新叶 / 老叶）以及叶尖/叶缘特写
- 光照均匀、无明显阴影、聚焦清晰
- 可选附带传感器/环境数据：土壤湿度 %、空气湿度 %、近期施药/施肥记录

## 关键观测特征

- 卷曲方向：上卷（叶片向上反卷）/ 下卷（叶片向下内卷）
- 焦边分布：叶尖灼烧 / 叶缘焦枯 / 整叶干枯
- 分布部位：老叶 / 新叶 / 顶端嫩叶 / 全株
- 伴随特征：叶色变化（黄化/紫红）、白粉、坏死斑、水浸状斑

## 输出字段（参考）

- `curl_direction` - 卷曲方向（up_curl / down_curl / mixed / none）
- `scorch_pattern` - 焦边分布（tip_burn / margin_scorch / whole_leaf_dry）
- `affected_leaves` - 受害叶层（old_leaves / new_leaves / top_leaves / whole_plant）
- `likely_causes` - 可能原因排序（drought / disease_powdery_mildew / virus / pesticide_damage / fertilizer_burn / cold_stress 等）
- `confidence_top1` - 最可能原因的置信度
- `evidence_hints` - 关键视觉证据描述

> 仅输出基于视觉（及可选土壤湿度）的可能原因排序，不输出具体农药/肥料名称或剂量。
