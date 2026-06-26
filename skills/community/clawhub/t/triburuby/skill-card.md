## Description: <br>
Helps users check in rituals, track streaks, and view tribe activity on TribuRuby. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a8ns](https://clawhub.ai/user/a8ns) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External TribuRuby users and athletes use this skill to view training context, track ritual completion and streaks, review tribe activity, and submit ritual check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a TribuRuby API key that can access training context and tribe member activity. <br>
Mitigation: Use a dedicated TribuRuby Agent API key and revoke or rotate it if the agent no longer needs access. <br>
Risk: The skill can submit ritual check-ins that affect user training records. <br>
Mitigation: Review the ritual, quantity, protocol, and date before allowing the agent to submit a check-in. <br>


## Reference(s): <br>
- [TribuRuby homepage](https://triburuby.app) <br>
- [TribuRuby agent API](https://triburuby.app/api/agent) <br>
- [ClawHub skill page](https://clawhub.ai/a8ns/triburuby) <br>
- [Publisher profile](https://clawhub.ai/user/a8ns) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text, markdown] <br>
**Output Format:** [Markdown and concise text with API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TRIBURUBY_API_KEY to access TribuRuby training context and submit check-ins when appropriate.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
