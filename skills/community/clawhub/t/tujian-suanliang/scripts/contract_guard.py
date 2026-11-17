# VENDORED from lis-skill-bus/lib/contract_guard.py sha256:e7a31a4a0beda884631a7bccd0555925ed21b54c7f3efdd3012298e3bb2b1f55
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contract_guard.py — cad-contract/v1 准入闸门（纯 stdlib，不联网）。

用途
----
算量技能在读取任何“识图契约”之前，先调用 ``guard_contract()``：

* provenance=reader/bus 且带非空 contract_id、哈希一致 -> ``formal``，可进正式台账；
* provenance=manual（或缺失）且调用方显式 ``allow_manual=True`` -> ``manual``，
  ``final_quantity=False``、``formal_ledger_eligible=False``；
* 其余情况抛 ``GuardError``，调用方应把 code/message/hint 原样给用户看。

错误码
------
1 缺依赖   2 输入不合法   3 来源未授权   4 版本或单位不一致   5 数据不足

红线
----
不联网；不读环境变量决定放行；``allow_manual`` 只能由调用方显式传参。
``source_sha256`` 是原图哈希，``contract_sha256`` 是契约文件哈希，两者分开存。

命令行
------
    python3 contract_guard.py --self-test
    python3 contract_guard.py <contract.json> [--allow-manual] [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import sys
from pathlib import Path

GUARD_VERSION = "1.0.0"
DEFAULT_SCHEMA = "cad-contract/v1"
FORMAL_PROVENANCE = {
    "reader": "reader",
    "bus": "bus",
    "cad-file-reader": "reader",
    "lis-skill-bus": "bus",
}
_SHA_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_MANUAL_COMMAND = (
    "python3 $HOME/.codex/skills/lis-skill-bus/lib/contract_guard.py {path} --allow-manual"
)


class GuardError(Exception):
    """契约闸门错误。code 见模块文档，message 给人看，hint 给可复制命令。"""

    def __init__(self, code: int, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.code = int(code)
        self.message = str(message)
        self.hint = str(hint or "")

    def __str__(self) -> str:
        text = "[GuardError %d] %s" % (self.code, self.message)
        if self.hint:
            text += "\n修复: " + self.hint
        return text


# --------------------------------------------------------------------------- #
# 基础工具
# --------------------------------------------------------------------------- #
def _nested(mapping, *keys):
    cur = mapping
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _q(value) -> str:
    return shlex.quote(str(value))


def _hint_set_schema(path: Path, schema: str) -> str:
    code = (
        "import json,sys;p=sys.argv[1];"
        "d=json.load(open(p,encoding='utf-8'));"
        "d['schema']=sys.argv[2];"
        "json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)"
    )
    return 'python3 -c "%s" %s %s' % (code, _q(path), _q(schema))


def _hint_set_unit(path: Path) -> str:
    code = (
        "import json,sys;p=sys.argv[1];"
        "d=json.load(open(p,encoding='utf-8'));"
        "d['coordinate_unit']='mm';"
        "json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)"
    )
    return 'python3 -c "%s" %s' % (code, _q(path))


def _hint_set_unit_scale(path: Path) -> str:
    code = (
        "import json,sys;p=sys.argv[1];"
        "d=json.load(open(p,encoding='utf-8'));"
        "d['unit_scale']=float(sys.argv[2]);"
        "json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)"
    )
    return '若坐标单位是 m，运行：python3 -c "%s" %s 1000；不确定就重新从 cad-file-reader 生成契约。' % (
        code,
        _q(path),
    )


def _hint_show_keys(path: Path) -> str:
    code = (
        "import json,sys;"
        "print(sorted(json.load(open(sys.argv[1],encoding='utf-8')).keys()))"
    )
    return 'python3 -c "%s" %s' % (code, _q(path))


def _hint_drop_hash(path: Path) -> str:
    code = (
        "import json,sys;p=sys.argv[1];"
        "d=json.load(open(p,encoding='utf-8'));"
        "d.pop('contract_sha256',None);"
        "json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)"
    )
    return (
        '若确认契约未被人为改动，删除过期内嵌哈希后重跑：python3 -c "%s" %s；'
        "否则请重新从 cad-file-reader 生成契约。" % (code, _q(path))
    )


def _hint_manual(path: Path) -> str:
    return "确需用手工契约时在算量入口加 --allow-manual（结果 final_quantity=false）；单独验证：" + _MANUAL_COMMAND.format(
        path=_q(path)
    )


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_contract(path: Path):
    """读契约并返回 (doc, digest, raw_size)。所有失败都转成 GuardError(2)。"""
    if not path.exists():
        raise GuardError(
            2,
            "契约文件不存在: %s" % path,
            hint="先确认路径：ls -l %s" % _q(path),
        )
    if not path.is_file():
        raise GuardError(2, "契约路径不是文件: %s" % path, hint="ls -ld %s" % _q(path))
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise GuardError(
            2,
            "契约文件读不了: %s（%s）" % (path, exc),
            hint="检查权限：ls -l %s" % _q(path),
        )
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise GuardError(
            2,
            "契约不是 UTF-8 文本: %s（%s）" % (path, exc),
            hint="另存为 UTF-8 后重跑：file %s" % _q(path),
        )
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as exc:
        raise GuardError(
            2,
            "契约 JSON 解析失败: %s 第 %d 行第 %d 列：%s"
            % (path, exc.lineno, exc.colno, exc.msg),
            hint="用 json.tool 定位：python3 -m json.tool %s" % _q(path),
        )
    if not isinstance(doc, dict):
        raise GuardError(
            2,
            "契约顶层必须是 JSON 对象，实际是 %s" % type(doc).__name__,
            hint="检查文件开头是否为 {：head -c 80 %s" % _q(path),
        )
    return doc, _sha256_bytes(raw), len(raw)


# --------------------------------------------------------------------------- #
# 字段取值（兼容顶层与常见嵌套位置）
# --------------------------------------------------------------------------- #
def _pick_provenance(doc: dict) -> str:
    candidates = [doc.get("provenance")]
    producer = doc.get("producer")
    if isinstance(producer, dict):
        candidates.append(producer.get("provenance"))
    contract = doc.get("contract")
    if isinstance(contract, dict):
        candidates.append(contract.get("provenance"))
    prov_meta = doc.get("_provenance")
    if isinstance(prov_meta, dict):
        candidates.extend([prov_meta.get("mode"), prov_meta.get("source"), prov_meta.get("source_skill")])
    for raw in candidates:
        if isinstance(raw, dict):
            raw = raw.get("mode") or raw.get("type") or raw.get("source")
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return ""


def _pick_contract_id(doc: dict) -> str:
    candidates = [
        doc.get("contract_id"),
        doc.get("contractId"),
        _nested(doc, "contract", "contract_id"),
        _nested(doc, "meta", "contract_id"),
        _nested(doc, "_provenance", "contract_id"),
    ]
    for raw in candidates:
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return ""


def _pick_embedded_hash(doc: dict):
    return doc.get("contract_sha256") or _nested(doc, "integrity", "contract_sha256")


def _pick_source_sha(doc: dict) -> str:
    candidates = [
        doc.get("source_sha256"),
        _nested(doc, "source", "sha256"),
        _nested(doc, "source", "source_sha256"),
        _nested(doc, "contract", "source_sha256"),
        _nested(doc, "contract", "source", "sha256"),
    ]
    for raw in candidates:
        if isinstance(raw, str) and raw.strip():
            return raw.strip().lower()
    return ""


def _pick_unit(doc: dict) -> str:
    candidates = [
        doc.get("coordinate_unit"),
        _nested(doc, "units", "coordinate"),
        _nested(doc, "coordinate", "unit"),
        _nested(doc, "contract", "coordinate_unit"),
        _nested(doc, "contract", "units", "coordinate"),
        _nested(doc, "source", "unit"),
    ]
    for raw in candidates:
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return ""


def _pick_unit_scale(doc: dict):
    candidates = [
        doc.get("unit_scale"),
        _nested(doc, "units", "scale"),
        _nested(doc, "contract", "unit_scale"),
        _nested(doc, "contract", "units", "scale"),
    ]
    for raw in candidates:
        if isinstance(raw, bool) or raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value > 0:
            return value
    return None


# --------------------------------------------------------------------------- #
# 主闸门
# --------------------------------------------------------------------------- #
def guard_contract(path, *, allow_manual=False, expected_schema=DEFAULT_SCHEMA,
                   required_keys=(), require_hash=True) -> dict:
    """校验契约来源与完整性。

    返回 ``{mode, provenance, contract_id, source_sha256, contract_sha256,
    warnings[], contract, formal_ledger_eligible}``；mode 只能是 formal 或 manual。
    """
    contract_path = Path(path)
    doc, digest, _size = _read_contract(contract_path)
    warnings = []

    # 1) 版本：schema / contract_version 必须等于 expected_schema
    schema = doc.get("schema")
    contract_version = doc.get("contract_version")
    if schema is None and contract_version is None:
        raise GuardError(
            4,
            "契约缺 schema/contract_version，无法确认是 %s。" % expected_schema,
            hint=_hint_set_schema(contract_path, expected_schema),
        )
    for label, value in (("schema", schema), ("contract_version", contract_version)):
        if value is not None and str(value).strip() != expected_schema:
            raise GuardError(
                4,
                "契约 %s=%r，要求 %s；版本不一致的契约不能进算量。"
                % (label, value, expected_schema),
                hint=_hint_set_schema(contract_path, expected_schema),
            )
    if schema is None:
        warnings.append(
            "契约用 contract_version 声明版本（%s），建议同时在顶层写 schema。" % contract_version
        )

    # 2) 必需顶层键
    missing = [key for key in (required_keys or ()) if key not in doc]
    if missing:
        raise GuardError(
            2,
            "契约缺顶层键: %s" % ", ".join(str(k) for k in missing),
            hint="先看现有键，再补齐缺失项：%s" % _hint_show_keys(contract_path),
        )

    # 3) 来源授权
    raw_prov = _pick_provenance(doc)
    prov_key = raw_prov.lower() if raw_prov else ""
    canonical_prov = FORMAL_PROVENANCE.get(prov_key, prov_key)
    contract_id = _pick_contract_id(doc)

    if canonical_prov in ("reader", "bus"):
        if not contract_id:
            raise GuardError(
                3,
                "来源为 reader/bus 但缺 contract_id，无法追溯，按未授权拒收。",
                hint=(
                    "用 cad-file-reader 重新生成正式契约（会自动带 contract_id）；"
                    "临时降级：" + _MANUAL_COMMAND.format(path=_q(contract_path))
                ),
            )
        mode = "formal"
    else:
        if not allow_manual:
            shown = raw_prov or "缺失（按 manual 处理）"
            raise GuardError(
                3,
                "契约 provenance=%s，不是 reader/bus，拒入正式算量。" % shown,
                hint=_hint_manual(contract_path),
            )
        mode = "manual"
        if raw_prov and prov_key != "manual":
            warnings.append("未知 provenance=%r，已按 manual 处理。" % raw_prov)
        if not raw_prov:
            warnings.append("契约未写 provenance，已按 manual 处理（final_quantity=false）。")

    # 4) 契约文件哈希（内嵌值是防替换的绊线；返回的 contract_sha256 永远是实算值）
    embedded = _pick_embedded_hash(doc)
    if embedded:
        if require_hash and str(embedded).strip().lower() != digest:
            raise GuardError(
                2,
                "contract_sha256 与契约文件实际 SHA-256 不一致：契约可能被改动或哈希过期。",
                hint=_hint_drop_hash(contract_path),
            )
    elif require_hash:
        warnings.append(
            "契约未内嵌 contract_sha256；已计算文件哈希，但无法用内嵌值防替换。"
        )
    if not require_hash:
        warnings.append("require_hash=False：跳过内嵌 contract_sha256 校验。")

    # 5) 坐标单位
    unit = _pick_unit(doc)
    unit_scale = _pick_unit_scale(doc)
    if not unit:
        raise GuardError(
            4,
            "坐标单位缺失：契约未声明 coordinate_unit，无法确认坐标是 mm。",
            hint=_hint_set_unit(contract_path),
        )
    if unit.strip().lower() != "mm":
        if unit_scale is None:
            raise GuardError(
                4,
                "坐标单位 %r 不是 mm，且未给 unit_scale（换算到 mm 的系数）。" % unit,
                hint=_hint_set_unit_scale(contract_path),
            )
        warnings.append(
            "坐标单位 %r，按 unit_scale=%s 换算为 mm；算量前务必核对。" % (unit, unit_scale)
        )
    elif unit_scale is not None and unit_scale != 1:
        warnings.append("单位已是 mm，但 unit_scale=%s；请确认是否需要换算。" % unit_scale)

    # 6) 原图哈希（只做记录与格式提醒，不替代契约哈希）
    source_sha = _pick_source_sha(doc)
    if not source_sha:
        warnings.append("契约缺 source_sha256（原图哈希），无法核对原图是否变化。")
    elif not _SHA_RE.match(source_sha):
        warnings.append("source_sha256 格式不像 64 位十六进制：%s…" % source_sha[:12])

    return {
        "mode": mode,
        "provenance": canonical_prov,
        "contract_id": contract_id,
        "source_sha256": source_sha,
        "contract_sha256": digest,
        "warnings": warnings,
        "contract": doc,
        "formal_ledger_eligible": mode == "formal",
    }


def stamp_result(result: dict, guard: dict) -> dict:
    """给算量结果补溯源字段；mode=manual 时强制 final_quantity=False。"""
    if not isinstance(result, dict):
        raise TypeError("stamp_result 需要 dict 类型的算量结果")
    if not isinstance(guard, dict) or guard.get("mode") not in ("formal", "manual"):
        raise ValueError("stamp_result 需要 guard_contract() 的返回值（mode=formal/manual）")

    result["provenance"] = guard.get("provenance") or ""
    result["contract_id"] = guard.get("contract_id") or ""
    result["source_sha256"] = guard.get("source_sha256") or ""
    result["contract_sha256"] = guard.get("contract_sha256") or ""
    result["contract_mode"] = guard.get("mode")
    result["formal_ledger_eligible"] = guard.get("mode") == "formal"
    if guard.get("mode") == "manual":
        result["final_quantity"] = False
    if guard.get("warnings"):
        result["contract_warnings"] = list(guard["warnings"])
    return result


# --------------------------------------------------------------------------- #
# 自测（不依赖 tests/fixtures，临时目录内生成 6 种输入）
# --------------------------------------------------------------------------- #
def _self_test() -> int:
    import tempfile

    checks = []

    def record(name, ok, detail):
        checks.append((name, bool(ok), detail))

    def expect(name, fn, want_mode=None, want_code=None):
        try:
            got = fn()
        except GuardError as exc:
            ok = want_code is not None and exc.code == want_code
            record(name, ok, "GuardError(%d)%s" % (exc.code, "" if ok else "，期望 %s" % want_code))
            return
        mode = got.get("mode") if isinstance(got, dict) else None
        ok = want_mode is not None and mode == want_mode
        record(name, ok, "mode=%s%s" % (mode, "" if ok else "，期望 %s" % want_mode))

    base = {
        "schema": DEFAULT_SCHEMA,
        "spec": "cad-file-reader/v0",
        "contract_id": "cad-20261109-selftest",
        "provenance": "reader",
        "coordinate_unit": "mm",
        "source": {"file": "selftest.dwg", "sha256": "ab" * 32},
    }
    manual = {
        "schema": DEFAULT_SCHEMA,
        "provenance": "manual",
        "coordinate_unit": "mm",
        "contract_id": "manual-selftest",
    }
    no_unit = {
        "schema": DEFAULT_SCHEMA,
        "provenance": "manual",
        "contract_id": "manual-selftest",
    }
    bad_hash = dict(base, contract_sha256="0" * 64)
    bad_version = dict(base, schema="cad-contract/v0")

    with tempfile.TemporaryDirectory(prefix="contract_guard_selftest_") as tmp:
        tmpdir = Path(tmp)

        def write(name, doc):
            path = tmpdir / name
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            return path

        p_formal = write("reader.json", base)
        p_manual = write("manual.json", manual)
        p_no_unit = write("no_unit.json", no_unit)
        p_bad_hash = write("bad_hash.json", bad_hash)
        p_bad_version = write("bad_version.json", bad_version)

        expect("1 合法 reader 契约 -> formal", lambda: guard_contract(p_formal), want_mode="formal")

        def case_manual():
            got = guard_contract(p_manual, allow_manual=True)
            stamped = stamp_result({"final_quantity": True, "total_t": 1.0}, got)
            assert got["mode"] == "manual", got["mode"]
            assert stamped["final_quantity"] is False, stamped
            assert stamped["formal_ledger_eligible"] is False, stamped
            return got

        expect(
            "2 手工契约+allow_manual -> manual/final_quantity=False",
            case_manual,
            want_mode="manual",
        )
        expect(
            "3 手工契约无开关 -> GuardError(3)",
            lambda: guard_contract(p_manual),
            want_code=3,
        )
        expect(
            "4 契约哈希不匹配 -> GuardError(2)",
            lambda: guard_contract(p_bad_hash),
            want_code=2,
        )
        expect(
            "5 版本 cad-contract/v0 -> GuardError(4)",
            lambda: guard_contract(p_bad_version),
            want_code=4,
        )
        expect(
            "6 单位缺失 -> GuardError(4)",
            lambda: guard_contract(p_no_unit, allow_manual=True),
            want_code=4,
        )

    passed = sum(1 for _name, ok, _detail in checks if ok)
    total = len(checks)
    for name, ok, detail in checks:
        print("  %s  %s (%s)" % ("PASS" if ok else "FAIL", name, detail))
    print("self-test: %d/%d PASS" % (passed, total))
    return 0 if passed == total else 1


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="cad-contract/v1 准入闸门（纯 stdlib，不联网）"
    )
    parser.add_argument("contract", nargs="?", help="契约 JSON 路径")
    parser.add_argument("--allow-manual", action="store_true", help="显式允许手工契约（结果 final_quantity=false）")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA, help="期望的契约版本，默认 cad-contract/v1")
    parser.add_argument("--require-key", action="append", default=[], help="要求存在的顶层键，可重复")
    parser.add_argument("--no-require-hash", action="store_true", help="跳过内嵌 contract_sha256 校验")
    parser.add_argument("--self-test", action="store_true", help="跑内置 6 项自测")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON（含 contract）")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()
    if not args.contract:
        parser.error("需要契约路径，或用 --self-test")

    try:
        guard = guard_contract(
            args.contract,
            allow_manual=args.allow_manual,
            expected_schema=args.schema,
            required_keys=tuple(args.require_key),
            require_hash=not args.no_require_hash,
        )
    except GuardError as exc:
        print("GuardError(%d): %s" % (exc.code, exc.message), file=sys.stderr)
        if exc.hint:
            print("修复: %s" % exc.hint, file=sys.stderr)
        return exc.code

    if args.json:
        print(json.dumps(guard, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            "mode=%s provenance=%s contract_id=%s formal_ledger_eligible=%s"
            % (
                guard["mode"],
                guard["provenance"],
                guard["contract_id"] or "-",
                guard["formal_ledger_eligible"],
            )
        )
        print("source_sha256=%s" % (guard["source_sha256"] or "-"))
        print("contract_sha256=%s" % guard["contract_sha256"])
        for warning in guard["warnings"]:
            print("WARN: %s" % warning)
    return 0


if __name__ == "__main__":
    sys.exit(main())
