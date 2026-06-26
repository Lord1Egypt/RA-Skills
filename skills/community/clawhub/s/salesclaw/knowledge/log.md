# SalesClaw 知识库操作日志

## 2026-05-18

### 初始化编织
- **操作**: Initial knowledge base bootstrap
- **来源**: salesclaw.db schema introspection + 数据观测
- **创建/更新**:
  - `salesclaw/SALESCLAW_SCHEMA.md` - 规范定义 + 3条关键设计决策
  - `salesclaw/entities/` - 14个实体页
  - `salesclaw/concepts/` - 6个概念页（行业分析方法）
  - `index.md` - 知识库索引
  - `log.md` - 本日志
- **摘要**: 基于 salesclaw.db 真实 schema 构建完整知识库

### 实体页清单
- `doctors.md` - 医生表
- `hospitals.md` - 医院表
- `products.md` - 产品表
- `sales_reps.md` - 销售代表表
- `sales_targets.md` - 销售目标表
- `visit_records.md` - 拜访记录表（含无外键设计说明）
- `sales_flows.md` - 销售目标Flow表（非产品流向）
- `customer_compliances.md` - 医生时序指标表（⚠️非费用表）
- `object_links.md` - 关系链接表（核心！）
- `object_events.md` - 事件记录表
- `ontology_objects.md` - 统一实体表
- `time_series_data.md` - 时序数据表
- `compliance_alerts.md` - 合规告警表
- `action_proposals.md` - 动作提案表
- `execution_logs.md` - 执行日志表

### 概念页清单
- `prescription-penetration.md` - 处方渗透率分析
- `hcp-influence-network.md` - HCP影响力网络推理
- `territory-coverage.md` - 区域覆盖分析
- `product-flow.md` - Product Flow 分析
- `market-penetration.md` - 市场渗透率预测
- `compliance-pattern.md` - 合规模式挖掘

---

*格式：日期 / 操作类型 / 来源 / 创建文件 / 摘要*
