#!/usr/bin/env python3
"""Scan a code change for review cues, weakened tests and likely secrets.

Run it from the repository you are changing. It needs only Python 3.8+ and git.

Examples:
  python3 change_scan.py                  # tracked changes and untracked files versus HEAD
  python3 change_scan.py --staged         # staged changes only
  python3 change_scan.py --base main      # everything on this branch since it left main
  git diff | python3 change_scan.py --diff-file -
  python3 change_scan.py --json           # machine-readable output

The tier it prints (T0 to T3) is a suggested floor based on file paths and
changed lines. Check it against the change's actual impact: it is not a verdict
and not a release gate. Secret values are never printed: findings show the rule,
the location and a redacted preview.

Exit status:
  0  no blocking findings
  1  a likely secret was found (with --strict, also test-weakening signals or new suppressions)
  2  usage error, or git/file reading failed
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple

# Bound memory use when reading untracked files; larger files need separate review.
MAX_UNTRACKED_BYTES = 1_000_000

# Shannon entropy (bits per character) below which a value caught by a heuristic
# rule is treated as a word or placeholder rather than a credential. A value needs
# at least eight distinct characters to reach 3.0; random keys score well above it.
MIN_HEURISTIC_ENTROPY = 3.0

IGNORE_MARKERS = ("change-scan: ignore", "pragma: allowlist secret")

TIER_NAMES = {0: "T0", 1: "T1", 2: "T2", 3: "T3"}


@dataclass
class FileChange:
    path: str
    old_path: Optional[str] = None
    status: str = "modified"  # added, deleted, modified, renamed, binary
    added: List[Tuple[int, str]] = field(default_factory=list)
    removed: List[Tuple[int, str]] = field(default_factory=list)


@dataclass
class Finding:
    kind: str
    path: str
    line: Optional[int]
    detail: str

    def as_dict(self) -> dict:
        return {"kind": self.kind, "path": self.path, "line": self.line, "detail": self.detail}


# --------------------------------------------------------------------------- diff parsing

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
GIT_HEADER_RE = re.compile(r'^diff --git "?a/(.*?)"? "?b/(.*?)"?$')


def _clean_path(raw: str) -> str:
    path = raw.split("\t", 1)[0].strip()
    if path.startswith('"') and path.endswith('"') and len(path) >= 2:
        path = path[1:-1]
    if path.startswith(("a/", "b/")):
        path = path[2:]
    return path


def parse_unified_diff(text: str) -> List[FileChange]:
    """Parse git or plain unified diff text into per-file added and removed lines."""
    files: List[FileChange] = []
    current: Optional[FileChange] = None
    in_hunk = False
    old_ln = new_ln = old_rem = new_rem = 0

    for raw in text.splitlines():
        if in_hunk and current is not None:
            # Hunk line counts decide where the hunk ends, so content lines that
            # happen to start with "---" or "+++" are not mistaken for headers.
            if raw.startswith("\\"):
                continue  # "\ No newline at end of file"
            if raw.startswith("+"):
                current.added.append((new_ln, raw[1:]))
                new_ln += 1
                new_rem -= 1
            elif raw.startswith("-"):
                current.removed.append((old_ln, raw[1:]))
                old_ln += 1
                old_rem -= 1
            else:  # context line, possibly with its leading space stripped
                old_ln += 1
                new_ln += 1
                old_rem -= 1
                new_rem -= 1
            if old_rem <= 0 and new_rem <= 0:
                in_hunk = False
            continue

        if raw.startswith("diff --git "):
            current = FileChange(path="")
            files.append(current)
            match = GIT_HEADER_RE.match(raw)
            if match:
                current.old_path, current.path = match.group(1), match.group(2)
            continue
        if raw.startswith("--- ") and (current is None or current.added or current.removed):
            # A plain unified diff without "diff --git" headers starts a new file here.
            current = FileChange(path="")
            files.append(current)
        if current is None:
            continue
        if raw.startswith("new file mode"):
            current.status = "added"
        elif raw.startswith("deleted file mode"):
            current.status = "deleted"
        elif raw.startswith("rename from "):
            current.old_path = raw[len("rename from "):]
            current.status = "renamed"
        elif raw.startswith("rename to "):
            current.path = raw[len("rename to "):]
            current.status = "renamed"
        elif raw.startswith("Binary files "):
            if current.status == "modified":
                current.status = "binary"
        elif raw.startswith("--- "):
            target = raw[4:].strip()
            if target != "/dev/null":
                current.old_path = _clean_path(target)
                if not current.path:
                    current.path = current.old_path
        elif raw.startswith("+++ "):
            target = raw[4:].strip()
            if target == "/dev/null":
                current.status = "deleted"
                current.path = current.old_path or current.path
            else:
                current.path = _clean_path(target)
                if current.old_path is None:
                    current.status = "added"
        elif raw.startswith("@@"):
            match = HUNK_RE.match(raw)
            if match:
                old_ln = int(match.group(1))
                old_rem = int(match.group(2) if match.group(2) is not None else 1)
                new_ln = int(match.group(3))
                new_rem = int(match.group(4) if match.group(4) is not None else 1)
                in_hunk = old_rem > 0 or new_rem > 0
    return [f for f in files if f.path]


# --------------------------------------------------------------------------- git access

class GitError(RuntimeError):
    pass


def _git(repo: str, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", repo, *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise GitError("git is not installed or not on PATH") from exc
    if result.returncode != 0:
        raise GitError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


# Scan raw patches: explicit prefixes, no colour, external diffs or text conversions.
DIFF_FLAGS = ("--no-color", "--no-ext-diff", "--no-textconv", "--src-prefix=a/", "--dst-prefix=b/", "-M", "--unified=0")


def collect_changes(repo: str, staged: bool, base: Optional[str], untracked: bool) -> List[FileChange]:
    top = _git(repo, "rev-parse", "--show-toplevel").strip()
    has_head = True
    try:
        _git(top, "rev-parse", "--verify", "--quiet", "HEAD")
    except GitError:
        has_head = False

    if staged:
        text = _git(top, "diff", "--cached", *DIFF_FLAGS)
        untracked = False
    elif base:
        merge_base = _git(top, "merge-base", base, "HEAD").strip()
        text = _git(top, "diff", merge_base, *DIFF_FLAGS)
    elif has_head:
        text = _git(top, "diff", "HEAD", *DIFF_FLAGS)
    else:  # a repository without commits yet
        text = _git(top, "diff", "--cached", *DIFF_FLAGS) + "\n" + _git(top, "diff", *DIFF_FLAGS)

    changes = parse_unified_diff(text)
    if untracked:
        changes.extend(_untracked_files(top))
    return changes


def _untracked_files(top: str) -> Iterable[FileChange]:
    listing = _git(top, "ls-files", "--others", "--exclude-standard", "-z")
    for rel in filter(None, listing.split("\0")):
        full = os.path.join(top, rel)
        try:
            if os.path.getsize(full) > MAX_UNTRACKED_BYTES:
                continue
            with open(full, "rb") as handle:
                data = handle.read()
        except OSError as exc:
            raise GitError(f"cannot read untracked file {rel}: {exc}") from exc
        if b"\0" in data[:8192]:
            yield FileChange(path=rel, status="binary")
            continue
        lines = data.decode("utf-8", errors="replace").splitlines()
        yield FileChange(path=rel, status="added", added=[(i + 1, line) for i, line in enumerate(lines)])


# --------------------------------------------------------------------------- classification

DOC_EXTENSIONS = (".md", ".markdown", ".rst", ".adoc", ".asciidoc")
DOC_BASENAMES = {"license", "licence", "notice", "authors", "contributors", "changelog", "copying"}
DOC_DIRS = ("doc/", "docs/", "documentation/")
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
UI_EXTENSIONS = (".tsx", ".jsx", ".vue", ".svelte", ".html", ".htm", ".css", ".scss", ".cshtml", ".razor", ".xaml")
JS_EXTENSIONS = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts")
CODE_EXTENSIONS = JS_EXTENSIONS + (
    ".py", ".cs", ".fs", ".vb", ".java", ".kt", ".go", ".rb", ".php", ".rs", ".swift", ".scala",
    ".sql", ".sh", ".ps1", ".vue", ".svelte",
)
TEST_TOKENS = {"test", "tests", "spec", "specs", "e2e"}
PROMPT_TOKENS = {"prompt", "prompts"}
AGENT_INSTRUCTION_FILES = {"agents.md", "claude.md", "skill.md"}
AUTH_TOKENS = {
    "auth", "authn", "authz", "authentication", "authorization", "authorisation", "oauth", "oauth2",
    "oidc", "saml", "sso", "login", "logout", "signin", "signout", "signup", "session", "sessions",
    "permission", "permissions", "rbac", "acl", "acls", "crypto", "cryptography", "password",
    "passwords", "credential", "credentials", "secret", "secrets", "jwt", "mfa", "totp",
}
PAYMENT_TOKENS = {
    "payment", "payments", "billing", "invoice", "invoices", "checkout", "refund", "refunds",
    "ledger", "payout", "payouts", "stripe", "paypal",
}
MIGRATION_TOKENS = {"migration", "migrations", "alembic", "flyway", "liquibase"}

DEPENDENCY_BASENAMES = {
    "package.json", "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "bun.lockb", "bun.lock", "constraints.txt", "pyproject.toml", "poetry.lock", "uv.lock", "pipfile",
    "pipfile.lock", "setup.py", "setup.cfg", "environment.yml", "directory.packages.props",
    "packages.config", "packages.lock.json", "go.mod", "go.sum", "cargo.toml", "cargo.lock", "gemfile",
    "gemfile.lock", "pom.xml", "build.gradle", "build.gradle.kts", "composer.json", "composer.lock",
}
CI_PREFIXES = (".github/workflows/", ".github/actions/", ".circleci/", ".buildkite/", ".azure-pipelines/", ".husky/", ".gitlab/ci/")
CI_BASENAMES = {
    ".gitlab-ci.yml", "jenkinsfile", "bitbucket-pipelines.yml", "azure-pipelines.yml",
    ".pre-commit-config.yaml", "dependabot.yml", "dependabot.yaml", "renovate.json", "renovate.json5",
    ".renovaterc", ".renovaterc.json",
}
# Classifies changed path names to suggest a review tier. File contents are checked separately: changed lines
# from the diff, and untracked files under the size limit read from disk, are scanned for likely secrets,
# which are reported with redacted previews.
BUILD_RE = re.compile(
    r"(^|/)(makefile|justfile|cmakelists\.txt|directory\.build\.(props|targets)|global\.json|nuget\.config|"
    r"\.(?:npmrc|yarnrc(?:\.yml)?)|pip\.conf|tsconfig[^/]*\.json|\.babelrc|"
    r"(vite|webpack|rollup|esbuild|tsup|babel)\.config\.[cm]?[jt]s)$"
)
LINT_CONFIG_RE = re.compile(
    r"(^|/)(\.eslintrc[^/]*|eslint\.config\.[cm]?[jt]s|\.flake8|\.?ruff\.toml|mypy\.ini|\.pylintrc|pylintrc|"
    r"\.rubocop\.yml|\.golangci\.ya?ml|\.editorconfig|\.globalconfig|stylecop\.json|\.stylelintrc[^/]*|"
    r"biome\.jsonc?)$"
)
CONTRACT_RE = re.compile(r"(^|/)(openapi|swagger|asyncapi)[^/]*\.(ya?ml|json)$|\.(proto|graphql|gql|avsc)$")
INFRA_RE = re.compile(
    r"\.(tf|tfvars|bicep|bicepparam)$|(^|/)(k8s|kubernetes|helm|charts|manifests|terraform|infra|infrastructure)/"
    r"|(^|/)pulumi\.[^/]*ya?ml$"
)
CONTAINER_RE = re.compile(r"(^|/)(dockerfile|[^/]*\.dockerfile|docker-compose[^/]*\.ya?ml|compose[^/]*\.ya?ml)$")
ENV_FILE_RE = re.compile(r"(^|/)\.env(\.[^/]+)?$|[^/]\.env$")
ENV_TEMPLATE_RE = re.compile(r"\.(example|sample|template|dist|defaults)$")
KEY_FILE_RE = re.compile(r"\.(pem|key|p12|pfx|jks|keystore)$|(^|/)id_(rsa|dsa|ecdsa|ed25519)$")

DESTRUCTIVE_SQL_RE = re.compile(
    r"\b(drop\s+(table|column|schema|database|index|view)|truncate\b|"
    r"alter\s+table\s+\S+\s+(drop|rename|alter\s+column)|delete\s+from\s+[\w.\"]+\s*;)",
    re.IGNORECASE,
)
DESTRUCTIVE_ORM_RE = re.compile(
    r"\b(op\.(drop_table|drop_column|alter_column|rename_table)|"
    r"migrationBuilder\.(DropTable|DropColumn|RenameColumn|RenameTable|AlterColumn)|"
    r"migrations\.(RemoveField|DeleteModel|RenameField|RenameModel|AlterField)|"
    r"remove_column|drop_table|rename_column|change_column|dropTable|dropColumn|renameColumn)\b"
)
AUTH_CODE_RE = re.compile(
    r"\bjwt\.(?:decode|encode)\b|\bverify\s*=\s*False\b|\bbcrypt\b|\bargon2\b|\bpbkdf2\b|\bscrypt\b|"
    r"\bhashlib\.(?:md5|sha1)\b|\bset_cookie\(|\bSetCookie\b|@login_required\b|\[Authorize\b|"
    r"\[AllowAnonymous\b|\bAllowAnonymous\(|\bUseAuthentication\(|\bUseAuthorization\(|"
    r"\bpassport\.(?:authenticate|use)\(|\bOAuth2PasswordBearer\b|\bHTTPBearer\b|\bcheck_password\b|"
    r"\bverify_password\b|\bTokenValidationParameters\b|\brejectUnauthorized\s*:\s*false\b|"
    r"\bInsecureSkipVerify\s*:\s*true\b|\bCORS_ALLOW_ALL|allow_origins\s*=\s*\[\s*[\"']\*"
)
LLM_RE = re.compile(
    r"\b(openai|anthropic|chat\.completions|messages\.create|google\.genai|generativeai|langchain|"
    r"llama_index|llamaindex|semantic_kernel|bedrock-runtime|invoke_model|azure\.ai\.inference|"
    r"ollama|fastmcp|modelcontextprotocol|tool_choice)\b",
    re.IGNORECASE,
)
NETWORK_RE = re.compile(
    r"\brequests\.(?:get|post|put|patch|delete|head|request|Session)\b|\bhttpx\.|\baiohttp\.|"
    r"\burllib\.request\b|\burlopen\(|\baxios\b|\bHttpClient\b|\bWebClient\b|\bRestTemplate\b|"
    r"\bhttp\.(?:Get|Post|NewRequest)\b|\bfetch\("
)
PERSONAL_DATA_RE = re.compile(
    r"\b(date_of_birth|dateofbirth|birth_date|birthdate|ssn|social_security|passport_number|"
    r"national_id|nationalid|tax_id|iban|credit_card|card_number|cardnumber|cvv)\b",
    re.IGNORECASE,
)


def _tokens(path: str, pairs: bool = False) -> set:
    """Split a path into lower-case words; with pairs, also join neighbours (sign + in)."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", path)
    parts = [t for t in re.split(r"[/._\-\s]+", spaced.lower()) if t]
    tokens = set(parts)
    if pairs:
        tokens.update(a + b for a, b in zip(parts, parts[1:]))
    return tokens


def _basename(path: str) -> str:
    return path.rsplit("/", 1)[-1].lower()


def is_test_path(path: str) -> bool:
    base = path.rsplit("/", 1)[-1]
    lower_base = base.lower()
    if _tokens(path) & TEST_TOKENS or lower_base == "conftest.py":
        return True
    return bool(
        re.match(r"test_.*\.py$", lower_base)
        or re.search(r"_test\.(py|go)$|\.(test|spec)\.[cm]?[jt]sx?$|_spec\.rb$", lower_base)
        or re.search(r"(Test|Tests|Spec|Specs|IT)\.(cs|java|kt|scala|fs|vb)$", base)
    )


def is_doc_path(path: str) -> bool:
    lower = path.lower()
    base = _basename(path)
    stem = base.split(".", 1)[0]
    if lower.endswith(DOC_EXTENSIONS):
        return True
    if stem in DOC_BASENAMES and (base == stem or base.endswith(".txt")):
        return True
    in_docs = lower.startswith(DOC_DIRS) or any("/" + d in lower for d in DOC_DIRS)
    return in_docs and lower.endswith((".txt",) + IMAGE_EXTENSIONS)


def is_dependency_path(path: str) -> bool:
    base = _basename(path)
    return (
        base in DEPENDENCY_BASENAMES
        or bool(re.match(r"requirements[^/]*\.(txt|in)$", base))
        or base.endswith((".csproj", ".fsproj", ".vbproj"))
    )


def suggest_tier(changes: List[FileChange]) -> Tuple[int, List[dict], List[str]]:
    """Return (suggested tier floor, reasons, advisory notes) for the change set."""
    reasons: dict = {}
    notes: List[str] = []

    def add(tier: int, label: str, path: str) -> None:
        entry = reasons.setdefault(label, {"tier": tier, "label": label, "files": []})
        entry["tier"] = max(entry["tier"], tier)
        if path not in entry["files"]:
            entry["files"].append(path)

    if not changes:
        return 0, [], ["No changes found."]

    ui_touched = lint_touched = False
    for change in changes:
        path = change.path
        lower = path.lower()
        base = _basename(path)
        tokens = _tokens(path, pairs=True)
        test = is_test_path(path)
        added_text = [text for _, text in change.added]
        changed_text = added_text + [text for _, text in change.removed]

        if not test and (tokens & PROMPT_TOKENS or base in AGENT_INSTRUCTION_FILES):
            add(2, "language model prompt or agent instructions", path)
            continue
        if is_doc_path(path):
            add(0, "documentation only", path)
            continue
        add(1, "code or configuration change", path)

        if not test and tokens & AUTH_TOKENS:
            add(3, "authentication, authorisation, sessions, secrets or cryptography", path)
        if not test and tokens & PAYMENT_TOKENS:
            add(3, "payments or billing", path)
        if ENV_FILE_RE.search(lower) and not ENV_TEMPLATE_RE.search(lower):
            add(3, "environment file that may hold secrets", path)
        if KEY_FILE_RE.search(lower):
            add(3, "key or certificate file", path)

        if not test and (tokens & MIGRATION_TOKENS or "db/migrate/" in lower or lower.endswith(".sql")):
            add(2, "schema, migration or SQL change", path)
            if any(DESTRUCTIVE_SQL_RE.search(t) or DESTRUCTIVE_ORM_RE.search(t) for t in added_text):
                add(3, "destructive or rewriting data change", path)

        if is_dependency_path(path):
            add(2, "dependency manifest or lockfile", path)
        if lower.startswith(CI_PREFIXES) or base in CI_BASENAMES or re.match(r"azure-pipelines[^/]*\.ya?ml$", base):
            add(2, "CI/CD pipeline, hook or automation", path)
        if BUILD_RE.search(lower):
            add(2, "build or package configuration", path)
        if INFRA_RE.search(lower):
            add(2, "infrastructure as code (inspect production networking/security impact)", path)
        if CONTAINER_RE.search(lower):
            add(2, "container build or runtime configuration", path)
        if CONTRACT_RE.search(lower):
            add(2, "public contract file", path)

        if not test and lower.endswith(CODE_EXTENSIONS):
            if any(AUTH_CODE_RE.search(t) for t in changed_text):
                add(3, "authentication, cryptography or security-sensitive code", path)
            if any(LLM_RE.search(t) for t in added_text):
                add(2, "language model, agent or MCP code", path)
            if any(NETWORK_RE.search(t) for t in added_text):
                add(2, "new network call (check timeouts, retries and SSRF)", path)
            if any(PERSONAL_DATA_RE.search(t) for t in added_text):
                add(2, "possible personal or financial data", path)

        ui_touched = ui_touched or lower.endswith(UI_EXTENSIONS)
        lint_touched = lint_touched or bool(LINT_CONFIG_RE.search(lower))

    ordered = sorted(reasons.values(), key=lambda r: (-r["tier"], r["label"]))
    minimum = max(r["tier"] for r in ordered)
    if minimum > 0:
        ordered = [r for r in ordered if r["label"] != "documentation only"]
    if minimum > 1:
        ordered = [r for r in ordered if r["label"] != "code or configuration change"]
    if ui_touched:
        notes.append("User interface files changed: run the accessibility checks.")
    if lint_touched:
        notes.append("Linter, formatter or analyser configuration changed: confirm no rule was relaxed.")
    return minimum, ordered, notes


# --------------------------------------------------------------------------- test weakening

ASSERT_RE = re.compile(
    r"\b(assert\w*|expect\s*\(|assertThat|Assert\.\w+|pytest\.raises|t\.(Error|Errorf|Fatal|Fatalf|Fail)\b|"
    r"require\.\w+|toThrow|[Vv]erify\s*\()|\.[Ss]hould\b"
)
SKIP_RE = re.compile(
    r"@pytest\.mark\.(skip|skipif|xfail)\b|pytest\.skip\(|@unittest\.skip|unittest\.skip\(|"
    r"\b(it|test|describe|context)\.(skip|todo)\b|\bx(it|describe|test)\s*\(|@Disabled\b|@Ignore\b|"
    r"\[Ignore\]|\[(Fact|Theory)\s*\(\s*Skip\s*=|\bt\.Skip(Now|f)?\(|test\.fixme\("
)
ONLY_RE = re.compile(r"\b(it|test|describe|context)\.only\b|\bf(it|describe)\s*\(")
RETRY_RE = re.compile(
    r"@pytest\.mark\.flaky|--reruns\b|\breruns\s*=|jest\.retryTimes\(|this\.retries\(|\bretries\s*:\s*[1-9]"
)
TEST_CONFIG_RE = re.compile(
    r"^((playwright|jest|vitest|cypress|karma|wdio)\.config\.[^/]+|\.mocharc[^/]*|pytest\.ini|tox\.ini|"
    r"setup\.cfg|pyproject\.toml|package\.json)$"
)
SUPPRESSION_RE = re.compile(
    r"#\s*type:\s*ignore|#\s*noqa|#\s*pragma:\s*no\s*cover|eslint-disable|@ts-ignore|@ts-nocheck|"
    r"@ts-expect-error|#pragma\s+warning\s+disable|//\s*nolint|@SuppressWarnings|\[SuppressMessage|"
    r"#\s*pylint:\s*disable|#\s*nosec\b|NOSONAR|rubocop:disable"
)
COVERAGE_FILES = {
    "setup.cfg", "pyproject.toml", ".coveragerc", "tox.ini", "package.json", ".nycrc", ".nycrc.json",
    "codecov.yml", ".codecov.yml", "jest.config.js", "jest.config.ts", "jest.config.mjs",
    "jest.config.cjs", "vitest.config.ts", "vitest.config.js", "vitest.config.mts",
}
COVERAGE_RE = re.compile(
    r"(fail_under|fail-under|cov-fail-under|branches|functions|lines|statements|target|minimum_coverage)"
    r"[\"']?\s*[:=]?\s*[\"']?(\d+(?:\.\d+)?)"
)


def find_weakening(changes: List[FileChange]) -> Tuple[List[Finding], List[Finding]]:
    """Flag deleted tests, net assertion loss, skip, focus and retry markers, suppressions, lower coverage."""
    weakening: List[Finding] = []
    suppressions: List[Finding] = []
    for change in changes:
        path = change.path
        base = _basename(path)
        test = is_test_path(path)
        doc = is_doc_path(path)
        test_config = bool(TEST_CONFIG_RE.match(base))
        js = base.endswith(JS_EXTENSIONS)
        if test and change.status == "deleted":
            weakening.append(Finding("test file deleted", path, None, "a test file was removed"))
            continue
        if test and change.status != "added":
            removed = sum(1 for _, t in change.removed if ASSERT_RE.search(t))
            added = sum(1 for _, t in change.added if ASSERT_RE.search(t))
            if removed > added:
                weakening.append(Finding(
                    "assertions removed", path, None,
                    f"net {removed - added} assertion line(s) removed; confirm the behaviour is still checked",
                ))
        # Details show only the matched marker, never the whole line, so a secret on
        # the same line cannot leak into the report.
        for line, text in change.added:
            match = SKIP_RE.search(text) if test else None
            if match:
                weakening.append(Finding("skip marker added", path, line, match.group(0).strip()))
            match = ONLY_RE.search(text) if test and js else None
            if match:
                weakening.append(Finding("focused test added", path, line, f"{match.group(0).strip()} stops other tests running"))
            match = RETRY_RE.search(text) if test or test_config else None
            if match:
                weakening.append(Finding("test retries added", path, line, match.group(0).strip()))
            match = SUPPRESSION_RE.search(text) if not doc else None
            if match:
                suppressions.append(Finding("suppression added", path, line, match.group(0).strip()))
        if base in COVERAGE_FILES or "coverage" in _tokens(path):
            old = {m.group(1): float(m.group(2)) for _, t in change.removed for m in COVERAGE_RE.finditer(t)}
            new = {m.group(1): float(m.group(2)) for _, t in change.added for m in COVERAGE_RE.finditer(t)}
            for key in sorted(set(old) & set(new)):
                if new[key] < old[key]:
                    weakening.append(Finding(
                        "coverage threshold lowered", path, None, f"{key}: {old[key]:g} -> {new[key]:g}"
                    ))
    return weakening, suppressions


# --------------------------------------------------------------------------- secrets

@dataclass
class SecretRule:
    name: str
    pattern: "re.Pattern[str]"
    keep: int = 0              # leading characters that are a public type prefix, safe to show
    show_full: bool = False    # the match is a marker such as a PEM header, not the secret itself
    heuristic: bool = False    # skipped in tests; placeholders and low-entropy values are ignored
    path_re: Optional["re.Pattern[str]"] = None  # only files whose lower-case path matches

_CRED_NAME = (
    r"(?:password|passwd|pwd|secret|api[_\-]?key|apikey|access[_\-]?key|auth[_\-]?token|"
    r"client[_\-]?secret|private[_\-]?key|token)"
)
CONFIG_FILE_RE = re.compile(r"(^|/)\.env(\.[^/]*)?$|\.(ya?ml|ini|cfg|conf|properties|toml|env)$")

SECRET_RULES = [
    SecretRule("private key block", re.compile(r"(-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----)"), show_full=True),
    SecretRule("AWS access key ID", re.compile(r"\b((?:AKIA|ASIA)[0-9A-Z]{16})\b"), keep=4),
    SecretRule("GitHub token", re.compile(r"\b((?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,})\b"), keep=4),
    SecretRule("GitHub fine-grained token", re.compile(r"\b(github_pat_[A-Za-z0-9_]{60,})\b"), keep=11),
    SecretRule("GitLab token", re.compile(r"\b(glpat-[A-Za-z0-9_\-]{20,})"), keep=6),
    SecretRule("Slack token", re.compile(r"\b(xox[abposr]-[A-Za-z0-9-]{10,})"), keep=5),
    SecretRule("Slack webhook URL", re.compile(r"(https://hooks\.slack\.com/services/[A-Za-z0-9/]{20,})"), keep=33),
    SecretRule("Stripe live key", re.compile(r"\b((?:sk|rk)_live_[A-Za-z0-9]{16,})"), keep=8),
    SecretRule("Google API key", re.compile(r"\b(AIza[0-9A-Za-z_\-]{35})"), keep=4),
    SecretRule("npm token", re.compile(r"\b(npm_[A-Za-z0-9]{36})\b"), keep=4),
    SecretRule("PyPI token", re.compile(r"\b(pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_\-]{50,})"), keep=5),
    SecretRule("Hugging Face token", re.compile(r"\b(hf_[A-Za-z0-9]{34,})\b"), keep=3),
    SecretRule("Anthropic API key", re.compile(r"\b(sk-ant-[A-Za-z0-9_\-]{20,})"), keep=7),
    SecretRule(
        "OpenAI-style API key",
        re.compile(r"\b(sk-(?:proj-|svcacct-|admin-)?(?=[A-Za-z0-9_\-]*[0-9])(?=[A-Za-z0-9_\-]*[A-Z])[A-Za-z0-9_\-]{20,})"),
        keep=3,
    ),
    SecretRule("JSON Web Token", re.compile(r"\b(eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,})"), keep=3),
    SecretRule("Azure storage account key", re.compile(r"(AccountKey=[A-Za-z0-9+/=]{40,})"), keep=11),
    SecretRule("Azure SAS signature", re.compile(r"[?&]sig=([A-Za-z0-9%+/=]{30,})")),
    SecretRule(
        "password in connection URL",
        re.compile(r"(?i)\b(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|redis|rediss|amqps?|mssql|sqlserver)://[^:\s/@]+:([^@\s]{4,})@"),
        heuristic=True,
    ),
    SecretRule(
        "credential assigned in code",
        re.compile(
            r"(?i)\b[\w.\-]*" + _CRED_NAME
            + r"[\"']?(?:\s*:\s*[A-Za-z_][\w.]*)?\s*(?::=|[:=])\s*[\"']([^\"'\s]{8,})[\"']"
        ),
        heuristic=True,
    ),
    SecretRule(
        "credential in configuration file",
        re.compile(r"(?i)^\s*(?:export\s+)?[\w.\-]*" + _CRED_NAME + r"\s*[:=]\s*([^\s\"'#]{8,})\s*(?:#.*)?$"),
        heuristic=True,
        path_re=CONFIG_FILE_RE,
    ),
]

# Documentation examples (AWS's documented sample key ends in EXAMPLE) and obvious fakes.
EXAMPLE_HINTS = ("example", "dummy", "fake", "placeholder", "redacted", "xxxxxxxx")
PLACEHOLDER_HINTS = EXAMPLE_HINTS + (
    "sample", "changeme", "change_me", "change-me", "your", "xxxx", "****", "todo", "<", ">", "${",
    "{{", "%(", "process.env", "os.environ", "getenv",
)


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = {ch: value.count(ch) for ch in set(value)}
    return -sum((n / len(value)) * math.log2(n / len(value)) for n in counts.values())


def redact(value: str, keep: int) -> str:
    keep = max(0, min(keep, len(value) - 4))
    return f"{value[:keep]}{'*' * 8} ({len(value)} chars)"


def _is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return value.startswith(("$", "%", "@")) or any(hint in lowered for hint in PLACEHOLDER_HINTS)


def find_secrets(changes: List[FileChange]) -> List[Finding]:
    findings: List[Finding] = []
    for change in changes:
        lower = change.path.lower()
        test = is_test_path(change.path)
        rules = [
            rule for rule in SECRET_RULES
            if not (rule.heuristic and test) and (rule.path_re is None or rule.path_re.search(lower))
        ]
        for line, text in change.added:
            if any(marker in text for marker in IGNORE_MARKERS):
                continue
            taken: List[Tuple[int, int]] = []
            for rule in rules:
                for match in rule.pattern.finditer(text):
                    start, end = match.span(1)
                    if any(start < t_end and t_start < end for t_start, t_end in taken):
                        continue
                    value = match.group(1)
                    if any(hint in value.lower() for hint in EXAMPLE_HINTS):
                        continue
                    if rule.heuristic and (_is_placeholder(value) or shannon_entropy(value) < MIN_HEURISTIC_ENTROPY):
                        continue
                    taken.append((start, end))
                    preview = value if rule.show_full else redact(value, rule.keep)
                    findings.append(Finding(rule.name, change.path, line, preview))
    return findings


# --------------------------------------------------------------------------- reporting

def build_report(changes: List[FileChange], strict: bool) -> dict:
    tier, reasons, notes = suggest_tier(changes)
    weakening, suppressions = find_weakening(changes)
    secrets = find_secrets(changes)
    exit_code = 1 if secrets or (strict and (weakening or suppressions)) else 0
    return {
        "files_changed": len(changes),
        "lines_added": sum(len(c.added) for c in changes),
        "lines_removed": sum(len(c.removed) for c in changes),
        "minimum_tier": TIER_NAMES[tier],  # A suggested floor to check against actual impact.
        "tier_reasons": reasons,
        "notes": notes,
        "test_weakening": [f.as_dict() for f in weakening],
        "suppressions": [f.as_dict() for f in suppressions],
        "secrets": [f.as_dict() for f in secrets],
        "exit_code": exit_code,
    }


def _location(item: dict) -> str:
    return f"{item['path']}:{item['line']}" if item.get("line") else item["path"]


def format_text(report: dict) -> str:
    out = [
        f"change_scan: {report['files_changed']} file(s), "
        f"+{report['lines_added']} -{report['lines_removed']} lines",
        f"Review cue: {report['minimum_tier']} (heuristic only; assess actual impact and reversibility)",
    ]
    for reason in report["tier_reasons"]:
        files = reason["files"]
        shown = ", ".join(files[:5]) + (f" and {len(files) - 5} more" if len(files) > 5 else "")
        out.append(f"  {TIER_NAMES[reason['tier']]}  {reason['label']}: {shown}")
    for note in report["notes"]:
        out.append(f"Note: {note}")
    sections = (
        ("Possible test weakening", report["test_weakening"]),
        ("Suppressions added", report["suppressions"]),
        ("Likely secrets (values redacted)", report["secrets"]),
    )
    for title, items in sections:
        if items:
            out.append(f"{title} ({len(items)}):")
            for item in items:
                out.append(f"  {_location(item)}  {item['kind']}: {item['detail']}")
    if report["secrets"]:
        out.append("Result: likely secret found. Remove it from the change; if it was ever real, revoke and rotate it.")
    elif report["exit_code"]:
        out.append("Result: strict mode found test-weakening signals or new suppressions. Justify or remove them.")
    else:
        out.append("Result: no blocking findings.")
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Flag review cues, weakened tests and likely secrets in a change.",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--staged", action="store_true", help="scan staged changes only")
    source.add_argument("--base", metavar="REF", help="scan everything since this branch diverged from REF")
    source.add_argument("--diff-file", metavar="PATH", help="scan a unified diff file instead of git ('-' reads stdin)")
    parser.add_argument("--repo", default=".", help="repository to scan (default: current directory)")
    parser.add_argument("--no-untracked", action="store_true", help="ignore untracked files")
    parser.add_argument("--strict", action="store_true", help="also exit 1 on test-weakening signals and new suppressions")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = parser.parse_args(argv)

    try:
        if args.diff_file:
            if args.diff_file == "-":
                text = sys.stdin.read()
            else:
                with open(args.diff_file, encoding="utf-8", errors="replace") as handle:
                    text = handle.read()
            changes = parse_unified_diff(text)
        else:
            changes = collect_changes(args.repo, args.staged, args.base, not args.no_untracked)
    except (GitError, OSError) as exc:
        print(f"change_scan: {exc}", file=sys.stderr)
        return 2

    report = build_report(changes, args.strict)
    print(json.dumps(report, indent=2) if args.json else format_text(report))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
