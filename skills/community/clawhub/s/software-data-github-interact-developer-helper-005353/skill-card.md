## Description:

Helps agent users, skill authors, maintainers, and teams plan and carry out GitHub-style development workflows such as bug fixing, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent users, skill authors, maintainers, and teams use this skill to structure practical GitHub-style work: clarify the request, inspect constraints, produce code or workflow artifacts, and verify the result. It is suited to bug fixing, setup hardening, reliability improvement, issue-oriented workflows, and adjacent skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may route unrelated requests containing common terms such as run, api, or issue through this skill.

Mitigation: Tighten or disable implicit invocation unless broad GitHub/developer workflow routing is desired.

Risk: The skill can produce development guidance, code, shell commands, or configuration that may be incomplete for a specific repository or environment.

Mitigation: Review generated changes and run the verification commands or checks before applying them to important systems.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-005353)
- [Popular ClawHub Github Skill Demand](https://clawhub.ai/skills/github)
- [GitHub Issue Creation Demand Signal](https://github.com/repoprompt/repoprompt-ce/issues/232)
- [Developer Workflow Demand Signal](https://news.ycombinator.com/item?id=48543969)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language guidance and Markdown artifacts, often with code blocks, checklists, shell commands, or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are task-dependent and should include assumptions, limits, verification notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
