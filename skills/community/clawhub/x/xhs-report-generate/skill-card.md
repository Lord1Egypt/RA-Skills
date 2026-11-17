## Description:

Searches Xiaohongshu public notes, note details, comments, and creator posts so an agent can support trend research, competitor analysis, KOL screening, and marketing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, creators, and analysts use this skill to collect public Xiaohongshu data by keyword, note URL, or creator profile URL, then pass structured results to downstream summarization, comparison, and report generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Guaikei API token, search terms, Xiaohongshu URLs, and request parameters to a third-party API service.

Mitigation: Use only after confirming the API service is acceptable for the data involved, and prefer deployments that pass credentials through authorization headers with documented retention practices.

Risk: Generated log files may contain sensitive Xiaohongshu URLs, xsec_token values, search terms, or business research results.

Mitigation: Treat the logs directory as sensitive, restrict access, delete logs when no longer needed, and prefer versions that make logging opt-in and redact URL tokens.

Risk: The authoritative security review marked the release as needing review because it handles credentials and saved results in ways users may not expect.

Mitigation: Review the skill before installation and scan the release artifact before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-report-generate)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results are written to local JSON log files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
