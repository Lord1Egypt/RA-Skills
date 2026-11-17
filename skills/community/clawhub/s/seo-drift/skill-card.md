## Description:

SEO drift monitoring: capture baselines of SEO-critical elements, detect changes, and track regressions over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO practitioners, and site operators use this skill to baseline SEO-critical page elements before a release, compare later page states against that baseline, and review historical SEO drift for a URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided pages and keeps local baseline and history data in a SQLite cache.

Mitigation: Use it only for pages whose SEO metadata and fetched-content-derived history may be retained locally, and clear the local drift cache when retention is no longer needed.

## Reference(s):

- [SEO Drift Comparison Rules](references/comparison-rules.md)
- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-drift)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference locally stored SQLite baseline and comparison history for user-provided URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
