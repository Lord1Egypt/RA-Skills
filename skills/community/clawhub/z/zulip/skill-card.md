## Description: <br>
Interact with Zulip chat platform via REST API and Python client. Use when you need to read messages from streams/topics, send messages to channels or users, manage DM conversations, list users, or integrate with Zulip organizations for team communication workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suky57](https://clawhub.ai/user/suky57) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a Zulip organization for reading streams, topics, direct messages, and mentions, and for sending messages or sharing uploaded files through a configured bot account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and send Zulip chat content using the permissions of the configured bot account. <br>
Mitigation: Use a restricted bot account and review recipients, topics, message content, and uploaded files before allowing send or upload actions. <br>
Risk: The Zulip bot API key grants access to organization data and actions available to that bot. <br>
Mitigation: Protect the zuliprc file, avoid putting real keys directly in shell commands, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Zulip API Quick Reference](references/api-quick-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, shell, curl, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that call the Zulip API using credentials from a zuliprc configuration file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
