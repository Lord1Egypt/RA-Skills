#!/usr/bin/env python3
"""
Quick validation script for skills — structured output with PASS/FAIL/SKIP.

Usage:
   python quick_validate.py <skill_directory>

Output:
   {
     "valid": true/false,
     "checks":  [{item: str, status: PASS|FAIL|SKIP, detail: str}],
     "suggestions": [str]
   }

- FAIL items → fix before proceeding.
- SKIP items → expected for some skill types, not an error.
- suggestions → discuss with the user; some are optional.
- Checks are signals to review, not mandates — not every check applies
  to every architecture. When in doubt, ask the user.
"""

import sys
import re
import os
import stat
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required but not installed.")
    print("Install it with: pip install pyyaml")
    sys.exit(1)

# ── Helpers ──────────────────────────────────────────────

def _clean_code_blocks(text):
    return re.sub(r'```[\s\S]*?```', '', text)

def _extract_body(content, frontmatter_end):
    """Return the markdown body (after frontmatter), stripped of leading blank lines."""
    body = content[frontmatter_end:].lstrip('\n')
    return body

def _body_line_count(body):
    """Count meaningful lines in the body (exclude empty lines)."""
    lines = [l for l in body.split('\n') if l.strip()]
    return len(lines)

def _find_bundled_files(skill_path):
    """Return {dir: [filenames]} for scripts/, references/, assets/."""
    result = {}
    for d in ('scripts', 'references', 'assets'):
        p = skill_path / d
        if p.is_dir():
            files = [f.name for f in p.iterdir() if f.is_file() and not f.name.startswith('__')]
            result[d] = files
        else:
            result[d] = []
    return result

def _extract_refs_from_content(content, clean_code=True):
    """Extract all bundled resource paths referenced in SKILL.md.
    Set clean_code=False to include references inside code blocks (e.g., bash commands)."""
    if clean_code:
        content = _clean_code_blocks(content)
    refs = set()
    # Markdown links
    for m in re.finditer(r'\[([^\]]*)\]\(([^\)]+)\)', content):
        path = m.group(2).split('#')[0].split('?')[0].strip()
        path = re.sub(r'^\./', '', path)
        if path.startswith(('scripts/', 'references/', 'assets/')):
            refs.add(path)
    # Inline backtick (skip triple-backtick code fences via lookahead/lookbehind)
    for m in re.finditer(r'(?<!`)`([^`]+)`(?!`)', content):
        parts = m.group(1).strip().split()
        if not parts:
            continue
        path = parts[0]
        if path.startswith(('scripts/', 'references/', 'assets/')):
            refs.add(path)
    # Fenced code blocks (bash/python commands often reference bundled resources)
    for m in re.finditer(r'```[a-z]*\n(.*?)```', content, re.DOTALL):
        for line in m.group(1).split('\n'):
            line = line.strip()
            if line.startswith(('scripts/', 'references/', 'assets/')):
                parts = line.split()
                if parts:
                    refs.add(parts[0])
    return refs

# ── Checks ───────────────────────────────────────────────

def check_broken_references(skill_path, content):
    """Return list of unreachable bundled-resource references."""
    cleaned = _clean_code_blocks(content)
    bad = []
    checked = set()
    for m in re.finditer(r'\[([^\]]*)\]\(([^\)]+)\)', cleaned):
        path = m.group(2).split('#')[0].split('?')[0].strip()
        path = re.sub(r'^\./', '', path)
        if path.startswith(('scripts/', 'references/', 'assets/')):
            if path not in checked:
                checked.add(path)
                if not (skill_path / path).exists():
                    bad.append(path)
    for m in re.finditer(r'(?<!`)`([^`]+)`(?!`)', cleaned):
        parts = m.group(1).strip().split()
        if not parts:
            continue
        path = parts[0]
        if path.startswith(('scripts/', 'references/', 'assets/')):
            if path not in checked:
                checked.add(path)
                if not (skill_path / path).exists():
                    bad.append(path)
    return bad

# ── Main validation ──────────────────────────────────────

def validate_skill(skill_path):
    """Run all checks. Returns {valid, checks, suggestions}."""
    skill_path = Path(skill_path).resolve()
    checks = []
    suggestions = []

    # ── 1. SKILL.md existence ──
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return {"valid": False,
                "checks": [{"item": "SKILL.md exists", "status": "FAIL"}],
                "suggestions": []}
    checks.append({"item": "SKILL.md exists", "status": "PASS"})

    content = skill_md.read_text(encoding='utf-8')

    # ── 2. Frontmatter ──
    if not content.startswith('---'):
        return {"valid": False,
                "checks": checks + [{"item": "Frontmatter: YAML format", "status": "FAIL"}],
                "suggestions": []}
    checks.append({"item": "Frontmatter: YAML format", "status": "PASS"})

    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        checks.append({"item": "Frontmatter: parseable", "status": "FAIL"})
        return _build_result(checks, [])
    checks.append({"item": "Frontmatter: parseable", "status": "PASS"})

    try:
        fm = yaml.safe_load(fm_match.group(1))
        if not isinstance(fm, dict):
            checks.append({"item": "Frontmatter: YAML dict", "status": "FAIL"})
            return _build_result(checks, [])
    except yaml.YAMLError as e:
        checks.append({"item": "Frontmatter: YAML dict", "status": "FAIL",
                       "detail": str(e)})
        return _build_result(checks, [])

    # Allowed properties
    ALLOWED = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}
    unexpected = set(fm.keys()) - ALLOWED
    if unexpected:
        checks.append({"item": "Frontmatter: allowed keys", "status": "FAIL",
                       "detail": f"unexpected: {', '.join(sorted(unexpected))}"})
    else:
        checks.append({"item": "Frontmatter: allowed keys", "status": "PASS"})

    # name
    name = fm.get('name', '')
    if not isinstance(name, str):
        checks.append({"item": "Frontmatter: name (string)", "status": "FAIL"})
        return _build_result(checks, [])
    name = name.strip()
    if not name:
        checks.append({"item": "Frontmatter: name (present)", "status": "FAIL"})
        return _build_result(checks, [])
    checks.append({"item": "Frontmatter: name (present)", "status": "PASS", "detail": name})

    if not re.match(r'^[a-z0-9-]+$', name):
        checks.append({"item": "Frontmatter: name (kebab-case)", "status": "FAIL",
                       "detail": name})
    elif name.startswith('-') or name.endswith('-') or '--' in name:
        checks.append({"item": "Frontmatter: name (no bad hyphens)", "status": "FAIL",
                       "detail": name})
    elif len(name) > 64:
        checks.append({"item": "Frontmatter: name (≤64 chars)", "status": "FAIL",
                       "detail": f"{len(name)} chars"})
    else:
        checks.append({"item": "Frontmatter: name (format)", "status": "PASS", "detail": name})

    if skill_path.name != name:
        checks.append({"item": "Frontmatter: name matches directory", "status": "FAIL",
                       "detail": f"dir={skill_path.name}, name={name}"})
    else:
        checks.append({"item": "Frontmatter: name matches directory", "status": "PASS"})

    # description
    desc = fm.get('description', '')
    if not isinstance(desc, str):
        checks.append({"item": "Frontmatter: description (string)", "status": "FAIL"})
        return _build_result(checks, [])
    desc = desc.strip()
    if not desc:
        checks.append({"item": "Frontmatter: description (present)", "status": "FAIL"})
    else:
        desc_check = "PASS" if len(desc) <= 1024 else "FAIL"
        detail = f"{len(desc)} chars"
        if 'use when' in desc.lower():
            detail += ", includes 'Use when'"
        else:
            detail += ", missing 'Use when'"
        checks.append({"item": "Frontmatter: description (≤1024 + 'Use when')",
                       "status": desc_check, "detail": detail})

    if '<' in desc or '>' in desc:
        checks.append({"item": "Frontmatter: description (no <>)", "status": "FAIL"})
    else:
        checks.append({"item": "Frontmatter: description (no <>)", "status": "PASS"})

    # compatibility (optional)
    compat = fm.get('compatibility', '')
    if compat:
        if isinstance(compat, str) and len(compat) <= 500:
            checks.append({"item": "Frontmatter: compatibility (≤500)", "status": "PASS"})
        else:
            checks.append({"item": "Frontmatter: compatibility (≤500)", "status": "FAIL"})
    else:
        checks.append({"item": "Frontmatter: compatibility (≤500)", "status": "SKIP",
                       "detail": "not set"})

    # ── 3. Body checks (extract body after frontmatter) ──
    body = _extract_body(content, fm_match.end())
    cleaned = _clean_code_blocks(content)
    line_count = _body_line_count(body)

    if line_count <= 500:
        checks.append({"item": "Body: ≤ 500 lines", "status": "PASS",
                       "detail": f"{line_count}/500"})
    else:
        checks.append({"item": "Body: ≤ 500 lines", "status": "FAIL",
                       "detail": f"{line_count}/500"})
        suggestions.append("Split body into bundled resources (Progressive Disclosure)")

    # Pre-Step Rationalization Bias Check (replaces old rationalization table)
    if re.search(r'Pre-Step.*Bias.*Check', cleaned, re.IGNORECASE):
        checks.append({"item": "Body: Pre-Step Bias Check", "status": "PASS"})
    else:
        checks.append({"item": "Body: Pre-Step Bias Check", "status": "FAIL",
                       "detail": "not detected"})
        suggestions.append("Add a Pre-Step Rationalization Bias Check to the Workflows section — 3 self-checks: Re-read, Follow references, Check completion")

    # workflow numbering
    wf_match = re.search(r'## [^#\n]*[Ww]orkflow', cleaned)
    if wf_match:
        rest = cleaned[wf_match.start():]
        section = re.search(r'(## [^#\n]*[Ww]orkflow.*?)(?=\n## |\Z)', rest, re.DOTALL)
        if section and (re.search(r'\n\d+\.', section.group(1)) or
                        re.search(r'###.*[Pp]hase\s+\d+', section.group(1)) or
                        re.search(r'#+\s*[Ss]tep\s+\d+', section.group(1))):
            checks.append({"item": "Workflow: numbered steps", "status": "PASS",
                           "detail": "Phase/Step/numbered pattern"})
        else:
            checks.append({"item": "Workflow: numbered steps", "status": "FAIL",
                           "detail": "no numbering detected"})
    else:
        checks.append({"item": "Workflow: numbered steps", "status": "SKIP",
                       "detail": "no workflow section"})

    # workflow overview
    if wf_match:
        rest = cleaned[wf_match.start():]
        section = re.search(r'(## [^#\n]*[Ww]orkflow.*?\n)(.*?)(?=\n###|\Z)', rest, re.DOTALL)
        if section:
            intro = section.group(2).strip()
            # intro exists if there's non-empty, non-heading, non-list-only text
            intro_lines = [l for l in intro.split('\n') if l.strip() and not l.strip().startswith(('-', '*', '#'))]
            if intro_lines:
                checks.append({"item": "Workflow: process overview", "status": "PASS"})
            else:
                checks.append({"item": "Workflow: process overview", "status": "FAIL",
                               "detail": "no intro paragraph before first sub-step"})
        else:
            checks.append({"item": "Workflow: process overview", "status": "FAIL"})
    else:
        checks.append({"item": "Workflow: process overview", "status": "SKIP",
                       "detail": "no workflow section"})

    # pseudocode
    if re.search(r'```[a-z]*\n', body):
        checks.append({"item": "Workflow: pseudocode/code examples", "status": "PASS"})
    else:
        checks.append({"item": "Workflow: pseudocode/code examples", "status": "SKIP",
                       "detail": "no code blocks — OK if simple workflow"})

    # checklist pattern
    if re.search(r'^- \[[ x]\] ', body, re.MULTILINE):
        checks.append({"item": "Workflow: checklist pattern", "status": "PASS"})
    else:
        checks.append({"item": "Workflow: checklist pattern", "status": "SKIP",
                       "detail": "not needed for simple workflows"})

    # ── 4. Resource checks ──
    bundled = _find_bundled_files(skill_path)
    content_refs = _extract_refs_from_content(content, clean_code=False)

    # broken references
    broken = check_broken_references(skill_path, content)
    if broken:
        checks.append({"item": "References: all valid", "status": "FAIL",
                       "detail": f"broken: {', '.join(broken)}"})
    else:
        checks.append({"item": "References: all valid", "status": "PASS"})

    # all bundled files are linked
    all_linked = True
    unlinked = []
    for dirname, files in bundled.items():
        for f in files:
            expected = f"{dirname}/{f}"
            if expected not in content_refs:
                all_linked = False
                unlinked.append(expected)
    if unlinked:
        checks.append({"item": "References: all linked from SKILL.md", "status": "FAIL",
                       "detail": f"unlinked: {', '.join(unlinked)}"})
    else:
        checks.append({"item": "References: all linked from SKILL.md", "status": "PASS",
                       "detail": f"{sum(len(v) for v in bundled.values())} files covered"})

    # reference depth ≤ 1 (strip trailing / to avoid false positive on dir refs)
    deep_refs = [r for r in content_refs if r.rstrip('/').count('/') > 1]
    if deep_refs:
        checks.append({"item": "References: depth ≤ 1 level", "status": "FAIL",
                       "detail": f"deep refs: {', '.join(deep_refs)}"})
    else:
        status = "SKIP" if not content_refs else "PASS"
        checks.append({"item": "References: depth ≤ 1 level", "status": status})

    # TOC for large reference files
    large_no_toc = []
    refs_dir = skill_path / 'references'
    if refs_dir.is_dir():
        for rf in refs_dir.glob('*.md'):
            try:
                rtext = rf.read_text(encoding='utf-8')
                rlines = len([l for l in rtext.split('\n') if l.strip()])
                if rlines > 300:
                    # check for TOC: heading + links or numbered list in first 50 lines
                    first_50 = '\n'.join(rtext.split('\n')[:50])
                    has_toc = bool(re.search(r'(?:Table of Contents|## Contents|^[-*]\s+\[.+\])', first_50, re.MULTILINE))
                    if not has_toc:
                        large_no_toc.append(rf.name)
            except Exception:
                pass
    if large_no_toc:
        checks.append({"item": "References: TOC for >300 line files", "status": "FAIL",
                       "detail": f"missing TOC: {', '.join(large_no_toc)}"})
    else:
        checks.append({"item": "References: TOC for >300 line files", "status": "SKIP",
                       "detail": "no large refs or all have TOC"})

    # scripts present
    script_files = bundled.get('scripts', [])
    if script_files:
        checks.append({"item": "Scripts: files present", "status": "PASS",
                       "detail": f"{len(script_files)} file(s)"})
    else:
        checks.append({"item": "Scripts: files present", "status": "SKIP",
                       "detail": "no scripts — OK if not needed"})

    # scripts executable (Linux/macOS only; skip on Windows)
    if script_files and os.name != 'nt':
        non_exec = []
        for sf in script_files:
            sp = skill_path / 'scripts' / sf
            if sf.endswith(('.py', '.sh')):
                try:
                    mode = sp.stat().st_mode
                    if not (mode & stat.S_IEXEC):
                        non_exec.append(sf)
                except Exception:
                    pass
        if non_exec:
            checks.append({"item": "Scripts: executable permissions", "status": "FAIL",
                           "detail": f"not +x: {', '.join(non_exec)}"})
        else:
            checks.append({"item": "Scripts: executable permissions", "status": "PASS"})
    else:
        checks.append({"item": "Scripts: executable permissions", "status": "SKIP"})

    # scripts syntax valid (py_compile check, no execution)
    if script_files:
        import py_compile
        syntax_errors = []
        for sf in script_files:
            if sf.endswith('.py'):
                try:
                    py_compile.compile(str(skill_path / 'scripts' / sf), doraise=True)
                except py_compile.PyCompileError as e:
                    syntax_errors.append(f"{sf}: {e}")
        if syntax_errors:
            checks.append({"item": "Scripts: syntax valid", "status": "FAIL",
                           "detail": "; ".join(syntax_errors)})
        else:
            checks.append({"item": "Scripts: syntax valid", "status": "PASS"})
    else:
        checks.append({"item": "Scripts: syntax valid", "status": "SKIP"})

    # assets purity (no .md in assets/)
    asset_files = bundled.get('assets', [])
    md_assets = [a for a in asset_files if a.endswith('.md')]
    if md_assets:
        checks.append({"item": "Assets: no .md files", "status": "FAIL",
                       "detail": f".md in assets/: {', '.join(md_assets)}"})
    else:
        checks.append({"item": "Assets: no .md files", "status": "PASS"})

    # ── 5. Optional tables (suggestions, not failures) ──
    has_gotchas = bool(re.search(r'\|.*ID.*Issue.*Symptom.*Fix.*\|', cleaned))
    if not has_gotchas:
        suggestions.append("Add a Gotchas/Guardrails table (| ID | Issue / Symptom | Fix |)")

    has_verification = bool(re.search(r'\|.*Check.*Evidence.*\|', cleaned))
    if not has_verification:
        suggestions.append("Add a Verification table (| Check | Evidence |)")

    # forbidden files
    forbidden = ['README.md', 'CHANGELOG.md', 'INSTALLATION_GUIDE.md']
    for f in forbidden:
        if (skill_path / f).exists():
            suggestions.append(f"Remove auxiliary file {f} — not needed for skills")

    # ── 6. Content hygiene ──
    # Developer artifact comments (// in markdown body, outside code blocks)
    dev_artifacts = re.findall(r'^\s*//.{5,}', body, re.MULTILINE)
    if dev_artifacts:
        checks.append({"item": "Body: no developer artifact comments (//...)",
                       "status": "FAIL",
                       "detail": f"{len(dev_artifacts)} line(s): {dev_artifacts[:3]}"})
    else:
        checks.append({"item": "Body: no developer artifact comments (//...)",
                       "status": "PASS"})

    # Common typos in skill content (outside code blocks)
    typo_patterns = {
        'Critial': 'Critical',
        'erros': 'errors',
        'verification able': 'verification table',
    }
    found_typos = []
    for typo, fix in typo_patterns.items():
        if re.search(r'\b' + re.escape(typo) + r'\b', cleaned):
            found_typos.append(f"'{typo}' → '{fix}'")
    if found_typos:
        checks.append({"item": "Body: common typos",
                       "status": "FAIL",
                       "detail": '; '.join(found_typos)})
    else:
        checks.append({"item": "Body: common typos", "status": "PASS"})

    return _build_result(checks, suggestions)

def _build_result(checks, suggestions):
    has_fail = any(c['status'] == 'FAIL' for c in checks)
    return {"valid": not has_fail, "checks": checks, "suggestions": suggestions}

# ── CLI ──────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    result = validate_skill(sys.argv[1])
    print(result)
