## Description:

Captures learnings, errors, feature requests, and corrections so coding agents can record and promote recurring lessons into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivercagropecuaria-cyber](https://clawhub.ai/user/drivercagropecuaria-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep local learning logs for command failures, user corrections, missing capabilities, outdated knowledge, and recurring workflow lessons. It also provides optional hook reminders and guidance for promoting high-value lessons into project or workspace memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and memory files can capture secrets, personal data, transcripts, credentials, proprietary details, or raw error output.

Mitigation: Review entries before saving or sharing them, keep .learnings/ out of version control unless intentional, and avoid storing sensitive or proprietary material.

Risk: Broad hook reminders and cross-session sharing can create privacy or user-control concerns if enabled globally.

Mitigation: Prefer project-level hook configuration, replace empty matchers with narrower triggers, and enable hook behavior only after reviewing the scripts and intended scope.

Risk: Automatically promoted lessons can introduce incorrect or misleading guidance into long-lived agent memory.

Mitigation: Promote only reviewed, broadly applicable lessons and periodically prune stale or low-confidence entries.

## Reference(s):

- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and learning-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to create or update local learning files and optionally emit hook reminders; no structured API output.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
