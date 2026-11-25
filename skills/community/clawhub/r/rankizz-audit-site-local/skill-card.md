## Description:

Audit a public website for technical SEO, on-page content, structured data, GEO readiness, and AEO readiness using only the agent's local browser, shell, filesystem, and network resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners, marketers, and developers can use the skill to run a bounded local audit of a public website and receive evidence-based findings and prioritized recommendations without paid provider data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler may send requests to internal network services when run in an environment that can reach private services; scanner coverage was partial.

Mitigation: Run the crawler in a trusted environment with limited network access, and keep private-network access disabled unless the target is a site you control.

## Reference(s):

- [Audit checklist](references/audit-checklist.md)
- [Audit report contract](references/report-contract.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML, JSON]

**Output Format:** [Chat recap and evidence-based Markdown or HTML audit report; optional JSON crawl inventory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded site coverage, URL evidence, stated limitations, and prioritized actions]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
