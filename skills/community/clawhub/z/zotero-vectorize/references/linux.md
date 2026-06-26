# Linux notes

## Default Zotero data directory

Usually:

```text
/home/<user>/Zotero
```

or equivalently `~/Zotero`.

Important contents:

- `zotero.sqlite`
- `storage/`

## Common Linux pitfalls

- Multiple Python interpreters / venv confusion
- Missing system libraries for PDF/text tooling
- Path differences in sandboxed package installs

Always verify the actual Zotero data directory from the app UI before assuming defaults.
