#!/usr/bin/env python3
"""Validate .stylelintrc / stylelint.config.js configuration files."""

import sys
import json
import re
import os

SEVERITIES = {"error": 3, "warning": 2, "info": 1}

KNOWN_RULES = {
    "alpha-value-notation", "at-rule-empty-line-before", "at-rule-no-unknown",
    "block-no-empty", "color-function-notation", "color-hex-length",
    "color-named", "color-no-hex", "color-no-invalid-hex",
    "comment-empty-line-before", "comment-no-empty", "comment-whitespace-inside",
    "custom-media-pattern", "custom-property-empty-line-before",
    "custom-property-no-missing-var-function", "custom-property-pattern",
    "declaration-block-no-duplicate-custom-properties",
    "declaration-block-no-duplicate-properties",
    "declaration-block-no-redundant-longhand-properties",
    "declaration-block-no-shorthand-property-overrides",
    "declaration-block-single-line-max-declarations",
    "declaration-empty-line-before", "declaration-no-important",
    "declaration-property-unit-allowed-list",
    "declaration-property-value-allowed-list",
    "declaration-property-value-disallowed-list",
    "font-family-name-quotes", "font-family-no-duplicate-names",
    "font-family-no-missing-generic-family-keyword",
    "font-weight-notation", "function-calc-no-unspaced-operator",
    "function-disallowed-list", "function-linear-gradient-no-nonstandard-direction",
    "function-name-case", "function-no-unknown", "function-url-no-scheme-relative",
    "function-url-quotes", "hue-degree-notation",
    "import-notation", "keyframe-block-no-duplicate-selectors",
    "keyframe-declaration-no-important", "keyframes-name-pattern",
    "length-zero-no-unit", "max-nesting-depth",
    "media-feature-name-allowed-list", "media-feature-name-disallowed-list",
    "media-feature-name-no-unknown", "media-feature-name-no-vendor-prefix",
    "media-feature-name-unit-allowed-list", "media-feature-range-notation",
    "media-query-no-invalid", "named-grid-areas-no-invalid",
    "no-descending-specificity", "no-duplicate-at-import-rules",
    "no-duplicate-selectors", "no-empty-source", "no-invalid-double-slash-comments",
    "no-invalid-position-at-import-rule", "no-irregular-whitespace",
    "no-unknown-animations", "no-unknown-custom-media",
    "no-unknown-custom-properties", "number-max-precision",
    "property-allowed-list", "property-disallowed-list",
    "property-no-unknown", "property-no-vendor-prefix",
    "rule-empty-line-before", "rule-selector-property-disallowed-list",
    "selector-attribute-name-disallowed-list",
    "selector-attribute-operator-allowed-list",
    "selector-class-pattern", "selector-combinator-allowed-list",
    "selector-disallowed-list", "selector-id-pattern",
    "selector-max-attribute", "selector-max-class",
    "selector-max-combinators", "selector-max-compound-selectors",
    "selector-max-id", "selector-max-pseudo-class",
    "selector-max-specificity", "selector-max-type",
    "selector-max-universal", "selector-nested-pattern",
    "selector-no-qualifying-type", "selector-no-vendor-prefix",
    "selector-not-notation", "selector-pseudo-class-allowed-list",
    "selector-pseudo-class-disallowed-list", "selector-pseudo-class-no-unknown",
    "selector-pseudo-element-allowed-list", "selector-pseudo-element-colon-notation",
    "selector-pseudo-element-no-unknown", "selector-type-case",
    "selector-type-no-unknown", "shorthand-property-no-redundant-values",
    "string-no-newline", "unit-allowed-list", "unit-disallowed-list",
    "unit-no-unknown", "value-keyword-case", "value-no-vendor-prefix",
}

DEPRECATED_RULES = {
    "at-rule-blacklist": "at-rule-disallowed-list",
    "at-rule-property-requirelist": None,
    "at-rule-whitelist": "at-rule-allowed-list",
    "block-closing-brace-empty-line-before": None,
    "block-closing-brace-newline-after": None,
    "block-closing-brace-newline-before": None,
    "block-closing-brace-space-after": None,
    "block-closing-brace-space-before": None,
    "block-opening-brace-newline-after": None,
    "block-opening-brace-newline-before": None,
    "block-opening-brace-space-after": None,
    "block-opening-brace-space-before": None,
    "color-function-comma-space-after": None,
    "color-function-comma-space-before": None,
    "color-function-parentheses-space-inside": None,
    "declaration-bang-space-after": None,
    "declaration-bang-space-before": None,
    "declaration-block-semicolon-newline-after": None,
    "declaration-block-semicolon-newline-before": None,
    "declaration-block-semicolon-space-after": None,
    "declaration-block-semicolon-space-before": None,
    "declaration-block-trailing-semicolon": None,
    "declaration-colon-newline-after": None,
    "declaration-colon-space-after": None,
    "declaration-colon-space-before": None,
    "function-blacklist": "function-disallowed-list",
    "function-comma-newline-after": None,
    "function-comma-newline-before": None,
    "function-comma-space-after": None,
    "function-comma-space-before": None,
    "function-max-empty-lines": None,
    "function-parentheses-newline-inside": None,
    "function-parentheses-space-inside": None,
    "function-whitespace-after": None,
    "function-whitelist": "function-allowed-list",
    "indentation": None,
    "max-empty-lines": None,
    "max-line-length": None,
    "media-feature-colon-space-after": None,
    "media-feature-colon-space-before": None,
    "media-feature-name-blacklist": "media-feature-name-disallowed-list",
    "media-feature-name-whitelist": "media-feature-name-allowed-list",
    "media-feature-parentheses-space-inside": None,
    "media-feature-range-operator-space-after": None,
    "media-feature-range-operator-space-before": None,
    "media-query-list-comma-newline-after": None,
    "media-query-list-comma-newline-before": None,
    "media-query-list-comma-space-after": None,
    "media-query-list-comma-space-before": None,
    "no-eol-whitespace": None,
    "no-extra-semicolons": None,
    "no-missing-end-of-source-newline": None,
    "number-leading-zero": None,
    "number-no-trailing-zeros": None,
    "property-blacklist": "property-disallowed-list",
    "property-whitelist": "property-allowed-list",
    "selector-attribute-brackets-space-inside": None,
    "selector-attribute-operator-blacklist": "selector-attribute-operator-disallowed-list",
    "selector-attribute-operator-whitelist": "selector-attribute-operator-allowed-list",
    "selector-combinator-space-after": None,
    "selector-combinator-space-before": None,
    "selector-descendant-combinator-no-non-space": None,
    "selector-list-comma-newline-after": None,
    "selector-list-comma-newline-before": None,
    "selector-list-comma-space-after": None,
    "selector-list-comma-space-before": None,
    "selector-pseudo-class-blacklist": "selector-pseudo-class-disallowed-list",
    "selector-pseudo-class-whitelist": "selector-pseudo-class-allowed-list",
    "selector-pseudo-element-blacklist": "selector-pseudo-element-disallowed-list",
    "selector-pseudo-element-whitelist": "selector-pseudo-element-allowed-list",
    "string-quotes": None,
    "unicode-bom": None,
    "unit-blacklist": "unit-disallowed-list",
    "unit-whitelist": "unit-allowed-list",
    "value-list-comma-newline-after": None,
    "value-list-comma-newline-before": None,
    "value-list-comma-space-after": None,
    "value-list-comma-space-before": None,
    "value-list-max-empty-lines": None,
}

KNOWN_CONFIG_KEYS = {
    "rules", "extends", "plugins", "processors", "overrides",
    "customSyntax", "defaultSeverity", "ignoreDisables",
    "reportDescriptionlessDisables", "reportInvalidScopeDisables",
    "reportNeedlessDisables", "ignoreFiles", "fix",
    "allowEmptyInput", "cache", "cacheLocation", "cacheStrategy",
    "configBasedir", "formatter",
}

KNOWN_EXTENDS = [
    "stylelint-config-standard", "stylelint-config-recommended",
    "stylelint-config-standard-scss", "stylelint-config-recommended-scss",
    "stylelint-config-prettier", "stylelint-config-css-modules",
    "stylelint-config-tailwindcss", "stylelint-config-html",
    "stylelint-config-standard-vue",
]


def load_config(path):
    with open(path, "r") as f:
        content = f.read().strip()

    if path.endswith(".json") or path.endswith(".stylelintrc"):
        content_stripped = content
        if content_stripped.startswith("//") or "/*" in content_stripped:
            lines = []
            for line in content_stripped.split("\n"):
                stripped = line.strip()
                if stripped.startswith("//"):
                    continue
                lines.append(line)
            content_stripped = "\n".join(lines)
        return json.loads(content_stripped)

    if path.endswith(".yaml") or path.endswith(".yml"):
        return simple_yaml_parse(content)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    try:
        return simple_yaml_parse(content)
    except Exception:
        pass

    raise ValueError(f"Cannot parse config file: {path}")


def simple_yaml_parse(text):
    result = {}
    current_key = None
    current_list = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        if stripped.startswith("- "):
            if current_key and current_list is not None:
                val = stripped[2:].strip().strip('"').strip("'")
                current_list.append(val)
            continue

        m = re.match(r'^([a-zA-Z_-]+)\s*:\s*(.*)$', stripped)
        if m:
            key = m.group(1)
            val = m.group(2).strip()

            if not val:
                current_key = key
                current_list = []
                result[key] = current_list
            elif val.startswith("["):
                items = val[1:-1].split(",")
                result[key] = [i.strip().strip('"').strip("'") for i in items if i.strip()]
                current_key = key
                current_list = None
            elif val in ("true", "True"):
                result[key] = True
                current_key = key
                current_list = None
            elif val in ("false", "False"):
                result[key] = False
                current_key = key
                current_list = None
            elif val.startswith('"') or val.startswith("'"):
                result[key] = val.strip('"').strip("'")
                current_key = key
                current_list = None
            else:
                try:
                    result[key] = int(val)
                except ValueError:
                    result[key] = val
                current_key = key
                current_list = None

    return result


def validate_config(data, issues):
    if not isinstance(data, dict):
        issues.append(("error", "invalid-config-type", "Config root must be an object"))
        return

    for key in data:
        if key not in KNOWN_CONFIG_KEYS:
            issues.append(("warning", "unknown-config-key", f"Unknown config key '{key}'"))

    validate_rules(data, issues)
    validate_extends(data, issues)
    validate_plugins(data, issues)
    validate_overrides(data, issues)
    validate_severity(data, issues)
    validate_ignore_files(data, issues)


def validate_rules(data, issues):
    rules = data.get("rules", {})
    if not rules:
        if "extends" not in data:
            issues.append(("warning", "no-rules-or-extends", "Config has no 'rules' and no 'extends' — nothing to lint"))
        return

    if not isinstance(rules, dict):
        issues.append(("error", "rules-not-object", "'rules' must be an object"))
        return

    for rule_name, rule_val in rules.items():
        if rule_name in DEPRECATED_RULES:
            replacement = DEPRECATED_RULES[rule_name]
            if replacement:
                issues.append(("warning", "deprecated-rule", f"Rule '{rule_name}' is deprecated — use '{replacement}'"))
            else:
                issues.append(("warning", "deprecated-rule", f"Rule '{rule_name}' is deprecated (removed in Stylelint 16, use Prettier for formatting)"))

        elif rule_name not in KNOWN_RULES and "/" not in rule_name:
            issues.append(("info", "unknown-rule", f"Rule '{rule_name}' not in known Stylelint rules (may be from a plugin)"))

        if rule_val is None:
            issues.append(("warning", "null-rule-value", f"Rule '{rule_name}' is null — use 'null' explicitly to disable or remove it"))

        if isinstance(rule_val, list) and len(rule_val) >= 2:
            severity_val = rule_val[0]
            if isinstance(severity_val, str) and severity_val not in ("error", "warning", True, False, "true", "false"):
                pass

    disabled_count = 0
    for rule_name, rule_val in rules.items():
        if rule_val is False or rule_val is None or (isinstance(rule_val, list) and len(rule_val) > 0 and rule_val[0] is None):
            disabled_count += 1

    if disabled_count > len(rules) * 0.5 and len(rules) > 5:
        issues.append(("info", "many-disabled-rules", f"{disabled_count}/{len(rules)} rules are disabled — consider removing them or using a different extends"))


def validate_extends(data, issues):
    extends = data.get("extends")
    if extends is None:
        return

    if isinstance(extends, str):
        extends = [extends]

    if not isinstance(extends, list):
        issues.append(("error", "extends-not-list", "'extends' must be a string or array"))
        return

    seen = set()
    for ext in extends:
        if not isinstance(ext, str):
            continue

        if ext in seen:
            issues.append(("warning", "duplicate-extends", f"Duplicate extends entry: '{ext}'"))
        seen.add(ext)

    has_prettier = any("prettier" in str(e).lower() for e in extends)
    has_standard = any("standard" in str(e).lower() for e in extends)
    if has_prettier and has_standard:
        prettier_idx = -1
        standard_idx = -1
        for i, ext in enumerate(extends):
            if "prettier" in str(ext).lower():
                prettier_idx = i
            if "standard" in str(ext).lower():
                standard_idx = i
        if prettier_idx < standard_idx:
            issues.append(("warning", "prettier-before-standard", "stylelint-config-prettier should be LAST in extends (after standard config)"))


def validate_plugins(data, issues):
    plugins = data.get("plugins")
    if plugins is None:
        return

    if isinstance(plugins, str):
        plugins = [plugins]

    if not isinstance(plugins, list):
        issues.append(("error", "plugins-not-list", "'plugins' must be a string or array"))
        return

    seen = set()
    for plugin in plugins:
        if not isinstance(plugin, str):
            continue
        if plugin in seen:
            issues.append(("warning", "duplicate-plugin", f"Duplicate plugin: '{plugin}'"))
        seen.add(plugin)

    rules = data.get("rules", {})
    if isinstance(rules, dict):
        plugin_prefixes = set()
        for rule_name in rules:
            if "/" in rule_name:
                prefix = rule_name.split("/")[0]
                plugin_prefixes.add(prefix)

        if plugin_prefixes and not plugins:
            issues.append(("warning", "plugin-rules-without-plugins", f"Rules with plugin prefixes ({', '.join(sorted(plugin_prefixes))}) but no plugins declared"))


def validate_overrides(data, issues):
    overrides = data.get("overrides")
    if overrides is None:
        return

    if not isinstance(overrides, list):
        issues.append(("error", "overrides-not-list", "'overrides' must be an array"))
        return

    for i, override in enumerate(overrides):
        if not isinstance(override, dict):
            issues.append(("warning", "invalid-override", f"Override #{i+1} is not an object"))
            continue

        if "files" not in override:
            issues.append(("error", "override-missing-files", f"Override #{i+1} must have 'files' property"))

        if "rules" not in override and "customSyntax" not in override:
            issues.append(("info", "override-no-rules", f"Override #{i+1} has no 'rules' or 'customSyntax'"))

        if "rules" in override and isinstance(override["rules"], dict):
            for rule_name in override["rules"]:
                if rule_name in DEPRECATED_RULES:
                    replacement = DEPRECATED_RULES[rule_name]
                    if replacement:
                        issues.append(("warning", "deprecated-rule-override", f"Override #{i+1}: rule '{rule_name}' is deprecated — use '{replacement}'"))
                    else:
                        issues.append(("warning", "deprecated-rule-override", f"Override #{i+1}: rule '{rule_name}' is deprecated"))


def validate_severity(data, issues):
    ds = data.get("defaultSeverity")
    if ds is not None and ds not in ("error", "warning"):
        issues.append(("warning", "invalid-default-severity", f"defaultSeverity '{ds}' should be 'error' or 'warning'"))


def validate_ignore_files(data, issues):
    ignore = data.get("ignoreFiles")
    if ignore is None:
        return

    if isinstance(ignore, str):
        ignore = [ignore]

    if isinstance(ignore, list):
        for pattern in ignore:
            if isinstance(pattern, str) and pattern in ("*", "**/*", "**"):
                issues.append(("warning", "ignore-everything", f"ignoreFiles pattern '{pattern}' matches everything"))


def format_text(issues, path):
    if not issues:
        return f"✅ {path}: no issues found"
    lines = [f"{'❌' if any(s == 'error' for s, _, _ in issues) else '⚠️'} {path}: {len(issues)} issue(s)\n"]
    for severity, rule, msg in sorted(issues, key=lambda x: -SEVERITIES.get(x[0], 0)):
        icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(severity, "•")
        lines.append(f"  {icon} [{severity}] {rule}: {msg}")
    return "\n".join(lines)


def format_json(issues, path):
    return json.dumps({
        "file": path,
        "issues": [{"severity": s, "rule": r, "message": m} for s, r, m in issues],
        "summary": {
            "total": len(issues),
            "errors": sum(1 for s, _, _ in issues if s == "error"),
            "warnings": sum(1 for s, _, _ in issues if s == "warning"),
            "info": sum(1 for s, _, _ in issues if s == "info"),
        }
    }, indent=2)


def format_summary(issues, path):
    errs = sum(1 for s, _, _ in issues if s == "error")
    warns = sum(1 for s, _, _ in issues if s == "warning")
    infos = sum(1 for s, _, _ in issues if s == "info")
    status = "FAIL" if errs else ("WARN" if warns else "PASS")
    return f"{status} | {path} | {len(issues)} issues ({errs} errors, {warns} warnings, {infos} info)"


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("Usage: stylelint_validator.py <command> [options] <file>")
        print()
        print("Commands:")
        print("  lint        Full config validation")
        print("  rules       Check rules only (deprecated, unknown, conflicts)")
        print("  deprecated  List deprecated rules in config")
        print("  validate    Alias for lint")
        print()
        print("Options:")
        print("  --format text|json|summary   Output format (default: text)")
        print("  --min-severity error|warning|info   Filter by minimum severity")
        print("  --strict                     Exit 1 on any issue")
        print()
        print("Supported files:")
        print("  .stylelintrc, .stylelintrc.json, .stylelintrc.yaml, .stylelintrc.yml")
        print()
        print("Examples:")
        print("  stylelint_validator.py lint .stylelintrc.json")
        print("  stylelint_validator.py deprecated --format json .stylelintrc")
        sys.exit(0)

    cmd = args[0]
    fmt = "text"
    min_sev = "info"
    strict = False
    path = None

    i = 1
    while i < len(args):
        if args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif args[i] == "--min-severity" and i + 1 < len(args):
            min_sev = args[i + 1]
            i += 2
        elif args[i] == "--strict":
            strict = True
            i += 1
        else:
            path = args[i]
            i += 1

    if not path:
        for candidate in [".stylelintrc", ".stylelintrc.json", ".stylelintrc.yaml", ".stylelintrc.yml"]:
            if os.path.exists(candidate):
                path = candidate
                break
        if not path:
            print("Error: no stylelint config file found", file=sys.stderr)
            sys.exit(2)

    if not os.path.exists(path):
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(2)

    try:
        data = load_config(path)
    except Exception as e:
        print(f"Error parsing {path}: {e}", file=sys.stderr)
        sys.exit(2)

    issues = []

    if cmd in ("lint", "validate"):
        validate_config(data, issues)
    elif cmd == "rules":
        validate_rules(data, issues)
    elif cmd == "deprecated":
        rules = data.get("rules", {})
        if isinstance(rules, dict):
            for rule_name in rules:
                if rule_name in DEPRECATED_RULES:
                    replacement = DEPRECATED_RULES[rule_name]
                    if replacement:
                        issues.append(("warning", "deprecated-rule", f"'{rule_name}' → '{replacement}'"))
                    else:
                        issues.append(("warning", "deprecated-rule", f"'{rule_name}' removed in Stylelint 16"))
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(2)

    min_level = SEVERITIES.get(min_sev, 1)
    issues = [(s, r, m) for s, r, m in issues if SEVERITIES.get(s, 0) >= min_level]

    if fmt == "json":
        print(format_json(issues, path))
    elif fmt == "summary":
        print(format_summary(issues, path))
    else:
        print(format_text(issues, path))

    if strict and issues:
        sys.exit(1)
    elif any(s == "error" for s, _, _ in issues):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
