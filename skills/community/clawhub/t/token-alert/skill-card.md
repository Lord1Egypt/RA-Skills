## Description: <br>
Token Alert monitors Clawdbot session token usage and reports threshold-based alerts through CLI output, an interactive dashboard, and optional notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r00tid](https://clawhub.ai/user/r00tid) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to check remaining session context, monitor active sessions, and receive warnings before token budgets are exhausted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard and local proxy can access session metadata and conversation history through a gateway token. <br>
Mitigation: Use the CLI checker for lower-risk monitoring, keep any proxy bound to localhost, rotate exposed gateway tokens, and avoid running the dashboard while browsing untrusted sites. <br>
Risk: Auto-export and auto-summary behavior can export conversation history or send summary commands into an active session. <br>
Mitigation: Leave automation disabled unless explicitly needed, review generated exports and summaries, and delete exported session data when it is no longer required. <br>
Risk: Optional provider keys, notification setup, and dashboard settings may be stored locally. <br>
Mitigation: Configure only the providers required, protect local configuration files, and confirm how to disable scheduled checks and remove stored dashboard history. <br>


## Reference(s): <br>
- [Token Alert on ClawHub](https://clawhub.ai/r00tid/token-alert) <br>
- [Clawdbot Documentation](https://docs.clawd.bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples, status summaries, and dashboard or notification setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open a local dashboard and may store dashboard settings or usage history locally when those features are used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
