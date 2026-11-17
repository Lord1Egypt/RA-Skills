## Description:

Instinct-based continuous learning system that captures confidence-scored, project-scoped learnings and helps agents evolve them into reusable skills, commands, and agent guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, and recurring project patterns as instincts or learning entries, then review, promote, and evolve those learnings into reusable agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent observation of broad tool activity can capture sensitive project or session data.

Mitigation: Prefer project-level hooks, add redaction and retention limits before enabling broad observation, and keep learning files out of version control unless intentionally sharing.

Risk: Promoting session learnings into future agent instructions can preserve incorrect or misleading guidance.

Mitigation: Require human review before promotion and scan generated or evolved skills before deployment.

## Reference(s):

- [Self Improving Agent ClawHub listing](https://clawhub.ai/huamu668/skills/self-improving-agent-ecc)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML instinct examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update learning files, project-scoped instinct files, hook configuration, and generated skill, command, or agent drafts when applied by an agent.]

## Skill Version(s):

2.1.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
