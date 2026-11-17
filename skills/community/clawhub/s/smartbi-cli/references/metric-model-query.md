# 新旧指标模型的资源发现与取数

本参考是 `smartbi-cli` 数据查询场景的分支，不是独立 Skill。先核对目标环境的目录与查询契约；资源目录中的类型、查询请求中的模型类型和 AI 问数选中资源的类型各有用途，不能随意互换。

| 用户所指 | 目录资源类型 | 直接取数路径 |
|---|---|---|
| 数据模型 | `AUGMENTED_DATASET` | `data-model-query.md` 的模型元数据 → MQL/只读 SQL |
| 新指标模型 | `MT_MODEL` | 先解析该指标模型关联的可查询数据模型；当前环境可从其 `MT_DATAMODELS` 目录定位 `AUGMENTED_DATASET`，再按目标指标和维度选择模型取数。部署提供指标模型专用查询接口时，先核实契约再使用。 |
| 旧指标模型 | `TABULAR_DATASET` | `tabularmodel.getSimpleDataSet`/`getDataSet` 元数据 → `tabularmodel.queryDataSetDataIterator` |

用户明确问“数据模型”时只枚举 `AUGMENTED_DATASET`；问“指标模型”时分别枚举 `MT_MODEL` 和 `TABULAR_DATASET`；泛问“模型/可用模型”，或在模型问数语境下问“数据资产”时，分别枚举三类并标明分类。使用 `catalogtree.listCatalogElementsByResourceType` 的单类型请求；当前已有部署的多类型合并枚举结果少于逐类枚举，不能未对账就以合并结果宣称完整。目录返回的 `MT_MODEL` 是新指标模型资源，不是增强数据集 ID；`datamodel.getDataModelTrees` 不支持该 ID，并不意味着该指标模型不能取数。目录可见也不证明任何具体指标已可查询，需要完成下面的资源映射与字段校验。

## 旧指标模型直接取数

用已核实的 `TABULAR_DATASET` ID 调 `tabularmodel.getSimpleDataSet`，请求体 `{"req":{"dataSetId":"<MODEL_ID>"}}`。从返回的 `dimensions`、`measures`、`views`、`parameters` 解析问句；需要完整定义时再调 `tabularmodel.getDataSet`。按当前 `describe` 构造 `tabularmodel.queryDataSetDataIterator` 的 `{"req":{"dataSetId":"<MODEL_ID>","requestId":"<REQUEST_ID>","query":{"rows":["<已核实的字段名>"]}}}`，筛选、分组、排序及结果迭代器均以该接口契约为准。已在一种模型上验证只读查询返回结果；不能套用增强数据集的 MQL/SQL 请求体、`dataTable` 行数规则或凭一行结果推断所有模型都可用。

## 新指标模型直接取数

先对已核实的 `MT_MODEL` ID 使用当前目录契约读取子资源。若有 `MT_DATAMODELS`，进入其下选择包含用户所需指标和维度的 `AUGMENTED_DATASET`，再按 `data-model-query.md` 取元数据并执行只读 MQL/SQL。不要默认选第一个，也不要把 `MT_MODEL` 目录 ID 伪装为 `AUGMENTED_DATASET`。已在一个指标模型下验证关联数据模型的 MQL 可以返回数据；其他指标模型可能因权限、未生成关联模型或部署能力不同需要另行查证。若当前环境提供专用指标模型查询接口，核对其模型类型与请求契约后可直接走该接口；找不到有效映射或接口时如实说明具体限制，不泛称新指标模型不支持取数。

## AI 问数

用户明确要求 AI 问数时进入 `sessions-and-logs.md` 的会话路径，按部署实际接受的资源类型选中对象，不把直接取数要求自动转为 AI。当前环境的已训练资源清单可出现 `AUGMENTED_DATASET` 和 `TABULAR_DATASET`；一个新指标模型的关联数据模型也在该清单中，但 `MT_MODEL` 根资源未直接出现。先核实新指标模型到 AI 可用资源的映射或专用入口，再传真实资源 ID/type；目录发现成功或训练清单命中仅证明候选资源存在，不代替实际问数执行与结果校验。不同部署可以有其他 AI 问数契约，按当前 `describe` 核实。
