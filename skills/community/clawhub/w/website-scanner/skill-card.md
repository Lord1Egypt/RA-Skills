## Description:

Scans website and domain infrastructure, content, SEO signals, crawler files, and third-party data, with optional deep scans and technical report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugogu](https://clawhub.ai/user/hugogu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and analysts use this skill to inspect public or authorized domains, audit website metadata and SEO, and produce technical reports for documentation or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned sites can influence follow-up requests through sitemap data and cause unintended outbound requests from the user's environment.

Mitigation: Use only against public or authorized targets, preferably from an isolated environment with restricted egress, and review targets before deep scans.

Risk: Scanning internal domains or sensitive investigations may disclose information to third-party lookup services.

Mitigation: Avoid sensitive targets unless outbound disclosure to DNS, WHOIS, geolocation, and search services is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hugogu/skills/website-scanner)
- [Publisher profile](https://clawhub.ai/user/hugogu)
- [ipapi geolocation lookup endpoint](https://ipapi.co/{ip}/json/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, PDF, Shell commands]

**Output Format:** [Console Markdown report with optional JSON or PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on target availability and external DNS, WHOIS, geolocation, and search responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
