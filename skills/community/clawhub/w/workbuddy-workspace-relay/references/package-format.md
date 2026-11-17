# WorkBuddy Workspace Relay package format

## Package envelope

The outer file uses the `.wbpack` extension and is an age passphrase-encrypted
gzip-compressed tar archive. The extension is only a product label; the age
header provides encryption and authentication.

The decrypted archive contains exactly one root, `payload/`:

```text
payload/
├── workspace/
│   └── <project files and directories>
├── HANDOFF.md
├── manifest.json
└── runtime.json
```

The restore script places the project files at the selected destination and
places the three migration records under `.workbuddy-relay/` so a source file
named `HANDOFF.md` is never overwritten by package metadata.

## `manifest.json`

Required fields:

```json
{
  "format": "workbuddy-workspace-relay",
  "format_version": "0.1",
  "project_name": "example",
  "created_at": "2026-08-01T00:00:00Z",
  "source_os": "Darwin",
  "source_arch": "arm64",
  "workspace_folder": "workspace",
  "file_count": 1,
  "total_bytes": 12,
  "directories": ["workspace/docs"],
  "files": [
    {
      "path": "workspace/README.md",
      "size": 12,
      "sha256": "<64 lowercase hexadecimal characters>",
      "mode": 420
    }
  ],
  "excluded_rules": {},
  "skipped_symlink_count": 0
}
```

`files[].path` must be relative to `workspace/`. `files[].sha256` is computed
from the staged payload, then checked again after decryption. Missing data is a
failure, not zero.

## `runtime.json`

Runtime metadata is non-sensitive context only:

- source operating system and architecture;
- Python version;
- current Git branch when available;
- names of common runtime executables found on the source machine.

Never add environment values, tokens, credential paths, browser state, or
absolute user paths to this file.

## Restore invariants

Before writing into the destination, the restore script must:

1. decrypt the age envelope into a temporary file;
2. reject unsafe tar members and unexpected roots;
3. parse all three metadata files as UTF-8;
4. compare manifest paths with actual regular files;
5. compare every file's size and SHA-256;
6. choose an empty destination or a fresh non-overwriting sibling;
7. move only the validated project tree and migration records into place.

The restore operation never executes a restored file. WorkBuddy decides what to
read next after it loads `.workbuddy-relay/HANDOFF.md`.
