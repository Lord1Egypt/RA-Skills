---
name: r-package-dev
description: Build, check, and submit R packages to CRAN or Bioconductor. Use when creating a new R package from scratch, fixing R CMD check errors/warnings, preparing for CRAN or Bioconductor submission, setting up GitHub Actions CI for R packages, writing S4 classes extending Bioconductor containers (SummarizedExperiment, GRanges), adding roxygen2 documentation with @references and DOIs, or debugging BiocCheck issues. Covers both CRAN and Bioconductor workflows with real submission experience.
---

# R Package Development — CRAN & Bioconductor

## Package Skeleton

```r
usethis::create_package("~/mypkg")
usethis::use_mit_license("Author Name")   # CRAN
# OR: License: Artistic-2.0              # Bioconductor standard
usethis::use_testthat()
usethis::use_vignette("introduction")
usethis::use_readme_md()
usethis::use_news_md()
```

Required: DESCRIPTION, NAMESPACE, LICENSE, NEWS.md, README.md,
.Rbuildignore, .gitignore

## DESCRIPTION

### CRAN rules
- Title: title case, ≤65 chars, no period
- Description: ≥2 sentences, ends with period
- Software names in quotes: 'CmdStan', 'OpenSSL'
- `Authors@R`: use `person()` with aut, cre roles + ORCID
- Imports: only packages actually called via `::` or `importFrom`
- Suggests: must have `requireNamespace()` guard in code

### Bioconductor additions
- Version: `0.99.0` for new submissions
- `biocViews:` required (e.g., Genetics, Sequencing, QualityControl)
- `LazyData: false` (Bioconductor requirement)
- ≥2 Bioconductor packages in Imports
- `VignetteBuilder: knitr`
- Collate field listing all R/*.R files in dependency order

## R/ Code Standards

Never use in R/ files:

| Forbidden | Use instead |
|-----------|-------------|
| `library()` / `require()` | `::` or `@importFrom` |
| `T` / `F` | `TRUE` / `FALSE` |
| `sapply()` | `vapply()` (type-safe) |
| `1:length(x)` | `seq_along(x)` / `seq_len(n)` |
| `cat()` / `print()` | `message()` (except in `show` methods) |
| `options()` / `par()` | Never modify global state |
| `@slot` direct access | Use accessor generics |
| `<<<-` | Never use global assignment |
| `set.seed()` / `browser()` | Remove before submission |

## Documentation (roxygen2)

Every `@export` function must have:
- `@param` for all arguments
- `@return` describing the return value
- `@examples` that run in <5 seconds
- `@references` with DOIs for methods: `\doi{10.xxxx/yyyy}`

Use `\donttest{}` for slow examples. Never `\dontrun{}`.

## S4 Classes (Bioconductor)

For infrastructure packages extending Bioconductor classes:

```r
# Define generic — this is the extension point
setGeneric("myFunction", function(x, ...)
    standardGeneric("myFunction"))

# Define method for your class
setMethod("myFunction", "MyClass", function(x, ...) {
    # implementation
})
```

Key principle: analytical operations should be **generics**, not
plain functions. This lets downstream packages specialize behavior
for their own classes. See references/bioconductor.md.

## Testing

```r
devtools::test()                    # all tests
covr::package_coverage()            # target ≥80%
```

Test error paths with `expect_error()`, not just happy paths.

## R CMD check

```r
rcmdcheck::rcmdcheck(
    args = c("--no-manual", "--as-cran"),
    error_on = "warning"
)
```

For Bioconductor, also run:
```r
BiocCheck::BiocCheck("pkg_0.99.0.tar.gz", `new-package` = TRUE)
BiocCheck::BiocCheckGitClone(".")
```

## GitHub Actions CI

See references/github-actions.md for platform-specific configs.

**CRAN packages**: use `r-lib/actions` standard workflow.
**Bioconductor packages**: use `r-lib/actions/setup-r-dependencies`
which auto-resolves Bioc deps from DESCRIPTION.

## Visualization (publication grade)

See references/visualization.md for Nature/Science style standards.

Key rules:
- Colorblind-safe palette: Wong (2011) *Nat Methods* 8:441
- `theme_classic()`, no gridlines, 8pt base font
- No titles on figures (titles go in captions)
- Panel labels: bold lowercase **a**, **b**, **c**
- Paired dot plots > bar charts for before/after comparisons

## Submission

### CRAN
Upload tarball to https://xmpalantir.wu.ac.at/cransubmit/
Include `cran-comments.md`. See references/cran.md.

### Bioconductor
1. Register at https://support.bioconductor.org (same email as DESCRIPTION)
2. Subscribe to bioc-devel mailing list
3. Add SSH key to GitHub
4. Make repo Public
5. Open issue at https://github.com/Bioconductor/Contributions/issues/new
   See references/bioconductor.md for the submission template.

## Common Issues

See references/troubleshooting.md for solutions to frequent
R CMD check and BiocCheck problems.
