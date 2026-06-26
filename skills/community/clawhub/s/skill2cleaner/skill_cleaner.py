#!/usr/bin/env python3
"""
Skill Cleaner - OpenClaw / Claude Code 通用版
扫描工作区无效 Skill，并支持禁用或卸载。
"""

import os
import json
import yaml
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional

# ================== 路径配置（自动适配） ==================
try:
    # OpenClaw 标准路径
    WORKSPACE_SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
    OPENCLAW_CONFIG_FILE = Path.home() / ".openclaw" / "openclaw.json"
except Exception:
    WORKSPACE_SKILLS_DIR = None
    OPENCLAW_CONFIG_FILE = None
# =========================================================


class SkillStatus:
    VALID = "valid"
    MISSING_DEPENDENCY = "missing-dependency"
    DISABLED = "disabled"
    API_KEY_MISSING = "api-key-missing"
    SKILL_FILE_MISSING = "skill-file-missing"


def run_cli(cmd: List[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()


def get_installed_skills() -> List[Dict]:
    if not WORKSPACE_SKILLS_DIR:
        return []
    output = run_cli(["openclaw", "skills", "list", "--json"])
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return []


def get_skill_directory(skill_name: str) -> Optional[Path]:
    if not WORKSPACE_SKILLS_DIR:
        return None
    target = WORKSPACE_SKILLS_DIR / skill_name
    if target.exists():
        return target
    for d in WORKSPACE_SKILLS_DIR.iterdir():
        if d.is_dir() and d.name.endswith(skill_name):
            return d
    return None


def load_skill_manifest(skill_dir: Path) -> Optional[Dict]:
    manifest_path = skill_dir / "SKILL.md"
    if manifest_path.exists():
        content = manifest_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    return yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    pass
    yaml_path = skill_dir / "skill.yaml"
    if yaml_path.exists():
        return yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    return None


def get_required_env_vars(manifest: Dict) -> List[str]:
    required = []
    env_info = manifest.get("env", []) or manifest.get("environment", [])
    if isinstance(env_info, list):
        for item in env_info:
            if isinstance(item, str):
                required.append(item)
            elif isinstance(item, dict):
                required.append(item.get("name", ""))
    elif isinstance(env_info, dict):
        required = list(env_info.keys())
    return [var for var in {*required} if var]


def check_env_vars(vars: List[str]) -> bool:
    for var in vars:
        if not os.getenv(var):
            return False
    return True


def check_disabled(skill_name: str) -> bool:
    if not OPENCLAW_CONFIG_FILE or not OPENCLAW_CONFIG_FILE.exists():
        return False
    try:
        config = json.loads(OPENCLAW_CONFIG_FILE.read_text())
        disabled = config.get("skills", {}).get("disabled", [])
        return skill_name in disabled
    except Exception:
        return False


def diagnose_skill(skill_info: Dict) -> Dict:
    name = skill_info.get("name", "unknown")
    result = {"name": name, "status": SkillStatus.VALID, "reason": ""}

    if check_disabled(name):
        result["status"] = SkillStatus.DISABLED
        result["reason"] = f"Skill '{name}' 已在配置中被禁用。"
        return result

    skill_dir = get_skill_directory(name)
    if not skill_dir:
        result["status"] = SkillStatus.SKILL_FILE_MISSING
        result["reason"] = f"未找到 Skill '{name}' 的安装目录。"
        return result

    manifest = load_skill_manifest(skill_dir)
    if not manifest:
        result["status"] = SkillStatus.CONFIG_INVALID
        result["reason"] = f"缺少有效的清单文件。"
        return result

    required_vars = get_required_env_vars(manifest)
    if required_vars and not check_env_vars(required_vars):
        missing = [v for v in required_vars if not os.getenv(v)]
        result["status"] = SkillStatus.API_KEY_MISSING
        result["reason"] = f"缺少环境变量：{', '.join(missing)}"
        return result

    result["reason"] = "一切正常"
    return result


def scan_all_skills() -> List[Dict]:
    installed = get_installed_skills()
    results = []
    for skill in installed:
        results.append(diagnose_skill(skill))
    return results


def format_report(diagnostics: List[Dict]) -> str:
    valid = [d for d in diagnostics if d["status"] == SkillStatus.VALID]
    invalid = [d for d in diagnostics if d["status"] != SkillStatus.VALID]
    lines = ["=== Skill 状态检查报告 ==="]
    if invalid:
        lines.append(f"\n❌ 无效 Skill ({len(invalid)}个)：")
        for item in invalid:
            lines.append(f"  • {item['name']} [{item['status']}]")
            lines.append(f"    原因：{item['reason']}")
    else:
        lines.append("\n✅ 所有 Skill 均正常工作。")
    if valid:
        lines.append(f"\n✅ 有效 Skill ({len(valid)}个)：")
        for item in valid:
            lines.append(f"  • {item['name']}")
    return "\n".join(lines)


def perform_cleanup(invalid_skills: List[Dict], action: str = "disable") -> str:
    logs = []
    for skill in invalid_skills:
        name = skill["name"]
        if action == "disable":
            cmd = ["openclaw", "skills", "disable", name]
        elif action == "uninstall":
            cmd = ["openclaw", "skills", "uninstall", name, "--force"]
        else:
            continue
        output = run_cli(cmd)
        logs.append(f"[{name}] {output}")
    return "\n".join(logs)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        if len(sys.argv) < 4:
            print(
                "用法: python skill_cleaner.py clean <disable|uninstall> <skill1,skill2,...>"
            )
            return
        action = sys.argv[2]
        skill_list = [s.strip() for s in sys.argv[3].split(",")]
        diagnostics = [diagnose_skill({"name": name}) for name in skill_list]
        print(perform_cleanup(diagnostics, action))
        return

    diagnostics = scan_all_skills()
    print(format_report(diagnostics))


if __name__ == "__main__":
    main()
