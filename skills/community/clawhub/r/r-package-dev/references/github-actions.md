# GitHub Actions CI for R Packages

## Bioconductor Package (recommended)

Uses `r-lib/actions` standard actions — auto-resolves Bioc deps:

```yaml
name: R-CMD-check

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  R-CMD-check:
    runs-on: ${{ matrix.config.os }}
    name: ${{ matrix.config.os }} (${{ matrix.config.r }})
    strategy:
      fail-fast: false
      matrix:
        config:
          - {os: ubuntu-latest, r: 'release'}
          - {os: macos-latest, r: 'release'}
          - {os: windows-latest, r: 'release'}
    env:
      GITHUB_PAT: ${{ secrets.GITHUB_TOKEN }}
      _R_CHECK_FORCE_SUGGESTS_: false

    steps:
      - uses: actions/checkout@v4
      - uses: r-lib/actions/setup-r@v2
        with:
          r-version: ${{ matrix.config.r }}
          use-public-rspm: true
      - uses: r-lib/actions/setup-pandoc@v2
      - uses: r-lib/actions/setup-r-dependencies@v2
        with:
          extra-packages: any::rcmdcheck
          needs: check
      - uses: r-lib/actions/check-r-package@v2
        with:
          args: '"--no-manual"'
          error-on: '"error"'
```

Key: `setup-r-dependencies` reads DESCRIPTION and installs from
both CRAN and Bioconductor automatically. No manual
`BiocManager::install()` needed.

Use `error-on: '"error"'` not `"warning"` — system-level warnings
(qpdf, LaTeX) would otherwise fail the build.

## CRAN Package with Non-CRAN Suggests

When Suggests includes packages not on CRAN (e.g., cmdstanr):

```yaml
- name: Install dependencies
  run: |
    install.packages(c("remotes", "rcmdcheck"))
    desc <- readLines("DESCRIPTION")
    desc <- desc[!grepl("^\\s+cmdstanr", desc)]
    writeLines(desc, "DESCRIPTION")
    remotes::install_deps(dependencies = TRUE)
  shell: Rscript {0}

- name: Restore DESCRIPTION
  run: git checkout -- DESCRIPTION

- name: Check
  run: rcmdcheck::rcmdcheck(args = c("--no-manual", "--as-cran"),
       error_on = "error", check_dir = "check")
  shell: Rscript {0}
  env:
    _R_CHECK_FORCE_SUGGESTS_: false
```
