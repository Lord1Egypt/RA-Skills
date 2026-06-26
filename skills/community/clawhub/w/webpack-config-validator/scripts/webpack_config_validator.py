#!/usr/bin/env python3
"""
Webpack Config Validator
Validate JSON-exported webpack configuration files for structural correctness,
entry/output issues, module/loader problems, plugin hygiene, optimization hints,
and best practices.
Usage: python3 webpack_config_validator.py <command> <file> [--strict] [--format text|json|summary] [--mode production|development]
Commands: validate, check, explain, suggest

Note: webpack configs are JS/TS. This validator works with JSON-exported configs.
Export via: node -e "console.log(JSON.stringify(require('./webpack.config.js')))"
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

KNOWN_TOP_LEVEL_KEYS = {
    "entry", "output", "module", "plugins", "resolve", "optimization",
    "devServer", "devtool", "mode", "target", "externals", "context",
    "node", "performance", "stats", "watch", "watchOptions",
    "experiments", "infrastructureLogging", "cache", "snapshot",
    "name", "dependencies", "loader", "parallelism", "profile",
    "recordsPath", "recordsInputPath", "recordsOutputPath",
    "amd", "bail", "ignoreWarnings",
}

DEPRECATED_TOP_LEVEL_KEYS = {
    "loaders": "Use 'module.rules' instead (deprecated since webpack 2).",
}

DEPRECATED_LOADERS: dict[str, str] = {
    "raw-loader": "asset/source (webpack 5 built-in)",
    "url-loader": "asset (webpack 5 built-in)",
    "file-loader": "asset/resource (webpack 5 built-in)",
    "json-loader": "built-in since webpack 2 (remove entirely)",
}

DEPRECATED_PLUGINS: dict[str, str] = {
    "UglifyJsPlugin": "TerserPlugin (terser-webpack-plugin)",
    "UglifyJSPlugin": "TerserPlugin (terser-webpack-plugin)",
    "ExtractTextPlugin": "MiniCssExtractPlugin (mini-css-extract-plugin)",
    "CommonsChunkPlugin": "optimization.splitChunks (webpack 4+ built-in)",
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

def load_config(path: str) -> tuple[dict | None, Finding | None]:
    """Load and parse a JSON webpack config file. Returns (data, error_finding)."""
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
            f"Expected a JSON object at top level, got {type(data).__name__}")

    return data, None


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------

def check_structure(data: dict) -> list[Finding]:
    """S4, S5: Check required fields and unknown/deprecated top-level keys."""
    findings: list[Finding] = []

    # S4: Missing required fields (entry, output)
    missing = []
    if "entry" not in data:
        missing.append("entry")
    if "output" not in data:
        missing.append("output")
    if missing:
        findings.append(Finding("S4", "error",
            f"Missing required top-level field(s): {', '.join(missing)}",
            "Every webpack config needs at least 'entry' and 'output'."))

    # S5: Unknown/deprecated top-level keys
    for key in data:
        if key in DEPRECATED_TOP_LEVEL_KEYS:
            findings.append(Finding("S5", "warning",
                f"Deprecated top-level key '{key}'",
                DEPRECATED_TOP_LEVEL_KEYS[key]))
        elif key not in KNOWN_TOP_LEVEL_KEYS:
            findings.append(Finding("S5", "info",
                f"Unknown top-level key '{key}' — may be a typo or custom property",
                "Check webpack documentation for valid configuration keys."))

    return findings


def check_entry_output(data: dict, mode: str | None) -> list[Finding]:
    """E1-E4: Check entry and output configuration."""
    findings: list[Finding] = []

    # E1: Missing entry point
    entry = data.get("entry")
    if entry is not None:
        if isinstance(entry, str) and entry.strip() == "":
            findings.append(Finding("E1", "error",
                "Entry point is an empty string",
                "Specify a valid entry file, e.g. './src/index.js'."))
        elif isinstance(entry, dict) and len(entry) == 0:
            findings.append(Finding("E1", "error",
                "Entry is an empty object — no entry points defined",
                "Add at least one entry point, e.g. { \"main\": \"./src/index.js\" }."))
        elif isinstance(entry, list) and len(entry) == 0:
            findings.append(Finding("E1", "error",
                "Entry is an empty array — no entry points defined",
                "Add at least one entry file to the array."))

    # E2: Output without path
    output = data.get("output")
    if isinstance(output, dict):
        if "path" not in output:
            findings.append(Finding("E2", "error",
                "Output section missing 'path' property",
                "Add output.path — e.g. path.resolve(__dirname, 'dist'). "
                "In JSON export this appears as an absolute path string."))

        # E3: Output filename without hash for production
        filename = output.get("filename", "")
        effective_mode = mode or data.get("mode")
        if isinstance(filename, str) and effective_mode == "production":
            has_hash = any(h in filename for h in [
                "[hash]", "[contenthash]", "[chunkhash]", "[fullhash]"
            ])
            if not has_hash and filename:
                findings.append(Finding("E3", "warning",
                    f"Output filename '{filename}' has no content hash for production",
                    "Use [contenthash] in filename for long-term caching, "
                    "e.g. '[name].[contenthash].js'."))

        # E4: publicPath not set
        if "publicPath" not in output:
            findings.append(Finding("E4", "warning",
                "output.publicPath not set",
                "Set publicPath to ensure assets are loaded from the correct URL. "
                "Common values: '/', '/assets/', 'auto'."))

    return findings


def _extract_loaders(rule: dict) -> list[str]:
    """Extract loader names from a module rule."""
    loaders: list[str] = []
    # use / loader (single)
    for key in ("use", "loader"):
        val = rule.get(key)
        if isinstance(val, str):
            loaders.append(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, str):
                    loaders.append(item)
                elif isinstance(item, dict):
                    loader_name = item.get("loader", "")
                    if isinstance(loader_name, str) and loader_name:
                        loaders.append(loader_name)
        elif isinstance(val, dict):
            loader_name = val.get("loader", "")
            if isinstance(loader_name, str) and loader_name:
                loaders.append(loader_name)
    return loaders


def _extract_test_pattern(rule: dict) -> str | None:
    """Extract the test regex pattern from a rule (as string)."""
    test_val = rule.get("test")
    if test_val is None:
        return None
    if isinstance(test_val, str):
        return test_val
    if isinstance(test_val, dict):
        # JSON-serialized RegExp sometimes appears as { "source": "...", "flags": "..." }
        return test_val.get("source", str(test_val))
    return str(test_val)


def check_module_rules(data: dict) -> list[Finding]:
    """M1-M4: Check module.rules configuration."""
    findings: list[Finding] = []
    module = data.get("module")

    if not isinstance(module, dict):
        return findings

    rules = module.get("rules", [])
    if not isinstance(rules, list):
        return findings

    seen_tests: dict[str, list[str]] = {}  # test_pattern -> [loaders]
    all_loaders: list[str] = []
    has_js_ts_loader = False

    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue

        # M1: Rules without test pattern
        test_pattern = _extract_test_pattern(rule)
        if test_pattern is None:
            # oneOf / rules nesting is valid without test
            if "oneOf" not in rule and "rules" not in rule:
                findings.append(Finding("M1", "warning",
                    f"Rule at index {i} has no 'test' pattern",
                    "Every rule should have a 'test' to match file types, "
                    "e.g. test: /\\.js$/."))

        # Extract loaders for further checks
        loaders = _extract_loaders(rule)
        all_loaders.extend(loaders)

        # Track test -> loaders for M2
        if test_pattern is not None:
            key = test_pattern
            if key not in seen_tests:
                seen_tests[key] = []
            seen_tests[key].extend(loaders)

        # M3: Deprecated loaders
        for loader in loaders:
            # Normalize loader name (strip -loader suffix variations, query params)
            loader_base = loader.split("?")[0].split("!")[0].strip()
            if loader_base in DEPRECATED_LOADERS:
                replacement = DEPRECATED_LOADERS[loader_base]
                findings.append(Finding("M3", "warning",
                    f"Deprecated loader '{loader_base}' in rule {i}",
                    f"Replace with {replacement}."))

        # Check if this rule handles JS/TS
        if test_pattern is not None:
            test_str = str(test_pattern).lower()
            if any(ext in test_str for ext in [".js", ".jsx", ".ts", ".tsx", "js", "ts"]):
                for loader in loaders:
                    loader_base = loader.split("?")[0].split("!")[0].strip()
                    if loader_base in ("babel-loader", "ts-loader", "esbuild-loader",
                                       "swc-loader", "@babel/register"):
                        has_js_ts_loader = True

        # Check nested oneOf rules
        one_of = rule.get("oneOf", [])
        if isinstance(one_of, list):
            for j, sub_rule in enumerate(one_of):
                if isinstance(sub_rule, dict):
                    sub_loaders = _extract_loaders(sub_rule)
                    all_loaders.extend(sub_loaders)
                    for loader in sub_loaders:
                        loader_base = loader.split("?")[0].split("!")[0].strip()
                        if loader_base in DEPRECATED_LOADERS:
                            replacement = DEPRECATED_LOADERS[loader_base]
                            findings.append(Finding("M3", "warning",
                                f"Deprecated loader '{loader_base}' in rule {i} oneOf[{j}]",
                                f"Replace with {replacement}."))
                        if loader_base in ("babel-loader", "ts-loader", "esbuild-loader",
                                           "swc-loader", "@babel/register"):
                            has_js_ts_loader = True

    # M2: Duplicate loader for same test
    for test_pattern, loaders in seen_tests.items():
        loader_counts: dict[str, int] = {}
        for loader in loaders:
            loader_base = loader.split("?")[0].split("!")[0].strip()
            loader_counts[loader_base] = loader_counts.get(loader_base, 0) + 1
        for loader_name, count in loader_counts.items():
            if count > 1 and loader_name:
                findings.append(Finding("M2", "warning",
                    f"Loader '{loader_name}' appears {count} times for test '{test_pattern}'",
                    "Duplicate loaders cause double processing. Remove the duplicate."))

    # M4: Missing babel-loader or ts-loader for JS/TS files
    if rules and not has_js_ts_loader:
        findings.append(Finding("M4", "info",
            "No babel-loader, ts-loader, esbuild-loader, or swc-loader found for JS/TS files",
            "If your project uses modern JS/TS, add a transpilation loader. "
            "This may be intentional if using only vanilla JS."))

    return findings


def _extract_plugin_name(plugin: Any) -> str | None:
    """Extract plugin constructor name from JSON-serialized plugin."""
    if isinstance(plugin, dict):
        # Common JSON serialization patterns:
        # { "constructor": "HtmlWebpackPlugin", ... }
        # { "_pluginName": "HtmlWebpackPlugin", ... }
        # { "pluginName": "HtmlWebpackPlugin", ... }
        for key in ("constructor", "_pluginName", "pluginName", "__pluginName",
                     "name", "_name"):
            val = plugin.get(key)
            if isinstance(val, str) and val:
                return val
        # Fallback: check if there's a key matching *Plugin pattern
        for key in plugin:
            if isinstance(key, str) and key.endswith("Plugin"):
                return key
    if isinstance(plugin, str):
        return plugin
    return None


def check_plugins(data: dict) -> list[Finding]:
    """P1-P4: Check plugin configuration."""
    findings: list[Finding] = []
    plugins = data.get("plugins")

    if not isinstance(plugins, list):
        return findings

    seen_plugins: dict[str, int] = {}
    has_mini_css_plugin = False
    has_html_plugin = False
    html_plugin_has_template = False

    for i, plugin in enumerate(plugins):
        name = _extract_plugin_name(plugin)

        if name:
            # P1: Deprecated plugins
            if name in DEPRECATED_PLUGINS:
                replacement = DEPRECATED_PLUGINS[name]
                findings.append(Finding("P1", "error",
                    f"Deprecated plugin '{name}' at index {i}",
                    f"Replace with {replacement}."))

            # Track for P2 duplicate check
            seen_plugins[name] = seen_plugins.get(name, 0) + 1

            # P3: HtmlWebpackPlugin without template
            if "HtmlWebpackPlugin" in name or "html-webpack-plugin" in name.lower():
                has_html_plugin = True
                if isinstance(plugin, dict):
                    options = plugin.get("options", plugin.get("userOptions", plugin))
                    if isinstance(options, dict) and "template" in options:
                        html_plugin_has_template = True

            # Track MiniCssExtractPlugin
            if "MiniCssExtractPlugin" in name or "mini-css-extract-plugin" in name.lower():
                has_mini_css_plugin = True

    # P2: Duplicate plugin instances
    for name, count in seen_plugins.items():
        if count > 1:
            findings.append(Finding("P2", "warning",
                f"Plugin '{name}' instantiated {count} times",
                "Multiple instances of the same plugin can cause conflicts. "
                "Usually only one instance is needed."))

    # P3: HtmlWebpackPlugin without template
    if has_html_plugin and not html_plugin_has_template:
        findings.append(Finding("P3", "info",
            "HtmlWebpackPlugin used without explicit template",
            "Without a template, the default HTML is generated. "
            "Consider specifying template: './src/index.html' for control."))

    # P4: MiniCssExtractPlugin without corresponding loader
    if has_mini_css_plugin:
        module = data.get("module", {})
        rules = module.get("rules", []) if isinstance(module, dict) else []
        has_extract_loader = False

        def _check_loaders_for_extract(rule_list: list) -> bool:
            for rule in rule_list:
                if not isinstance(rule, dict):
                    continue
                loaders = _extract_loaders(rule)
                for loader in loaders:
                    loader_base = loader.split("?")[0].split("!")[0].strip()
                    if "mini-css-extract-plugin" in loader_base.lower() or \
                       "MiniCssExtractPlugin" in loader:
                        return True
                # Check oneOf
                one_of = rule.get("oneOf", [])
                if isinstance(one_of, list) and _check_loaders_for_extract(one_of):
                    return True
            return False

        has_extract_loader = _check_loaders_for_extract(rules)

        if not has_extract_loader:
            findings.append(Finding("P4", "warning",
                "MiniCssExtractPlugin present but no corresponding loader in module.rules",
                "Add MiniCssExtractPlugin.loader to your CSS rule's 'use' array "
                "to extract CSS into separate files."))

    return findings


def check_optimization(data: dict, mode: str | None) -> list[Finding]:
    """O1-O3: Check optimization configuration."""
    findings: list[Finding] = []
    optimization = data.get("optimization", {})
    effective_mode = mode or data.get("mode")

    # O1: Missing splitChunks
    if not isinstance(optimization, dict) or "splitChunks" not in optimization:
        findings.append(Finding("O1", "info",
            "No optimization.splitChunks configuration",
            "splitChunks enables automatic code splitting for shared dependencies. "
            "Add optimization: { splitChunks: { chunks: 'all' } } for better caching."))

    # O2: Missing minimizer
    if not isinstance(optimization, dict) or "minimizer" not in optimization:
        findings.append(Finding("O2", "info",
            "No custom optimization.minimizer configured",
            "Webpack uses TerserPlugin by default in production. "
            "Customize minimizer to add CSS minification or tune settings."))

    # O3: devtool set to eval/source-map in production
    devtool = data.get("devtool")
    if devtool is not None and effective_mode == "production":
        devtool_str = str(devtool).lower()
        if "eval" in devtool_str:
            findings.append(Finding("O3", "warning",
                f"devtool '{devtool}' uses eval in production mode",
                "eval-based source maps expose source code and are slow. "
                "Use 'source-map' or 'hidden-source-map' for production."))
        elif devtool_str == "source-map":
            findings.append(Finding("O3", "info",
                "devtool 'source-map' in production exposes full source maps",
                "Consider 'hidden-source-map' or 'nosources-source-map' "
                "to avoid exposing source code to end users."))

    return findings


def check_best_practices(data: dict) -> list[Finding]:
    """B1-B4: Check best practices."""
    findings: list[Finding] = []

    # B1: Missing resolve.extensions
    resolve = data.get("resolve", {})
    if isinstance(resolve, dict):
        if "extensions" not in resolve:
            findings.append(Finding("B1", "info",
                "Missing resolve.extensions",
                "Set resolve.extensions to auto-resolve imports without file extensions, "
                "e.g. ['.js', '.jsx', '.ts', '.tsx', '.json']."))
    else:
        findings.append(Finding("B1", "info",
            "Missing resolve configuration",
            "Add resolve.extensions to auto-resolve imports, "
            "e.g. resolve: { extensions: ['.js', '.jsx', '.ts', '.tsx'] }."))

    # B2: Absolute paths in config (outside of output.path which is expected)
    _check_absolute_paths(data, findings, path_prefix="", skip_keys={"path"})

    # B3: No mode set
    if "mode" not in data:
        findings.append(Finding("B3", "warning",
            "No 'mode' set (development/production/none)",
            "Set mode to enable webpack's built-in optimizations. "
            "Without mode, webpack defaults to 'production' with a warning."))

    # B4: Missing devServer hint
    if "devServer" not in data:
        findings.append(Finding("B4", "info",
            "No devServer configuration",
            "Add devServer for local development with hot module replacement. "
            "Example: devServer: { port: 3000, hot: true }."))

    return findings


def _check_absolute_paths(data: Any, findings: list[Finding], path_prefix: str,
                           skip_keys: set[str] | None = None, depth: int = 0) -> None:
    """Recursively check for hardcoded absolute paths in config values."""
    if depth > 10:  # prevent deep recursion
        return

    if skip_keys is None:
        skip_keys = set()

    if isinstance(data, dict):
        for key, val in data.items():
            if key in skip_keys and path_prefix == "output":
                continue  # output.path is expected to be absolute
            current_path = f"{path_prefix}.{key}" if path_prefix else key
            _check_absolute_paths(val, findings, current_path, skip_keys, depth + 1)
    elif isinstance(data, list):
        for i, val in enumerate(data):
            current_path = f"{path_prefix}[{i}]"
            _check_absolute_paths(val, findings, current_path, skip_keys, depth + 1)
    elif isinstance(data, str):
        # Check for absolute filesystem paths (not URLs)
        if re.match(r'^(/[a-zA-Z]|[A-Z]:\\)', data) and not data.startswith("http"):
            # Skip output.path — it's supposed to be absolute
            if path_prefix.startswith("output.path"):
                return
            findings.append(Finding("B2", "warning",
                f"Hardcoded absolute path at '{path_prefix}': {data[:80]}",
                "Use path.resolve() or relative paths for portability across machines."))


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def validate_all(data: dict, mode: str | None = None) -> list[Finding]:
    """Run all checks and return combined findings."""
    findings: list[Finding] = []
    findings.extend(check_structure(data))
    findings.extend(check_entry_output(data, mode))
    findings.extend(check_module_rules(data))
    findings.extend(check_plugins(data))
    findings.extend(check_optimization(data, mode))
    findings.extend(check_best_practices(data))
    return findings


# ---------------------------------------------------------------------------
# Rule explanations (for 'explain' command)
# ---------------------------------------------------------------------------

RULE_EXPLANATIONS: dict[str, dict[str, str]] = {
    "S1": {
        "name": "File Not Found",
        "category": "Structure",
        "severity": "error",
        "description": "The webpack config JSON file does not exist or cannot be read.",
        "fix": "Ensure the file path is correct and the file has read permissions. "
               "Export with: node -e \"console.log(JSON.stringify(require('./webpack.config.js')))\" > config.json",
    },
    "S2": {
        "name": "Empty Config",
        "category": "Structure",
        "severity": "error",
        "description": "The config file is empty (zero bytes or only whitespace).",
        "fix": "Re-export the webpack config to JSON. The file must contain a valid JSON object.",
    },
    "S3": {
        "name": "Invalid JSON",
        "category": "Structure",
        "severity": "error",
        "description": "The file contains invalid JSON syntax that cannot be parsed.",
        "fix": "Ensure the export produces valid JSON. Functions and RegExp objects are not JSON-serializable "
               "and must be converted to strings.",
    },
    "S4": {
        "name": "Missing Required Fields",
        "category": "Structure",
        "severity": "error",
        "description": "Missing 'entry' or 'output' — the two essential webpack config fields.",
        "fix": "Add entry (string, array, or object) and output (object with path and filename).",
    },
    "S5": {
        "name": "Unknown/Deprecated Keys",
        "category": "Structure",
        "severity": "warning/info",
        "description": "Top-level key is deprecated (e.g. 'loaders') or not recognized by webpack.",
        "fix": "Remove or rename deprecated keys. Check webpack docs for valid configuration options.",
    },
    "E1": {
        "name": "Empty Entry Point",
        "category": "Entry/Output",
        "severity": "error",
        "description": "Entry point is defined but empty (empty string, object, or array).",
        "fix": "Specify at least one entry file, e.g. entry: './src/index.js'.",
    },
    "E2": {
        "name": "Output Missing Path",
        "category": "Entry/Output",
        "severity": "error",
        "description": "Output section exists but has no 'path' property.",
        "fix": "Add output.path with an absolute directory path for the build output.",
    },
    "E3": {
        "name": "No Content Hash in Production",
        "category": "Entry/Output",
        "severity": "warning",
        "description": "Output filename lacks a content hash token in production mode.",
        "fix": "Use [contenthash] in output.filename for cache busting, e.g. '[name].[contenthash].js'.",
    },
    "E4": {
        "name": "publicPath Not Set",
        "category": "Entry/Output",
        "severity": "warning",
        "description": "output.publicPath is not configured, which can cause asset loading issues.",
        "fix": "Set output.publicPath to the URL path where assets will be served, e.g. '/' or '/assets/'.",
    },
    "M1": {
        "name": "Rule Without Test",
        "category": "Module/Rules",
        "severity": "warning",
        "description": "A module rule has no 'test' pattern to match files.",
        "fix": "Add a test property with a regex pattern, e.g. test: /\\.js$/.",
    },
    "M2": {
        "name": "Duplicate Loader",
        "category": "Module/Rules",
        "severity": "warning",
        "description": "Same loader appears multiple times for the same test pattern.",
        "fix": "Remove the duplicate loader to avoid double processing.",
    },
    "M3": {
        "name": "Deprecated Loader",
        "category": "Module/Rules",
        "severity": "warning",
        "description": "Using a loader that is deprecated in webpack 5 (raw-loader, url-loader, file-loader, json-loader).",
        "fix": "Replace with webpack 5 asset modules: asset/source, asset, asset/resource.",
    },
    "M4": {
        "name": "No JS/TS Transpilation Loader",
        "category": "Module/Rules",
        "severity": "info",
        "description": "No babel-loader, ts-loader, esbuild-loader, or swc-loader found for JS/TS files.",
        "fix": "Add a transpilation loader if using modern JS/TS syntax. "
               "Example: { test: /\\.tsx?$/, use: 'ts-loader' }.",
    },
    "P1": {
        "name": "Deprecated Plugin",
        "category": "Plugins",
        "severity": "error",
        "description": "Using a plugin that is deprecated or removed in webpack 4/5.",
        "fix": "Replace with the modern equivalent (TerserPlugin, MiniCssExtractPlugin, splitChunks).",
    },
    "P2": {
        "name": "Duplicate Plugin",
        "category": "Plugins",
        "severity": "warning",
        "description": "Same plugin instantiated multiple times, which can cause conflicts.",
        "fix": "Remove duplicate plugin instances. Usually only one instance per plugin is needed.",
    },
    "P3": {
        "name": "HtmlWebpackPlugin Without Template",
        "category": "Plugins",
        "severity": "info",
        "description": "HtmlWebpackPlugin is used without an explicit template file.",
        "fix": "Add template: './src/index.html' to HtmlWebpackPlugin options for control over the HTML.",
    },
    "P4": {
        "name": "MiniCssExtractPlugin Without Loader",
        "category": "Plugins",
        "severity": "warning",
        "description": "MiniCssExtractPlugin is present but its loader is not found in module.rules.",
        "fix": "Add MiniCssExtractPlugin.loader to your CSS rule's 'use' array to extract CSS into files.",
    },
    "O1": {
        "name": "No splitChunks",
        "category": "Optimization",
        "severity": "info",
        "description": "No optimization.splitChunks configuration for code splitting.",
        "fix": "Add optimization.splitChunks: { chunks: 'all' } for automatic vendor splitting.",
    },
    "O2": {
        "name": "No Custom Minimizer",
        "category": "Optimization",
        "severity": "info",
        "description": "No custom minimizer configured. Webpack uses TerserPlugin by default in production.",
        "fix": "Customize minimizer to add CSS minification or tune JS minification settings.",
    },
    "O3": {
        "name": "Devtool in Production",
        "category": "Optimization",
        "severity": "warning/info",
        "description": "devtool setting may expose source code or slow down production builds.",
        "fix": "Use 'hidden-source-map' or 'nosources-source-map' for production.",
    },
    "B1": {
        "name": "Missing resolve.extensions",
        "category": "Best Practices",
        "severity": "info",
        "description": "resolve.extensions not configured — imports require full file extensions.",
        "fix": "Add resolve.extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'].",
    },
    "B2": {
        "name": "Absolute Paths",
        "category": "Best Practices",
        "severity": "warning",
        "description": "Hardcoded absolute filesystem paths reduce config portability.",
        "fix": "Use path.resolve(__dirname, 'relative/path') or relative paths instead.",
    },
    "B3": {
        "name": "No Mode Set",
        "category": "Best Practices",
        "severity": "warning",
        "description": "No mode set (development/production/none). Webpack defaults to 'production' with a warning.",
        "fix": "Set mode: 'production' or mode: 'development' explicitly.",
    },
    "B4": {
        "name": "No devServer Config",
        "category": "Best Practices",
        "severity": "info",
        "description": "No devServer configuration for local development.",
        "fix": "Add devServer: { port: 3000, hot: true } for hot module replacement during development.",
    },
}


# ---------------------------------------------------------------------------
# Suggestion engine (for 'suggest' command)
# ---------------------------------------------------------------------------

def generate_suggestions(data: dict, findings: list[Finding]) -> list[dict]:
    """Generate actionable fix suggestions from findings."""
    suggestions: list[dict] = []

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

        # Add concrete JSON snippets for common fixes
        if f.rule_id == "S4":
            suggestion["snippet"] = '{ "entry": "./src/index.js", "output": { "path": "/absolute/dist", "filename": "bundle.js" } }'
        elif f.rule_id == "E1":
            suggestion["snippet"] = '"entry": "./src/index.js"'
        elif f.rule_id == "E2":
            suggestion["snippet"] = '"output": { "path": "/absolute/path/to/dist", "filename": "[name].[contenthash].js" }'
        elif f.rule_id == "E3":
            suggestion["snippet"] = '"filename": "[name].[contenthash].js"'
        elif f.rule_id == "E4":
            suggestion["snippet"] = '"publicPath": "/"'
        elif f.rule_id == "B1":
            suggestion["snippet"] = '"resolve": { "extensions": [".js", ".jsx", ".ts", ".tsx", ".json"] }'
        elif f.rule_id == "B3":
            suggestion["snippet"] = '"mode": "production"'
        elif f.rule_id == "B4":
            suggestion["snippet"] = '"devServer": { "port": 3000, "hot": true }'
        elif f.rule_id == "O1":
            suggestion["snippet"] = '"optimization": { "splitChunks": { "chunks": "all" } }'
        elif f.rule_id == "M3":
            # Extract deprecated loader name
            match = re.search(r"'([^']+)'", f.message)
            if match:
                loader = match.group(1)
                if loader in DEPRECATED_LOADERS:
                    suggestion["snippet"] = f'"type": "{DEPRECATED_LOADERS[loader].split(" ")[0]}"  // replaces {loader}'
        elif f.rule_id == "P1":
            match = re.search(r"'([^']+)'", f.message)
            if match:
                plugin = match.group(1)
                if plugin in DEPRECATED_PLUGINS:
                    suggestion["snippet"] = f'// Replace {plugin} with {DEPRECATED_PLUGINS[plugin]}'

        suggestions.append(suggestion)

    return suggestions


# ---------------------------------------------------------------------------
# Summary helper
# ---------------------------------------------------------------------------

def _summary_counts(findings: list[Finding]) -> dict:
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    return {"errors": errors, "warnings": warnings, "infos": infos, "total": len(findings)}


def _summary_text(findings: list[Finding]) -> str:
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

def cmd_validate(data: dict, path: str, mode: str | None) -> dict:
    """Full validation with summary."""
    findings = validate_all(data, mode)
    errors = [f for f in findings if f.severity == "error"]
    return {
        "command": "validate",
        "file": path,
        "valid": len(errors) == 0,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_check(data: dict, path: str, mode: str | None) -> dict:
    """Quick check — errors and warnings only."""
    findings = validate_all(data, mode)
    filtered = [f for f in findings if f.severity in ("error", "warning")]
    return {
        "command": "check",
        "file": path,
        "passed": all(f.severity != "error" for f in findings),
        "findings": [f.to_dict() for f in filtered],
        "counts": _summary_counts(filtered),
        "summary": _summary_text(filtered),
    }


def cmd_explain(data: dict | None, path: str) -> dict:
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


def cmd_suggest(data: dict, path: str, mode: str | None) -> dict:
    """Run validation and generate fix suggestions."""
    findings = validate_all(data, mode)
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
    title = f"webpack.config {cmd} — {path}"
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
            lines.append("[OK] No suggestions — webpack config looks good")
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
    lines.append(f"webpack.config {cmd}: {path}")

    if cmd == "explain":
        lines.append(f"Rules: {result.get('total_rules', 0)}")
        categories: dict[str, int] = {}
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
        description="Validate JSON-exported webpack configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Commands:
  validate   Full validation with all rules
  check      Quick check (errors and warnings only)
  explain    Show all rules with descriptions
  suggest    Run validation and propose fixes

Note: webpack configs are JS/TS. This validator works with JSON-exported configs.
Export via: node -e "console.log(JSON.stringify(require('./webpack.config.js')))" > config.json

Examples:
  python3 webpack_config_validator.py validate config.json
  python3 webpack_config_validator.py validate config.json --strict --mode production
  python3 webpack_config_validator.py check config.json --format json
  python3 webpack_config_validator.py explain config.json
  python3 webpack_config_validator.py suggest config.json --format summary
"""
    )
    parser.add_argument("command", choices=["validate", "check", "explain", "suggest"],
                        help="Command to run")
    parser.add_argument("file", help="Path to JSON-exported webpack config")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (CI mode)")
    parser.add_argument("--format", choices=["text", "json", "summary"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--mode", choices=["production", "development"], default=None,
                        help="Override mode context for mode-specific rules")

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
            result = cmd_validate(data, args.file, args.mode)
        elif args.command == "check":
            result = cmd_check(data, args.file, args.mode)
        elif args.command == "suggest":
            result = cmd_suggest(data, args.file, args.mode)

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
