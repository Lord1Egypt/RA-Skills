## Description:

Guides GitHub issue, pull request, CI, and repository work for coding agents by turning repository context into safe action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and agent users use this skill to inspect GitHub issues, pull requests, CI, and repository context, then convert those signals into triage summaries, implementation checklists, safe command plans, and final status notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation could apply GitHub workflow guidance to repository actions the user did not intend.

Mitigation: Use the skill only for explicit GitHub issue, PR, CI, or repository-planning requests.

Risk: Authenticated GitHub tools could modify live repository state or expose private repository context.

Mitigation: Review before installing in agents with private repository access, scope credentials carefully, and require confirmation before any gh or API action that labels, assigns, comments, closes, merges, or otherwise changes live repository state.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with checklists, command plans, code or configuration snippets, and status notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI or API command plans; live repository mutations require explicit user authorization.]

## Skill Version(s):

0.1.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
