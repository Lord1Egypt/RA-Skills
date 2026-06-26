# Windows notes

## Default Zotero data directory

Usually:

```text
C:\Users\<UserName>\Zotero
```

Important contents:

- `zotero.sqlite`
- `storage\`

## Best way to confirm the real path

In Zotero:

- `Edit`
- `Preferences`
- `Advanced`
- `Show Data Directory`

## PowerShell example

```powershell
cd <workspace>
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install sentence-transformers PyMuPDF numpy
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## Common Windows pitfalls

- Long path / special character issues in PDF filenames
- SQLite lock errors if Zotero is still open
- Slow first-time HuggingFace model download
- PowerShell quoting differences
