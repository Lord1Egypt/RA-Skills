## Description:

Searches Xiaohongshu public notes by brand or product keyword, retrieves note details and comments, and helps monitor authentic customer feedback for marketing analysis and product improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, and analysts use this skill to collect public Xiaohongshu keyword results, note details, comments, and creator posts for content planning, competitive monitoring, KOL screening, and reputation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords, note URLs, profile URLs, and retrieved public data are sent to the GUAIKEI third-party API.

Mitigation: Use the skill only when this data sharing is acceptable, and avoid submitting sensitive or confidential URLs and keywords.

Risk: The skill requires a GUAIKEI_API_TOKEN and token handling deserves installation-time review.

Mitigation: Use a limited or disposable token where possible and rotate or revoke it after high-risk use.

Risk: Results are saved locally under a logs directory, which may retain tokenized links or analysis inputs.

Mitigation: Review and delete local logs after use according to the user's data retention requirements.

## Reference(s):

- [Skill options and invocation guide](references/options.md)
- [Changelog](references/changelog.md)
- [GUAIKEI API service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands; executed commands return structured JSON and save local result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, note URL, creator profile URL, content type, sort, time range, and limit parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
