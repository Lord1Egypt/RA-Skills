# CRAN Submission

## Pre-submission Checklist

```
[ ] R CMD check --as-cran: 0 errors, 0 warnings on R-devel
[ ] devtools::document() up to date
[ ] spelling::spell_check_package() clean
[ ] urlchecker::url_check() all valid
[ ] No non-ASCII in R/ files
[ ] All @export have @return, @param, @examples
[ ] Title ≤65 chars, no period
[ ] Authors@R has cre + cph roles
[ ] NEWS.md mentions current version
[ ] cran-comments.md updated
[ ] CI green on release + oldrel + macOS + Windows
```

## cran-comments.md Template

```markdown
## R CMD check results
0 errors | 0 warnings | 1 note
* New submission

## Test environments
* local [OS], R [version]
* GitHub Actions: ubuntu-latest, macos-latest, windows-latest

## Reverse dependencies
New package, no reverse dependencies.
```

Always explain NOTEs (misspelled author names, non-CRAN Suggests).

## Submission Process

1. Upload tarball to https://xmpalantir.wu.ac.at/cransubmit/
2. Confirmation email → click link within 24 hours
3. Auto-check → human review (1-5 business days)

If auto-check fails: fix, rebuild tarball, resubmit (same version).

## Handling Reviewer Feedback

Common requests:
- "Add \value to .Rd files" → add `@return` to every `@export`
- "Unwrap \dontrun{}" → change to `\donttest{}`
- "Explain [words]" → update cran-comments.md and resubmit

Keep same version number for resubmission.
