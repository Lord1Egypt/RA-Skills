## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and fetches public creator post lists as structured JSON for content research, competitor analysis, KOL screening, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, marketers, content operators, and analysts use this skill to collect public Xiaohongshu content and creator data for topic research, competitor monitoring, comment analysis, KOL screening, and trend reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu queries, URLs, and a Guaikei API token to the provider.

Mitigation: Install only when that data sharing is acceptable, avoid printing the token, and rotate the token if it is exposed.

Risk: Generated logs can retain research history and token-bearing links.

Mitigation: Regularly delete or protect the logs directory and avoid sharing log files without review.

Risk: The skill is intended for public Xiaohongshu data and can be misused if pointed at private, hidden, or unauthorized content workflows.

Mitigation: Use it only for public content collection and confirm that downstream use complies with authorization and distribution limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-content-and-creator-data-guaikei)
- [Guaikei website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and writes command results to a logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
