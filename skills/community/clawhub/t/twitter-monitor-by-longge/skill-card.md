## Description: <br>
Monitor X/Twitter accounts for new tweets and send notifications to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmmuffin](https://clawhub.ai/user/mmmuffin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor a configured X/Twitter account for new tweets and receive Telegram chat notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive Twitter session cookies. <br>
Mitigation: Store cookie values only in protected environment variables or a secrets manager, do not commit or paste them into logs, and review the skill before installation. <br>
Risk: The security review found insufficient handling or safety disclosure for Twitter session cookies. <br>
Mitigation: Prefer a version that uses official scoped API credentials or clearly documents cookie handling before using it with sensitive accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmmuffin/twitter-monitor-by-longge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mmmuffin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command and environment-variable instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Twitter session cookie values and Telegram bot/chat identifiers supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
