#!/usr/bin/env python3
"""Fixture test for bounded project profile detection."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "analyze_project_profile.py"
spec = importlib.util.spec_from_file_location("project_profile", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

if module.yaml is None:
    print(json.dumps({"result": "skipped", "reason": "PyYAML not installed", "remediation": "pip install pyyaml"}, ensure_ascii=False))
    raise SystemExit(0)


def main() -> None:
    project = Path(tempfile.mkdtemp(prefix="project-profile-"))
    (project / "package.json").write_text(json.dumps({"dependencies": {"react": "18.3.1", "react-dom": "18.3.1"}}), encoding="utf-8")
    (project / "src").mkdir()
    (project / "src" / "App.tsx").write_text("export default function App() { return null }", encoding="utf-8")
    (project / "src" / "worker.py").write_text("print('fixture')", encoding="utf-8")
    (project / ".audit-snapshots").mkdir()
    (project / ".audit-snapshots" / "ignored.py").write_text("print('ignored')", encoding="utf-8")
    (project / ".codex-plugin").mkdir()
    (project / ".codex-plugin" / "plugin.json").write_text("{}", encoding="utf-8")
    report = module.detect(project, max_files=20, max_depth=4)
    ids = {item["id"] for item in report["detected_technologies"]}
    assert "react" in ids
    assert "python" in ids
    assert any(item["type"] == "AI Agent 工具开发" for item in report["inferred_project_types"])
    assert any(item["project_type"] == "Web前端-React" for item in report["recommendations"])
    python_evidence = next(item for item in report["detected_technologies"] if item["id"] == "python")["evidence"]
    assert not any(".audit-snapshots" in item["path"] for item in python_evidence)
    assert report["limits"]["truncated"] is False
    assert isinstance(report["fingerprint_errors"], list)
    assert report["mode"] == "read_only"
    empty_project = Path(tempfile.mkdtemp(prefix="project-profile-empty-"))
    empty_report = module.detect(empty_project, max_files=20, max_depth=4)
    assert [item["project_type"] for item in empty_report["recommendations"]] == ["通用"]
    print(json.dumps({"result": "passed", "detected": len(ids), "recommendations": len(report["recommendations"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
