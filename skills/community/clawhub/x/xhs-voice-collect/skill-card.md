## Description:

xhs-voice-collect helps agents retrieve structured public Xiaohongshu notes, note details, comments, and creator posts for content research, competitor analysis, KOL screening, and trend insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Developers, marketers, content creators, and analysts use this command skill to collect public Xiaohongshu data through keyword search, note and comment lookup, and creator post monitoring for downstream summaries, comparisons, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and collected results to the Guaikei API.

Mitigation: Install and run it only when that external API data flow is acceptable for the user's task and authorization scope.

Risk: GUAIKEI_API_TOKEN values and Xiaohongshu URLs that include xsec_token parameters are sensitive.

Mitigation: Treat tokens and token-bearing URLs as secrets, avoid exposing them in shared workspaces, and redact them from reports or support requests.

Risk: The skill can store full collected outputs in a local logs directory.

Mitigation: Review or delete local logs regularly and use workspace log controls when results may contain sensitive social-media data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-voice-collect)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN. Successful, empty, and error CLI runs emit JSON status objects and may write full result logs locally.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
