from __future__ import annotations

import sys
from pathlib import Path

def doctor(root: Path) -> dict:
    rules = root.parent / "rules" / "scan-rules.json"
    return {"schema_version":"1.0", "operation":"doctor", "status":"completed", "offline_scan":"ready" if rules.exists() else "unavailable", "file_redaction":"ready", "endpoint_audit":"missing_configuration", "response_filter":"not_attached", "execution_gate":"not_attached", "system_sandbox":"unverified", "runtime":{"python":sys.version.split()[0]}, "limitations":["未接入宿主全局拦截；端点体检需单独本地配置"], "summary":"钟馗卫士状态已检查"}

