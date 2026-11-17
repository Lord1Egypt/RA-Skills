## Description:

Helps AI-agent users and skill maintainers create, fix, harden, and validate Gog-style Google Workspace productivity workflows with practical plans, checklists, code, and verification notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn demand for Gog-style Google Workspace workflows into actionable work plans, templates, checklists, implementation support, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording and implicit invocation can route Google Workspace, CLI, Gmail, Drive, Calendar, Contacts, or bug-fix requests to this skill more often than intended.

Mitigation: Review the trigger keywords and implicit invocation policy before installation, and narrow them for environments that require stricter routing.

Risk: Workflow advice, generated commands, or configuration snippets could be incorrect for a user's specific environment.

Mitigation: Review proposed changes before execution and validate outputs against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-140251)
- [Popular ClawHub Skill Demand: Gog](https://clawhub.ai/skills/gog)
- [Popular ClawHub Skill Demand: Github](https://clawhub.ai/skills/github)
- [V2EX Community Signal](https://www.v2ex.com/t/1226876)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable workflows, templates, decision aids, assumptions, limits, and follow-up risks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
