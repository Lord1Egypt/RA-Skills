#!/usr/bin/env python3
"""
Install skill bundles from skills.csv.
"""
import argparse
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


BUNDLE_INFO: List[Dict[str, str]] = [
    {
        "id": "thinktank-core",
        "name": "智库研究核心包",
        "purpose": "覆盖信息获取、文档处理、分析和基础交付，是默认主力技能包。",
    },
    {
        "id": "academic-research-plus",
        "name": "学术研究增强包",
        "purpose": "用于补强 arXiv、Google Scholar、论文精读和论文对比等学术研究场景。",
    },
    {
        "id": "monitoring-and-insight",
        "name": "动态监测增强包",
        "purpose": "用于新闻跟踪、趋势观察，以及补充搜索与网页抓取等持续监测类任务。",
    },
    {
        "id": "analysis-modeling-plus",
        "name": "分析建模增强包",
        "purpose": "用于市场分析、商业分析框架、SWOT 和数据分析等研究建模任务。",
    },
    {
        "id": "delivery-plus",
        "name": "材料转换与展示增强包",
        "purpose": "用于处理非常规输入材料和展示化输出，比如扫描版 PDF 转 Word、文章转信息图。",
    },
]

MODE_INFO: Dict[str, str] = {
    "restricted": "默认模式：不安装需要 API Key 或依赖中国以外网络的 skill。",
    "standard": "完整模式：安装 bundle 中全部 keep=yes 的 skill。",
}

REQUIRED_COLUMNS = {
    "bundle_id",
    "slug",
    "keep",
    "restricted_keep",
}


def load_skills(csv_file: Path) -> List[dict]:
    """Load and parse the skills.csv configuration."""
    if not csv_file.exists():
        print(f"Error: {csv_file} not found", file=sys.stderr)
        sys.exit(1)

    with csv_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            print(
                f"Error: {csv_file} is missing required columns: {', '.join(sorted(missing))}",
                file=sys.stderr,
            )
            sys.exit(1)
        return list(reader)


def is_keep(row: dict) -> bool:
    return row.get("keep", "").strip().lower() in {"yes", "true", "1"}


def is_restricted_keep(row: dict) -> bool:
    value = row.get("restricted_keep", "").strip().lower()
    if value not in {"yes", "no", "true", "false", "1", "0"}:
        slug = row.get("slug", "<unknown>")
        print(
            f"Error: invalid restricted_keep value for {slug}: {row.get('restricted_keep', '')}",
            file=sys.stderr,
        )
        sys.exit(1)
    return value in {"yes", "true", "1"}


def bundle_meta(bundle_id: str) -> Dict[str, str] | None:
    for bundle in BUNDLE_INFO:
        if bundle["id"] == bundle_id:
            return bundle
    return None


def command_exists(command: str) -> bool:
    return resolve_command(command) is not None


def resolve_command(command: str) -> str | None:
    resolved = shutil.which(command)
    if resolved:
        return resolved

    probe_cmd = f"where {command}" if os.name == "nt" else f"command -v {command}"
    probe = subprocess.run(
        probe_cmd,
        shell=True,
        text=True,
        capture_output=True,
    )
    if probe.returncode != 0:
        return None

    for line in probe.stdout.splitlines():
        candidate = line.strip()
        if candidate:
            return candidate
    return None


def powershell_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def run_cli_command(
    command: str,
    args: List[str],
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        shell_path = resolve_command("pwsh") or resolve_command("powershell")
        if not shell_path:
            print(
                "Error: no PowerShell executable found to run CLI commands on Windows.",
                file=sys.stderr,
            )
            sys.exit(1)

        command_expr = "& " + " ".join(powershell_quote(part) for part in [command, *args])
        return subprocess.run(
            [shell_path, "-NoProfile", "-Command", command_expr],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            cwd=str(cwd) if cwd else None,
        )

    shell_path = resolve_command("bash") or resolve_command("sh")
    if not shell_path:
        print(
            "Error: no bash/sh executable found to run CLI commands.",
            file=sys.stderr,
        )
        sys.exit(1)

    import shlex
    command_expr = " ".join(shlex.quote(part) for part in [command, *args])
    return subprocess.run(
        [shell_path, "-lc", command_expr],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        cwd=str(cwd) if cwd else None,
    )


def combined_output(result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(part for part in [result.stdout, result.stderr] if part).strip()


def default_install_workdir() -> Path:
    return Path.home() / ".agents"


def resolve_install_target(workdir: str, skills_dir: str) -> Tuple[Path, str, Path]:
    workdir_path = Path(workdir).expanduser().resolve()
    skills_dir_norm = skills_dir.strip().replace("\\", "/").strip("/")
    if not skills_dir_norm:
        print("Error: install dir must not be empty.", file=sys.stderr)
        sys.exit(1)

    install_path = workdir_path.joinpath(*skills_dir_norm.split("/"))
    return workdir_path, skills_dir_norm, install_path


def list_bundles(rows: List[dict]) -> None:
    """Print available bundles with their descriptions."""
    print("Available bundles:")
    print(f"Default mode: restricted")
    print(f"  {MODE_INFO['restricted']}")
    print(f"  如需完整安装，可使用 --mode standard")
    print()
    for bundle in BUNDLE_INFO:
        bundle_id = bundle["id"]
        standard_count = sum(
            1
            for row in rows
            if is_keep(row) and row.get("bundle_id", "").strip() == bundle_id
        )
        restricted_count = sum(
            1
            for row in rows
            if is_keep(row)
            and is_restricted_keep(row)
            and row.get("bundle_id", "").strip() == bundle_id
        )
        print(
            f"  - {bundle_id} | {bundle['name']} "
            f"(restricted {restricted_count} / standard {standard_count})"
        )
        print(f"    {bundle['purpose']}")


def get_bundle_skills(rows: List[dict], bundle_id: str, mode: str) -> List[str]:
    """Get skill slugs for a specific bundle under the selected mode."""
    skills = [
        row["slug"].strip()
        for row in rows
        if is_keep(row)
        and row.get("bundle_id", "").strip() == bundle_id
        and row.get("slug")
        and (mode == "standard" or is_restricted_keep(row))
    ]
    return skills


def bundle_exists(bundle_id: str) -> bool:
    return bundle_meta(bundle_id) is not None


def collect_skills(rows: List[dict], bundle_ids: List[str], mode: str) -> Tuple[List[str], List[str]]:
    """Collect and deduplicate skills from multiple bundles."""
    seen: Set[str] = set()
    skills: List[str] = []
    empty_bundles: List[str] = []

    for bundle_id in bundle_ids:
        if not bundle_exists(bundle_id):
            print(f"Error: Unknown bundle: {bundle_id}", file=sys.stderr)
            print(file=sys.stderr)
            list_bundles(rows)
            sys.exit(1)

        bundle_skills = get_bundle_skills(rows, bundle_id, mode)
        if not bundle_skills:
            empty_bundles.append(bundle_id)
            continue

        for slug in bundle_skills:
            if slug not in seen:
                seen.add(slug)
                skills.append(slug)

    return skills, empty_bundles


def install_skills(skills: List[str], registry: str, workdir: str, skills_dir: str) -> None:
    """Install skills using clawdhub CLI."""
    if not skills:
        print("Error: No skill slugs found for the selected bundle(s).", file=sys.stderr)
        sys.exit(1)

    if not command_exists("clawdhub"):
        print(
            "Error: clawdhub command not found. Please install clawdhub CLI first.",
            file=sys.stderr,
        )
        sys.exit(1)

    workdir_path, skills_dir_norm, install_path = resolve_install_target(workdir, skills_dir)
    workdir_path.mkdir(parents=True, exist_ok=True)
    install_path.mkdir(parents=True, exist_ok=True)

    print(f"Install target: {install_path}")
    print("Skills to install:")
    for slug in skills:
        print(f"  - {slug}")
    print()

    for slug in skills:
        print(f"Installing {slug}...")
        result = run_cli_command(
            "clawdhub",
            [
                "--workdir",
                str(workdir_path),
                "--dir",
                skills_dir_norm,
                "install",
                slug,
                "--no-input",
                f"--registry={registry}",
            ],
            cwd=workdir_path,
        )
        if result.returncode == 0:
            stdout = combined_output(result)
            if stdout:
                print(stdout)
            continue

        output = combined_output(result)
        already_installed = "Already installed:" in output
        if already_installed:
            print(output)
            print(f"Skipping {slug}; already installed.")
            continue

        not_found = "SkillsHubNotFound" in output or f"skill not found: {slug}" in output
        can_fallback = registry == "https://cn.clawhub-mirror.com" and not_found

        if can_fallback:
            print(f"Mirror missing {slug}; falling back to clawdhub official registry...")
            fallback_result = run_cli_command(
                "clawdhub",
                [
                    "--workdir",
                    str(workdir_path),
                    "--dir",
                    skills_dir_norm,
                    "install",
                    slug,
                    "--no-input",
                    "--registry=https://clawhub.ai",
                ],
                cwd=workdir_path,
            )
            if fallback_result.returncode == 0:
                fallback_output = combined_output(fallback_result)
                if fallback_output:
                    print(fallback_output)
                continue

            print(combined_output(fallback_result), file=sys.stderr)
            print(
                f"Error installing {slug}: official-registry fallback failed with exit code {fallback_result.returncode}.",
                file=sys.stderr,
            )
            sys.exit(1)

        if output:
            print(output, file=sys.stderr)
        print(
            f"Error installing {slug}: clawdhub install failed with exit code {result.returncode}.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install skill bundles from skills.csv",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("bundles", nargs="*", help="Bundle IDs to install")
    parser.add_argument("--list", action="store_true", help="List available bundles")
    parser.add_argument(
        "--mode",
        choices=["restricted", "standard"],
        default="restricted",
        help="Install mode (default: restricted)",
    )
    parser.add_argument("--registry", default="https://cn.clawhub-mirror.com", help="Registry URL")
    parser.add_argument(
        "--workdir",
        default=str(default_install_workdir()),
        help="ClawdHub workdir (default: ~/.agents)",
    )
    parser.add_argument(
        "--dir",
        default="skills",
        help="Skills directory relative to --workdir (default: skills)",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    csv_file = skill_dir / "skills.csv"
    rows = load_skills(csv_file)

    if args.list:
        list_bundles(rows)
        return

    if not args.bundles:
        parser.print_help()
        print()
        list_bundles(rows)
        sys.exit(1)

    print(f"Selected bundles: {' '.join(args.bundles)}")
    print(f"Install mode: {args.mode}")
    print(f"  {MODE_INFO[args.mode]}")
    workdir_path, skills_dir_norm, install_path = resolve_install_target(args.workdir, args.dir)
    print(f"Install destination: {install_path}")
    skills, empty_bundles = collect_skills(rows, args.bundles, args.mode)

    for bundle_id in empty_bundles:
        print(
            f"Note: {bundle_id} has no installable skills under mode={args.mode}.",
            file=sys.stderr,
        )

    if not skills:
        print(
            f"Error: none of the selected bundles have installable skills under mode={args.mode}.",
            file=sys.stderr,
        )
        sys.exit(1)

    install_skills(skills, args.registry, str(workdir_path), skills_dir_norm)


if __name__ == "__main__":
    main()
