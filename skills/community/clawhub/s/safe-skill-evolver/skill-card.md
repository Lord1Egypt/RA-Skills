## Description:

Safely create, improve, audit, and refactor OpenClaw skills by analyzing skill files and proposing user-confirmed diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deathrowsushy](https://clawhub.ai/user/deathrowsushy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to draft new skills, improve existing skills, audit safety and quality, and prepare structured diffs before any approved file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad skill directories or related logs that contain sensitive details.

Mitigation: Constrain each audit or improvement task to a named skill folder and exclude credentials, .env files, private keys, session history, and unrelated projects unless separately approved.

Risk: Session notes or LEARNINGS.md updates may capture sensitive or unnecessary operational details.

Mitigation: Review and redact proposed note content before approving any write.

Risk: Proposed skill changes could introduce inaccurate, unsafe, or misleading guidance.

Mitigation: Review the diff, confirm the rationale, and run validation or security checks before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deathrowsushy/skills/safe-skill-evolver)
- [Publisher profile](https://clawhub.ai/user/deathrowsushy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured diffs, code blocks, JSON script output, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file edits, new SKILL.md drafts, validation reports, and command previews; writes require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
