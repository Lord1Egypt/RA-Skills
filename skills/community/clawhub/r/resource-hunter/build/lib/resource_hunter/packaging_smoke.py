from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import sysconfig
import tempfile
from pathlib import Path
from typing import Any

from ._version import __version__

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


_PROBED_MODULES = ("pip", "venv", "setuptools.build_meta", "wheel")
_WINDOWS_STORE_ALIAS_NAMES = {"python.exe", "python3.exe", "pythonw.exe", "python3w.exe"}
_BOOTSTRAPPABLE_BUILD_BLOCKERS = frozenset({"setuptools.build_meta", "wheel"})
_FALLBACK_BUILD_REQUIREMENTS = ("setuptools>=69", "wheel")
_MODULE_DISTRIBUTION_FALLBACKS = {"setuptools.build_meta": "setuptools"}
_MODULE_PROBE_SCRIPT = "\n".join(
    [
        "import importlib.metadata",
        "import importlib.util",
        "import json",
        "MODULES = ('pip', 'venv', 'setuptools.build_meta', 'wheel')",
        "DISTRIBUTION_FALLBACKS = {'setuptools.build_meta': 'setuptools'}",
        "def has_distribution(name):",
        "    try:",
        "        importlib.metadata.distribution(name)",
        "    except importlib.metadata.PackageNotFoundError:",
        "        return False",
        "    return True",
        "def has(name):",
        "    distribution = DISTRIBUTION_FALLBACKS.get(name)",
        "    try:",
        "        return importlib.util.find_spec(name) is not None",
        "    except AssertionError:",
        "        if distribution is not None:",
        "            return has_distribution(distribution)",
        "        return False",
        "    except ImportError:",
        "        return False",
        "print(json.dumps({name: has(name) for name in MODULES}))",
    ]
)


def _distribution_available(distribution_name: str) -> bool:
    try:
        importlib.metadata.distribution(distribution_name)
    except importlib.metadata.PackageNotFoundError:
        return False
    return True


def module_available(module_name: str) -> bool:
    distribution_name = _MODULE_DISTRIBUTION_FALLBACKS.get(module_name)
    try:
        return importlib.util.find_spec(module_name) is not None
    except AssertionError:
        if distribution_name is not None:
            return _distribution_available(distribution_name)
        return False
    except ImportError:
        return False


def packaging_blockers(*, has_pip: bool, has_build_backend: bool, has_wheel: bool) -> list[str]:
    blockers: list[str] = []
    if not has_pip:
        blockers.append("pip")
    if not has_build_backend:
        blockers.append("setuptools.build_meta")
    if not has_wheel:
        blockers.append("wheel")
    return blockers


def console_script_strategy(*, has_venv: bool, console_smoke_ready: bool) -> str:
    if not console_smoke_ready:
        return "blocked"
    return "venv" if has_venv else "prefix-install"


def strategy_family(strategy: str | None) -> str | None:
    if strategy is None:
        return None
    if strategy == "blocked":
        return "blocked"
    return "usable"


def _requested_project_root(project_root: Path | str | None) -> str | None:
    if project_root is None:
        return None
    return str(Path(project_root).resolve())


def _project_root_source(project_root: Path | str | None) -> str:
    return "argument" if project_root is not None else "discovered"


def _same_python(python_executable: str) -> bool:
    return os.path.normcase(os.path.abspath(python_executable)) == os.path.normcase(os.path.abspath(sys.executable))


def _module_statuses_via_subprocess(python_executable: str) -> dict[str, bool]:
    try:
        with tempfile.TemporaryDirectory(prefix="resource-hunter-module-probe-") as tmp_dir:
            probe_script = Path(tmp_dir) / "probe_packaging_modules.py"
            probe_script.write_text(_MODULE_PROBE_SCRIPT, encoding="utf-8")
            probe = _run_command([python_executable, str(probe_script)], cwd=Path.cwd())
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"Unable to inspect packaging modules via {python_executable}: {exc}") from exc

    if probe["returncode"] != 0:
        detail = (probe.get("stderr") or probe.get("stdout") or f"exit code {probe['returncode']}").strip()
        raise RuntimeError(f"Unable to inspect packaging modules via {python_executable}: {detail}")

    try:
        payload = json.loads(probe["stdout"])
    except json.JSONDecodeError as exc:
        detail = probe["stdout"].strip() or "<empty stdout>"
        raise RuntimeError(
            f"Unable to inspect packaging modules via {python_executable}: invalid probe output {detail!r}"
        ) from exc

    return {module_name: bool(payload.get(module_name)) for module_name in _PROBED_MODULES}


def _module_statuses(*, python_executable: str | None = None) -> dict[str, bool]:
    interpreter = python_executable or sys.executable
    if not python_executable or _same_python(python_executable):
        try:
            return {module_name: module_available(module_name) for module_name in _PROBED_MODULES}
        except AssertionError:
            return _module_statuses_via_subprocess(interpreter)

    return _module_statuses_via_subprocess(interpreter)


def _packaging_probe_error_status(error: str) -> dict[str, Any]:
    return {
        "pip": None,
        "venv": None,
        "setuptools_build_meta": None,
        "wheel": None,
        "wheel_build_ready": False,
        "python_module_smoke_ready": False,
        "console_script_smoke_ready": False,
        "full_packaging_smoke_ready": False,
        "blockers": [],
        "optional_gaps": [],
        "console_script_strategy": "blocked",
        "error": error,
    }


def packaging_status(*, python_executable: str | None = None) -> dict[str, Any]:
    try:
        module_status = _module_statuses(python_executable=python_executable)
    except RuntimeError as exc:
        return _packaging_probe_error_status(str(exc))

    has_pip = module_status["pip"]
    has_venv = module_status["venv"]
    has_build_backend = module_status["setuptools.build_meta"]
    has_wheel = module_status["wheel"]
    wheel_build_ready = has_pip and has_build_backend and has_wheel
    module_smoke_ready = wheel_build_ready
    console_smoke_ready = wheel_build_ready
    blockers = packaging_blockers(
        has_pip=has_pip,
        has_build_backend=has_build_backend,
        has_wheel=has_wheel,
    )
    optional_gaps = ["venv"] if not has_venv else []
    return {
        "pip": has_pip,
        "venv": has_venv,
        "setuptools_build_meta": has_build_backend,
        "wheel": has_wheel,
        "wheel_build_ready": wheel_build_ready,
        "python_module_smoke_ready": module_smoke_ready,
        "console_script_smoke_ready": console_smoke_ready,
        "full_packaging_smoke_ready": console_smoke_ready,
        "blockers": blockers,
        "optional_gaps": optional_gaps,
        "console_script_strategy": console_script_strategy(
            has_venv=has_venv,
            console_smoke_ready=console_smoke_ready,
        ),
    }


def annotate_project_packaging_status(
    packaging: dict[str, Any],
    *,
    project_root: Path | str | None = None,
    resolved_project_root: Path | str | None = None,
    include_bootstrap_metadata: bool = True,
) -> dict[str, Any]:
    annotated = dict(packaging)
    requested_root = _requested_project_root(project_root)
    resolved_root = Path(resolved_project_root).resolve() if resolved_project_root is not None else find_project_root(project_root)
    annotated["project_root"] = str(resolved_root) if resolved_root else None
    annotated["project_root_source"] = _project_root_source(project_root)
    if requested_root is not None:
        annotated["requested_project_root"] = requested_root
    if not include_bootstrap_metadata:
        return annotated
    blockers = annotated.get("blockers") or []
    bootstrap_ready = False
    bootstrap_requirements: list[str] = []
    bootstrap_strategy = annotated.get("console_script_strategy") or console_script_strategy(
        has_venv=bool(annotated.get("venv")),
        console_smoke_ready=bool(annotated.get("console_script_smoke_ready")),
    )
    if not annotated.get("error") and blockers and resolved_root is not None and _can_bootstrap_build_requirements(annotated):
        bootstrap_ready = True
        bootstrap_requirements = _project_build_requirements(resolved_root)
        bootstrap_strategy = console_script_strategy(has_venv=bool(annotated.get("venv")), console_smoke_ready=True)
    annotated["bootstrap_build_deps_ready"] = bootstrap_ready
    annotated["bootstrap_build_requirements"] = bootstrap_requirements
    annotated["bootstrap_console_script_strategy"] = bootstrap_strategy
    annotated["packaging_smoke_ready_with_bootstrap"] = bool(annotated.get("full_packaging_smoke_ready")) or bootstrap_ready
    return annotated


def _packaging_candidate_key(python_executable: str) -> str:
    return os.path.normcase(os.path.abspath(python_executable))


def _python_from_prefix(prefix: str | None) -> str | None:
    if not prefix:
        return None
    prefix_dir = Path(prefix)
    for candidate in (prefix_dir / "Scripts" / "python.exe", prefix_dir / "bin" / "python"):
        if candidate.exists():
            return str(candidate)
    return None


def _py_launcher_candidates() -> list[str]:
    launcher = shutil.which("py")
    if launcher is None:
        return []
    try:
        probe = _run_command([launcher, "-0p"], cwd=Path.cwd(), timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if probe["returncode"] != 0:
        return []

    candidates: list[str] = []
    seen: set[str] = set()
    for line in probe["stdout"].splitlines():
        match = re.search(r"([A-Za-z]:\\.*python(?:w)?\.exe)$", line.strip())
        if match is None:
            continue
        candidate = match.group(1)
        key = _packaging_candidate_key(candidate)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(candidate)
    return candidates


def _is_windows_store_python_alias(python_executable: str) -> bool:
    normalized = python_executable.replace("/", "\\").lower()
    if "\\microsoft\\windowsapps\\" not in normalized:
        return False
    return normalized.rsplit("\\", 1)[-1] in _WINDOWS_STORE_ALIAS_NAMES


def _packaging_python_candidates() -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = [("current", sys.executable)]
    for env_name, source in (("VIRTUAL_ENV", "virtual-env"), ("CONDA_PREFIX", "conda")):
        candidate = _python_from_prefix(os.environ.get(env_name))
        if candidate:
            candidates.append((source, candidate))
    for command in ("python", "python3"):
        candidate = shutil.which(command)
        if candidate:
            candidates.append((f"path:{command}", candidate))
    for candidate in _py_launcher_candidates():
        candidates.append(("py-launcher", candidate))

    unique_candidates: list[tuple[str, str]] = []
    seen: set[str] = set()
    for source, candidate in candidates:
        if source != "current" and _is_windows_store_python_alias(candidate):
            continue
        key = _packaging_candidate_key(candidate)
        if key in seen:
            continue
        seen.add(key)
        unique_candidates.append((source, candidate))
    return unique_candidates


def discover_packaging_pythons(
    *,
    project_root: Path | str | None = None,
    allow_bootstrap_build_deps: bool = False,
) -> list[dict[str, Any]]:
    resolved_root = find_project_root(project_root)
    discovered: list[dict[str, Any]] = []
    for source, python_executable in _packaging_python_candidates():
        status = annotate_project_packaging_status(
            packaging_status(python_executable=python_executable),
            project_root=project_root,
            resolved_project_root=resolved_root,
        )
        bootstrap_ready = bool(status.get("bootstrap_build_deps_ready"))
        discovered.append(
            {
                "python": python_executable,
                "source": source,
                "ready": bool(status.get("packaging_smoke_ready_with_bootstrap")) if allow_bootstrap_build_deps else bool(status.get("full_packaging_smoke_ready")),
                "bootstrap_ready": bootstrap_ready,
                "packaging": status,
            }
        )
    return discovered


def select_packaging_python(
    *,
    project_root: Path | str | None = None,
    allow_bootstrap_build_deps: bool = False,
) -> tuple[str | None, list[dict[str, Any]]]:
    candidates = discover_packaging_pythons(
        project_root=project_root,
        allow_bootstrap_build_deps=allow_bootstrap_build_deps,
    )
    for candidate in candidates:
        if candidate["ready"]:
            return candidate["python"], candidates
    return None, candidates


def find_project_root(start: Path | str | None = None) -> Path | None:
    candidate = Path(start or Path.cwd()).resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "src" / "resource_hunter").exists():
            return path
    return None


def _clean_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    return env


def _env_with_pythonpath(*paths: Path) -> dict[str, str]:
    env = _clean_env()
    pythonpath_entries = [str(path) for path in paths if path]
    if pythonpath_entries:
        env["PYTHONPATH"] = os.pathsep.join(pythonpath_entries)
    return env


def _project_build_requirements(project_root: Path) -> list[str]:
    if tomllib is None:
        return list(_FALLBACK_BUILD_REQUIREMENTS)

    pyproject_path = project_root / "pyproject.toml"
    try:
        pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return list(_FALLBACK_BUILD_REQUIREMENTS)

    requires = pyproject.get("build-system", {}).get("requires")
    if not isinstance(requires, list):
        return list(_FALLBACK_BUILD_REQUIREMENTS)

    requirements = [item for item in requires if isinstance(item, str) and item.strip()]
    return requirements or list(_FALLBACK_BUILD_REQUIREMENTS)


def _can_bootstrap_build_requirements(packaging: dict[str, Any]) -> bool:
    blockers = packaging.get("blockers") or []
    return bool(blockers) and bool(packaging.get("pip")) and set(blockers).issubset(_BOOTSTRAPPABLE_BUILD_BLOCKERS)


def _run_command(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: int = 180,
) -> dict[str, Any]:
    result = subprocess.run(
        args,
        cwd=str(cwd),
        env=env or _clean_env(),
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "command": args,
        "cwd": str(cwd),
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _venv_console_script(venv_dir: Path, script_name: str) -> Path:
    scripts_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    candidates = [scripts_dir / script_name]
    if os.name == "nt":
        candidates.insert(0, scripts_dir / f"{script_name}.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _prefix_paths(prefix_dir: Path) -> tuple[Path, list[Path]]:
    vars_map = {
        "base": str(prefix_dir),
        "platbase": str(prefix_dir),
        "installed_base": str(prefix_dir),
        "installed_platbase": str(prefix_dir),
    }
    scripts_dir = Path(sysconfig.get_path("scripts", vars=vars_map))
    site_paths: list[Path] = []
    for key in ("purelib", "platlib"):
        site_path = Path(sysconfig.get_path(key, vars=vars_map))
        if site_path not in site_paths:
            site_paths.append(site_path)
    return scripts_dir, site_paths


def _prefix_console_script(prefix_dir: Path, script_name: str) -> Path:
    scripts_dir, _ = _prefix_paths(prefix_dir)
    candidates = [scripts_dir / script_name]
    if os.name == "nt":
        candidates.insert(0, scripts_dir / f"{script_name}.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _prefix_env(prefix_dir: Path) -> dict[str, str]:
    env = _clean_env()
    _, site_paths = _prefix_paths(prefix_dir)
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in site_paths)
    return env


def _command_step(
    name: str,
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    stdout_contains: str | None = None,
    stdout_equals: str | None = None,
) -> dict[str, Any]:
    step = {"name": name, **_run_command(args, cwd=cwd, env=env)}
    stdout = step["stdout"]
    step["stdout_contains"] = stdout_contains
    step["stdout_equals"] = stdout_equals
    ok = step["returncode"] == 0
    if ok and stdout_contains is not None:
        ok = stdout_contains in stdout
    if ok and stdout_equals is not None:
        ok = stdout.strip() == stdout_equals
    step["ok"] = ok
    return step


def _append_failure(
    payload: dict[str, Any],
    reason: str,
    *,
    step: dict[str, Any] | None = None,
    step_name: str | None = None,
) -> dict[str, Any]:
    payload["ok"] = False
    payload["reason"] = reason
    failed_step = step_name or (step["name"] if step is not None else None)
    if failed_step is not None:
        payload["failed_step"] = failed_step
    return payload


def _annotate_packaging_python_payload(
    payload: dict[str, Any],
    *,
    packaging_python: str | None,
    packaging_python_source: str | None,
    packaging_python_candidates: list[dict[str, Any]] | None = None,
    packaging_python_auto_selected: bool | None = None,
) -> dict[str, Any]:
    payload["packaging_python"] = packaging_python or payload.get("python") or sys.executable
    if packaging_python_source is None:
        packaging_python_source = "argument" if packaging_python is not None else "current"
    payload["packaging_python_source"] = packaging_python_source
    if packaging_python_candidates is not None:
        payload["packaging_python_candidates"] = packaging_python_candidates
    if packaging_python_auto_selected is not None:
        payload["packaging_python_auto_selected"] = packaging_python_auto_selected
    return payload


def run_packaging_smoke(
    *,
    project_root: Path | str | None = None,
    python_executable: str | None = None,
    packaging_python_source: str | None = None,
    packaging_python_candidates: list[dict[str, Any]] | None = None,
    packaging_python_auto_selected: bool | None = None,
    bootstrap_build_deps: bool = False,
) -> dict[str, Any]:
    python_bin = python_executable or sys.executable
    requested_root = _requested_project_root(project_root)
    resolved_root = find_project_root(project_root)
    packaging = annotate_project_packaging_status(
        packaging_status(python_executable=python_bin),
        project_root=project_root,
        resolved_project_root=resolved_root,
    )
    strategy = packaging["console_script_strategy"]
    payload: dict[str, Any] = {
        "ok": False,
        "reason": "",
        "python": python_bin,
        "project_root": str(resolved_root) if resolved_root else None,
        "project_root_source": packaging.get("project_root_source"),
        "packaging": packaging,
        "strategy": strategy,
        "strategy_family": strategy_family(strategy),
        "workspace": None,
        "wheel": None,
        "console_script": None,
        "bootstrapped_build_requirements": [],
        "bootstrap_overlay": None,
        "steps": [],
    }
    if requested_root is not None:
        payload["requested_project_root"] = requested_root
    payload = _annotate_packaging_python_payload(
        payload,
        packaging_python=python_executable,
        packaging_python_source=packaging_python_source,
        packaging_python_candidates=packaging_python_candidates,
        packaging_python_auto_selected=packaging_python_auto_selected,
    )

    if resolved_root is None:
        return _append_failure(
            payload,
            "Packaging smoke requires a project root containing pyproject.toml and src/resource_hunter.",
            step_name="resolve-project-root",
        )

    packaging_error = packaging.get("error")
    if packaging_error:
        return _append_failure(payload, f"Packaging smoke is blocked: {packaging_error}", step_name="packaging-status")

    blockers = packaging.get("blockers") or []
    if blockers and not bootstrap_build_deps:
        blockers = ", ".join(packaging["blockers"])
        return _append_failure(payload, f"Packaging smoke is blocked: {blockers}", step_name="packaging-gate")

    with tempfile.TemporaryDirectory(prefix="resource-hunter-packaging-") as tmp_dir:
        workspace = Path(tmp_dir)
        payload["workspace"] = str(workspace)
        dist_dir = workspace / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        build_env: dict[str, str] | None = None

        if blockers:
            if not packaging.get("bootstrap_build_deps_ready"):
                joined_blockers = ", ".join(blockers)
                return _append_failure(
                    payload,
                    f"Packaging smoke is blocked: {joined_blockers}",
                    step_name="bootstrap-feasibility",
                )

            overlay_dir = workspace / "build-overlay"
            overlay_dir.mkdir(parents=True, exist_ok=True)
            requirements = packaging.get("bootstrap_build_requirements") or _project_build_requirements(resolved_root)
            bootstrap_step = _command_step(
                "bootstrap-build-deps",
                [
                    python_bin,
                    "-m",
                    "pip",
                    "install",
                    "--disable-pip-version-check",
                    "--no-input",
                    "--target",
                    str(overlay_dir),
                    *requirements,
                ],
                cwd=workspace,
            )
            payload["steps"].append(bootstrap_step)
            payload["bootstrapped_build_requirements"] = requirements
            payload["bootstrap_overlay"] = str(overlay_dir)
            if not bootstrap_step["ok"]:
                return _append_failure(payload, "Build dependency bootstrap failed.", step=bootstrap_step)

            build_env = _env_with_pythonpath(overlay_dir)
            strategy = packaging.get("bootstrap_console_script_strategy") or console_script_strategy(
                has_venv=bool(packaging.get("venv")),
                console_smoke_ready=True,
            )
            payload["strategy"] = strategy
            payload["strategy_family"] = strategy_family(strategy)

        build_step = _command_step(
            "build-wheel",
            [
                python_bin,
                "-m",
                "pip",
                "wheel",
                "--no-deps",
                "--no-build-isolation",
                "--wheel-dir",
                str(dist_dir),
                str(resolved_root),
            ],
            cwd=resolved_root,
            env=build_env,
        )
        payload["steps"].append(build_step)
        if not build_step["ok"]:
            return _append_failure(payload, "Wheel build failed.", step=build_step)

        wheels = sorted(dist_dir.glob("resource_hunter-*.whl"))
        if len(wheels) != 1:
            return _append_failure(
                payload,
                f"Expected exactly one wheel in {dist_dir}, found {len(wheels)}.",
                step_name="wheel-artifact",
            )

        wheel_path = wheels[0]
        payload["wheel"] = str(wheel_path)

        env: dict[str, str] | None = None
        install_cwd = workspace
        smoke_python = python_bin
        console_script: Path
        if strategy == "venv":
            import venv

            venv_dir = workspace / "venv"
            venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
            smoke_python = str(_venv_python(venv_dir))
            console_script = _venv_console_script(venv_dir, "resource-hunter")
            install_step = _command_step(
                "install-wheel",
                [smoke_python, "-m", "pip", "install", "--no-index", str(wheel_path)],
                cwd=install_cwd,
            )
        else:
            install_root = workspace / "prefix"
            env = _prefix_env(install_root)
            console_script = _prefix_console_script(install_root, "resource-hunter")
            install_step = _command_step(
                "install-wheel",
                [python_bin, "-m", "pip", "install", "--no-index", "--prefix", str(install_root), str(wheel_path)],
                cwd=install_cwd,
            )

        payload["steps"].append(install_step)
        if not install_step["ok"]:
            return _append_failure(payload, "Wheel installation failed.", step=install_step)

        payload["console_script"] = str(console_script)
        if not console_script.exists():
            return _append_failure(
                payload,
                f"Console script was not generated: {console_script}",
                step_name="console-script",
            )

        for step in (
            _command_step(
                "python-module-help",
                [smoke_python, "-m", "resource_hunter", "--help"],
                cwd=install_cwd,
                env=env,
                stdout_contains="usage:",
            ),
            _command_step(
                "python-module-version",
                [smoke_python, "-m", "resource_hunter", "--version"],
                cwd=install_cwd,
                env=env,
                stdout_equals=f"resource-hunter {__version__}",
            ),
            _command_step(
                "console-script-help",
                [str(console_script), "--help"],
                cwd=install_cwd,
                env=env,
                stdout_contains="usage:",
            ),
            _command_step(
                "console-script-version",
                [str(console_script), "--version"],
                cwd=install_cwd,
                env=env,
                stdout_equals=f"resource-hunter {__version__}",
            ),
        ):
            payload["steps"].append(step)
            if not step["ok"]:
                return _append_failure(payload, f"Packaging smoke step failed: {step['name']}.", step=step)

    payload["ok"] = True
    payload["reason"] = "Packaging smoke passed."
    return payload


def format_packaging_smoke_text(payload: dict[str, Any]) -> str:
    packaging_python = payload.get("packaging_python") or payload.get("python")
    packaging_python_source = payload.get("packaging_python_source")
    if packaging_python_source == "argument":
        python_label = f"{packaging_python} (via --python)"
    elif packaging_python_source == "environment":
        python_label = f"{packaging_python} (via RESOURCE_HUNTER_PACKAGING_PYTHON)"
    elif packaging_python_source == "auto":
        if payload.get("packaging_python_auto_selected"):
            python_label = f"{packaging_python} (auto-selected)"
        else:
            python_label = f"{packaging_python} (auto fallback to current interpreter)"
    else:
        python_label = f"{packaging_python} (current interpreter)"

    strategy = payload.get("strategy")
    if strategy == "prefix-install":
        strategy_text = "prefix fallback"
    else:
        strategy_text = strategy or "unknown"

    packaging = payload.get("packaging", {})
    blockers = packaging.get("blockers") or []
    project_root_source = payload.get("project_root_source") or packaging.get("project_root_source") or "unknown"
    lines = [
        "Resource Hunter packaging smoke",
        f"Python: {python_label}",
        f"project_root: {payload.get('project_root') or 'unresolved'}",
        f"project_root_source: {project_root_source}",
        f"strategy: {strategy_text}",
        f"strategy_family: {payload.get('strategy_family') or 'unknown'}",
        f"blockers: {', '.join(blockers) if blockers else 'none'}",
        f"result: {'ok' if payload.get('ok') else 'failed'}",
        f"reason: {payload.get('reason')}",
    ]
    requested_project_root = payload.get("requested_project_root")
    if requested_project_root and requested_project_root != payload.get("project_root"):
        lines.insert(3, f"requested_project_root: {requested_project_root}")
    if packaging.get("error"):
        lines.append(f"packaging_error: {packaging['error']}")
    if payload.get("wheel"):
        lines.append(f"wheel: {payload['wheel']}")
    if payload.get("console_script"):
        lines.append(f"console_script: {payload['console_script']}")
    if payload.get("bootstrapped_build_requirements"):
        lines.append(
            f"build_dependency_bootstrap: {', '.join(payload['bootstrapped_build_requirements'])}"
        )
    elif packaging.get("bootstrap_build_deps_ready"):
        lines.append(
            f"build_dependency_bootstrap_available: {', '.join(packaging.get('bootstrap_build_requirements') or [])}"
        )
    if payload.get("failed_step"):
        lines.append(f"failed_step: {payload['failed_step']}")
    steps = payload.get("steps") or []
    if steps:
        lines.append("")
        lines.append("Steps:")
        for step in steps:
            lines.append(f"- {step['name']}: {'ok' if step.get('ok') else 'failed'} (rc={step['returncode']})")
    candidates = payload.get("packaging_python_candidates") or []
    if candidates:
        lines.append("")
        lines.append("Auto-discovered packaging candidates:")
        for candidate in candidates:
            candidate_packaging = candidate.get("packaging", {})
            candidate_error = candidate_packaging.get("error")
            candidate_blockers = candidate_packaging.get("blockers") or []
            candidate_optional_gaps = candidate_packaging.get("optional_gaps") or []
            if candidate_error:
                detail = f"error: {candidate_error}"
            elif candidate.get("ready") and candidate.get("bootstrap_ready") and not candidate_packaging.get("full_packaging_smoke_ready"):
                strategy = candidate_packaging.get("bootstrap_console_script_strategy") or "unknown"
                detail = f"ready via bootstrap (strategy: {strategy})"
                if candidate_optional_gaps:
                    detail += f"; optional gaps: {', '.join(candidate_optional_gaps)}"
            elif candidate.get("ready"):
                if candidate_optional_gaps:
                    detail = f"ready (optional gaps: {', '.join(candidate_optional_gaps)})"
                else:
                    detail = "ready"
            else:
                detail = f"blocked ({', '.join(candidate_blockers) if candidate_blockers else 'unknown'})"
            lines.append(f"- {candidate['python']} [{candidate['source']}]: {detail}")
    return "\n".join(lines)
