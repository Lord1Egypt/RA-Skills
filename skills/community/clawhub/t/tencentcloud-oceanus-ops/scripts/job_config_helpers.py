#!/usr/bin/env python3
"""Job config helper utilities — constants, SQL/JAR payload builders, draft confirmation.

Extracted from job_development.py for better modularity.

Provides:
- Job type / ResourceRef type constants
- SQL encoding, placeholder parsing, MetadataV1 building
- JAR ProgramArgs building (deprecated)
- Job type detection and requirement
- SQL input reading, resource ref parsing/validation
- Draft summary formatting and confirmation gate
"""

import base64
import json
import re
import sys
import tempfile

from client import (
    call_api,
    error_response,
    require_confirmation,
)


# ═══════════════════════════════════════════════════════════════════════════
# Job Type Constants
# ═══════════════════════════════════════════════════════════════════════════

JOB_TYPE_SQL = 1
JOB_TYPE_JAR = 2

_JOB_TYPE_NAMES = {JOB_TYPE_SQL: "SQL", JOB_TYPE_JAR: "JAR"}


# ═══════════════════════════════════════════════════════════════════════════
# ResourceRef Usage Type Constants (作业引用资源时的"用途"分类)
# ═══════════════════════════════════════════════════════════════════════════
#
# IMPORTANT: ResourceRef.Type and Resource.Type are TWO DIFFERENT enums.
#
# Resource.Type — describes the resource artifact itself (set when uploading):
#     1 = jar package         (RESOURCE_TYPE_JAR)
#     2 = config / dependency (RESOURCE_TYPE_DEPENDENCY)
#   See `resource_management.py` for the resource-side constants.
#
# ResourceRef.Type — describes how a job consumes a resource (set in the
# job draft / job config payload). Authoritative backend definition:
#     RESOURCE_REF_USAGE_TYPE_MAIN           = 1
#     RESOURCE_REF_USAGE_TYPE_DEPENDENCY     = 2
#     RESOURCE_REF_USAGE_TYPE_DEPENDENCY_JAR = 0
#
#     0 = DEPENDENCY_JAR — 辅助 jar 包（**非主程序**），例如 UDF jar、
#                          connector jar、其它依赖 jar。SQL / JAR 作业
#                          引用 **jar 包** 时统一使用 Type=0。
#     1 = MAIN           — JAR 作业的主程序包。**仅 JAR 作业** 且必须
#                          恰好一个；SQL 作业不允许出现。
#     2 = DEPENDENCY     — 非 jar 的依赖文件（配置文件 / 资源文件，例如
#                          `.properties`、`.json`、`.conf`）。SQL / JAR
#                          作业引用 **配置文件** 时使用 Type=2。
#
# 选 Type 的简单决策树（针对单个 ResourceRef 条目）：
#   - 它是 JAR 作业的"主程序包"吗？→ Type=1 (MAIN)
#   - 它是一个 jar 包（非主程序）？→ Type=0 (DEPENDENCY_JAR)
#   - 它是配置文件 / 非 jar 资源？→ Type=2 (DEPENDENCY)
#
# Do NOT mix Resource.Type with ResourceRef.Type:
#   - 一个 UDF jar：上传时 Resource.Type=1（jar 包），在作业中引用时
#     ResourceRef.Type=0 (DEPENDENCY_JAR)。
#   - 一个 `.properties` 配置：上传时 Resource.Type=2（配置文件），在
#     作业中引用时 ResourceRef.Type=2 (DEPENDENCY)。

RESOURCE_REF_TYPE_DEPENDENCY_JAR = 0
RESOURCE_REF_TYPE_MAIN = 1
RESOURCE_REF_TYPE_DEPENDENCY = 2
_RESOURCE_REF_TYPE_NAMES = {
    RESOURCE_REF_TYPE_DEPENDENCY_JAR: "DEPENDENCY_JAR",
    RESOURCE_REF_TYPE_MAIN: "MAIN",
    RESOURCE_REF_TYPE_DEPENDENCY: "DEPENDENCY",
}
_RESOURCE_REF_TYPE_VALID = (
    RESOURCE_REF_TYPE_DEPENDENCY_JAR,
    RESOURCE_REF_TYPE_MAIN,
    RESOURCE_REF_TYPE_DEPENDENCY,
)


# ═══════════════════════════════════════════════════════════════════════════
# SQL encoding & placeholder parsing
# ═══════════════════════════════════════════════════════════════════════════


def encode_sql(sql_code):
    """Encode plain-text SQL to base64 string for API requests."""
    return base64.b64encode(sql_code.encode("utf-8")).decode("ascii")


# ── SQL ${var} placeholder parsing ─────────────────────────────────────────
#
# Oceanus backend supports three placeholder forms (parse_sql_service.go:42-45):
#   1. ${name}           — no default
#   2. ${name:default}   — new form, default after colon
#   3. ${name}:default   — legacy form, default after closing brace
#
# We replicate that in Python and split per-table so that each variable entry
# in MetadataV1 is associated with the table whose WITH clause used it.
#
# Output of `_extract_sql_variables(sql_code)` is a list of:
#   {table, key, placeholder, default_value, table_type}
# where `table_type` follows METADATA_TABLE_VARIABLE_TYPE_*:
#   1 = META_TABLE      (referenced metastore table — not yet supported here)
#   2 = TEMPORAL_TABLE  (CREATE [TEMPORARY] TABLE ... — the common case)
#   3 = CDAS            (CREATE CATALOG / CREATE DATABASE AS — not yet supported)

# Match a single CREATE [TEMPORARY] TABLE <name> ( ... ) WITH ( ... )
_CREATE_TABLE_WITH_RE = re.compile(
    r"CREATE\s+(?:TEMPORARY\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
    r"(?:`([^`]+)`|([A-Za-z_][\w\.]*))"   # group(1) backticked OR group(2) bare
    r"\s*\([^;]*?\)\s*WITH\s*\((?P<with_body>[^;]*?)\)\s*;",
    re.IGNORECASE | re.DOTALL,
)

# Inside a WITH body: 'key' = '<value>'
_WITH_KV_RE = re.compile(
    r"['\"]([^'\"]+)['\"]\s*=\s*['\"]([^'\"]*)['\"]",
)

# Three placeholder forms inside a WITH value:
_PH_NEW = re.compile(r"\$\{([^}:]+):([^}]+)\}")    # ${name:default}
_PH_LEGACY = re.compile(r"\$\{([^}]+)\}:(\S+)")    # ${name}:default
_PH_BARE = re.compile(r"\$\{([^}:]+)\}")            # ${name}


def _scan_placeholders_in_value(value):
    """Yield (placeholder, default_value) tuples found in a WITH value."""
    seen_spans = []

    def _overlaps(span):
        for s, e in seen_spans:
            if not (span[1] <= s or span[0] >= e):
                return True
        return False

    for m in _PH_NEW.finditer(value):
        if _overlaps(m.span()):
            continue
        seen_spans.append(m.span())
        yield m.group(1).strip(), m.group(2).strip()
    for m in _PH_LEGACY.finditer(value):
        if _overlaps(m.span()):
            continue
        seen_spans.append(m.span())
        yield m.group(1).strip(), m.group(2).strip()
    for m in _PH_BARE.finditer(value):
        if _overlaps(m.span()):
            continue
        seen_spans.append(m.span())
        yield m.group(1).strip(), ""


def extract_sql_variables(sql_code):
    """Parse SQL to find every ${var} occurrence and the table it belongs to.

    Returns a list of dicts: {table, key, placeholder, default_value, table_type}.
    Only `CREATE [TEMPORARY] TABLE` blocks are scanned.
    """
    out = []
    for m in _CREATE_TABLE_WITH_RE.finditer(sql_code):
        table = m.group(1) or m.group(2) or ""
        with_body = m.group("with_body")
        for kv in _WITH_KV_RE.finditer(with_body):
            key, value = kv.group(1), kv.group(2)
            for placeholder, default_value in _scan_placeholders_in_value(value):
                out.append({
                    "table": table,
                    "key": key,
                    "placeholder": placeholder,
                    "default_value": default_value,
                    "table_type": 2,
                })
    return out


def _resolve_variables_via_api(region, workspace_id, placeholders, verbose=False):
    """Call DescribeVariables and return {placeholder_name: variable_item}.

    Returns ({} ,error_response_dict) on failure so callers can short-circuit.
    """
    if not placeholders:
        return {}, None
    names = sorted({p for p in placeholders})

    result = call_api("DescribeVariables", {"WorkSpaceId": workspace_id}, region)
    if not result.get("success"):
        return {}, result

    var_set = (result.get("data") or {}).get("VariableSet", []) or []
    by_name = {v.get("Name", ""): v for v in var_set}

    resolved = {}
    for n in names:
        v = by_name.get(n)
        if v is not None:
            resolved[n] = v
    return resolved, None


def _build_metadata_v1(sql_code, resolved_variables, reference_tables=None,
                       catalogs=None):
    """Build MetadataV1.Metadata from parsed SQL + resolved API data.

    Args:
        sql_code: Plain-text SQL code.
        resolved_variables: {placeholder_name: variable_item} from DescribeVariables.
        reference_tables: Optional list of reference table dicts for MetadataV1.
            Each dict: {"catalog": str, "database": str, "table": str, "version": int}
        catalogs: Optional list of catalog dicts for MetadataV1.
            Each dict: {"name": str, "defaultDatabase": str, "type": int, ...}

    Returns the MetadataV1 dict (NOT base64-encoded yet) and the list of
    placeholders that were not resolved.
    """
    parsed = extract_sql_variables(sql_code)

    variables = []
    unresolved = []
    for entry in parsed:
        v = resolved_variables.get(entry["placeholder"])
        if v is None:
            unresolved.append(entry["placeholder"])
            value = entry["default_value"]
            var_id = ""
        else:
            var_type = int(v.get("Type") or 0)
            value = v.get("Value", "") if var_type == 1 else ""
            var_id = v.get("SerialId", "")

        variables.append({
            "table": entry["table"],
            "key": entry["key"],
            "placeholder": entry["placeholder"],
            "value": value,
            "variableId": var_id,
            "table_type": entry["table_type"],
        })

    grouped = {}
    for v in variables:
        gkey = ("_default", "_default", v["table"], v["table_type"])
        grouped.setdefault(gkey, []).append({
            "key": v["key"],
            "value": v["value"],
            "variableId": v["variableId"],
            "placeholder": v["placeholder"],
        })

    var_items = []
    for (cat, db, tbl, tt), entries in grouped.items():
        var_items.append({
            "catalog": cat,
            "database": db,
            "table": tbl,
            "type": tt,
            "variableEntries": entries,
        })

    # Build referenceTables
    ref_tables = []
    if reference_tables:
        for rt in reference_tables:
            ref_tables.append({
                "catalog": rt.get("catalog", ""),
                "database": rt.get("database", ""),
                "table": rt.get("table", ""),
                "version": rt.get("version", 0),
            })

    metadata_v1 = {
        "Metadata": {
            "referenceTables": ref_tables,
            "variables": var_items,
        }
    }

    # Add catalogs if provided
    if catalogs:
        metadata_v1["Metadata"]["catalogs"] = catalogs

    return metadata_v1, unresolved


# ═══════════════════════════════════════════════════════════════════════════
# Catalog / Reference Table resolution for Metadata
# ═══════════════════════════════════════════════════════════════════════════

# Catalog type constants (same as metadata_query.py)
_CATALOG_TYPE_OCEANUS = 0
_CATALOG_TYPE_HIVE = 1

# HADOOP_USER_NAME properties required for Hive catalog jobs
_HADOOP_USER_NAME_PROPERTIES = [
    {"Key": "containerized.taskmanager.env.HADOOP_USER_NAME", "Value": "hadoop"},
    {"Key": "containerized.master.env.HADOOP_USER_NAME", "Value": "hadoop"},
]

# Async polling constants for external catalog queries
_ASYNC_INITIAL_INTERVAL = 1.0
_ASYNC_MAX_INTERVAL = 5.0
_ASYNC_MAX_RETRIES = 30


def _async_poll_for_metadata(action, params, region, verbose=False):
    """Poll an async metadata query until completion (used internally by metadata builder).

    Same logic as metadata_query._async_poll but avoids circular import.
    """
    import time as _time

    params["IsAsync"] = 1
    params.pop("AsyncTaskId", None)

    result = call_api(action, params, region)
    if not result.get("success"):
        return None, result

    data = result.get("data", {})
    async_status = data.get("AsyncStatus", 0)
    if async_status == 1:
        return data, None

    async_task_id = data.get("AsyncTaskId", "")
    if not async_task_id:
        return data, None

    interval = _ASYNC_INITIAL_INTERVAL
    for attempt in range(1, _ASYNC_MAX_RETRIES + 1):
        if verbose:
            sys.stderr.write(
                f"  [metadata resolve] {action} poll {attempt}/{_ASYNC_MAX_RETRIES}...\n"
            )
            sys.stderr.flush()
        _time.sleep(interval)

        poll_params = dict(params)
        poll_params["AsyncTaskId"] = async_task_id
        result = call_api(action, poll_params, region)
        if not result.get("success"):
            return None, result

        data = result.get("data", {})
        if data.get("AsyncStatus", 0) == 1:
            return data, None

        interval = min(interval * 1.5, _ASYNC_MAX_INTERVAL)

    return None, {
        "success": False,
        "operation": action,
        "error": {
            "code": "AsyncTimeout",
            "message": f"Async query for {action} timed out during metadata resolution.",
        },
    }


def resolve_catalog_refs(region, workspace_id, catalog_refs,
                         existing_catalogs=None,
                         cluster_id=None, flink_version=None, verbose=False):
    """Resolve catalog references into MetadataV1 catalogs and referenceTables.

    **IMPORTANT — API case inconsistency**:
    The backend returns Metadata with *uppercase* ``Catalogs`` (via
    DescribeJobConfigs) but expects *lowercase* ``catalogs`` when writing
    (ModifyDraftConfig / CreateJobConfig).  The two are the same data; the
    uppercase version already contains the correct ``catalogVersion`` (e.g.
    Hive ``2.3.5``), ``configFilePath``, etc.  Therefore, when the caller
    already has the existing draft Metadata, we should re-use its uppercase
    ``Catalogs`` entries directly (written back as lowercase ``catalogs``)
    instead of re-building them from ``DescribeCatalogs`` (which lacks
    component-specific version info like the actual Hive version).

    Args:
        region: API region.
        workspace_id: Workspace serial ID (space-xxx).
        catalog_refs: List of dicts describing catalog/table references.
            Each dict: {"catalog": "name", "database": "db", "table": "tbl"}
            "catalog" is required; "database" and "table" are optional.
        existing_catalogs: Optional list of catalog dicts from the existing
            draft's Metadata.Catalogs (uppercase C).  When provided, matching
            entries are used directly — preserving the correct catalogVersion
            and other fields that the backend already resolved.
        cluster_id: Optional cluster ID for external catalog queries.
        flink_version: Optional Flink version for external catalog queries.
        verbose: Whether to print progress info.

    Returns:
        (catalogs_list, reference_tables_list, error_response_or_None, has_hive)
        catalogs_list: List of catalog config dicts for MetadataV1.Metadata.catalogs
        reference_tables_list: List of reference table dicts for MetadataV1.Metadata.referenceTables
        has_hive: Boolean — True if any referenced catalog is of type HIVE (type=1)
    """
    if not catalog_refs:
        return [], [], None, False

    # Build a lookup from existing (uppercase) Catalogs by name for reuse
    existing_by_name = {}
    if existing_catalogs:
        for ec in existing_catalogs:
            ec_name = ec.get("name", "")
            if ec_name:
                existing_by_name[ec_name] = ec

    # Step 1: Get all catalogs to map name → catalog info (for type lookup etc.)
    result = call_api("DescribeCatalogs", {"WorkSpaceId": workspace_id}, region)
    if not result.get("success"):
        return [], [], result, False

    all_catalogs = (result.get("data") or {}).get("Catalogs", []) or []
    catalog_by_name = {}
    for c in all_catalogs:
        catalog_by_name[c.get("Name", "")] = c

    catalogs_out = []
    ref_tables_out = []
    seen_catalog_names = set()
    has_hive = False

    for ref in catalog_refs:
        cat_name = ref.get("catalog", "")
        db_name = ref.get("database", "")
        table_name = ref.get("table", "")

        if not cat_name:
            continue

        cat_info = catalog_by_name.get(cat_name)
        if not cat_info:
            if verbose:
                sys.stderr.write(f"  [WARN] Catalog '{cat_name}' not found in workspace\n")
            continue

        cat_type = cat_info.get("Type", 0)
        cat_serial_id = cat_info.get("SerialId", "")
        cat_id = cat_info.get("Id", 0)

        # Track whether any referenced catalog is Hive
        if cat_type == _CATALOG_TYPE_HIVE:
            has_hive = True

        # Add catalog to output list (deduplicated by name).
        # Priority: reuse existing draft Catalogs entry (which has the correct
        # catalogVersion etc.); fall back to building from DescribeCatalogs.
        if cat_name not in seen_catalog_names:
            seen_catalog_names.add(cat_name)

            existing_entry = existing_by_name.get(cat_name)
            if existing_entry:
                # Reuse the backend-populated entry directly (it has the
                # correct catalogVersion, configFilePath, etc.)
                catalogs_out.append(existing_entry)
                if verbose:
                    sys.stderr.write(
                        f"  [INFO] Reusing existing Catalog entry for '{cat_name}' "
                        f"(catalogVersion={existing_entry.get('catalogVersion', '')})\n"
                    )
            else:
                # Fallback: build from DescribeCatalogs (new catalog not yet
                # in draft). For external catalogs we leave catalogVersion
                # empty — the backend will fill it on the next read.
                if cat_type == _CATALOG_TYPE_OCEANUS:
                    catalog_version = cat_info.get("FlinkVersion", "")
                else:
                    catalog_version = ""
                catalog_entry = {
                    "name": cat_name,
                    "defaultDatabase": cat_info.get("DefaultDatabase", ""),
                    "type": cat_type,
                    "catalogVersion": catalog_version,
                    "catalogId": cat_id,
                }
                catalogs_out.append(catalog_entry)
                if verbose:
                    sys.stderr.write(
                        f"  [INFO] Built new catalog entry for '{cat_name}' "
                        f"(type={cat_type}, catalogVersion='{catalog_version}')\n"
                    )

        # Build reference table entry — only for default (Oceanus) catalog (type=0).
        # External catalogs (HIVE/JDBC etc., type!=0) should NOT be added to
        # referenceTables because RunJobs metadata validation cannot resolve
        # external catalog tables and will fail with "Meta Table not found".
        if table_name and cat_type == _CATALOG_TYPE_OCEANUS:
            ref_table_entry = {
                "catalog": cat_name,
                "database": db_name,
                "table": table_name,
            }

            # For default catalog (type=0), try to get table version
            if db_name and table_name:
                # Query default catalog tree to find table version
                meta_params = {"WorkSpaceId": workspace_id}
                if cat_serial_id:
                    meta_params["SerialId"] = cat_serial_id
                meta_result = call_api("DescribeMetaCatalogs", meta_params, region)
                if meta_result.get("success"):
                    meta_data = meta_result.get("data", {})
                    for mc in (meta_data.get("CatalogSet") or []):
                        for mdb in (mc.get("DatabaseSet") or []):
                            if mdb.get("Name", "") == db_name:
                                for mt in (mdb.get("MetaTableSet") or []):
                                    if mt.get("Name", "") == table_name:
                                        ref_table_entry["version"] = mt.get("Version", 0)
                                        break

            ref_tables_out.append(ref_table_entry)
        elif table_name and cat_type != _CATALOG_TYPE_OCEANUS and verbose:
            sys.stderr.write(
                f"  [INFO] Skipping referenceTables entry for external catalog "
                f"'{cat_name}.{db_name}.{table_name}' (type={cat_type})\n"
            )

    return catalogs_out, ref_tables_out, None, has_hive


# ═══════════════════════════════════════════════════════════════════════════
# Properties merge utility
# ═══════════════════════════════════════════════════════════════════════════


def merge_properties(existing_properties, new_properties):
    """Merge new properties into existing ones (Key-based upsert).

    Existing properties are preserved; new properties with the same Key
    overwrite the existing value.  New keys are appended.

    Args:
        existing_properties: list of {"Key": str, "Value": str} from draft.
        new_properties: list of {"Key": str, "Value": str} to merge in.

    Returns:
        Merged list of {"Key": str, "Value": str}.
    """
    if not existing_properties and not new_properties:
        return []
    if not new_properties:
        return list(existing_properties or [])
    if not existing_properties:
        return list(new_properties)

    # Build ordered dict from existing
    by_key = {}
    order = []
    for p in existing_properties:
        k = p.get("Key", "")
        by_key[k] = p.get("Value", "")
        order.append(k)

    # Upsert new
    for p in new_properties:
        k = p.get("Key", "")
        if k not in by_key:
            order.append(k)
        by_key[k] = p.get("Value", "")

    return [{"Key": k, "Value": by_key[k]} for k in order]


def detect_hive_in_properties(properties):
    """Check whether the Properties list already contains HADOOP_USER_NAME entries.

    Returns True if both containerized.taskmanager.env.HADOOP_USER_NAME and
    containerized.master.env.HADOOP_USER_NAME are present.
    """
    if not properties:
        return False
    keys = {p.get("Key", "") for p in properties}
    return (
        "containerized.taskmanager.env.HADOOP_USER_NAME" in keys
        and "containerized.master.env.HADOOP_USER_NAME" in keys
    )


def ensure_hive_properties(properties, has_hive_catalog, verbose=False):
    """If the job references a Hive catalog, ensure HADOOP_USER_NAME properties exist.

    Merges the required HADOOP_USER_NAME entries into the properties list.
    If they already exist, their values are preserved (not overwritten).

    Args:
        properties: Existing properties list (may be None or []).
        has_hive_catalog: Boolean from resolve_catalog_refs or metadata inspection.
        verbose: Print info to stderr.

    Returns:
        Updated properties list.
    """
    if not has_hive_catalog:
        return properties or []

    existing = properties or []
    if detect_hive_in_properties(existing):
        if verbose:
            sys.stderr.write(
                "  [INFO] HADOOP_USER_NAME properties already present, skipping injection\n"
            )
        return existing

    if verbose:
        sys.stderr.write(
            "  [INFO] Hive catalog detected — injecting HADOOP_USER_NAME properties\n"
        )

    return merge_properties(existing, _HADOOP_USER_NAME_PROPERTIES)


# ═══════════════════════════════════════════════════════════════════════════
# ProgramArgs builders (SQL / JAR)
# ═══════════════════════════════════════════════════════════════════════════


def build_sql_program_args(existing_program_args, sql_code,
                           region=None, workspace_id=None,
                           catalog_refs=None, reference_tables=None,
                           existing_metadata=None,
                           cluster_id=None, flink_version=None,
                           verbose=False):
    """Replace SqlCode (and Metadata) in ProgramArgs JSON with base64-encoded payloads.

    Args:
        existing_program_args: Existing ProgramArgs JSON string (from draft).
        sql_code: Plain-text SQL code.
        region: API region for variable/catalog resolution.
        workspace_id: Workspace ID for variable/catalog resolution.
        catalog_refs: Optional list of catalog reference dicts for Metadata.
            Each dict: {"catalog": "name", "database": "db", "table": "tbl"}
            Used to auto-resolve catalog details and build referenceTables/catalogs.
        reference_tables: Optional list of pre-built reference table dicts.
            Each dict: {"catalog": str, "database": str, "table": str, "version": int}
            If provided directly, skip auto-resolution for these tables.
        existing_metadata: Optional dict — the *decoded* Metadata from the
            existing draft (i.e. the ``Metadata`` key's parsed JSON value).
            Used to extract the backend-populated uppercase ``Catalogs`` list
            so that ``resolve_catalog_refs`` can reuse entries with the
            correct ``catalogVersion`` instead of rebuilding them.
        cluster_id: Optional cluster ID for external catalog async queries.
        flink_version: Optional Flink version for external catalog queries.
        verbose: Whether to print progress info.

    Returns:
        Tuple (program_args_json:str, unresolved_placeholders:list[str], has_hive:bool).
        has_hive is True when any referenced catalog is Hive type.
    """
    try:
        pa = json.loads(existing_program_args)
    except (json.JSONDecodeError, TypeError):
        pa = {}
    pa["SqlCode"] = encode_sql(sql_code)

    unresolved = []
    resolved_vars = {}
    catalogs_list = None
    ref_tables_list = reference_tables
    has_hive = False

    # Extract existing uppercase Catalogs from draft Metadata (if available)
    existing_catalogs = None
    if existing_metadata:
        meta_inner = existing_metadata.get("Metadata", {})
        existing_catalogs = meta_inner.get("Catalogs") or None

    # Resolve variables if SQL contains ${...} placeholders
    if region and workspace_id and ("${" in (sql_code or "")):
        resolved_vars, err = _resolve_variables_via_api(
            region, workspace_id,
            placeholders=[e["placeholder"] for e in extract_sql_variables(sql_code)],
            verbose=verbose,
        )
        if err is not None:
            resolved_vars = {}

    # Resolve catalog references if provided
    if region and workspace_id and catalog_refs:
        catalogs_list, auto_ref_tables, err, _has_hive = resolve_catalog_refs(
            region, workspace_id, catalog_refs,
            existing_catalogs=existing_catalogs,
            cluster_id=cluster_id, flink_version=flink_version,
            verbose=verbose,
        )
        has_hive = _has_hive
        if err is None and auto_ref_tables:
            # Merge auto-resolved tables with explicitly provided ones
            if ref_tables_list:
                ref_tables_list = ref_tables_list + auto_ref_tables
            else:
                ref_tables_list = auto_ref_tables
        if err and verbose:
            sys.stderr.write(
                f"  [WARN] Catalog reference resolution failed: "
                f"{err.get('error', {}).get('message', 'unknown')}\n"
            )

    # Build metadata if we have variables, catalog refs, or reference tables
    has_variables = ("${" in (sql_code or "")) and region and workspace_id
    has_refs = ref_tables_list or catalogs_list
    if has_variables or has_refs:
        metadata_v1, unresolved = _build_metadata_v1(
            sql_code, resolved_vars,
            reference_tables=ref_tables_list,
            catalogs=catalogs_list,
        )
        metadata_json = json.dumps(metadata_v1, ensure_ascii=False)
        pa["Metadata"] = base64.b64encode(metadata_json.encode("utf-8")).decode("ascii")

    return json.dumps(pa, ensure_ascii=False), unresolved, has_hive


def build_jar_program_args(existing_program_args, entrypoint_class=None,
                           program_args=None, resource_refs=None):
    """DEPRECATED. Do not use.

    Earlier versions nested EntrypointClass / ResourceRefs inside the ProgramArgs
    JSON. This is incorrect. Kept only for backward compatibility.
    """
    try:
        pa = json.loads(existing_program_args)
    except (json.JSONDecodeError, TypeError):
        pa = {}

    pa.pop("SqlCode", None)

    if entrypoint_class is not None:
        pa["EntrypointClass"] = entrypoint_class
    if program_args is not None:
        pa["ProgramArgs"] = program_args
    if resource_refs is not None:
        pa["ResourceRefs"] = resource_refs

    return json.dumps(pa, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════
# Job type detection and requirement
# ═══════════════════════════════════════════════════════════════════════════


def detect_job_type(draft_config, args):
    """Resolve job type strictly from explicit sources — no heuristics.

    Resolution order:
      1. draft_config.JobType (authoritative when the job already exists)
      2. args.job_type (must be explicitly passed by the caller)

    Returns int (JOB_TYPE_SQL or JOB_TYPE_JAR), or None.
    """
    draft_job_type = draft_config.get("JobType")
    if draft_job_type in (JOB_TYPE_SQL, JOB_TYPE_JAR):
        return draft_job_type

    arg_job_type = getattr(args, "job_type", None)
    if arg_job_type is not None:
        try:
            jt = int(arg_job_type)
        except (TypeError, ValueError):
            return None
        if jt in (JOB_TYPE_SQL, JOB_TYPE_JAR):
            return jt

    return None


def infer_job_type_from_args(args):
    """Return the explicit --job_type, or None if not provided.

    No heuristics: never infer the job type from --entrypoint_class /
    --resource_refs / --program_args.
    """
    explicit = getattr(args, "job_type", None)
    if explicit is None:
        return None
    try:
        jt = int(explicit)
    except (TypeError, ValueError):
        return None
    if jt not in (JOB_TYPE_SQL, JOB_TYPE_JAR):
        return None
    return jt


def require_job_type(args, subcommand):
    """Resolve job type from --job_type or return a ValidationError result.

    Returns:
        tuple (job_type:int|None, error_result:dict|None).
    """
    job_type = infer_job_type_from_args(args)
    if job_type is None:
        return None, error_response(
            subcommand,
            "ValidationError",
            "必须显式传入 --job_type (1=SQL, 2=JAR)，不再根据其它参数推断作业类型",
        )
    return job_type, None


# ═══════════════════════════════════════════════════════════════════════════
# SQL input reading & ResourceRef parsing/validation
# ═══════════════════════════════════════════════════════════════════════════


def read_sql_input(args):
    """Read SQL content from --sql or --sql_file argument.

    Returns plain-text SQL string, or None if neither provided.
    """
    if getattr(args, "sql", None):
        return args.sql
    if getattr(args, "sql_file", None):
        try:
            with open(args.sql_file, "r", encoding="utf-8") as f:
                return f.read()
        except IOError:
            return None
    return None


def parse_resource_refs(args):
    """Parse --resource_refs JSON string into a list of dicts.

    Returns:
        tuple (refs:list|None, error_msg:str|None).
    """
    raw = getattr(args, "resource_refs", None)
    if not raw:
        return None, None
    try:
        refs = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        return None, f"--resource_refs 不是合法 JSON: {exc}"
    if not isinstance(refs, list):
        return None, "--resource_refs 必须是 JSON 数组，例如 '[{\"ResourceId\":\"resource-xxx\",\"Type\":0,\"Version\":1}]'"
    for i, item in enumerate(refs):
        if not isinstance(item, dict):
            return None, f"--resource_refs[{i}] 必须是对象，得到: {item!r}"
        if not item.get("ResourceId"):
            return None, f"--resource_refs[{i}] 缺少 ResourceId"
        if "Type" not in item:
            return None, (
                f"--resource_refs[{i}] 缺少 Type；"
                f"Type 表示资源在作业中的用途："
                f"0=DEPENDENCY_JAR(辅助 jar 包，非主程序)，"
                f"1=MAIN(JAR 主程序，仅 JAR 作业且必须恰好一个)，"
                f"2=DEPENDENCY(配置文件等非 jar 资源)"
            )
        try:
            t = int(item["Type"])
        except (TypeError, ValueError):
            return None, (
                f"--resource_refs[{i}].Type 必须是整数 "
                f"(0=DEPENDENCY_JAR, 1=MAIN, 2=DEPENDENCY)，得到: {item['Type']!r}"
            )
        if t not in _RESOURCE_REF_TYPE_VALID:
            return None, (
                f"--resource_refs[{i}].Type={t} 非法；"
                f"ResourceRef.Type 只能是 0(DEPENDENCY_JAR)、1(MAIN) 或 2(DEPENDENCY)。"
                f"注意它与 Resource.Type(1=jar 包, 2=配置文件) 不是同一概念。"
            )
        item["Type"] = t
    return refs, None


def validate_resource_refs_for_job_type(refs, job_type):
    """Enforce job-type-specific rules on a parsed ResourceRefs list.

    Returns:
        str|None — error message when invalid, None when OK.
    """
    if refs is None:
        return None

    main_indexes = [i for i, r in enumerate(refs)
                    if int(r.get("Type", 0)) == RESOURCE_REF_TYPE_MAIN]

    if job_type == JOB_TYPE_JAR:
        if len(main_indexes) == 0:
            return (
                "JAR 作业的 --resource_refs 必须包含 **恰好一个** 主程序包条目 (Type=1, MAIN)，"
                "当前一个都没有。请在依赖列表中明确指定哪一个 jar 资源是主程序包，"
                "示例: '[{\"ResourceId\":\"resource-main\",\"Type\":1,\"Version\":1}, "
                "{\"ResourceId\":\"resource-lib\",\"Type\":0,\"Version\":1}]'"
            )
        if len(main_indexes) > 1:
            dup_ids = [refs[i].get("ResourceId", "?") for i in main_indexes]
            return (
                f"JAR 作业的 --resource_refs 只能有 **一个** 主程序包 (Type=1, MAIN)，"
                f"当前检测到 {len(main_indexes)} 个: {dup_ids}。"
                "请在这些资源中选择一个作为主包 (Type=1)，"
                "其余 jar 改为 Type=0 (DEPENDENCY_JAR)，配置文件改为 Type=2 (DEPENDENCY)。"
            )
        return None

    if job_type == JOB_TYPE_SQL:
        if main_indexes:
            offending = [refs[i].get("ResourceId", "?") for i in main_indexes]
            return (
                f"SQL 作业的 --resource_refs 不能包含 Type=1 (MAIN) 主程序包条目，"
                f"违规条目: {offending}。SQL 作业引用的资源请按用途选择："
                f"jar 包用 Type=0 (DEPENDENCY_JAR)，配置文件用 Type=2 (DEPENDENCY)。"
                f"注意 ResourceRef.Type 与 Resource.Type 不是同一概念："
                f"上传 jar 时 Resource.Type=1，但在作业中引用它时 ResourceRef.Type=0 (DEPENDENCY_JAR)。"
            )
        return None

    return None


def resolve_resource_refs(args, job_type, subcommand):
    """Parse + validate --resource_refs against job_type.

    Returns:
        tuple (refs:list|None, error_result:dict|None).
    """
    refs, parse_err = parse_resource_refs(args)
    if parse_err:
        return None, error_response(subcommand, "ValidationError", parse_err)
    val_err = validate_resource_refs_for_job_type(refs, job_type)
    if val_err:
        return None, error_response(subcommand, "ValidationError", val_err)
    return refs, None


# ═══════════════════════════════════════════════════════════════════════════
# Draft Confirmation — used by create_job_config
# ═══════════════════════════════════════════════════════════════════════════

DRAFT_SUMMARY_MAX_LEN = 2000


def format_draft_summary(job_type, sql_code=None, entrypoint_class=None,
                         program_args=None, resource_refs=None,
                         config_params=None, base_version=None,
                         properties=None):
    """Format a human-readable summary of the draft config about to be published."""
    lines = []
    lines.append("═" * 55)
    lines.append("  草稿配置摘要 — 即将发布为新版本")
    lines.append("═" * 55)
    lines.append("")

    job_type_name = _JOB_TYPE_NAMES.get(job_type, str(job_type))
    lines.append(f"  作业类型: {job_type_name}")

    if base_version is not None:
        lines.append(f"  基于版本: v{base_version}")

    cp = config_params or {}
    if cp.get("FlinkVersion"):
        lines.append(f"  Flink 版本: {cp['FlinkVersion']}")
    if cp.get("JdkVersion"):
        lines.append(f"  JDK 版本: {cp['JdkVersion']}")
    if cp.get("DefaultParallelism"):
        lines.append(f"  默认并行度: {cp['DefaultParallelism']}")
    if cp.get("Remark"):
        lines.append(f"  备注: {cp['Remark']}")

    lines.append("")

    if job_type == JOB_TYPE_SQL:
        lines.append("  ── SQL 代码 ──")
        if sql_code:
            for sl in sql_code.strip().splitlines():
                lines.append(f"  {sl}")
        else:
            lines.append("  (未提供 SQL 代码，将使用草稿中已有的 SQL)")
        lines.append("")
    else:
        lines.append("  ── JAR 配置 ──")
        if entrypoint_class:
            lines.append(f"  EntrypointClass: {entrypoint_class}")
        if program_args:
            lines.append(f"  ProgramArgs: {program_args}")
        lines.append("")

    if resource_refs:
        lines.append(f"  ── 资源引用 (ResourceRefs, 共 {len(resource_refs)} 个) ──")
        for i, ref in enumerate(resource_refs, 1):
            rid = ref.get("ResourceId", "?")
            rtype = int(ref.get("Type", -1))
            rtype_name = _RESOURCE_REF_TYPE_NAMES.get(rtype, str(rtype))
            rver = ref.get("Version", "?")
            lines.append(f"  [{i}] {rid} (Type={rtype} {rtype_name}, Version={rver})")
        lines.append("")
    else:
        lines.append("  ── 资源引用: 无 ──")
        lines.append("")

    if properties:
        lines.append(f"  ── 高级参数 (Properties, 共 {len(properties)} 个) ──")
        for p in properties:
            lines.append(f"  {p.get('Key', '?')} = {p.get('Value', '')}")
        lines.append("")

    lines.append("═" * 55)
    return "\n".join(lines)


def confirm_draft_before_publish(operation, draft_summary, skip_flag, confirm_flag):
    """Show draft summary and require confirmation before publishing.

    Returns None to proceed, or an error_response dict to abort.
    """
    if skip_flag:
        return None

    if len(draft_summary) > DRAFT_SUMMARY_MAX_LEN:
        try:
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", prefix="oceanus_draft_summary_",
                delete=False, encoding="utf-8",
            )
            tmp.write(draft_summary)
            tmp.close()
            print(
                f"\n[{operation}] 草稿配置内容较长，已写入临时文件: {tmp.name}\n"
                f"[{operation}] 请查看后确认是否发布。",
                file=sys.stderr,
            )
        except OSError as exc:
            print(
                f"\n[{operation}] 无法创建临时文件({exc})，直接输出摘要:\n",
                file=sys.stderr,
            )
            print(draft_summary, file=sys.stderr)
    else:
        print(f"\n{draft_summary}", file=sys.stderr)

    return require_confirmation(
        operation,
        "确认以上草稿配置无误，发布为新版本？(如需跳过此确认，请加 --skip_draft_confirm)",
        False,
    )
