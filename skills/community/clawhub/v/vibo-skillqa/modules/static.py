"""Static scan module: structure, frontmatter, referenced paths, sizes."""

import re
from pathlib import Path

try:
    import yaml  # PyYAML (optional; a minimal fallback parser is included)
except Exception:  # pragma: no cover
    yaml = None

MAGIC_PATH_RE = re.compile(r"(?:/home/|/root/|/etc/(?!hosts)|/Users/|C:\\)")
# Files created at runtime (license, usage log) — legitimately absent from
# a fresh package; references to them are not broken paths.
RUNTIME_GENERATED = {
    "vibo_license.dat", "vibo_usage.json", "vibo_usage.jsonl",
    "web_cache.json", "guardian_config.json", "hermes_memory.web",
    "_quick_index.json", "extra_model_paths.yaml", "KNOWN_ISSUES.md",
    "KNOWN_ISSUES", "package-lock.json", "pyproject.toml", "requirements.txt",
    ".env", "config.json", "config.yaml", "templates/_quick_index.json",
    "tsconfig.json", "package.json", ".comfyui-agent.json",
    "PERF.md", "CHANGELOG.md", "TASKS.md", "TODO.md", "NOTES.md", "HINTS.md",
    "o.png", "out.png", "result.png", "output.png",
}

# code identifiers / DOM APIs that look like files but are not:
# console.log, db.config, process.stdout, document.body...
NON_PATH_IDENTIFIERS = {
    "console.log", "console.error", "console.warn", "console.info",
    "process.stdout", "process.stderr", "db.config", "document.body",
    "document.title", "window.location", "stdout", "stderr",
    "sideeffects", "side-effects", "perf.mark", "performance.now",
}
TILDE_RE = re.compile(r"~\/")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
VERSION_MENTION_RE = re.compile(r"\b\d+\.\d+\.\d+\b")
BACKTICK_RE = re.compile(r"`([^`]+)`")
PATH_TOKEN_RE = re.compile(
    r"[\w./-]+\.(?:json|yaml|yml|py|sh|js|md|toml|txt|cfg|conf|ini|dat|csv|"
    r"png|jpe?g|gif|svg|html|sql|log)"
)
KNOWN_EXTS = {".py", ".sh", ".js", ".json", ".yaml", ".yml", ".md", ".toml",
              ".txt", ".cfg", ".conf", ".ini", ".dat", ".csv", ".png", ".jpg",
              ".jpeg", ".gif", ".svg", ".html", ".sql", ".log"}
MIN_SKILLMD_BYTES = 200
MAX_ROOT_BINARY = 1024 * 1024
MAX_FILE_SIZE = 5 * 1024 * 1024


def _check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _module_status(checks):
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "warn" for c in checks):
        return "warn"
    return "pass"


def _parse_frontmatter(text):
    """Return frontmatter dict, or None if the block is missing.

    On parse errors a dict with a "_error" key is returned.
    """
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    block = "\n".join(lines[1:end])
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
            if isinstance(data, dict):
                return data
            return {"_error": "frontmatter is not a mapping"}
        except Exception as e:
            return {"_error": str(e)}
    # Minimal fallback parser (no PyYAML installed).
    data = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip("\"'")
            if val.startswith("[") and val.endswith("]"):
                val = [x.strip().strip("\"'") for x in
                       val[1:-1].split(",") if x.strip()]
            data[key] = val
    return data


def _referenced_missing(md_text, skill_dir):
    """Find paths referenced in SKILL.md that do not exist. Returns (missing, checked)."""
    seen, missing = set(), []
    checked = 0
    candidates = []
    for m in BACKTICK_RE.finditer(md_text):
        for tok in m.group(1).split():
            # backtick tokens are only checked when they look like a file
            # reference (known extension); words like `yes/no` are not paths
            if Path(tok).suffix.lower() in KNOWN_EXTS:
                candidates.append((tok, True))  # from backticks (example/doc)
    for m in PATH_TOKEN_RE.finditer(md_text):
        candidates.append((m.group(0), False))
    missing_warn = []
    for tok, from_backtick in candidates:
        tok = tok.strip().rstrip(".,;:)]}>\"'`")
        if not tok or tok in seen:
            continue
        seen.add(tok)
        if tok.startswith(("/", "~", "$", "-")):
            continue  # absolute/tilde/var paths are handled elsewhere
        if "://" in tok or tok.startswith(("http://", "https://", "www.")):
            continue
        if "/" not in tok and Path(tok).suffix.lower() not in KNOWN_EXTS:
            continue  # plain words like "python3" are not file references
        # placeholder paths in examples (path/to/…, example.com/…) are correct
        # practice, not broken references
        low = tok.lower()
        if low.startswith(("path/to/", "example/", "sample/", "your-", "<",
                           "path/to", "examples/")):
            continue
        # code identifiers are NOT files: console.log, db.config, process.stdout
        if low in NON_PATH_IDENTIFIERS:
            continue
        # word continued by letters = part of a longer identifier, not a file
        # (db.conf from db.config.findFirst(), sideEffects from sideEffects:)
        rest = md_text[md_text.find(tok) + len(tok):] if tok in md_text else ""
        if rest[:1].isalnum() or rest[:1] == "_":
            continue
        # method call: console.log( → token followed by "(" is a function call
        if rest[:1] == "(":
            continue
        # dated artifacts (2026-06-21_zimage_hero.json) are generated output
        if re.match(r"\d{4}-\d{2}-\d{2}_.*\.", tok):
            continue
        # editor/tool configs (.claude/settings.json, .cursor/rules) are
        # per-user runtime files, not part of the package
        if low.startswith((".claude/", ".cursor/", ".vscode/", ".idea/")):
            continue
        p = Path(skill_dir) / tok
        checked += 1
        found = p.exists() or any(Path(skill_dir).rglob(tok))
        if not found:
            # files may live outside the skill subfolder but inside the repo
            parent = Path(skill_dir).parent
            for _ in range(4):
                if (parent / tok).exists() or any(parent.rglob(tok)):
                    found = True
                    break
                parent = parent.parent
        if not found:
            # runtime-generated files are legitimately absent from the package
            if tok in RUNTIME_GENERATED:
                continue
            (missing_warn if from_backtick else missing).append(tok)
    return missing, checked, missing_warn


def _empty_broken(skill_dir, md_path):
    empty, huge_bin = [], []
    for p in sorted(Path(skill_dir).rglob("*")):
        if not p.is_file():
            continue
        if p.resolve() == Path(md_path).resolve():
            continue
        try:
            size = p.stat().st_size
        except OSError:
            empty.append(str(p.relative_to(skill_dir)))
            continue
        if p.name == ".gitkeep":
            continue  # convention: empty file that keeps an empty dir in git
        if size == 0:
            empty.append(str(p.relative_to(skill_dir)))
            continue
        if p.parent == Path(skill_dir) and size > MAX_ROOT_BINARY:
            try:
                with open(p, "rb") as fh:
                    fh.read(64).decode("utf-8")
            except UnicodeDecodeError:
                huge_bin.append(str(p.relative_to(skill_dir)))
    return empty, huge_bin


def _big_files(skill_dir, limit):
    big = []
    for p in sorted(Path(skill_dir).rglob("*")):
        if p.is_file():
            try:
                if p.stat().st_size > limit:
                    big.append(str(p.relative_to(skill_dir)))
            except OSError:
                pass
    return big


def _find_magic(text):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in MAGIC_PATH_RE.finditer(line):
            out.append(f"{m.group(0)} (line {i})")
            if len(out) >= 5:
                return out
    return out


def _version_mentions(text, version):
    body = text
    if text.startswith("---"):
        lines = text.splitlines()
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body = "\n".join(lines[i + 1:])
                break
    out = []
    for m in VERSION_MENTION_RE.finditer(body):
        tok = m.group(0)
        if tok == version:
            continue
        # IPv4 addresses (127.0.0.1, 3.173.21.63) are not versions
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$", tok):
            continue
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}$", tok) \
                and re.search(rf"{re.escape(tok)}\.\d+", body):
            continue  # partial IPv4 (3.173.21 of 3.173.21.63)
        out.append(tok)
    return out


class StaticScan:
    name = "static"
    title = {"ru": "Статический анализ", "en": "Static scan"}

    def run(self, ctx):
        t = ctx.t
        skill = Path(ctx.skill_path)
        md = skill / "SKILL.md"
        checks = []
        md_text = None
        frontmatter = None

        # 1. SKILL.md exists / readable / not empty
        if not md.exists():
            checks.append(_check("skilmd_exists", "fail",
                                 t("check.skilmd_exists.missing")))
        else:
            try:
                md_text = md.read_text(encoding="utf-8", errors="replace")
                size = len(md_text.encode("utf-8"))
                if size <= MIN_SKILLMD_BYTES:
                    checks.append(_check("skilmd_exists", "fail",
                                         t("check.skilmd_exists.empty", size=size)))
                else:
                    checks.append(_check("skilmd_exists", "pass",
                                         t("check.skilmd_exists.ok", size=size)))
            except OSError as e:
                checks.append(_check("skilmd_exists", "fail",
                                     t("check.skilmd_exists.unreadable", err=e)))

        # 2. valid YAML frontmatter
        if md_text is not None:
            frontmatter = _parse_frontmatter(md_text)
            if frontmatter is None:
                checks.append(_check("frontmatter_valid", "fail",
                                     t("check.frontmatter_valid.missing")))
            elif frontmatter.get("_error"):
                checks.append(_check("frontmatter_valid", "fail",
                                     t("check.frontmatter_valid.fail",
                                       err=frontmatter["_error"])))
            else:
                checks.append(_check("frontmatter_valid", "pass",
                                     t("check.frontmatter_valid.ok")))
        else:
            checks.append(_check("frontmatter_valid", "fail",
                                 t("check.frontmatter_valid.missing")))

        # 3. required fields
        if isinstance(frontmatter, dict) and not frontmatter.get("_error"):
            required = ["name", "description"]
            missing = [f for f in required if not frontmatter.get(f)]
            if missing:
                checks.append(_check("frontmatter_fields", "fail",
                                     t("check.frontmatter_fields.fail",
                                       fields=", ".join(missing))))
            elif not frontmatter.get("version"):
                # version is NOT required by the base spec — recommended for
                # marketplaces (warn, not fail)
                checks.append(_check("frontmatter_fields", "warn",
                                     t("check.frontmatter_fields.warn_version")))
            else:
                has_tools = bool(frontmatter.get("tools")
                                 or frontmatter.get("allowed-tools"))
                if has_tools:
                    checks.append(_check("frontmatter_fields", "pass",
                                         t("check.frontmatter_fields.ok")))
                else:
                    checks.append(_check("frontmatter_fields", "warn",
                                         t("check.frontmatter_fields.warn")))
        else:
            checks.append(_check("frontmatter_fields", "fail",
                                 t("check.frontmatter_fields.nofm")))

        # 4. referenced paths exist
        internal = bool(isinstance(frontmatter, dict) and frontmatter.get("internal"))
        if md_text is not None:
            missing, checked, missing_warn = _referenced_missing(md_text, skill)
            if internal:
                # internal skills legitimately reference project files that
                # live outside the skill folder ($VIBO/...) — not a defect
                checks.append(_check("referenced_paths_exist", "pass",
                                     t("check.referenced_paths_exist.internal")))
            elif missing:
                checks.append(_check("referenced_paths_exist", "fail",
                                     t("check.referenced_paths_exist.fail",
                                       paths=", ".join(missing[:5]))))
            elif missing or missing_warn:
                checks.append(_check("referenced_paths_exist", "warn",
                                     t("check.referenced_paths_exist.warn",
                                       paths=", ".join((missing + missing_warn)[:5]))))
            else:
                checks.append(_check("referenced_paths_exist", "pass",
                                     t("check.referenced_paths_exist.ok",
                                       n=checked)))
        else:
            checks.append(_check("referenced_paths_exist", "warn",
                                 t("check.no_skilmd")))

        # 5. no empty / broken files
        empty, huge_bin = _empty_broken(skill, md)
        if empty:
            checks.append(_check("no_empty_broken_files", "fail",
                                 t("check.no_empty_broken_files.fail",
                                   files=", ".join(empty[:5]))))
        elif huge_bin:
            checks.append(_check("no_empty_broken_files", "warn",
                                 t("check.no_empty_broken_files.warn",
                                   files=", ".join(huge_bin[:5]))))
        else:
            checks.append(_check("no_empty_broken_files", "pass",
                                 t("check.no_empty_broken_files.ok")))

        # 6. no magic absolute paths
        if md_text is not None:
            magic = _find_magic(md_text)
            if magic and not internal:
                checks.append(_check("no_magic_paths", "fail",
                                     t("check.no_magic_paths.fail",
                                       paths=", ".join(magic[:5]))))
            elif magic or TILDE_RE.search(md_text):
                checks.append(_check("no_magic_paths", "warn",
                                     t("check.no_magic_paths.warn")))
            else:
                checks.append(_check("no_magic_paths", "pass",
                                     t("check.no_magic_paths.ok")))
        else:
            checks.append(_check("no_magic_paths", "warn", t("check.no_skilmd")))

        # 7. reasonable sizes
        big = _big_files(skill, MAX_FILE_SIZE)
        if big:
            checks.append(_check("reasonable_sizes", "warn",
                                 t("check.reasonable_sizes.warn",
                                   files=", ".join(big[:5]))))
        else:
            checks.append(_check("reasonable_sizes", "pass",
                                 t("check.reasonable_sizes.ok")))

        # 8. version consistency
        version = frontmatter.get("version") if isinstance(frontmatter, dict) else None
        if internal:
            checks.append(_check("version_consistent", "pass",
                                 t("check.version_consistent.internal")))
        elif version:
            if not SEMVER_RE.match(str(version)):
                checks.append(_check("version_consistent", "warn",
                                     t("check.version_consistent.notsemver",
                                       v=version)))
            else:
                mentions = _version_mentions(md_text or "", str(version))
                if mentions:
                    checks.append(_check("version_consistent", "warn",
                                         t("check.version_consistent.mentions",
                                           mentions=", ".join(mentions[:5]))))
                else:
                    checks.append(_check("version_consistent", "pass",
                                         t("check.version_consistent.ok",
                                           v=version)))
        else:
            checks.append(_check("version_consistent", "warn",
                                 t("check.version_consistent.noversion")))

        status = _module_status(checks)
        n_fail = sum(1 for c in checks if c["status"] == "fail")
        n_warn = sum(1 for c in checks if c["status"] == "warn")
        details = t("module.summary", total=len(checks), fail=n_fail, warn=n_warn)
        return {"module": self.name, "status": status, "checks": checks,
                "details": details}
