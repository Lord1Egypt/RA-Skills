## Description:

User-invoked reflection with three modes: Learn for approved project learnings, Retro for evidence-based engineering retrospectives, and Write Skill for codifying recurring patterns into reusable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkenny0](https://clawhub.ai/user/kkenny0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to record user-approved project learnings, run git-backed retrospectives, and turn repeated practices into reusable agent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project learnings can influence future agent sessions.

Mitigation: Record, update, prune, or export learnings only after explicit user invocation and review proposed .taku, AGENTS.md, or CLAUDE.md changes before approval.

Risk: Retrospectives may include contributor metadata and git-history-derived project details.

Mitigation: Review retrospective output before saving or sharing it, especially when contributor names, emails, or sensitive project context appear.

Risk: Skill-writing output can change reusable agent behavior.

Mitigation: Require user confirmation before creating or editing skills, test the skill against pressure scenarios, and review generated skill files before deployment.

## Reference(s):

- [Retrospective Report Scaffold](references/retro-report.md)
- [taku-write-skill - TDD for Documentation](references/writing-skills.md)
- [Taku Reflect on ClawHub](https://clawhub.ai/kkenny0/skills/taku-reflect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional JSONL records, shell command snippets, reports, and skill file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .taku files, retrospective reports, AGENTS.md or CLAUDE.md bootstrap blocks, or skill files only after user direction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
