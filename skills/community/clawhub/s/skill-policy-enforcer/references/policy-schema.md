# Policy schema

`skill-policy-enforcer` accepts JSON or a simple YAML subset. JSON is recommended for CI. YAML support is dependency-free and handles scalar values plus list values.

## Fields

```yaml
policy_name: "strict-skill-policy"
max_skill_md_words: 1200
max_file_size_kb: 256
allow_network: false
allow_secret_reads: false
require_files:
  - SKILL.md
allowed_frontmatter_fields:
  - name
  - description
forbidden_paths:
  - .env
  - .ssh
  - id_rsa
  - credentials
forbidden_patterns:
  - "curl .*\\|.*sh"
  - "Invoke-Expression"
warn_patterns:
  - "TODO"
  - "placeholder"
```

## Severity model

- Required-file, frontmatter, secret-read, forbidden-path, forbidden-pattern, file-size, and network violations are `deny` by default.
- `warn_patterns` produce `warn`.
- Missing optional metadata produces `warn`.

## Notes

- Patterns are regular expressions and are matched case-insensitively.
- Path checks match against normalized relative paths and file content.
- Use an explicit policy file to loosen default rules; do not override findings in prose.

