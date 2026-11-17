from __future__ import annotations

import importlib.util

from .common import *

SUBPROCESS_EXEC_CALL_NAMES = {"run", "Popen", "call", "check_call", "check_output"}
EVIDENCE_FILE_LIST_LIMIT = 8


def is_generated_python_cache(path: Path) -> bool:
    return "__pycache__" in {part.lower() for part in path.parts} or path.suffix.lower() in {".pyc", ".pyo"}


def normalized_relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def audit_definition_relative_paths() -> set[str]:
    base = Path("scripts") / "skill_usefulness_audit_lib"
    return {
        (base / "common.py").as_posix(),
        (base / "constants.py").as_posix(),
        (base / "reporting.py").as_posix(),
        (base / "risk_signatures.py").as_posix(),
        (base / "risk_signatures_encoding.py").as_posix(),
        (base / "risk_signatures_execution.py").as_posix(),
        (base / "risk_signatures_network.py").as_posix(),
        (base / "risk_signatures_sensitive.py").as_posix(),
        (base / "risk_quality.py").as_posix(),
    }


def add_risk_hit(hits: dict[str, dict[str, object]], label: str, severity: float, relative: str) -> None:
    hit = hits.setdefault(label, {"severity": severity, "files": []})
    hit["severity"] = max(float(hit["severity"]), severity)
    files = hit["files"]
    if isinstance(files, list) and relative not in files and len(files) < 3:
        files.append(relative)


def risk_result_from_hits(hits: dict[str, dict[str, object]]) -> dict[str, object]:
    risk_score = round(sum(float(item["severity"]) for item in hits.values()), 2)
    if risk_score >= 4.0:
        risk_level = "high"
    elif risk_score >= 2.0:
        risk_level = "medium"
    elif risk_score > 0:
        risk_level = "low"
    else:
        risk_level = "none"

    evidence = [
        {"label": label, "severity": item["severity"], "files": item["files"]}
        for label, item in sorted(hits.items())
    ]
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_flags": [item["label"] for item in evidence],
        "risk_evidence": evidence,
    }


def python_exec_call_labels(text: str) -> set[str]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set()

    subprocess_aliases = {"subprocess"}
    os_aliases = {"os"}
    subprocess_call_names: set[str] = set()
    labels: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "subprocess":
                    subprocess_aliases.add(alias.asname or alias.name)
                if alias.name == "os":
                    os_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            for alias in node.names:
                if alias.name in SUBPROCESS_EXEC_CALL_NAMES:
                    subprocess_call_names.add(alias.asname or alias.name)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in subprocess_call_names:
                labels.add("script-exec-call")
            elif func.id in {"eval", "exec"}:
                labels.add("dynamic-exec")
        elif isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.value.id in subprocess_aliases and func.attr in SUBPROCESS_EXEC_CALL_NAMES:
                labels.add("script-exec-call")
            elif func.value.id in os_aliases and func.attr == "system":
                labels.add("script-exec-call")
    return labels


def install_surface_labels(path: Path, relative: str, text: str) -> set[str]:
    labels: set[str] = set()
    name = path.name.lower()
    if name == "package.json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {}
        scripts = payload.get("scripts") if isinstance(payload, dict) else None
        if isinstance(scripts, dict) and any(key in scripts for key in INSTALL_LIFECYCLE_SCRIPT_KEYS):
            labels.add("install-hook")
    elif name == "setup.py":
        labels.add("packaging-exec-surface")
    elif name == "pyproject.toml" and re.search(r"(?m)^\s*build-backend\s*=", text):
        labels.add("packaging-exec-surface")
    elif relative.startswith(".github/workflows/") and re.search(r"(?m)^\s*run\s*:", text):
        labels.add("ci-automation-surface")
    return labels


def markdown_container_line(line: str) -> tuple[str, int, int, bool]:
    value = line
    quote_depth = 0
    while True:
        quote = re.match(r"^ {0,3}>[ \t]?", value)
        if not quote:
            break
        quote_depth += 1
        value = value[quote.end() :]
    indent = len(value) - len(value.lstrip(" \t"))
    value = value.lstrip(" \t")
    list_marker = re.match(r"(?:[-+*]|\d+[.)])(?:[ \t]+)", value)
    has_list_marker = bool(list_marker)
    if list_marker:
        indent += list_marker.end()
        value = value[list_marker.end() :].lstrip(" \t")
    return value, quote_depth, indent, has_list_marker


def preceding_list_indent(
    lines: list[tuple[str, int, int, bool]],
    index: int,
    quote_depth: int,
    opening_indent: int,
) -> int | None:
    if opening_indent <= 0:
        return None
    cursor = index - 1
    while cursor >= 0:
        line, current_quote_depth, indent, has_list_marker = lines[cursor]
        if current_quote_depth != quote_depth:
            break
        if not line.strip():
            cursor -= 1
            continue
        if has_list_marker and indent <= opening_indent:
            return indent
        if indent < opening_indent:
            break
        cursor -= 1
    return None


def fenced_code_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    lines = [markdown_container_line(line) for line in text.splitlines()]
    opening_pattern = re.compile(r"^(`{3,}|~{3,})[^\n]*$")
    index = 0
    while index < len(lines):
        opening_line, opening_quote_depth, opening_indent, opening_list_marker = lines[index]
        opening_list_container = (
            opening_list_marker
            or opening_indent >= 4
            or preceding_list_indent(lines, index, opening_quote_depth, opening_indent) is not None
        )
        opening = opening_pattern.match(opening_line)
        if not opening:
            index += 1
            continue
        marker = opening.group(1)
        marker_char = marker[0]
        marker_length = len(marker)
        closing_pattern = re.compile(rf"^{re.escape(marker_char) * marker_length}{re.escape(marker_char)}*\s*$")
        content: list[str] = []
        index += 1
        container_boundary = False
        while index < len(lines):
            line, quote_depth, indent, _list_marker = lines[index]
            if line.strip() and opening_quote_depth and quote_depth < opening_quote_depth:
                container_boundary = True
                break
            if (
                line.strip()
                and opening_list_container
                and quote_depth == opening_quote_depth
                and indent < opening_indent
            ):
                container_boundary = True
                break
            if closing_pattern.match(line):
                break
            content.append(line)
            index += 1
        if content and "\n".join(content).strip():
            blocks.append("\n".join(content))
        if index < len(lines) and closing_pattern.match(lines[index][0]):
            index += 1
        elif container_boundary:
            continue
    return blocks


def scan_risk_text(
    hits: dict[str, dict[str, object]],
    path: Path,
    relative: str,
    text: str,
) -> None:
    text_lower = text.lower()
    suffix = path.suffix.lower()
    for rule in COMPILED_RISK_RULES:
        label = str(rule["label"])
        if suffix == ".py" and label == "shell-exec":
            continue
        if any(pattern.search(text_lower) for pattern in rule["patterns"]):
            add_risk_hit(hits, label, float(rule["severity"]), relative)
    if suffix == ".py":
        for label in python_exec_call_labels(text):
            severity = 2.0 if label == "dynamic-exec" else 1.0
            add_risk_hit(hits, label, severity, relative)
    for label in install_surface_labels(path, relative, text):
        severity = 2.0 if label == "install-hook" else 1.0
        add_risk_hit(hits, label, severity, relative)


def scan_risk(
    root: Path,
    self_relative_path: Path | None = None,
    ignored_relative_paths: set[str] | None = None,
    skill_markdown_text: str | None = None,
) -> dict[str, object]:
    hits: dict[str, dict[str, object]] = {}
    ignored_paths = set(ignored_relative_paths or set())
    linked_reference_paths = set(referenced_paths_from_body(skill_markdown_text or ""))
    if self_relative_path is not None:
        ignored_paths.add(self_relative_path.as_posix())
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if is_generated_python_cache(path):
            continue
        relative_path = path.relative_to(root)
        relative = relative_path.as_posix()
        if relative in ignored_paths:
            continue
        relative_parts = {part.lower() for part in relative_path.parts}
        if "references" in relative_parts:
            if relative not in linked_reference_paths or path.suffix.lower() not in TEXT_FILE_SUFFIXES:
                continue
            try:
                if path.stat().st_size > MAX_SCAN_BYTES:
                    continue
            except OSError:
                continue
            code_blocks = fenced_code_blocks(read_text(path))
            if code_blocks:
                scan_risk_text(hits, path, relative, "\n".join(code_blocks))
            continue
        if path.name == "SKILL.md":
            text = skill_markdown_text if skill_markdown_text is not None else read_text(path)
            code_blocks = fenced_code_blocks(text)
            if code_blocks:
                scan_risk_text(hits, path, relative, "\n".join(code_blocks))
            continue
        if path.suffix.lower() not in RISK_SCAN_SUFFIXES:
            continue
        if relative_path.parent != Path(".") and not any(part.lower() in RISK_SCAN_DIRS for part in relative_path.parts[:-1]):
            continue
        try:
            if path.stat().st_size > MAX_SCAN_BYTES:
                continue
        except OSError:
            continue
        text = read_text(path)
        scan_risk_text(hits, path, relative, text)

    return risk_result_from_hits(hits)


def promote_private_content_risk(risk: dict[str, object], quality: dict[str, object]) -> dict[str, object]:
    hits: dict[str, dict[str, object]] = {}
    for item in risk.get("risk_evidence", []):
        if not isinstance(item, dict):
            continue
        label = str(item.get("label", "") or "")
        if not label:
            continue
        hits[label] = {
            "severity": float(item.get("severity", 0.0) or 0.0),
            "files": list(item.get("files", []) or [])[:3],
        }
    for item in quality.get("static_quality_evidence", []):
        if not isinstance(item, dict) or item.get("label") != "private-content-artifact":
            continue
        files = list(item.get("files", []) or [])
        if files:
            for relative in files[:3]:
                add_risk_hit(hits, "private-content-artifact", 4.0, str(relative))
        else:
            add_risk_hit(hits, "private-content-artifact", 4.0, "bundle")
    return risk_result_from_hits(hits)


def relative_label(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def text_profile_for_files(root: Path, files: list[Path]) -> tuple[int, dict[str, dict[str, object]]]:
    total = 0
    profiles: dict[str, dict[str, object]] = {}
    for path in files:
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        size = file_size(path)
        label = relative_label(root, path)
        if size > MAX_SCAN_BYTES:
            units = math.ceil(size / TEXT_BYTES_PER_CONTEXT_UNIT)
            total += units
            profiles[label] = {
                "context_units": units,
                "lines": None,
                "has_toc": False,
                "read": False,
            }
            continue
        text = read_text(path)
        units = estimate_context_units(text)
        total += units
        profiles[label] = {
            "context_units": units,
            "lines": text.count("\n") + (1 if text else 0),
            "has_toc": has_reference_toc(text),
            "read": True,
        }
    return total, profiles


def resource_metrics(root: Path, dirname: str) -> dict[str, object]:
    files = sorted_files(root / dirname)
    context_units, text_profiles = text_profile_for_files(root, files)
    return {
        "count": len(files),
        "bytes": sum(file_size(path) for path in files),
        "context_units": context_units,
        "files": files,
        "text_profiles": text_profiles,
    }


def quality_issue(
    label: str,
    penalty: float,
    reason: str,
    files: list[str] | None = None,
    metrics: dict[str, object] | None = None,
) -> dict[str, object]:
    item: dict[str, object] = {
        "label": label,
        "penalty": round(penalty, 2),
        "reason": reason,
    }
    if files:
        item["files"] = files
    if metrics:
        item["metrics"] = metrics
    return item


GENERIC_REFERENCE_STEMS = {"guide", "guides", "reference", "references", "doc", "docs", "notes", "workflow", "workflows"}
PRIVATE_ROOT_CONTENT_SUFFIXES = {".cfg", ".conf", ".env", ".ini", ".json", ".properties", ".toml", ".yaml", ".yml"}


def reference_is_directly_disclosed(body_lower: str, root: Path, path: Path) -> bool:
    relative = relative_label(root, path).lower()
    filename = path.name.lower()
    stem = path.stem.lower()
    if relative in body_lower or filename in body_lower:
        return True
    if len(stem) < 5 or stem in GENERIC_REFERENCE_STEMS:
        return False
    return re.search(rf"(?<![a-z0-9_-]){re.escape(stem)}(?![a-z0-9_-])", body_lower) is not None


def has_reference_toc(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in REFERENCE_TOC_MARKERS)


def vague_resource_files(root: Path, files: list[Path]) -> list[str]:
    matches = []
    for path in files:
        stem = path.stem
        if any(pattern.search(stem) for pattern in VAGUE_RESOURCE_NAME_PATTERNS):
            matches.append(relative_label(root, path))
    return matches


def python_syntax_error_files(root: Path, files: list[Path]) -> list[str]:
    matches = []
    for path in files:
        if path.suffix.lower() != ".py" or file_size(path) > MAX_SCAN_BYTES:
            continue
        try:
            ast.parse(read_text(path), filename=str(path))
        except SyntaxError:
            matches.append(relative_label(root, path))
    return matches


def module_candidates(base: Path, parts: list[str]) -> list[Path]:
    if not parts:
        return []
    path = base.joinpath(*parts)
    return [path.with_suffix(".py"), path / "__init__.py"]


def local_module_exists(base: Path, parts: list[str]) -> bool:
    return any(candidate.exists() for candidate in module_candidates(base, parts))


def absolute_module_available(path: Path, root: Path, module: str) -> bool:
    parts = module.split(".")
    search_roots = [path.parent, root, root / "scripts"]
    if any(local_module_exists(base, parts) for base in search_roots):
        return True
    top_level = parts[0]
    if top_level in getattr(sys, "stdlib_module_names", set()):
        return True
    try:
        return importlib.util.find_spec(top_level) is not None
    except (ImportError, AttributeError, ValueError):
        return False


def python_import_error_files(root: Path, files: list[Path]) -> list[str]:
    class SameScopeImportVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.imports: list[ast.Import | ast.ImportFrom] = []

        def visit_Import(self, node: ast.Import) -> None:
            self.imports.append(node)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            self.imports.append(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

    def same_scope_import_ids(statements: list[ast.stmt]) -> set[int]:
        visitor = SameScopeImportVisitor()
        for statement in statements:
            visitor.visit(statement)
        return {id(node) for node in visitor.imports}

    matches: list[str] = []
    for path in files:
        if path.suffix.lower() != ".py" or file_size(path) > MAX_SCAN_BYTES:
            continue
        try:
            tree = ast.parse(read_text(path), filename=str(path))
        except SyntaxError:
            continue
        optional_imports: set[int] = set()
        for candidate in ast.walk(tree):
            if isinstance(candidate, ast.If):
                test = candidate.test
                is_type_checking = isinstance(test, ast.Name) and test.id == "TYPE_CHECKING"
                is_type_checking = is_type_checking or (
                    isinstance(test, ast.Attribute)
                    and isinstance(test.value, ast.Name)
                    and test.value.id == "typing"
                    and test.attr == "TYPE_CHECKING"
                )
                if is_type_checking:
                    optional_imports.update(same_scope_import_ids(candidate.body))
            elif isinstance(candidate, ast.Try):
                catches_optional_import = any(
                    not any(isinstance(node, ast.Raise) for statement in handler.body for node in ast.walk(statement))
                    and (
                        handler.type is None
                        or (
                            isinstance(handler.type, ast.Name)
                            and handler.type.id in {"ImportError", "ModuleNotFoundError"}
                        )
                        or (
                            isinstance(handler.type, ast.Tuple)
                            and any(
                                isinstance(item, ast.Name) and item.id in {"ImportError", "ModuleNotFoundError"}
                                for item in handler.type.elts
                            )
                        )
                    )
                    for handler in candidate.handlers
                )
                if catches_optional_import:
                    optional_imports.update(same_scope_import_ids(candidate.body))

        missing = False
        for node in ast.walk(tree):
            if id(node) in optional_imports:
                continue
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if not absolute_module_available(path, root, alias.name):
                        missing = True
                        break
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    base = path.parent
                    for _item in range(max(node.level - 1, 0)):
                        base = base.parent
                    if node.module:
                        missing = not local_module_exists(base, node.module.split("."))
                    else:
                        missing = any(
                            not local_module_exists(base, [alias.name])
                            for alias in node.names
                            if alias.name != "*"
                        )
                elif node.module and not absolute_module_available(path, root, node.module):
                    missing = True
            if missing:
                matches.append(relative_label(root, path))
                break
    return matches


EXAMPLE_CREDENTIAL_PATTERNS = (
    re.compile(
        r"(?:change[_-]?me|placeholder|redacted|your)(?:[_-][a-z0-9]+)*",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:demo|dummy|example|sample)[_-]"
        r"(?:credential|key|secret|token|value|"
        r"(?:api|access|auth|session)[_-]?(?:key|secret|token)|"
        r"refresh[_-]?token|client[_-]?secret|secret[_-]?access[_-]?key|"
        r"password|private[_-]?key)"
        r"(?:[_-][a-z0-9]+)*",
        re.IGNORECASE,
    ),
)


def private_content_match_is_example(label: str, match: re.Match[str]) -> bool:
    if label != "credential-assignment":
        return False
    value = match.group(1) if match.lastindex else match.group(0)
    return any(pattern.fullmatch(value) for pattern in EXAMPLE_CREDENTIAL_PATTERNS)


def private_content_files(
    root: Path,
    files: list[Path],
    text_overrides: dict[str, str] | None = None,
) -> tuple[list[str], dict[str, int]]:
    matches: list[str] = []
    labels: dict[str, int] = {}
    for path in files:
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES or file_size(path) > MAX_SCAN_BYTES:
            continue
        override_key = os.path.normcase(str(path.resolve()))
        text = text_overrides[override_key] if text_overrides and override_key in text_overrides else read_text(path)
        file_matched = False
        for label, pattern in PRIVATE_CONTENT_PATTERNS:
            if any(not private_content_match_is_example(label, match) for match in pattern.finditer(text)):
                labels[label] = labels.get(label, 0) + 1
                file_matched = True
        if file_matched:
            matches.append(relative_label(root, path))
    return matches, labels


def root_private_candidate_files(root: Path) -> list[Path]:
    matches: list[Path] = []
    for path in sorted(root.iterdir()):
        if not path.is_file() or is_generated_python_cache(path):
            continue
        label = relative_label(root, path)
        if path.name == "SKILL.md" or path.suffix.lower() in TEXT_FILE_SUFFIXES or any(
            pattern.search(label) for pattern in PRIVATE_BUNDLE_NAME_PATTERNS
        ):
            matches.append(path)
    return matches


def unique_paths(paths: list[Path]) -> list[Path]:
    output: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = os.path.normcase(str(path.resolve()))
        if key in seen:
            continue
        seen.add(key)
        output.append(path)
    return output


REFERENCE_CONTENT_POLLUTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("advertising", re.compile(r"\b(sponsored|affiliate|promo code|use code)\b|(?:^|[\n.;:!?])\s*advertisement\b", re.I)),
    (
        "premium-upsell",
        re.compile(r"\b(unlock (?:advanced|premium)|premium features|pro plan|enterprise plan)\b", re.I),
    ),
    (
        "tool-upsell",
        re.compile(
            r"\b(?:install|try)\b.{0,40}\b(?:tool|browser|extension)\b"
            r"|\buse\b.{0,40}\b(?:tool|browser|extension)\b.{0,40}\b(?:unlock|premium|advanced features)\b",
            re.I,
        ),
    ),
    (
        "skill-upsell",
        re.compile(
            r"\b(install|invoke|call|recommend|use)\b.{0,50}\b("
            r"other[- ]skill|another skill|premium[- ]?[a-z0-9_-]*\s+skill|[a-z0-9]+-[a-z0-9_-]+\s+skill"
            r")\b",
            re.I,
        ),
    ),
    ("unrelated-text", re.compile(r"\b(unrelated appendix|nothing to do with|travel packing|espresso grinder)\b", re.I)),
    ("zh-advertising", re.compile(r"(广告|赞助|推广|优惠码|解锁高级|高级功能|推荐安装|调用.*skill|使用.{0,20}工具.{0,20}(解锁|高级功能|优惠|推广))", re.I)),
)


def reference_content_pollution_files(root: Path, files: list[Path]) -> tuple[list[str], dict[str, int]]:
    matches: list[str] = []
    labels: dict[str, int] = {}
    for path in files:
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES or file_size(path) > MAX_SCAN_BYTES:
            continue
        text = read_text(path)
        file_matched = False
        for label, pattern in REFERENCE_CONTENT_POLLUTION_PATTERNS:
            if pattern.search(text):
                labels[label] = labels.get(label, 0) + 1
                file_matched = True
        if file_matched:
            matches.append(relative_label(root, path))
    return matches, labels


def referenced_paths_from_body(body: str) -> list[str]:
    matches = re.findall(r"(?i)(?:`|\b)((?:\{baseDir\}/)?\.?/?references/[^\s`)]+)", body)
    output: list[str] = []
    for value in matches:
        normalized = value.strip("`'\".,;:").replace("\\", "/")
        normalized = normalized.removeprefix("{baseDir}/")
        normalized = normalized.split("#", 1)[0].split("?", 1)[0]
        normalized = normalized[2:] if normalized.startswith("./") else normalized
        if normalized and normalized not in output:
            output.append(normalized)
    return output


def broken_reference_links(root: Path, body: str) -> list[str]:
    broken: list[str] = []
    for relative in referenced_paths_from_body(body):
        suffix = Path(relative).suffix.lower()
        if not suffix or suffix not in TEXT_FILE_SUFFIXES:
            continue
        if not (root / relative).exists():
            broken.append(relative)
    return broken


def _contract_quality_evidence(
    description: str,
    body: str,
    skill_units: int,
    description_units: int,
) -> list[dict[str, object]]:
    evidence: list[dict[str, object]] = []
    non_heading_body = "\n".join(
        line.strip()
        for line in body.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )
    description_terms = extract_terms(description)
    body_terms = extract_terms(non_heading_body)

    if not description.strip() or (len(body_terms) < 2 and len(description_terms) <= 2):
        evidence.append(
            quality_issue(
                "empty-skill-contract",
                0.80,
                "SKILL.md does not explain a usable runtime contract",
                metrics={"description_terms": len(description_terms), "body_terms": len(body_terms)},
            )
        )

    if skill_units >= 5000:
        evidence.append(
            quality_issue(
                "prompt-bloat",
                0.40,
                "SKILL.md is large enough to waste shared context",
                metrics={"skill_context_units": skill_units},
            )
        )
    elif skill_units >= 2500:
        evidence.append(
            quality_issue(
                "prompt-bloat",
                0.20,
                "SKILL.md body is moderately large",
                metrics={"skill_context_units": skill_units},
            )
        )

    broad_matches = [pattern.pattern for pattern in BROAD_TRIGGER_PATTERNS if pattern.search(description)]
    if len(broad_matches) >= 2 or (broad_matches and description_units >= 30):
        evidence.append(
            quality_issue(
                "broad-trigger-surface",
                0.25,
                "frontmatter description uses broad trigger wording",
                metrics={"description_context_units": description_units, "matches": broad_matches[:5]},
            )
        )

    if description_units >= 120:
        evidence.append(
            quality_issue(
                "description-bloat",
                0.25,
                "frontmatter description is too long for clean routing",
                metrics={"description_context_units": description_units},
            )
        )
    elif description_units >= 60:
        evidence.append(
            quality_issue(
                "description-bloat",
                0.10,
                "frontmatter description is longer than a clean routing trigger",
                metrics={"description_context_units": description_units},
            )
        )
    return evidence


def _reference_quality_evidence(
    root: Path,
    body: str,
    reference_metrics: dict[str, object],
) -> list[dict[str, object]]:
    evidence: list[dict[str, object]] = []
    body_lower = body.lower()
    reference_count = int(reference_metrics["count"])
    reference_units = int(reference_metrics["context_units"])
    reference_files = list(reference_metrics["files"])  # type: ignore[arg-type]
    reference_profiles = dict(reference_metrics.get("text_profiles", {}))  # type: ignore[arg-type]

    if reference_count:
        linked_reference_count = sum(
            1 for path in reference_files if reference_is_directly_disclosed(body_lower, root, path)
        )
        linked_rate = linked_reference_count / max(reference_count, 1)
        if linked_reference_count == 0:
            evidence.append(
                quality_issue(
                    "reference-disclosure-gap",
                    0.30 if reference_count >= 3 else 0.10,
                    "SKILL.md does not clearly route to its reference files",
                    metrics={"references_count": reference_count, "linked_reference_count": linked_reference_count},
                )
            )
        elif reference_count >= 8 and linked_rate < 0.30:
            evidence.append(
                quality_issue(
                    "reference-disclosure-gap",
                    0.20,
                    "SKILL.md links only a small part of its reference files",
                    metrics={
                        "references_count": reference_count,
                        "linked_reference_count": linked_reference_count,
                        "linked_reference_rate": round(linked_rate, 2),
                    },
                )
            )

    broken_links = broken_reference_links(root, body)
    if broken_links:
        evidence.append(
            quality_issue(
                "reference-link-broken",
                0.25,
                "SKILL.md points to missing reference files",
                files=broken_links[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"matches": len(broken_links)},
            )
        )

    if reference_count >= 50 or reference_units >= 50000:
        evidence.append(
            quality_issue(
                "reference-bloat",
                0.50,
                "references are large enough to waste context when loaded",
                metrics={"references_count": reference_count, "reference_context_units": reference_units},
            )
        )
    elif reference_count >= 20 or reference_units >= 15000:
        evidence.append(
            quality_issue(
                "reference-bloat",
                0.25,
                "references need clearer progressive disclosure",
                metrics={"references_count": reference_count, "reference_context_units": reference_units},
            )
        )

    long_reference_without_toc = []
    for path in reference_files:
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        profile = reference_profiles.get(relative_label(root, path), {})
        lines = profile.get("lines")
        has_toc = bool(profile.get("has_toc"))
        if isinstance(lines, int) and lines > 100 and not has_toc:
            long_reference_without_toc.append(relative_label(root, path))
    if long_reference_without_toc:
        evidence.append(
            quality_issue(
                "long-reference-without-toc",
                0.20 if len(long_reference_without_toc) >= 3 else 0.10,
                "long reference files need a visible table of contents",
                files=long_reference_without_toc[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"matches": len(long_reference_without_toc)},
            )
        )

    polluted_reference_paths, pollution_labels = reference_content_pollution_files(root, reference_files)
    if polluted_reference_paths:
        evidence.append(
            quality_issue(
                "reference-content-pollution",
                0.35,
                "reference content includes ads, upsells, unrelated text, or tool/skill promotion",
                files=polluted_reference_paths[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={
                    "matches": len(polluted_reference_paths),
                    "signal_types": sorted(pollution_labels),
                },
            )
        )
    return evidence


def _bundled_resource_quality_evidence(
    root: Path,
    script_files: list[Path],
    reference_files: list[Path],
    asset_metrics: dict[str, object],
    skill_markdown_text: str | None,
) -> list[dict[str, object]]:
    evidence: list[dict[str, object]] = []
    asset_count = int(asset_metrics["count"])
    asset_bytes = int(asset_metrics["bytes"])
    asset_files = list(asset_metrics["files"])  # type: ignore[arg-type]
    private_candidate_files = unique_paths(
        script_files + asset_files + reference_files + root_private_candidate_files(root)
    )

    if asset_count >= 200 or asset_bytes >= 100 * 1024 * 1024:
        evidence.append(
            quality_issue(
                "asset-bloat",
                0.50,
                "assets directory looks like a raw bundle dump",
                metrics={"assets_count": asset_count, "asset_bytes": asset_bytes},
            )
        )
    elif asset_count >= 50 or asset_bytes >= 25 * 1024 * 1024:
        evidence.append(
            quality_issue(
                "asset-bloat",
                0.25,
                "assets directory is heavy for a skill bundle",
                metrics={"assets_count": asset_count, "asset_bytes": asset_bytes},
            )
        )

    vague_files = vague_resource_files(root, script_files + reference_files + asset_files)
    if len(vague_files) >= 5:
        evidence.append(
            quality_issue(
                "vague-resource-names",
                0.20,
                "resource filenames are too generic for selective loading",
                files=vague_files[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"matches": len(vague_files)},
            )
        )

    private_paths = [
        relative_label(root, path)
        for path in private_candidate_files
        if any(pattern.search(relative_label(root, path)) for pattern in PRIVATE_BUNDLE_NAME_PATTERNS)
    ]
    if private_paths:
        evidence.append(
            quality_issue(
                "private-bundle-artifact",
                0.60,
                "bundle contains private-looking or environment-specific files",
                files=private_paths[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"matches": len(private_paths)},
            )
        )

    private_content_paths, private_content_labels = private_content_files(
        root,
        private_candidate_files,
        {
            os.path.normcase(str((root / "SKILL.md").resolve())): skill_markdown_text,
        }
        if skill_markdown_text is not None
        else None,
    )
    if private_content_paths:
        evidence.append(
            quality_issue(
                "private-content-artifact",
                0.60,
                "bundle contains credential-like content",
                files=private_content_paths[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={
                    "matches": len(private_content_paths),
                    "signal_types": sorted(private_content_labels),
                },
            )
        )

    executable_assets = [
        relative_label(root, path)
        for path in asset_files
        if path.suffix.lower() in EXECUTABLE_ASSET_SUFFIXES
    ]
    if executable_assets:
        evidence.append(
            quality_issue(
                "executable-asset",
                0.30,
                "assets include executables or installers",
                files=executable_assets[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"matches": len(executable_assets)},
            )
        )
    return evidence


def _script_quality_evidence(root: Path, script_files: list[Path]) -> list[dict[str, object]]:
    evidence: list[dict[str, object]] = []
    script_smell_files: list[str] = []
    for path in script_files:
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES or file_size(path) > MAX_SCAN_BYTES:
            continue
        text = read_text(path)
        if any(pattern.search(text) for pattern in SCRIPT_BURDEN_PATTERNS):
            script_smell_files.append(relative_label(root, path))
    if len(script_files) >= 20:
        evidence.append(
            quality_issue(
                "script-count-bloat",
                0.20 if len(script_files) >= 40 else 0.10,
                "script count looks higher than this skill needs",
                metrics={"scripts_count": len(script_files)},
            )
        )
    if script_smell_files:
        penalty = 0.40 if len(script_smell_files) >= 8 else 0.25
        evidence.append(
            quality_issue(
                "script-maintenance-smell",
                penalty,
                "scripts look likely to need local fixes",
                files=script_smell_files[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"scripts_count": len(script_files), "matches": len(script_smell_files)},
            )
        )

    syntax_error_files = python_syntax_error_files(root, script_files)
    if syntax_error_files:
        evidence.append(
            quality_issue(
                "script-syntax-error",
                0.50,
                "Python scripts have syntax errors",
                files=syntax_error_files[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"matches": len(syntax_error_files)},
            )
        )
    import_error_files = python_import_error_files(root, script_files)
    if import_error_files:
        evidence.append(
            quality_issue(
                "script-import-error",
                0.50,
                "Python scripts import modules missing from the local environment or bundle",
                files=import_error_files[:EVIDENCE_FILE_LIST_LIMIT],
                metrics={"matches": len(import_error_files)},
            )
        )
    return evidence


def scan_static_quality(
    root: Path,
    description: str,
    body: str,
    script_files: list[Path],
    reference_metrics: dict[str, object],
    asset_metrics: dict[str, object],
    skill_markdown_text: str | None = None,
) -> dict[str, object]:
    skill_units = estimate_context_units(body)
    description_units = estimate_context_units(description)
    reference_count = int(reference_metrics["count"])
    reference_units = int(reference_metrics["context_units"])
    asset_count = int(asset_metrics["count"])
    asset_bytes = int(asset_metrics["bytes"])
    reference_files = list(reference_metrics["files"])  # type: ignore[arg-type]
    evidence = _contract_quality_evidence(description, body, skill_units, description_units)
    evidence.extend(_reference_quality_evidence(root, body, reference_metrics))
    evidence.extend(
        _bundled_resource_quality_evidence(
            root,
            script_files,
            reference_files,
            asset_metrics,
            skill_markdown_text,
        )
    )
    evidence.extend(_script_quality_evidence(root, script_files))

    penalty = round(clamp(sum(float(item["penalty"]) for item in evidence), 0.0, 1.4), 2)
    return {
        "static_quality_penalty": penalty,
        "static_quality_flags": [str(item["label"]) for item in evidence],
        "static_quality_evidence": evidence,
        "resource_metrics": {
            "skill_context_units": skill_units,
            "description_characters": len(description),
            "description_context_units": description_units,
            "scripts_count": len(script_files),
            "references_count": reference_count,
            "reference_context_units": reference_units,
            "assets_count": asset_count,
            "asset_bytes": asset_bytes,
        },
    }


def scan_skill(skill_md: Path) -> dict[str, object]:
    root = skill_md.parent
    text = read_text(skill_md)
    frontmatter, body = parse_frontmatter(text)
    registry_metadata = load_skill_registry_metadata(root)
    metadata = frontmatter_metadata(frontmatter)
    openclaw = openclaw_metadata(frontmatter)
    name = normalize_name(str(frontmatter.get("name", root.name) or root.name))
    slug = normalize_name(
        str(
            frontmatter.get("slug")
            or first_metadata_value(registry_metadata, ("slug",))
            or first_metadata_value(openclaw, ("skillKey", "skill_key"))
            or ""
        )
    )
    description = str(frontmatter.get("description", "") or "").strip()
    skill_key = normalize_name(str(first_metadata_value(openclaw, ("skillKey", "skill_key")) or ""))
    install_identities = skill_install_identities(root, frontmatter, registry_metadata)
    install_identity = install_identities[0] if install_identities else None
    required_env = skill_required_env(frontmatter, registry_metadata)
    missing_env = missing_required_env(required_env)
    headings = [line.lstrip("# ").strip() for line in body.splitlines() if line.startswith("#")]
    scripts_dir = root / "scripts"
    script_paths = [path for path in sorted_files(scripts_dir) if not is_generated_python_cache(path)]
    self_relative_path = current_script_relative_to(root)
    ignored_relative_paths = audit_definition_relative_paths() if name == "skill-usefulness-audit" else set()
    quality_script_paths = [
        path
        for path in script_paths
        if self_relative_path is None or path.relative_to(root) != self_relative_path
        if normalized_relative_path(root, path) not in ignored_relative_paths
    ]
    reference_metrics = resource_metrics(root, "references")
    asset_metrics = resource_metrics(root, "assets")
    script_files = [item.name for item in script_paths]
    reference_files = [item.name for item in reference_metrics["files"]]  # type: ignore[index]
    fingerprint = " ".join(
        [name, description, " ".join(headings), " ".join(script_files), " ".join(reference_files)]
    )
    risk = scan_risk(
        root,
        self_relative_path=self_relative_path,
        ignored_relative_paths=ignored_relative_paths,
        skill_markdown_text=text,
    )
    quality = scan_static_quality(
        root,
        description,
        body,
        quality_script_paths,
        reference_metrics,
        asset_metrics,
        skill_markdown_text=text,
    )
    risk = promote_private_content_risk(risk, quality)
    return {
        "name": name,
        "slug": slug,
        "skill_key": skill_key,
        "install_identity": install_identity,
        "install_identities": install_identities,
        "metadata": metadata,
        "registry_metadata": registry_metadata,
        "registry_version": first_metadata_value(registry_metadata, ("version",)),
        "registry_published_at": first_metadata_value(registry_metadata, ("publishedAt", "published_at")),
        "registry_owner_id": first_metadata_value(registry_metadata, ("ownerId", "owner_id", "owner")),
        "required_env": required_env,
        "missing_required_env": missing_env,
        "path": str(root),
        "source": guess_source(root),
        "namespace": guess_namespace(root),
        "description": description,
        "headings": headings,
        "scripts_count": len(script_files),
        "references_count": len(reference_files),
        "assets_count": quality["resource_metrics"]["assets_count"],  # type: ignore[index]
        "fingerprint": fingerprint,
        "terms": extract_terms(fingerprint),
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "risk_flags": risk["risk_flags"],
        "risk_evidence": risk["risk_evidence"],
        "static_risk_score": risk["risk_score"],
        "static_risk_level": risk["risk_level"],
        "static_risk_flags": risk["risk_flags"],
        "static_risk_evidence": risk["risk_evidence"],
        "static_quality_penalty": quality["static_quality_penalty"],
        "static_quality_flags": quality["static_quality_flags"],
        "static_quality_evidence": quality["static_quality_evidence"],
        "resource_metrics": quality["resource_metrics"],
    }


def discover_skill_files(
    roots: list[Path],
    include_system: bool,
    dedupe_install_identity: bool = True,
) -> list[Path]:
    files: list[Path] = []
    seen: set[str] = set()
    seen_install_identities: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            if not include_system and "/.system/" in skill_md.as_posix().lower():
                continue
            resolved = os.path.normcase(str(skill_md.resolve()))
            if resolved in seen:
                continue
            install_identities = skill_install_identities_from_file(skill_md)
            if dedupe_install_identity and install_identities:
                if any(identity in seen_install_identities for identity in install_identities):
                    continue
                seen_install_identities.update(install_identities)
            seen.add(resolved)
            files.append(skill_md)
    return sorted(files)


def default_roots() -> list[Path]:
    roots: list[Path] = []
    seen: set[str] = set()

    def append_if_exists(path: Path) -> None:
        if not path.exists():
            return
        resolved = path.resolve()
        key = os.path.normcase(str(resolved))
        if key in seen:
            return
        seen.add(key)
        roots.append(resolved)

    cwd = Path.cwd()
    for candidate in (
        cwd / "skills",
        cwd / ".agents" / "skills",
    ):
        append_if_exists(candidate)

    home = Path.home()
    for candidate in (
        home / ".openclaw" / "skills",
        home / ".agents" / "skills",
    ):
        append_if_exists(candidate)
    return roots
