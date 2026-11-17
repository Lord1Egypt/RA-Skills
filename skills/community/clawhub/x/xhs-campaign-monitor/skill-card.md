## Description:

XHS Campaign Monitor helps agents search Xiaohongshu public notes, inspect note details and comments, and list public creator posts for campaign research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market analysts, and agent developers use this skill to collect structured public Xiaohongshu data for topic research, competitor monitoring, comment analysis, creator tracking, and downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu URLs, keywords, and the configured GUAIKEI API token to guaikei.com.

Mitigation: Review the data-sharing path before use, configure only an intended GUAIKEI_API_TOKEN, and avoid submitting sensitive or unauthorized inputs.

Risk: CLI runs save structured result data, including tokenized URLs and collected comments, under logs/.

Mitigation: Treat generated logs as sensitive, delete them when no longer needed, and avoid shared or synced working directories unless that persistence is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-campaign-monitor)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; CLI execution returns JSON and saves JSON result files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands call guaikei.com for Xiaohongshu public-data retrieval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
