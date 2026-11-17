## Description:

Fetches current top trending topics on X (Twitter) for any country using public aggregators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anishtr4](https://clawhub.ai/user/anishtr4)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve current X trend names, ranks, links, and available volume data for a selected country without logging into X.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches and displays third-party web content, which can change, become unavailable, or include unexpected terminal output.

Mitigation: Sanitize displayed trend text, use JSON mode for scripted consumption, and review output before using it in downstream automation.

Risk: Network requests currently depend on the public aggregator responding promptly and with a manageable response size.

Mitigation: Add request timeout and response-size limits before using the skill in shared or automated environments.

Risk: Dependency and lockfile age can affect CLI reliability and supply-chain exposure over time.

Mitigation: Update dependencies and regenerate the lockfile before publication or deployment.

## Reference(s):

- [X Trends ClawHub Skill Page](https://clawhub.ai/anishtr4/skills/x-trends)
- [getdaytrends.com](https://getdaytrends.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands]

**Output Format:** [Colorized terminal table or JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited by user-supplied country and count options, and depend on public getdaytrends.com availability and content.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence; artifact SKILL.md and package.json declare 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
