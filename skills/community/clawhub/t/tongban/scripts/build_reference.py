#!/usr/bin/env python3
"""Build compact Markdown and department references for the skill."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict[str, str]]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = read_jsonl(Path(args.input))
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    departments = {}
    by_department = collections.defaultdict(list)
    for row in rows:
        departments[row["department_code"]] = {
            "code": row["department_code"],
            "name": row["department_name"],
            "short_name": row["department_short_name"],
        }
        by_department[row["department_code"]].append(row)

    (out_dir / "departments.json").write_text(
        json.dumps(sorted(departments.values(), key=lambda d: d["code"]), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# 上海一网通办市级事项索引",
        "",
        "本索引用于快速定位部门和事项。详情以官方一网通办页面和 021-12345 为准。",
        "",
        "## 使用方法",
        "",
        "1. 用用户描述中的关键词在本文件和 `service_items.jsonl` 中检索。",
        "2. 同时检索个人/法人；如果身份明确，优先对应身份。",
        "3. 返回候选事项时附 `guide_url` 和线上办理标记。",
        "",
        "## 部门摘要",
        "",
    ]

    for code in sorted(by_department):
        dept = departments[code]
        rows_for_dept = by_department[code]
        personal = sum(1 for row in rows_for_dept if row["role"] == "个人")
        legal = sum(1 for row in rows_for_dept if row["role"] == "法人")
        online = sum(1 for row in rows_for_dept if row["online_available"] == "true")
        lines.append(f"### {dept['short_name']}（{dept['name']}，{code}）")
        lines.append("")
        lines.append(f"- 个人事项：{personal}；法人事项：{legal}；标记可网上办理：{online}")
        examples = rows_for_dept[:8]
        for row in examples:
            lines.append(
                f"- [{row['role']}] {row['item_name']} / {row['subitem_name']} | "
                f"{row['item_type']} | 网上办理：{row['st_net'] or '未知'} | {row['guide_url']}"
            )
        lines.append("")

    (out_dir / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote index and {len(departments)} departments to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
