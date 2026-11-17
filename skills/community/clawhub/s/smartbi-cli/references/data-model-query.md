# Direct SmartBI model query contract

Use the target environment's registered OpenAPI operations and current `describe` contract. Examples below are request shapes, not customer model definitions; replace every model, source, field and filter using current metadata and the user's question.

## Discovery and metadata

When the model, route and scope are already clear, use this guide directly; load `query-routing.md` only for unresolved routing, discovery, scope, completeness, or semantic-validation decisions. Prefer MQL for supported model dimensions and measures; use read-only SQL when explicitly requested or MQL is unsuitable and SQL contracts and semantic metadata are sufficient. No model training or conversation is required. First resolve the **business resource** in the catalog unless a model ID is already verified. `smartbi list` enumerates registered API operations, not models. Use a confirmed catalog search for a named business topic; list by resource type only when enumeration is needed or search is unavailable. Then use the verified model ID for metadata and query. Follow the shortest verified chain: call directly when the operation contract is already confirmed for the current environment and version; otherwise describe the known operation, load docs only for unresolved contract details, and discover operations only when the operation key is unknown. Prefer a registered Overview that supplies the needed metadata; reuse sufficient metadata already read in this task. Field trees and full definitions fill gaps. The SQL overview below is one such source, not a mandatory CGI probe. The following commands are **alternatives/conditional steps, not a sequence to run in full**:

```bash
smartbi call catalogtree.searchCatalogTree \
  -d @model-search.json --profile <PROFILE> --agent

smartbi call catalogtree.listCatalogElementsByResourceType \
  -d @model-list.json --profile <PROFILE> --agent

smartbi call datamodel.cgi.getSqlModelOverview \
  -d @sql-overview.json --profile <PROFILE> --agent

smartbi call datamodel.getDataModelTrees \
  -d @field-tree.json --profile <PROFILE> --agent
```

This file's MQL/SQL chain is for `AUGMENTED_DATASET`; the broader model discovery and `MT_MODEL`/`TABULAR_DATASET` query paths are in `metric-model-query.md`. A `MT_MODEL` catalog ID is not an augmented-dataset ID; resolve its associated queryable model or deployment-specific query contract before direct retrieval. Model IDs and types are environment-specific. When the current search contract supports `purviewType`, set the appropriate explicit permission (for ordinary visible resources, commonly `REF`); do not assume the omitted-value behavior is identical across deployments. If a targeted search is empty, verify the permission and search mode before concluding that no model exists. `catalogtree.searchCatalogElementsByAlias` is an exact alias search; its hit can be a same-named folder rather than a model. Always inspect the returned resource type and ID before requesting model metadata. Use type enumeration when the user asks which models are available, or as a bounded fallback when targeted search fails.

The field-tree API `datamodel.getDataModelTrees` requires the plural array form:

```json
{"modelIds": ["<MODEL_ID>"]}
```

`<MODEL_ID>` must be a nonempty, catalog-verified ID. The `suggestedCall` value `{"modelIds":[]}` is a schema placeholder and yields no model metadata; do not execute it. If no ID is available, search the catalog instead of asking the business user to supply one. Check each catalog operation against the current `describe` contract before first use.

A field-tree response can also be `[]` for a verified, nonempty model ID; this alone does not establish that the model is missing or inaccessible. If the model definition is needed, try the registered `tabularmodel.getDataSet` with that ID and inspect the relevant views, dimensions, measures and relations. Do not turn this fallback into a routine full-definition fetch when the field tree already supplies enough metadata.

The SQL overview operation may not be registered on every installation; verify it with `describe` before calling it.

## SQL

Operation: `datamodel.queryDataBySql`
HTTP: `POST /api/v1/datamodel/datamodel/query-data-by-sql`
Request body: an outer `req` object containing:

```json
{
  "req": {
    "modelId": "<MODEL_ID>",
    "modelType": "<MODEL_TYPE>",
    "sql": "SELECT year(\"<DATE_COLUMN>\") AS \"年\", SUM(\"<ADDITIVE_MEASURE>\") AS \"<ADDITIVE_MEASURE>\" FROM \"<LOGICAL_TABLE>\" WHERE \"<DATE_COLUMN>\" >= DATE '2025-01-01' AND \"<DATE_COLUMN>\" < DATE '2026-01-01' GROUP BY year(\"<DATE_COLUMN>\") ORDER BY \"年\" LIMIT 100",
    "params": [],
    "extraTables": [],
    "showDataTable": true
  }
}
```

`sql` is DuckDB SQL over the model's available logical tables. It must be read-only. Use the model overview or field tree to determine exact logical table/column names and joins; do not use underlying physical database table names. `params` contains model parameters as `{name, values}`; omit or leave empty only when the model has no global parameters. `extraTables` is for explicitly supported additional tables and must not be used to bypass model governance.

The SQL aggregation shown is valid only for a confirmed additive measure. Resolve the underlying column and model formula before using SUM; semantic time levels are not necessarily stored columns. The illustrative date range must be replaced by the requested range.

### Resolving SQL FROM

The SQL `FROM` value is a data-model logical table or view alias, not a physical database table name. Derive it from the current model's metadata. In some verified models this is the same source/measure-folder alias exposed by `datamodel.getDataModelTrees` and used as `mql.from`; this is a model-specific observation, not a universal alias.

If `DAO_ID_IS_NULL` occurs for an otherwise valid read-only SQL shape, first verify that the logical `FROM` resolves in the model. Do not start renaming columns or inventing physical table names. If the metadata does not expose a usable logical source, stop and report that the SQL model metadata is insufficient.

Semantic time levels such as `年`, `年季`, and `年月` may not be physical columns of the logical fact table. When the metadata identifies a date column, derive the requested level with DuckDB functions such as `year("<DATE_COLUMN>")` rather than assuming a same-named base column.

## MQL

Operation: `datamodel.queryDataByMql`
HTTP: `POST /api/v1/datamodel/datamodel/query-data-by-mql`
Request body: an outer `req` object containing:

```json
{
  "req": {
    "modelId": "<MODEL_ID>",
    "modelType": "<MODEL_TYPE>",
    "mql": {
      "from": "<MODEL_SOURCE>",
      "dims": ["年"],
      "metrics": ["<ADDITIVE_MEASURE>"],
      "dimFilter": "\"年\" >= 2022",
      "metricFilter": "",
      "sort": [["年", "ASC"]],
      "limit": 100,
      "offset": 0
    },
    "params": [],
    "showDataTable": true
  }
}
```

Use only dimensions, metrics, source names, and filters confirmed by the field tree/model metadata. Preserve the dimension's hierarchy/path where the contract requires it (for example `客户维.分公司名称` rather than an unqualified technical field name). A physical table such as `dim_cust_info` is not a verified MQL `from` or SQL logical `FROM` merely because it appears in model internals. `mql.with` supports calculated columns, base measures, and calculated measures; calculated-measure expressions use MDX semantics, not SQL syntax.

Construct `dimFilter` using the current MQL contract and verified dimension paths and value types. In a verified model, string comparisons used single-quoted values and hierarchy-qualified fields, with `AND` between conditions; do not generalize one model's names or assume every filter expression is accepted. For a value whose presence or encoding is uncertain, a bounded unfiltered grouping of the relevant dimension can establish candidate values before a filtered query. Do not make that extra call when values are already verified; if a filtered result is empty and the value domain was not checked, distinguish “zero returned rows” from a proven absence of matching business data.

When the field tree cannot establish a measure formula, raw-column mapping, relation, parameter, or usable source alias, discover and describe `tabularmodel.getDataSet` if available. Its request is `{"req":{"dataSetId":"<MODEL_ID>"}}`; inspect only the relevant parts of views, relations, measures and parameters. In a verified model, a physical `views[*].name` failed as SQL `FROM` while its `views[*].alias` succeeded; use the alias only after checking the model's query contract. The full definition is an on-demand supplement, not a routine prerequisite. Do not treat hidden supporting measures as user-facing fields merely because the full definition includes them.

For model-level calculated measures spanning multiple sources, use the model's formula and verified contract. `from` is optional in the MQL contract; do not invent a single fact-table source for a root-level measure. Validate its components at the same filters and grain. A formula explicitly defined by the model takes precedence over a calculation inferred from its business name.

An aggregation enum in the schema is not proof it executes on this model/server. If a combined `with` request fails, isolate the suspected definition with a bounded diagnostic call; do not retry the entire failing bundle repeatedly or conclude all aggregation types are unavailable. Never silently replace a failed percentile/median with an average. Where independent raw detail cannot be obtained, report statistical identity checks separately from full numerical verification.

Preserving a model definition does not prove its business label is correct: a measure named as an amount may actually use COUNT. Disclose conflicts with the requested business meaning and resolve the intended measure before presenting a monetary answer; do not silently change the model aggregation.

For median/percentile questions, verify the statistical convention when it affects the answer (e.g. even-sized median and continuous vs discrete percentile). Runtime success and min/max bounds do not prove the expected convention. If a complete bounded raw sample is available, calculate independently and disclose any discrepancy; otherwise qualify the result instead of calling it verified. Local fallback must state the method and completeness, not masquerade as native MQL success.

When a source is needed, `mql.from` is the logical model-view/source alias that contains the requested measures. Select it from the current field tree; it is not automatically the model name or model alias. Model-level calculated measures follow the optional-source rule above. If multiple candidate aliases exist, choose the one that contains the target measures. Retry at most once with another candidate explicitly present in the same metadata response; do not guess names.

## Slicing validation

Before grouping a measure by a dimension from another view or fact source, use already available model metadata to check source ownership, relation direction/cardinality and whether the dimension can filter the measure at the requested grain. If the field tree cannot establish this, read only the relevant `getDataSet` definition on demand. Lack of a *direct* relation alone is not proof that MQL is invalid: a verified shared dimension or bridge can be valid. Conversely, the mere presence of both fields in one model does not prove that slicing is valid. If no sound path is established, do not send a speculative grouped MQL. Use read-only SQL only when logical views, join keys, row grain and aggregation semantics are verified; aggregate at the correct fact grain before any join that could fan out. Otherwise explain the unresolved model relationship rather than inventing a join.

After a grouped query, repeated identical values across distinct categories are a warning, particularly for a cross-fact slice; equal values can also be real data. If mutually exclusive groups each repeat an already verified overall total, the slice is inconsistent and must not be delivered; no duplicate total query is needed. Otherwise check whether the filter actually applies and whether the grouped result is consistent with the model's relationship. Withhold a suspect business conclusion until verified. For an additive metric split into mutually exclusive, exhaustive groups, reconcile the complete grouped sum with a same-scope, same-period total, reusing a total already obtained in this task when valid. Preserve null/unclassified groups and use precision-appropriate tolerance. Do not sum stock values across time, distinct counts, ratios or overlapping groups merely to force this check. A failed reconciliation blocks that grouped conclusion; a passed one does not independently prove each group's source value. Do not promote a diagnostic SQL rewrite to the answer without the same checks.

Also check the *visible dimension tuple*, not just whether metric values repeat. A query may return multiple rows with the same displayed dimension values; those rows are not distinct business groups. Before reporting a group total, establish whether the metric is additive across those rows and the complete row sum reconciles with a separate same-filter total (or another verified equivalent). Otherwise preserve the returned rows and state that the requested visible grain has not been established; do not silently deduplicate or present one row as the group total.

## Result handling

Ordinary queries target the complete result at the requested filters and grain, and can deliver validated `dataTable` rows directly; CSV or another file is optional. Unless the user asks for TopN, first N or a sample, `limit` is a request batch size rather than a delivery cap. Continue full pages until completion is established; follow `query-routing.md` when result size or runtime prevents completion. Count the actual rows in `dataTable.data` for each page. Do not assume `rowCount` equals that page size: some MQL responses return a larger count for a limited page. Establish rowCount semantics from the current contract/observed pagination before using it as a total or consistency check. Check current `describe` for transport capabilities: the verified MQL and SQL contracts declare `streaming: false` and `application/json`. Client-side page delivery is possible, but neither CLI chunking nor Baize SSE establishes native row streaming for these operations.

Both operations return a result with modelId, s3Url, rowCount and optional dataTable. Check CLI ok and business success/error. When s3Url is non-empty, download using the supported SDK contract and verify actual bytes/file format (do not assume Parquet from the suffix). If s3Url is absent, the actual `dataTable.data` rows can serve as the complete result of a bounded query only after its requested range and pagination end are verified; `rowCount` alone cannot establish this. If the page reaches `limit`, continue with stable pagination until an end condition is verified; if completion cannot be established, report the delivered range as partial. Validate ratio/time-grain semantics per query-routing.md before aggregating or merging results.

Within one task, reuse model metadata and confirmed operation contracts while the environment, identity and model definition remain applicable; a full model definition is not a default prerequisite and is not persisted as a Skill cache. Combine compatible measures in one query only when source, filter, time grain and aggregation semantics align. If a combined query fails, isolate the failing measure rather than treating every measure as unsupported. Query latency and tool timeout diagnosis follow `troubleshooting.md`; no historical duration is a cross-environment baseline.
