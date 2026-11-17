#!/usr/bin/env python3
"""
Unit tests for TencentCloud Oceanus CLI — pure-logic only, no network calls.

Covers:
- client.py        — response envelopes, signature, _extract_rows, require_args,
                     require_confirmation (non-TTY)
- job_config_helpers.py
                   — encode_sql, extract_sql_variables (3 placeholder forms),
                     merge_properties, detect/ensure_hive_properties,
                     job_type detection/validation, resource_refs parsing &
                     job-type validation, read_sql_input, _build_metadata_v1,
                     build_sql/jar_program_args, format_draft_summary,
                     confirm_draft_before_publish (skip path)
- resource_change_ops.py
                   — process_remove_resources, format_resource_changes_summary
- resource_resolver.py
                   — resolve_region (canonical input only), resolve_version
- job_runtime.py   — _resolve_start_mode, VALID_START_MODES
- job_observability.py
                   — _default_time_range, _build_cos_info (CDC & normal)

Run:
    python scripts/unit_test.py
    python -m unittest discover -s scripts -p 'unit_test.py' -v
"""

import argparse
import base64
import io
import json
import os
import sys
import tempfile
import time
import unittest
from types import SimpleNamespace
from unittest import mock

# Ensure scripts/ is on sys.path when invoked via `python -m unittest` etc.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import client
import job_config_helpers as jch
import resource_change_ops as rco
import resource_resolver as rr
import job_runtime as jrt
import job_observability as jobs


# ─── Helpers ──────────────────────────────────────────────────────────────
# Force require_confirmation() into the non-TTY branch regardless of how the
# tests are launched (CI pipe vs. interactive terminal). Otherwise, when a
# developer runs `python scripts/unit_test.py` directly in their terminal,
# the safety prompt would block on input() and the suite would hang.

def _force_non_tty():
    """Return a context manager that makes sys.stdin/stdout look non-interactive."""
    fake_stdin = mock.MagicMock(spec=io.IOBase)
    fake_stdin.isatty.return_value = False
    fake_stdout = mock.MagicMock(spec=io.IOBase)
    fake_stdout.isatty.return_value = False
    return mock.patch.multiple(sys, stdin=fake_stdin, stdout=fake_stdout)


# ═══════════════════════════════════════════════════════════════════════════
# client.py
# ═══════════════════════════════════════════════════════════════════════════


class TestResponseEnvelopes(unittest.TestCase):
    def test_success_response_shape(self):
        env = client.success_response("OpX", {"k": 1}, request_id="rid-1")
        self.assertTrue(env["success"])
        self.assertEqual(env["operation"], "OpX")
        self.assertEqual(env["data"], {"k": 1})
        self.assertEqual(env["request_id"], "rid-1")
        self.assertNotIn("error", env)

    def test_error_response_shape(self):
        env = client.error_response("OpY", "Boom", "bad", request_id="rid-2")
        self.assertFalse(env["success"])
        self.assertEqual(env["operation"], "OpY")
        self.assertEqual(env["error"], {"code": "Boom", "message": "bad"})
        self.assertEqual(env["request_id"], "rid-2")

    def test_error_response_default_request_id(self):
        env = client.error_response("OpZ", "Code", "msg")
        self.assertEqual(env["request_id"], "")


class TestExtractRows(unittest.TestCase):
    def test_list_passthrough(self):
        self.assertEqual(client._extract_rows([1, 2, 3]), [1, 2, 3])

    def test_dict_finds_first_list_value(self):
        self.assertEqual(
            client._extract_rows({"a": "x", "b": [{"k": 1}], "c": [{"k": 2}]}),
            [{"k": 1}],
        )

    def test_dict_no_list_returns_none(self):
        self.assertIsNone(client._extract_rows({"a": "x", "b": 1}))

    def test_scalar_returns_none(self):
        self.assertIsNone(client._extract_rows("hello"))
        self.assertIsNone(client._extract_rows(42))


class TestBuildAuthorization(unittest.TestCase):
    """The signature is deterministic; verify structure and stability."""

    def test_authorization_structure(self):
        auth = client._build_authorization(
            secret_id="AKIDxxxxxxxxxxxxxxxxxxxxxxxx",
            secret_key="SKxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            service="oceanus",
            date="2025-01-01",
            timestamp="1735689600",
            payload='{"Limit":10}',
        )
        self.assertTrue(auth.startswith("TC3-HMAC-SHA256 "))
        self.assertIn("Credential=AKIDxxxxxxxxxxxxxxxxxxxxxxxx/2025-01-01/oceanus/tc3_request", auth)
        self.assertIn("SignedHeaders=content-type;host", auth)
        # Signature must be 64-char hex
        sig_part = auth.split("Signature=", 1)[1]
        self.assertEqual(len(sig_part), 64)
        int(sig_part, 16)  # must parse as hex

    def test_authorization_deterministic(self):
        kwargs = dict(
            secret_id="AKID-test", secret_key="SK-test", service="oceanus",
            date="2025-01-01", timestamp="1735689600", payload="{}",
        )
        a = client._build_authorization(**kwargs)
        b = client._build_authorization(**kwargs)
        self.assertEqual(a, b)

    def test_authorization_changes_with_payload(self):
        base = dict(secret_id="A", secret_key="K", service="oceanus",
                    date="2025-01-01", timestamp="1", payload="{}")
        sig1 = client._build_authorization(**base).split("Signature=")[1]
        base2 = dict(base)
        base2["payload"] = '{"x":1}'
        sig2 = client._build_authorization(**base2).split("Signature=")[1]
        self.assertNotEqual(sig1, sig2)


class TestRequireArgs(unittest.TestCase):
    def test_all_present(self):
        ns = SimpleNamespace(name="job", region="ap-guangzhou", subcommand="create_job")
        self.assertIsNone(client.require_args(ns, "name", "region"))

    def test_missing_returns_error(self):
        ns = SimpleNamespace(name="job", region="", subcommand="create_job")
        err = client.require_args(ns, "name", "region")
        self.assertIsNotNone(err)
        self.assertFalse(err["success"])
        self.assertEqual(err["error"]["code"], "ValidationError")
        self.assertIn("--region", err["error"]["message"])

    def test_whitespace_only_is_missing(self):
        ns = SimpleNamespace(name="   ", subcommand="x")
        err = client.require_args(ns, "name")
        self.assertIsNotNone(err)
        self.assertEqual(err["error"]["code"], "ValidationError")

    def test_none_is_missing(self):
        ns = SimpleNamespace(name=None, subcommand="x")
        err = client.require_args(ns, "name")
        self.assertIsNotNone(err)


class TestRequireConfirmation(unittest.TestCase):
    def test_flag_present_passes(self):
        self.assertIsNone(client.require_confirmation("op", "msg", flag_present=True))

    def test_non_tty_returns_safety_required(self):
        # Force non-TTY so the test is deterministic in any environment
        # (including an interactive developer terminal).
        with _force_non_tty():
            err = client.require_confirmation("op", "this will delete", flag_present=False)
        self.assertIsNotNone(err)
        self.assertFalse(err["success"])
        self.assertEqual(err["error"]["code"], "SafetyCheckRequired")
        self.assertIn("--confirm", err["error"]["message"])


# ═══════════════════════════════════════════════════════════════════════════
# job_config_helpers.py
# ═══════════════════════════════════════════════════════════════════════════


class TestEncodeSql(unittest.TestCase):
    def test_ascii(self):
        encoded = jch.encode_sql("SELECT 1")
        self.assertEqual(base64.b64decode(encoded).decode("utf-8"), "SELECT 1")

    def test_unicode(self):
        sql = "SELECT '中文' as name"
        encoded = jch.encode_sql(sql)
        self.assertEqual(base64.b64decode(encoded).decode("utf-8"), sql)


class TestExtractSqlVariables(unittest.TestCase):
    def test_no_placeholder(self):
        sql = "CREATE TABLE t1 (a INT) WITH ('x' = '1');"
        self.assertEqual(jch.extract_sql_variables(sql), [])

    def test_no_create_table(self):
        # Variables outside CREATE TABLE blocks are not picked up
        sql = "SELECT ${not_seen} FROM t;"
        self.assertEqual(jch.extract_sql_variables(sql), [])

    def test_bare_placeholder(self):
        sql = "CREATE TABLE t1 (a INT) WITH ('topic' = '${tp}');"
        out = jch.extract_sql_variables(sql)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["table"], "t1")
        self.assertEqual(out[0]["key"], "topic")
        self.assertEqual(out[0]["placeholder"], "tp")
        self.assertEqual(out[0]["default_value"], "")
        self.assertEqual(out[0]["table_type"], 2)

    def test_new_form_placeholder_with_default(self):
        sql = "CREATE TABLE t1 (a INT) WITH ('k' = '${tp:my_default}');"
        out = jch.extract_sql_variables(sql)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["placeholder"], "tp")
        self.assertEqual(out[0]["default_value"], "my_default")

    def test_legacy_form_placeholder(self):
        sql = "CREATE TABLE t1 (a INT) WITH ('k' = '${tp}:legacy_def');"
        out = jch.extract_sql_variables(sql)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["placeholder"], "tp")
        self.assertEqual(out[0]["default_value"], "legacy_def")

    def test_temporary_table_supported(self):
        sql = "CREATE TEMPORARY TABLE t1 (a INT) WITH ('k' = '${v}');"
        out = jch.extract_sql_variables(sql)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["table"], "t1")

    def test_backticked_name(self):
        sql = "CREATE TABLE `my_tbl` (a INT) WITH ('k' = '${v}');"
        out = jch.extract_sql_variables(sql)
        self.assertEqual(out[0]["table"], "my_tbl")

    def test_multiple_tables_and_vars(self):
        sql = (
            "CREATE TABLE t1 (a INT) WITH ('k1' = '${v1}', 'k2' = '${v2:def2}');\n"
            "CREATE TABLE t2 (b INT) WITH ('k3' = '${v3}:def3');"
        )
        out = jch.extract_sql_variables(sql)
        # 3 placeholders in total
        self.assertEqual(len(out), 3)
        tables = {(e["table"], e["placeholder"]) for e in out}
        self.assertIn(("t1", "v1"), tables)
        self.assertIn(("t1", "v2"), tables)
        self.assertIn(("t2", "v3"), tables)


class TestMergeProperties(unittest.TestCase):
    def test_both_empty(self):
        self.assertEqual(jch.merge_properties([], []), [])
        self.assertEqual(jch.merge_properties(None, None), [])

    def test_only_existing(self):
        existing = [{"Key": "a", "Value": "1"}]
        self.assertEqual(jch.merge_properties(existing, []), existing)
        self.assertEqual(jch.merge_properties(existing, None), existing)

    def test_only_new(self):
        new = [{"Key": "a", "Value": "1"}]
        self.assertEqual(jch.merge_properties(None, new), new)

    def test_upsert_overwrites_existing(self):
        existing = [{"Key": "a", "Value": "old"}, {"Key": "b", "Value": "B"}]
        new = [{"Key": "a", "Value": "new"}, {"Key": "c", "Value": "C"}]
        merged = jch.merge_properties(existing, new)
        # Order: a, b (existing order) then c (new key appended)
        self.assertEqual([m["Key"] for m in merged], ["a", "b", "c"])
        self.assertEqual({m["Key"]: m["Value"] for m in merged},
                         {"a": "new", "b": "B", "c": "C"})


class TestHiveProperties(unittest.TestCase):
    HADOOP_KEYS = {
        "containerized.taskmanager.env.HADOOP_USER_NAME",
        "containerized.master.env.HADOOP_USER_NAME",
    }

    def test_detect_returns_false_when_missing(self):
        self.assertFalse(jch.detect_hive_in_properties(None))
        self.assertFalse(jch.detect_hive_in_properties([]))
        self.assertFalse(jch.detect_hive_in_properties([{"Key": "x", "Value": "1"}]))

    def test_detect_returns_false_when_only_one_present(self):
        props = [{"Key": "containerized.taskmanager.env.HADOOP_USER_NAME", "Value": "hadoop"}]
        self.assertFalse(jch.detect_hive_in_properties(props))

    def test_detect_returns_true_when_both_present(self):
        props = [{"Key": k, "Value": "hadoop"} for k in self.HADOOP_KEYS]
        self.assertTrue(jch.detect_hive_in_properties(props))

    def test_ensure_hive_no_op_when_no_hive(self):
        existing = [{"Key": "x", "Value": "1"}]
        self.assertEqual(jch.ensure_hive_properties(existing, has_hive_catalog=False), existing)
        self.assertEqual(jch.ensure_hive_properties(None, has_hive_catalog=False), [])

    def test_ensure_hive_injects_when_hive_and_missing(self):
        out = jch.ensure_hive_properties([], has_hive_catalog=True)
        keys = {p["Key"] for p in out}
        self.assertEqual(keys, self.HADOOP_KEYS)

    def test_ensure_hive_preserves_existing_values(self):
        existing = [
            {"Key": "containerized.taskmanager.env.HADOOP_USER_NAME", "Value": "custom"},
            {"Key": "containerized.master.env.HADOOP_USER_NAME", "Value": "custom"},
        ]
        out = jch.ensure_hive_properties(existing, has_hive_catalog=True)
        self.assertEqual(out, existing)


class TestJobTypeHelpers(unittest.TestCase):
    def test_infer_explicit_sql(self):
        ns = SimpleNamespace(job_type=1)
        self.assertEqual(jch.infer_job_type_from_args(ns), jch.JOB_TYPE_SQL)

    def test_infer_explicit_jar(self):
        ns = SimpleNamespace(job_type="2")
        self.assertEqual(jch.infer_job_type_from_args(ns), jch.JOB_TYPE_JAR)

    def test_infer_invalid_returns_none(self):
        self.assertIsNone(jch.infer_job_type_from_args(SimpleNamespace(job_type=None)))
        self.assertIsNone(jch.infer_job_type_from_args(SimpleNamespace(job_type="abc")))
        self.assertIsNone(jch.infer_job_type_from_args(SimpleNamespace(job_type=99)))

    def test_detect_prefers_draft_config(self):
        ns = SimpleNamespace(job_type=1)
        self.assertEqual(jch.detect_job_type({"JobType": 2}, ns), 2)

    def test_detect_falls_back_to_args(self):
        ns = SimpleNamespace(job_type=1)
        self.assertEqual(jch.detect_job_type({}, ns), 1)

    def test_detect_returns_none_when_neither(self):
        self.assertIsNone(jch.detect_job_type({}, SimpleNamespace(job_type=None)))

    def test_require_job_type_ok(self):
        ns = SimpleNamespace(job_type=1)
        jt, err = jch.require_job_type(ns, "create_job_config")
        self.assertEqual(jt, 1)
        self.assertIsNone(err)

    def test_require_job_type_missing(self):
        ns = SimpleNamespace(job_type=None)
        jt, err = jch.require_job_type(ns, "create_job_config")
        self.assertIsNone(jt)
        self.assertIsNotNone(err)
        self.assertEqual(err["error"]["code"], "ValidationError")


class TestParseResourceRefs(unittest.TestCase):
    def test_none_returns_none(self):
        refs, err = jch.parse_resource_refs(SimpleNamespace(resource_refs=None))
        self.assertIsNone(refs)
        self.assertIsNone(err)

    def test_invalid_json(self):
        refs, err = jch.parse_resource_refs(SimpleNamespace(resource_refs="not-json"))
        self.assertIsNone(refs)
        self.assertIn("不是合法 JSON", err)

    def test_not_array(self):
        refs, err = jch.parse_resource_refs(
            SimpleNamespace(resource_refs='{"ResourceId":"r","Type":1}')
        )
        self.assertIsNone(refs)
        self.assertIn("JSON 数组", err)

    def test_item_not_object(self):
        refs, err = jch.parse_resource_refs(SimpleNamespace(resource_refs='[1,2]'))
        self.assertIsNone(refs)
        self.assertIn("必须是对象", err)

    def test_missing_resource_id(self):
        refs, err = jch.parse_resource_refs(
            SimpleNamespace(resource_refs='[{"Type":0}]')
        )
        self.assertIsNone(refs)
        self.assertIn("ResourceId", err)

    def test_missing_type(self):
        refs, err = jch.parse_resource_refs(
            SimpleNamespace(resource_refs='[{"ResourceId":"r-1"}]')
        )
        self.assertIsNone(refs)
        self.assertIn("Type", err)

    def test_invalid_type_value(self):
        refs, err = jch.parse_resource_refs(
            SimpleNamespace(resource_refs='[{"ResourceId":"r-1","Type":7}]')
        )
        self.assertIsNone(refs)
        self.assertIn("非法", err)

    def test_type_string_coerced_to_int(self):
        refs, err = jch.parse_resource_refs(
            SimpleNamespace(resource_refs='[{"ResourceId":"r-1","Type":"1"}]')
        )
        self.assertIsNone(err)
        self.assertEqual(refs[0]["Type"], 1)
        self.assertIsInstance(refs[0]["Type"], int)

    def test_valid_array(self):
        raw = '[{"ResourceId":"r-1","Type":1,"Version":1},{"ResourceId":"r-2","Type":0,"Version":2}]'
        refs, err = jch.parse_resource_refs(SimpleNamespace(resource_refs=raw))
        self.assertIsNone(err)
        self.assertEqual(len(refs), 2)


class TestValidateResourceRefsForJobType(unittest.TestCase):
    def test_none_passes(self):
        self.assertIsNone(jch.validate_resource_refs_for_job_type(None, jch.JOB_TYPE_SQL))

    def test_sql_with_main_rejected(self):
        refs = [{"ResourceId": "r-1", "Type": 1, "Version": 1}]
        err = jch.validate_resource_refs_for_job_type(refs, jch.JOB_TYPE_SQL)
        self.assertIsNotNone(err)
        self.assertIn("MAIN", err)

    def test_sql_with_dep_only_passes(self):
        refs = [
            {"ResourceId": "r-1", "Type": 0, "Version": 1},
            {"ResourceId": "r-2", "Type": 2, "Version": 1},
        ]
        self.assertIsNone(jch.validate_resource_refs_for_job_type(refs, jch.JOB_TYPE_SQL))

    def test_jar_without_main_rejected(self):
        refs = [{"ResourceId": "r-1", "Type": 0, "Version": 1}]
        err = jch.validate_resource_refs_for_job_type(refs, jch.JOB_TYPE_JAR)
        self.assertIsNotNone(err)
        self.assertIn("MAIN", err)

    def test_jar_with_two_main_rejected(self):
        refs = [
            {"ResourceId": "r-1", "Type": 1, "Version": 1},
            {"ResourceId": "r-2", "Type": 1, "Version": 1},
        ]
        err = jch.validate_resource_refs_for_job_type(refs, jch.JOB_TYPE_JAR)
        self.assertIsNotNone(err)
        self.assertIn("MAIN", err)

    def test_jar_with_exactly_one_main_passes(self):
        refs = [
            {"ResourceId": "r-1", "Type": 1, "Version": 1},
            {"ResourceId": "r-2", "Type": 0, "Version": 1},
        ]
        self.assertIsNone(jch.validate_resource_refs_for_job_type(refs, jch.JOB_TYPE_JAR))


class TestResolveResourceRefs(unittest.TestCase):
    def test_resolve_ok(self):
        raw = '[{"ResourceId":"r-1","Type":0,"Version":1}]'
        refs, err = jch.resolve_resource_refs(
            SimpleNamespace(resource_refs=raw), jch.JOB_TYPE_SQL, "create_job_config"
        )
        self.assertIsNone(err)
        self.assertEqual(refs[0]["ResourceId"], "r-1")

    def test_resolve_parse_error(self):
        refs, err = jch.resolve_resource_refs(
            SimpleNamespace(resource_refs="not-json"), jch.JOB_TYPE_SQL, "x"
        )
        self.assertIsNone(refs)
        self.assertEqual(err["error"]["code"], "ValidationError")

    def test_resolve_validation_error(self):
        # SQL job with MAIN entry must fail validation
        raw = '[{"ResourceId":"r-1","Type":1,"Version":1}]'
        refs, err = jch.resolve_resource_refs(
            SimpleNamespace(resource_refs=raw), jch.JOB_TYPE_SQL, "x"
        )
        self.assertIsNone(refs)
        self.assertEqual(err["error"]["code"], "ValidationError")


class TestReadSqlInput(unittest.TestCase):
    def test_inline_sql(self):
        ns = SimpleNamespace(sql="SELECT 1", sql_file=None)
        self.assertEqual(jch.read_sql_input(ns), "SELECT 1")

    def test_sql_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".sql", delete=False, encoding="utf-8"
        ) as fp:
            fp.write("SELECT '中文'")
            path = fp.name
        try:
            ns = SimpleNamespace(sql=None, sql_file=path)
            self.assertEqual(jch.read_sql_input(ns), "SELECT '中文'")
        finally:
            os.unlink(path)

    def test_neither(self):
        ns = SimpleNamespace(sql=None, sql_file=None)
        self.assertIsNone(jch.read_sql_input(ns))

    def test_missing_file(self):
        ns = SimpleNamespace(sql=None, sql_file="/nonexistent/path/does/not/exist.sql")
        self.assertIsNone(jch.read_sql_input(ns))


class TestBuildMetadataV1(unittest.TestCase):
    def test_no_variables_no_refs(self):
        meta, unresolved = jch._build_metadata_v1("SELECT 1", {})
        self.assertEqual(unresolved, [])
        self.assertEqual(meta["Metadata"]["variables"], [])
        self.assertEqual(meta["Metadata"]["referenceTables"], [])

    def test_unresolved_variable(self):
        sql = "CREATE TABLE t1 (a INT) WITH ('k' = '${myvar:fallback}');"
        meta, unresolved = jch._build_metadata_v1(sql, {})
        self.assertIn("myvar", unresolved)
        # Expect one variable entry with default value
        var_items = meta["Metadata"]["variables"]
        self.assertEqual(len(var_items), 1)
        entries = var_items[0]["variableEntries"]
        self.assertEqual(entries[0]["value"], "fallback")
        self.assertEqual(entries[0]["variableId"], "")

    def test_resolved_variable_with_value(self):
        sql = "CREATE TABLE t1 (a INT) WITH ('k' = '${myvar}');"
        resolved = {
            "myvar": {"Type": 1, "Value": "real_value", "SerialId": "var-1"}
        }
        meta, unresolved = jch._build_metadata_v1(sql, resolved)
        self.assertEqual(unresolved, [])
        entries = meta["Metadata"]["variables"][0]["variableEntries"]
        self.assertEqual(entries[0]["value"], "real_value")
        self.assertEqual(entries[0]["variableId"], "var-1")

    def test_with_reference_tables(self):
        meta, _ = jch._build_metadata_v1(
            "SELECT 1", {},
            reference_tables=[{"catalog": "c", "database": "d", "table": "t", "version": 3}],
        )
        self.assertEqual(len(meta["Metadata"]["referenceTables"]), 1)
        self.assertEqual(meta["Metadata"]["referenceTables"][0]["version"], 3)

    def test_with_catalogs(self):
        meta, _ = jch._build_metadata_v1(
            "SELECT 1", {},
            catalogs=[{"name": "hive_cat", "type": 1}],
        )
        self.assertEqual(meta["Metadata"]["catalogs"][0]["name"], "hive_cat")


class TestBuildSqlProgramArgs(unittest.TestCase):
    def test_simple_sql_no_metadata(self):
        # No region/workspace_id and no $ in SQL -> no API call, no Metadata key
        pa, unresolved, has_hive = jch.build_sql_program_args(
            existing_program_args="{}",
            sql_code="SELECT 1",
        )
        out = json.loads(pa)
        self.assertEqual(out["SqlCode"], jch.encode_sql("SELECT 1"))
        self.assertNotIn("Metadata", out)
        self.assertEqual(unresolved, [])
        self.assertFalse(has_hive)

    def test_invalid_existing_program_args(self):
        # Garbage existing program args is treated as empty dict
        pa, _, _ = jch.build_sql_program_args(
            existing_program_args="not-json",
            sql_code="SELECT 1",
        )
        out = json.loads(pa)
        self.assertIn("SqlCode", out)

    def test_preserves_existing_keys(self):
        existing = json.dumps({"OtherField": "keep_me"})
        pa, _, _ = jch.build_sql_program_args(
            existing_program_args=existing, sql_code="SELECT 1",
        )
        out = json.loads(pa)
        self.assertEqual(out["OtherField"], "keep_me")
        self.assertIn("SqlCode", out)

    def test_with_explicit_reference_tables_builds_metadata(self):
        # Even without region/workspace_id, providing ref tables triggers metadata
        # build only if we also have variables; ref-only is gated by has_refs=True
        pa, _, _ = jch.build_sql_program_args(
            existing_program_args="{}",
            sql_code="SELECT 1",
            reference_tables=[{"catalog": "c", "database": "d", "table": "t", "version": 1}],
        )
        out = json.loads(pa)
        self.assertIn("Metadata", out)
        decoded = json.loads(base64.b64decode(out["Metadata"]).decode("utf-8"))
        self.assertEqual(decoded["Metadata"]["referenceTables"][0]["table"], "t")


class TestBuildJarProgramArgs(unittest.TestCase):
    def test_strips_sql_code(self):
        existing = json.dumps({"SqlCode": "abc"})
        pa = jch.build_jar_program_args(existing)
        self.assertNotIn("SqlCode", json.loads(pa))

    def test_sets_entrypoint_and_args(self):
        pa = jch.build_jar_program_args(
            "{}", entrypoint_class="com.x.Main",
            program_args="--foo bar", resource_refs=[{"ResourceId": "r", "Type": 1, "Version": 1}],
        )
        out = json.loads(pa)
        self.assertEqual(out["EntrypointClass"], "com.x.Main")
        self.assertEqual(out["ProgramArgs"], "--foo bar")
        self.assertEqual(out["ResourceRefs"][0]["ResourceId"], "r")


class TestFormatDraftSummary(unittest.TestCase):
    def test_sql_summary(self):
        s = jch.format_draft_summary(
            jch.JOB_TYPE_SQL, sql_code="SELECT 1",
            config_params={"FlinkVersion": "Flink-1.16", "JdkVersion": "8",
                           "DefaultParallelism": 4, "Remark": "demo"},
            base_version=3,
        )
        self.assertIn("作业类型: SQL", s)
        self.assertIn("Flink-1.16", s)
        self.assertIn("基于版本: v3", s)
        self.assertIn("SELECT 1", s)
        self.assertIn("资源引用: 无", s)

    def test_jar_summary_with_resources_and_props(self):
        s = jch.format_draft_summary(
            jch.JOB_TYPE_JAR,
            entrypoint_class="com.x.Main",
            program_args="--foo bar",
            resource_refs=[{"ResourceId": "r-1", "Type": 1, "Version": 2}],
            properties=[{"Key": "k", "Value": "v"}],
        )
        self.assertIn("作业类型: JAR", s)
        self.assertIn("EntrypointClass: com.x.Main", s)
        self.assertIn("Type=1 MAIN", s)
        self.assertIn("k = v", s)


class TestConfirmDraftBeforePublish(unittest.TestCase):
    def test_skip_returns_none(self):
        self.assertIsNone(jch.confirm_draft_before_publish(
            "create_job_config", "summary", skip_flag=True, confirm_flag=False,
        ))

    def test_non_tty_without_skip_returns_safety_required(self):
        # require_confirmation will hit the non-TTY branch — force it so the
        # test never blocks on input() in an interactive terminal.
        with _force_non_tty():
            err = jch.confirm_draft_before_publish(
                "create_job_config", "summary text", skip_flag=False, confirm_flag=False,
            )
        self.assertIsNotNone(err)
        self.assertEqual(err["error"]["code"], "SafetyCheckRequired")


# ═══════════════════════════════════════════════════════════════════════════
# resource_change_ops.py
# ═══════════════════════════════════════════════════════════════════════════


class TestProcessRemoveResources(unittest.TestCase):
    def test_basic_removal(self):
        existing = [
            {"ResourceId": "r-1", "Type": 0, "Version": 1},
            {"ResourceId": "r-2", "Type": 0, "Version": 1},
            {"ResourceId": "r-3", "Type": 0, "Version": 1},
        ]
        filtered, removed = rco.process_remove_resources("r-2,r-3", existing)
        self.assertEqual([r["ResourceId"] for r in filtered], ["r-1"])
        self.assertEqual(removed, ["r-2", "r-3"])

    def test_id_not_in_existing_is_dropped(self):
        existing = [{"ResourceId": "r-1"}]
        filtered, removed = rco.process_remove_resources("r-2", existing)
        self.assertEqual(filtered, existing)
        self.assertEqual(removed, [])

    def test_strips_whitespace_and_empty(self):
        existing = [{"ResourceId": "r-1"}, {"ResourceId": "r-2"}]
        filtered, removed = rco.process_remove_resources(" r-1 , , r-2 ", existing)
        self.assertEqual(filtered, [])
        self.assertEqual(removed, ["r-1", "r-2"])


class TestFormatResourceChangesSummary(unittest.TestCase):
    def test_no_change(self):
        s = rco.format_resource_changes_summary([], [], [])
        self.assertIn("无变更", s)

    def test_full_change_set(self):
        added = [{"ResourceId": "r-new", "Type": 1, "Version": 1}]
        updated = [{"resource_id": "r-old", "file": "/tmp/x.jar"}]
        removed = ["r-gone"]
        s = rco.format_resource_changes_summary(added, updated, removed)
        self.assertIn("新增资源引用 (1 个)", s)
        self.assertIn("r-new", s)
        self.assertIn("MAIN", s)
        self.assertIn("更新资源文件 (1 个)", s)
        self.assertIn("r-old", s)
        self.assertIn("删除资源引用 (1 个)", s)
        self.assertIn("r-gone", s)


# ═══════════════════════════════════════════════════════════════════════════
# resource_resolver.py
# ═══════════════════════════════════════════════════════════════════════════


class TestResolveRegion(unittest.TestCase):
    """Only covers paths that don't call the API (canonical / empty input)."""

    def test_default_when_empty(self):
        res = rr.resolve_region(None)
        self.assertTrue(res["success"])
        self.assertEqual(res["region"], rr.DEFAULT_REGION)

    def test_already_canonical_ap(self):
        res = rr.resolve_region("ap-shanghai")
        self.assertTrue(res["success"])
        self.assertEqual(res["region"], "ap-shanghai")

    def test_already_canonical_na(self):
        res = rr.resolve_region("na-siliconvalley")
        self.assertTrue(res["success"])
        self.assertEqual(res["region"], "na-siliconvalley")

    def test_already_canonical_eu(self):
        res = rr.resolve_region("eu-frankfurt")
        self.assertTrue(res["success"])
        self.assertEqual(res["region"], "eu-frankfurt")


class TestResolveVersion(unittest.TestCase):
    def test_no_version_info_uses_defaults(self):
        res = rr.resolve_version(None)
        self.assertTrue(res["success"])
        self.assertEqual(res["flink_version"], rr.DEFAULT_FLINK_VERSION)
        self.assertEqual(res["jdk_version"], rr.DEFAULT_JDK_VERSION)

    def test_no_version_info_user_overrides(self):
        res = rr.resolve_version({}, flink_version="Flink-1.13", jdk_version="11")
        self.assertTrue(res["success"])
        self.assertEqual(res["flink_version"], "Flink-1.13")
        self.assertEqual(res["jdk_version"], "11")

    def test_supported_flink_check_passes(self):
        info = {
            "SupportedFlink": ["Flink-1.16", "Flink-1.13"],
            "JdkSupportVersion": [
                {"FlinkVersion": "Flink-1.16", "JdkVersions": ["8", "11"]},
            ],
        }
        res = rr.resolve_version(info, flink_version="Flink-1.16", jdk_version="11")
        self.assertTrue(res["success"])
        self.assertIn("8", res["supported_jdk"])

    def test_unsupported_flink_rejected(self):
        info = {"SupportedFlink": ["Flink-1.16"], "JdkSupportVersion": []}
        res = rr.resolve_version(info, flink_version="Flink-1.13")
        self.assertFalse(res["success"])
        self.assertEqual(res["error"]["code"], "UnsupportedFlinkVersion")

    def test_unsupported_jdk_rejected(self):
        info = {
            "SupportedFlink": ["Flink-1.16"],
            "JdkSupportVersion": [{"FlinkVersion": "Flink-1.16", "JdkVersions": ["8"]}],
        }
        res = rr.resolve_version(info, flink_version="Flink-1.16", jdk_version="11")
        self.assertFalse(res["success"])
        self.assertEqual(res["error"]["code"], "UnsupportedJdkVersion")


# ═══════════════════════════════════════════════════════════════════════════
# job_runtime.py
# ═══════════════════════════════════════════════════════════════════════════


class TestResolveStartMode(unittest.TestCase):
    def test_default_run_type_returns_latest(self):
        ns = SimpleNamespace(run_type=None, start_mode=None, custom_timestamp=None)
        mode, err = jrt._resolve_start_mode(ns)
        self.assertIsNone(err)
        self.assertEqual(mode, "LATEST")

    def test_run_type_4_requires_timestamp(self):
        ns = SimpleNamespace(run_type=4, start_mode=None, custom_timestamp=None)
        mode, err = jrt._resolve_start_mode(ns)
        self.assertIsNone(mode)
        self.assertEqual(err["error"]["code"], "ValidationError")

    def test_run_type_4_with_timestamp(self):
        ns = SimpleNamespace(run_type=4, start_mode=None, custom_timestamp="1700000000000")
        mode, err = jrt._resolve_start_mode(ns)
        self.assertIsNone(err)
        self.assertEqual(mode, "T1700000000000")

    def test_explicit_latest(self):
        ns = SimpleNamespace(run_type=1, start_mode="latest", custom_timestamp=None)
        mode, err = jrt._resolve_start_mode(ns)
        self.assertIsNone(err)
        self.assertEqual(mode, "LATEST")

    def test_explicit_earliest(self):
        ns = SimpleNamespace(run_type=1, start_mode="EARLIEST", custom_timestamp=None)
        mode, err = jrt._resolve_start_mode(ns)
        self.assertIsNone(err)
        self.assertEqual(mode, "EARLIEST")

    def test_explicit_t_timestamp(self):
        ns = SimpleNamespace(run_type=1, start_mode="T1234567890", custom_timestamp=None)
        mode, err = jrt._resolve_start_mode(ns)
        self.assertIsNone(err)
        self.assertEqual(mode, "T1234567890")

    def test_invalid_start_mode(self):
        ns = SimpleNamespace(run_type=1, start_mode="WHATEVER", custom_timestamp=None)
        mode, err = jrt._resolve_start_mode(ns)
        self.assertIsNone(mode)
        self.assertEqual(err["error"]["code"], "ValidationError")

    def test_valid_start_modes_constant(self):
        self.assertIn("LATEST", jrt.VALID_START_MODES)
        self.assertIn("EARLIEST", jrt.VALID_START_MODES)


# ═══════════════════════════════════════════════════════════════════════════
# job_observability.py
# ═══════════════════════════════════════════════════════════════════════════


class TestDefaultTimeRange(unittest.TestCase):
    def test_24h_window(self):
        start, end = jobs._default_time_range()
        now = int(time.time())
        # End within 5 seconds of now
        self.assertLessEqual(abs(end - now), 5)
        # Window is 24h
        self.assertEqual(end - start, 24 * 3600)


class TestBuildCosInfo(unittest.TestCase):
    def test_normal_cluster(self):
        cluster = {"LogCOSBucket": "my-log-bucket", "Region": "ap-guangzhou"}
        job = {"ClusterId": "cluster-x", "JobId": "cql-y", "Region": "ap-guangzhou"}
        res = jobs._build_cos_info(cluster, job, running_order_id="run-1")
        self.assertTrue(res["success"])
        self.assertEqual(res["bucket"], "my-log-bucket")
        self.assertEqual(res["cos_region"], "ap-guangzhou")
        self.assertEqual(
            res["path_prefix"],
            "job-running-log/cluster-x/cql-y/run-1/jobmanager/",
        )
        self.assertFalse(res["is_cdc"])

    def test_cdc_cluster(self):
        cluster = {"DefaultCOSBucket": "cdc-bucket", "Region": "ap-guangzhou", "CdcId": "cdc-abc"}
        job = {"ClusterId": "cluster-x", "JobId": "cql-y", "Region": "ap-guangzhou"}
        res = jobs._build_cos_info(cluster, job, running_order_id="run-1", component="taskmanager")
        self.assertTrue(res["success"])
        self.assertEqual(res["bucket"], "cdc-bucket")
        self.assertEqual(res["cos_region"], "cdc-abc.cos-cdc.ap-guangzhou")
        self.assertTrue(res["is_cdc"])
        self.assertIn("/taskmanager/", res["path_prefix"])

    def test_no_bucket_normal(self):
        cluster = {"LogCOSBucket": "", "Region": "ap-guangzhou"}
        job = {"ClusterId": "cluster-x", "JobId": "cql-y", "Region": "ap-guangzhou"}
        res = jobs._build_cos_info(cluster, job, running_order_id="r")
        self.assertFalse(res.get("success"))
        self.assertEqual(res["error"]["code"], "NoCOSBucket")

    def test_no_bucket_cdc(self):
        cluster = {"DefaultCOSBucket": "", "Region": "ap-guangzhou", "CdcId": "cdc-abc"}
        job = {"ClusterId": "cluster-x", "JobId": "cql-y", "Region": "ap-guangzhou"}
        res = jobs._build_cos_info(cluster, job, running_order_id="r")
        self.assertFalse(res.get("success"))
        self.assertEqual(res["error"]["code"], "NoCOSBucket")


# ═══════════════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main(verbosity=2)
