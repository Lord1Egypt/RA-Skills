# Domain → 文档路径索引

各 domain 的主要业务文档路径，供 Phase 2 文档加载时快速定位。
**仅收录 `docs/specs/` 下已有独立文档的 domain**。

> 本索引为 `SKILL.md` Phase 2 的补充参考，核心契约理解流程以 `SKILL.md` 为准。

| domain | 入口文档 | 说明 |
|--------|---------|------|
| `datamodel` | `/docs/specs/datamodel/guide.md` | 数据模型查询 |
| `tabularmodel` | `/docs/specs/tabularmodel/guide.md` | 表格模型管理 |
| `datamining` | `/docs/specs/datamining/guide.md` | 数据挖掘（ETL / 因果图 / 作业流） |

## datamodel

MQL 查数接口相关文档：

| 路径 | 说明 |
|------|------|
| `/docs/specs/datamodel/guides/query-data-by-mql.md` | MQL 取数使用指南（请求/响应/调用方式） |
| `/docs/specs/datamodel/mql/mql.md` | MQL 语法总览（dims/metrics/from/filter/sort/with） |
| `/docs/specs/datamodel/mql/common-types.md` | 公共类型（DataType/AggType/ParamValue/DataTable/ParquetResult） |
| `/docs/specs/datamodel/mql/references/cal-measures.md` | 计算指标（CAL_MEASURE / mdxExpr） |
| `/docs/specs/datamodel/mql/references/with-column.md` | 派生列（COLUMN / sqlExpr） |
| `/docs/specs/datamodel/mql/references/with-measure.md` | 派生度量（MEASURE / ref + aggType） |

## tabularmodel

数据模型管理相关文档：

| 路径 | 说明 |
|------|------|
| `/docs/specs/tabularmodel/mdl/mdl.md` | MDL 结构总览 |
| `/docs/specs/tabularmodel/mdl/common-types.md` | MDL 公共类型 |
| `/docs/specs/tabularmodel/mdl/references/measures.md` | 度量定义 |
| `/docs/specs/tabularmodel/mdl/references/dimensions.md` | 维度定义 |
| `/docs/specs/tabularmodel/mdl/references/columns.md` | 列定义 |
| `/docs/specs/tabularmodel/mdl/references/views.md` | 视图定义 |
| `/docs/specs/tabularmodel/mdl/references/relations.md` | 关系定义 |
| `/docs/specs/tabularmodel/mdl/references/calc-members.md` | 计算成员 |
| `/docs/specs/tabularmodel/mdl/references/named-sets.md` | 命名集 |
| `/docs/specs/tabularmodel/mdl/references/metrics-sets.md` | 指标集 |
| `/docs/specs/tabularmodel/mdl/references/parameters.md` | 参数定义 |
| `/docs/specs/tabularmodel/mdl/references/pre-aggregates.md` | 预聚合 |
| `/docs/specs/tabularmodel/mdl/references/obj-trees.md` | 对象树 |
| `/docs/specs/tabularmodel/mdl/references/table-relationships.md` | 表关系 |

## datamining

数据挖掘相关文档：

| 路径 | 说明 |
|------|------|
| `/docs/specs/datamining/etl/etl.md` | ETL 结构总览 |
| `/docs/specs/datamining/etl/references/node-structure.md` | ETL 节点结构 |
| `/docs/specs/datamining/etl/references/sql-node.md` | SQL 节点 |
| `/docs/specs/datamining/etl/references/smartbi-query.md` | Smartbi 查询节点 |
| `/docs/specs/datamining/etl/references/python-script.md` | Python 脚本节点 |
| `/docs/specs/datamining/etl/references/jdbc-datasource.md` | JDBC 数据源 |
| `/docs/specs/datamining/etl/references/jdbc-datatarget.md` | JDBC 数据目标 |
| `/docs/specs/datamining/etl/references/link.md` | ETL 连接 |
| `/docs/specs/datamining/etl/references/rules.md` | ETL 规则 |
| `/docs/specs/datamining/etl/references/examples.md` | ETL 示例 |
| `/docs/specs/datamining/jobflow/jobflow.md` | 作业流总览 |
| `/docs/specs/datamining/jobflow/references/node-structure.md` | 作业流节点结构 |
| `/docs/specs/datamining/jobflow/references/etl-job.md` | ETL 作业节点 |
| `/docs/specs/datamining/jobflow/references/start-job.md` | 启动作业节点 |
| `/docs/specs/datamining/jobflow/references/link.md` | 作业流连接 |
| `/docs/specs/datamining/jobflow/references/rules.md` | 作业流规则 |
| `/docs/specs/datamining/jobflow/references/examples.md` | 作业流示例 |
| `/docs/specs/datamining/casualgraph/casualgraph.md` | 因果图总览 |
| `/docs/specs/datamining/casualgraph/references/casual-node.md` | 因果节点 |
| `/docs/specs/datamining/casualgraph/references/casual-link.md` | 因果连接 |
| `/docs/specs/datamining/casualgraph/references/differences.md` | 因果图与作业流差异 |
| `/docs/specs/datamining/casualgraph/references/top-level.md` | 顶级结构 |
| `/docs/specs/datamining/casualgraph/references/examples.md` | 因果图示例 |

## 使用方式

Phase 2 `describe` 输出中，若 `description` 包含 `[说明](/docs/specs/...)` 形式的链接，直接用 `smartbi doc /docs/specs/... --agent` 加载。

本索引用于在 `description` 中无显式链接时，根据 domain 推断可能存在的文档路径。加载时仍应使用 `smartbi doc` 验证路径可用性。
