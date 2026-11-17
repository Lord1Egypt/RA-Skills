#!/usr/bin/env python3
"""
_env_check — classified env-var declaration check (false-positive governance v1.1).

Replaces the old "reads env == must declare" assumption with a two-stage model:

  Stage 1  extract per-access records (variable, file, line, language, form)
  Stage 2  classify each record into a finding code, then apply profile severity

Finding codes & default severities (profile may override per code):
  ENV_REQUIRED_UNDECLARED  required user config, undeclared   WARN (profile)
  ENV_OPTIONAL_OVERRIDE    has usable fallback                 hidden (JSON only)
  ENV_RUNTIME_INJECTED     runner/daemon contract injection    hidden (JSON only)
  ENV_AMBIENT              OS/process ambient                  hidden
  ENV_TEST_ONLY            tests/fixtures/debug entries only   hidden, never blocks
  ENV_REVIEW_REQUIRED      static analysis can't decide        INFO, no auto-metadata
  ENV_DECLARED_UNUSED      declared but code never reads       WARN (confirm, then remove)
  ENV_DECLARED_NON_USER    declared runtime-injected/ambient   WARN (remove declaration)

Contract lists (runtime-injected / ambient) live in config/env_contracts.json —
versioned, evidence-based, owned by the checker. Never pushed into audited
skills' metadata. No unbounded MULTICA_* prefix exemption: exact names only.
"""

import ast
import json
import re
from pathlib import Path

_CONTRACTS_PATH = Path(__file__).resolve().parent.parent / "config" / "env_contracts.json"

# Finding codes
F_REQUIRED_UNDECLARED = "ENV_REQUIRED_UNDECLARED"
F_OPTIONAL_OVERRIDE = "ENV_OPTIONAL_OVERRIDE"
F_RUNTIME_INJECTED = "ENV_RUNTIME_INJECTED"
F_AMBIENT = "ENV_AMBIENT"
F_TEST_ONLY = "ENV_TEST_ONLY"
F_REVIEW_REQUIRED = "ENV_REVIEW_REQUIRED"
F_DECLARED_UNUSED = "ENV_DECLARED_UNUSED"
F_DECLARED_NON_USER = "ENV_DECLARED_NON_USER"
F_DECLARED_INDIRECT = "ENV_DECLARED_INDIRECT"

# Default severity per code; profiles override via "env_severity" dict.
DEFAULT_SEVERITY = {
    F_REQUIRED_UNDECLARED: "WARN",
    F_OPTIONAL_OVERRIDE: None,   # None = hidden from text report, JSON evidence only
    F_RUNTIME_INJECTED: None,
    F_AMBIENT: None,
    F_TEST_ONLY: None,
    F_REVIEW_REQUIRED: "INFO",
    F_DECLARED_UNUSED: "WARN",
    F_DECLARED_NON_USER: "WARN",
    F_DECLARED_INDIRECT: None,  # hidden: JS alias/parse flow use, JSON evidence only
}

# Legacy fallback ambient list (subset of contract file content) — used only
# when config/env_contracts.json is missing or corrupt. Never raises.
_AMBIENT_ENV = {
    "PATH", "HOME", "USER", "PWD", "SHELL", "LANG", "LC_ALL", "TERM", "TMPDIR",
    "TMP", "TEMP", "PYTHONPATH", "VIRTUAL_ENV", "CI", "DEBUG", "NODE_ENV",
    "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy",
}

# Regex fallback patterns (used when a Python file fails to parse)
_ENV_ACCESS_PATTERNS = [
    re.compile(r'os\.environ\s*\[\s*[\'"]([A-Z_][A-Z0-9_]*)[\'"]\s*\]'),
    re.compile(r'os\.environ\.get\s*\(\s*[\'"]([A-Z_][A-Z0-9_]*)[\'"]'),
    re.compile(r'os\.getenv\s*\(\s*[\'"]([A-Z_][A-Z0-9_]*)[\'"]'),
    re.compile(r'process\.env\.([A-Z_][A-Z0-9_]*)'),
    re.compile(r'process\.env\s*\[\s*[\'"]([A-Z_][A-Z0-9_]*)[\'"]\s*\]'),
]

# Test/dev path markers → ENV_TEST_ONLY, never blocks a release
_TEST_PATH_RE = re.compile(
    r"(^|/)(tests?|test|fixtures?|__tests__|spec|e2e|mocks?|conftest)(/|\.|$)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# JS data-flow tracking for the environment object (v1.2)
#
# The direct-read regexes below only see `process.env.X` / `process.env["X"]`.
# Bundled/minified collectors typically alias first:
#
#   const environment = process.env                      // alias binding
#   const cfg = schema.parse(environment)               // Zod parse
#   const cfg = schema.safeParse({...environment})      // spread + safeParse
#   function loadConfig(env) { ... env.X ... }           // param binding
#   return { profile: env.MULTICA_PROFILE }              // return-value flow
#   const config = loadConfig(process.env)
#
# We track env-object identity through a bounded fixpoint (aliases, params,
# parse results, return values) and mark member accesses on those objects as
# INDIRECT uses. Indirect uses ONLY feed the reverse declared-unused check —
# they never satisfy/soften the forward classification (required/optional),
# because fallback evidence on an aliased access is not statically decidable.
# ---------------------------------------------------------------------------

_ENV_IDENT = r'[A-Za-z_$][\w$]*'
_JS_ALIAS_DEF = re.compile(
    rf'(?:const|let|var|;|,|^|\()\s*({_ENV_IDENT})\s*=\s*process\.env\s*(?=[;,)\n]|$)'
)
_JS_PARSE_CALL = re.compile(
    rf'(?:{_ENV_IDENT}(?:\.{_ENV_IDENT})*)\s*\.\s*(?:parse|safeParse)\s*\(\s*({_ENV_IDENT})'
)
_JS_SPREAD_INTO_PARSE = re.compile(
    rf'(?:{_ENV_IDENT}(?:\.{_ENV_IDENT})*)\s*\.\s*(?:parse|safeParse)\s*\(\s*\{{\s*\.\.\.\s*({_ENV_IDENT})'
)
_JS_FUNC_DEF = re.compile(
    rf'(?:function\s+({_ENV_IDENT})\s*|({_ENV_IDENT})\s*=\s*(?:async\s*)?)\(\s*([^(){{}}]*?)\s*\)\s*(?:=>|\{{)'
)


def _js_env_aliases(source: str) -> tuple:
    """Collect (env_aliases, parse_result_names) via bounded fixpoint.

    env_aliases:       identifiers bound to the environment object itself —
                       `const env = process.env`, function params whose call
                       site passes a tracked env object (`fn(process.env)`,
                       `loadConfig(env)`).
    parse_result_names: identifiers bound to schema.parse/safeParse results
                       of a tracked alias, or to config-loader call results
                       (`const config = loadConfig(process.env)`) — member
                       access on them is an INDIRECT env use.
    """
    aliases: set = set()
    parse_results: set = set()

    # seed: direct aliases of process.env (not member access)
    for m in _JS_ALIAS_DEF.finditer(source):
        aliases.add(m.group(1))

    for _ in range(4):                                # bounded fixpoint
        before = (len(aliases), len(parse_results))

        # (a) function params whose call site passes a tracked env object
        for fm in _JS_FUNC_DEF.finditer(source):
            fname = fm.group(1) or fm.group(2)
            params = [p.strip() for p in fm.group(3).split(",") if p.strip()]
            if not fname or not params:
                continue
            for call in re.finditer(
                    rf'\b{re.escape(fname)}\s*\(\s*([^()]*)\s*\)', source):
                args = [a.strip() for a in call.group(1).split(",") if a.strip()]
                for i, a in enumerate(args):
                    a_base = a.strip("() ")
                    if (a_base in aliases or a_base == "process.env"
                            or a_base in parse_results) and i < len(params):
                        aliases.add(params[i])

        # (b) parse results: const cfg = schema.parse(<alias>) and
        #     const cfg = schema.safeParse({...alias})
        for pat, group in ((_JS_PARSE_CALL, 1), (_JS_SPREAD_INTO_PARSE, 1)):
            for pm in pat.finditer(source):
                if pm.group(1) not in aliases:
                    continue
                m2 = re.search(
                    rf'(?:const|let|var|;|,|^)\s*({_ENV_IDENT})\s*=\s*'
                    + re.escape(pm.group(0)), source, re.MULTILINE)
                if m2:
                    parse_results.add(m2.group(1))

        # (b2) safeParse result member re-binding: const cfg = parsed.data
        #      — .data on a tracked parse result carries the parsed env
        for dm in re.finditer(
                rf'(?:const|let|var|;|,|^)\s*({_ENV_IDENT})\s*=\s*({_ENV_IDENT})\.data\b',
                source):
            if dm.group(2) in parse_results:
                parse_results.add(dm.group(1))

        # (c) config-loader call-site binding: const config = loadConfig(env)
        #     — result carries env data when the fn body reads the env object
        for cm in re.finditer(
                rf'(?:const|let|var|;|,|^)\s*({_ENV_IDENT})\s*=\s*'
                rf'({_ENV_IDENT})\s*\(\s*([^(),]*)\s*\)', source, re.MULTILINE):
            ret_name, fname, arg = cm.group(1), cm.group(2), cm.group(3).strip()
            arg_base = arg.strip("() ")
            if arg_base not in aliases and arg_base != "process.env" \
                    and arg_base not in parse_results:
                continue
            if _js_fn_reads_envobj(source, fname, aliases):
                parse_results.add(ret_name)

        if (len(aliases), len(parse_results)) == before:
            break

    return aliases, parse_results


def _js_fn_reads_envobj(source: str, fname: str, aliases: set) -> bool:
    """True when function `fname`'s body reads the env object (alias member
    access or process.env access). Best-effort: slice from the function
    definition to the next top-level function boundary; on any doubt keep
    the old WARN behavior (return False — under-approximate only preserves
    the previous finding, never hides a real read)."""
    fdef = re.search(rf'\bfunction\s+{re.escape(fname)}\s*\(', source)
    if fdef:
        body = source[fdef.start():]
    else:
        fdef = re.search(rf'(?:const|let|var)\s+{re.escape(fname)}\s*=\s*(?:async\s*)?\(',
                         source)
        if not fdef:
            return False
        body = source[fdef.start():]
    nxt = re.search(rf'\n(?:function\s+{_ENV_IDENT}\s|const\s+{_ENV_IDENT}\s*=)',
                    body[10:])
    if nxt:
        body = body[:nxt.start() + 10]
    if re.search(r'\bprocess\.env\b', body):
        return True
    for a in aliases:
        if re.search(rf'\b{re.escape(a)}\s*(?:\.|\[)', body):
            return True
    return False


def _load_env_contracts() -> dict:
    """Load platform env contracts. Returns {runtime_injected, ambient, source}."""
    try:
        with open(_CONTRACTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        runtime: set = set()
        ambient: set = set()
        for platform, block in data.items():
            if platform.startswith("_") or not isinstance(block, dict):
                continue
            runtime.update(block.get("runtimeInjected", []) or [])
            ambient.update(block.get("ambient", []) or [])
        if runtime or ambient:
            return {"runtime_injected": runtime, "ambient": ambient,
                    "source": "env_contracts.json"}
    except Exception:
        pass
    return {"runtime_injected": set(), "ambient": set(_AMBIENT_ENV),
            "source": "legacy-fallback"}


# ---------------------------------------------------------------------------
# Source preprocessing: comments & string literals must not produce findings
# ---------------------------------------------------------------------------

def _strip_py_noncode(source: str) -> str:
    """Blank COMMENT and STRING token text in Python source (keeps layout).

    tokenize-based: `# os.environ["X"]` comments and docstring prose never
    produce pseudo-findings. Best-effort — on any tokenize failure the raw
    source is returned (classifier marks unparsed records for review anyway).
    """
    try:
        import io
        import tokenize
        out_lines = source.splitlines(keepends=True)
        toks = list(tokenize.generate_tokens(io.StringIO(source).readline))
        for tok in toks:
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                s_row, s_col = tok.start
                e_row, e_col = tok.end
                if s_row == e_row:
                    line = out_lines[s_row - 1]
                    out_lines[s_row - 1] = line[:s_col] + " " * (e_col - s_col) + line[e_col:]
                else:
                    for r in range(s_row, e_row + 1):
                        line = out_lines[r - 1]
                        if r == s_row:
                            out_lines[r - 1] = line[:s_col] + " " * (len(line) - s_col)
                        elif r == e_row:
                            out_lines[r - 1] = " " * e_col + line[e_col:]
                        else:
                            out_lines[r - 1] = " " * len(line)
        return "".join(out_lines)
    except Exception:
        return source


def _blank_js_sh_noncode(source: str) -> str:
    """Blank comment text in JS/Shell sources (keeps line structure)."""
    out = []
    for ln in source.splitlines(keepends=True):
        stripped = ln.lstrip()
        if stripped.startswith("#") or stripped.startswith("//"):
            out.append(" " * len(ln))
            continue
        # trailing // comment — only when no quote appears before it (heuristic)
        if "//" in ln:
            idx = ln.index("//")
            before = ln[:idx]
            if before.count('"') % 2 == 0 and before.count("'") % 2 == 0:
                out.append(ln[:idx] + " " * (len(ln) - idx))
                continue
        out.append(ln)
    return "".join(out)


# ---------------------------------------------------------------------------
# Stage 1: access-record extraction
# ---------------------------------------------------------------------------

def _has_guard_after(lineno: int, lines: list, target: "str | None" = None,
                      window: int = 8) -> bool:
    """True when a fail-fast guard on `target` follows the read within
    `window` lines — evidence the var is REQUIRED. When `target` is known the
    guard must reference that same variable; without a target (inline use) the
    unanchored heuristic applies (rare, flagged heuristic in reason)."""
    chunk = "\n".join(lines[lineno: lineno + window])
    if target:
        t = re.escape(target)
        return bool(
            re.search(rf"if\s+not\s+{t}\b[^\n]*:\s*\n?\s*"
                      rf"(?:raise|sys\.exit|SystemExit|parser\.error|exit\b|return\s+\d|os\.exit)", chunk)
            or re.search(rf"if\s+not\s+{t}\s*:\s*(?:raise|sys\.exit|SystemExit|parser\.error|exit\()", chunk)
        )
    return bool(
        re.search(r"if\s+not\s+[\w.]+\s*[:\n]\s*\n?\s*"
                  r"(?:raise|sys\.exit|SystemExit|parser\.error|exit\b|return\s+\d|os\.exit)", chunk)
        or re.search(r"if\s+not\s+[\w.]+\s*:\s*(?:raise|sys\.exit|SystemExit|parser\.error|exit\()", chunk)
    )


def _has_fallback_after(lineno: int, lines: list, target: "str | None" = None,
                        window: int = 8) -> bool:
    """True when the defaultless read is guarded by a usable fallback within
    `window` lines, anchored to `target` when known (governance §3.2:
    `os.getenv('X')` followed by `if not value: value = DEFAULT`)."""
    chunk = "\n".join(lines[lineno: lineno + window])
    if target:
        t = re.escape(target)
        return bool(
            re.search(rf"if\s+not\s+{t}\b[^\n]*:\s*\n?\s*{t}\s*=", chunk)   # if not x: x = D
            or re.search(rf"\b{t}\s*=\s*{t}\s+or\s+\S", chunk)                  # x = x or D
            or re.search(rf"if\s+{t}\s+and\s+os\.path\.is(?:dir|file)\(", chunk)  # conditional use
        )
    # no target: unanchored heuristic (inline use) — rare, conservative
    return bool(
        re.search(r"if\s+not\s+[\w.]+\s*[:\n]\s*[\w.]+\s*=", chunk)
        or re.search(r"[\w.]+\s*=\s*[\w.]+\s+or\s+\S", chunk)
    )


def _qualname(node) -> "str | None":
    """Qualified name of an attribute/name chain: os.environ.get → 'os.environ.get'."""
    if isinstance(node, ast.Attribute):
        base = _qualname(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Name):
        return node.id
    return None


def _read_call_var(node: ast.Call) -> "str | None":
    """Return the env var name if `node` is an os.getenv / os.environ.get read."""
    qual = _qualname(node.func)
    if qual not in ("os.getenv", "os.environ.get"):
        return None
    if (node.args and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)):
        return node.args[0].value
    return None


def _read_subscript_var(node: ast.Subscript) -> "str | None":
    """Return the env var name if `node` is an os.environ["X"] access."""
    if _qualname(node.value) != "os.environ":
        return None
    sl = node.slice
    if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
        return sl.value
    return None


def _py_env_records(source: str, rel: str) -> list:
    """AST-based Python env access records. Falls back to regex over
    comment-stripped source when the file can't be parsed.

    v1.1.1 fixes (UGLIC-found):
    - os.getenv(...) was systematically missed (recv_name built 'os' instead
      of 'os.getenv') — now via _qualname.
    - `if os.environ["X"] == "y":` was misjudged as a WRITE by the line-text
      heuristic — writes are now decided by AST Assign targets only.
    - `X = os.getenv("V") or D` or-fallback was detected by regex over
      string-blanked code (could never match) — now detected via AST BoolOp.
    - guard/fallback windows matched ANY variable's `if not x: raise` /
      `x = x or d` within 8 lines — now anchored to the actual assign target.
    """
    records: list = []
    code = _strip_py_noncode(source)
    try:
        tree = ast.parse(source)
    except Exception:
        for pat in _ENV_ACCESS_PATTERNS[:3]:
            for m in pat.finditer(code):
                records.append({
                    "variable": m.group(1), "file": rel,
                    "line": code.count("\n", 0, m.start()) + 1,
                    "access": "regex-fallback (unparsed source)",
                    "lang": "py", "has_default": None, "or_fallback": False,
                    "guard_after": False, "fb_guard": False, "target": None,
                })
        return records

    lines = source.splitlines()

    def _usable_default(node) -> bool:
        if isinstance(node, ast.Constant):
            if node.value is None or isinstance(node.value, bool):
                return False
            return bool(str(node.value).strip())
        return isinstance(node, (ast.Name, ast.Attribute, ast.Call, ast.BinOp,
                                 ast.JoinedStr))

    # Pass 1: env WRITE targets (Assign/AugAssign/AnnAssign to os.environ[...])
    write_ids: set = set()
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            targets = [node.target]
        for tgt in targets:
            if isinstance(tgt, ast.Subscript) and _qualname(tgt.value) == "os.environ":
                write_ids.add(id(tgt))

    # Pass 2: reads with assign-target context
    # Map id(read-node) → target name (from enclosing Assign), plus or-fallback set
    read_target: dict = {}
    or_read_ids: set = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            tgt_names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            tgt = tgt_names[0] if tgt_names else None
            # direct: X = <read>
            if isinstance(node.value, ast.Call):
                v = _read_call_var(node.value)
                if v is not None:
                    read_target[id(node.value)] = tgt
            elif isinstance(node.value, ast.Subscript):
                v = _read_subscript_var(node.value)
                if v is not None:
                    read_target[id(node.value)] = tgt
            elif isinstance(node.value, ast.BoolOp) and isinstance(node.value.op, ast.Or):
                for val in node.value.values:
                    if isinstance(val, ast.Call):
                        v = _read_call_var(val)
                        if v is not None:
                            read_target[id(val)] = tgt
                            or_read_ids.add(id(val))
                    elif isinstance(val, ast.Subscript):
                        v = _read_subscript_var(val)
                        if v is not None:
                            read_target[id(val)] = tgt
                            or_read_ids.add(id(val))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            var = _read_call_var(node)
            if var is None or id(node) in write_ids:
                continue
            args = node.args
            has_default = len(args) > 1 and _usable_default(args[1])
            if has_default:
                access = "os.getenv with default"
            elif len(args) == 1:
                access = "os.getenv without default"
            else:
                access = "os.getenv with empty default"
            is_or = id(node) in or_read_ids
            tgt = read_target.get(id(node))
            records.append({
                "variable": var, "file": rel, "line": node.lineno,
                "access": ("os.getenv or-fallback" if is_or else access),
                "lang": "py", "has_default": has_default, "or_fallback": is_or,
                "guard_after": _has_guard_after(node.lineno, lines, tgt),
                "fb_guard": ((not has_default and not is_or
                              and _has_fallback_after(node.lineno, lines, tgt))),
                "target": tgt,
            })
        elif isinstance(node, ast.Subscript):
            if id(node) in write_ids:
                continue
            var = _read_subscript_var(node)
            if var is None:
                continue
            tgt = read_target.get(id(node))
            records.append({
                "variable": var, "file": rel, "line": node.lineno,
                "access": "os.environ subscript read", "lang": "py",
                "has_default": False, "or_fallback": False,
                "guard_after": _has_guard_after(node.lineno, lines, tgt),
                "fb_guard": _has_fallback_after(node.lineno, lines, tgt),
                "target": tgt,
            })

    # Regex overlay only for unparsed fallback path (above); AST path is complete.
    return records


def _js_env_records(source: str, rel: str) -> list:
    """JS/TS env access records (regex over comment-blanked source)."""
    records: list = []
    code = _blank_js_sh_noncode(source)
    seen: set = set()

    # v1.2: env-object data flow — aliases (const environment = process.env),
    # function params bound at call sites (fn(process.env)), Zod
    # parse/safeParse results, and config-loader return values. Member access
    # on those objects is an INDIRECT use (reverse-check evidence only).
    aliases, parse_results = _js_env_aliases(code)
    indirect: set = set()   # line numbers of alias-member accesses

    def _ln(m):
        return code.count("\n", 0, m.start()) + 1

    for m in re.finditer(r'process\.env\.([A-Z_][A-Z0-9_]*)\s*(\?\?|\|\|)\s*\S', code):
        seen.add((m.group(1), _ln(m)))
        records.append({
            "variable": m.group(1), "file": rel, "line": _ln(m),
            "access": f"process.env {m.group(2)} fallback", "lang": "js",
            "has_default": True, "or_fallback": True, "guard_after": False,
        })
    for m in re.finditer(r'process\.env\.([A-Z_][A-Z0-9_]*)', code):
        if (m.group(1), _ln(m)) in seen:
            continue
        records.append({
            "variable": m.group(1), "file": rel, "line": _ln(m),
            "access": "process.env direct read", "lang": "js",
            "has_default": False, "or_fallback": False, "guard_after": False,
        })
    for m in re.finditer(r'process\.env\s*\[\s*[\'"]([A-Z_][A-Z0-9_]*)[\'"]\s*\]', code):
        records.append({
            "variable": m.group(1), "file": rel, "line": _ln(m),
            "access": "process.env subscript read", "lang": "js",
            "has_default": False, "or_fallback": False, "guard_after": False,
        })

    # alias member access → INDIRECT use records (reverse-check only)
    for name in sorted(aliases | parse_results):
        for m in re.finditer(
                rf'\b{re.escape(name)}\s*(?:\.([A-Za-z_$][\w$]*)|\[\s*[\'"]([A-Za-z_$][\w$]*)[\'"]\s*\])',
                code):
            var = m.group(1) or m.group(2)
            if not var:
                continue
            line = _ln(m)
            indirect.add(line)
            records.append({
                "variable": var, "file": rel, "line": line,
                "access": ("alias member access" if name in aliases else
                            "schema parse result access"),
                "lang": "js", "has_default": False, "or_fallback": False,
                "guard_after": False, "indirect": True,
            })
    return records


def _sh_env_records(source: str, rel: str) -> list:
    """Shell env access records: ${VAR:-d} optional, ${VAR:?msg} required,
    plain $VAR reads."""
    records: list = []
    code = _blank_js_sh_noncode(source)

    def _ln(m):
        return code.count("\n", 0, m.start()) + 1

    for m in re.finditer(r'\$\{([A-Z_][A-Z0-9_]*):-[^}]*\}|\$\{([A-Z_][A-Z0-9_]*)-[^}]*\}', code):
        records.append({
            "variable": m.group(1) or m.group(2), "file": rel, "line": _ln(m),
            "access": "${VAR:-default} shell default", "lang": "sh",
            "has_default": True, "or_fallback": True, "guard_after": False,
        })
    for m in re.finditer(r'\$\{([A-Z_][A-Z0-9_]*):\?[^}]*\}', code):
        records.append({
            "variable": m.group(1), "file": rel, "line": _ln(m),
            "access": "${VAR:?message} required expansion", "lang": "sh",
            "has_default": False, "or_fallback": False, "guard_after": True,
        })
    # Direct $VAR reads. A bare $VAR only counts as an ENV read when the var
    # was not assigned locally first (shell locals shadow env). Collect local
    # assignment targets: NAME=... / read NAME / for NAME in ...
    local_names: set = set()
    for m in re.finditer(r'(?m)^[^#\n]*?\b([A-Z_][A-Z0-9_]*)=(?!=)', code):
        local_names.add(m.group(1))
    for m in re.finditer(r'\b(?:read|readarray|mapfile)\s+(-[a-z]+\s+)*([A-Z_][A-Z0-9_]*)\b', code):
        local_names.add(m.group(2))
    for m in re.finditer(r'\bfor\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\b', code):
        local_names.add(m.group(1))

    covered = {r["variable"] for r in records}
    for m in re.finditer(r'(?<![\{\\w$])\$([A-Z_][A-Z0-9_]{2,})(?![\w:}])', code):
        var = m.group(1)
        if var in covered or var in local_names:
            continue
        covered.add(var)
        records.append({
            "variable": var, "file": rel, "line": _ln(m),
            "access": "$VAR direct read", "lang": "sh",
            "has_default": False, "or_fallback": False, "guard_after": False,
        })
    return records


def extract_env_records(skill_dir: Path) -> list:
    """Stage 1: scan scripts/ for env access records across py/js/sh."""
    records: list = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return records
    for script in sorted(scripts_dir.rglob("*")):
        if not script.is_file():
            continue
        rel = str(script.relative_to(skill_dir))
        if _TEST_PATH_RE.search(rel):
            continue  # test files never produce blocking findings
        try:
            source = script.read_text(encoding="utf-8")
        except Exception:
            continue
        if script.suffix == ".py":
            records.extend(_py_env_records(source, rel))
        elif script.suffix in {".js", ".ts", ".mjs", ".cjs"}:
            records.extend(_js_env_records(source, rel))
        elif script.suffix == ".sh":
            records.extend(_sh_env_records(source, rel))
    return records


# ---------------------------------------------------------------------------
# Stage 2: classification
# ---------------------------------------------------------------------------

def _classify(records: list, declared: set, contracts: dict) -> tuple:
    """Classify records → (findings list, evidence list).

    findings:  entries with code/severity/variable/file/line/access/reason
    evidence:  ALL records (including hidden ones) as machine-readable proof
    """
    findings: list = []
    evidence: list = []
    runtime = contracts["runtime_injected"]
    ambient = contracts["ambient"]

    # Aggregate per variable: any optional access makes the var optional
    by_var: dict = {}
    for r in records:
        by_var.setdefault(r["variable"], []).append(r)

    for var, recs in sorted(by_var.items()):
        # 0. indirect-only variables never take part in the forward
        #    classification — they are only evidence for the reverse check.
        if all(r.get("indirect") for r in recs):
            continue
        # 1. test-only already filtered at extraction; path re-check for safety
        # 2. runtime-injected per contract (exact names, no prefix exemption)
        if var in runtime:
            evidence.append(_ev(var, recs, F_RUNTIME_INJECTED,
                                "injected by runner/daemon contract "
                                f"({contracts['source']})"))
            continue
        # 3. ambient
        if var in ambient:
            evidence.append(_ev(var, recs, F_AMBIENT,
                                "OS/process ambient context"))
            continue
        # 4. any access with a usable fallback → optional override
        if any(r.get("has_default") or r.get("or_fallback") for r in recs):
            evidence.append(_ev(var, recs, F_OPTIONAL_OVERRIDE,
                                "missing value falls back to a built-in default"))
            continue
        # 5. fallback-guard after a defaultless read → optional (governance
        #    §3.2: "os.getenv('X') 后跟 if not X: X = DEFAULT 判 optional")
        if all(r.get("fb_guard") or r.get("has_default") or r.get("or_fallback")
               for r in recs) and any(r.get("fb_guard") for r in recs):
            evidence.append(_ev(var, recs, F_OPTIONAL_OVERRIDE,
                                "defaultless read guarded by a usable fallback"))
            continue
        # 6. guard after read or required expansion → required
        if any(r.get("guard_after") for r in recs):
            if var in declared:
                evidence.append(_ev(var, recs, F_OPTIONAL_OVERRIDE,
                                    "required (fail-fast) and already declared"))
            else:
                findings.append(_fd(var, recs, F_REQUIRED_UNDECLARED,
                                     "no default and a fail-fast guard: core "
                                     "function stops without it"))
            continue
        # 7. os.environ["X"] subscript without default → required-leaning
        subscripts = [r for r in recs if "subscript" in r["access"]]
        no_defaults = [r for r in recs
                       if r.get("has_default") is False and not r.get("or_fallback")]
        if subscripts or no_defaults:
            if var in declared:
                evidence.append(_ev(var, recs, F_OPTIONAL_OVERRIDE,
                                    "required-leaning and already declared"))
            else:
                findings.append(_fd(var, recs, F_REQUIRED_UNDECLARED,
                                     "read without any default or fallback"))
            continue
        # 8. everything else → review
        evidence.append(_ev(var, recs, F_REVIEW_REQUIRED,
                            "necessity not decidable statically (data-flow "
                            "or cross-function context needed)"))

    # Reverse checks on declarations
    for var in sorted(declared - set(by_var)):
        findings.append({
            "code": F_DECLARED_UNUSED, "severity": DEFAULT_SEVERITY[F_DECLARED_UNUSED],
            "variable": var, "file": "SKILL.md", "line": None,
            "access": "frontmatter declaration",
            "classification": "declared_unused",
            "reason": "declared in metadata but no matching env read found in scripts/",
            "suggestedAction": "confirm-then-remove",
        })
    for var in sorted(set(by_var) & declared):
        # v1.2: alias/parse-flow member access (Zod-parsed config objects,
        # fn(process.env) params, loader return values) counts as a real use
        # for the reverse check — reported as ENV_DECLARED_INDIRECT evidence,
        # not a WARN. Direct reads still classify normally below.
        if any(r.get("indirect") for r in by_var[var]):
            evidence.append(_ev_indirect(var, by_var[var]))
            continue
        if var in runtime or var in ambient:
            findings.append({
                "code": F_DECLARED_NON_USER,
                "severity": DEFAULT_SEVERITY[F_DECLARED_NON_USER],
                "variable": var, "file": "SKILL.md", "line": None,
                "access": "frontmatter declaration",
                "classification": "declared_non_user",
                "reason": ("declared variable is runtime-injected/ambient — "
                           "not user config; remove the declaration"),
                "suggestedAction": "remove-declaration",
            })
    return findings, evidence


def _ev(var, recs, code, reason):
    return {
        "code": code, "variable": var,
        "locations": [{"file": r["file"], "line": r["line"],
                       "access": r["access"]} for r in recs],
        "classification": code_to_classification(code),
        "reason": reason, "suggestedAction": "none",
    }


def _ev_indirect(var, recs):
    """ENV_DECLARED_INDIRECT evidence entry — declared var used through a
    JS alias / Zod parse / config-loader data flow (v1.2). Console stays
    silent by default; JSON keeps the hit path as machine-readable proof."""
    locs = [{"file": r["file"], "line": r["line"], "access": r["access"]}
            for r in recs]
    return {
        "code": F_DECLARED_INDIRECT, "variable": var,
        "locations": locs,
        "classification": "declared_indirect",
        "reason": "used via env-object alias / schema parse / loader return "
                  "(data-flow tracked)",
        "suggestedAction": "none",
    }


def _fd(var, recs, code, reason):
    return {
        "code": code, "severity": DEFAULT_SEVERITY[code],
        "variable": var, "file": recs[0]["file"], "line": recs[0]["line"],
        "access": recs[0]["access"],
        "classification": code_to_classification(code),
        "reason": reason, "suggestedAction": "declare-in-metadata",
    }


def code_to_classification(code: str) -> str:
    return {
        F_REQUIRED_UNDECLARED: "required_undeclared",
        F_OPTIONAL_OVERRIDE: "optional_override",
        F_RUNTIME_INJECTED: "runtime_injected",
        F_AMBIENT: "ambient",
        F_TEST_ONLY: "test_only",
        F_REVIEW_REQUIRED: "review_required",
        F_DECLARED_UNUSED: "declared_unused",
        F_DECLARED_NON_USER: "declared_non_user",
        F_DECLARED_INDIRECT: "declared_indirect",
    }.get(code, "unknown")


# ---------------------------------------------------------------------------
# Public entry: profile-driven severity + backward-compatible issue shape
# ---------------------------------------------------------------------------

def check_env_declarations(skill_dir: Path, declared: set,
                           profile: dict | None = None) -> dict:
    """Full classified check. Returns:

    {
      "issues":   [profile-visible issues, legacy shape + code/variable fields],
      "findings": [all findings incl. hidden, machine-readable],
      "evidence": [hidden/non-blocking classified records],
      "contracts_source": "env_contracts.json" | "legacy-fallback",
    }
    """
    profile = profile or {}
    # Per-code severity from profile; legacy declaration_vs_code key still
    # honored for ENV_REQUIRED_UNDECLARED when env_severity is absent.
    per_code = profile.get("env_severity") or {}
    legacy = (profile or {}).get("declaration_vs_code", "WARN")
    if legacy and legacy.upper() == "OFF":
        per_code = {**per_code, F_REQUIRED_UNDECLARED: "OFF",
                    F_DECLARED_UNUSED: "OFF", F_DECLARED_NON_USER: "OFF"}

    contracts = _load_env_contracts()
    records = extract_env_records(skill_dir)
    findings, evidence = _classify(records, declared, contracts)

    # Apply profile severity; None severity → hidden from issues (JSON only)
    visible = []
    for fd in findings:
        code = fd["code"]
        sev = per_code.get(code, DEFAULT_SEVERITY.get(code))
        if sev is None or (isinstance(sev, str) and sev.upper() == "OFF"):
            continue
        fd = dict(fd)
        fd["severity"] = sev.upper()
        visible.append(fd)

    # Backward-compatible issue shape (healthcheck printer expects
    # file/line/message/severity) — message built by caller via i18n.
    issues = [{
        "file": fd["file"],
        "line": fd.get("line"),
        "severity": fd["severity"],
        "code": fd["code"],
        "variable": fd["variable"],
        "access": fd.get("access", ""),
        "reason": fd.get("reason", ""),
    } for fd in visible]

    return {
        "issues": issues,
        "findings": findings,
        "evidence": evidence,
        "contracts_source": contracts["source"],
    }
