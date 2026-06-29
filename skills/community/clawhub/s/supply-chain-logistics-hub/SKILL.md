---
name: 供应链与物流智能中枢
slug: supply-chain-logistics-hub
description: 端到端供应链管理与物流优化AI平台。覆盖需求预测、库存优化、采购决策、物流路径规划、关务合规（HS编码归类/RCEP原产地）、供应商风险监控、冷链管理、仓储布局优化。支持海运/空运/铁路/公路多式联运全网路径仿真。
version: 1.0.0
author: ai-gaoqian
tags:
  - supply-chain
  - logistics
  - procurement
  - inventory-optimization
  - customs-compliance
  - rcep
  - freight-forwarding
  - warehouse-management
  - demand-forecasting
  - cold-chain
metadata:
  openclaw:
    requires: ">=1.0.0"
---

# 供应链与物流智能中枢

## 概述
覆盖计划(Plan)、采购(Source)、制造(Make)、交付(Deliver)、退货(Return)的SCOR模型全流程AI助手，适配制造业、零售、电商、医药等多行业场景。

## 核心能力

### 1. 需求预测与库存优化
- 时间序列预测（ARIMA/Prophet/LSTM选型建议）
- 安全库存与再订货点动态计算
- ABC-XYZ 分类与差异化补货策略
- 多级库存（MEIO）网络优化
- 呆滞库存预警与去化方案

### 2. 采购与供应商管理
- 供应商评估与绩效评分卡（QCDMES模型）
- RFP/RFQ 自动生成与报价对比
- 供应商风险预警（财务/地缘/合规/ESG）
- 采购合同条款模板库
- 集中采购 vs 分散采购策略分析

### 3. 物流与运输优化
- 多式联运路径规划（海运/空运/铁路/公路）
- 集装箱配载优化（3D Bin Packing）
- 运费比价与承运人选择
- 最后一公里配送策略
- 逆向物流与退货网络设计

### 4. 关务与贸易合规
- HS 编码智能归类（含归类争议案例库）
- RCEP/CPTPP/USMCA 原产地规则判定
- 关税税率查询与优惠方案对比
- 出口管制（ECCN/EAR/ITAR）合规检查
- AEO 认证准备指导

### 5. 仓储管理
- 仓库布局优化（ABC分区/动线设计）
- WMS 核心流程设计（收货/上架/拣货/包装/发货）
- 波次策略与订单合并
- 自动化设备选型建议（AGV/AMR/分拣机）

### 6. 供应链风险与韧性
- 供应商集中度风险分析
- 地缘政治风险地图
- 自然灾害暴露评估
- 业务连续性计划（BCP）模板
- 近岸/友岸外包策略评估

## 内置数据集
- 全球主要港口时效与拥堵指数
- HS 编码数据库（2027版）
- RCEP 关税减让表
- 各运输方式碳排放因子
- 仓储运营KPI基准（行业平均）

## 输出格式
- 供应链网络优化方案
- 库存策略建议书
- 运输路径对比矩阵
- 关税最优方案报告
- 供应商风险评估热力图
