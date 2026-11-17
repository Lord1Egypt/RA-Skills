## Description:

xhs-word-cloud helps agents search public Xiaohongshu notes, retrieve note details and comments, and collect public creator posts for content research and competitive analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market analysts, and agent developers use this skill to collect structured public Xiaohongshu data for topic research, competitor monitoring, KOL screening, trend analysis, and follow-on reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note/profile URLs, limits, and GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use the skill only when that data sharing is acceptable, and treat GUAIKEI_API_TOKEN as a secret that is monitored and rotated when needed.

Risk: Generated local logs can retain saved comments or competitive research results.

Mitigation: Regularly delete the generated logs directory when the collected data should not persist locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-word-cloud)
- [Guaikei API service](https://www.guaikei.com)
- [Parameter and invocation guide](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance]

**Output Format:** [Structured JSON results from Node.js CLI commands, with optional local JSON log files and concise markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, note URL, creator profile URL, sort, time, content type, and limit parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
