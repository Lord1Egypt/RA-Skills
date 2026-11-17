#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contract_support.py — 算量技能共用支撑（纯 stdlib，不联网，不下载）。

职责只有五件：
1. 探测 cad-file-reader / lis-skill-bus 是否就绪（只读，不自动安装）；
2. 生成统一 run_manifest；
3. 写 JSON sidecar（原子替换）；
4. 生成 site_handoff.json（下游布置图/吊装用，不改主输出口径）；
5. 输出可复制的安装命令。

识别与契约校验不在这里做：识图由 cad-file-reader 负责，准入由 contract_guard 负责。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

READER_MIN = "0.41.0"
BUS_MIN = "0.1.11"
PYTHON_MIN = (3, 10)
INSTALL_HINT = (
    "skillhub install cad-file-reader --namespace user_43faedd6\n"
    "bash ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/install_skillbus.sh --apply"
)
HANDOFF_SCHEMA = "site-handoff/v1"


def _first_dir(candidates):
    for cand in candidates:
        if not cand:
            continue
        path = Path(str(cand)).expanduser()
        if (path / "scripts").is_dir():
            return path.resolve()
    return None


def _sandbox_root():
    """测试沙箱：设置 CODEX_SKILLS_ROOT 后只搜索该目录，与 entry_gate 判定一致。"""
    raw = str(os.environ.get("CODEX_SKILLS_ROOT") or "").strip()
    if not raw:
        return None
    return Path(raw).expanduser().resolve()


def find_reader():
    sandbox = _sandbox_root()
    if sandbox is not None:
        return _first_dir([sandbox / "cad-file-reader"])
    return _first_dir([
        os.environ.get("CAD_FILE_READER_HOME"),
        os.environ.get("CAD_SKILL_DIR"),
        Path.home() / ".codex" / "skills" / "cad-file-reader",
        Path.home() / ".claude" / "skills" / "cad-file-reader",
        *sorted(Path.home().glob(".workbuddy/skills/*/cad-file-reader")),
    ])


def find_bus():
    sandbox = _sandbox_root()
    if sandbox is not None:
        return _first_dir([sandbox / "lis-skill-bus"])
    return _first_dir([
        os.environ.get("SKILLBUS_HOME"),
        Path.home() / ".codex" / "skills" / "lis-skill-bus",
        Path.home() / ".claude" / "skills" / "lis-skill-bus",
    ])


def _manifest_version(root):
    """版本优先级：manifest.json → _meta.json → skillbus.py 的 VERSION。

    bus 分发包常只有 _meta.json（平台发布版本）；代码内 VERSION 可能落后，
    两者不一致时以 _meta.json 为准，并在 check_deps 里给出 warning。
    """
    if root is None:
        return ""
    for name in ("manifest.json", "_meta.json"):
        try:
            data = json.loads((root / name).read_text(encoding="utf-8"))
        except Exception:
            continue
        version = str(data.get("version") or "").strip()
        if version:
            return version
    return _code_version(root)


def _code_version(root):
    if root is None:
        return ""
    for rel in (Path("skillbus.py"), Path("scripts") / "skillbus.py", Path("__init__.py")):
        path = root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        match = re.search(r'VERSION\s*=\s*["\']([0-9][^"\']*)["\']', text)
        if match:
            return match.group(1)
    return ""


def _ver_tuple(text):
    parts = []
    for piece in str(text or "").split("."):
        try:
            parts.append(int(piece))
        except ValueError:
            break
    return tuple(parts)


def _at_least(actual, minimum):
    if not actual:
        return False
    a, m = _ver_tuple(actual), _ver_tuple(minimum)
    if not a or not m:
        return False
    width = max(len(a), len(m))
    return a + (0,) * (width - len(a)) >= m + (0,) * (width - len(m))


def check_deps(require_reader=True, require_bus=True):
    """返回依赖状态；只读，不触发任何安装或下载。"""
    reader = find_reader()
    bus = find_bus()
    reader_version = _manifest_version(reader)
    bus_version = _manifest_version(bus)
    missing = []
    problems = []
    if require_reader:
        if reader is None:
            missing.append("cad-file-reader>=%s" % READER_MIN)
        elif reader_version and not _at_least(reader_version, READER_MIN):
            problems.append("cad-file-reader 版本 %s < %s" % (reader_version, READER_MIN))
    if require_bus:
        if bus is None:
            missing.append("lis-skill-bus>=%s" % BUS_MIN)
        elif bus_version and not _at_least(bus_version, BUS_MIN):
            problems.append("lis-skill-bus 版本 %s < %s" % (bus_version, BUS_MIN))
    python_ok = sys.version_info[:2] >= PYTHON_MIN
    if not python_ok:
        problems.append("Python %d.%d < %d.%d" % (
            sys.version_info[0], sys.version_info[1], PYTHON_MIN[0], PYTHON_MIN[1]))
    ok = not missing and not problems
    warnings = []
    code_version = _code_version(bus)
    if bus is not None and bus_version and code_version and bus_version != code_version:
        warnings.append("lis-skill-bus 发布版本 %s 与代码 VERSION %s 不一致（已知遗留，按发布版本判定）"
                        % (bus_version, code_version))
    return {
        "ok": ok,
        "ready_for_formal_pipeline": ok,
        "cad_file_reader": {
            "found": reader is not None,
            "path": str(reader or ""),
            "version": reader_version,
            "min": READER_MIN,
        },
        "lis_skill_bus": {
            "found": bus is not None,
            "path": str(bus or ""),
            "version": bus_version,
            "code_version": _code_version(bus),
            "min": BUS_MIN,
        },
        "python": {
            "version": "%d.%d.%d" % sys.version_info[:3],
            "min": "%d.%d" % PYTHON_MIN,
            "ok": python_ok,
        },
        "missing": missing,
        "problems": problems,
        "warnings": warnings,
        "install_hint": INSTALL_HINT,
    }


def format_deps(status):
    lines = ["前置依赖检查（只读，不自动安装）", ""]
    for key, label in (("cad_file_reader", "cad-file-reader"),
                       ("lis_skill_bus", "lis-skill-bus")):
        row = status.get(key) or {}
        flag = "OK" if row.get("found") else "MISSING"
        version = row.get("version") or "版本未知"
        lines.append("  [%s] %s %s  %s" % (flag, label, version, row.get("path") or ""))
    py = status.get("python") or {}
    lines.append("  [%s] python %s（要求 >= %s）" % (
        "OK" if py.get("ok") else "FAIL", py.get("version"), py.get("min")))
    for problem in status.get("problems") or []:
        lines.append("  [FAIL] " + problem)
    for warning in status.get("warnings") or []:
        lines.append("  [WARN] " + warning)
    if not status.get("ok"):
        lines += ["", "缺依赖或版本不足。复制执行：", INSTALL_HINT]
    else:
        lines += ["", "正式链路就绪：cad-file-reader → lis-skill-bus → 算量技能"]
    return "\n".join(lines)


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, data):
    """原子写 JSON，避免中断留下半个文件。"""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=target.name + ".", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp, target)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return target


def run_manifest(skill, skill_version, guard=None, argv=None, extra_requires=None):
    guard = guard or {}
    requires = {
        "skills": {"cad-file-reader": ">=%s" % READER_MIN,
                   "lis-skill-bus": ">=%s" % BUS_MIN},
        "python": ">=3.10",
    }
    if extra_requires:
        requires.update(extra_requires)
    return {
        "schema": "run-manifest/v1",
        "entry_policy": "contract-only",
        "manual_requires_flag": True,
        "skill": skill,
        "skill_version": skill_version,
        "generated_at": now_iso(),
        "argv": list(sys.argv[1:] if argv is None else argv),
        "contract_id": guard.get("contract_id") or "",
        "source_sha256": guard.get("source_sha256") or "",
        "contract_sha256": guard.get("contract_sha256") or "",
        "provenance": guard.get("provenance") or "manual",
        "reader_version": guard.get("reader_version") or "",
        "requires": requires,
    }


def provenance_fields(guard):
    guard = guard or {}
    mode = guard.get("mode") or "manual"
    return {
        "provenance": guard.get("provenance") or "manual",
        "contract_id": guard.get("contract_id") or "",
        "source_sha256": guard.get("source_sha256") or "",
        "contract_sha256": guard.get("contract_sha256") or "",
        "reader_version": guard.get("reader_version") or "",
        "final_quantity": bool(guard.get("formal_ledger_eligible")) if mode == "formal" else False,
        "formal_ledger_eligible": bool(guard.get("formal_ledger_eligible")) if mode == "formal" else False,
    }


def handoff_member(member_id, *, weight_t=None, length_m=None, section="", grade="",
                   x_m=None, y_m=None, z_m=None, zone="",
                   weight_basis="unknown", coord_status="missing", **extra):
    if weight_t is None:
        weight_basis = "unknown"
    if x_m is None or y_m is None:
        coord_status = "missing"
    row = {
        "id": str(member_id or ""),
        "weight_t": weight_t,
        "length_m": length_m,
        "section": str(section or ""),
        "grade": str(grade or ""),
        "x_m": x_m,
        "y_m": y_m,
        "z_m": z_m,
        "zone": str(zone or ""),
        "weight_basis": weight_basis,
        "coord_status": coord_status,
    }
    row.update(extra)
    return row


def build_handoff(project, specialty, guard, members):
    guard = guard or {}
    return {
        "schema": HANDOFF_SCHEMA,
        "project": str(project or ""),
        "contract_id": guard.get("contract_id") or "",
        "source_sha256": guard.get("source_sha256") or "",
        "specialty": specialty,
        "generated_at": now_iso(),
        "members": list(members or []),
    }


def write_handoff(out_dir, project, specialty, guard, members):
    return write_json(Path(out_dir) / "site_handoff.json",
                      build_handoff(project, specialty, guard, members))
