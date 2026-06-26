# R Package Troubleshooting

## R CMD check

| Problem | Fix |
|---------|-----|
| no visible binding for `.data$col` | `utils::globalVariables(".data")` at file top |
| Imports not imported from: 'pkg' | Remove from Imports or add `@importFrom` |
| Variables with usage in Rd but not in code (`example_whe`) | Use `@docType data` + `@name` + `@usage data(name)` + `NULL` (not `"name"`) |
| Non-standard file at top level | Add to `.Rbuildignore` |
| Documented arguments not in \usage | `@param` names must match function signature exactly |
| no visible global function: `slot` | Add `@importFrom methods slot` |
| no visible global function: `mcols<-` | Add `@importFrom S4Vectors mcols mcols<-` |

## BiocCheck

| Problem | Fix |
|---------|-----|
| Consider adding ORCID | Add `comment = c(ORCID = "...")` in `person()` — optional |
| Function > 50 lines | Informational NOTE, not blocking. Refactor if possible |
| Consider DataImport biocView | Add to biocViews if relevant |
| Support Site email not found | Register at support.bioconductor.org with DESCRIPTION email |
| Cannot determine mailing list | Subscribe at stat.ethz.ch/mailman/listinfo/bioc-devel |

## GitHub Actions CI

| Problem | Fix |
|---------|-----|
| Bioc deps not found | Use `r-lib/actions/setup-r-dependencies@v2` (auto-resolves) |
| `error_on = "warning"` fails | Change to `error_on = "error"` — qpdf/LaTeX warnings are system-level |
| Vignette build fails: no pandoc | Add `r-lib/actions/setup-pandoc@v2` step |
| ggplot2 not available | Add to Suggests + `requireNamespace()` guard |

## Bioconductor Submission

| Problem | Fix |
|---------|-----|
| Issue auto-closed "(inactive)" | Check: SSH key on GitHub, support site email matches DESCRIPTION |
| `rbind`/`cbind` on RSE subclass fails | Use standalone `combineRows()`/`combineCols()` functions instead |
| `[` subsetting loses custom slots | Override `[` method with `callNextMethod()` + `new()` |
| Vignette references deleted files | Update `system.file()` paths after data file changes |
| git commits show wrong author | `git filter-branch --env-filter` to rewrite all commits |

## Real Data Validation

Never use only simulated data for package demos. Use real published
data to validate:
- Formulas produce literature-consistent values
- QC thresholds are biologically meaningful
- Figures show real biological patterns, not random noise

Cite data sources with DOI in all figures and documentation.
