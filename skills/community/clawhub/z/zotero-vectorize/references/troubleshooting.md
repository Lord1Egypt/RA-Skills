# Troubleshooting

## SQLite / snapshot issues

### Symptom
Snapshot or DB read fails, often with `database is locked`.

### Response
1. Ask the user to close Zotero.
2. Retry `snapshot_zotero_db.py`.
3. Continue only after a snapshot succeeds.

## Model download / loading issues

### Symptom
`SentenceTransformer(...)` fails or times out.

### Response
1. Verify `sentence-transformers` and `torch` are installed.
2. Test model loading in a minimal Python shell.
3. If network is restricted, ask the user to pre-download the model.

## Missing PDFs

### Symptom
A Zotero item has a PDF attachment row, but the file cannot be found.

### Response
1. Confirm `storage/` points to the active Zotero data directory.
2. Check whether the attachment is linked externally rather than stored under Zotero.
3. Record the missing item in the summary instead of silently skipping it.

## Bad PDF extraction

### Symptom
PDF exists, but extracted text is empty or low quality.

### Response
1. Report that extraction quality is poor.
2. Do not invent full text.
3. Keep the item out of `fulltext_vectors.json` unless the script extracted usable text.
4. OCR is an enhancement, not a first-version requirement.

## Incremental update safety

### Rule
Never run `apply_incremental_updates.py` before reporting the missing items and obtaining user confirmation.

## Backup retention

### Rule
Before rewriting store files, create backups and retain only:

- latest backup
- previous backup

Do not keep unbounded historical backups.
