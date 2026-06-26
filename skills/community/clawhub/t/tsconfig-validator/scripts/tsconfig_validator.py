#!/usr/bin/env python3
"""TSConfig Validator — lint, validate, and audit tsconfig.json files.

Pure Python stdlib. No dependencies.
"""
import sys, os, re, json, argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Known compiler options
# ---------------------------------------------------------------------------

KNOWN_COMPILER_OPTIONS = {
    'target', 'module', 'lib', 'outDir', 'rootDir', 'strict',
    'esModuleInterop', 'skipLibCheck', 'forceConsistentCasingInFileNames',
    'resolveJsonModule', 'declaration', 'declarationMap', 'sourceMap',
    'incremental', 'tsBuildInfoFile', 'composite', 'noEmit', 'jsx',
    'jsxFactory', 'jsxFragmentFactory', 'moduleResolution', 'baseUrl',
    'paths', 'rootDirs', 'typeRoots', 'types', 'allowJs', 'checkJs',
    'maxNodeModuleJsDepth', 'noImplicitAny', 'strictNullChecks',
    'strictFunctionTypes', 'strictBindCallApply',
    'strictPropertyInitialization', 'noImplicitThis', 'alwaysStrict',
    'noUnusedLocals', 'noUnusedParameters', 'noImplicitReturns',
    'noFallthroughCasesInSwitch', 'noUncheckedIndexedAccess',
    'noPropertyAccessFromIndexSignature', 'allowSyntheticDefaultImports',
    'emitDecoratorMetadata', 'experimentalDecorators', 'isolatedModules',
    'preserveConstEnums', 'allowImportingTsExtensions', 'noEmitOnError',
    'removeComments', 'outFile', 'downlevelIteration', 'importHelpers',
    'verbatimModuleSyntax', 'moduleDetection', 'allowArbitraryExtensions',
    'customConditions', 'useDefineForClassFields',
    'exactOptionalPropertyTypes',
}

KNOWN_TOP_LEVEL_KEYS = {
    'compilerOptions', 'include', 'exclude', 'files', 'extends',
    'references', 'watchOptions', 'typeAcquisition', 'buildOptions',
    'ts-node',
}

OUTDATED_TARGETS = {'es3', 'es5', 'es2015', 'es6'}


# ---------------------------------------------------------------------------
# Comment stripping
# ---------------------------------------------------------------------------

def strip_json_comments(text):
    """Strip // and /* */ comments from JSON text (tsconfig allows them)."""
    result = []
    i = 0
    n = len(text)
    in_string = False
    escape = False

    while i < n:
        c = text[i]

        if in_string:
            result.append(c)
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                in_string = False
            i += 1
            continue

        # not in string
        if c == '"':
            in_string = True
            result.append(c)
            i += 1
        elif c == '/' and i + 1 < n and text[i + 1] == '/':
            # line comment — skip to end of line
            i += 2
            while i < n and text[i] != '\n':
                i += 1
        elif c == '/' and i + 1 < n and text[i + 1] == '*':
            # block comment — skip to */
            i += 2
            while i + 1 < n and not (text[i] == '*' and text[i + 1] == '/'):
                i += 1
            i += 2  # skip */
        else:
            result.append(c)
            i += 1

    return ''.join(result)


# ---------------------------------------------------------------------------
# Trailing comma stripping
# ---------------------------------------------------------------------------

def strip_trailing_commas(text):
    """Strip trailing commas before } or ] (common in tsconfig)."""
    return re.sub(r',\s*([}\]])', r'\1', text)


# ---------------------------------------------------------------------------
# Issue model
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, rule, severity, message, line=0):
        self.rule = rule
        self.severity = severity  # error, warning, info
        self.message = message
        self.line = line

    def to_dict(self):
        return {
            'rule': self.rule,
            'severity': self.severity,
            'message': self.message,
            'line': self.line,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_line(lines, pattern, start=0):
    """Find line number (1-based) containing pattern."""
    for i in range(start, len(lines)):
        if pattern in lines[i]:
            return i + 1
    return 0


def get_opt(compiler_options, key, default=None):
    """Get a compiler option value, case-sensitive."""
    return compiler_options.get(key, default)


# ---------------------------------------------------------------------------
# Structure rules (1-5)
# ---------------------------------------------------------------------------

def lint_structure(config, lines, raw_text):
    """Check structural validity."""
    issues = []

    # Rule 3: empty-config — no compilerOptions
    if 'compilerOptions' not in config or not config['compilerOptions']:
        issues.append(Issue('empty-config', 'warning',
            'tsconfig has no `compilerOptions` — using all defaults',
            1))

    # Rule 2: unknown-compiler-option
    co = config.get('compilerOptions', {})
    if isinstance(co, dict):
        for key in co:
            if key not in KNOWN_COMPILER_OPTIONS:
                issues.append(Issue('unknown-compiler-option', 'warning',
                    f'Unknown compilerOption: `{key}`',
                    find_line(lines, f'"{key}"') or 1))

    # Rule 4: missing-include — no include or files
    if 'include' not in config and 'files' not in config:
        issues.append(Issue('missing-include', 'info',
            'No `include` or `files` specified — TypeScript will include all .ts files',
            1))

    # Rule 5: conflicting-include-exclude
    include = config.get('include', [])
    exclude = config.get('exclude', [])
    if isinstance(include, list) and isinstance(exclude, list):
        overlap = set(include) & set(exclude)
        for pat in overlap:
            issues.append(Issue('conflicting-include-exclude', 'warning',
                f'Pattern `{pat}` appears in both `include` and `exclude`',
                find_line(lines, pat) or 1))

    return issues


# ---------------------------------------------------------------------------
# Strictness rules (6-11)
# ---------------------------------------------------------------------------

def lint_strictness(config, lines):
    """Check strictness-related options."""
    issues = []
    co = config.get('compilerOptions', {})
    if not isinstance(co, dict):
        co = {}

    strict = get_opt(co, 'strict')

    # Rule 6: strict-not-enabled
    if strict is not True:
        issues.append(Issue('strict-not-enabled', 'warning',
            '`strict` is not enabled — consider setting `"strict": true`',
            find_line(lines, '"compilerOptions"') or 1))

    # Rule 7: no-implicit-any
    if get_opt(co, 'noImplicitAny') is False:
        issues.append(Issue('no-implicit-any', 'warning',
            '`noImplicitAny` is explicitly set to false — implicit any types reduce safety',
            find_line(lines, '"noImplicitAny"') or 1))

    # Rule 8: strict-null-checks
    if get_opt(co, 'strictNullChecks') is False:
        issues.append(Issue('strict-null-checks', 'warning',
            '`strictNullChecks` is explicitly set to false — null errors will be missed',
            find_line(lines, '"strictNullChecks"') or 1))

    # Rule 9: no-unchecked-indexed
    if get_opt(co, 'noUncheckedIndexedAccess') is not True:
        issues.append(Issue('no-unchecked-indexed', 'info',
            '`noUncheckedIndexedAccess` not enabled — index access returns T instead of T|undefined',
            find_line(lines, '"compilerOptions"') or 1))

    # Rule 10: no-unused-locals
    if get_opt(co, 'noUnusedLocals') is not True:
        issues.append(Issue('no-unused-locals', 'info',
            '`noUnusedLocals` not enabled — unused variables will not cause errors',
            find_line(lines, '"compilerOptions"') or 1))

    # Rule 11: no-unused-params
    if get_opt(co, 'noUnusedParameters') is not True:
        issues.append(Issue('no-unused-params', 'info',
            '`noUnusedParameters` not enabled — unused parameters will not cause errors',
            find_line(lines, '"compilerOptions"') or 1))

    return issues


# ---------------------------------------------------------------------------
# Compatibility rules (12-16)
# ---------------------------------------------------------------------------

def lint_compat(config, lines):
    """Check target/module compatibility."""
    issues = []
    co = config.get('compilerOptions', {})
    if not isinstance(co, dict):
        co = {}

    target = get_opt(co, 'target', '')
    module_val = get_opt(co, 'module', '')
    module_res = get_opt(co, 'moduleResolution', '')
    jsx = get_opt(co, 'jsx')

    if isinstance(target, str):
        target_lower = target.lower()
    else:
        target_lower = ''

    if isinstance(module_val, str):
        module_lower = module_val.lower()
    else:
        module_lower = ''

    if isinstance(module_res, str):
        module_res_lower = module_res.lower()
    else:
        module_res_lower = ''

    # Rule 12: outdated-target
    if target_lower in OUTDATED_TARGETS:
        issues.append(Issue('outdated-target', 'warning',
            f'Target `{target}` is outdated — consider ES2020 or newer',
            find_line(lines, '"target"') or 1))

    # Rule 13: module-target-mismatch
    if module_lower == 'commonjs' and target_lower in ('esnext', 'es2022', 'es2023', 'es2024'):
        issues.append(Issue('module-target-mismatch', 'warning',
            f'Module `{module_val}` with target `{target}` is unusual — ESNext target typically pairs with ESNext/NodeNext module',
            find_line(lines, '"module"') or 1))
    if module_lower in ('esnext', 'es2022') and target_lower in ('es5', 'es3', 'es2015', 'es6'):
        issues.append(Issue('module-target-mismatch', 'warning',
            f'Module `{module_val}` with target `{target}` is mismatched — modern module system with legacy target',
            find_line(lines, '"module"') or 1))

    # Rule 14: jsx-without-react
    if jsx and isinstance(jsx, str):
        jsx_lower = jsx.lower()
        if jsx_lower in ('react', 'react-jsx', 'react-jsxdev'):
            has_react_setting = (
                get_opt(co, 'jsxFactory') is not None or
                get_opt(co, 'jsxFragmentFactory') is not None or
                jsx_lower in ('react-jsx', 'react-jsxdev')  # these are self-contained
            )
            if jsx_lower == 'react' and not get_opt(co, 'jsxFactory'):
                # classic jsx transform without explicit factory is fine (default React.createElement)
                pass

    # Rule 15: node-module-resolution
    if module_res_lower == 'node':
        issues.append(Issue('node-module-resolution', 'info',
            '`moduleResolution: "node"` is legacy — consider `node16`, `nodenext`, or `bundler`',
            find_line(lines, '"moduleResolution"') or 1))

    # Rule 16: es-interop
    if get_opt(co, 'esModuleInterop') is not True:
        issues.append(Issue('es-interop', 'warning',
            '`esModuleInterop` not enabled — may cause issues with CommonJS default imports',
            find_line(lines, '"compilerOptions"') or 1))

    return issues


# ---------------------------------------------------------------------------
# Best practices rules (17-22)
# ---------------------------------------------------------------------------

def lint_best_practices(config, lines):
    """Check best practices."""
    issues = []
    co = config.get('compilerOptions', {})
    if not isinstance(co, dict):
        co = {}

    # Rule 17: missing-outdir
    if get_opt(co, 'outDir') is None and get_opt(co, 'noEmit') is not True:
        issues.append(Issue('missing-outdir', 'info',
            '`outDir` not set — compiled .js files will be placed next to source .ts files',
            find_line(lines, '"compilerOptions"') or 1))

    # Rule 18: missing-rootdir
    if get_opt(co, 'rootDir') is None and get_opt(co, 'noEmit') is not True:
        issues.append(Issue('missing-rootdir', 'info',
            '`rootDir` not set — output directory structure may be unstable',
            find_line(lines, '"compilerOptions"') or 1))

    # Rule 19: skip-lib-check
    if get_opt(co, 'skipLibCheck') is not True:
        issues.append(Issue('skip-lib-check', 'info',
            '`skipLibCheck` not enabled — type-checking .d.ts files slows compilation',
            find_line(lines, '"compilerOptions"') or 1))

    # Rule 20: source-map-in-prod
    if get_opt(co, 'sourceMap') is True and get_opt(co, 'declaration') is not True:
        issues.append(Issue('source-map-in-prod', 'info',
            '`sourceMap` is true but `declaration` is false — source maps without declarations may leak source in production',
            find_line(lines, '"sourceMap"') or 1))

    # Rule 21: incremental-not-enabled
    if get_opt(co, 'incremental') is not True and get_opt(co, 'composite') is not True:
        issues.append(Issue('incremental-not-enabled', 'info',
            '`incremental` not enabled — builds will be slower without caching',
            find_line(lines, '"compilerOptions"') or 1))

    # Rule 22: paths-without-baseurl
    if get_opt(co, 'paths') is not None and get_opt(co, 'baseUrl') is None:
        issues.append(Issue('paths-without-baseurl', 'error',
            '`paths` is defined but `baseUrl` is not set — path mappings require `baseUrl`',
            find_line(lines, '"paths"') or 1))

    return issues


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def lint_file(filepath, rules='all'):
    """Lint a single tsconfig.json file. Returns list of Issues."""
    raw = Path(filepath).read_text(encoding='utf-8', errors='replace')
    lines = raw.splitlines()

    # Strip comments and trailing commas, then parse
    cleaned = strip_json_comments(raw)
    cleaned = strip_trailing_commas(cleaned)

    try:
        config = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return [Issue('invalid-json', 'error', f'Invalid JSON: {e}', 1)]

    if not isinstance(config, dict):
        return [Issue('invalid-json', 'error', 'tsconfig root is not an object', 1)]

    issues = []
    if rules in ('all', 'structure', 'validate'):
        issues.extend(lint_structure(config, lines, raw))
    if rules in ('all', 'strictness', 'strict'):
        issues.extend(lint_strictness(config, lines))
    if rules in ('all', 'compat'):
        issues.extend(lint_compat(config, lines))
    if rules in ('all', 'practices'):
        issues.extend(lint_best_practices(config, lines))

    return issues


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def format_text(filepath, issues):
    lines = []
    for iss in sorted(issues, key=lambda x: x.line):
        lines.append(f'{filepath}:{iss.line} {iss.severity} [{iss.rule}] {iss.message}')
    return '\n'.join(lines)


def format_json(filepath, issues):
    return json.dumps({
        'file': str(filepath),
        'issues': [i.to_dict() for i in issues],
        'summary': {
            'errors': sum(1 for i in issues if i.severity == 'error'),
            'warnings': sum(1 for i in issues if i.severity == 'warning'),
            'info': sum(1 for i in issues if i.severity == 'info'),
        }
    }, indent=2)


def format_markdown(filepath, issues):
    lines = [f'## {filepath}', '', '| Severity | Rule | Line | Message |',
             '|----------|------|------|---------|']
    for iss in sorted(issues, key=lambda x: x.line):
        sev = {'error': 'ERROR', 'warning': 'WARN', 'info': 'INFO'}.get(iss.severity, iss.severity)
        lines.append(f'| {sev} | `{iss.rule}` | {iss.line} | {iss.message} |')
    errs = sum(1 for i in issues if i.severity == 'error')
    warns = sum(1 for i in issues if i.severity == 'warning')
    infos = sum(1 for i in issues if i.severity == 'info')
    lines.append(f'\n**{len(issues)} issues** ({errs} errors, {warns} warnings, {infos} info)')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='TSConfig Validator')
    sub = parser.add_subparsers(dest='command', required=True)

    # lint
    p_lint = sub.add_parser('lint', help='Run all lint rules')
    p_lint.add_argument('path', help='tsconfig.json file')
    p_lint.add_argument('--strict', action='store_true', help='Exit 1 on warnings too')
    p_lint.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # strict
    p_strict = sub.add_parser('strict', help='Check strictness-related options')
    p_strict.add_argument('path', help='tsconfig.json file')
    p_strict.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # compat
    p_compat = sub.add_parser('compat', help='Check target/module compatibility')
    p_compat.add_argument('path', help='tsconfig.json file')
    p_compat.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # validate
    p_val = sub.add_parser('validate', help='Structural validation')
    p_val.add_argument('path', help='tsconfig.json file')
    p_val.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    args = parser.parse_args()

    rule_map = {
        'lint': 'all',
        'strict': 'strict',
        'compat': 'compat',
        'validate': 'validate',
    }
    rules = rule_map[args.command]

    filepath = args.path
    if not Path(filepath).is_file():
        print(f'File not found: {filepath}', file=sys.stderr)
        sys.exit(1)

    fmt = getattr(args, 'format', 'text')
    strict_mode = getattr(args, 'strict', False)

    issues = lint_file(filepath, rules)
    errs = sum(1 for i in issues if i.severity == 'error')
    warns = sum(1 for i in issues if i.severity == 'warning')
    infos = sum(1 for i in issues if i.severity == 'info')

    if fmt == 'text':
        if issues:
            print(format_text(filepath, issues))
        total = errs + warns + infos
        print(f'\n{total} issues ({errs} errors, {warns} warnings, {infos} info)')
    elif fmt == 'json':
        print(format_json(filepath, issues))
    elif fmt == 'markdown':
        if issues:
            print(format_markdown(filepath, issues))

    if errs > 0:
        sys.exit(1)
    if strict_mode and warns > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
