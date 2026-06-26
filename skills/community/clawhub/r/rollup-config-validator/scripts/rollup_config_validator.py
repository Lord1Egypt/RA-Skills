#!/usr/bin/env python3
"""Rollup Config Validator — validate Rollup bundler configuration (JSON format)."""

import json
import re
import sys
from pathlib import Path

VALID_TOP_KEYS = {
    "input", "output", "external", "plugins", "cache", "onwarn", "onLog",
    "strictDeprecations", "context", "moduleContext", "treeshake",
    "experimentalCacheExpiry", "perf", "preserveEntrySignatures",
    "preserveSymlinks", "shimMissingExports", "watch", "makeAbsoluteExternalsRelative",
    "maxParallelFileOps", "logLevel",
}

VALID_OUTPUT_KEYS = {
    "dir", "file", "format", "globals", "name", "plugins", "assetFileNames",
    "banner", "chunkFileNames", "compact", "dynamicImportInCjs", "entryFileNames",
    "esModule", "exports", "extend", "externalImportAssertions", "externalImportAttributes",
    "footer", "freeze", "generatedCode", "hoistTransitiveImports", "importAttributesKey",
    "inlineDynamicImports", "interop", "intro", "manualChunks", "minifyInternalExports",
    "noConflict", "outro", "paths", "preserveModules", "preserveModulesRoot",
    "sanitizeFileName", "sourcemap", "sourcemapBaseUrl", "sourcemapExcludeSources",
    "sourcemapFile", "sourcemapIgnoreList", "sourcemapPathTransform", "strict",
    "systemNullSetters", "validate", "amd", "indent",
}

DEPRECATED_PLUGINS = {
    "rollup-plugin-node-resolve": "@rollup/plugin-node-resolve",
    "rollup-plugin-commonjs": "@rollup/plugin-commonjs",
    "rollup-plugin-json": "@rollup/plugin-json",
    "rollup-plugin-babel": "@rollup/plugin-babel",
    "rollup-plugin-replace": "@rollup/plugin-replace",
    "rollup-plugin-alias": "@rollup/plugin-alias",
    "rollup-plugin-inject": "@rollup/plugin-inject",
    "rollup-plugin-sucrase": "@rollup/plugin-sucrase",
    "rollup-plugin-terser": "@rollup/plugin-terser",
    "rollup-plugin-typescript": "@rollup/plugin-typescript",
    "rollup-plugin-url": "@rollup/plugin-url",
    "rollup-plugin-wasm": "@rollup/plugin-wasm",
    "rollup-plugin-yaml": "@rollup/plugin-yaml",
    "rollup-plugin-image": "@rollup/plugin-image",
    "rollup-plugin-dsv": "@rollup/plugin-dsv",
    "rollup-plugin-graphql-tag": "@rollup/plugin-graphql",
    "rollup-plugin-multi-entry": "@rollup/plugin-multi-entry",
    "rollup-plugin-legacy": "@rollup/plugin-legacy",
    "rollup-plugin-strip": "@rollup/plugin-strip",
    "rollup-plugin-virtual": "@rollup/plugin-virtual",
}

NODE_BUILTINS = {
    "assert", "buffer", "child_process", "cluster", "crypto", "dgram", "dns",
    "events", "fs", "http", "http2", "https", "net", "os", "path", "perf_hooks",
    "process", "querystring", "readline", "stream", "string_decoder", "timers",
    "tls", "tty", "url", "util", "v8", "vm", "worker_threads", "zlib",
    "node:assert", "node:buffer", "node:child_process", "node:cluster",
    "node:crypto", "node:dgram", "node:dns", "node:events", "node:fs",
    "node:http", "node:http2", "node:https", "node:net", "node:os", "node:path",
    "node:perf_hooks", "node:process", "node:querystring", "node:readline",
    "node:stream", "node:string_decoder", "node:timers", "node:tls", "node:tty",
    "node:url", "node:util", "node:v8", "node:vm", "node:worker_threads", "node:zlib",
}


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
        icon = "❌" if self.severity == "error" else "⚠️"
        s = f"{icon} [{self.rule_id}] {self.message}"
        if self.detail:
            s += f"\n   → {self.detail}"
        return s


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

    comment_re = re.compile(r'//.*?$|/\*.*?\*/', re.MULTILINE | re.DOTALL)
    cleaned = comment_re.sub('', text)
    cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)
    try:
        data = json.loads(cleaned)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"


def normalize_config(config):
    if isinstance(config, list):
        return config
    return [config]


def get_plugin_name(plugin):
    if isinstance(plugin, str):
        return plugin
    if isinstance(plugin, dict) and "name" in plugin:
        return plugin["name"]
    return ""


def validate_single(config, filepath, config_idx=None):
    findings = []
    prefix = f"Config #{config_idx}: " if config_idx is not None else ""

    unknown = set(config.keys()) - VALID_TOP_KEYS
    if unknown:
        findings.append(Finding("S3", "warning",
            f"{prefix}Unknown top-level keys: {', '.join(sorted(unknown))}"))

    inp = config.get("input")
    if not inp:
        findings.append(Finding("S5", "error",
            f"{prefix}Missing 'input' entry point"))

    output = config.get("output")
    if not output:
        findings.append(Finding("O1", "error",
            f"{prefix}Missing 'output' configuration"))
    else:
        outputs = output if isinstance(output, list) else [output]
        for i, out in enumerate(outputs):
            if not isinstance(out, dict):
                continue
            out_prefix = f"{prefix}output[{i}]: " if len(outputs) > 1 else f"{prefix}"

            out_unknown = set(out.keys()) - VALID_OUTPUT_KEYS
            if out_unknown:
                findings.append(Finding("S3", "warning",
                    f"{out_prefix}Unknown output keys: {', '.join(sorted(out_unknown))}"))

            fmt = out.get("format")
            if not fmt:
                findings.append(Finding("O2", "warning",
                    f"{out_prefix}Missing output.format (defaults to 'es')",
                    "Explicitly set format: 'es', 'cjs', 'iife', 'umd', 'amd', or 'system'"))

            if out.get("file") and out.get("dir"):
                findings.append(Finding("O3", "warning",
                    f"{out_prefix}Both output.file and output.dir specified",
                    "Use file for single-file output or dir for code-splitting"))

            if fmt in ("iife", "umd") and not out.get("name"):
                findings.append(Finding("O4", "warning",
                    f"{out_prefix}format '{fmt}' requires output.name for the global variable",
                    "Set name: 'MyLibrary' for browser/UMD builds"))

            if out.get("sourcemap") and not out.get("sourcemapExcludeSources"):
                pass  # O6 only if sourcemap is true, but this is very optional

        if len(outputs) > 1:
            format_files = {}
            for out in outputs:
                if isinstance(out, dict):
                    key = (out.get("format", "es"), out.get("file"), out.get("dir"))
                    if key in format_files and not key[1] and not key[2]:
                        findings.append(Finding("O5", "warning",
                            f"{prefix}Multiple outputs with format '{key[0]}' without distinct file/dir"))
                    format_files[key] = True

    external = config.get("external", [])
    if isinstance(external, list):
        for ext in external:
            if isinstance(ext, str) and ext.startswith("/") and ext.endswith("/"):
                findings.append(Finding("E2", "warning",
                    f"{prefix}Regex pattern in external: {ext}",
                    "Regex externals are fragile; prefer explicit module names or a function"))

    plugins = config.get("plugins", [])
    if isinstance(plugins, list):
        plugin_names = [get_plugin_name(p) for p in plugins]

        resolve_idx = -1
        commonjs_idx = -1
        for i, pn in enumerate(plugin_names):
            if "node-resolve" in pn or "resolve" == pn:
                resolve_idx = i
            if "commonjs" in pn:
                commonjs_idx = i

        if resolve_idx >= 0 and commonjs_idx >= 0 and resolve_idx > commonjs_idx:
            findings.append(Finding("P1", "warning",
                f"{prefix}@rollup/plugin-node-resolve should come before @rollup/plugin-commonjs",
                "Resolve must locate modules before commonjs transforms them"))

        if commonjs_idx >= 0 and resolve_idx < 0:
            findings.append(Finding("P2", "warning",
                f"{prefix}@rollup/plugin-commonjs without @rollup/plugin-node-resolve",
                "commonjs plugin needs node-resolve to find node_modules packages"))

        for pn in plugin_names:
            if pn in DEPRECATED_PLUGINS:
                findings.append(Finding("P4", "warning",
                    f"{prefix}Deprecated plugin: {pn}",
                    f"Replace with {DEPRECATED_PLUGINS[pn]}"))

    treeshake = config.get("treeshake")
    if treeshake is False:
        findings.append(Finding("T1", "warning",
            f"{prefix}treeshake: false disables dead code elimination",
            "Only disable for debugging; re-enable for production builds"))
    elif isinstance(treeshake, dict):
        if treeshake.get("moduleSideEffects") is False:
            findings.append(Finding("T2", "warning",
                f"{prefix}treeshake.moduleSideEffects: false may break libraries with side effects",
                "Consider using sideEffects field in package.json instead"))

    watch = config.get("watch")
    if isinstance(watch, dict):
        if "clearScreen" not in watch:
            findings.append(Finding("B3", "warning",
                f"{prefix}watch config without clearScreen setting",
                "Set clearScreen: false to preserve terminal output during watch"))

    return findings


def validate(config_data, filepath):
    configs = normalize_config(config_data)
    all_findings = []

    for i, config in enumerate(configs):
        if not isinstance(config, dict):
            all_findings.append(Finding("S2", "error", f"Config #{i+1} is not an object"))
            continue
        idx = i + 1 if len(configs) > 1 else None
        all_findings.extend(validate_single(config, filepath, idx))

    return all_findings


def format_text(findings, filepath):
    if not findings:
        return f"✅ {filepath}: No issues found"
    lines = [f"📋 {filepath}: {len(findings)} issue(s) found\n"]
    for f in findings:
        lines.append(f.to_text())
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    lines.append(f"\n{'❌' if errors else '⚠️'} {errors} error(s), {warnings} warning(s)")
    return "\n".join(lines)


def format_json(findings, filepath):
    return json.dumps({
        "file": filepath,
        "findings": [f.to_dict() for f in findings],
        "summary": {
            "errors": sum(1 for f in findings if f.severity == "error"),
            "warnings": sum(1 for f in findings if f.severity == "warning"),
            "total": len(findings),
        }
    }, indent=2)


def format_summary(findings, filepath):
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return f"{status} | {filepath} | {errors} errors, {warnings} warnings"


def explain_config(config_data, filepath):
    configs = normalize_config(config_data)
    lines = [f"📖 Rollup Config Explanation: {filepath}\n"]

    for i, config in enumerate(configs):
        if not isinstance(config, dict):
            continue
        if len(configs) > 1:
            lines.append(f"--- Config #{i+1} ---")

        inp = config.get("input")
        if inp:
            if isinstance(inp, dict):
                lines.append(f"Entry points: {json.dumps(inp)}")
            elif isinstance(inp, list):
                lines.append(f"Entry points: {', '.join(inp)}")
            else:
                lines.append(f"Entry point: {inp}")

        output = config.get("output")
        if output:
            outputs = output if isinstance(output, list) else [output]
            lines.append(f"\nOutput ({len(outputs)} target{'s' if len(outputs) > 1 else ''}):")
            for j, out in enumerate(outputs):
                if isinstance(out, dict):
                    fmt = out.get("format", "es")
                    dest = out.get("file") or out.get("dir") or "(no path)"
                    name = out.get("name", "")
                    desc = f"  • [{fmt}] → {dest}"
                    if name:
                        desc += f" (global: {name})"
                    lines.append(desc)

        external = config.get("external", [])
        if external:
            if isinstance(external, list):
                lines.append(f"\nExternal modules: {', '.join(str(e) for e in external[:10])}")
                if len(external) > 10:
                    lines.append(f"  ... and {len(external) - 10} more")

        plugins = config.get("plugins", [])
        if plugins:
            lines.append(f"\nPlugins ({len(plugins)}):")
            for p in plugins:
                pn = get_plugin_name(p)
                lines.append(f"  • {pn or '(anonymous)'}")

        treeshake = config.get("treeshake")
        if treeshake is False:
            lines.append("\nTreeshake: DISABLED")
        elif isinstance(treeshake, dict):
            lines.append(f"\nTreeshake: custom ({json.dumps(treeshake, default=str)[:80]})")

    return "\n".join(lines)


def suggest_improvements(config_data, filepath):
    configs = normalize_config(config_data)
    lines = [f"💡 Suggestions for {filepath}\n"]
    suggestions = []

    for config in configs:
        if not isinstance(config, dict):
            continue

        plugins = config.get("plugins", [])
        plugin_names = [get_plugin_name(p) for p in plugins] if isinstance(plugins, list) else []

        has_resolve = any("resolve" in pn for pn in plugin_names)
        has_commonjs = any("commonjs" in pn for pn in plugin_names)
        has_terser = any("terser" in pn for pn in plugin_names)

        if not has_resolve:
            suggestions.append("Add @rollup/plugin-node-resolve to resolve node_modules imports")

        if not has_commonjs and has_resolve:
            suggestions.append("Add @rollup/plugin-commonjs to handle CommonJS dependencies")

        if not has_terser:
            suggestions.append("Consider @rollup/plugin-terser for production minification")

        output = config.get("output")
        if output:
            outputs = output if isinstance(output, list) else [output]
            formats = [o.get("format") for o in outputs if isinstance(o, dict)]
            if "es" not in formats and "esm" not in formats:
                suggestions.append("Consider adding an ESM output format for modern bundlers")
            if "cjs" not in formats and "commonjs" not in formats:
                suggestions.append("Consider adding a CJS output for Node.js compatibility")

        treeshake = config.get("treeshake")
        if treeshake is False:
            suggestions.append("Re-enable treeshake for production builds to reduce bundle size")

        for pn in plugin_names:
            if pn in DEPRECATED_PLUGINS:
                suggestions.append(f"Migrate {pn} → {DEPRECATED_PLUGINS[pn]}")

    if not suggestions:
        lines.append("No suggestions — config looks good!")
    else:
        for s in list(dict.fromkeys(suggestions)):
            lines.append(f"  • {s}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: rollup_config_validator.py <command> <file> [--format text|json|summary] [--strict]")
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

    config_data, error = load_config(filepath)
    if error:
        if command in ("validate", "check"):
            finding = Finding("S1" if "not found" in error else "S4", "error", error)
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

    if command == "explain":
        print(explain_config(config_data, filepath))
        sys.exit(0)

    if command == "suggest":
        print(suggest_improvements(config_data, filepath))
        sys.exit(0)

    findings = validate(config_data, filepath)

    if command == "check":
        findings = [f for f in findings if f.rule_id.startswith("S")]

    if strict:
        for f in findings:
            if f.severity == "warning":
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
