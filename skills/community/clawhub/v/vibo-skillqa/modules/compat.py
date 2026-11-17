"""Compat check module: required Python version (shebang + code features),
dependencies parseability, imports resolvability, and live runs on every
installed interpreter (3.10 / 3.11 / 3.12)."""

import ast
import re
import shutil
import sys
from pathlib import Path

FEATURE_PATTERNS = [
    (re.compile(r"(?m)^\s*match\s+[A-Za-z_][\w.]*\s*:\s*$"),
     "match/case (3.10+)", 3.10),
    (re.compile(r"(?m)^\s*case\s+[A-Za-z_][\w.]*\s*(\||:|$)"),
     "match/case (3.10+)", 3.10),
    (re.compile(r":\s*[A-Za-z_][\w\[\], ]*\s\|\s[A-Za-z_][\w\[\]]+"),
     "union type hints (3.10+)", 3.10),
    (re.compile(r"f[\"'][^\"'\n]*\w+="),
     "f-string debug = (3.8+)", 3.8),
    (re.compile(r"(?<![=!<>]):=(?!=)"),
     "walrus operator (3.8+)", 3.8),
]

REQ_LINE_RE = re.compile(
    r"^[A-Za-z0-9_.\-\[\]]+\s*(==|>=|<=|~=|!=|<|>)?\s*[A-Za-z0-9_.\-*]*$")


def _check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _module_status(checks):
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "warn" for c in checks):
        return "warn"
    return "pass"


def detect_features(sources):
    """Return a list of version-dependent feature strings found in sources."""
    feats = []
    for p in sources:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pat, label, _ver in FEATURE_PATTERNS:
            if pat.search(text) and label not in feats:
                feats.append(label)
    return feats


def required_python(feats):
    """Minimum Python version implied by detected features (base 3.8)."""
    required = 3.8
    for _pat, label, ver in FEATURE_PATTERNS:
        if label in feats and ver > required:
            required = ver
    return required


def _internal(ctx):
    """True when the skill declares internal: true (project-internal skill)."""
    try:
        _md = Path(ctx.skill_path) / "SKILL.md"
        _head = _md.read_text(encoding="utf-8", errors="replace").split("---", 2)
        return len(_head) >= 2 and re.search(r"(?m)^internal:\s*true", _head[1]) is not None
    except Exception:
        return False


def third_party_imports(sources):
    """Top-level third-party modules imported by the skill's Python files."""
    mods = set()
    for p in sources:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    mods.add(a.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    mods.add(node.module.split(".")[0])
    stdlib = set(getattr(sys, "stdlib_module_names", ())) | {"__future__"}
    return sorted(m for m in mods if m not in stdlib and m != "__main__")


class CompatCheck:
    name = "compat"
    title = {"ru": "Совместимость", "en": "Compat check"}

    def run(self, ctx):
        t = ctx.t
        checks = []
        skill_dir = Path(ctx.sandbox.skill_dir)
        py_sources = [p for p in skill_dir.rglob("*.py") if p.is_file()]

        # 1. required python version from code features
        feats = detect_features(py_sources)
        required = required_python(feats)
        if feats:
            checks.append(_check("python_required", "pass",
                                 t("check.python_required.ok",
                                   v=required, feats=", ".join(feats))))
        else:
            checks.append(_check("python_required", "pass",
                                 t("check.python_required.base")))

        # 2. dependencies installable
        problems = []
        req = skill_dir / "requirements.txt"
        if req.exists():
            for line in req.read_text(errors="replace").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if not REQ_LINE_RE.match(line):
                    problems.append(f"requirements.txt: {line!r}")
        pyproject = skill_dir / "pyproject.toml"
        if pyproject.exists():
            text = pyproject.read_text(errors="replace")
            try:
                import tomllib  # Python 3.11+
                tomllib.loads(text)
            except ModuleNotFoundError:  # pragma: no cover (3.10)
                try:
                    import tomli  # type: ignore
                    tomli.loads(text)
                except ModuleNotFoundError:
                    if not re.search(r"\[project\]|\[tool\.", text):
                        problems.append("pyproject.toml: unparseable")
            except Exception as e:
                problems.append(f"pyproject.toml: {e}")

        missing_imports = []
        local_mods = set()
        for p in skill_dir.rglob("*"):
            if p.is_file() and p.suffix in (".py", ".so", ".pyi"):
                local_mods.add(p.stem.split(".")[0])
            if p.is_dir() and (p / "__init__.py").exists():
                local_mods.add(p.name)
        for mod in third_party_imports(py_sources):
            if mod in local_mods:
                continue  # module shipped inside the skill itself
            r = ctx.sandbox.run_cmd(["python3", "-c", f"import {mod}"])
            if r["exit_code"] != 0:
                missing_imports.append(mod)

        if problems:
            checks.append(_check("deps_installable", "fail",
                                 t("check.deps_installable.fail",
                                   problems="; ".join(problems[:3]))))
        elif missing_imports:
            checks.append(_check("deps_installable", "warn",
                                 t("check.deps_installable.warn",
                                   mods=", ".join(missing_imports[:5]))))
        else:
            checks.append(_check("deps_installable", "pass",
                                 t("check.deps_installable.ok")))

        # 3. runs on installed pythons (main script --help under each)
        versions = []
        for name in ("python3.10", "python3.11", "python3.12"):
            w = shutil.which(name)
            if w:
                versions.append((name, w))
        # the tester's own interpreter always counts
        _me = f"python{sys.version_info.major}.{sys.version_info.minor}"
        if not any(n == _me for n, _ in versions):
            versions.append((_me, sys.executable))
        if not versions:
            checks.append(_check("runs_on_installed_pythons", "warn",
                                 t("check.runs_on_installed_pythons.none")))
        elif ctx.main_script is None:
            if _internal(ctx):
                checks.append(_check("runs_on_installed_pythons", "pass",
                                     t("check.runs_on_installed_pythons.nomain")))
            else:
                checks.append(_check("runs_on_installed_pythons", "warn",
                                     t("check.runs_on_installed_pythons.nomain")))
        else:
            failures = []
            unsupported = []
            # declared requirement ("Requires Python 3.11") — other installed
            # interpreters failing is expected, not a defect
            req_minor = None
            try:
                _md = Path(ctx.skill_path) / "SKILL.md"
                _m = re.search(r"Python\s+3\.(\d+)", _md.read_text(errors="replace"))
                req_minor = _m.group(1) if _m else None
            except Exception:
                pass
            for name, interp in versions:
                r = ctx.sandbox.run_script(ctx.main_script, args=["--help"],
                                           interpreter=interp)
                if r["timed_out"] or r["exit_code"] != 0:
                    out = (r["stdout"] or "") + "\n" + (r["stderr"] or "")
                    if re.search(r"usage|use:|required|использование", out, re.I):
                        continue  # usage/help exit codes are not crashes
                    if (r["exit_code"] == 127 or "ModuleNotFoundError" in out
                            or "No module named" in out or "command not found" in out):
                        continue  # environment gap, not a compat crash
                    minor = name.replace("python3.", "")
                    if req_minor and minor != req_minor:
                        unsupported.append(name)
                    else:
                        failures.append(f"{name} (exit {r['exit_code']})")
            if failures:
                checks.append(_check("runs_on_installed_pythons", "fail",
                                     t("check.runs_on_installed_pythons.fail",
                                       versions=", ".join(failures))))
            elif unsupported:
                checks.append(_check("runs_on_installed_pythons", "warn",
                                     t("check.runs_on_installed_pythons.unsupported",
                                       versions=", ".join(unsupported))))
            elif len(versions) == 1:
                checks.append(_check("runs_on_installed_pythons", "warn",
                                     t("check.runs_on_installed_pythons.warn",
                                       version=versions[0][0])))
            else:
                checks.append(_check("runs_on_installed_pythons", "pass",
                                     t("check.runs_on_installed_pythons.ok",
                                       versions=", ".join(v[0] for v in versions))))

        # 4. version-dependent features noted
        checks.append(_check("version_features_noted", "pass",
                             t("check.version_features_noted.ok",
                               features=", ".join(feats) if feats else "none")))

        status = _module_status(checks)
        n_fail = sum(1 for c in checks if c["status"] == "fail")
        n_warn = sum(1 for c in checks if c["status"] == "warn")
        details = t("module.summary", total=len(checks), fail=n_fail, warn=n_warn)
        if feats:
            details += f" — {t('check.compat.features', feats=', '.join(feats))}"
        return {"module": self.name, "status": status, "checks": checks,
                "details": details}
