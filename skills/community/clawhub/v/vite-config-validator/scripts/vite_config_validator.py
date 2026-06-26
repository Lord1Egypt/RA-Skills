#!/usr/bin/env python3
"""
Vite Config Validator
Validate Vite configuration files (JSON-exported) for structural correctness,
build settings, server configuration, resolve/CSS options, plugin hygiene, and
best practices.
Usage: python3 vite_config_validator.py <command> <file> [--strict] [--format text|json|summary]
Commands: validate, check, explain, suggest
"""

import sys
import os
import re
import json
import argparse
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_TOP_LEVEL_KEYS = {
    "root", "base", "mode", "define", "plugins", "resolve", "css", "json",
    "esbuild", "assetsInclude", "server", "build", "preview", "optimizeDeps",
    "ssr", "worker", "test",
}

VALID_BUILD_TARGETS = {
    "modules", "esnext",
    "es2015", "es2016", "es2017", "es2018", "es2019", "es2020",
    "es2021", "es2022", "es2023", "es2024",
    "chrome87", "chrome88", "chrome89", "chrome90", "chrome91",
    "firefox78", "firefox85", "firefox90",
    "safari13", "safari14", "safari15",
    "edge88", "edge89", "edge90",
    "node12", "node14", "node16", "node18", "node20",
}

VALID_MINIFY_VALUES = {True, False, "terser", "esbuild"}

DEPRECATED_ROLLUP_PLUGINS = {
    "rollup-plugin-babel": "@rollup/plugin-babel",
    "rollup-plugin-node-resolve": "@rollup/plugin-node-resolve",
    "rollup-plugin-commonjs": "@rollup/plugin-commonjs",
    "rollup-plugin-json": "@rollup/plugin-json",
    "rollup-plugin-replace": "@rollup/plugin-replace",
    "rollup-plugin-alias": "@rollup/plugin-alias",
    "rollup-plugin-typescript": "@rollup/plugin-typescript",
    "rollup-plugin-terser": "@rollup/plugin-terser",
    "rollup-plugin-url": "@rollup/plugin-url",
    "rollup-plugin-image": "@rollup/plugin-image",
}

DEPRECATED_VITE_PLUGINS = {
    "vite-plugin-html": "@vitejs/plugin-legacy or vite-plugin-html-config",
    "vite-plugin-imp": "vite-plugin-components (auto-import)",
    "vite-plugin-style-import": "vite-plugin-lib-css",
    "vite-plugin-restart": "built-in Vite 5+ server.watch",
    "vite-plugin-mock": "vite-plugin-mock-dev-server",
}

VALID_CSS_MODULES_OPTIONS = {
    "scopeBehaviour", "globalModulePaths", "generateScopedName",
    "hashPrefix", "localsConvention",
}


# ---------------------------------------------------------------------------
# Finding class
# ---------------------------------------------------------------------------

class Finding:
    """A single validation finding."""

    SEVERITIES = ("error", "warning", "info")

    def __init__(self, rule_id: str, severity: str, message: str, detail: str = ""):
        assert severity in self.SEVERITIES, f"Invalid severity: {severity}"
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.detail = detail

    def to_dict(self) -> dict:
        d = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
        }
        if self.detail:
            d["detail"] = self.detail
        return d

    def __repr__(self):
        return f"Finding({self.rule_id}, {self.severity}, {self.message!r})"


# ---------------------------------------------------------------------------
# JSON loading
# ---------------------------------------------------------------------------

def load_config(path: str) -> tuple:
    """Load and parse a Vite config JSON file. Returns (data, error_finding)."""
    # S1: File not found or unreadable
    if not os.path.exists(path):
        return None, Finding("S1", "error", f"File not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return None, Finding("S1", "error", f"Cannot read file: {e}")

    # S2: Empty config
    if len(content.strip()) == 0:
        return None, Finding("S2", "error", "Config file is empty")

    # S3: Invalid JSON syntax
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return None, Finding("S3", "error", f"Invalid JSON syntax: {e}")

    if not isinstance(data, dict):
        return None, Finding("S3", "error",
            "Config must be a JSON object (got {})".format(type(data).__name__))

    return data, None


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------

def check_structure(data: dict) -> list:
    """S4, S5: Check top-level keys and defineConfig hint."""
    findings = []

    # S4: Unknown top-level keys
    unknown = set(data.keys()) - VALID_TOP_LEVEL_KEYS
    if unknown:
        for key in sorted(unknown):
            findings.append(Finding("S4", "warning",
                f"Unknown top-level key: '{key}'",
                f"Valid keys: {', '.join(sorted(VALID_TOP_LEVEL_KEYS))}"))

    # S5: defineConfig wrapper hint
    findings.append(Finding("S5", "info",
        "JSON export cannot verify defineConfig() wrapper",
        "Wrap your config with defineConfig() in vite.config.ts for type safety "
        "and IDE autocompletion: export default defineConfig({ ... })"))

    return findings


def check_build(data: dict) -> list:
    """B1-B5: Check build configuration."""
    findings = []
    build = data.get("build")

    if build is None:
        return findings

    if not isinstance(build, dict):
        findings.append(Finding("B1", "warning",
            "build must be an object",
            "Set build: { outDir: 'dist', ... }"))
        return findings

    # B1: Missing build.outDir (info)
    if "outDir" not in build:
        findings.append(Finding("B1", "info",
            "Missing build.outDir — defaults to 'dist'",
            "Explicitly set build.outDir for clarity, especially in monorepos."))

    # B2: build.target invalid value
    target = build.get("target")
    if target is not None:
        targets = [target] if isinstance(target, str) else target
        if isinstance(targets, list):
            for t in targets:
                if isinstance(t, str):
                    t_lower = t.lower()
                    # Check against known targets or patterns like esNNNN, chromeNN, etc.
                    matched = False
                    if t_lower in VALID_BUILD_TARGETS:
                        matched = True
                    elif re.match(r'^es20\d{2}$', t_lower):
                        matched = True
                    elif re.match(r'^(chrome|firefox|safari|edge|node)\d+$', t_lower):
                        matched = True
                    if not matched:
                        findings.append(Finding("B2", "error",
                            f"Invalid build.target value: '{t}'",
                            "Valid targets: 'modules', 'esnext', 'es20XX', or browser versions "
                            "like 'chrome87', 'firefox78', 'safari13'."))

    # B3: build.minify invalid value
    minify = build.get("minify")
    if minify is not None:
        if minify not in (True, False, "terser", "esbuild"):
            findings.append(Finding("B3", "error",
                f"Invalid build.minify value: {minify!r}",
                "Valid values: true, false, 'terser', or 'esbuild'."))

    # B4: build.sourcemap with 'hidden' in development
    sourcemap = build.get("sourcemap")
    mode = data.get("mode", "")
    if sourcemap == "hidden" and mode in ("development", "dev"):
        findings.append(Finding("B4", "warning",
            "build.sourcemap is 'hidden' in development mode",
            "Hidden sourcemaps in development make debugging harder. "
            "Use true or 'inline' for development builds."))

    # B5: Deprecated Rollup plugins in build.rollupOptions
    rollup_options = build.get("rollupOptions")
    if isinstance(rollup_options, dict):
        plugins = rollup_options.get("plugins", [])
        if isinstance(plugins, list):
            for plugin in plugins:
                if isinstance(plugin, (str, dict)):
                    plugin_name = plugin if isinstance(plugin, str) else plugin.get("name", "")
                    for deprecated, replacement in DEPRECATED_ROLLUP_PLUGINS.items():
                        if deprecated in str(plugin_name):
                            findings.append(Finding("B5", "warning",
                                f"Deprecated Rollup plugin detected: '{deprecated}'",
                                f"Migrate to '{replacement}'. The rollup-plugin-* namespace "
                                "is deprecated in favor of @rollup/plugin-*."))
        # Also check for plugin references in output config
        output = rollup_options.get("output")
        if isinstance(output, dict):
            out_plugins = output.get("plugins", [])
            if isinstance(out_plugins, list):
                for plugin in out_plugins:
                    if isinstance(plugin, (str, dict)):
                        plugin_name = plugin if isinstance(plugin, str) else plugin.get("name", "")
                        for deprecated, replacement in DEPRECATED_ROLLUP_PLUGINS.items():
                            if deprecated in str(plugin_name):
                                findings.append(Finding("B5", "warning",
                                    f"Deprecated Rollup plugin in output: '{deprecated}'",
                                    f"Migrate to '{replacement}'."))

    return findings


def check_server(data: dict) -> list:
    """V1-V4: Check server configuration."""
    findings = []
    server = data.get("server")

    if server is None:
        return findings

    if not isinstance(server, dict):
        return findings

    # V1: server.port out of valid range
    port = server.get("port")
    if port is not None:
        if isinstance(port, (int, float)):
            port_int = int(port)
            if port_int < 1 or port_int > 65535:
                findings.append(Finding("V1", "error",
                    f"server.port {port_int} is out of valid range (1-65535)",
                    "Use a port between 1024 and 65535. Common dev ports: 3000, 5173, 8080."))
            elif port_int < 1024:
                findings.append(Finding("V1", "warning",
                    f"server.port {port_int} is a privileged port (<1024)",
                    "Privileged ports require root access. Use a port >= 1024."))
        else:
            findings.append(Finding("V1", "error",
                f"server.port must be a number, got {type(port).__name__}",
                "Set server.port to a number like 3000 or 5173."))

    # V2: server.host set to true/0.0.0.0 security warning
    host = server.get("host")
    if host is True or host == "0.0.0.0":
        findings.append(Finding("V2", "warning",
            "server.host exposes dev server to all network interfaces",
            "Setting host to true or '0.0.0.0' makes the dev server accessible "
            "from any device on the network. Use 'localhost' or '127.0.0.1' for local-only."))

    # V3: server.proxy with invalid target URLs
    proxy = server.get("proxy")
    if isinstance(proxy, dict):
        url_pattern = re.compile(r'^https?://[^\s]+$')
        for path_key, proxy_config in proxy.items():
            target = None
            if isinstance(proxy_config, str):
                target = proxy_config
            elif isinstance(proxy_config, dict):
                target = proxy_config.get("target")

            if target is not None and isinstance(target, str):
                if not url_pattern.match(target):
                    findings.append(Finding("V3", "warning",
                        f"Proxy target for '{path_key}' may be invalid: '{target}'",
                        "Proxy targets should be valid URLs like 'http://localhost:3001'."))

    # V4: server.https without cert/key paths
    https_config = server.get("https")
    if https_config is True:
        findings.append(Finding("V4", "warning",
            "server.https enabled without cert/key paths",
            "Set server.https to an object with 'key' and 'cert' paths, or use "
            "@vitejs/plugin-basic-ssl for auto-generated certificates."))
    elif isinstance(https_config, dict):
        has_key = "key" in https_config
        has_cert = "cert" in https_config
        if not has_key or not has_cert:
            missing = []
            if not has_key:
                missing.append("key")
            if not has_cert:
                missing.append("cert")
            findings.append(Finding("V4", "warning",
                f"server.https missing: {', '.join(missing)}",
                "Both 'key' and 'cert' paths are required for HTTPS."))

    return findings


def check_resolve(data: dict) -> list:
    """R1-R3: Check resolve configuration."""
    findings = []
    resolve = data.get("resolve")

    if resolve is None:
        return findings

    if not isinstance(resolve, dict):
        return findings

    # R1: resolve.alias with absolute paths (portability)
    alias = resolve.get("alias")
    if isinstance(alias, dict):
        for alias_key, alias_path in alias.items():
            if isinstance(alias_path, str):
                # Check for absolute paths that aren't using path.resolve() patterns
                if alias_path.startswith("/") and not alias_path.startswith("/${"):
                    findings.append(Finding("R1", "warning",
                        f"resolve.alias '{alias_key}' uses absolute path: '{alias_path}'",
                        "Absolute paths break portability. Use path.resolve() or "
                        "fileURLToPath(new URL('./src', import.meta.url)) in vite.config.ts."))
    elif isinstance(alias, list):
        for entry in alias:
            if isinstance(entry, dict):
                replacement = entry.get("replacement", "")
                find = entry.get("find", "")
                if isinstance(replacement, str) and replacement.startswith("/"):
                    findings.append(Finding("R1", "warning",
                        f"resolve.alias for '{find}' uses absolute path: '{replacement}'",
                        "Absolute paths break portability across machines/CI."))

    # R2: Missing resolve.extensions for TypeScript projects
    extensions = resolve.get("extensions")
    # Heuristic: if there are .ts/.tsx references in alias or other config hints
    has_ts_hints = False
    if isinstance(alias, dict):
        for v in alias.values():
            if isinstance(v, str) and (".ts" in v or "typescript" in v.lower()):
                has_ts_hints = True
                break
    # Also check esbuild or build config for TS hints
    esbuild = data.get("esbuild", {})
    if isinstance(esbuild, dict) and esbuild.get("loader") in ("tsx", "ts"):
        has_ts_hints = True
    # Check plugins for @vitejs/plugin-react or similar
    plugins = data.get("plugins", [])
    if isinstance(plugins, list):
        for p in plugins:
            if isinstance(p, dict) and "name" in p:
                pname = str(p["name"]).lower()
                if "react" in pname or "vue" in pname or "svelte" in pname:
                    has_ts_hints = True

    if has_ts_hints and not extensions:
        findings.append(Finding("R2", "info",
            "TypeScript project detected but resolve.extensions not set",
            "Consider adding resolve.extensions: ['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json'] "
            "if you experience module resolution issues."))

    # R3: resolve.dedupe with empty array
    dedupe = resolve.get("dedupe")
    if isinstance(dedupe, list) and len(dedupe) == 0:
        findings.append(Finding("R3", "warning",
            "resolve.dedupe is an empty array",
            "An empty dedupe array has no effect. Either add packages to deduplicate "
            "or remove the option entirely."))

    return findings


def check_css(data: dict) -> list:
    """C1-C3: Check CSS configuration."""
    findings = []
    css = data.get("css")

    if css is None:
        return findings

    if not isinstance(css, dict):
        return findings

    # C1: css.preprocessorOptions without corresponding preprocessor dependency hint
    preproc = css.get("preprocessorOptions")
    if isinstance(preproc, dict):
        preprocessors_used = list(preproc.keys())
        dep_map = {
            "scss": "sass",
            "sass": "sass",
            "less": "less",
            "styl": "stylus",
            "stylus": "stylus",
        }
        for pp in preprocessors_used:
            if pp in dep_map:
                dep_name = dep_map[pp]
                findings.append(Finding("C1", "info",
                    f"css.preprocessorOptions.{pp} configured — ensure '{dep_name}' is installed",
                    f"Vite requires '{dep_name}' as a peer dependency for {pp} preprocessing. "
                    f"Install with: npm install -D {dep_name}"))

    # C2: css.modules with invalid options
    modules = css.get("modules")
    if isinstance(modules, dict):
        unknown_opts = set(modules.keys()) - VALID_CSS_MODULES_OPTIONS
        if unknown_opts:
            findings.append(Finding("C2", "warning",
                f"css.modules has unknown options: {', '.join(sorted(unknown_opts))}",
                f"Valid css.modules options: {', '.join(sorted(VALID_CSS_MODULES_OPTIONS))}"))

        # Check localsConvention value
        convention = modules.get("localsConvention")
        if convention is not None:
            valid_conventions = {"camelCase", "camelCaseOnly", "dashes", "dashesOnly", None}
            if convention not in valid_conventions:
                findings.append(Finding("C2", "warning",
                    f"css.modules.localsConvention has invalid value: '{convention}'",
                    "Valid values: 'camelCase', 'camelCaseOnly', 'dashes', 'dashesOnly'."))

    # C3: css.postcss pointing to non-existent file
    postcss = css.get("postcss")
    if isinstance(postcss, str):
        # It's a path to a PostCSS config file
        if not os.path.exists(postcss):
            findings.append(Finding("C3", "warning",
                f"css.postcss references non-existent file: '{postcss}'",
                "Ensure the PostCSS config file exists at the specified path, "
                "or use an inline PostCSS config object."))

    return findings


def check_plugins(data: dict) -> list:
    """P1-P2: Check plugins configuration."""
    findings = []
    plugins = data.get("plugins")

    if plugins is None:
        return findings

    if not isinstance(plugins, list):
        return findings

    # P1: Empty plugins array
    if len(plugins) == 0:
        findings.append(Finding("P1", "info",
            "plugins array is empty",
            "An empty plugins array has no effect. Add plugins or remove the key."))
        return findings

    # P2: Deprecated plugin names
    for plugin in plugins:
        plugin_name = None
        if isinstance(plugin, str):
            plugin_name = plugin
        elif isinstance(plugin, dict):
            plugin_name = plugin.get("name", "")
        elif isinstance(plugin, list) and len(plugin) > 0:
            # Array form: [pluginName, options]
            plugin_name = str(plugin[0]) if plugin[0] else None

        if plugin_name and isinstance(plugin_name, str):
            for deprecated, replacement in DEPRECATED_VITE_PLUGINS.items():
                if deprecated in plugin_name:
                    findings.append(Finding("P2", "warning",
                        f"Deprecated Vite plugin detected: '{deprecated}'",
                        f"Consider migrating to '{replacement}'."))

    return findings


def check_best_practices(data: dict) -> list:
    """X1-X3: Check best practices."""
    findings = []

    # X1: No mode set (info)
    if "mode" not in data:
        findings.append(Finding("X1", "info",
            "No mode set in config",
            "Vite defaults to 'development' for serve and 'production' for build. "
            "Set mode explicitly if you need environment-specific behavior in the config itself."))

    # X2: Missing base for non-root deployments (info)
    if "base" not in data:
        findings.append(Finding("X2", "info",
            "No base path set — defaults to '/'",
            "Set base if deploying to a subdirectory (e.g., base: '/my-app/'). "
            "Required for GitHub Pages, subpath deployments, etc."))

    # X3: build.chunkSizeWarningLimit too high (>2000)
    build = data.get("build", {})
    if isinstance(build, dict):
        chunk_limit = build.get("chunkSizeWarningLimit")
        if isinstance(chunk_limit, (int, float)) and chunk_limit > 2000:
            findings.append(Finding("X3", "warning",
                f"build.chunkSizeWarningLimit is very high ({chunk_limit} kB)",
                "A limit above 2000 kB effectively silences chunk size warnings. "
                "Large chunks hurt load performance. Consider code splitting instead of "
                "raising the limit. Default is 500 kB."))

    return findings


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def validate_all(data: dict) -> list:
    """Run all checks and return combined findings."""
    findings = []
    findings.extend(check_structure(data))
    findings.extend(check_build(data))
    findings.extend(check_server(data))
    findings.extend(check_resolve(data))
    findings.extend(check_css(data))
    findings.extend(check_plugins(data))
    findings.extend(check_best_practices(data))
    return findings


# ---------------------------------------------------------------------------
# Rule explanations (for 'explain' command)
# ---------------------------------------------------------------------------

RULE_EXPLANATIONS = {
    "S1": {
        "name": "File Not Found",
        "category": "Structure",
        "severity": "error",
        "description": "The config JSON file does not exist or cannot be read.",
        "fix": "Ensure the file path is correct and the file has read permissions.",
    },
    "S2": {
        "name": "Empty Config",
        "category": "Structure",
        "severity": "error",
        "description": "The config file is empty (zero bytes or only whitespace).",
        "fix": "Export your Vite config to JSON: node -e \"import('./vite.config.ts').then(m => console.log(JSON.stringify(m.default)))\" > vite.config.json",
    },
    "S3": {
        "name": "Invalid JSON",
        "category": "Structure",
        "severity": "error",
        "description": "The file contains invalid JSON syntax that cannot be parsed.",
        "fix": "Fix the JSON syntax error reported in the message. Use a JSON linter or re-export from vite.config.ts.",
    },
    "S4": {
        "name": "Unknown Top-Level Key",
        "category": "Structure",
        "severity": "warning",
        "description": "A top-level key is not a recognized Vite config option. May indicate a typo or plugin-specific config placed at the wrong level.",
        "fix": "Check the Vite docs for valid top-level keys. Plugin options usually go inside the plugins array, not at the top level.",
    },
    "S5": {
        "name": "defineConfig Wrapper Hint",
        "category": "Structure",
        "severity": "info",
        "description": "JSON export cannot verify that the config uses defineConfig(). This is just a reminder.",
        "fix": "Wrap your config: import { defineConfig } from 'vite'; export default defineConfig({ ... })",
    },
    "B1": {
        "name": "Missing outDir",
        "category": "Build",
        "severity": "info",
        "description": "No build.outDir specified — Vite defaults to 'dist'.",
        "fix": "Add build.outDir if you need a custom output directory.",
    },
    "B2": {
        "name": "Invalid Build Target",
        "category": "Build",
        "severity": "error",
        "description": "build.target contains an invalid value. Must be an ES version, browser version, or 'modules'/'esnext'.",
        "fix": "Use valid targets: 'modules', 'esnext', 'es2020', 'chrome87', 'firefox78', 'safari13', 'node18', etc.",
    },
    "B3": {
        "name": "Invalid Minify Value",
        "category": "Build",
        "severity": "error",
        "description": "build.minify must be true, false, 'terser', or 'esbuild'.",
        "fix": "Set build.minify to true, false, 'terser', or 'esbuild'. Default is 'esbuild'.",
    },
    "B4": {
        "name": "Hidden Sourcemap in Development",
        "category": "Build",
        "severity": "warning",
        "description": "Using 'hidden' sourcemaps in development mode makes debugging difficult.",
        "fix": "Use build.sourcemap: true or 'inline' for development. Reserve 'hidden' for production.",
    },
    "B5": {
        "name": "Deprecated Rollup Plugin",
        "category": "Build",
        "severity": "warning",
        "description": "Using a deprecated rollup-plugin-* package instead of the scoped @rollup/plugin-* replacement.",
        "fix": "Migrate from rollup-plugin-X to @rollup/plugin-X. The old namespace is unmaintained.",
    },
    "V1": {
        "name": "Invalid Server Port",
        "category": "Server",
        "severity": "error",
        "description": "server.port is outside the valid range (1-65535) or is a privileged port (<1024).",
        "fix": "Use a port between 1024 and 65535. Common choices: 3000, 5173, 8080.",
    },
    "V2": {
        "name": "Exposed Dev Server",
        "category": "Server",
        "severity": "warning",
        "description": "server.host is true or '0.0.0.0', exposing the dev server to the entire network.",
        "fix": "Use 'localhost' or '127.0.0.1' for local-only access. Only expose if you need LAN/mobile testing.",
    },
    "V3": {
        "name": "Invalid Proxy Target",
        "category": "Server",
        "severity": "warning",
        "description": "A proxy target URL does not look like a valid HTTP(S) URL.",
        "fix": "Proxy targets should start with http:// or https:// (e.g., 'http://localhost:3001').",
    },
    "V4": {
        "name": "HTTPS Without Certificates",
        "category": "Server",
        "severity": "warning",
        "description": "server.https is enabled but missing key/cert file paths.",
        "fix": "Provide key and cert paths, or use @vitejs/plugin-basic-ssl for auto-generated dev certs.",
    },
    "R1": {
        "name": "Absolute Path in Alias",
        "category": "Resolve",
        "severity": "warning",
        "description": "resolve.alias uses an absolute filesystem path, which breaks portability across machines and CI.",
        "fix": "Use path.resolve(__dirname, './src') or fileURLToPath(new URL('./src', import.meta.url)).",
    },
    "R2": {
        "name": "Missing Extensions for TypeScript",
        "category": "Resolve",
        "severity": "info",
        "description": "TypeScript project detected but resolve.extensions not explicitly set.",
        "fix": "Add resolve.extensions: ['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json'] if needed.",
    },
    "R3": {
        "name": "Empty Dedupe Array",
        "category": "Resolve",
        "severity": "warning",
        "description": "resolve.dedupe is set to an empty array, which has no effect.",
        "fix": "Add packages to deduplicate (e.g., ['react', 'react-dom']) or remove the option.",
    },
    "C1": {
        "name": "Preprocessor Dependency Hint",
        "category": "CSS",
        "severity": "info",
        "description": "CSS preprocessor options are configured but the required preprocessor package may not be installed.",
        "fix": "Install the preprocessor as a dev dependency: npm install -D sass/less/stylus.",
    },
    "C2": {
        "name": "Invalid CSS Modules Option",
        "category": "CSS",
        "severity": "warning",
        "description": "css.modules contains an unknown or invalid option.",
        "fix": "Valid css.modules options: scopeBehaviour, globalModulePaths, generateScopedName, hashPrefix, localsConvention.",
    },
    "C3": {
        "name": "Missing PostCSS Config",
        "category": "CSS",
        "severity": "warning",
        "description": "css.postcss references a file path that does not exist.",
        "fix": "Create the PostCSS config file or use an inline config object.",
    },
    "P1": {
        "name": "Empty Plugins Array",
        "category": "Plugins",
        "severity": "info",
        "description": "The plugins array is empty. It has no effect.",
        "fix": "Add plugins or remove the empty array.",
    },
    "P2": {
        "name": "Deprecated Vite Plugin",
        "category": "Plugins",
        "severity": "warning",
        "description": "A known deprecated Vite plugin is in use. It may not work with newer Vite versions.",
        "fix": "Migrate to the suggested replacement plugin.",
    },
    "X1": {
        "name": "No Mode Set",
        "category": "Best Practices",
        "severity": "info",
        "description": "No mode is set in the config. Vite defaults to 'development' for serve and 'production' for build.",
        "fix": "Set mode explicitly if you need environment-specific behavior in the config.",
    },
    "X2": {
        "name": "Missing Base Path",
        "category": "Best Practices",
        "severity": "info",
        "description": "No base path set. Defaults to '/'. Required for subdirectory deployments.",
        "fix": "Set base: '/my-app/' if deploying to a subdirectory (GitHub Pages, etc.).",
    },
    "X3": {
        "name": "Chunk Size Limit Too High",
        "category": "Best Practices",
        "severity": "warning",
        "description": "build.chunkSizeWarningLimit is set above 2000 kB, effectively silencing chunk warnings.",
        "fix": "Use code splitting (dynamic imports) instead of raising the limit. Default is 500 kB.",
    },
}


# ---------------------------------------------------------------------------
# Suggestion engine (for 'suggest' command)
# ---------------------------------------------------------------------------

def generate_suggestions(data: dict, findings: list) -> list:
    """Generate actionable fix suggestions from findings."""
    suggestions = []

    for f in findings:
        rule = RULE_EXPLANATIONS.get(f.rule_id)
        if not rule:
            continue

        suggestion = {
            "rule_id": f.rule_id,
            "severity": f.severity,
            "problem": f.message,
            "fix": rule["fix"],
        }

        # Add concrete config snippets for common fixes
        if f.rule_id == "B1":
            suggestion["snippet"] = '"build": { "outDir": "dist" }'
        elif f.rule_id == "B3":
            suggestion["snippet"] = '"build": { "minify": "esbuild" }'
        elif f.rule_id == "X1":
            suggestion["snippet"] = '"mode": "development"'
        elif f.rule_id == "X2":
            suggestion["snippet"] = '"base": "/my-app/"'
        elif f.rule_id == "V2":
            suggestion["snippet"] = '"server": { "host": "localhost" }'
        elif f.rule_id == "R3":
            suggestion["snippet"] = '"resolve": { "dedupe": ["react", "react-dom"] }'
        elif f.rule_id == "P1":
            suggestion["snippet"] = '// Remove empty plugins array or add plugins'
        elif f.rule_id == "S5":
            suggestion["snippet"] = "import { defineConfig } from 'vite'\nexport default defineConfig({ ... })"
        elif f.rule_id == "V4":
            suggestion["snippet"] = ('"server": { "https": { '
                '"key": "./certs/key.pem", "cert": "./certs/cert.pem" } }')
        elif f.rule_id == "X3":
            suggestion["snippet"] = '"build": { "chunkSizeWarningLimit": 500 }'
        elif f.rule_id == "B4":
            suggestion["snippet"] = '"build": { "sourcemap": true }'

        suggestions.append(suggestion)

    return suggestions


# ---------------------------------------------------------------------------
# Summary helper
# ---------------------------------------------------------------------------

def _summary_counts(findings: list) -> dict:
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    return {"errors": errors, "warnings": warnings, "infos": infos, "total": len(findings)}


def _summary_text(findings: list) -> str:
    c = _summary_counts(findings)
    parts = []
    if c["errors"]:
        parts.append(f"{c['errors']} error(s)")
    if c["warnings"]:
        parts.append(f"{c['warnings']} warning(s)")
    if c["infos"]:
        parts.append(f"{c['infos']} info")
    return ", ".join(parts) if parts else "No issues found"


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_validate(data: dict, path: str) -> dict:
    """Full validation with summary."""
    findings = validate_all(data)
    errors = [f for f in findings if f.severity == "error"]
    return {
        "command": "validate",
        "file": path,
        "valid": len(errors) == 0,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_check(data: dict, path: str) -> dict:
    """Quick check — errors and warnings only."""
    findings = validate_all(data)
    filtered = [f for f in findings if f.severity in ("error", "warning")]
    return {
        "command": "check",
        "file": path,
        "passed": all(f.severity != "error" for f in findings),
        "findings": [f.to_dict() for f in filtered],
        "counts": _summary_counts(filtered),
        "summary": _summary_text(filtered),
    }


def cmd_explain(data, path: str) -> dict:
    """Explain all rules with their categories and severity."""
    rules = []
    for rule_id in sorted(RULE_EXPLANATIONS.keys()):
        info = RULE_EXPLANATIONS[rule_id]
        rules.append({
            "rule_id": rule_id,
            "name": info["name"],
            "category": info["category"],
            "severity": info["severity"],
            "description": info["description"],
            "fix": info["fix"],
        })
    return {
        "command": "explain",
        "file": path,
        "rules": rules,
        "total_rules": len(rules),
    }


def cmd_suggest(data: dict, path: str) -> dict:
    """Run validation and generate fix suggestions."""
    findings = validate_all(data)
    suggestions = generate_suggestions(data, findings)
    return {
        "command": "suggest",
        "file": path,
        "suggestions": suggestions,
        "total": len(suggestions),
        "summary": _summary_text(findings),
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    title = f"vite.config {cmd} — {path}"
    lines.append(title)
    lines.append("=" * len(title))

    if cmd == "explain":
        for rule in result.get("rules", []):
            lines.append("")
            lines.append(f"  {rule['rule_id']}: {rule['name']} [{rule['category']}] ({rule['severity']})")
            lines.append(f"    {rule['description']}")
            lines.append(f"    Fix: {rule['fix']}")
        lines.append("")
        lines.append(f"Total rules: {result.get('total_rules', 0)}")
        return "\n".join(lines)

    if cmd == "suggest":
        suggestions = result.get("suggestions", [])
        if not suggestions:
            lines.append("[OK] No suggestions — Vite config looks good")
        else:
            for s in suggestions:
                sev = s["severity"].upper().ljust(7)
                lines.append(f"[{sev}] {s['rule_id']}: {s['problem']}")
                lines.append(f"         Fix: {s['fix']}")
                if "snippet" in s:
                    lines.append(f"         Add: {s['snippet']}")
                lines.append("")
        lines.append(f"Summary: {result.get('summary', '')}")
        return "\n".join(lines)

    # validate / check
    findings = result.get("findings", [])
    if not findings:
        lines.append("[OK] No issues found")
    else:
        for f in findings:
            sev = f["severity"].upper().ljust(7)
            lines.append(f"[{sev}] {f['rule_id']}: {f['message']}")
            if f.get("detail"):
                lines.append(f"         {f['detail']}")

    if cmd == "validate":
        valid_str = "VALID" if result.get("valid") else "INVALID"
        lines.append("")
        lines.append(f"Result: {valid_str}")

    if cmd == "check":
        passed_str = "PASSED" if result.get("passed") else "FAILED"
        lines.append("")
        lines.append(f"Result: {passed_str}")

    summary = result.get("summary")
    if summary:
        lines.append(f"Summary: {summary}")

    return "\n".join(lines)


def format_json(result: dict) -> str:
    return json.dumps(result, indent=2)


def format_summary(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    lines.append(f"vite.config {cmd}: {path}")

    if cmd == "explain":
        lines.append(f"Rules: {result.get('total_rules', 0)}")
        categories = {}
        for rule in result.get("rules", []):
            cat = rule["category"]
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items()):
            lines.append(f"  {cat}: {count} rules")
        return "\n".join(lines)

    counts = result.get("counts", {})
    lines.append(f"Errors: {counts.get('errors', 0)}")
    lines.append(f"Warnings: {counts.get('warnings', 0)}")
    lines.append(f"Info: {counts.get('infos', 0)}")

    if "valid" in result:
        lines.append(f"Valid: {'yes' if result['valid'] else 'no'}")
    if "passed" in result:
        lines.append(f"Passed: {'yes' if result['passed'] else 'no'}")

    if cmd == "suggest":
        lines.append(f"Suggestions: {result.get('total', 0)}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate Vite configuration files (JSON-exported)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Commands:
  validate   Full validation with all rules
  check      Quick check (errors and warnings only)
  explain    Show all rules with descriptions
  suggest    Run validation and propose fixes

Export your vite.config.ts to JSON first:
  node -e "import('./vite.config.ts').then(m => console.log(JSON.stringify(m.default)))" > vite.config.json

Examples:
  python3 vite_config_validator.py validate vite.config.json
  python3 vite_config_validator.py validate vite.config.json --strict
  python3 vite_config_validator.py check vite.config.json --format json
  python3 vite_config_validator.py explain vite.config.json
  python3 vite_config_validator.py suggest vite.config.json --format summary
"""
    )
    parser.add_argument("command", choices=["validate", "check", "explain", "suggest"],
                        help="Command to run")
    parser.add_argument("file", help="Path to Vite config JSON file")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (CI mode)")
    parser.add_argument("--format", choices=["text", "json", "summary"], default="text",
                        help="Output format (default: text)")

    args = parser.parse_args()

    # For 'explain', we don't need a valid file (but accept the arg for consistency)
    if args.command == "explain":
        result = cmd_explain(None, args.file)
    else:
        # Load and parse file
        data, parse_error = load_config(args.file)
        if parse_error:
            result = {
                "command": args.command,
                "file": args.file,
                "findings": [parse_error.to_dict()],
                "counts": {"errors": 1, "warnings": 0, "infos": 0, "total": 1},
                "summary": "1 error(s)",
            }
            if args.command == "validate":
                result["valid"] = False
            elif args.command == "check":
                result["passed"] = False
            elif args.command == "suggest":
                result["suggestions"] = []
                result["total"] = 0

            formatter = {"text": format_text, "json": format_json, "summary": format_summary}
            print(formatter[args.format](result))
            sys.exit(2)

        # Run command
        if args.command == "validate":
            result = cmd_validate(data, args.file)
        elif args.command == "check":
            result = cmd_check(data, args.file)
        elif args.command == "suggest":
            result = cmd_suggest(data, args.file)

    # Format output
    formatter = {"text": format_text, "json": format_json, "summary": format_summary}
    print(formatter[args.format](result))

    # Exit code
    if args.command == "explain":
        sys.exit(0)

    findings = result.get("findings", [])
    has_errors = any(f["severity"] == "error" for f in findings)
    has_warnings = any(f["severity"] == "warning" for f in findings)

    if has_errors:
        sys.exit(1)
    if args.strict and has_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
