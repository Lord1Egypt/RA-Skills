# Approval Flow (zotero-pdf-upload)

Use this flow to avoid accidental writes.

1. Parse / inspect first (read-only)
   - `parse-url`
   - `list-collections`
   - `choose-collection`
2. If no strong collection match, return `pending-new-collection-approval`.
3. Create collection only after explicit human approval:
   - `create-collection --approve-create`
4. Create item metadata only after explicit human approval:
   - `create-item --approve-write`
5. PDF upload is optional and controlled by:
   - config `zotero.allowPdfUpload`
   - `create-item --attach-pdf ...`

## Safety defaults

- No write command runs unless approval flag is provided.
- Collection auto-creation is not part of matching step.
- API key should come from env/path before inline config.
