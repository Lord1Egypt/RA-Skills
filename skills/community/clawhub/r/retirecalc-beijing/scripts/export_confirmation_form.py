#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fmt(v: object) -> str:
    if v is None:
        return ""
    return str(v)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export manual confirmation form from ingested json.")
    parser.add_argument("--input", required=True, help="ingested json path")
    parser.add_argument("--output", required=True, help="markdown output path")
    args = parser.parse_args()

    data = load_json(Path(args.input))
    payload = data.get("payload", {})
    person = payload.get("person", {})
    current = payload.get("current", {})
    review = data.get("review", {})
    conf = review.get("field_confidence", {})
    low = set(review.get("low_confidence_fields", []))

    fields = [
        ("name", person.get("name", "")),
        ("birth_date", person.get("birth_date", "")),
        ("category", person.get("category", "")),
        ("as_of", current.get("as_of", "")),
        ("actual_contribution_months", current.get("actual_contribution_months", "")),
        ("deemed_contribution_months", current.get("deemed_contribution_months", "")),
        ("actual_pre_1998_07_months", current.get("actual_pre_1998_07_months", "")),
        ("personal_account_balance", current.get("personal_account_balance", "")),
        ("z_actual", current.get("z_actual", "")),
        ("unemployment_benefit_months", current.get("unemployment_benefit_months", "")),
        ("employment_type", current.get("employment_type", "")),
        ("is_4050_eligible", current.get("is_4050_eligible", "")),
        ("subsidy_already_used_months", current.get("subsidy_already_used_months", "")),
        ("subsidy_insurances", current.get("subsidy_insurances", "")),
    ]

    lines = []
    lines.append("# 退休金测算字段确认表")
    lines.append("")
    lines.append(f"- 输入文件: `{data.get('source', {}).get('input_file', '')}`")
    lines.append(f"- 输入格式: `{data.get('source', {}).get('input_format', '')}`")
    lines.append(f"- 需人工确认: `{str(review.get('needs_manual_confirmation', False)).lower()}`")
    lines.append("")
    lines.append("| 字段 | 当前值 | 置信度 | 需确认 | 确认后值 |")
    lines.append("|---|---:|---:|---|---|")

    for k, v in fields:
        c = float(conf.get(k, 0.0))
        need = "YES" if k in low else "NO"
        lines.append(f"| `{k}` | `{fmt(v)}` | `{c:.2f}` | `{need}` |  |")

    lines.append("")
    lines.append("## 说明")
    lines.append("- `YES` 字段建议人工核对后再计算。")
    lines.append("- 若修改值，请直接填写“确认后值”，并同步回写到测算输入JSON。")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
