## Description: <br>
Maintains separate file-based memory contexts for WhatsApp groups and direct messages so an agent can recall prior discussion, decisions, tasks, participants, and notes without mixing conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to maintain per-chat WhatsApp memory for groups and DMs, inject recent context before responding, and record decisions, tasks, participants, preferences, and follow-ups after important exchanges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores WhatsApp group and DM summaries, identifiers, tasks, preferences, and follow-ups in local plaintext files. <br>
Mitigation: Define which chats may be logged, avoid secrets and sensitive personal data, set retention and deletion rules, and restrict filesystem permissions before use. <br>
Risk: Cross-chat search, owner briefings, or git backup integration can surface or replicate private conversation context beyond the original chat. <br>
Mitigation: Review search and briefing outputs before sharing them, keep backups private, and disable or tightly scope git backup workflows for sensitive chats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/whatsapp-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell functions and local file layout examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads local plaintext memory files under $HOME/.openclaw/workspace/memory/whatsapp when the shell functions are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
