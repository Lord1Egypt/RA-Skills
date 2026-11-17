## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and collects public creator posts for content research, competitor analysis, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External creators, brand marketers, market analysts, and agent developers use this skill to collect structured public Xiaohongshu data for topic research, competitor monitoring, comment analysis, creator review, and trend reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, target URLs, and the GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Use a scoped token, rotate it as needed, and run the skill only when sharing those inputs with Guaikei is acceptable.

Risk: Generated logs may contain research history, comments, and access-bearing Xiaohongshu URLs.

Mitigation: Store logs in a protected location and periodically delete logs that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-note-detail)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON results on stdout with optional Markdown guidance and local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js and GUAIKEI_API_TOKEN; result logs are written under logs/.]

## Skill Version(s):

1.0.0 (source: skill metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
