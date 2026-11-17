## Description:

Generates a daily A-share high-dividend stock batting-zone report using a five-factor dividend strategy score and pushes the ranked results to Huawei negative screen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loveapleace](https://clawhub.ai/user/loveapleace)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily ranked report for configured A-share high-dividend stocks after market close. It is designed for research-oriented monitoring and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reuses an authCode from another skill and may serialize that credential into dry-run output.

Mitigation: Configure a dedicated credential for this skill and prevent credentials from being written to dry-run files or logs.

Risk: The skill invokes a hard-coded local push script path.

Mitigation: Require explicit user approval for the integration path or replace it with a documented, configurable command.

Risk: The report depends on external market and financial data sources that may be unavailable or stale.

Mitigation: Review fallback values and displayed data freshness before relying on generated rankings.

## Reference(s):

- [Five-factor scoring formula](references/scoring-formula.md)
- [Stock Batting Zone ClawHub page](https://clawhub.ai/loveapleace/skills/stock-batting-zone)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown report content with JSON push payloads and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily report content is intended to stay under the Huawei negative screen character limit.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
