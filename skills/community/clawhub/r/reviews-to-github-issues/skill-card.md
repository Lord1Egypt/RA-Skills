## Description:

Turns recent negative App Store / Google Play reviews into deduplicated GitHub issues - one issue per problem topic, with linked and quoted reviews, new reviews added as comments to the existing issue instead of duplicates. Uses AppGoat review data and the gh CLI (or the GitHub MCP server). Use when the user says "turn reviews into issues", "file bugs from app reviews", "what are users complaining about, make tickets", "sync App Store reviews to GitHub" or sets up a daily review triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzawadzki](https://clawhub.ai/user/rafalzawadzki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app teams use this skill to review recent low-rated App Store and Google Play feedback, group actionable reports by problem, and create or update deduplicated GitHub issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports broader app monitoring than the review-to-issue purpose describes, and its analysis of one workflow expression is incomplete.

Mitigation: Review the watch behavior and the unanalyzed workflow expression before installation.

Risk: The security guidance flags uncertainty about what AppGoat requests transmit and command-line API-key exposure.

Mitigation: Confirm the transmitted data and resolve how the API key is exposed before using the skill.

## Reference(s):

- [AppGoat REST API reference](artifact/reference/api.md)
- [AppGoat event setup guide](artifact/events/README.md)
- [ClawHub skill release](https://clawhub.ai/rafalzawadzki/skills/reviews-to-github-issues)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [GitHub issue and comment text, run reports, shell snippets, and YAML workflow configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most 5 new issues and 3 review pages per run; review quotes are limited to 200 characters each.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
