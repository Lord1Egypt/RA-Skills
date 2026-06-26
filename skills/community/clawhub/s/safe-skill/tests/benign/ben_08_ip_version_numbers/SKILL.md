---
name: changelog-gen
version: 3.2.1
description: Generate changelogs from git history.
---

# Changelog Generator

Auto-generate changelogs from commit history.

## Version History

- v3.2.1 — Bug fixes for date formatting
- v3.2.0 — Added support for semantic versioning (1.2.3 format)
- v3.1.0 — Group commits by 2.0.0 semver ranges
- v3.0.0 — Major rewrite, new templating engine
- v2.5.0 — Performance: reduced memory from 512.0 to 256.0 MB
- v1.0.0 — Initial release

## Configuration

```yaml
output_format: markdown
version_pattern: "X.Y.Z"
group_by: minor_version
date_format: "YYYY.MM.DD"
```

## Supported Schemes

- Semantic: 1.2.3, 10.20.30
- Calendar: 2026.03.13
- Build: 1.0.0.4567
