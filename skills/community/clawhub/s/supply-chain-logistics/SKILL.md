---
name: Supply Chain & Logistics Optimizer
slug: supply-chain-logistics
description: 全球供应链与物流智能优化技能。覆盖需求预测、库存优化、路径规划、供应商评估、关务合规、碳足迹追踪、仓储布局设计。内置运筹学模型（线性规划/整数规划/动态规划），支持SAP/Oracle NetSuite/金蝶等ERP系统对接，适配跨境电商、制造业、冷链、医药物流等多行业场景。
version: 1.0.0
author: ai-gaoqian
tags:
  - supply-chain
  - logistics
  - inventory
  - procurement
  - warehousing
metadata:
  openclaw:
    requires:
      - python>=3.10
      - numpy
      - scipy
---

# Supply Chain & Logistics Optimizer

Intelligent supply chain optimization covering demand forecasting, inventory management, routing, procurement, customs compliance, and carbon tracking.

## Core Modules

### 1. Demand Forecasting
- Time-series models (ARIMA, Prophet, LSTM-ready)
- Seasonal decomposition and trend analysis
- Promotion/lift factor modeling
- New product launch demand estimation
- Bullwhip effect quantification and mitigation

### 2. Inventory Optimization
| Model | Use Case |
|-------|----------|
| EOQ (Economic Order Quantity) | Stable demand items |
| (s, Q) Reorder Point | Continuous review |
| (R, S) Periodic Review | Scheduled replenishment |
| Newsvendor Model | Perishable/fashion goods |
| Multi-echelon optimization | Distributed warehouse networks |

- Safety stock calculation (service level 90%/95%/99%)
- ABC/XYZ classification
- Dead stock identification and liquidation plan
- Cross-docking opportunity analysis

### 3. Route & Transportation Optimization
- Vehicle Routing Problem (VRP/CVRP/VRPTW) solver
- Last-mile delivery optimization
- Multi-modal transport planning (sea/air/rail/road)
- Carrier rate comparison and selection
- Fuel cost and CO2 emission calculation
- Real-time traffic integration (高德/Google Maps API)

### 4. Supplier & Procurement Management
- Supplier scorecard (quality/delivery/cost/responsiveness)
- RFQ/RFP generation and bid analysis
- Supplier risk assessment (geopolitical, financial, compliance)
- Contract lifecycle management
- Multi-sourcing strategy optimization

### 5. Customs & Trade Compliance
- HS code classification (WCO Harmonized System)
- Import/export documentation generation
- Free Trade Agreement (FTA) eligibility check
- Tariff calculation and duty drawback
- Restricted party screening
- Country-of-origin determination

### 6. Warehouse Design & Layout
- Slotting optimization (ABC velocity-based)
- Pick path optimization
- Labor allocation and shift planning
- Storage type recommendation (pallet/rack/bins)
- WMS integration templates

### 7. Carbon Footprint Tracking
- Scope 1/2/3 emissions calculation
- Transportation carbon accounting (GLEC Framework)
- Supplier carbon scorecard
- Carbon offset procurement suggestions
- ESG report data preparation

## Industry Templates

| Industry | Pre-configured Models |
|----------|----------------------|
| Cross-border E-commerce | Multi-warehouse + FBA/FBM + tariff |
| Manufacturing | MRP + BOM explosion + JIT |
| Cold Chain | Temperature monitoring + shelf-life |
| Pharma | GDP compliance + serialization |
| Retail | Omni-channel + store fulfillment |

## Usage

```yaml
# Optimize inventory
optimize: inventory
warehouse: [Shanghai, Guangzhou, Chengdu]
products: SKU_list.csv
service_level: 0.95
output: replenishment_plan.xlsx

# Route optimization
optimize: routing
depot: Shenzhen
deliveries: 45
vehicles: 8
constraints: [time_windows, capacity]
output: route_plan.json
```
