# SKILL.md - SalesClaw v3.0

医药销售业务本体数据库 v3.0（138张表）。

**核心理念**：用户问题 → NL2SQL → SQL 模板复用 → 归因分析

---

## 数据库连接

| 项目 | 值 |
|------|---|
| Host | `localhost` |
| Port | `3306` |
| User | `ontology` |
| Database | `salesclaw` |
| 连接管理 | `tools/db.py`（`get_conn()` / `query_all()` / `query_one()`）|

```python
from db import query_all, query_one
rows = query_all("SELECT * FROM dim_products LIMIT 5")
```

---

## 知识库

**路径**: `~/.openclaw/workspace/skills/salesclaw/knowledge/`

```
knowledge/
├── index.md                      ← 总索引
├── entities/                     ← 138张表的字段说明（doctors/hospitals/dim_products/...）
├── concepts/                     ← 业务概念（three-layer-attribution / expense-red-green / ...）
└── sql_templates/               ← 沉淀的 SQL 模板（NL2SQL 复用）
```

---

## SQL 模板（高频问题沉淀）

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

---

## 三层归因模型（归因分析标准方法论）

### 结构归因（What - 规模维度）

**问题**：失血发生在哪个结构单元？

分析方向：
- 品种维度：哪个品种贡献主要失血？
- 省区维度：大区 → 省区 → 地区逐层下探
- 时间维度：定位断崖点（哪个月开始下滑）
- 医院层级：一级/二级/三级分层

```sql
-- 定位省区处方量贡献（结构归因第一步）
SELECT province,
       SUM(prescription_volume) as vol,
       SUM(prescription_volume) / SUM(SUM(prescription_volume)) OVER () * 100 as share_pct
FROM fct_prescription_flow
WHERE product_id = :product_id
GROUP BY province
ORDER BY vol DESC;
```

### 行为归因（Why - 驱动维度）

**问题**：结构单元的失血是因为什么行为变化？

分析方向：
- 覆盖行为：流向医院数是否下降？
- 拜访行为：代表拜访频次是否下降？
- 竞品行为：竞品是否有学术活动/准入变化？
- 通道行为：医院准入/招标是否有变化？

### 决策归因（Who - 责任维度）

**问题**：谁（哪个代表/哪条线）应对变化负责？

分析方向：
- 个人分层：Top/Bottom 代表分层对比达成率
- 分管人责任：区域经理覆盖效率是否达标
- 组织连带：区域负责人是否尽到管理责任

---

## DeltaWeight 计算规范（费用告警标准）

```
DeltaWeight = 某省区某费用类型占比 - 全国该费用类型占比

省区费用占比 = 该省该费用类型金额 / 该省费用总额
全国费用占比 = 该费用类型金额 / 全国费用总额
```

| 告警级别 | 阈值 | 响应时间 |
|---------|------|---------|
| 🔴 红灯 | DeltaWeight ≥ 30ppt | 24h |
| 🟡 黄灯 | DeltaWeight ≥ 15ppt | 1周 |

---

## 诊断会话表（归因推理引擎）

| 表 | 用途 |
|------|------|
| `fct_diagnosis_session` | 每次告警触发一次诊断会话 |
| `fct_reasoning_step` | 每层归因的每一步记录 |
| `dim_diagnosis_rules` | 诊断规则模板（5条预置）|
| `conclusions` | 归因结论输出 |

---

## 核心关系边（星型拓扑，以 ontology_objects 为中心）

```
ontology_objects.id（中心节点）
    ↓
    ├── object_links（关系边：代表←→医生、代表←→医院、竞品关系）
    ├── object_events（事件边：拜访、学术活动、处方事件）
    └── time_series_data（时序边：处方量趋势、费用趋势）
```

---

## 工具说明（Tools）

| 工具 | 文件 | 功能 |
|------|------|------|
| 业务路由器 | `tools/ask.py` | 意图识别 + 10大业务模块查询 |
| 推理引擎 | `tools/inference.py` | 三层归因诊断会话（structure→behavior→decision，含置信度传播+反例探测+Early Exit）|
| 知识 API | `tools/knowledge.py` | 统一知识消费：load_sql_template / load_entity_schema / load_concept / render_sql |
| 数据库连接 | `tools/db.py` | 连接池管理（超时重试+降级+错误透出）|
| 初始化 | `tools/init_mysql.py` | 从 init.sql 初始化 |

> **使用方式**：用户问题 → NL2SQL → 常见问题沉淀为 SQL 模板；复杂推理链路（如三层归因）由工具封装。
