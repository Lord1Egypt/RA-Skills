## Description: <br>
Branch a coding session into a new conversation with full context handoff -- generate structured handoff doc, startup prompts, and guide the new session to pick up exactly where you left off. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to preserve project state when moving a long or branching coding session into a new conversation. It analyzes the current session and project, writes a structured handoff document, validates it with a checklist, and produces a startup prompt for the next session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to read broad project, IDE, identity, memory, scheduled-task, channel, connector, and environment-variable context. <br>
Mitigation: Limit scanning to project-local files unless the user explicitly approves broader WorkBuddy identity, memory, task, channel, connector, and environment-variable review. <br>
Risk: The generated handoff file may persist sensitive personal, path, project, or secret-adjacent context if not reviewed. <br>
Mitigation: Review the handoff before committing or sharing it, and use repo-relative paths and placeholders for personal or secret values. <br>


## Reference(s): <br>
- [Session Branch on ClawHub](https://clawhub.ai/edwardwason/session-branch) <br>
- [Handoff Template](references/handoff-template.md) <br>
- [Validation Checklist](references/checklist.md) <br>
- [Startup Prompts](references/startup-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown handoff document plus text startup prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create docs/session-handoff.md or .workbuddy/session-handoff.md depending on target IDE.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and changelog, released 2026-06-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
