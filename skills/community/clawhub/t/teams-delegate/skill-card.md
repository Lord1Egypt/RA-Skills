## Description: <br>
Delegates Microsoft Teams inbox management to an AI agent for message summaries, priority filtering, drafts, and replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[takeovernat](https://clawhub.ai/user/takeovernat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees who use Microsoft Teams can have an agent review chats, summarize unread conversations, draft context-aware replies, and send approved responses while escalating urgent, sensitive, or VIP messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and send Microsoft Teams messages from the user's Microsoft account. <br>
Mitigation: Use least-privilege Microsoft Graph permissions, require human approval for sensitive or VIP messages, and keep auto-reply windows time-limited. <br>
Risk: Broad Microsoft Graph permissions or tenant-wide admin consent could expose workplace messages beyond the intended workflow. <br>
Mitigation: Avoid tenant-wide admin consent unless required and limit consent to the smallest scopes needed for the user's task. <br>
Risk: Reusable authentication tokens are cached locally. <br>
Mitigation: Protect the local token cache and delete or revoke it when the delegation period ends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/takeovernat/teams-delegate) <br>
- [Microsoft Graph API reference](references/graph-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text Teams summaries or replies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft Graph permissions and stores reusable Microsoft authentication tokens locally.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
