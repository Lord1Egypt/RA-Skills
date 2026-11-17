## Description:

Adds equilibrium-constrained reasoning to OpenClaw assistants so symbolic operations are validated for balance before execution or persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[architect-sis](https://clawhub.ai/user/architect-sis)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add symbolic equilibrium checks, validation loops, and persistence-aware reasoning patterns to assistant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe import-path behavior can affect code loading.

Mitigation: Review the skill before installation and remove the hard-coded import path before running it outside an isolated environment.

Risk: File-vault behavior can affect local files when persistent storage is enabled.

Mitigation: Use FileVault only with trusted keys and records, and validate that record paths remain contained within the intended vault directory.

Risk: The optional Postgres backend can send vault data to a configured database.

Mitigation: Enable the Postgres backend only when database persistence is intended and the connection target is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/architect-sis/skills/sis-skill)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide symbolic reasoning traces, validation results, demo output, and vault configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
