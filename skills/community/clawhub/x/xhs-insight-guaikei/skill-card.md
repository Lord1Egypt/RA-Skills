## Description:

Searches, views, and retrieves public Xiaohongshu notes, comments, and creator posts as structured data for content research, competitor analysis, KOL screening, trend monitoring, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, and analysts use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts. The results support content planning, comment analysis, competitor monitoring, KOL screening, trend tracking, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu links, search terms, and a Guaikei API token to the Guaikei service.

Mitigation: Install and run it only when that external data sharing is acceptable, and provide a scoped token intended for this service.

Risk: Generated logs may contain research targets, comments, profile data, and Xiaohongshu URLs with xsec_token values.

Mitigation: Treat logs as sensitive output, protect or delete them after use, and avoid committing logs to source control.

Risk: The security review recommends a version that avoids placing API tokens in query strings and supports redacted logging.

Mitigation: Prefer an updated release with safer token handling and configurable or redacted logging before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-insight-guaikei)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON with optional Markdown summaries and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save task results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
