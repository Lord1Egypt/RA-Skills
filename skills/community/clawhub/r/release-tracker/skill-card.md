## Description: <br>
Track GitHub repository releases and generate prioritized summaries with delivery to Discord, Telegram, Slack, or plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jo9900](https://clawhub.ai/user/jo9900) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release managers use this skill to monitor one or more GitHub repositories, prioritize release-note changes by configured keywords, and deliver concise update summaries to chat channels or text output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled release monitoring can post summaries to external chat channels. <br>
Mitigation: Verify every outputChannel before enabling Discord, Telegram, or Slack delivery, and start with text output or a private channel. <br>
Risk: GitHub release checks require an authenticated GitHub CLI session. <br>
Mitigation: Use a least-privileged GitHub login for release monitoring. <br>
Risk: The local CHANGELOG fallback reads from a configured package path when release body content is sparse. <br>
Mitigation: Avoid the local CHANGELOG fallback unless the exact file path has been explicitly approved. <br>


## Reference(s): <br>
- [Configuration Examples](references/config-examples.md) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text summaries, JSON configuration examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Discord forum posts, Discord channel messages, Telegram messages, Slack messages, and plain text output with channel-specific length and formatting constraints.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
