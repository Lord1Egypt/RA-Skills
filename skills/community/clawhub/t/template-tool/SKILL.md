---
name: template-tool
description: Process text templates with variable substitution. Use for generating dynamic content from template files.
---
# Template - Text Template Processor

Replace placeholders in template files with provided values. Supports variable substitution with configurable delimiters for content generation.

## Usage
```bash
template-tool [options] <template_file> [key=value...]
```

## Options

- `-d DELIM`: Use custom delimiter (default: {{ }})
- `-o FILE`: Write output to file

## Examples

```bash
template-tool greeting.txt name=World
template-tool report.md title="Annual Report" year=2026
echo "Hello {{name}}" | template-tool name=Jack
```