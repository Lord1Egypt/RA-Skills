## Description:

Low-volume web configuration auditor with JavaScript bundle security analysis for headers, DNS, TLS, exposed configuration, and client-side XSS or secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-hussein](https://clawhub.ai/user/z-hussein)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to review web configuration and client-side bundles on domains they own or are explicitly authorized to assess. It produces findings on headers, DNS, TLS, exposed paths, subdomains, and JavaScript patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports unrestricted redirects that could reach internal services.

Mitigation: Run checks only against authorized domains and review redirect destinations before following them.

Risk: ClawScan reports crawl and reporting weaknesses that could exceed or undermine the stated low-volume scope; the scan is partial because some references could not be resolved.

Mitigation: Limit checks to the authorized target and needed scope, inspect unresolved package references, and verify findings before relying on them.

## Reference(s):

- [web-checker on ClawHub](https://clawhub.ai/z-hussein/skills/web-checker)
- [OpenClaw documentation](https://docs.openclaw.ai/)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Terminal findings, JSON report, or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Low-volume web audit findings; JavaScript bundles are analyzed statically without execution.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
