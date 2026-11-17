## Description:

Scan local or staged ClawHub skills before installation; report High/Critical findings and optionally quarantine managed skills. A scan is not proof of safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-allen-oneal](https://clawhub.ai/user/jason-allen-oneal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to scan local or staged ClawHub skills before installation, inventory installed skill roots, review scanner reports, and optionally quarantine managed skills with High or Critical findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local shell wrappers that can copy installed skill directories and move managed skills into quarantine.

Mitigation: Review the wrapper scripts and run them only from a trusted workspace with paths and environment variables set deliberately.

Risk: The wrappers depend on separate local tools and packages, including the Cisco skill scanner checkout, the OpenClaw CLI for catalog mode, and npm-resolved clawhub staging.

Mitigation: Trust and review those dependencies before using `--catalog`, staged install, or optional watcher flows.

Risk: A clean or warning-only scan can still miss unsafe behavior, and scanner errors or malformed reports do not establish safety.

Mitigation: Treat reports as review evidence, keep fail-closed behavior enabled, and do not execute candidate skill code as part of review.

Risk: Filesystem discovery and systemd path templates do not provide complete catalog coverage or a pre-load security boundary.

Mitigation: Use explicit roots or trusted catalog mode for intended sources, and do not rely on the watcher as the only installation control.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/jason-allen-oneal/skills/skill-scanner-guard)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [COMPATIBILITY.md](artifact/COMPATIBILITY.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with inline bash commands and local scanner report paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, python3, and uv; ClawHub staging also requires npx. Scanner reports should be reviewed and are not safety guarantees.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
