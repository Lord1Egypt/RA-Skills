"""TOML-based configuration loader for spex."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None


class SpexConfig(TypedDict, total=False):
    """TypedDict for spex configuration keys."""

    spex_root: str
    branch_management: bool
    main_branch_name: str
    submit_method: str
    debug: bool

_CONFIG_SCHEMA: list[tuple[str, str | bool, str]] = [
    ("spex_root", ".spex", "Root directory for spec storage"),
    ("branch_management", True, "Create and manage branches for specs"),
    ("main_branch_name", "", "Restrict spec creation to this branch"),
    ("submit_method", "merge", "How to submit completed work: merge or pr"),
    ("debug", False, "Append script traces to <spec_dir>/debug.log"),
]

_DEFAULTS: SpexConfig = {k: v for k, v, _ in _CONFIG_SCHEMA}

@dataclass
class ProjectContext:
    """Full project context including git metadata and spex configuration."""

    cwd: Path
    top_workdir: Path | None
    main_worktree: Path | None
    remote_url: str
    branch: str
    user_name: str
    user_email: str
    spex_tomls: list[Path] = field(default_factory=list)
    config: dict = field(default_factory=dict)
    spex_root: str = ""
    spex_roots: list[str] = field(default_factory=list)

    def in_git_workdir(self) -> bool:
        return self.top_workdir is not None

    def is_related_to(self, spec) -> bool:
        """Check if this project context is related to the given spec.

        Accepts a SpecMeta instance, a Spec instance (with .meta attribute),
        a dict (like load_meta().to_dict()), or a Path (spec directory).
        """
        from common import load_meta, same_path

        # Not in a git repo — matches everything
        if self.top_workdir is None and self.main_worktree is None:
            return True

        # Extract workdir and main_worktree from the spec parameter
        if isinstance(spec, Path):
            meta = load_meta(spec)
            if meta is None:
                return True
            spec_workdir = meta.workdir
            spec_main_worktree = meta.main_worktree
        elif hasattr(spec, "meta"):
            # Spec instance with .meta attribute
            spec_workdir = spec.meta.workdir
            spec_main_worktree = spec.meta.main_worktree
        elif isinstance(spec, dict):
            spec_workdir = spec.get("workdir", "")
            spec_main_worktree = spec.get("main_worktree", "")
        else:
            # Assume object with .workdir and .main_worktree attributes
            spec_workdir = getattr(spec, "workdir", "")
            spec_main_worktree = getattr(spec, "main_worktree", "")

        # No workdir record means matches any project
        if not spec_workdir:
            return True

        # Compare top_workdir
        if self.top_workdir is not None and spec_workdir:
            if same_path(str(self.top_workdir), spec_workdir):
                return True

        # Compare main_worktree
        if self.main_worktree is not None and spec_main_worktree:
            if same_path(str(self.main_worktree), spec_main_worktree):
                return True

        return False

_SENTINEL = object()
_top_workdir_cache: dict = {}
_main_worktree_cache: dict = {}
_config_cache: dict | None = None
_project_context_cache: dict[str, ProjectContext] = {}
_spex_config_file_override: str | None = None


def set_spex_config_file(path: str | None) -> None:
    """Set an explicit config file path (from --spex-config-file CLI flag)."""
    global _spex_config_file_override
    _spex_config_file_override = path

def _get_main_worktree(workdir: str | Path | None = None) -> Path | None:
    """Return the git main worktree, or None if not inside a repo. Cached.

    Handles linked worktrees and submodules: when .git is a file, resolves
    back to the main worktree via ``git worktree list --porcelain``.
    """
    key = str(Path(workdir).resolve()) if workdir else None
    cached = _main_worktree_cache.get(key, _SENTINEL)
    if cached is not _SENTINEL:
        return cached

    top_workdir = _get_top_workdir(workdir)
    if top_workdir is None:
        _main_worktree_cache[key] = None
        return None

    dot_git = top_workdir / ".git"

    if dot_git.is_dir():
        _main_worktree_cache[key] = top_workdir
        return top_workdir

    # .git is a file → linked worktree or submodule
    list_cwd: str | Path | None = workdir

    super_result = subprocess.run(
        ["git", "rev-parse", "--show-superproject-working-tree"],
        capture_output=True, text=True, cwd=workdir,
    )
    if super_result.returncode == 0 and super_result.stdout.strip():
        list_cwd = super_result.stdout.strip()

    wt_result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True, text=True, cwd=list_cwd,
    )
    value: Path | None = None
    if wt_result.returncode == 0:
        for line in wt_result.stdout.splitlines():
            if line.startswith("worktree "):
                value = Path(line[len("worktree "):]).resolve()
                break

    _main_worktree_cache[key] = value
    return value

def _get_top_workdir(workdir: str | Path | None = None) -> Path | None:
    """Return the git top workdir, or None if not inside a repo. Cached."""
    key = str(Path(workdir).resolve()) if workdir else None
    cached = _top_workdir_cache.get(key, _SENTINEL)
    if cached is not _SENTINEL:
        return cached
    cmd = ["git", "rev-parse", "--show-toplevel"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=workdir)
    value = Path(result.stdout.strip()).resolve() if result.returncode == 0 else None
    _top_workdir_cache[key] = value
    return value


def _find_spex_tomls(
    main_worktree: Path | None, workdir: str | Path | None = None
) -> list[Path]:
    """Discover .spex.toml files in priority order (highest first).

    Walk from a starting directory upward to filesystem root, collecting
    existing .spex.toml files. When inside a git repo, start from
    main_worktree; otherwise start from workdir (or cwd).
    Then check ~/.spex.toml as a fallback.

    If --spex-config-file or SPEX_CONFIG_FILE is set, skip discovery and
    return only that file. Raises FileNotFoundError if it doesn't exist.
    """
    config_file = _spex_config_file_override or os.environ.get("SPEX_CONFIG_FILE")
    if config_file:
        p = Path(config_file).expanduser().resolve()
        if not p.is_file():
            raise FileNotFoundError(
                f"Specified spex config file does not exist: {config_file}"
            )
        return [p]

    candidates: list[Path] = []
    visited: set[Path] = set()

    if main_worktree is not None:
        start = main_worktree.resolve()
    else:
        start = Path(workdir).resolve() if workdir else Path.cwd().resolve()

    current = start
    while True:
        toml_path = current / ".spex.toml"
        if toml_path.is_file():
            candidates.append(toml_path)
            visited.add(toml_path.resolve())
        parent = current.parent
        if parent == current:
            break
        current = parent

    home_toml = (Path.home() / ".spex.toml").resolve()
    if home_toml.is_file() and home_toml not in visited:
        candidates.append(home_toml)

    return candidates


def _load_toml_config(path: Path) -> dict | None:
    """Read a single TOML file. Return None if missing or unparseable."""
    if not path.is_file():
        return None
    if tomllib is None:
        import sys
        print(
            "error: TOML parser not available. "
            "Run 'spex init' or 'pip install tomli' to install dependencies.",
            file=sys.stderr,
        )
        return None
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError):
        return None


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dicts. Keys in *override* take precedence."""
    merged = base.copy()
    for key, val in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(val, dict):
            merged[key] = _deep_merge(merged[key], val)
        else:
            merged[key] = val
    return merged


def _merge_configs(spex_tomls: list[Path]) -> dict:
    """Merge TOML configs. spex_tomls is highest-priority-first."""
    merged: dict = {}
    for path in reversed(spex_tomls):
        data = _load_toml_config(path)
        if data is not None:
            merged = _deep_merge(merged, data.get("spex", {}))
    return merged


def load_config(workdir: str | Path | None = None) -> dict:
    """Main entry point: resolve spex configuration with caching."""
    global _config_cache

    if _config_cache is not None:
        return _config_cache

    main_wt = _get_main_worktree(workdir)
    spex_tomls = _find_spex_tomls(main_wt, workdir)
    merged = _merge_configs(spex_tomls)

    result: dict = {**_DEFAULTS, **merged}

    _config_cache = result
    return _config_cache


def get_top_workdir(workdir: str | Path | None = None) -> Path | None:
    """Public wrapper for _get_top_workdir."""
    return _get_top_workdir(workdir)


def get_main_worktree(workdir: str | Path | None = None) -> Path | None:
    """Public wrapper for _get_main_worktree."""
    return _get_main_worktree(workdir)


def get_spex_tomls(workdir: str | Path | None = None) -> list[Path]:
    """Return the discovered TOML config paths (highest priority first)."""
    main_wt = _get_main_worktree(workdir)
    return _find_spex_tomls(main_wt, workdir)


def _resolve_spex_roots(
    spex_tomls: list[Path],
    main_worktree: Path | None,
    workdir: str | Path | None = None,
) -> list[str]:
    """Resolve spex_root to a list of directory paths using per-level configs.

    Each .spex.toml that sets spex_root governs its own directory and all
    child directories below it. When walking upward from start, the effective
    spex_root at each level is determined by the nearest .spex.toml at or
    above that level.

    Same-level rule: if the directory being checked is the same directory
    where the governing .spex.toml lives, the candidate path is added
    unconditionally (even if it doesn't exist yet).
    """
    if main_worktree is not None:
        start = main_worktree.resolve()
    else:
        start = Path(workdir).resolve() if workdir else Path.cwd().resolve()

    # Build list of directories from start to filesystem root
    path_dirs: list[Path] = []
    current = start
    while True:
        path_dirs.append(current)
        parent = current.parent
        if parent == current:
            break
        current = parent

    # Map toml directories to their index in path_dirs (only if they set spex_root)
    path_set = {d: i for i, d in enumerate(path_dirs)}
    toml_at: dict[int, str] = {}  # index -> spex_root value
    unmapped_tomls: list[tuple[Path, str]] = []  # (toml_dir, spex_root) for off-path tomls

    for toml_path in spex_tomls:
        toml_dir = toml_path.parent.resolve()
        data = _load_toml_config(toml_path)
        sr = (data or {}).get("spex", {}).get("spex_root")
        if sr is None:
            continue
        if toml_dir in path_set:
            toml_at[path_set[toml_dir]] = sr
        else:
            unmapped_tomls.append((toml_dir, sr))

    # Sweep from root-end to start-end computing (effective_spex_root, same_level)
    n = len(path_dirs)
    governing: list[tuple[str, bool]] = [("", False)] * n
    current_effective = _DEFAULTS["spex_root"]
    for i in range(n - 1, -1, -1):
        if i in toml_at:
            current_effective = toml_at[i]
            governing[i] = (current_effective, True)
        else:
            governing[i] = (current_effective, False)

    # Build results
    results: list[str] = []
    visited: set[str] = set()

    for i, d in enumerate(path_dirs):
        spex_root_val, same_level = governing[i]
        expanded = Path(spex_root_val).expanduser()

        if expanded.is_absolute():
            candidate = expanded
        else:
            candidate = d / spex_root_val

        resolved_str = str(candidate.resolve())
        if resolved_str not in visited:
            if same_level or candidate.is_dir():
                results.append(resolved_str)
                visited.add(resolved_str)

    # Handle tomls not on the path (e.g. home fallback when ~ is not an ancestor)
    for toml_dir, sr in unmapped_tomls:
        expanded = Path(sr).expanduser()
        candidate = expanded if expanded.is_absolute() else toml_dir / sr
        resolved_str = str(candidate.resolve())
        if resolved_str not in visited:
            results.append(resolved_str)
            visited.add(resolved_str)

    # Always append ~/<default_spex_root> as final fallback
    home_default = str((Path.home() / _DEFAULTS["spex_root"]).resolve())
    if home_default not in visited:
        results.append(home_default)

    return results


def resolve_spex_root_and_roots(
    workdir: str | Path | None = None,
) -> tuple[str, list[str]]:
    """Return (primary_spex_root, all_spex_roots) based on per-level config.

    The primary root is the first (highest-priority) entry in the roots list.
    """
    main_wt = _get_main_worktree(workdir)
    spex_tomls = _find_spex_tomls(main_wt, workdir)
    roots = _resolve_spex_roots(spex_tomls, main_wt, workdir)
    if roots:
        return (roots[0], roots)
    return ("", [])


def _git_field(cmd: list[str], cwd: str | Path | None = None) -> str:
    """Run a git command and return stripped stdout, or "" on failure."""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip() if result.returncode == 0 else ""


def _get_remote_url(cwd: str | Path | None = None) -> str:
    """Get remote URL: prefer 'origin', fall back to first available remote."""
    url = _git_field(["git", "remote", "get-url", "origin"], cwd=cwd)
    if url:
        return url
    first_remote = _git_field(["git", "remote"], cwd=cwd).split("\n")[0]
    if first_remote:
        return _git_field(["git", "remote", "get-url", first_remote], cwd=cwd)
    return ""


def get_project_context(workdir: str | Path | None = None) -> ProjectContext:
    """Return a fully resolved ProjectContext, cached by resolved workdir.

    Aggregates git metadata, discovered TOML paths, merged config, and
    resolved spex_root/spex_roots into a single object.
    """
    workdir = Path(workdir).resolve() if workdir else Path.cwd().resolve()
    cache_key = str(workdir)

    if cache_key in _project_context_cache:
        return _project_context_cache[cache_key]

    top_workdir = _get_top_workdir(workdir)
    main_worktree = _get_main_worktree(workdir)
    user_name = _git_field(["git", "config", "user.name"], cwd=workdir)
    user_email = _git_field(["git", "config", "user.email"], cwd=workdir)

    if top_workdir is not None:
        remote_url = _get_remote_url(cwd=workdir)
        try:
            from branch import get_current_branch
            branch = get_current_branch(cwd=workdir)
        except RuntimeError:
            branch = ""
    else:
        remote_url = ""
        branch = ""

    spex_tomls = _find_spex_tomls(main_worktree, workdir)
    config = load_config(workdir)
    spex_roots = _resolve_spex_roots(spex_tomls, main_worktree, workdir)
    spex_root = spex_roots[0] if spex_roots else ""

    ctx = ProjectContext(
        cwd=workdir,
        top_workdir=top_workdir,
        main_worktree=main_worktree,
        remote_url=remote_url,
        branch=branch,
        user_name=user_name,
        user_email=user_email,
        spex_tomls=spex_tomls,
        config=config,
        spex_root=spex_root,
        spex_roots=spex_roots,
    )
    _project_context_cache[cache_key] = ctx
    return ctx


def generate_default_toml() -> str:
    """Generate a TOML string with all config defaults as commented-out entries."""
    return generate_updated_toml({})


def _render_toml_value(value) -> str:
    """Render a Python value as a TOML literal."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def generate_updated_toml(
    user_config: dict, force_keys: set | None = None,
) -> str:
    """Generate a TOML string preserving user-set values from an existing config.

    Keys in user_config with non-default values are rendered uncommented.
    Keys matching defaults or absent from user_config are commented out.
    Keys in force_keys are always rendered uncommented.
    Keys in user_config that are not in the current schema are appended
    at the end (explicit values) so upgrades never drop unknown settings.
    """
    if force_keys is None:
        force_keys = set()
    schema_keys = {key for key, _, _ in _CONFIG_SCHEMA}
    lines = ["[spex]"]
    for i, (key, default, comment) in enumerate(_CONFIG_SCHEMA):
        if i > 0:
            lines.append("")
        lines.append(f"# {comment}")
        value = user_config.get(key)
        is_explicit = value is not None and value != default
        if is_explicit or key in force_keys:
            rendered = _render_toml_value(
                value if value is not None else default)
            lines.append(f"{key} = {rendered}")
        else:
            rendered = _render_toml_value(default)
            lines.append(f"# {key} = {rendered}")
    for key, value in user_config.items():
        if key in schema_keys:
            continue
        lines.append("")
        lines.append("# Preserved (not in current schema)")
        lines.append(f"{key} = {_render_toml_value(value)}")
    return "\n".join(lines) + "\n"


def safe_update_toml(toml_path, dry_run=False):
    """Safe-update a single .spex.toml with the latest config schema.

    Reads the existing file, preserves user-set keys (including keys not
    in the current schema), and regenerates with the full schema. New
    schema keys appear as commented-out defaults.

    Returns True if the file was (or would be) modified.
    """
    existing = _load_toml_config(toml_path)
    user_config = (existing or {}).get("spex", {})
    force = {"spex_root"} if "spex_root" in user_config else set()
    new_content = generate_updated_toml(user_config, force_keys=force)
    if not toml_path.is_file():
        return False
    old_content = toml_path.read_text(encoding="utf-8")
    if new_content != old_content:
        if not dry_run:
            toml_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def get_effective_user_config(workdir: str | Path | None = None) -> dict:
    """Return merged user-set config values (without defaults) for a workdir.

    Discovers .spex.toml files relative to workdir and merges their [spex]
    tables. Only explicitly set keys are included — commented-out defaults
    are not. Use this to create a new project-level .spex.toml that inherits
    parent settings.
    """
    main_wt = _get_main_worktree(workdir)
    spex_tomls = _find_spex_tomls(main_wt, workdir)
    return _merge_configs(spex_tomls)


def clear_config_cache() -> None:
    """Clear the module-level configuration and worktree root caches."""
    global _config_cache, _top_workdir_cache, _main_worktree_cache
    global _project_context_cache, _spex_config_file_override
    _config_cache = None
    _top_workdir_cache = {}
    _main_worktree_cache = {}
    _project_context_cache = {}
    _spex_config_file_override = None
