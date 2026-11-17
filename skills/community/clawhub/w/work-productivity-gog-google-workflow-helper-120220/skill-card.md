## Description:

Helps agent users and skill authors create, repair, harden, and validate Gog-style Google Workspace productivity workflows with practical plans, checklists, analysis, code guidance, and local-first decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn Gog-style Google productivity needs into concrete workflows, implementation plans, bug-fix guidance, safety hardening steps, and reusable checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad Google, Workspace, CLI, or bug-fix requests where a more specific skill would be preferable.

Mitigation: Narrow triggers or invocation policy when precise routing matters, and review the proposed workflow before deployment.

Risk: Workflow or code guidance could be incorrect or incomplete for a user's specific productivity setup.

Mitigation: Validate outputs against the stated success criteria and keep assumptions, limits, and required inputs visible to reviewers.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill release page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-120220)
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog)
- [Hacker News: Gmail storage discussion](https://news.ycombinator.com/item?id=48969253)
- [Hacker News: local Git-backed notes workflow discussion](https://news.ycombinator.com/item?id=48968447)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing workflow artifacts and verification notes; no code execution, credential handling, persistence, or hidden data access is indicated by the security evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
