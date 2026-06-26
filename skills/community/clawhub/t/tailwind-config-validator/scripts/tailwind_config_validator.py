#!/usr/bin/env python3
"""
Tailwind Config Validator
Validate JSON-exported Tailwind CSS configuration files for structural correctness,
content path issues, theme misconfiguration, dark mode problems, plugin hygiene,
and best practices.
Usage: python3 tailwind_config_validator.py <command> <file> [--strict] [--format text|json|summary]
Commands: validate, lint, content, theme

Note: Tailwind configs are JS/TS. This validator works with JSON-exported configs.
Export via: node -e "console.log(JSON.stringify(require('./tailwind.config.js')))"
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
    "content", "theme", "plugins", "presets", "darkMode", "prefix",
    "important", "separator", "corePlugins", "safelist", "blocklist",
    "future", "experimental",
}

VALID_DARK_MODE_VALUES = {"media", "class", "selector"}

DEPRECATED_OFFICIAL_PLUGINS = {
    "@tailwindcss/forms": "In Tailwind v4, @tailwindcss/forms functionality is included by default.",
    "@tailwindcss/typography": "In Tailwind v4, @tailwindcss/typography functionality is included by default.",
    "@tailwindcss/aspect-ratio": "In Tailwind v4, aspect-ratio utilities are built-in.",
    "@tailwindcss/line-clamp": "Since Tailwind v3.3, line-clamp utilities are built-in.",
}

JS_TS_EXTENSIONS = {".js", ".ts", ".cjs", ".mjs"}

# Theme keys that are commonly overridden by mistake (losing all defaults)
THEME_OVERRIDE_WARN_KEYS = {
    "colors", "spacing", "fontFamily", "fontSize", "fontWeight",
    "borderRadius", "screens", "zIndex", "opacity", "lineHeight",
    "letterSpacing", "maxWidth", "minHeight", "width", "height",
}

# CSS size units for breakpoint parsing
SIZE_UNIT_RE = re.compile(r'^(\d+(?:\.\d+)?)(px|em|rem)$')


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
    """Load and parse a JSON Tailwind config file. Returns (data, error_finding)."""
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

    # S5: Detect JS/TS config (not JSON)
    stripped = content.strip()
    if (stripped.startswith("module.exports") or
            stripped.startswith("export default") or
            stripped.startswith("export const") or
            stripped.startswith("const ") or
            stripped.startswith("import ") or
            stripped.startswith("/** @type")):
        return None, Finding("S5", "error",
            "File appears to be JS/TS, not JSON",
            "Export your Tailwind config as JSON first: "
            "node -e \"console.log(JSON.stringify(require('./tailwind.config.js')))\" > config.json")

    # S3: Invalid JSON syntax
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return None, Finding("S3", "error", f"Invalid JSON syntax: {e}")

    if not isinstance(data, dict):
        return None, Finding("S3", "error",
            f"Expected a JSON object at top level, got {type(data).__name__}")

    # S2 (variant): Empty object
    if len(data) == 0:
        return None, Finding("S2", "error",
            "Config is an empty object — no configuration defined",
            "Add at least a 'content' array for Tailwind to work.")

    return data, None


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------

def check_structure(data: dict) -> list[Finding]:
    """S4: Check for unknown top-level keys."""
    findings: list[Finding] = []

    for key in data:
        if key not in KNOWN_TOP_LEVEL_KEYS:
            findings.append(Finding("S4", "warning",
                f"Unknown top-level key '{key}' — may be a typo or unsupported property",
                f"Valid top-level keys: {', '.join(sorted(KNOWN_TOP_LEVEL_KEYS))}."))

    return findings


def check_content(data: dict) -> list[Finding]:
    """C1-C5: Check content configuration."""
    findings: list[Finding] = []

    content = data.get("content")

    # C1 / B1: Missing content paths entirely
    if content is None:
        findings.append(Finding("C1", "error",
            "Missing 'content' paths — required for tree-shaking",
            "Without content paths, Tailwind cannot purge unused CSS. "
            "Add content: ['./src/**/*.{html,js,ts,jsx,tsx}']."))
        return findings

    # Content can be an array or an object with "files" key (v3.2+)
    content_paths: list = []
    if isinstance(content, list):
        content_paths = content
    elif isinstance(content, dict):
        files = content.get("files", [])
        if isinstance(files, list):
            content_paths = files
        else:
            findings.append(Finding("C1", "error",
                "content.files is not an array",
                "content.files must be an array of glob patterns."))
            return findings
    else:
        findings.append(Finding("C1", "error",
            f"'content' must be an array or object, got {type(content).__name__}",
            "Set content to an array of glob patterns, "
            "e.g. ['./src/**/*.{html,js,ts,jsx,tsx}']."))
        return findings

    # C2: Empty content array
    if len(content_paths) == 0:
        findings.append(Finding("C2", "warning",
            "Content array is empty — no files will be scanned for class usage",
            "Add glob patterns to content, e.g. ['./src/**/*.{html,js,ts,jsx,tsx}']."))
        return findings

    for i, pattern in enumerate(content_paths):
        if not isinstance(pattern, str):
            continue

        # C3: Content paths including node_modules
        if "node_modules" in pattern:
            findings.append(Finding("C3", "warning",
                f"Content path [{i}] includes node_modules: '{pattern}'",
                "Scanning node_modules severely impacts build performance. "
                "Only include specific packages if needed."))

        # C4: Glob too broad (e.g. **/* without extension filter)
        if "**/*" in pattern:
            # Check if there's an extension filter after the glob
            after_glob = pattern.split("**/*")[-1]
            if not after_glob or after_glob == "/":
                findings.append(Finding("C4", "warning",
                    f"Content path [{i}] uses overly broad glob: '{pattern}'",
                    "Add an extension filter, e.g. '**/*.{{html,js,ts,jsx,tsx}}' "
                    "to avoid scanning unnecessary files."))

        # C5: Suspicious patterns
        if re.match(r'^\*\.\w+$', pattern):
            findings.append(Finding("C5", "info",
                f"Content path [{i}] is a shallow glob: '{pattern}'",
                "This only matches files in the current directory. "
                "Use './**/*.ext' or './src/**/*.ext' for recursive matching."))

        # C5: Bare *.css is suspicious — Tailwind doesn't scan CSS for class names
        if pattern.endswith("*.css") or pattern.endswith(".css"):
            findings.append(Finding("C5", "info",
                f"Content path [{i}] targets CSS files: '{pattern}'",
                "Tailwind scans content files for class names used in markup/JS. "
                "CSS files typically don't contain Tailwind class references."))

    return findings


def check_theme(data: dict) -> list[Finding]:
    """T1-T5: Check theme configuration."""
    findings: list[Finding] = []

    theme = data.get("theme")
    if not isinstance(theme, dict):
        return findings

    extend = theme.get("extend")
    has_extend = "extend" in theme and isinstance(extend, dict)

    # T2: Empty theme.extend
    if has_extend and len(extend) == 0:
        findings.append(Finding("T2", "info",
            "theme.extend is an empty object — no customizations defined",
            "Add custom values to theme.extend to merge with Tailwind defaults, "
            "or remove the empty extend block."))

    # T1: Overriding theme keys directly (without extend)
    for key in theme:
        if key == "extend":
            continue
        if key in THEME_OVERRIDE_WARN_KEYS:
            findings.append(Finding("T1", "warning",
                f"theme.{key} overrides all default {key} — "
                f"use theme.extend.{key} instead",
                "Placing keys directly under 'theme' replaces the entire default set. "
                "Move to 'theme.extend' to merge with defaults."))

    # T3: Invalid color values (check both theme.colors and theme.extend.colors)
    _check_color_values(theme.get("colors"), "theme.colors", findings)
    if has_extend:
        _check_color_values(extend.get("colors"), "theme.extend.colors", findings)

    # T4: String references that look like they need theme() callback
    _check_theme_references(theme, "theme", findings)
    if has_extend:
        _check_theme_references(extend, "theme.extend", findings)

    # T5: Screen breakpoints not in ascending order
    _check_screen_order(theme.get("screens"), "theme.screens", findings)
    if has_extend:
        _check_screen_order(extend.get("screens"), "theme.extend.screens", findings)

    return findings


def _check_color_values(colors: Any, path: str, findings: list[Finding]) -> None:
    """T3: Check that color values are strings (or nested color objects)."""
    if not isinstance(colors, dict):
        return

    for key, val in colors.items():
        if isinstance(val, dict):
            # Nested shade object (e.g. blue: { 100: "#...", 500: "#..." })
            for shade, shade_val in val.items():
                if not isinstance(shade_val, str):
                    findings.append(Finding("T3", "warning",
                        f"Invalid color value at {path}.{key}.{shade} "
                        f"— expected string, got {type(shade_val).__name__}",
                        "Color values must be CSS color strings "
                        "(hex, rgb, hsl, etc)."))
        elif not isinstance(val, str):
            findings.append(Finding("T3", "warning",
                f"Invalid color value at {path}.{key} "
                f"— expected string, got {type(val).__name__}",
                "Color values must be CSS color strings "
                "(hex, rgb, hsl, etc)."))


def _check_theme_references(theme_section: dict, path: str,
                             findings: list[Finding]) -> None:
    """T4: Detect string values that look like theme references without callback."""
    if not isinstance(theme_section, dict):
        return

    for key, val in theme_section.items():
        if key == "extend":
            continue
        if isinstance(val, dict):
            for sub_key, sub_val in val.items():
                if isinstance(sub_val, str) and "theme(" in sub_val:
                    findings.append(Finding("T4", "info",
                        f"String 'theme(...)' reference at {path}.{key}.{sub_key}",
                        "In JSON-exported configs, theme() callbacks are lost. "
                        "This string is likely non-functional — "
                        "replace with the actual resolved value."))


def _parse_breakpoint_px(value: Any) -> float | None:
    """Parse a breakpoint value to px. Returns None if unparseable."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = SIZE_UNIT_RE.match(value.strip())
        if match:
            num = float(match.group(1))
            unit = match.group(2)
            if unit == "px":
                return num
            elif unit == "em":
                return num * 16
            elif unit == "rem":
                return num * 16
    if isinstance(value, dict):
        # { min: "640px" } form
        min_val = value.get("min")
        if min_val is not None:
            return _parse_breakpoint_px(min_val)
    return None


def _check_screen_order(screens: Any, path: str,
                         findings: list[Finding]) -> None:
    """T5: Check that screen breakpoints are in ascending order."""
    if not isinstance(screens, dict):
        return

    prev_name = None
    prev_px = None

    for name, value in screens.items():
        px = _parse_breakpoint_px(value)
        if px is not None and prev_px is not None:
            if px < prev_px:
                findings.append(Finding("T5", "warning",
                    f"Screen '{name}' ({value}) is smaller than "
                    f"preceding '{prev_name}' at {path}",
                    "Breakpoints should be in ascending order for "
                    "mobile-first responsive design to work correctly."))
        if px is not None:
            prev_name = name
            prev_px = px


def check_dark_mode(data: dict) -> list[Finding]:
    """D1-D2: Check darkMode configuration."""
    findings: list[Finding] = []

    dark_mode = data.get("darkMode")
    if dark_mode is None:
        return findings

    # D1: Invalid darkMode value
    if isinstance(dark_mode, str):
        if dark_mode not in VALID_DARK_MODE_VALUES:
            findings.append(Finding("D1", "error",
                f"Invalid darkMode value '{dark_mode}'",
                "darkMode must be 'media', 'class', or 'selector'. "
                "For a custom selector, use ['selector', '.my-class']."))

        # D2: "class" deprecated in v3.4+
        if dark_mode == "class":
            findings.append(Finding("D2", "info",
                "darkMode 'class' is deprecated since v3.4 — use 'selector' instead",
                "The 'class' strategy still works but 'selector' is the recommended "
                "replacement. It provides more flexibility (any CSS selector, not just class)."))

    elif isinstance(dark_mode, list):
        # ["selector", ".custom-class"] form
        if len(dark_mode) != 2:
            findings.append(Finding("D1", "error",
                f"darkMode array must have exactly 2 elements, got {len(dark_mode)}",
                "Use ['selector', '.my-class'] or ['class', '.my-class'] format."))
        elif not isinstance(dark_mode[0], str) or dark_mode[0] not in ("selector", "class"):
            findings.append(Finding("D1", "error",
                f"darkMode array first element must be 'selector' or 'class', "
                f"got '{dark_mode[0]}'",
                "Use ['selector', '.my-class'] format."))
        elif not isinstance(dark_mode[1], str):
            findings.append(Finding("D1", "error",
                f"darkMode array second element must be a CSS selector string",
                "Use ['selector', '.my-class'] format."))

        # D2: "class" in array form also deprecated
        if len(dark_mode) >= 1 and dark_mode[0] == "class":
            findings.append(Finding("D2", "info",
                "darkMode ['class', ...] is deprecated since v3.4 — "
                "use ['selector', ...] instead",
                "Replace 'class' with 'selector' for forward compatibility."))
    else:
        findings.append(Finding("D1", "error",
            f"darkMode must be a string or array, got {type(dark_mode).__name__}",
            "Use 'media', 'selector', or ['selector', '.my-class']."))

    return findings


def check_plugins(data: dict) -> list[Finding]:
    """P1-P3: Check plugin configuration."""
    findings: list[Finding] = []

    plugins = data.get("plugins")
    if plugins is None:
        return findings

    # P2: Plugins not an array
    if not isinstance(plugins, list):
        findings.append(Finding("P2", "error",
            f"'plugins' must be an array, got {type(plugins).__name__}",
            "Set plugins to an array: plugins: [require('@tailwindcss/forms')]. "
            "In JSON export, plugin entries appear as strings or objects."))
        return findings

    # P1: Empty plugins array
    if len(plugins) == 0:
        findings.append(Finding("P1", "info",
            "plugins array is empty",
            "Remove the empty plugins array, or add plugins as needed."))
        return findings

    # P3: Deprecated official plugins
    for i, plugin in enumerate(plugins):
        plugin_name = None
        if isinstance(plugin, str):
            plugin_name = plugin
        elif isinstance(plugin, dict):
            # JSON-serialized plugin — look for name-like keys
            for key in ("name", "_name", "pluginName", "handler", "__plugin"):
                val = plugin.get(key)
                if isinstance(val, str) and val:
                    plugin_name = val
                    break

        if plugin_name:
            for deprecated, msg in DEPRECATED_OFFICIAL_PLUGINS.items():
                if deprecated in plugin_name:
                    findings.append(Finding("P3", "info",
                        f"Plugin '{deprecated}' at index {i} is built-in "
                        f"since Tailwind v4",
                        msg + " Remove the plugin if upgrading."))

    return findings


def check_best_practices(data: dict) -> list[Finding]:
    """B1-B6: Check best practices."""
    findings: list[Finding] = []

    # B1: No content paths at all (duplicate of C1 for the 'validate' all-rules flow)
    content = data.get("content")
    if content is None:
        findings.append(Finding("B1", "error",
            "No content paths defined — tree-shaking will not work",
            "Tailwind needs content paths to scan for used classes. "
            "Without them, either all utilities are included (huge CSS) "
            "or none are (broken styles)."))
    elif isinstance(content, list) and len(content) == 0:
        findings.append(Finding("B1", "error",
            "Content array is empty — tree-shaking will not work",
            "Add file glob patterns to content for Tailwind to scan."))
    elif isinstance(content, dict):
        files = content.get("files", [])
        if isinstance(files, list) and len(files) == 0:
            findings.append(Finding("B1", "error",
                "content.files is empty — tree-shaking will not work",
                "Add file glob patterns to content.files for Tailwind to scan."))

    # B2: important: true globally
    important = data.get("important")
    if important is True:
        findings.append(Finding("B2", "warning",
            "important: true applies !important to all utilities (anti-pattern)",
            "Prefer important: '#app' to scope specificity to a root selector "
            "instead of global !important. This avoids conflicts with third-party CSS."))

    # B3: Prefix with special characters
    prefix = data.get("prefix")
    if isinstance(prefix, str) and prefix:
        if re.search(r'[^a-zA-Z0-9_-]', prefix):
            findings.append(Finding("B3", "warning",
                f"Prefix '{prefix}' contains special characters",
                "Prefixes should only contain alphanumeric characters, hyphens, "
                "and underscores. Special characters may cause issues with "
                "CSS class name matching."))

    # B4: corePlugins disabled entirely
    core_plugins = data.get("corePlugins")
    if isinstance(core_plugins, dict) and len(core_plugins) > 0:
        all_false = all(v is False for v in core_plugins.values())
        if all_false:
            findings.append(Finding("B4", "warning",
                f"All {len(core_plugins)} corePlugins are set to false "
                f"— Tailwind generates no utilities",
                "This disables all utility generation. If intentional, "
                "consider using a minimal CSS framework instead."))
    elif core_plugins is False:
        findings.append(Finding("B4", "warning",
            "corePlugins set to false — all core plugins disabled",
            "This disables all utility generation. "
            "Use an object to disable specific plugins selectively."))

    # B5: Large safelist
    safelist = data.get("safelist")
    if isinstance(safelist, list) and len(safelist) > 50:
        findings.append(Finding("B5", "warning",
            f"Large safelist with {len(safelist)} entries — may bloat CSS output",
            "Safelisting more than 50 patterns significantly increases CSS size. "
            "Review whether all safelisted classes are truly needed. "
            "Consider using content paths to auto-detect dynamic classes."))

    # B6: Missing theme.extend (all customizations override defaults)
    theme = data.get("theme")
    if isinstance(theme, dict):
        has_custom_keys = any(k != "extend" for k in theme)
        has_extend = "extend" in theme and isinstance(theme["extend"], dict)
        if has_custom_keys and not has_extend:
            findings.append(Finding("B6", "warning",
                "theme has custom keys but no 'extend' block — "
                "all customizations replace Tailwind defaults",
                "Use theme.extend to add custom values while keeping defaults. "
                "Keys placed directly under theme (not extend) completely "
                "replace the default values for that key."))

    return findings


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def validate_all(data: dict) -> list[Finding]:
    """Run all checks and return combined findings."""
    findings: list[Finding] = []
    findings.extend(check_structure(data))
    findings.extend(check_content(data))
    findings.extend(check_theme(data))
    findings.extend(check_dark_mode(data))
    findings.extend(check_plugins(data))
    findings.extend(check_best_practices(data))
    return findings


def validate_content_only(data: dict) -> list[Finding]:
    """Run only content-related checks."""
    findings: list[Finding] = []
    findings.extend(check_content(data))
    # Also include B1 (no content paths) from best practices
    content = data.get("content")
    if content is None:
        findings.append(Finding("B1", "error",
            "No content paths defined — tree-shaking will not work",
            "Tailwind needs content paths to scan for used classes."))
    return findings


def validate_theme_only(data: dict) -> list[Finding]:
    """Run only theme-related checks."""
    return check_theme(data)


# ---------------------------------------------------------------------------
# Rule explanations
# ---------------------------------------------------------------------------

RULE_EXPLANATIONS: dict[str, dict[str, str]] = {
    "S1": {
        "name": "File Not Found",
        "category": "Structure",
        "severity": "error",
        "description": "The Tailwind config JSON file does not exist or cannot be read.",
        "fix": "Ensure the file path is correct and the file has read permissions. "
               "Export with: node -e \"console.log(JSON.stringify(require('./tailwind.config.js')))\" > config.json",
    },
    "S2": {
        "name": "Empty Config",
        "category": "Structure",
        "severity": "error",
        "description": "The config file is empty (zero bytes, whitespace only, or empty object).",
        "fix": "Re-export the Tailwind config to JSON. The file must contain a valid JSON object "
               "with at least a 'content' array.",
    },
    "S3": {
        "name": "Invalid JSON",
        "category": "Structure",
        "severity": "error",
        "description": "The file contains invalid JSON syntax that cannot be parsed.",
        "fix": "Ensure the export produces valid JSON. Functions, require() calls, and "
               "RegExp objects are not JSON-serializable.",
    },
    "S4": {
        "name": "Unknown Top-Level Keys",
        "category": "Structure",
        "severity": "warning",
        "description": "Unrecognized top-level key that may be a typo or unsupported property.",
        "fix": "Check the Tailwind CSS documentation for valid configuration keys. "
               "Valid: content, theme, plugins, presets, darkMode, prefix, important, "
               "separator, corePlugins, safelist, blocklist, future, experimental.",
    },
    "S5": {
        "name": "JS/TS Config Detected",
        "category": "Structure",
        "severity": "error",
        "description": "The file appears to be JavaScript/TypeScript, not JSON.",
        "fix": "Export as JSON: node -e \"console.log(JSON.stringify(require('./tailwind.config.js')))\" > config.json",
    },
    "C1": {
        "name": "Missing Content Paths",
        "category": "Content",
        "severity": "error",
        "description": "No content paths configured. Required for Tailwind's tree-shaking in v3+.",
        "fix": "Add content: ['./src/**/*.{html,js,ts,jsx,tsx}'] to specify which files "
               "Tailwind should scan for class names.",
    },
    "C2": {
        "name": "Empty Content Array",
        "category": "Content",
        "severity": "warning",
        "description": "Content array exists but contains no glob patterns.",
        "fix": "Add file glob patterns, e.g. './src/**/*.{html,js,ts,jsx,tsx}'.",
    },
    "C3": {
        "name": "Content Includes node_modules",
        "category": "Content",
        "severity": "warning",
        "description": "Content paths include node_modules, severely impacting build performance.",
        "fix": "Remove node_modules from content paths. If a specific package uses "
               "Tailwind classes, add only that package's path.",
    },
    "C4": {
        "name": "Broad Content Glob",
        "category": "Content",
        "severity": "warning",
        "description": "Content glob is too broad (e.g. **/* without extension filter).",
        "fix": "Add extension filters: '**/*.{html,js,ts,jsx,tsx}' instead of '**/*'.",
    },
    "C5": {
        "name": "Suspicious Content Pattern",
        "category": "Content",
        "severity": "info",
        "description": "Content path has a suspicious pattern that may not work as intended.",
        "fix": "Review the glob pattern. CSS files don't contain class references. "
               "Shallow globs (*.ext) only match the current directory.",
    },
    "T1": {
        "name": "Theme Override Without Extend",
        "category": "Theme",
        "severity": "warning",
        "description": "A theme key directly overrides all Tailwind defaults for that category.",
        "fix": "Move the key to theme.extend to merge with defaults instead of replacing them. "
               "e.g. theme.extend.colors instead of theme.colors.",
    },
    "T2": {
        "name": "Empty theme.extend",
        "category": "Theme",
        "severity": "info",
        "description": "theme.extend exists but contains no customizations.",
        "fix": "Add custom values or remove the empty extend block.",
    },
    "T3": {
        "name": "Invalid Color Value",
        "category": "Theme",
        "severity": "warning",
        "description": "A color value is not a string (must be a CSS color like hex, rgb, hsl).",
        "fix": "Ensure all color values are CSS color strings: '#ff0000', 'rgb(255,0,0)', etc.",
    },
    "T4": {
        "name": "Theme Reference Without Callback",
        "category": "Theme",
        "severity": "info",
        "description": "A string containing 'theme(...)' was found, but callbacks are lost in JSON export.",
        "fix": "Replace theme() references with the actual resolved values in the JSON export.",
    },
    "T5": {
        "name": "Breakpoints Not Ascending",
        "category": "Theme",
        "severity": "warning",
        "description": "Custom screen breakpoints are not in ascending order.",
        "fix": "Reorder breakpoints from smallest to largest for mobile-first design to work correctly.",
    },
    "D1": {
        "name": "Invalid darkMode Value",
        "category": "Dark Mode",
        "severity": "error",
        "description": "darkMode has an invalid value. Must be 'media', 'class', 'selector', "
                       "or ['selector', '.custom-class'].",
        "fix": "Set darkMode to 'media' (OS preference), 'selector' (manual toggle), "
               "or ['selector', '.my-dark-class'] for a custom selector.",
    },
    "D2": {
        "name": "darkMode 'class' Deprecated",
        "category": "Dark Mode",
        "severity": "info",
        "description": "darkMode 'class' is deprecated since Tailwind v3.4. Use 'selector' instead.",
        "fix": "Replace darkMode: 'class' with darkMode: 'selector'. "
               "The 'selector' strategy is more flexible and forward-compatible.",
    },
    "P1": {
        "name": "Empty Plugins Array",
        "category": "Plugins",
        "severity": "info",
        "description": "The plugins array is empty.",
        "fix": "Remove the empty array or add plugins as needed.",
    },
    "P2": {
        "name": "Plugins Not Array",
        "category": "Plugins",
        "severity": "error",
        "description": "The plugins field is not an array.",
        "fix": "Set plugins to an array: plugins: [require('@tailwindcss/forms')].",
    },
    "P3": {
        "name": "Deprecated Official Plugin",
        "category": "Plugins",
        "severity": "info",
        "description": "An official Tailwind plugin that is built-in since v4.",
        "fix": "Remove the plugin when upgrading to Tailwind v4 — the functionality is included by default.",
    },
    "B1": {
        "name": "No Content Paths (Best Practice)",
        "category": "Best Practices",
        "severity": "error",
        "description": "No content paths defined — Tailwind's tree-shaking cannot remove unused CSS.",
        "fix": "Add content: ['./src/**/*.{html,js,ts,jsx,tsx}'] to enable tree-shaking.",
    },
    "B2": {
        "name": "Global Important",
        "category": "Best Practices",
        "severity": "warning",
        "description": "important: true makes every utility use !important, an anti-pattern.",
        "fix": "Use important: '#app' to scope specificity to a root selector instead.",
    },
    "B3": {
        "name": "Prefix Special Characters",
        "category": "Best Practices",
        "severity": "warning",
        "description": "The prefix contains special characters that may break class matching.",
        "fix": "Use only alphanumeric characters, hyphens, and underscores in the prefix.",
    },
    "B4": {
        "name": "All Core Plugins Disabled",
        "category": "Best Practices",
        "severity": "warning",
        "description": "All core plugins are disabled — Tailwind generates no utility classes.",
        "fix": "Remove corePlugins or selectively disable only the plugins you don't need.",
    },
    "B5": {
        "name": "Large Safelist",
        "category": "Best Practices",
        "severity": "warning",
        "description": "Safelist has more than 50 entries, significantly bloating CSS output.",
        "fix": "Review safelisted classes. Use content path scanning for dynamic classes "
               "instead of safelisting.",
    },
    "B6": {
        "name": "No theme.extend",
        "category": "Best Practices",
        "severity": "warning",
        "description": "Theme customizations replace defaults entirely because theme.extend is missing.",
        "fix": "Use theme.extend.{key} to add custom values while keeping Tailwind defaults.",
    },
}


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


def _deduplicate_findings(findings: list[Finding]) -> list[Finding]:
    """Remove duplicate findings (same rule_id + message)."""
    seen: set[tuple[str, str]] = set()
    deduped: list[Finding] = []
    for f in findings:
        key = (f.rule_id, f.message)
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    return deduped


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_validate(data: dict, path: str) -> dict:
    """Full validation with summary."""
    findings = _deduplicate_findings(validate_all(data))
    errors = [f for f in findings if f.severity == "error"]
    return {
        "command": "validate",
        "file": path,
        "valid": len(errors) == 0,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_lint(data: dict, path: str) -> dict:
    """Run all rules (alias for validate)."""
    result = cmd_validate(data, path)
    result["command"] = "lint"
    return result


def cmd_content(data: dict, path: str) -> dict:
    """Check content configuration only."""
    findings = _deduplicate_findings(validate_content_only(data))
    errors = [f for f in findings if f.severity == "error"]
    return {
        "command": "content",
        "file": path,
        "passed": len(errors) == 0,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_theme(data: dict, path: str) -> dict:
    """Check theme configuration only."""
    findings = _deduplicate_findings(validate_theme_only(data))
    errors = [f for f in findings if f.severity == "error"]
    return {
        "command": "theme",
        "file": path,
        "passed": len(errors) == 0,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    title = f"tailwind.config {cmd} — {path}"
    lines.append(title)
    lines.append("=" * len(title))

    findings = result.get("findings", [])
    if not findings:
        lines.append("[OK] No issues found")
    else:
        for f in findings:
            sev = f["severity"].upper().ljust(7)
            lines.append(f"[{sev}] {f['rule_id']}: {f['message']}")
            if f.get("detail"):
                lines.append(f"         {f['detail']}")

    if "valid" in result:
        valid_str = "VALID" if result.get("valid") else "INVALID"
        lines.append("")
        lines.append(f"Result: {valid_str}")

    if "passed" in result:
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
    lines.append(f"tailwind.config {cmd}: {path}")

    counts = result.get("counts", {})
    lines.append(f"Errors: {counts.get('errors', 0)}")
    lines.append(f"Warnings: {counts.get('warnings', 0)}")
    lines.append(f"Info: {counts.get('infos', 0)}")

    if "valid" in result:
        lines.append(f"Valid: {'yes' if result['valid'] else 'no'}")
    if "passed" in result:
        lines.append(f"Passed: {'yes' if result['passed'] else 'no'}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate JSON-exported Tailwind CSS configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Commands:
  validate   Full validation with all rules
  lint       Run all rules (alias for validate)
  content    Check content configuration
  theme      Check theme configuration

Note: Tailwind configs are JS/TS. This validator works with JSON-exported configs.
Export via: node -e "console.log(JSON.stringify(require('./tailwind.config.js')))" > config.json

Examples:
  python3 tailwind_config_validator.py validate config.json
  python3 tailwind_config_validator.py validate config.json --strict --format json
  python3 tailwind_config_validator.py lint config.json --format summary
  python3 tailwind_config_validator.py content config.json
  python3 tailwind_config_validator.py theme config.json --format json
"""
    )
    parser.add_argument("command", choices=["validate", "lint", "content", "theme"],
                        help="Command to run")
    parser.add_argument("file", help="Path to JSON-exported Tailwind config")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (CI mode)")
    parser.add_argument("--format", choices=["text", "json", "summary"], default="text",
                        help="Output format (default: text)")

    args = parser.parse_args()

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
        if args.command in ("validate", "lint"):
            result["valid"] = False
        elif args.command in ("content", "theme"):
            result["passed"] = False

        formatter = {"text": format_text, "json": format_json, "summary": format_summary}
        print(formatter[args.format](result))
        sys.exit(2)

    # Run command
    if args.command == "validate":
        result = cmd_validate(data, args.file)
    elif args.command == "lint":
        result = cmd_lint(data, args.file)
    elif args.command == "content":
        result = cmd_content(data, args.file)
    elif args.command == "theme":
        result = cmd_theme(data, args.file)

    # Format output
    formatter = {"text": format_text, "json": format_json, "summary": format_summary}
    print(formatter[args.format](result))

    # Exit code
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
