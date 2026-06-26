## Description: <br>
Append to daily notes and create notes in Reflect. Use for capturing thoughts, todos, or syncing information to your knowledge graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergical](https://clawhub.ai/user/sergical) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to capture chat-derived todos, links, meeting notes, summaries, and reminders into a Reflect knowledge graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write notes and links to the user's Reflect graph using a bearer token. <br>
Mitigation: Install only when Reflect write access is intended, keep REFLECT_TOKEN private, use the narrowest token Reflect allows, and revoke the token when the skill is no longer needed. <br>
Risk: Sensitive chat content or secrets could be saved into Reflect if the agent is asked to capture them. <br>
Mitigation: Review note and link content before saving, and avoid storing secrets or sensitive content unless that is the user's explicit intent. <br>
Risk: Reflect note contents cannot be read back, edited, searched, or deleted by this append-oriented skill. <br>
Mitigation: Use the skill for capture workflows, and rely on Reflect's own interface for review, search, edits, or deletion. <br>


## Reference(s): <br>
- [Reflect](https://reflect.app) <br>
- [Reflect OAuth Developer Console](https://reflect.app/developer/oauth) <br>
- [Reflect API](https://reflect.app/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/sergical/reflect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Reflect API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REFLECT_TOKEN and REFLECT_GRAPH_ID environment variables for API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
