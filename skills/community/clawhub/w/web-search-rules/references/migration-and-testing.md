# Migration, Dry Runs, Testing, and Release

## v2 to v3 config migration

Legacy path:

```text
~/.workbuddy/skills/web-search-rules/config.json
```

Canonical v3 path:

```text
~/.skill-config/web-search-rules/config.json
```

Migration rules:

1. Detect legacy config read-only.
2. Show source path, target path, platform, and store names.
3. Ask before creating the v3 config.
4. Copy only non-secret fields.
5. Do not delete or modify the legacy config.
6. Append an audit record with operation `config_migration`.

## Dry-run report format

Use this format before delete, cleanup, upload, or migration:

```text
Dry Run Report
Operation: migrate
Source platform: obsidian
Target platform: feishu-wiki
Items: 42
Cloud upload: yes
Backup/version history: available on target, source unchanged
Manifest: ~/.skill-config/web-search-rules/manifests/confirm-20260509-001.json
Confirmation required: confirm migrate 42 items to feishu-wiki
```

## Test scenarios

Security:

- Path traversal with `..` is rejected.
- Similar-prefix vault paths are rejected.
- Symlink targets outside allowed roots are rejected.
- Secret-like config fields are rejected.
- Browser automation cannot start without explicit platform confirmation.
- Cloud upload cannot run without batch confirmation.

Rules:

- Exact URL beats broader domain whitelist when the exact URL is blacklisted.
- Blacklist beats whitelist by default.
- Expired rules are ignored.
- Duplicate URLs collapse to one staged item.
- Tracking parameters are removed for matching but original URLs are retained.

Platforms:

- Each adapter can read rules, stage content, archive confirmed content, show delete dry-run, and handle a failed write.
- NotebookLM warns that content is uploaded to Google and never automates login.
- Obsidian writes only inside an approved vault path.

Migration:

- Empty v3 config can be created from scratch.
- v2 config can be migrated after confirmation.
- Legacy config is not deleted.

## Release checklist

- `SKILL.md`, `SECURITY.md`, and `_meta.json` show `4.0.0`.
- Clawhub Security Notice names filesystem access, browser automation, cloud upload, deletion, and migration.
- All reference files are UTF-8 and contain no mojibake.
- Examples do not include real credentials.
- A rollback copy of the v2.0.2 package is retained outside the v3 package.
