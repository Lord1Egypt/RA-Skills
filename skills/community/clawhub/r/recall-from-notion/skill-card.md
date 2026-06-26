## Description: <br>
Recall user memories from the Notion Memory Store and use them as context when personal background, preferences, past decisions, or project context would improve the response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smilelight](https://clawhub.ai/user/smilelight) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this workflow skill to let an agent retrieve relevant personal memories from a Notion Memory Store before answering context-sensitive requests. It is intended for recall and context injection, not for creating or modifying Notion records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can proactively and silently use personal memories in broad situations. <br>
Mitigation: Review privacy behavior before installing, ask for a fresh or generic answer when memory should not be used, and keep sensitive material out of the memory database. <br>
Risk: Notion access may expose private workspace content beyond the intended Memory Store if permissions are broad. <br>
Mitigation: Use least-privilege Notion access scoped to the Memory Store and avoid storing secrets or sensitive internal links there. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smilelight/recall-from-notion) <br>
- [OpenClaw Notion skill](https://clawhub.ai/steipete/notion) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Text] <br>
**Output Format:** [Markdown context block with grouped recalled memories and Notion API call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only recall; injects up to 10-15 ranked memories when relevant.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
