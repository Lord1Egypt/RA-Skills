## Description:

Skill Alchemy Main orchestrates Lens and LEAP to turn a requested person, methodology, or skill-fusion goal into an installable SKILL.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to brief, route, and run skill distillation or fusion workflows for Claude Code or Codex, with configurable depth and checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills may incorporate mutable public skill files or fetched exemplars without strong trust controls.

Mitigation: Review sources before installation, prefer pinned versions or immutable commits, and require approval before using fetched exemplars.

Risk: Some bundled workflows may inspect prompts, responses, or persistent memory stores.

Mitigation: Inspect Lens, LEAP, and any bundled skill before use, and run only in workspaces where the operator has approved the data exposure and state changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentsope/skills/skillalchemy)
- [README_EN.md](artifact/README_EN.md)
- [Technical Documentation](artifact/技术文档.md)
- [LEAP Skill Grammar](artifact/skills/LEAP/references/skill-grammar.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated SKILL.md files and install commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create output/<target>-skill/ directories with generated skill files and intermediate evidence when the workflow runs.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
