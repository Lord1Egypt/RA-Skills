"""OpenClaw instance discovery, bundled roots, and runtime reconciliation."""

import json
import os
import shutil
import subprocess
from pathlib import Path

from ..util import norm


def find_openclaw_bundled_skills(env=None):
    """Resolve bundled Skills across npm shims, direct bins, links, and pnpm."""
    environment = os.environ if env is None else env
    if environment.get("SKILL_VITALS_DISABLE_OPENCLAW_BUNDLED") == "1":
        return None
    executable = shutil.which("openclaw", path=environment.get("PATH"))
    if not executable:
        return None
    raw, resolved = Path(executable), Path(executable).resolve()
    candidates = []
    for anchor in (raw.parent, resolved.parent, *resolved.parents):
        candidates.extend((anchor / "node_modules" / "openclaw" / "skills",
                           anchor / "openclaw" / "skills"))
        if anchor.name == "openclaw":
            candidates.append(anchor / "skills")
    candidates.extend(raw.parent.glob(
        "node_modules/.pnpm/openclaw@*/node_modules/openclaw/skills"))
    seen = set()
    for candidate in candidates:
        key = norm(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.is_dir() and any(candidate.glob("*/SKILL.md")):
            return candidate.resolve()
    return None


def read_openclaw_roots(home=None, env=None, bundled_finder=None):
    """Discover OpenClaw instance roots and preserve instance/config evidence."""
    environment = os.environ if env is None else env
    base = Path(home) if home is not None else Path(os.path.expanduser("~"))
    roots = []
    for instance in base.glob(".open*"):
        if not instance.is_dir():
            continue
        config = instance / "openclaw.json"
        if not config.is_file():
            continue
        try:
            data = json.loads(config.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            data = {}
        metadata = {
            "instance_id": instance.name,
            "instance_root": norm(instance.resolve()),
            "config_path": norm(config.resolve()),
            "skill_entries": ((data.get("skills") or {}).get("entries") or {}),
            "plugin_entries": ((data.get("plugins") or {}).get("entries") or {}),
            "plugin_allow": ((data.get("plugins") or {}).get("allow") or []),
            "skills_prompt_budget_chars": (((data.get("skills") or {}).get("limits") or {})
                                             .get("maxSkillsPromptChars")),
        }
        for name, kind in (("skills", "managed"), ("plugin-skills", "plugin")):
            roots.append((str(instance / name), {**metadata, "root_kind": kind}))
        workspace = (((data.get("agents") or {}).get("defaults") or {}).get("workspace"))
        if isinstance(workspace, str) and workspace:
            workspace_root = Path(os.path.expandvars(os.path.expanduser(workspace))) / "skills"
            roots.append((str(workspace_root), {**metadata, "root_kind": "workspace"}))
        roots.append((str(base / ".agents" / "skills"),
                      {**metadata, "root_kind": "shared-user"}))
        finder = bundled_finder or find_openclaw_bundled_skills
        try:
            npm_skills = finder(env=environment)
        except TypeError:
            npm_skills = finder()
        if npm_skills:
            roots.append((str(npm_skills), {**metadata, "root_kind": "bundled"}))
    return roots


def read_openclaw_runtime(instance_root, env=None, executable=None):
    """Ask OpenClaw for the authoritative eligible catalog for one instance."""
    state = {"available": False, "source": "openclaw skills list --eligible --json",
             "skills": [], "errors": []}
    environment = dict(os.environ if env is None else env)
    executable = executable or shutil.which("openclaw", path=environment.get("PATH"))
    if not executable:
        state["errors"].append("openclaw executable not found")
        return state
    environment["OPENCLAW_STATE_DIR"] = str(instance_root)
    workspace = Path(instance_root) / "workspace"
    try:
        process = subprocess.run(
            [executable, "skills", "list", "--eligible", "--json", "--agent", "main"],
            cwd=str(workspace if workspace.is_dir() else instance_root), env=environment,
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        state["errors"].append(str(exc))
        return state
    if process.returncode:
        state["errors"].append(process.stderr.strip()[-500:] or f"exit={process.returncode}")
        return state
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        state["errors"].append(f"invalid JSON: {exc}")
        return state
    state["skills"] = payload.get("skills", [])
    state["available"] = True
    state["instance_id"] = Path(instance_root).name
    return state


def apply_openclaw_runtime(skills, runtimes):
    """Overlay eligible/model-visible state returned by OpenClaw itself."""
    for runtime in runtimes:
        if not runtime.get("available"):
            continue
        instance_id = runtime.get("instance_id")
        by_name = {metadata.get("name"): metadata
                   for metadata in runtime.get("skills", [])}
        for record in skills:
            if (record["host_family"] != "openclaw" or
                    record["instance_id"] != instance_id):
                continue
            metadata = by_name.get(record["name"])
            if not metadata:
                record.update({
                    "loaded": False,
                    "discoverable": False,
                    "loaded_state": False,
                    "runtime_verified": True,
                    "loaded_reason": "openclaw-cli-not-eligible",
                })
                continue
            record.update({
                "loaded": bool(metadata.get("modelVisible", True)),
                "discoverable": True,
                "enabled_state": not bool(metadata.get("disabled", False)),
                "loaded_state": bool(metadata.get("modelVisible", True)),
                "runtime_verified": True,
                "loaded_reason": "openclaw-cli-eligible-model-visible",
                "runtime_status": "eligible-model-visible",
                "body_loaded_state": None,
                "openclaw_runtime": metadata,
            })
    return skills
