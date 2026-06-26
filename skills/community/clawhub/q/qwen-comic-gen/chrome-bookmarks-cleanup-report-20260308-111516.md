# Chrome Bookmarks Cleanup Report

**Generated**: 2026-03-08 11:15:16
**Backup**: C:\Users\Xiabi\.openclaw\workspace\bookmarks-backup\Bookmarks.backup.20260308-111515

## Statistics

- Total URLs: 351
- Total Folders: 21
- Used (30 days): 0
- Unused (>1 year): 351

## Folders to Delete

@(if (.Count -gt 0) {  | ForEach-Object { "- " } } else { "- None found" }) -join "
"

## Next Steps

1. Open Chrome Bookmark Manager (Ctrl+Shift+O)
2. Delete the folders listed above
3. Reorganize remaining bookmarks

See chrome-bookmarks-reorganization-plan.md for detailed plan.
