#!/usr/bin/env python3
"""
init_project.py — 初始化项目的 Synapse + Pipeline 环境

用法:
    python3 init_project.py /path/to/project

执行内容:
1. 检测 .git/ 存在
2. 调用 scaffold.py 创建 .knowledge/ .synapse/ 目录
3. 调用 gitnexus analyze --force 建图
4. 创建 pipeline 项目
"""

import sys
import subprocess
from pathlib import Path


def check_git_repo(project: Path) -> bool:
    """Check if project is a git repository."""
    git_dir = project / ".git"
    if not git_dir.exists():
        print(f"Error: {project} is not a git repository")
        return False
    return True


def verify_scaffold_contract(project: Path) -> tuple[bool, list]:
    """验证 scaffold 产出是否符合合约

    Required files:
    - .knowledge/CLAUDE.md
    - .knowledge/log.md
    - .knowledge/index.md
    - .synapse/memory/

    Returns: (passed, violations)
    """
    required = [
        ".knowledge/CLAUDE.md",
        ".knowledge/log.md",
        ".knowledge/index.md",
        ".synapse/memory/",
    ]
    violations = []
    for path in required:
        if not (project / path).exists():
            violations.append(f"Missing: {path}")
    return len(violations) == 0, violations


def run_scaffold(project: Path) -> bool:
    """Run synapse-core scaffold.py."""
    scaffold_script = Path.home() / ".claude" / "skills" / "synapse-core" / "scripts" / "scaffold.py"
    if not scaffold_script.exists():
        print(f"Error: scaffold.py not found at {scaffold_script}")
        print()
        print("Manual fix:")
        print("  Check if synapse-core skill is installed:")
        print("  ls ~/.claude/skills/synapse-core/scripts/scaffold.py")
        return False

    try:
        result = subprocess.run(
            ["python3", str(scaffold_script), str(project)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[Scaffold] {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Scaffold Error] {e.stderr}")
        print()
        print("Manual fix:")
        print(f"  python3 ~/.claude/skills/synapse-core/scripts/scaffold.py {project}")
        return False


def get_gitnexus_bin() -> str:
    """Get path to gitnexus binary (bundled or global)."""
    # Try bundled version first
    bundled = Path(__file__).parent.parent / "node_modules" / ".bin" / "gitnexus"
    if bundled.exists():
        return str(bundled)
    # Fallback to global
    return "gitnexus"


def run_gitnexus_analyze(project: Path) -> bool:
    """Run gitnexus analyze --force."""
    gitnexus_bin = get_gitnexus_bin()
    try:
        result = subprocess.run(
            [gitnexus_bin, "analyze", "--force"],
            cwd=project,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[GitNexus] {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[GitNexus Error] {e.stderr}")
        print()
        print("Manual fix:")
        print(f"  cd {project}")
        print(f"  {gitnexus_bin} analyze --force")
        return False
    except FileNotFoundError:
        print(f"[GitNexus Error] gitnexus not found at {gitnexus_bin}")
        print()
        print("Manual fix:")
        print("  Re-run install.sh to install bundled gitnexus")
        return False


def get_pipeline_workspace() -> Path:
    """Get pipeline workspace path from config or default."""
    config_file = Path(__file__).parent / "config.json"
    if config_file.exists():
        try:
            import json
            with open(config_file) as f:
                config = json.load(f)
            workspace = config.get("pipeline", {}).get("workspace", "~/pipeline-workspace")
            return Path(workspace).expanduser()
        except (json.JSONDecodeError, IOError):
            pass
    return Path.home() / "pipeline-workspace"


def create_pipeline_project(project: Path, pipeline_workspace: Path) -> bool:
    """Create pipeline project if not exists."""
    project_name = project.name
    pipeline_project = pipeline_workspace / project_name

    if pipeline_project.exists():
        print(f"[Pipeline] Project '{project_name}' already exists")
        return True

    try:
        result = subprocess.run(
            ["python3", "pipeline.py", "new", project_name],
            cwd=pipeline_workspace,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[Pipeline] {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Pipeline Error] {e.stderr}")
        print()
        print("Manual fix:")
        print(f"  cd {pipeline_workspace}")
        print(f"  python3 pipeline.py new {project_name}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 init_project.py /path/to/project")
        sys.exit(1)

    project = Path(sys.argv[1]).resolve()
    pipeline_workspace = get_pipeline_workspace()

    if not project.exists():
        print(f"Error: Project directory {project} does not exist")
        sys.exit(1)

    print(f"Initializing Synapse + Pipeline for {project}...")
    print("=" * 60)

    # Step 1: Check git repo
    print("[1/4] Checking git repository...")
    if not check_git_repo(project):
        sys.exit(1)
    print("  ✓ Git repository detected")

    # Step 2: Run scaffold
    print("[2/4] Running synapse-core scaffold...")
    if not run_scaffold(project):
        print("  ⚠ Scaffold failed, continuing anyway...")
    else:
        print("  ✓ Scaffold completed")
        # Verify scaffold contract
        print("[2.5/4] Verifying scaffold contract...")
        passed, violations = verify_scaffold_contract(project)
        if passed:
            print("  ✓ Contract verified: All required files present")
        else:
            print("  ⚠ Contract violations:")
            for v in violations:
                print(f"    - {v}")
            print()
            print("  Manual fix:")
            print(f"    python3 ~/.claude/skills/synapse-core/scripts/scaffold.py {project}")

    # Step 3: Run gitnexus analyze
    print("[3/4] Running gitnexus analyze...")
    if not run_gitnexus_analyze(project):
        print("  ⚠ GitNexus analyze failed, you can run it manually later")
    else:
        print("  ✓ GitNexus analyze completed")

    # Step 4: Create pipeline project
    print("[4/4] Creating pipeline project...")
    if not create_pipeline_project(project, pipeline_workspace):
        print("  ⚠ Pipeline project creation failed, you can create it manually")
    else:
        print("  ✓ Pipeline project created")

    print("=" * 60)
    print("Initialization complete!")
    print()
    print("Next steps:")
    print("  cd ~/pipeline-workspace")
    print(f"  python3 pipeline.py run-pipeline {project.name} --input 'Your requirement'")


if __name__ == "__main__":
    main()
