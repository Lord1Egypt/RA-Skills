"""JUnit XML renderer."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from .model import Report, Status


def render_junit(report: Report, path: Path) -> Path:
    data = report.to_dict()
    checks = data["checks"]
    failures = sum(1 for check in checks if check["status"] == Status.FAIL.value)
    errors = sum(1 for check in checks if check["status"] == Status.ERROR.value)
    skipped = sum(1 for check in checks if check["status"] in (Status.SKIP.value, Status.UNKNOWN.value))
    total_time = sum(float(check.get("duration_ms") or 0) for check in checks) / 1000.0

    suite = ET.Element(
        "testsuite",
        {
            "name": "ue-audit",
            "tests": str(len(checks)),
            "failures": str(failures),
            "errors": str(errors),
            "skipped": str(skipped),
            "time": f"{total_time:.3f}",
        },
    )
    properties = ET.SubElement(suite, "properties")
    for name, value in (
        ("run_id", data["run_id"]),
        ("tool", f"{data['tool']} {data['tool_version']}"),
        ("project", str(data["project"].get("root", ""))),
        ("manifest_sha256", str(data["readonly_proof"].get("after_manifest_sha256", ""))),
    ):
        ET.SubElement(properties, "property", {"name": name, "value": value})

    for check in checks:
        case = ET.SubElement(
            suite,
            "testcase",
            {
                "classname": "ue_audit.checks",
                "name": f"{check['check_id']} {check['title']}",
                "time": f"{float(check.get('duration_ms') or 0) / 1000.0:.3f}",
            },
        )
        status = check["status"]
        summary = str(check.get("summary") or "")
        if status == Status.FAIL.value:
            failure = ET.SubElement(case, "failure", {"message": summary or "check failed"})
            failure.text = "\n".join(
                f"{finding['severity']}: {finding['title']}: {finding['message']}"
                for finding in check.get("findings", [])
            )
        elif status == Status.ERROR.value:
            error = ET.SubElement(case, "error", {"message": summary or "check error"})
            error.text = summary
        elif status in (Status.SKIP.value, Status.UNKNOWN.value):
            ET.SubElement(case, "skipped", {"message": summary or status})
        else:
            output = ET.SubElement(case, "system-out")
            output.text = summary

    tree = ET.ElementTree(suite)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        ET.indent(tree, space="  ")
    except AttributeError:
        pass
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return path
