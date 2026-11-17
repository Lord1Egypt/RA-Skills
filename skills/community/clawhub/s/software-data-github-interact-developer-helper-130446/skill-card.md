## Description:

Helps agent users and maintainers plan, implement, and verify GitHub-style developer workflows such as bug fixes, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and AI-agent users use this skill to turn GitHub-style development requests into practical workflows, checklists, code changes, analysis, or implementation support. It is aimed at local-hardware-friendly work where the agent clarifies constraints, produces an actionable deliverable, and verifies the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate broadly for developer and GitHub-related requests.

Mitigation: Confirm the skill is relevant to the current task before relying on its workflow or recommendations.

Risk: Generated code, workflow, or repository-change guidance may affect local repository state or public GitHub content.

Mitigation: Review proposed changes and run appropriate verification before applying code, configuration, or workflow updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-130446)
- [Requirement Plan](references/requirement-plan.md)
- [GitHub Workflow Demand Evidence](https://clawhub.ai/skills/github)
- [GitHub Issue Evidence](https://github.com/420KanaCoin/integrate-mcp-with-copilot/issues/1)
- [Hacker News GitHub Platform Discussion](https://news.ycombinator.com/item?id=48611303)
- [Hacker News GitHub CI Discussion](https://news.ycombinator.com/item?id=48624574)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, verification notes, reusable checklists, and follow-up risks when useful.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
