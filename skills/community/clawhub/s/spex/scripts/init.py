#!/usr/bin/env python3
"""Initialize the spex environment."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import site
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from cli import ArgumentParser
from common import (
    _create_default_toml,
    _sync_all_templates,
    ensure_initialized,
    logger,
)
from config import (
    clear_config_cache,
    generate_updated_toml,
    get_main_worktree,
    get_project_context,
    get_top_workdir,
    load_config,
    safe_update_toml,
)

# PyPI package name -> importable module name for presence checks.
_PKG_TO_IMPORT = {
    "jinja2": "jinja2",
    "tomli": "tomli",
}


def is_initialized(workdir=None):
    """Check if spex environment is initialized.

    Returns True if a spex_root is resolved and its specs/ directory exists.
    """
    ctx = get_project_context(workdir)
    if not ctx.spex_tomls:
        return False
    if ctx.spex_root and not Path(ctx.spex_root).is_dir():
        return False
    return True


def _deps_for_env_check(pyproject_path: Path) -> list[str]:
    """Return package names that must be importable in this Python.

    Includes unconditional deps from pyproject.toml. Also includes
    ``tomli`` when running on Python < 3.11 (matches the environment
    marker in the skill pyproject).
    """
    deps = _parse_pyproject_deps(pyproject_path)
    content = pyproject_path.read_text(encoding="utf-8")
    # Support the only conditional dep we ship today.
    if sys.version_info < (3, 11) and re.search(
        r"tomli[^;\n]*;\s*python_version\s*<\s*[\"']3\.11[\"']",
        content,
    ):
        if "tomli" not in deps:
            deps.append("tomli")
    return deps


def _deps_satisfied(skill_dir: Path) -> bool:
    """Return True if all required runtime packages are importable."""
    pyproject = skill_dir / "pyproject.toml"
    if not pyproject.is_file():
        return True
    for pkg in _deps_for_env_check(pyproject):
        mod = _PKG_TO_IMPORT.get(pkg, pkg.replace("-", "_"))
        if importlib.util.find_spec(mod) is None:
            return False
    return True


def _install_deps(verbose=False, dry_run=False):
    """Install Python dependencies from the skill's pyproject.toml.

    Skips installation when required packages are already importable.
    Otherwise tries multiple methods in order:
    1. pip install (standard)
    2. uv pip install (fast, if available)
    3. Manual wheel download + extract (fallback when pip is broken)
    """
    from common import _get_skill_path

    skill_dir = _get_skill_path()
    satisfied = _deps_satisfied(skill_dir)
    if dry_run:
        if satisfied:
            logger.info(
                "Would skip dependency installation (already satisfied)",
            )
        else:
            logger.info("Would install dependencies from %s", skill_dir)
        return True
    if satisfied:
        logger.info("Dependencies already satisfied, skipping pip.")
        return True
    if verbose:
        logger.info("Installing dependencies from %s ...", skill_dir)

    # Method 1: pip install
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", str(skill_dir), "--quiet"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        logger.info("Installed Python dependencies (via pip).")
        return True

    logger.warning("pip install failed, trying fallbacks...")

    # Method 2: uv pip install (if available)
    uv = shutil.which("uv")
    if uv:
        if verbose:
            logger.info("Trying uv pip install ...")
        result = subprocess.run(
            [uv, "pip", "install", str(skill_dir), "--quiet",
             "--system", "--python", sys.executable],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            logger.info("Installed Python dependencies (via uv).")
            return True
        logger.warning("uv install failed, trying wheel download...")

    # Method 3: Direct wheel download + extract
    if verbose:
        logger.info("Trying direct wheel installation ...")
    if _install_wheels_direct(skill_dir, verbose=verbose):
        logger.info("Installed Python dependencies (via wheel download).")
        return True

    logger.error(
        "Warning: failed to install Python dependencies.\n"
        "  Install them manually with: %s -m pip install %s\n"
        "  Or install 'uv' (https://docs.astral.sh/uv/) and re-run 'spex init'.",
        sys.executable, skill_dir,
    )
    return False


def _install_wheels_direct(skill_dir, verbose=False):
    """Install dependencies by downloading and extracting wheels directly.

    Parses pyproject.toml to find dependencies, resolves them via PyPI,
    downloads wheels, and extracts them to site-packages.
    """
    site_packages = site.getsitepackages()[0]

    # Parse pyproject.toml for dependencies
    pyproject = skill_dir / "pyproject.toml"
    if not pyproject.is_file():
        return False

    deps = _parse_pyproject_deps(pyproject)
    if not deps:
        return True  # No deps to install

    for dep in deps:
        if verbose:
            logger.info("  Installing %s via wheel download ...", dep)
        if not _install_single_wheel(dep, site_packages, verbose=verbose):
            return False
    return True


def _parse_pyproject_deps(pyproject_path):
    """Extract runtime dependencies from pyproject.toml.

    Skips conditional deps (python_version constraints) since those
    are handled by the environment check separately.
    """
    content = pyproject_path.read_text(encoding="utf-8")
    # Find the [project] dependencies block
    match = re.search(
        r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL
    )
    if not match:
        return []

    deps = []
    for line in match.group(1).splitlines():
        line = line.strip().strip(",")
        if not line or line.startswith("#"):
            continue
        # Skip conditional dependencies (e.g. tomli for python < 3.11)
        if "python_version" in line:
            continue
        # Extract package name (before any version specifier)
        pkg = re.split(r"[><=!~;\[]", line)[0].strip().strip("\"'")
        if pkg:
            deps.append(pkg)
    return deps


def _install_single_wheel(pkg, site_packages, verbose=False):
    """Download and install a single package via wheel from PyPI."""
    pypi_url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        result = subprocess.run(
            ["curl", "-sL", pypi_url],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return False
        pypi_data = json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return False

    # Find a compatible wheel
    py_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    platform = "macosx" if sys.platform == "darwin" else ""
    arch = "arm64" if platform else ""

    files = pypi_data.get("urls", [])
    wheel_url = None
    for f in files:
        fn = f["filename"]
        if not fn.endswith(".whl"):
            continue
        # Prefer platform-specific wheel for current Python version
        if py_version in fn:
            if not platform or (platform in fn and arch in fn):
                wheel_url = f["url"]
                break
        # Fallback: pure Python wheel
        if "py3-none-any" in fn and wheel_url is None:
            wheel_url = f["url"]

    if wheel_url is None:
        return False

    try:
        with tempfile.NamedTemporaryFile(suffix=".whl", delete=False) as tmp:
            result = subprocess.run(
                ["curl", "-sL", wheel_url, "-o", tmp.name],
                capture_output=True, timeout=30,
            )
            if result.returncode != 0:
                return False

            z = zipfile.ZipFile(tmp.name)
            for name in z.namelist():
                if name.endswith("/"):
                    continue  # skip directory entries
                dest = os.path.join(site_packages, name)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(z.read(name))
            return True
    except (subprocess.TimeoutExpired, OSError, zipfile.BadZipFile):
        return False


def _install_cli(verbose=False, dry_run=False):
    """Install spex CLI symlink to ~/.local/bin."""
    import shutil as _shutil

    from common import _get_skill_path

    script_path = _get_skill_path() / "scripts" / "spex"
    link_dir = Path.home() / ".local" / "bin"
    link_path = link_dir / "spex"

    if dry_run:
        logger.info("Would install CLI: %s -> %s", link_path, script_path)
        return

    found = _shutil.which("spex")
    if found and Path(found).resolve() == script_path.resolve():
        logger.info("CLI already installed: %s", found)
        return

    try:
        link_dir.mkdir(parents=True, exist_ok=True)
        if link_path.is_symlink() or link_path.exists():
            link_path.unlink()
        link_path.symlink_to(script_path)
        logger.info("Installed CLI: %s -> %s", link_path, script_path)
    except PermissionError:
        logger.warning(
            "Warning: cannot install CLI to %s (permission denied)", link_dir
        )


def _resolve_target_dir(dir_path):
    """Resolve target directory for init.

    If dir_path is inside a git repo, returns the main worktree (handles
    submodules and linked worktrees). Otherwise returns dir_path as-is.
    """
    target = Path(dir_path).resolve()
    if not target.is_dir():
        logger.error("Error: not a directory: %s", dir_path)
        sys.exit(1)

    main_wt = get_main_worktree(str(target))
    return main_wt if main_wt is not None else target


def _init_target_toml(target_dir, verbose=False, dry_run=False):
    """Create .spex.toml in target_dir if it does not exist.

    The new file inherits effective config values from parent tomls.
    """
    toml_path = Path(target_dir) / ".spex.toml"
    if toml_path.is_file():
        logger.info("Config already exists: %s", toml_path)
        return

    if dry_run:
        logger.info("Would create: %s", toml_path)
        return

    effective = load_config(str(target_dir))
    content = generate_updated_toml(effective, force_keys={"spex_root"})
    toml_path.write_text(content, encoding="utf-8")
    logger.info("Created: %s", toml_path)


def _create_toml_config(workdir=None, verbose=False, dry_run=False):
    """Create or safely update .spex.toml files with the latest config schema."""
    ctx = get_project_context(workdir)

    if ctx.spex_tomls:
        changed = False
        for toml_path in ctx.spex_tomls:
            path = Path(toml_path)
            if dry_run:
                if safe_update_toml(path, dry_run=True):
                    logger.info("Would reinitialize: %s", path)
                else:
                    logger.info("Config up-to-date: %s", path)
            elif safe_update_toml(path):
                logger.info("Reinitialized: %s", path)
                changed = True
            else:
                logger.info("Config up-to-date: %s", path)
        if changed:
            clear_config_cache()
        return

    home_toml = Path.home() / ".spex.toml"
    if dry_run:
        if home_toml.is_file():
            if safe_update_toml(home_toml, dry_run=True):
                logger.info("Would reinitialize: %s", home_toml)
            else:
                logger.info("Config up-to-date: %s", home_toml)
        else:
            logger.info("Would create: %s", home_toml)
        return
    result = _create_default_toml()
    if result == "created":
        logger.info("Created: %s", home_toml)
        clear_config_cache()
    elif result == "updated":
        logger.info("Reinitialized: %s", home_toml)
        clear_config_cache()
    else:
        logger.info("Config up-to-date: %s", home_toml)


def run_init(
    workdir=None, target_dir=None, verbose=False, dry_run=False,
    skip_deps=False,
):
    """Run full spex initialization."""
    if dry_run:
        verbose = True

    if workdir is None:
        top = get_top_workdir()
        workdir = str(top) if top else None

    if skip_deps:
        logger.info("Skipping dependency installation (--skip-deps).")
    else:
        _install_deps(verbose=verbose, dry_run=dry_run)

    if target_dir:
        resolved = _resolve_target_dir(target_dir)
        _init_target_toml(resolved, verbose=verbose, dry_run=dry_run)
        if not dry_run:
            clear_config_cache()
        workdir = str(resolved)

    _create_toml_config(workdir=workdir, verbose=verbose, dry_run=dry_run)

    if dry_run and target_dir:
        effective = load_config(str(resolved))
        spex_root_val = effective.get("spex_root", ".spex")
        spex_root = Path(spex_root_val)
        if not spex_root.is_absolute():
            spex_root = resolved / spex_root
    else:
        ctx = get_project_context(workdir)
        spex_root = Path(ctx.spex_root)

    ensure_initialized(str(spex_root), verbose=verbose, dry_run=dry_run)
    _sync_all_templates(spex_root, verbose=verbose, dry_run=dry_run)

    _install_cli(verbose=verbose, dry_run=dry_run)
    logger.info("Initialization complete.")


def _build_parser() -> ArgumentParser:
    """Build the argument parser for ``spex init``."""
    parser = ArgumentParser(
        prog="spex init",
        description="Initialize the spex environment.",
    )
    parser.add_argument(
        "dir",
        nargs="?",
        default=None,
        help="Target directory to initialize (resolves to git main worktree)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if initialized (exit 0 = yes, exit 1 = no)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed operations during initialization",
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true",
        help="Preview operations without executing them",
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Skip Python dependency installation",
    )
    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse(argv)

    if args.check:
        sys.exit(0 if is_initialized() else 1)

    run_init(
        target_dir=args.dir,
        verbose=args.verbose,
        dry_run=args.dry_run,
        skip_deps=args.skip_deps,
    )


if __name__ == "__main__":
    from common import setup_logging
    setup_logging()
    main()
