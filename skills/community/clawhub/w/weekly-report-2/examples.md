# Weekly Report — Examples

## Example 1: Standard weekly report

**User request**: "生成本周的周报"

**Command** (Windows):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate-report.ps1 -Repo . -Days 7
```

**Sample output** (`weekly-report.md`):

```markdown
# Weekly Report

**Report period**: 2026-08-25 ~ 2026-08-31
**Commits**: 12 | **Files changed**: 34 | **Contributors**: 2

## Accomplished
- Implemented user login with JWT token refresh
- Added invoice export to PDF
- Fixed date-parsing bug in the reporting module

## In Progress
- Dashboard chart integration (blocked on design)

## Issues & Risks
- None

## Next Week Plan
- (To be filled)

## Commit Details
| Hash | Date | Author | Message |
|------|------|--------|---------|
| a1b2c3d | 08-26 | Alice | feat(auth): add JWT refresh flow |
| e4f5a6b | 08-26 | Bob   | fix(report): parse ISO dates |
| ...
```

## Example 2: Filter by author and longer range

**Command**:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate-report.ps1 -Repo . -Days 14 -Author "Alice" -Output alice-report.md
```

**Result**: Only commits authored by `Alice` in the last 14 days; the
"Contributors" count becomes 1.

## Example 3: Non-Git folder fallback

If `-Repo` points to a folder that is not a Git repository, the agent lists
files whose modification time falls inside the range and builds the report
from that, adding the note `based on file timestamps` to the header.
