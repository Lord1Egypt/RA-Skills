## Description:

Helps AI-agent users, skill authors, maintainers, and teams plan, troubleshoot, harden, and validate Agent Browser-style productivity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn Agent Browser-style productivity needs into practical workflows, checklists, analysis, code changes, or decision support. It is especially suited for bug fixing, setup hardening, reliability improvement, and adjacent browser automation workflow planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad browser and automation activation wording.

Mitigation: Invoke it explicitly by name when workflow guidance is intended, and review outputs before applying generated browser automation changes.

Risk: Generated workflow or code guidance could be incorrect, incomplete, or unsuitable for a user's environment.

Mitigation: Validate the output against the user's stated success criteria, inspect proposed changes, and test locally before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-agent-browser-workflow-helper-140424)
- [Requirement Plan](references/requirement-plan.md)
- [Agent Browser demand signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Hacker News demand signal](https://news.ycombinator.com/item?id=48947713)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, prose, checklists, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation notes, assumptions, remaining risks, and follow-up work for the requested workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
