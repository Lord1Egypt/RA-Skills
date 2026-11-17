## Description:

Helps agent users, skill authors, maintainers, and teams create practical workflows, checklists, analysis, implementation support, and reliability improvements for Gog-style Google Workspace productivity tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn Gog-style Google Workspace productivity needs into concrete plans, templates, checklists, code changes, or decision support. It is intended for practical workflow help around bug fixing, setup hardening, reliability, and adjacent skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation keywords can cause this workflow helper to appear during unrelated Google, workspace, CLI, Gmail, Calendar, Drive, Contacts, or bug-fix tasks.

Mitigation: Invoke the skill explicitly or narrow activation before installation when broad implicit activation is not desired.

Risk: As a documentation-only workflow helper, it may still produce incorrect or incomplete guidance for a specific productivity setup.

Mitigation: Review the generated plan, checklist, code, or configuration against the user's stated success criteria before applying it.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-130446)
- [Popular ClawHub Skill Demand: Gog](https://clawhub.ai/skills/gog)
- [Popular ClawHub Skill Demand: Github](https://clawhub.ai/skills/github)
- [Google Workspace Browser Compatibility Discussion](https://news.ycombinator.com/item?id=48625428)
- [Multi-Agent Architecture Discussion](https://www.v2ex.com/t/1222063)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with code, shell, and configuration snippets when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, visible limits, validation notes, and follow-up risks when helpful.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
