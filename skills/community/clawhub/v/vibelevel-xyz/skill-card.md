## Description: <br>
Check any GitHub developer's vibe score across 7 dimensions, compare coders, view leaderboards, and summarize who's shipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therealstein](https://clawhub.ai/user/therealstein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to look up public GitHub profile vibe data, compare two GitHub users, or summarize vibelevel.xyz leaderboard-style signals in an agent response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The lookup script sends the GitHub usernames requested by the user to vibelevel.xyz. <br>
Mitigation: Use the skill only when an external lookup is intended, and avoid submitting usernames that should not be shared with the service. <br>
Risk: The skill depends on a curl-based external service request and may fail when vibelevel.xyz is unavailable, rate limited, or returns an error. <br>
Mitigation: Handle returned error messages in the agent response and ask the user to retry or verify the username when appropriate. <br>


## Reference(s): <br>
- [Vibelevel homepage](https://vibelevel.xyz) <br>
- [Vibelevel profile URL pattern](https://vibelevel.xyz/USERNAME) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with shell command execution guidance and parsed JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq on macOS or Linux; sends requested GitHub usernames to vibelevel.xyz for lookup.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
