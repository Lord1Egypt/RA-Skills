#!/usr/bin/env python3
"""SWC Config Validator — validate .swcrc and package.json#swc files."""

import json
import os
import re
import sys
from pathlib import Path

VALID_TOP_KEYS = {
    "$schema", "jsc", "module", "minify", "env", "isModule", "sourceMaps",
    "inlineSourcesContent", "emitSourceMapColumns", "inputSourceMap",
    "test", "exclude", "filename",
}

VALID_PARSER_SYNTAX = {"ecmascript", "typescript"}

VALID_TARGETS = {
    "es3", "es5",
    "es2015", "es2016", "es2017", "es2018", "es2019", "es2020",
    "es2021", "es2022", "es2023", "es2024",
    "esnext",
}

VALID_MODULE_TYPES = {
    "es6", "commonjs", "umd", "amd", "nodenext", "systemjs",
}

ESM_ONLY_FEATURES = {
    "importMeta", "dynamicImport", "staticBlocks",
}


def load_config(filepath):
    path = Path(filepath)
    if not path.exists():
        return None, f"File not found: {filepath}"
    try:
        text = path.read_text(encoding="utf-8").strip()
    except Exception as e:
        return None, f"Cannot read file: {e}"
    if not text:
        return None, "File is empty"

    if path.name == "package.json":
        try:
            pkg = json.loads(text)
            if "swc" not in pkg:
                return None, "No 'swc' key in package.json"
            return pkg["swc"], None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"
    else:
        # Try plain JSON first (avoids mangling URLs/strings that contain //)
        try:
            return json.loads(text), None
        except json.JSONDecodeError:
            pass
        # Fallback: strip JS-style comments (common in .swcrc authored by humans)
        # Only strip // outside quoted strings by using a state-machine approach
        comment_re = re.compile(r'("(?:[^"\\]|\\.)*")|//[^\n]*|(/\*.*?\*/)',
                                re.DOTALL)
        def _strip(m):
            if m.group(1):   # inside a quoted string — keep as-is
                return m.group(1)
            return ""        # comment — remove
        cleaned = comment_re.sub(_strip, text)
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)
        try:
            return json.loads(cleaned), None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"


class Finding:
    def __init__(self, rule_id, severity, message, detail=None):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.detail = detail

    def to_dict(self):
        d = {"rule": self.rule_id, "severity": self.severity, "message": self.message}
        if self.detail:
            d["detail"] = self.detail
        return d

    def to_text(self):
        icon = "❌" if self.severity == "error" else ("⚠️" if self.severity == "warning" else "ℹ️")
        s = f"{icon} [{self.rule_id}] {self.message}"
        if self.detail:
            s += f"\n   → {self.detail}"
        return s


def validate(config, filepath):
    findings = []

    # ── Structure rules ──────────────────────────────────────────────────────

    # S4: Unknown top-level keys
    unknown = set(config.keys()) - VALID_TOP_KEYS
    if unknown:
        findings.append(Finding("S4", "warning",
            f"Unknown top-level keys: {', '.join(sorted(unknown))}",
            f"Valid keys: {', '.join(sorted(VALID_TOP_KEYS))}"))

    # S5: Missing jsc key
    if "jsc" not in config:
        findings.append(Finding("S5", "warning",
            "Missing 'jsc' key",
            "Most SWC configs need 'jsc' to configure the parser, transform, and compilation target"))

    # ── JSC Config rules ─────────────────────────────────────────────────────

    jsc = config.get("jsc")
    if isinstance(jsc, dict):
        parser = jsc.get("parser", {})
        if isinstance(parser, dict):
            syntax = parser.get("syntax")

            # J1: Invalid parser syntax
            if syntax is not None and syntax not in VALID_PARSER_SYNTAX:
                findings.append(Finding("J1", "error",
                    f"Invalid parser syntax: '{syntax}'",
                    f"Must be one of: {', '.join(sorted(VALID_PARSER_SYNTAX))}"))

            # J2: JSX enabled without React transform
            jsx_enabled = parser.get("jsx", False)
            transform = jsc.get("transform", {})
            react_transform = isinstance(transform, dict) and "react" in transform
            if jsx_enabled and not react_transform:
                findings.append(Finding("J2", "warning",
                    "JSX enabled in parser but no jsc.transform.react configured",
                    "Add jsc.transform.react (e.g. { runtime: 'automatic' }) to handle JSX output"))

            # T1: React transform without parser.jsx enabled (cross-rule, placed here for context)
            if react_transform and not jsx_enabled:
                findings.append(Finding("T1", "error",
                    "jsc.transform.react is configured but parser.jsx is not enabled",
                    "Set parser.jsx: true to enable JSX parsing"))

        # J3: Deprecated loose mode in jsc.transform
        transform = jsc.get("transform", {})
        if isinstance(transform, dict):
            loose = transform.get("loose")
            if loose is True:
                findings.append(Finding("J3", "warning",
                    "Deprecated loose mode in jsc.transform",
                    "loose mode may produce spec-non-compliant output; prefer explicit assumption flags instead"))

            # T2: Legacy decorators without decoratorsBeforeExport
            decorator_version = transform.get("decoratorVersion")
            legacy_decorators = transform.get("legacyDecorator", False)
            decorators_before_export = transform.get("decoratorsBeforeExport")
            if legacy_decorators and decorators_before_export is None:
                findings.append(Finding("T2", "warning",
                    "Legacy decorators enabled without decoratorsBeforeExport",
                    "Set jsc.transform.decoratorsBeforeExport: true or false to avoid ambiguity"))

            # T3: Conflicting useDefineForClassFields
            use_define = jsc.get("transform", {}).get("useDefineForClassFields")
            exper = jsc.get("externalHelpers")
            if use_define is False and isinstance(parser, dict) and parser.get("syntax") == "typescript":
                findings.append(Finding("T3", "warning",
                    "useDefineForClassFields: false with TypeScript parser",
                    "TypeScript class fields default to define semantics; setting false can break TS behaviour"))

            # T4: Deprecated constModules
            const_modules = jsc.get("experimental", {})
            if isinstance(const_modules, dict) and "constModules" in const_modules:
                findings.append(Finding("T4", "warning",
                    "Deprecated constModules in jsc.experimental",
                    "constModules is no longer recommended; use explicit imports instead"))

        # J4: Missing target
        target = jsc.get("target")
        if target is None:
            findings.append(Finding("J4", "warning",
                "No compilation target specified (jsc.target is missing)",
                "Add jsc.target (e.g. 'es2017') to control output syntax level"))

        # J5: Invalid target value
        elif isinstance(target, str) and target.lower() not in VALID_TARGETS:
            findings.append(Finding("J5", "error",
                f"Invalid jsc.target: '{target}'",
                f"Must be one of: {', '.join(sorted(VALID_TARGETS))}"))

    elif jsc is not None:
        findings.append(Finding("J1", "error",
            "jsc must be an object, got " + type(jsc).__name__))

    # ── Module rules ─────────────────────────────────────────────────────────

    module_config = config.get("module")
    module_type = None
    if isinstance(module_config, dict):
        module_type = module_config.get("type")

        # M1: Unknown module type
        if module_type is not None and module_type not in VALID_MODULE_TYPES:
            findings.append(Finding("M1", "error",
                f"Unknown module type: '{module_type}'",
                f"Must be one of: {', '.join(sorted(VALID_MODULE_TYPES))}"))

        # M2: modules: false equivalent without bundler context (isModule: false)
        is_module = config.get("isModule")
        if is_module is False and module_type in ("es6", "nodenext"):
            findings.append(Finding("M2", "warning",
                f"isModule: false with module type '{module_type}'",
                "isModule: false tells SWC the input is a script, not an ES module — this conflicts with ESM output"))

        # M3: CommonJS module with ESM-only features
        if module_type == "commonjs" and isinstance(jsc, dict):
            parser = jsc.get("parser", {})
            if isinstance(parser, dict):
                for feat in ESM_ONLY_FEATURES:
                    if parser.get(feat, False):
                        findings.append(Finding("M3", "warning",
                            f"CommonJS module with ESM-only parser feature: {feat}",
                            "ESM-only features may not work correctly when outputting CommonJS"))
                        break

    # ── Transform rules (cross-file, not in jsc block) ───────────────────────

    # T2 / T3 / T4 already handled above inside jsc block

    # ── Minification rules ───────────────────────────────────────────────────

    minify = config.get("minify")
    jsc_minify = isinstance(jsc, dict) and jsc.get("minify")

    if minify or jsc_minify:
        minify_config = jsc_minify if isinstance(jsc_minify, dict) else {}

        compress = minify_config.get("compress", True)
        mangle = minify_config.get("mangle", True)
        dead_code = minify_config.get("deadCode", False)

        # N1: Minification enabled with compress: false
        if minify and compress is False:
            findings.append(Finding("N1", "warning",
                "Minification enabled but jsc.minify.compress is false",
                "compress: false skips dead-code elimination and expression simplification"))

        # N2: Mangle enabled without compress
        if mangle and compress is False:
            findings.append(Finding("N2", "warning",
                "jsc.minify.mangle enabled without compress",
                "Mangling identifiers without compressing may produce hard-to-debug output with no size benefit"))

        # N3: Drop console in development config
        compress_opts = minify_config.get("compress")
        if isinstance(compress_opts, dict):
            drop_console = compress_opts.get("drop_console", False)
            env_section = config.get("env", {})
            dev_config = isinstance(env_section, dict) and "development" in env_section
            if drop_console and dev_config:
                findings.append(Finding("N3", "warning",
                    "drop_console enabled in a config that also has a development env section",
                    "Dropping console statements in development makes debugging much harder"))

    # ── Best practices ───────────────────────────────────────────────────────

    # B1: sourceMaps not configured
    source_maps = config.get("sourceMaps")
    if source_maps is None or source_maps is False:
        findings.append(Finding("B1", "warning",
            "sourceMaps not configured",
            "Add sourceMaps: true (or 'inline') to enable source map generation for easier debugging"))

    # B2: No env config for different environments
    env_section = config.get("env")
    if not env_section or (isinstance(env_section, dict) and not env_section):
        findings.append(Finding("B2", "info",
            "No env config for different environments",
            "Consider adding an 'env' block to apply different transforms for development/production/test"))

    return findings


def format_text(findings, filepath):
    if not findings:
        return f"✅ {filepath}: No issues found"
    lines = [f"📋 {filepath}: {len(findings)} issue(s) found\n"]
    for f in findings:
        lines.append(f.to_text())
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    parts = []
    if errors:
        parts.append(f"{errors} error(s)")
    if warnings:
        parts.append(f"{warnings} warning(s)")
    if infos:
        parts.append(f"{infos} info")
    icon = "❌" if errors else ("⚠️" if warnings else "ℹ️")
    lines.append(f"\n{icon} {', '.join(parts)}")
    return "\n".join(lines)


def format_json(findings, filepath):
    return json.dumps({
        "file": filepath,
        "findings": [f.to_dict() for f in findings],
        "summary": {
            "errors": sum(1 for f in findings if f.severity == "error"),
            "warnings": sum(1 for f in findings if f.severity == "warning"),
            "info": sum(1 for f in findings if f.severity == "info"),
            "total": len(findings),
        }
    }, indent=2)


def format_summary(findings, filepath):
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return f"{status} | {filepath} | {errors} errors, {warnings} warnings"


def explain_config(config, filepath):
    lines = [f"📖 SWC Config Explanation: {filepath}\n"]

    jsc = config.get("jsc", {})
    if isinstance(jsc, dict):
        parser = jsc.get("parser", {})
        if isinstance(parser, dict):
            syntax = parser.get("syntax", "(not set)")
            jsx = parser.get("jsx", False)
            tsx = parser.get("tsx", False)
            decorators = parser.get("decorators", False)
            lines.append(f"Parser:")
            lines.append(f"  • syntax: {syntax}")
            if jsx:
                lines.append(f"  • JSX: enabled")
            if tsx:
                lines.append(f"  • TSX: enabled")
            if decorators:
                lines.append(f"  • decorators: enabled")

        target = jsc.get("target")
        if target:
            lines.append(f"\nCompilation target: {target}")

        transform = jsc.get("transform", {})
        if isinstance(transform, dict):
            react = transform.get("react")
            if react:
                runtime = react.get("runtime", "classic") if isinstance(react, dict) else "configured"
                lines.append(f"\nReact transform: runtime={runtime}")
            if transform.get("legacyDecorator"):
                lines.append("  • legacyDecorator: enabled")
            if transform.get("loose"):
                lines.append("  • loose mode: enabled")

        if jsc.get("minify"):
            lines.append("\nMinification: enabled via jsc.minify")

    module_config = config.get("module", {})
    if isinstance(module_config, dict):
        mtype = module_config.get("type", "(not set)")
        lines.append(f"\nModule output type: {mtype}")

    if config.get("minify"):
        lines.append("\nTop-level minify: enabled")

    source_maps = config.get("sourceMaps")
    if source_maps:
        lines.append(f"\nsourceMaps: {source_maps}")

    env_section = config.get("env", {})
    if isinstance(env_section, dict) and env_section:
        lines.append(f"\nEnvironment overrides: {', '.join(env_section.keys())}")

    return "\n".join(lines)


def suggest_improvements(config, filepath):
    lines = [f"💡 Suggestions for {filepath}\n"]
    suggestions = []

    jsc = config.get("jsc", {}) if isinstance(config.get("jsc"), dict) else {}

    # Suggest adding target
    if not jsc.get("target"):
        suggestions.append("Add jsc.target (e.g. 'es2017') — without it SWC defaults to ES5 which is larger")

    # Suggest sourceMaps
    if not config.get("sourceMaps"):
        suggestions.append("Add sourceMaps: true to enable source maps for easier debugging")

    # Suggest env block
    if not config.get("env"):
        suggestions.append("Add an 'env' block to apply different settings per environment (development/production/test)")

    # Suggest runtime: automatic for React (only when react transform is explicitly configured)
    transform = jsc.get("transform", {}) if isinstance(jsc.get("transform"), dict) else {}
    react = transform.get("react")
    if isinstance(react, dict) and react.get("runtime") != "automatic":
        suggestions.append("Set jsc.transform.react.runtime: 'automatic' to avoid importing React in every JSX file")

    # Suggest externalHelpers for large projects
    if not jsc.get("externalHelpers"):
        suggestions.append("Consider jsc.externalHelpers: true to avoid inlining SWC helpers in every file (use @swc/helpers package)")

    # Suggest keepClassNames in production
    minify_cfg = jsc.get("minify", {}) if isinstance(jsc.get("minify"), dict) else {}
    if config.get("minify") and not minify_cfg.get("keepClassNames"):
        suggestions.append("If class names matter at runtime (e.g. decorators, DI containers), set jsc.minify.keepClassNames: true")

    if not suggestions:
        lines.append("No suggestions — config looks good!")
    else:
        for s in suggestions:
            lines.append(f"  • {s}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: swc_config_validator.py <command> <file> [--format text|json|summary] [--strict]")
        print("Commands: validate, check, explain, suggest")
        sys.exit(2)

    command = sys.argv[1]
    filepath = sys.argv[2]
    fmt = "text"
    strict = False
    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]
        if arg == "--strict":
            strict = True

    config, error = load_config(filepath)
    if error:
        if command in ("validate", "check"):
            rule = "S1" if "not found" in error else ("S2" if "empty" in error.lower() else "S3")
            finding = Finding(rule, "error", error)
            if fmt == "json":
                print(format_json([finding], filepath))
            elif fmt == "summary":
                print(format_summary([finding], filepath))
            else:
                print(finding.to_text())
            sys.exit(2 if "not found" in error else 1)
        else:
            print(f"❌ {error}")
            sys.exit(2)

    if not isinstance(config, dict):
        print("❌ Config must be a JSON object")
        sys.exit(1)

    if command == "explain":
        print(explain_config(config, filepath))
        sys.exit(0)

    if command == "suggest":
        print(suggest_improvements(config, filepath))
        sys.exit(0)

    findings = validate(config, filepath)

    if command == "check":
        findings = [f for f in findings if f.rule_id.startswith("S")]

    if strict:
        for f in findings:
            if f.severity in ("warning", "info"):
                f.severity = "error"

    if fmt == "json":
        print(format_json(findings, filepath))
    elif fmt == "summary":
        print(format_summary(findings, filepath))
    else:
        print(format_text(findings, filepath))

    errors = sum(1 for f in findings if f.severity == "error")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
