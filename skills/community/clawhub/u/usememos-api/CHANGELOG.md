# Changelog

## 1.0.2 (2026-03-06)

### Added
- `memo_comments.py` script to list, add, and delete comments on memos
- Comments API documentation in references/api.md

### Fixed
- Upload scripts now validate attachment size > 0 to catch silent upload failures
- `upload_and_link_attachment.py` accepts full resource names (`memos/...`) by
  stripping the prefix automatically

## 1.0.1 (2026-03-05)

### Fixed
- **Attachment linking bug**: uploading multiple images to a memo replaced all
  previous attachments instead of appending — only the last image survived.
  The PATCH now fetches existing attachments first and appends the new one.

### Added
- Integration tests for image uploads (1 PNG, 2 PNGs, 1 JPG, 3 JPGs) that
  run against a live UseMemos instance using the actual scripts
- `package.sh` script for packaging the skill for clawhub.ai publishing

## 1.0.0 (2026-02-24)

Initial release.

- Create memos with visibility control and inline `#tag` support
- List recent memos with optional limit and tag filter
- Search memos by content keyword
- Upload file attachments (base64-encoded via API)
- Upload and link attachments to existing memos in one step
- API reference documentation for UseMemos v1 endpoints
