from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    required_paths = [
        repo_root / "SKILL.md",
        repo_root / "README.md",
        repo_root / "skill.json",
        repo_root / "manifest.json",
        repo_root / "data" / "historical_cases.json",
        repo_root / "data" / "user_cases.json",
        repo_root / "examples" / "case_submission_template.json",
        repo_root / "prompts" / "add_case_intake.md",
        repo_root / "prompts" / "sandbox_simulation.md",
        repo_root / "scripts" / "add_case.py",
        repo_root / "src" / "case_store.py",
        repo_root / "src" / "main.py",
        repo_root / "tests" / "test_cli.py",
    ]

    missing = [str(path.relative_to(repo_root)) for path in required_paths if not path.exists()]
    if missing:
        print("缺少关键文件:", ", ".join(missing), file=sys.stderr)
        return 1

    skill_metadata = json.loads((repo_root / "skill.json").read_text(encoding="utf-8"))
    if skill_metadata.get("slug") != "yi-shi-wei-jian":
        print("skill.json 中的 slug 不正确。", file=sys.stderr)
        return 1

    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "src" / "main.py"),
            "--question",
            "公司内部出现派系对抗，我资源偏弱，但必须推进一项涉及利益调整的新制度。",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    template_result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "src" / "main.py"),
            "--print-case-template",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )
    if template_result.returncode != 0:
        print(template_result.stderr, file=sys.stderr)
        return template_result.returncode
    if '"id": "new-historical-case-id"' not in template_result.stdout:
        print("新增案例模板输出不正确。", file=sys.stderr)
        return 1

    required_sections = [
        "【局面判断】",
        "【历史参照】",
        "【关键变量】",
        "【可选路径】",
        "【沙盘推演】",
        "【借鉴原则】",
        "【边界提醒】",
    ]
    for section in required_sections:
        if section not in result.stdout:
            print(f"CLI 输出缺少 section: {section}", file=sys.stderr)
            return 1

    print("安装验证通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
