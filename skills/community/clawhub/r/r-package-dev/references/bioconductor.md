# Bioconductor Submission Guide

## Pre-submission Checklist

```
[ ] Version: 0.99.0
[ ] R CMD check: 0 errors, 0 warnings
[ ] BiocCheck: 0 errors, 0 warnings
[ ] BiocCheckGitClone: 0 errors, 0 warnings
[ ] biocViews present and valid
[ ] ≥2 Bioconductor packages in Imports
[ ] LazyData: false
[ ] VignetteBuilder: knitr
[ ] Vignette uses BiocStyle, has sessionInfo()
[ ] Package-level man page exists (?Package-package)
[ ] All man pages have \value and \examples
[ ] All @export use slot() not @ for slot access
[ ] No library()/require() in R/ code
[ ] NEWS.md has current version
[ ] Authors@R has real name, email, ORCID (recommended)
[ ] Git author matches DESCRIPTION (use git filter-branch if needed)
[ ] SSH key added to GitHub
[ ] Registered at support.bioconductor.org
[ ] Subscribed to bioc-devel mailing list
[ ] Repo is Public
```

## S4 Infrastructure Design

Make analytical functions **generics**, not plain functions:

```r
# In AllGenerics.R
setGeneric("flagISNV", function(x, filter, ...)
    standardGeneric("flagISNV"))

setGeneric("calcDiversity", function(x, ...)
    standardGeneric("calcDiversity"))

# In methods.R — your class's implementation
setMethod("flagISNV", "WithinHostExperiment",
    function(x, filter = ISNVFilter(), ...) {
    # implementation
})
```

This lets downstream packages define methods for their own classes,
making your package infrastructure rather than just a tool.

## Subsetting: Preserve Custom Slots

If your class extends RangedSummarizedExperiment with extra slots:

```r
setMethod("[", "MyClass",
    function(x, i, j, ..., drop = TRUE) {
    result <- callNextMethod()
    new("MyClass", result,
        mySlot1 = mySlot1(x),
        mySlot2 = mySlot2(x))
})
```

Without this, `whe[1:5, ]` loses custom slots.

## combineCols Bug

`cbind` on RSE subclasses can fail with "DataFrames must have
non-NULL, non-duplicated rownames." Fix: strip rownames before
building the merged SE:

```r
combineCols <- function(...) {
    # ... collect components ...
    rr <- rowRanges(args[[1L]])
    rownames(rr) <- NULL  # critical fix
    # ... build SE from matrices ...
}
```

## Submission Template

Title: `PackageName`

```
Update the following URL to point to the GitHub repository of
the package you wish to submit to _Bioconductor_

- Repository: https://github.com/USERNAME/PACKAGENAME

Confirm the following by editing each check box to '[x]'

- [x] I understand that by submitting my package to _Bioconductor_,
  the package source and all review commentary are visible to the
  general public.

- [x] I have read the _Bioconductor_ [Package Submission][2]
  instructions. My package is consistent with the _Bioconductor_
  [Package Guidelines][1].

- [x] I understand Bioconductor [Package Naming Policy][9] and
  acknowledge Bioconductor may retain use of package name.

- [x] I understand that a minimum requirement for package acceptance
  is to pass R CMD check and R CMD BiocCheck with no ERROR or WARNINGS.

- [x] My package addresses statistical or bioinformatic issues related
  to the analysis and comprehension of high throughput genomic data.

- [x] I am committed to the long-term maintenance of my package.

- [x] I am aware of the [Bioconductor Code of Conduct][8] and
  will abide by it.

[1]: https://contributions.bioconductor.org/develop-overview.html
[2]: https://contributions.bioconductor.org/submission-overview.html
[3]: https://support.bioconductor.org
[4]: https://stat.ethz.ch/mailman/listinfo/bioc-devel
[8]: https://bioconductor.org/about/code-of-conduct/
[9]: https://contributions.bioconductor.org/bioconductor-package-submissions.html#naming-policy
```

## Git Author Fix

If commits show wrong author (e.g., placeholder from development):

```bash
git filter-branch -f --env-filter '
export GIT_AUTHOR_NAME="RealName"
export GIT_AUTHOR_EMAIL="real@email.com"
export GIT_COMMITTER_NAME="RealName"
export GIT_COMMITTER_EMAIL="real@email.com"
' HEAD
git push --force origin main
```
