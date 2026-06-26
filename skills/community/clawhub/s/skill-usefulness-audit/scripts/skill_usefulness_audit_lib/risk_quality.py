from __future__ import annotations

from .common import *

def is_generated_python_cache(path: Path) -> bool:
    return "__pycache__" in {part.lower() for part in path.parts} or path.suffix.lower() in {".pyc", ".pyo"}


def normalized_relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def audit_definition_relative_paths() -> set[str]:
    base = Path("scripts") / "skill_usefulness_audit_lib"
    return {
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
                if alias.name in {"run", "Popen", "call", "check_call", "check_output"}:
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
            if func.value.id in subprocess_aliases and func.attr in {"run", "Popen", "call", "check_call", "check_output"}:
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


def scan_risk(
    root: Path,
    self_relative_path: Path | None = None,
    ignored_relative_paths: set[str] | None = None,
) -> dict[str, object]:
    hits: dict[str, dict[str, object]] = {}
    ignored_paths = set(ignored_relative_paths or set())
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
            continue
        if path.name == "SKILL.md":
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
        text_lower = text.lower()
        for rule in COMPILED_RISK_RULES:
            label = str(rule["label"])
            if path.suffix.lower() == ".py" and label == "shell-exec":
                continue
            if any(pattern.search(text_lower) for pattern in rule["patterns"]):
                add_risk_hit(hits, label, float(rule["severity"]), relative)
        if path.suffix.lower() == ".py":
            for label in python_exec_call_labels(text):
                severity = 2.0 if label == "dynamic-exec" else 1.0
                add_risk_hit(hits, label, severity, relative)
        for label in install_surface_labels(path, relative, text):
            severity = 2.0 if label == "install-hook" else 1.0
            add_risk_hit(hits, label, severity, relative)

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


def reference_is_directly_disclosed(body_lower: str, root: Path, path: Path) -> bool:
    relative = relative_label(root, path).lower()
    filename = path.name.lower()
    stem = path.stem.lower()
    if relative in body_lower or filename in body_lower:
        return True
    if len(stem) < 5:
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


def private_content_files(root: Path, files: list[Path]) -> tuple[list[str], dict[str, int]]:
    matches: list[str] = []
    labels: dict[str, int] = {}
    for path in files:
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES or file_size(path) > MAX_SCAN_BYTES:
            continue
        text = read_text(path)
        file_matched = False
        for label, pattern in PRIVATE_CONTENT_PATTERNS:
            if pattern.search(text):
                labels[label] = labels.get(label, 0) + 1
                file_matched = True
        if file_matched:
            matches.append(relative_label(root, path))
    return matches, labels


def scan_static_quality(
    root: Path,
    description: str,
    body: str,
    script_files: list[Path],
    reference_metrics: dict[str, object],
    asset_metrics: dict[str, object],
) -> dict[str, object]:
    evidence: list[dict[str, object]] = []
    skill_units = estimate_context_units(body)
    description_units = estimate_context_units(description)
    reference_count = int(reference_metrics["count"])
    reference_units = int(reference_metrics["context_units"])
    asset_count = int(asset_metrics["count"])
    asset_bytes = int(asset_metrics["bytes"])
    body_lower = body.lower()
    reference_files = list(reference_metrics["files"])  # type: ignore[arg-type]
    reference_profiles = dict(reference_metrics.get("text_profiles", {}))  # type: ignore[arg-type]
    asset_files = list(asset_metrics["files"])  # type: ignore[arg-type]

    if skill_units >= 5000:
        evidence.append(
            quality_issue(
                "prompt-bloat",
                0.40,
                "SKILL.md body is large enough to pressure the shared context budget",
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
                "frontmatter description uses broad trigger language",
                metrics={"description_context_units": description_units, "matches": broad_matches[:5]},
            )
        )

    if description_units >= 120:
        evidence.append(
            quality_issue(
                "description-bloat",
                0.25,
                "frontmatter description is too long for a routing trigger",
                metrics={"description_context_units": description_units},
            )
        )
    elif description_units >= 60:
        evidence.append(
            quality_issue(
                "description-bloat",
                0.10,
                "frontmatter description is longer than a concise routing trigger",
                metrics={"description_context_units": description_units},
            )
        )

    if reference_count >= 3:
        linked_reference_count = sum(
            1 for path in reference_files if reference_is_directly_disclosed(body_lower, root, path)
        )
        linked_rate = linked_reference_count / max(reference_count, 1)
        if linked_reference_count == 0:
            evidence.append(
                quality_issue(
                    "reference-disclosure-gap",
                    0.30,
                    "reference files are not directly discoverable from SKILL.md",
                    metrics={"references_count": reference_count, "linked_reference_count": linked_reference_count},
                )
            )
        elif reference_count >= 8 and linked_rate < 0.30:
            evidence.append(
                quality_issue(
                    "reference-disclosure-gap",
                    0.20,
                    "few reference files are directly linked from SKILL.md",
                    metrics={
                        "references_count": reference_count,
                        "linked_reference_count": linked_reference_count,
                        "linked_reference_rate": round(linked_rate, 2),
                    },
                )
            )

    if reference_count >= 50 or reference_units >= 50000:
        evidence.append(
            quality_issue(
                "reference-bloat",
                0.50,
                "references are large enough to encourage over-loading context",
                metrics={"references_count": reference_count, "reference_context_units": reference_units},
            )
        )
    elif reference_count >= 20 or reference_units >= 15000:
        evidence.append(
            quality_issue(
                "reference-bloat",
                0.25,
                "references need review for progressive disclosure",
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
                "long reference files are missing a visible table of contents",
                files=long_reference_without_toc[:8],
                metrics={"matches": len(long_reference_without_toc)},
            )
        )

    if asset_count >= 200 or asset_bytes >= 100 * 1024 * 1024:
        evidence.append(
            quality_issue(
                "asset-bloat",
                0.50,
                "assets directory is large enough to look like a bundle dump",
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
                "resource filenames are too generic for reliable selective loading",
                files=vague_files[:8],
                metrics={"matches": len(vague_files)},
            )
        )

    private_paths = [
        relative_label(root, path)
        for path in asset_files + reference_files
        if any(pattern.search(relative_label(root, path)) for pattern in PRIVATE_BUNDLE_NAME_PATTERNS)
    ]
    if private_paths:
        evidence.append(
            quality_issue(
                "private-bundle-artifact",
                0.60,
                "bundle contains files that look private or environment-specific",
                files=private_paths[:8],
                metrics={"matches": len(private_paths)},
            )
        )

    private_content_paths, private_content_labels = private_content_files(
        root,
        script_files + asset_files + reference_files,
    )
    if private_content_paths:
        evidence.append(
            quality_issue(
                "private-content-artifact",
                0.60,
                "bundle contains content that looks like private credentials or keys",
                files=private_content_paths[:8],
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
                "assets contain executable binaries or installers",
                files=executable_assets[:8],
                metrics={"matches": len(executable_assets)},
            )
        )

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
                "large script count should be reviewed for over-bundling",
                metrics={"scripts_count": len(script_files)},
            )
        )
    if script_smell_files:
        penalty = 0.40 if len(script_smell_files) >= 8 else 0.25
        evidence.append(
            quality_issue(
                "script-maintenance-smell",
                penalty,
                "scripts look likely to require agent repair or local adjustment",
                files=script_smell_files[:8],
                metrics={"scripts_count": len(script_files), "matches": len(script_smell_files)},
            )
        )

    syntax_error_files = python_syntax_error_files(root, script_files)
    if syntax_error_files:
        evidence.append(
            quality_issue(
                "script-syntax-error",
                0.50,
                "Python scripts contain syntax errors",
                files=syntax_error_files[:8],
                metrics={"matches": len(syntax_error_files)},
            )
        )

    penalty = round(clamp(sum(float(item["penalty"]) for item in evidence), 0.0, 1.4), 2)
    return {
        "static_quality_penalty": penalty,
        "static_quality_flags": [str(item["label"]) for item in evidence],
        "static_quality_evidence": evidence,
        "resource_metrics": {
            "skill_context_units": skill_units,
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
    risk = scan_risk(root, self_relative_path=self_relative_path, ignored_relative_paths=ignored_relative_paths)
    quality = scan_static_quality(root, description, body, quality_script_paths, reference_metrics, asset_metrics)
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


def discover_skill_files(roots: list[Path], include_system: bool) -> list[Path]:
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
            if install_identities:
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
