"""Explicit roots -> collect -> probe -> reconcile orchestration."""

import os
from pathlib import Path

from .adapters.claude import read_host_config
from .adapters.codex import apply_codex_runtime, read_codex_runtime
from .adapters.hermes import read_hermes_external_dirs
from .adapters.openclaw import (
    apply_openclaw_runtime,
    read_openclaw_roots,
    read_openclaw_runtime,
)
from .adapters.workbuddy import (
    WORKBUDDY_ORPHANED,
    read_workbuddy_builtin_roots,
    read_workbuddy_welcome_mode,
)
from .discovery import collect, scan_skill_dir
from .util import norm


def build_inventory(host, paths, default_roots, env=None, home=None, cwd=None):
    """Collect disk inventory, probe selected runtimes, and reconcile evidence."""
    environment = os.environ if env is None else env
    home_path = Path(home) if home is not None else Path(os.path.expanduser("~"))
    cwd_path = Path(cwd) if cwd is not None else Path.cwd()

    enabled_plugins, usage, host_config = read_host_config(home=home_path)
    plugins_known = host_config is not None

    roots = list(default_roots)
    for path, metadata in read_openclaw_roots(home=home_path, env=environment):
        roots.append(("openclaw", path, metadata))
    for path in read_hermes_external_dirs(home=home_path, env=environment):
        roots.append(("hermes", path))

    workbuddy_mode, workbuddy_roots = None, []
    if environment.get("SKILL_VITALS_DISABLE_WORKBUDDY_BUILTINS") != "1":
        workbuddy_mode = read_workbuddy_welcome_mode(home=home_path)
        workbuddy_roots = read_workbuddy_builtin_roots(home=home_path)
        for path, metadata in workbuddy_roots:
            roots.append(("workbuddy", path, {
                **metadata, "workbuddy_welcome_mode": workbuddy_mode,
            }))

    if host != "all":
        roots = [root for root in roots if root[0] == host or
                 (host == "claude-code" and root[0] == "claude-code-plugins")]
    roots += [(host if host != "all" else "custom", path) for path in paths]
    skills, scanned, unreadable = collect(
        roots, enabled_plugins, usage, plugins_known, home=home_path, cwd=cwd_path)

    openclaw_runtime = []
    if (environment.get("SKILL_VITALS_DISABLE_OPENCLAW_RUNTIME") != "1" and
            host in ("all", "openclaw")):
        instance_roots = sorted({
            root[2].get("instance_root") for root in roots
            if len(root) > 2 and root[0] == "openclaw" and root[2].get("instance_root")
        })
        openclaw_runtime = [
            read_openclaw_runtime(Path(path), env=environment)
            for path in instance_roots
        ]
        skills = apply_openclaw_runtime(skills, openclaw_runtime)

    codex_runtime = {
        "available": False,
        "source": "codex app-server skills/list",
        "skills": [],
        "errors": ["host not selected"],
    }
    if environment.get("SKILL_VITALS_DISABLE_CODEX_RUNTIME") == "1":
        codex_runtime["errors"] = ["disabled by SKILL_VITALS_DISABLE_CODEX_RUNTIME"]
    elif host in ("all", "codex"):
        codex_runtime = read_codex_runtime(cwd_path, env=environment)
        if codex_runtime["available"]:
            codex_runtime_scanner = lambda *args, **kwargs: scan_skill_dir(
                *args, home_n=norm(home_path), cwd_n=norm(cwd_path), **kwargs)
            skills = apply_codex_runtime(skills, codex_runtime, codex_runtime_scanner)

    return {
        "skills": skills,
        "scanned_roots": scanned,
        "unreadable_skills": unreadable,
        "roots": roots,
        "enabled_plugins": enabled_plugins,
        "usage": usage,
        "host_config": host_config,
        "plugins_known": plugins_known,
        "workbuddy_mode": workbuddy_mode,
        "workbuddy_roots": workbuddy_roots,
        "workbuddy_orphaned": list(WORKBUDDY_ORPHANED),
        "openclaw_runtime": openclaw_runtime,
        "codex_runtime": codex_runtime,
    }
