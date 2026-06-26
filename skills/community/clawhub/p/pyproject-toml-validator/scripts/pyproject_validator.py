#!/usr/bin/env python3
"""Validate pyproject.toml files for Python projects (PEP 517/621)."""

import sys
import json
import re
import os

try:
    import tomllib
except ImportError:
    tomllib = None

SEVERITIES = {"error": 3, "warning": 2, "info": 1}

VALID_BUILD_BACKENDS = [
    "setuptools.build_meta", "flit_core.buildapi", "hatchling.build",
    "pdm.backend", "poetry.core.masonry.api", "maturin", "scikit_build_core.build",
    "mesonpy", "whey",
]

SPDX_LICENSES = [
    "MIT", "Apache-2.0", "GPL-2.0-only", "GPL-2.0-or-later",
    "GPL-3.0-only", "GPL-3.0-or-later", "BSD-2-Clause", "BSD-3-Clause",
    "ISC", "MPL-2.0", "LGPL-2.1-only", "LGPL-2.1-or-later",
    "LGPL-3.0-only", "LGPL-3.0-or-later", "AGPL-3.0-only",
    "AGPL-3.0-or-later", "Unlicense", "CC0-1.0", "0BSD", "Artistic-2.0",
    "BSL-1.0", "ECL-2.0", "PSF-2.0", "Zlib",
]

TROVE_CLASSIFIER_PREFIXES = [
    "Development Status", "Environment", "Framework", "Intended Audience",
    "License", "Natural Language", "Operating System",
    "Programming Language", "Topic", "Typing",
]

KNOWN_TOOL_SECTIONS = [
    "ruff", "mypy", "pytest", "black", "isort", "pylint", "flake8",
    "coverage", "tox", "bandit", "pyright", "pydocstyle", "yapf",
    "autopep8", "setuptools", "hatch", "pdm", "poetry", "flit",
    "cibuildwheel", "towncrier", "bumpversion", "bump2version",
    "semantic_release", "commitizen", "numpydoc",
]

PROJECT_FIELDS = {
    "name", "version", "description", "readme", "requires-python",
    "license", "license-files", "authors", "maintainers", "keywords",
    "classifiers", "urls", "scripts", "gui-scripts", "entry-points",
    "dependencies", "optional-dependencies", "dynamic",
}

BUILD_SYSTEM_FIELDS = {"requires", "build-backend", "backend-path"}


def parse_toml(path):
    if tomllib:
        with open(path, "rb") as f:
            return tomllib.load(f)
    with open(path, "r") as f:
        content = f.read()
    return simple_toml_parse(content)


def simple_toml_parse(text):
    result = {}
    current = result
    stack = [result]
    current_key_path = []

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        header = re.match(r'^\[([^\[\]]+)\]$', stripped)
        array_header = re.match(r'^\[\[([^\[\]]+)\]\]$', stripped)

        if array_header:
            parts = [p.strip() for p in array_header.group(1).split(".")]
            current = result
            for i, part in enumerate(parts[:-1]):
                current = current.setdefault(part, {})
            key = parts[-1]
            if key not in current:
                current[key] = []
            entry = {}
            current[key].append(entry)
            current = entry
            current_key_path = parts
        elif header:
            parts = [p.strip().strip('"') for p in header.group(1).split(".")]
            current = result
            for part in parts:
                current = current.setdefault(part, {})
            current_key_path = parts
        else:
            m = re.match(r'^([A-Za-z0-9_\-."]+)\s*=\s*(.+)$', stripped)
            if m:
                key = m.group(1).strip().strip('"')
                val = parse_toml_value(m.group(2).strip())
                current[key] = val

    return result


def parse_toml_value(val):
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    if val.startswith("'") and val.endswith("'"):
        return val[1:-1]
    if val == "true":
        return True
    if val == "false":
        return False
    if val.startswith("["):
        inner = val[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in smart_split(inner, ","):
            item = item.strip()
            if item:
                items.append(parse_toml_value(item))
        return items
    if val.startswith("{"):
        inner = val[1:-1].strip()
        if not inner:
            return {}
        d = {}
        for pair in smart_split(inner, ","):
            pair = pair.strip()
            if "=" in pair:
                k, v = pair.split("=", 1)
                d[k.strip().strip('"')] = parse_toml_value(v.strip())
        return d
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


def smart_split(text, sep):
    parts = []
    depth = 0
    current = []
    in_str = None
    for ch in text:
        if ch in ('"', "'") and in_str is None:
            in_str = ch
        elif ch == in_str:
            in_str = None
        elif in_str is None:
            if ch in ("[", "{"):
                depth += 1
            elif ch in ("]", "}"):
                depth -= 1
            elif ch == sep and depth == 0:
                parts.append("".join(current))
                current = []
                continue
        current.append(ch)
    if current:
        parts.append("".join(current))
    return parts


def validate_project(data, issues):
    project = data.get("project", {})
    if not project:
        issues.append(("warning", "missing-project-table", "No [project] table found"))
        return

    if "name" not in project and "name" not in project.get("dynamic", []):
        issues.append(("error", "missing-name", "[project] must have 'name' field"))
    elif "name" in project:
        name = project["name"]
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$', str(name)):
            issues.append(("error", "invalid-name", f"Project name '{name}' doesn't match PEP 508 naming"))

    if "version" not in project and "version" not in project.get("dynamic", []):
        issues.append(("warning", "missing-version", "[project] should have 'version' or list it in 'dynamic'"))

    if "description" not in project:
        issues.append(("info", "missing-description", "[project] should have 'description'"))

    if "requires-python" in project:
        rp = str(project["requires-python"])
        if not re.match(r'^[><=!~]+\s*\d+(\.\d+)*(\s*,\s*[><=!~]+\s*\d+(\.\d+)*)*$', rp):
            issues.append(("warning", "invalid-requires-python", f"'requires-python' value '{rp}' may be malformed"))

    if "license" in project:
        lic = project["license"]
        if isinstance(lic, str):
            if lic not in SPDX_LICENSES and not lic.startswith("LicenseRef-"):
                issues.append(("info", "unknown-license", f"License '{lic}' not in common SPDX list"))
        elif isinstance(lic, dict):
            if "text" not in lic and "file" not in lic:
                issues.append(("warning", "invalid-license-table", "License table should have 'text' or 'file'"))

    if "classifiers" in project:
        classifiers = project["classifiers"]
        if isinstance(classifiers, list):
            for clf in classifiers:
                if isinstance(clf, str):
                    prefix = clf.split(" :: ")[0] if " :: " in clf else ""
                    if prefix and prefix not in TROVE_CLASSIFIER_PREFIXES:
                        issues.append(("info", "unknown-classifier-prefix", f"Classifier prefix '{prefix}' not recognized"))

    if "keywords" in project:
        kw = project["keywords"]
        if isinstance(kw, list) and len(kw) > 20:
            issues.append(("info", "too-many-keywords", f"Found {len(kw)} keywords — consider limiting to ~10-15"))

    if "authors" in project:
        authors = project["authors"]
        if isinstance(authors, list):
            for i, author in enumerate(authors):
                if isinstance(author, dict) and "name" not in author and "email" not in author:
                    issues.append(("warning", "empty-author", f"Author #{i+1} has no 'name' or 'email'"))

    if "dependencies" in project:
        deps = project["dependencies"]
        if isinstance(deps, list):
            validate_dependency_list(deps, "dependencies", issues)

    if "optional-dependencies" in project:
        opt = project["optional-dependencies"]
        if isinstance(opt, dict):
            for group, deps in opt.items():
                if isinstance(deps, list):
                    validate_dependency_list(deps, f"optional-dependencies.{group}", issues)

    for key in project:
        if key not in PROJECT_FIELDS:
            issues.append(("warning", "unknown-project-field", f"Unknown field '{key}' in [project]"))

    if "dynamic" in project:
        dynamic = project["dynamic"]
        if isinstance(dynamic, list):
            for field in dynamic:
                if field == "name":
                    issues.append(("error", "name-in-dynamic", "'name' cannot be listed in 'dynamic'"))
                if field not in PROJECT_FIELDS:
                    issues.append(("warning", "unknown-dynamic-field", f"Unknown dynamic field '{field}'"))
                if field in project and field != "name":
                    issues.append(("warning", "static-and-dynamic", f"Field '{field}' is both static and listed in 'dynamic'"))


def validate_dependency_list(deps, section, issues):
    seen = {}
    for dep in deps:
        if not isinstance(dep, str):
            continue
        pkg = re.split(r'[><=!~\[;@\s]', dep)[0].strip().lower()
        pkg_normalized = re.sub(r'[-_.]+', '-', pkg)
        if pkg_normalized in seen:
            issues.append(("warning", "duplicate-dependency", f"Duplicate dependency '{pkg}' in {section} (also at index {seen[pkg_normalized]})"))
        seen[pkg_normalized] = deps.index(dep)

        if dep.strip() == pkg and not re.search(r'[><=!~@]', dep):
            issues.append(("info", "unpinned-dependency", f"Dependency '{pkg}' in {section} has no version constraint"))


def validate_build_system(data, issues):
    bs = data.get("build-system", {})
    if not bs:
        issues.append(("warning", "missing-build-system", "No [build-system] table — needed for PEP 517"))
        return

    if "requires" not in bs:
        issues.append(("error", "missing-build-requires", "[build-system] must have 'requires'"))
    elif isinstance(bs["requires"], list) and len(bs["requires"]) == 0:
        issues.append(("error", "empty-build-requires", "[build-system].requires is empty"))

    if "build-backend" not in bs:
        issues.append(("warning", "missing-build-backend", "[build-system] should specify 'build-backend'"))
    elif isinstance(bs["build-backend"], str):
        backend = bs["build-backend"]
        if backend not in VALID_BUILD_BACKENDS:
            issues.append(("info", "unusual-build-backend", f"Build backend '{backend}' is not a common choice"))

    for key in bs:
        if key not in BUILD_SYSTEM_FIELDS:
            issues.append(("warning", "unknown-build-system-field", f"Unknown field '{key}' in [build-system]"))


def validate_tool_sections(data, issues):
    tool = data.get("tool", {})
    if not tool:
        return

    for section in tool:
        if section not in KNOWN_TOOL_SECTIONS:
            issues.append(("info", "unknown-tool-section", f"Tool section [tool.{section}] not in common tools list"))

    if "ruff" in tool:
        validate_ruff(tool["ruff"], issues)

    if "mypy" in tool:
        validate_mypy(tool["mypy"], issues)

    if "pytest" in tool:
        validate_pytest(tool["pytest"], issues)

    if "black" in tool:
        validate_black(tool["black"], issues)

    if "isort" in tool:
        validate_isort(tool["isort"], issues)

    if "black" in tool and "ruff" in tool:
        ruff_conf = tool["ruff"]
        if isinstance(ruff_conf, dict):
            format_conf = ruff_conf.get("format", {})
            if isinstance(format_conf, dict) and format_conf:
                issues.append(("info", "ruff-and-black", "[tool.ruff.format] and [tool.black] both present — may conflict"))

    if "isort" in tool and "ruff" in tool:
        ruff_conf = tool["ruff"]
        if isinstance(ruff_conf, dict):
            lint = ruff_conf.get("lint", ruff_conf)
            select = lint.get("select", [])
            if isinstance(select, list) and "I" in select:
                issues.append(("info", "ruff-isort-and-isort", "Ruff 'I' rules enabled alongside [tool.isort] — may conflict"))


def validate_ruff(conf, issues):
    if not isinstance(conf, dict):
        return
    if "line-length" in conf:
        ll = conf["line-length"]
        if isinstance(ll, int) and (ll < 40 or ll > 200):
            issues.append(("warning", "ruff-line-length", f"Ruff line-length={ll} is unusual (typical: 79-120)"))

    if "target-version" in conf:
        tv = str(conf["target-version"])
        if not re.match(r'^py3\d+$', tv):
            issues.append(("warning", "ruff-target-version", f"Ruff target-version '{tv}' format should be 'py3XX'"))

    lint = conf.get("lint", {})
    if isinstance(lint, dict):
        select = lint.get("select", [])
        ignore = lint.get("ignore", [])
        if isinstance(select, list) and isinstance(ignore, list):
            overlap = set(select) & set(ignore)
            if overlap:
                issues.append(("warning", "ruff-select-ignore-overlap", f"Ruff rules in both select and ignore: {', '.join(sorted(overlap))}"))


def validate_mypy(conf, issues):
    if not isinstance(conf, dict):
        return
    if "python_version" in conf:
        pv = str(conf["python_version"])
        if not re.match(r'^3\.\d+$', pv):
            issues.append(("warning", "mypy-python-version", f"mypy python_version '{pv}' format should be '3.X'"))

    bool_opts = ["strict", "ignore_missing_imports", "warn_return_any",
                 "warn_unused_configs", "disallow_untyped_defs",
                 "disallow_any_generics", "check_untyped_defs"]
    for opt in bool_opts:
        if opt in conf and not isinstance(conf[opt], bool):
            issues.append(("warning", "mypy-type-mismatch", f"mypy option '{opt}' should be boolean, got {type(conf[opt]).__name__}"))


def validate_pytest(conf, issues):
    if not isinstance(conf, dict):
        return
    ini = conf.get("ini_options", conf)
    if isinstance(ini, dict):
        if "addopts" in ini:
            addopts = str(ini["addopts"])
            if "--no-header" in addopts and "-q" in addopts and "--tb=no" in addopts:
                issues.append(("info", "pytest-silent", "pytest addopts suppresses most output — may hide useful info"))
        if "testpaths" in ini:
            tp = ini["testpaths"]
            if isinstance(tp, list) and len(tp) == 0:
                issues.append(("warning", "pytest-empty-testpaths", "pytest testpaths is empty"))


def validate_black(conf, issues):
    if not isinstance(conf, dict):
        return
    if "line-length" in conf:
        ll = conf["line-length"]
        if isinstance(ll, int) and (ll < 40 or ll > 200):
            issues.append(("warning", "black-line-length", f"Black line-length={ll} is unusual"))
    if "target-version" in conf:
        tv = conf["target-version"]
        if isinstance(tv, list):
            for v in tv:
                if not re.match(r'^py3\d+$', str(v)):
                    issues.append(("warning", "black-target-version", f"Black target-version '{v}' format should be 'py3XX'"))


def validate_isort(conf, issues):
    if not isinstance(conf, dict):
        return
    if "profile" in conf:
        profile = str(conf["profile"])
        valid_profiles = ["black", "django", "pycharm", "google", "open_stack", "plone", "attrs", "hug"]
        if profile not in valid_profiles:
            issues.append(("warning", "isort-unknown-profile", f"isort profile '{profile}' not recognized"))


def validate_file(path):
    issues = []

    if not os.path.exists(path):
        return [("error", "file-not-found", f"File not found: {path}")]

    try:
        data = parse_toml(path)
    except Exception as e:
        return [("error", "parse-error", f"Failed to parse TOML: {e}")]

    validate_project(data, issues)
    validate_build_system(data, issues)
    validate_tool_sections(data, issues)

    top_level_known = {"project", "build-system", "tool"}
    for key in data:
        if key not in top_level_known and key != "dependency-groups":
            issues.append(("info", "unknown-top-level", f"Unknown top-level table '[{key}]'"))

    return issues


def format_text(issues, path):
    if not issues:
        return f"✅ {path}: no issues found"
    lines = [f"{'❌' if any(s == 'error' for s, _, _ in issues) else '⚠️'} {path}: {len(issues)} issue(s)\n"]
    for severity, rule, msg in sorted(issues, key=lambda x: -SEVERITIES.get(x[0], 0)):
        icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(severity, "•")
        lines.append(f"  {icon} [{severity}] {rule}: {msg}")
    return "\n".join(lines)


def format_json(issues, path):
    return json.dumps({
        "file": path,
        "issues": [{"severity": s, "rule": r, "message": m} for s, r, m in issues],
        "summary": {
            "total": len(issues),
            "errors": sum(1 for s, _, _ in issues if s == "error"),
            "warnings": sum(1 for s, _, _ in issues if s == "warning"),
            "info": sum(1 for s, _, _ in issues if s == "info"),
        }
    }, indent=2)


def format_summary(issues, path):
    errs = sum(1 for s, _, _ in issues if s == "error")
    warns = sum(1 for s, _, _ in issues if s == "warning")
    infos = sum(1 for s, _, _ in issues if s == "info")
    status = "FAIL" if errs else ("WARN" if warns else "PASS")
    return f"{status} | {path} | {len(issues)} issues ({errs} errors, {warns} warnings, {infos} info)"


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("Usage: pyproject_validator.py <command> [options] <file>")
        print()
        print("Commands:")
        print("  validate    Full validation (project + build-system + tools)")
        print("  project     Validate [project] table only")
        print("  build       Validate [build-system] table only")
        print("  tools       Validate [tool.*] sections only")
        print()
        print("Options:")
        print("  --format text|json|summary   Output format (default: text)")
        print("  --min-severity error|warning|info   Filter by minimum severity")
        print("  --strict                     Exit 1 on any issue")
        print()
        print("Examples:")
        print("  pyproject_validator.py validate pyproject.toml")
        print("  pyproject_validator.py project --format json pyproject.toml")
        print("  pyproject_validator.py tools --min-severity warning pyproject.toml")
        sys.exit(0)

    cmd = args[0]
    fmt = "text"
    min_sev = "info"
    strict = False
    path = None

    i = 1
    while i < len(args):
        if args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif args[i] == "--min-severity" and i + 1 < len(args):
            min_sev = args[i + 1]
            i += 2
        elif args[i] == "--strict":
            strict = True
            i += 1
        else:
            path = args[i]
            i += 1

    if not path:
        path = "pyproject.toml"

    if not os.path.exists(path):
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(2)

    try:
        data = parse_toml(path)
    except Exception as e:
        print(f"Error parsing {path}: {e}", file=sys.stderr)
        sys.exit(2)

    issues = []

    if cmd == "validate":
        validate_project(data, issues)
        validate_build_system(data, issues)
        validate_tool_sections(data, issues)
        for key in data:
            if key not in {"project", "build-system", "tool", "dependency-groups"}:
                issues.append(("info", "unknown-top-level", f"Unknown top-level table '[{key}]'"))
    elif cmd == "project":
        validate_project(data, issues)
    elif cmd == "build":
        validate_build_system(data, issues)
    elif cmd == "tools":
        validate_tool_sections(data, issues)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(2)

    min_level = SEVERITIES.get(min_sev, 1)
    issues = [(s, r, m) for s, r, m in issues if SEVERITIES.get(s, 0) >= min_level]

    if fmt == "json":
        print(format_json(issues, path))
    elif fmt == "summary":
        print(format_summary(issues, path))
    else:
        print(format_text(issues, path))

    if strict and issues:
        sys.exit(1)
    elif any(s == "error" for s, _, _ in issues):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
