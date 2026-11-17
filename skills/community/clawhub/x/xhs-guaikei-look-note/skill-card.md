## Description:

This skill helps an agent search public Xiaohongshu notes, fetch note details and comments, and list public creator posts for content research, competitor monitoring, trend analysis, and KOL evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market analysts, and MCN teams use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator post lists for content planning, competitor research, sentiment review, trend monitoring, and influencer evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real Guaikei API token and selected Xiaohongshu URLs or keywords may be used during execution.

Mitigation: Use a low-privilege or disposable token, keep it out of shared environments, and confirm authorization before sending URLs or keywords to guaikei.com.

Risk: Command results are automatically stored in a local logs directory.

Mitigation: Avoid shared workspaces for sensitive research targets, and inspect or clean the logs directory after use.

Risk: The skill is intended only for public Xiaohongshu data and does not support private or login-required content.

Mitigation: Use only public URLs or keywords that the user is allowed to process, and do not use the skill to obtain private, hidden, or login-gated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-guaikei-look-note)
- [engheng-art publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API and token site](https://www.guaikei.com)
- [Parameter and invocation reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands return structured JSON/text results and save local result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, note URL, creator profile URL, filters, sort mode, time range, and result limit parameters.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
