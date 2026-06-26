# SalesClaw 知识库索引

## SQL 模板（NL2SQL 沉淀）

| 模板 ID | 适用问题 | 优先级 |
|---------|---------|--------|
| `prescription_trend` | 品种趋势/处方量下滑/环比 | P0 |
| `expense_red_green` | 费用异常/DeltaWeight/红黄灯 | P0 |
| `rep_performance` | 代表绩效/红黄牌/达成率 | P0 |
| `target_attainment` | 区域达成/缺口分析 | P1 |
| `hospital_access` | 进院情况/VBP覆盖 | P1 |
| `prescription_penetration` | 渗透率/覆盖率/上量空间 | P1 |
| `doctor_profile` | 医生档案/KOL识别 | P1 |
| `data_overview` | 数据概览/记录数检查 | P2 |

## 实体页（Entities）

### 核心维度表
- [[salesclaw/knowledge/entities/doctors]] - 医生表（HCP）
- [[salesclaw/knowledge/entities/hospitals]] - 医院表
- [[salesclaw/knowledge/entities/dim_products]] - 品种表（静态层）
- [[salesclaw/knowledge/entities/dim_reps]] - 销售代表表
- [[salesclaw/knowledge/entities/dim_territories]] - 区域表（组织层级）
- [[salesclaw/knowledge/entities/dim_hospital_access]] - 医院准入表

### 事实表
- [[salesclaw/knowledge/entities/fct_prescription_flow]] - 处方流向表
- [[salesclaw/knowledge/entities/fct_expense_c2]] - 费用明细表

### 关系与事件
- [[salesclaw/knowledge/entities/ontology_objects]] - 统一实体表
- [[salesclaw/knowledge/entities/object_links]] - 关系链接表（核心）
- [[salesclaw/knowledge/entities/object_events]] - 事件记录表
- [[salesclaw/knowledge/entities/time_series_data]] - 时序数据表

### 其他业务表
- [[salesclaw/knowledge/entities/compliance_alerts]] - 合规告警表
- [[salesclaw/knowledge/entities/sales_targets]] - 销售目标表
- [[salesclaw/knowledge/entities/visit_records]] - 拜访记录表

## 概念页（Concepts）

### 归因与告警
- [[salesclaw/knowledge/concepts/three-layer-attribution]] - 三层归因操作手册
- [[salesclaw/knowledge/concepts/expense-red-green]] - 费用红黄绿灯标准（DeltaWeight）

### 分析方法
- [[salesclaw/knowledge/concepts/prescription-penetration]] - 处方渗透率分析
- [[salesclaw/knowledge/concepts/territory-coverage]] - 区域覆盖分析
- [[salesclaw/knowledge/concepts/product-flow]] - Product Flow分析
- [[salesclaw/knowledge/concepts/hcp-influence-network]] - HCP影响力网络
- [[salesclaw/knowledge/concepts/market-penetration]] - 市场渗透率预测
- [[salesclaw/knowledge/concepts/compliance-pattern]] - 合规模式挖掘

## 工具说明（Tools）

| 工具 | 文件 | 功能 |
|------|------|------|
| 业务路由器 | `tools/ask.py` | 意图识别 + 10大业务模块查询 |
| 推理引擎 | `tools/inference.py` | 三层归因诊断会话 |
| 数据库连接 | `tools/db.py` | 连接池管理 |
| 初始化 | `tools/init_mysql.py` | 从 init.sql 初始化 |
