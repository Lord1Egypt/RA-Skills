# Software Bill of Materials (SBOM) Template

The orchestrator produces the SBOM after surface stage consolidation by reading recon step files and dependency audit findings. Output to `{REPORTS_DIR}/sbom.md`.

---

    # Software Bill of Materials (SBOM)

    **Project:** [From recon step-01 Project Name]
    **Version:** [From package manifest version field, or "unversioned"]
    **Generated:** {ISO_TIMESTAMP}
    **Security Run:** {RUN_DIR}
    **SBOM Standard Reference:** This report maps to CycloneDX 1.5 / SPDX 2.3 field semantics in markdown form.

    ---

    ## Project Identity

    | Field | Value | Source |
    |-------|-------|--------|
    | Name | | package manifest |
    | Version | | package manifest |
    | Description | | README / manifest |
    | Repository URL | | git remote / manifest |
    | License | | manifest / LICENSE file |

    ---

    ## Languages & Runtimes

    | Language | Version | Where Used | File Count | Primary/Secondary |
    |----------|---------|-----------|------------|-------------------|

    Data sources: `step-01-metadata.md` (Primary Language, Runtime), `step-14-scope.md` (Languages Detected), file extension analysis.

    ---

    ## Frameworks & Platforms

    | Framework | Version | Category | Configuration File |
    |-----------|---------|----------|--------------------|

    Categories: Web Framework, CSS Framework, Testing, ORM, Build Tool, Cloud Platform, Container Runtime.

    ---

    ## Build Toolchain

    | Component | Tool | Version | Configuration |
    |-----------|------|---------|---------------|
    | Package Manager | | | |
    | Build System | | | |
    | Bundler | | | |
    | CI/CD Platform | | | |
    | Container Runtime | | | |
    | Infrastructure-as-Code | | | |

    ---

    ## Direct Dependencies — Backend

    | # | Package | Version | License | Registry | Security Relevance | Maintenance Status |
    |---|---------|---------|---------|----------|--------------------|--------------------|

    **Total:** [count]

    ---

    ## Direct Dependencies — Frontend

    | # | Package | Version | License | Registry | Security Relevance | Maintenance Status |
    |---|---------|---------|---------|----------|--------------------|--------------------|

    **Total:** [count]

    ---

    ## Direct Dependencies — Development

    | # | Package | Version | License | Registry | Purpose |
    |---|---------|---------|---------|----------|---------|

    **Total:** [count]

    ---

    ## Transitive Dependency Summary

    Parsed from lockfile(s): [package-lock.json / yarn.lock / pnpm-lock.yaml / poetry.lock / Pipfile.lock / go.sum / Cargo.lock / Gemfile.lock].

    | Metric | Value |
    |--------|-------|
    | Total transitive dependencies | |
    | Maximum dependency depth | |
    | Packages with multiple versions | |
    | Packages in both direct and transitive | |

    ### High-Risk Transitive Dependencies

    Only list transitive dependencies that are security-relevant (crypto, auth, parsers, HTTP clients) or have known vulnerabilities.

    | Package | Version | Depth | Parent Chain | Security Relevance |
    |---------|---------|-------|-------------|-------------------|

    ---

    ## Known Vulnerabilities

    Cross-reference with dependency audit findings (DEP-* findings from surface stage).

    | CVE / Advisory | Package | Installed Version | Fixed Version | Severity | CVSS | Reachable in Project? | Finding ID |
    |----------------|---------|-------------------|---------------|----------|------|-----------------------|------------|

    **Total known vulnerabilities:** [count]
    **Reachable in this project:** [count]
    **Fix available:** [count]

    ---

    ## License Inventory

    | License | Type | Package Count | Packages |
    |---------|------|---------------|----------|

    License types: Permissive (MIT, BSD, Apache-2.0, ISC), Weak Copyleft (LGPL, MPL), Strong Copyleft (GPL, AGPL), Public Domain (Unlicense, CC0), Proprietary, Unknown.

    ### License Risk Summary

    | Risk Level | Count | Details |
    |-----------|-------|---------|
    | No risk (Permissive) | | |
    | Low risk (Weak Copyleft) | | |
    | Medium risk (Strong Copyleft) | | Copyleft obligations may apply |
    | High risk (Unknown/Missing) | | License could not be determined |
    | Review needed (Proprietary) | | Custom license terms |

    ---

    ## Supply Chain Indicators

    | Indicator | Value | Assessment |
    |-----------|-------|------------|
    | Lockfile present and committed | Yes/No | |
    | Integrity hashes in lockfile | Yes/No | |
    | Private registry usage | Yes/No | |
    | Pre/post-install scripts | [count] | List packages with install scripts |
    | Packages with < 100 weekly downloads | [count] | Typosquatting risk |
    | Packages with single maintainer | [count] | Bus factor risk |
    | Packages unmaintained (> 2 years) | [count] | Security patch risk |

    ---

    ## SPDX / CycloneDX Field Mapping

    For machine-readable SBOM export, map this report to standard formats:

    | This Report Section | CycloneDX 1.5 Field | SPDX 2.3 Field |
    |--------------------|---------------------|----------------|
    | Project Identity → Name | metadata.component.name | packages[0].name |
    | Project Identity → Version | metadata.component.version | packages[0].versionInfo |
    | Project Identity → License | metadata.component.licenses | packages[0].licenseConcluded |
    | Direct Dependencies | components[] | packages[] |
    | Package → License | components[].licenses | packages[].licenseConcluded |
    | Known Vulnerabilities | vulnerabilities[] | (via SPDX-Security namespace) |
    | Package → Registry | components[].purl | packages[].externalRefs[].referenceLocator |

    To generate a machine-readable SBOM from this data, use:
    - CycloneDX: `npx @cyclonedx/cyclonedx-npm` / `cyclonedx-py` / `cyclonedx-gomod`
    - SPDX: `spdx-sbom-generator` / `syft`

    ---

    ## Data Sources

    | Data | Source File | Collected By |
    |------|-----------|-------------|
    | Project metadata | recon/step-01-metadata.md | Recon agent (recon stage) |
    | Dependencies list | recon/step-13-dependencies.md | Recon agent (recon stage) |
    | Scope & languages | recon/step-14-scope.md | Recon agent (recon stage) |
    | CI/CD platform | recon/step-02-docs.md | Recon agent (recon stage) |
    | Vulnerability scan | findings/DEP-*.md | Dependency audit agent (surface stage) |
    | License & transitive data | Dependency audit agent output | Dependency audit agent (surface stage) |
