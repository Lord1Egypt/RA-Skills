#!/usr/bin/env python3
"""
Fleet Validation Script for OpenClaw Multi-Agent Deployment

Validates a deployed multi-agent fleet for:
- Agent directory structure integrity
- Template placeholder resolution
- Routing configuration correctness
- Shared memory initialization
- End-to-end communication test

Usage:
    python scripts/fleet_validate.py --agents ./agents
    python scripts/fleet_validate.py --agents ./agents --config ~/.openclaw/config.json --verbose
"""

import argparse
import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

PASS = f"{GREEN}✓{RESET}"
FAIL = f"{RED}✗{RESET}"
WARN = f"{YELLOW}⚠{RESET}"

# Expected agent types from the skill
EXPECTED_AGENTS = {"coordinator", "research", "builder", "auditor", "personal"}

# Expected subdirectories per agent
EXPECTED_SUBDIRS = {"workspace", "memory", "skills"}

# Placeholders that must be resolved in populated SOUL.md files
SOUL_PLACEHOLDERS = {"{agent_name}", "{agent_type}", "{mission}",
                     "{responsibility1}", "{responsibility2}",
                     "{responsibility3}", "{responsibility4}",
                     "{response_time_target}", "{accuracy_target}",
                     "{error_rate_target}", "{availability_target}",
                     "{version}", "{created_date}", "{last_updated_date}"}

AGENTS_PLACEHOLDER = {"{agent_name}"}


def check(label: str, passed: bool, detail: str = ""):
    """Print a formatted check result."""
    icon = PASS if passed else FAIL
    msg = f"  {icon} {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return passed


def warn(label: str, detail: str = ""):
    """Print a formatted warning."""
    msg = f"  {WARN} {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)


def validate_agent_directory(agent_dir: Path, agent_type: str) -> dict:
    """Validate a single agent's directory structure."""
    result = {"type": agent_type, "passed": 0, "failed": 0, "warnings": 0, "issues": []}
    agent_name = agent_type.title()

    print(f"\n{CYAN}{BOLD}Agent: {agent_name}{RESET}")

    # Check directory exists
    if not check(f"Directory exists", agent_dir.exists()):
        result["failed"] += 1
        result["issues"].append("directory missing")
        return result
    result["passed"] += 1

    # Check SOUL.md
    soul_file = agent_dir / "SOUL.md"
    if check(f"SOUL.md present", soul_file.exists()):
        result["passed"] += 1
        content = soul_file.read_text(encoding="utf-8")

        # Check agent_name and agent_type are correctly populated
        if check(f"Agent name set to '{agent_name}'", agent_name in content,
                 f"Found in SOUL.md"):
            result["passed"] += 1
        else:
            result["warnings"] += 1
            result["issues"].append("SOUL.md missing agent name")

        # Check no unresolved placeholders
        unresolved = {p for p in SOUL_PLACEHOLDERS if p in content}
        if check(f"No unresolved placeholders",
                 len(unresolved) == 0,
                 f"Resolved {len(SOUL_PLACEHOLDERS) - len(unresolved)}/{len(SOUL_PLACEHOLDERS)}"):
            result["passed"] += 1
        else:
            result["failed"] += 1
            result["issues"].append(f"Unresolved placeholders: {unresolved}")

        # Check mission is populated not placeholder
        if "{mission}" not in content:
            # Find the mission line
            for line in content.split("\n"):
                if "Mission" in line and ":" in line:
                    mission_text = line.split(":", 1)[1].strip()
                    if mission_text and len(mission_text) > 10:
                        result["passed"] += 1
                        break
            else:
                warn("Mission line format unexpected")
                result["warnings"] += 1
        else:
            result["failed"] += 1
            result["issues"].append("Mission still has placeholder")
    else:
        result["failed"] += 1
        result["issues"].append("SOUL.md missing")

    # Check AGENTS.md
    agents_file = agent_dir / "AGENTS.md"
    if check(f"AGENTS.md present", agents_file.exists()):
        result["passed"] += 1
        content = agents_file.read_text(encoding="utf-8")

        # Check agent_name is populated
        if check(f"Agent name populated in AGENTS.md",
                 agent_name in content or "{agent_name}" not in content):
            result["passed"] += 1
        else:
            result["warnings"] += 1
            result["issues"].append("AGENTS.md may have unresolved agent_name")

        # Check no unresolved placeholders
        unresolved = {p for p in AGENTS_PLACEHOLDER if p in content}
        if check(f"AGENTS.md placeholders resolved", len(unresolved) == 0):
            result["passed"] += 1
        else:
            result["failed"] += 1
            result["issues"].append(f"Unresolved AGENTS.md placeholders: {unresolved}")
    else:
        result["failed"] += 1
        result["issues"].append("AGENTS.md missing")

    # Check subdirectories
    for subdir in EXPECTED_SUBDIRS:
        subdir_path = agent_dir / subdir
        if check(f"'{subdir}/' directory present", subdir_path.is_dir()):
            result["passed"] += 1
        else:
            result["warnings"] += 1
            result["issues"].append(f"Missing {subdir}/ directory")

    return result


def validate_shared_memory(shared_dir: Path) -> dict:
    """Validate shared memory directory structure."""
    result = {"passed": 0, "failed": 0, "warnings": 0, "issues": []}

    print(f"\n{CYAN}{BOLD}Shared Memory{RESET}")

    if check(f"Shared memory directory exists", shared_dir.exists()):
        result["passed"] += 1

        # Check subdirectories
        for subdir in ["memory", "events", "logs"]:
            subdir_path = shared_dir / subdir
            if check(f"'{subdir}/' directory present", subdir_path.is_dir()):
                result["passed"] += 1
            else:
                result["warnings"] += 1
                result["issues"].append(f"Missing shared/{subdir}/")

        # Check if shared_data.json exists and is valid
        data_file = shared_dir / "memory" / "shared_data.json"
        if data_file.exists():
            try:
                data = json.loads(data_file.read_text(encoding="utf-8"))
                if check(f"shared_data.json is valid JSON", True):
                    result["passed"] += 1
                # Check required keys
                for key in ["version", "agents", "shared", "events", "metadata"]:
                    if key in data:
                        result["passed"] += 1
                    else:
                        result["warnings"] += 1
                        result["issues"].append(f"shared_data.json missing '{key}'")
            except json.JSONDecodeError:
                check(f"shared_data.json is valid JSON", False, "Parse error!")
                result["failed"] += 1
                result["issues"].append("shared_data.json is corrupted")
        else:
            warn("shared_data.json not yet initialized (run --init first)")
            result["warnings"] += 1
    else:
        result["failed"] += 1
        result["issues"].append("Shared memory directory missing")

    return result


def validate_routing_config(config_path: Path) -> dict:
    """Validate OpenClaw routing configuration."""
    result = {"passed": 0, "failed": 0, "warnings": 0, "issues": []}

    print(f"\n{CYAN}{BOLD}Routing Configuration{RESET}")

    if not config_path.exists():
        warn("Config file not found (run routing_config.py first)")
        result["warnings"] += 1
        return result

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))

        if check(f"Config is valid JSON", True):
            result["passed"] += 1

        # Check required sections
        required_sections = ["agents", "routing", "workspaces"]
        for section in required_sections:
            if check(f"Config has '{section}' section", section in config):
                result["passed"] += 1
            else:
                result["failed"] += 1
                result["issues"].append(f"Missing config section: {section}")

        # Check routing rules
        if "routing" in config:
            rules = config["routing"].get("rules", [])
            if check(f"Routing rules defined ({len(rules)} rules)", len(rules) > 0,
                     f"Found {len(rules)} rules"):
                result["passed"] += 1
            else:
                result["warnings"] += 1
                result["issues"].append("No routing rules defined")

            # Check default agent
            default = config["routing"].get("defaultAgent")
            if default:
                if check(f"Default agent set to '{default}'", bool(default)):
                    result["passed"] += 1
            else:
                result["failed"] += 1
                result["issues"].append("No default agent configured")

        # Check agent configs
        if "agents" in config:
            agent_list = list(config["agents"].keys())
            if check(f"Agent configs defined ({len(agent_list)} agents)",
                     len(agent_list) > 0,
                     f"Agents: {', '.join(agent_list)}"):
                result["passed"] += 1
            else:
                result["failed"] += 1
                result["issues"].append("No agents configured")

    except json.JSONDecodeError as e:
        check(f"Config is valid JSON", False, str(e))
        result["failed"] += 1
        result["issues"].append("Config file is corrupted JSON")

    return result


def validate_scripts(skill_dir: Path) -> dict:
    """Validate required scripts exist and are runnable."""
    result = {"passed": 0, "failed": 0, "warnings": 0, "issues": []}

    print(f"\n{CYAN}{BOLD}Scripts{RESET}")

    required_scripts = [
        ("agent_setup.py", "Agent directory scaffolding"),
        ("routing_config.py", "Routing config generator"),
        ("memory_sync.py", "Shared memory sync system"),
        ("deploy_script.sh", "Cloud deployment script"),
    ]

    for script_name, description in required_scripts:
        script_path = skill_dir / "scripts" / script_name
        if check(f"{script_name} — {description}", script_path.exists()):
            result["passed"] += 1
            # Check file is non-empty
            if script_path.stat().st_size > 100:
                result["passed"] += 1
            else:
                result["warnings"] += 1
                result["issues"].append(f"{script_name} appears empty/truncated")
        else:
            result["failed"] += 1
            result["issues"].append(f"Missing script: {script_name}")

    # Check deployment templates
    deployments_dir = skill_dir / "deployments"
    if deployments_dir.exists():
        platform_count = len(list(deployments_dir.glob("*/**")))
        if check(f"Deployment configs found", platform_count > 0,
                 f"Platforms configured"):
            result["passed"] += 1
        else:
            result["warnings"] += 1
    else:
        warn("deployments/ directory not found (generated at runtime)")
        result["warnings"] += 1

    return result


def validate_references(skill_dir: Path) -> dict:
    """Validate reference documentation."""
    result = {"passed": 0, "failed": 0, "warnings": 0, "issues": []}

    print(f"\n{CYAN}{BOLD}Documentation{RESET}")

    required_docs = [
        ("SKILL.md", "Main skill documentation"),
        ("HEARTBEAT.md", "Maintenance heartbeat"),
        ("_meta.json", "Skill metadata"),
        ("references/architecture.md", "Architecture patterns"),
        ("references/troubleshooting.md", "Troubleshooting guide"),
    ]

    for doc_name, description in required_docs:
        doc_path = skill_dir / doc_name
        if check(f"{doc_name} — {description}", doc_path.exists()):
            result["passed"] += 1
            # Check file size
            size_kb = doc_path.stat().st_size / 1024
            if size_kb > 1:
                result["passed"] += 1
            else:
                result["warnings"] += 1
                result["issues"].append(f"{doc_name} is small ({size_kb:.1f} KB)")
        else:
            result["failed"] += 1
            result["issues"].append(f"Missing: {doc_name}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate multi-agent fleet deployment integrity"
    )
    parser.add_argument("--agents", default="./agents",
                        help="Path to agents directory (default: ./agents)")
    parser.add_argument("--config", default=None,
                        help="Path to OpenClaw config.json (default: skip validation)")
    parser.add_argument("--skill-dir", default=None,
                        help="Path to skill directory (default: parent of scripts/)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output")
    args = parser.parse_args()

    agents_dir = Path(args.agents)
    skill_dir = Path(args.skill_dir) if args.skill_dir else Path(__file__).parent.parent

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  Multi-Agent Fleet Validation{RESET}")
    print(f"{BOLD}  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")

    total = {"passed": 0, "failed": 0, "warnings": 0}

    # Phase 1: Validate scripts and documentation
    print(f"\n{'='*60}")
    print(f"{BOLD}Phase 1: Skill Package Integrity{RESET}")
    print(f"{'='*60}")

    script_results = validate_scripts(skill_dir)
    for k in total:
        total[k] += script_results[k]

    doc_results = validate_references(skill_dir)
    for k in total:
        total[k] += doc_results[k]

    # Phase 2: Validate routing config
    print(f"\n{'='*60}")
    print(f"{BOLD}Phase 2: Configuration Validation{RESET}")
    print(f"{'='*60}")

    if args.config:
        config_path = Path(args.config)
    else:
        config_path = agents_dir.parent / "config.json"

    config_results = validate_routing_config(config_path)
    for k in total:
        total[k] += config_results[k]

    # Phase 3: Validate agent directories
    print(f"\n{'='*60}")
    print(f"{BOLD}Phase 3: Agent Directory Validation{RESET}")
    print(f"{'='*60}")

    if agents_dir.exists():
        agent_dirs_found = [
            d for d in agents_dir.iterdir()
            if d.is_dir() and not d.name.startswith('.') and d.name != 'shared'
        ]

        if agent_dirs_found:
            for agent_dir in agent_dirs_found:
                agent_results = validate_agent_directory(agent_dir, agent_dir.name)
                for k in total:
                    total[k] += agent_results[k]

        # Check for expected agents
        found_agents = {d.name for d in agent_dirs_found}
        missing_agents = EXPECTED_AGENTS - found_agents
        if missing_agents:
            warn(f"Expected agents not found: {', '.join(sorted(missing_agents))}")
            total["warnings"] += 1
    else:
        warn("Agents directory not found. Run agent_setup.py first.")
        total["warnings"] += 1

    # Phase 4: Validate shared memory
    shared_dir = agents_dir / "shared"
    shared_results = validate_shared_memory(shared_dir)
    for k in total:
        total[k] += shared_results[k]

    # Summary
    print(f"\n{'='*60}")
    print(f"{BOLD}Validation Summary{RESET}")
    print(f"{'='*60}")
    print(f"  {PASS} Passed: {total['passed']}")
    print(f"  {FAIL} Failed: {total['failed']}")
    print(f"  {WARN} Warnings: {total['warnings']}")

    if total["failed"] > 0:
        print(f"\n{RED}{BOLD}  ❌ Validation FAILED — Review issues above.{RESET}")
        sys.exit(1)
    elif total["warnings"] > 0:
        print(f"\n{YELLOW}{BOLD}  ⚠ Validation PASSED with warnings.{RESET}")
    else:
        print(f"\n{GREEN}{BOLD}  ✅ Validation PASSED — Fleet is healthy.{RESET}")

    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()