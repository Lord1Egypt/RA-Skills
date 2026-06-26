#!/usr/bin/env python3
"""Terraform Module Linter — lint .tf files for structure, naming, security, best practices."""

import sys
import os
import re
import json
import glob
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    file: str
    line: int
    rule: str
    severity: Severity
    message: str
    category: str


@dataclass
class HCLBlock:
    block_type: str  # resource, variable, output, module, data, locals, terraform, provider
    labels: list
    attributes: dict
    line: int
    raw: str
    nested: list = field(default_factory=list)


def parse_hcl_simple(filepath):
    """Simple HCL parser — extracts blocks and attributes."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except (IOError, OSError):
        return []

    content_no_comments = re.sub(r'#[^\n]*', '', content)
    content_no_comments = re.sub(r'//[^\n]*', '', content_no_comments)
    content_no_comments = re.sub(r'/\*.*?\*/', '', content_no_comments, flags=re.DOTALL)

    blocks = []
    block_pattern = re.compile(
        r'^(\w+)\s+(?:"([^"]+)"\s+)?(?:"([^"]+)"\s+)?\{',
        re.MULTILINE
    )

    for match in block_pattern.finditer(content_no_comments):
        block_type = match.group(1)
        label1 = match.group(2) or ''
        label2 = match.group(3) or ''
        labels = [l for l in [label1, label2] if l]

        line = content_no_comments[:match.start()].count('\n') + 1

        brace_start = match.end() - 1
        brace_count = 1
        pos = match.end()
        while pos < len(content_no_comments) and brace_count > 0:
            if content_no_comments[pos] == '{':
                brace_count += 1
            elif content_no_comments[pos] == '}':
                brace_count -= 1
            pos += 1

        body = content_no_comments[match.end():pos-1]

        attrs = {}
        for attr_match in re.finditer(r'(\w+)\s*=\s*(.+?)(?:\n|$)', body):
            key = attr_match.group(1)
            val = attr_match.group(2).strip()
            attrs[key] = val

        blocks.append(HCLBlock(
            block_type=block_type, labels=labels,
            attributes=attrs, line=line, raw=body
        ))

    return blocks


def collect_tf_files(path):
    if os.path.isfile(path) and path.endswith('.tf'):
        return [path]
    if os.path.isdir(path):
        return sorted(glob.glob(os.path.join(path, '*.tf')))
    return []


def lint_structure(path, all_blocks, files):
    issues = []
    is_dir = os.path.isdir(path)

    if is_dir:
        filenames = {os.path.basename(f) for f in files}
        if 'main.tf' not in filenames:
            issues.append(Issue(path, 1, "missing-main-tf", Severity.WARNING,
                                "Missing main.tf — recommended for module structure", "structure"))
        if 'variables.tf' not in filenames:
            issues.append(Issue(path, 1, "missing-variables-tf", Severity.INFO,
                                "Missing variables.tf — recommended for module structure", "structure"))
        if 'outputs.tf' not in filenames:
            issues.append(Issue(path, 1, "missing-outputs-tf", Severity.INFO,
                                "Missing outputs.tf — recommended for module structure", "structure"))

    has_terraform_block = False
    has_required_providers = False
    for block in all_blocks:
        if block.block_type == 'terraform':
            has_terraform_block = True
            if 'required_providers' in block.raw:
                has_required_providers = True
            if 'required_version' not in block.attributes and 'required_version' not in block.raw:
                issues.append(Issue(path, block.line, "missing-required-version", Severity.WARNING,
                                    "terraform block missing required_version constraint", "structure"))

    if not has_terraform_block and is_dir:
        issues.append(Issue(path, 1, "missing-terraform-block", Severity.WARNING,
                            "No terraform block found — add required_version and required_providers",
                            "structure"))

    variables = {}
    for block in all_blocks:
        if block.block_type == 'variable' and block.labels:
            var_name = block.labels[0]
            variables[var_name] = block

            if not block.raw.strip():
                issues.append(Issue(path, block.line, "empty-variable", Severity.WARNING,
                                    f"Empty variable block '{var_name}'", "structure"))

            if 'description' not in block.attributes and 'description' not in block.raw:
                issues.append(Issue(path, block.line, "missing-variable-description", Severity.WARNING,
                                    f"Variable '{var_name}' missing description", "structure"))

    all_content = ''
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                all_content += fh.read()
        except (IOError, OSError):
            pass

    for var_name, block in variables.items():
        pattern = rf'var\.{re.escape(var_name)}\b'
        if not re.search(pattern, all_content):
            issues.append(Issue(path, block.line, "unused-variable", Severity.WARNING,
                                f"Variable '{var_name}' declared but not referenced", "structure"))

    for block in all_blocks:
        if block.block_type == 'output' and block.labels:
            if not block.raw.strip():
                issues.append(Issue(path, block.line, "empty-output", Severity.WARNING,
                                    f"Empty output block '{block.labels[0]}'", "structure"))

    return issues


def lint_naming(path, all_blocks):
    issues = []
    snake_case = re.compile(r'^[a-z][a-z0-9]*(_[a-z0-9]+)*$')

    for block in all_blocks:
        if block.block_type in ('resource', 'data') and len(block.labels) >= 2:
            name = block.labels[1]
            if not snake_case.match(name):
                issues.append(Issue(path, block.line, f"{block.block_type}-naming", Severity.WARNING,
                                    f"{block.block_type.title()} name '{name}' should be snake_case",
                                    "naming"))

        elif block.block_type == 'variable' and block.labels:
            name = block.labels[0]
            if not snake_case.match(name):
                issues.append(Issue(path, block.line, "variable-naming", Severity.WARNING,
                                    f"Variable name '{name}' should be snake_case", "naming"))

        elif block.block_type == 'output' and block.labels:
            name = block.labels[0]
            if not snake_case.match(name):
                issues.append(Issue(path, block.line, "output-naming", Severity.WARNING,
                                    f"Output name '{name}' should be snake_case", "naming"))

        elif block.block_type == 'module' and block.labels:
            name = block.labels[0]
            if not snake_case.match(name):
                issues.append(Issue(path, block.line, "module-naming", Severity.WARNING,
                                    f"Module name '{name}' should be snake_case", "naming"))

        elif block.block_type == 'locals':
            for attr_name in block.attributes:
                if not snake_case.match(attr_name):
                    issues.append(Issue(path, block.line, "local-naming", Severity.WARNING,
                                        f"Local name '{attr_name}' should be snake_case", "naming"))

    return issues


SECRET_PATTERNS = [
    (r'(?i)(password|secret|token|api_key|access_key)\s*=\s*"[^"]{4,}"', "hardcoded-secret",
     "Possible hardcoded secret/credential"),
    (r'(?i)(aws_access_key_id|aws_secret_access_key)\s*=\s*"[A-Za-z0-9/+=]{16,}"', "hardcoded-aws-key",
     "Hardcoded AWS credentials detected"),
]

SECURITY_PATTERNS = [
    (r'"0\.0\.0\.0/0"', "open-cidr", "Overly permissive CIDR block 0.0.0.0/0"),
    (r'"\*"', "wildcard-action", "Wildcard (*) in IAM policy action or resource"),
    (r'(?i)publicly_accessible\s*=\s*true', "public-access", "Resource is publicly accessible"),
    (r'(?i)public_access\s*=\s*true', "public-access-enabled", "Public access is enabled"),
]


def lint_security(path, all_blocks, files):
    issues = []

    for f in files:
        try:
            with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                lines = fh.readlines()
        except (IOError, OSError):
            continue

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//'):
                continue

            for pattern, rule, msg in SECRET_PATTERNS:
                if re.search(pattern, line):
                    issues.append(Issue(f, i, rule, Severity.ERROR, msg, "security"))

            for pattern, rule, msg in SECURITY_PATTERNS:
                if re.search(pattern, line):
                    issues.append(Issue(f, i, rule, Severity.WARNING, msg, "security"))

    for block in all_blocks:
        if block.block_type == 'variable' and block.labels:
            var_name = block.labels[0].lower()
            is_sensitive_name = any(w in var_name for w in
                                    ['password', 'secret', 'token', 'key', 'credential'])
            if is_sensitive_name:
                if 'sensitive' not in block.raw and 'sensitive' not in block.attributes:
                    issues.append(Issue(path, block.line, "missing-sensitive-flag", Severity.WARNING,
                                        f"Variable '{block.labels[0]}' looks sensitive but missing "
                                        f"'sensitive = true'", "security"))

    return issues


def lint_best_practices(path, all_blocks):
    issues = []

    for block in all_blocks:
        if block.block_type == 'variable' and block.labels:
            if 'type' not in block.attributes and 'type' not in block.raw:
                issues.append(Issue(path, block.line, "missing-variable-type", Severity.INFO,
                                    f"Variable '{block.labels[0]}' missing type constraint",
                                    "best-practices"))

        if block.block_type == 'output' and block.labels:
            if 'description' not in block.attributes and 'description' not in block.raw:
                issues.append(Issue(path, block.line, "missing-output-description", Severity.WARNING,
                                    f"Output '{block.labels[0]}' missing description",
                                    "best-practices"))

        if block.block_type == 'resource' and len(block.labels) >= 2:
            resource_type = block.labels[0]

            taggable_prefixes = ['aws_', 'azurerm_', 'google_']
            if any(resource_type.startswith(p) for p in taggable_prefixes):
                skip_types = {'aws_iam_policy', 'aws_iam_role_policy', 'aws_iam_policy_attachment',
                              'aws_route53_record', 'aws_cloudwatch_log_group'}
                if resource_type not in skip_types:
                    if 'tags' not in block.raw and 'tags' not in block.attributes:
                        issues.append(Issue(path, block.line, "missing-tags", Severity.INFO,
                                            f"Resource '{block.labels[1]}' ({resource_type}) "
                                            f"missing tags", "best-practices"))

            stateful_types = {'aws_db_instance', 'aws_rds_cluster', 'aws_s3_bucket',
                              'aws_dynamodb_table', 'azurerm_storage_account',
                              'google_sql_database_instance'}
            if resource_type in stateful_types:
                if 'lifecycle' not in block.raw:
                    issues.append(Issue(path, block.line, "missing-lifecycle", Severity.INFO,
                                        f"Stateful resource '{block.labels[1]}' ({resource_type}) "
                                        f"consider adding lifecycle block (prevent_destroy)",
                                        "best-practices"))

    return issues


def format_text(issues):
    if not issues:
        return "\033[32m\u2714 No issues found\033[0m"

    icons = {Severity.ERROR: "\033[31m\u2716\033[0m", Severity.WARNING: "\033[33m\u26a0\033[0m",
             Severity.INFO: "\033[36m\u2139\033[0m"}
    lines = []
    current_file = None
    for issue in sorted(issues, key=lambda i: (i.file, i.line)):
        if issue.file != current_file:
            current_file = issue.file
            lines.append(f"\n\033[1m{current_file}\033[0m")
        icon = icons.get(issue.severity, "")
        lines.append(f"  {icon} {issue.line}:{issue.rule} — {issue.message}")

    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    lines.append(f"\n{errors} error(s), {warnings} warning(s), {infos} info(s)")
    return '\n'.join(lines)


def format_json(issues):
    return json.dumps([{
        'file': i.file, 'line': i.line, 'rule': i.rule,
        'severity': i.severity.value, 'message': i.message,
        'category': i.category
    } for i in issues], indent=2)


def format_summary(issues):
    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    files = len(set(i.file for i in issues))
    return (f"Files: {files} | Errors: {errors} | Warnings: {warnings} | "
            f"Info: {infos} | Total: {len(issues)}")


def main():
    if len(sys.argv) < 3:
        print("Usage: terraform_module_linter.py <command> <path> [options]")
        print("Commands: lint, security, naming, validate")
        print("Options: --format json|text|summary")
        sys.exit(2)

    command = sys.argv[1]
    path = sys.argv[2]
    fmt = 'text'

    for i, arg in enumerate(sys.argv):
        if arg == '--format' and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]

    files = collect_tf_files(path)
    if not files:
        print(f"No .tf files found at '{path}'")
        sys.exit(2)

    all_blocks = []
    for f in files:
        all_blocks.extend(parse_hcl_simple(f))

    issues = []
    if command == 'lint':
        issues.extend(lint_structure(path, all_blocks, files))
        issues.extend(lint_naming(path, all_blocks))
        issues.extend(lint_security(path, all_blocks, files))
        issues.extend(lint_best_practices(path, all_blocks))
    elif command == 'security':
        issues.extend(lint_security(path, all_blocks, files))
    elif command == 'naming':
        issues.extend(lint_naming(path, all_blocks))
    elif command == 'validate':
        issues.extend(lint_structure(path, all_blocks, files))
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)

    if fmt == 'json':
        print(format_json(issues))
    elif fmt == 'summary':
        print(format_summary(issues))
    else:
        print(format_text(issues))

    has_errors = any(i.severity == Severity.ERROR for i in issues)
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
