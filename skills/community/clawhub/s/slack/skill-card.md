## Description: <br>
Use when you need to control Slack from Clawdbot via the slack tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace operators use this skill to let an agent perform Slack workspace actions such as reacting to messages, reading recent messages, sending or editing messages, managing pins, listing emoji, and fetching member information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack bot tokens and app scopes can expose workspace capabilities beyond the intended use. <br>
Mitigation: Install only with a trusted Slack bot token configuration, keep app scopes limited, and use the skill only in intended workspaces and channels. <br>
Risk: Message edits, deletes, pins, unpins, and reactions can change visible Slack workspace state. <br>
Mitigation: Confirm the target channel, message timestamp, and requested action before executing edits, deletes, pin changes, or reactions. <br>
Risk: Reading messages, private channel content, or member information can expose sensitive workspace data. <br>
Mitigation: Limit use to authorized channels and users, and confirm before reading private channel content or member information. <br>


## Reference(s): <br>
- [ClawHub Slack skill page](https://clawhub.ai/steipete/slack) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, guidance] <br>
**Output Format:** [JSON Slack tool requests with concise action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions may read, send, edit, delete, pin, unpin, react to messages, fetch member info, and list emoji using the configured Slack bot token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
