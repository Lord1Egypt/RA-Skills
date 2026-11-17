## Description:

Provides structured Xiaohongshu public-content data for viral post discovery, competitor monitoring, KOL screening, comment analysis, and marketing review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, analysts, and agent developers use this skill to retrieve structured Xiaohongshu keyword, post, comment, and creator-publication data for content planning, competitive analysis, KOL review, and trend monitoring. The skill retrieves data only and does not replace strategic judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, Xiaohongshu URLs, xsec_token-bearing links, and the GUAIKEI_API_TOKEN are sent to the Guaikei service.

Mitigation: Use the skill only when this data transfer is acceptable, and prefer a token that can be rotated.

Risk: Generated result files in the logs directory may contain sensitive research targets, URLs, or retrieved public-content data.

Mitigation: Treat logs as sensitive working data and delete old result files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-search-guaikei)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be written to a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
