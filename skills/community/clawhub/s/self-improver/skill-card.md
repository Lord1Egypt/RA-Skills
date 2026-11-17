## Description:

Self-improving agent system for OpenClaw that enables continuous learning from interactions, errors, recoveries, and performance metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to collect learnings from sessions, errors, recoveries, and performance signals, then review, export, or apply those learnings to improve future agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning records may contain private prompts, tracebacks, secrets, or business data.

Mitigation: Inspect and redact learning JSON files and Markdown exports before reuse, sharing, or email.

Risk: Executable Python hooks are loaded from the workspace hooks directory.

Mitigation: Install only in trusted workspaces and restrict write access to the hooks directory.

Risk: Automatic learning or application of stored records can reuse unreviewed content.

Mitigation: Keep auto_learn and auto_apply disabled until stored learnings have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leohuang8688/skills/self-improver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [CLI text, Markdown exports, and JSON learning files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist learning records in the workspace and load Python hooks from the workspace hooks directory.]

## Skill Version(s):

3.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
