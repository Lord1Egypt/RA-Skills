## Description:

Helps legal operations teams record redacted lessons about contract risks, compliance gaps, regulatory changes, and litigation exposure for later review and improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Legal operations staff and their agents use this skill to capture process-level legal findings in local Markdown logs, review recurring issues, and propose improvements to legal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning logs could expose privileged communications or confidential matter details.

Mitigation: Record only redacted process-level lessons; omit privileged or confidential details and keep .learnings/ out of version control unless entries are reviewed.

Risk: Optional hooks could persistently influence agent behavior outside the intended project.

Mitigation: Enable hooks only within the project after reviewing their scripts; do not install them globally.

Risk: Promoting unreviewed lessons could introduce incorrect legal guidance into agent instructions or reusable skills.

Mitigation: Require an explicitly approved diff before updating agent instruction files, rules, hooks, or generated skills.

## Reference(s):

- [ClawHub release](https://clawhub.ai/jose-compu/skills/self-improving-legal)
- [Examples](artifact/references/examples.md)
- [Hooks setup](artifact/references/hooks-setup.md)
- [OpenClaw integration](artifact/references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with optional shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local Markdown learning logs and suggest reviewed workflow updates.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
