## Description:

Run Trivy vulnerability scans on containers, filesystems, and IaC — then triage findings by exploitability, reachability, and business impact with AI-powered prioritization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and DevSecOps teams use this skill to run Trivy scans across images, filesystems, repositories, Kubernetes clusters, IaC, and SBOMs, then turn vulnerability, secret, misconfiguration, and compliance findings into prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scans can inspect sensitive targets and may surface secrets or private dependency information.

Mitigation: Scope scan targets deliberately, keep generated reports in protected locations, and review findings before sharing results.

Risk: External EPSS and KEV enrichment can send discovered CVE identifiers to third-party services.

Mitigation: Approve external lookups for sensitive projects or run without enrichment when disclosure of CVE lists is not acceptable.

Risk: Shared temporary report paths can expose or overwrite scan output on multi-user systems.

Mitigation: Use per-run, access-controlled output paths instead of reusable shared /tmp filenames.

Risk: Copied CI/CD examples that use mutable action references can change behavior unexpectedly.

Mitigation: Pin CI actions and scanner versions to reviewed immutable versions before production use.

## Reference(s):

- [Trivy Debian Repository](https://aquasecurity.github.io/trivy-repo/deb)
- [FIRST EPSS API](https://api.first.org/data/v1/epss?cve=$CVES)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, tables, remediation steps, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include .trivyignore entries, CI/CD snippets, compliance mappings, trend comparisons, and prioritized vulnerability summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
