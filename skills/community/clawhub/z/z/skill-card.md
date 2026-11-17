## Description:

Anti-skill-crawler defense system. Detects and mitigates unauthorized crawling, scraping, and bulk extraction of skill definitions, prompt content, and instruction sets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to passively monitor skill-access metadata for patterns consistent with bulk skill crawling or prompt scraping and to receive alerts for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill monitors request metadata patterns and may generate logs or alerts about access behavior.

Mitigation: Confirm this monitoring is acceptable for the deployment environment and limit access to metadata, logs, and alerts to authorized operators.

Risk: Crawler detection can produce false positives that lead to unnecessary operational response.

Mitigation: Keep countermeasures manual, review the alert evidence before acting, and tune thresholds such as detection sensitivity, analysis window, and cooldown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/z)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with structured alert examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces passive detection summaries, operator alerts, audit log guidance, and recommended manual follow-up actions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
