## Description:

Find and qualify company websites by detected technologies using Crawlora's tech-stack dataset and live website checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and research teams use this skill to find websites matching a technology profile or qualify a supplied domain list, then check public evidence before drawing conclusions about technical fit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora receives the API key and submitted domains, URLs, and technology filters.

Mitigation: Keep the key in the environment; use public website targets and avoid private or sensitive internal targets unless sharing them is intended.

Risk: Incomplete or stale detections can misclassify a website's technology fit.

Mitigation: Check evidence and freshness, live-check shortlisted sites, and label unknowns or discrepancies instead of treating missing detections as proof of absence.

## Reference(s):

- [Crawlora website](https://crawlora.net)
- [Tech-stack endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/techstack-prospecting)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown table or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes domains, verified identities when available, detected technologies, confidence and evidence, freshness and live-check status, fit rationale, source URLs, and unknowns.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
