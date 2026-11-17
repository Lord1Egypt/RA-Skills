## Description:

Searches public Xiaohongshu notes by keyword and retrieves note details, comments, and creator post lists for content research, trend discovery, KOL evaluation, and competitive analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External content creators, marketers, analysts, and agent operators use this skill to collect public Xiaohongshu note and creator data for topic research, trend tracking, comment analysis, and competitive review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note or profile URLs, and retrieved public content or comments to guaikei.com.

Mitigation: Use only when the user is authorized to share the requested public data with that service.

Risk: API credentials may be exposed if tokens are printed, logged, or passed through URL query strings.

Mitigation: Configure GUAIKEI_API_TOKEN through the environment, avoid printing it, rotate exposed tokens, and ask the publisher to move authentication out of query strings.

Risk: Saved logs can retain public comments, content, links, and interaction data that may be sensitive in context.

Mitigation: Treat logs as sensitive working data, delete them when no longer needed, and request redaction or no-save controls where appropriate.

Risk: Broad social-media requests could trigger the skill when the user did not explicitly intend Xiaohongshu data collection.

Mitigation: Confirm the platform and target input before running commands, especially for vague trend or popular-content requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-look-note-guaikei)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Files, Guidance]

**Output Format:** [JSON stdout and saved log files, with Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require GUAIKEI_API_TOKEN and may save retrieved results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
