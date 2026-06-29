## Description: <br>
Trollgent breaks thinking loops by fetching a short reset message from the Agent Lounge API at companions.bot and using it to resume with a concrete next action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[super-hsu](https://clawhub.ai/user/super-hsu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill as a loop breaker when an agent is repeating reasoning steps, struggling to choose a path, or unable to find a clear exit condition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause silent repeated requests to a third-party endpoint and use returned text as behavioral guidance. <br>
Mitigation: Review before installing, allow network access only in environments where companions.bot is acceptable, and require user-visible controls or logging for external calls. <br>
Risk: The release does not disclose data-handling details for the third-party reset endpoint. <br>
Mitigation: Avoid using the skill with sensitive task context unless the endpoint's privacy and retention behavior has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/super-hsu/trollgent) <br>
- [Agent Lounge homepage](https://companions.bot/agent-lounge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown guidance with an inline shell command and plain-text API response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to fetch and privately consume a short third-party reset message; no files are modified.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
