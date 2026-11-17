## Description:

Skill Gardener helps agents create or repair local skills from verified reusable workflows after a non-obvious fix, recurring procedure, stale skill, or request to save a workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadowninex](https://clawhub.ai/user/shadowninex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skill Gardener to preserve verified procedures as local skills, repair stale skill instructions, validate staged candidates, and link them back to source evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized use can modify user-owned skill files and influence future agent behavior.

Mitigation: Keep automatic gardening disabled unless desired, review proposed diffs, and validate staged candidates before applying changes.

Risk: Learning records, transcripts, tool output, and external packages can contain sensitive data or embedded instruction overrides.

Mitigation: Treat these materials only as evidence, retain no secrets or raw private transcripts, and reject instruction overrides, exfiltration, or weakened safeguards.

## Reference(s):

- [Companion integrations](references/integrations.md)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [Self-Improving Agent companion reference](https://github.com/pskoett/self-improving-agent)
- [Skill Vetter companion reference](https://clawhub.ai/spclaudehome/skills/skill-vetter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional code or configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or edit local skill files when authorized; the bundled audit helper emits JSON reports.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
