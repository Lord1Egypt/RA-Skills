## Description:

Auto-wires new skills into core agent files by reading skill definitions, agent rules, soul sections, and hooks, then registering the installed skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to onboard newly installed skills by extracting their triggers, rules, sections, and hooks and wiring them into persistent agent configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist instructions from installed skills into core agent behavior.

Mitigation: Use it only in controlled environments and require exact diffs before any write.

Risk: Onboarding untrusted skills may introduce broad triggers or weak review controls.

Mitigation: Review and scan each skill before onboarding, and reject unexpected writes or trigger expansion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyber-bye/skills/skill-onboarder)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown status summaries and structured configuration entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform idempotent updates to persistent agent files after confirmation.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
