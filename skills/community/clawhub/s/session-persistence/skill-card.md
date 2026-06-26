## Description: <br>
Helps OpenClaw preserve session context across restarts by reading, appending, and archiving local conversation summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winter1102](https://clawhub.ai/user/winter1102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw can use this skill to maintain local session summaries so agents can recover recent context after restarts and archive useful conversation notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation summaries may contain secrets, sensitive business data, or personal data saved in local memory files. <br>
Mitigation: Avoid saving sensitive data, inspect the ./memory files regularly, and delete retained summaries when they are no longer needed. <br>
Risk: Automatic reuse of previous summaries can reintroduce stale or inappropriate context into new sessions. <br>
Mitigation: Review restored summaries before relying on them and clear last-session-summary.md when starting unrelated or sensitive work. <br>
Risk: Installation requires manual AGENTS.md changes that could alter agent behavior. <br>
Mitigation: Review any AGENTS.md changes manually before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/winter1102/session-persistence) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/winter1102) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell script behavior and local file conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API calls are described; behavior depends on local memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
