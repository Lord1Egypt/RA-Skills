## Description:

RLM-style long-context controller that treats inputs as external context, slices/peeks/searches, and spawns recursive subcalls with strict safety limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywyze](https://clawhub.ai/user/skywyze)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to analyze large documents, dense logs, datasets, and repositories that exceed normal context limits by storing inputs externally, planning bounded slices, spawning sub-agent analysis, and aggregating structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run bundled helper scripts and spawn sub-agent sessions, and evidence.security notes that autonomous exec and session spawning are part of the risk profile.

Mitigation: Use it only in a controlled workspace, review generated toolcalls before execution, and enable disableModelInvocation when explicit confirmation is required.

Risk: The skill writes full input copies and generated prompts to disk, while redaction has stated limits.

Mitigation: Avoid sensitive inputs unless the redaction behavior is acceptable for the workload, and run cleanup after use when temporary artifacts should not persist.

Risk: The cleanup flow can delete matching scratch files when CLEAN_RETENTION=0 is used.

Mitigation: Review cleanup retention and ignore rules before running cleanup in workspaces that contain artifacts worth preserving.

## Reference(s):

- [RLM Controller on ClawHub](https://clawhub.ai/skywyze/skills/rlm-controller)
- [OpenClaw](https://github.com/Skywyze/openclaw)
- [Getting Started Guide](docs/flows.md)
- [Security Model](docs/security.md)
- [Policy Reference](docs/policy.md)
- [Security Checklist](docs/security_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON manifests, plain-text summaries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write context copies, prompts, plans, spawn manifests, logs, and summaries to workspace scratch paths during operation.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
