## Description:

Safely validate, dry-run, publish, and verify ClawHub skills and OpenClaw plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoffrey-xiao](https://clawhub.ai/user/geoffrey-xiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect, dry-run, publish, and verify ClawHub skill or OpenClaw plugin releases while preserving user control over authentication and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish real ClawHub skills or OpenClaw plugins after authentication.

Mitigation: Use dry-runs first, present the account, target, version, file set, fingerprint, and exact command, then require explicit user confirmation immediately before publication.

Risk: Authentication changes the local credential state and may expose sensitive credentials if handled incorrectly.

Mitigation: Use the ClawHub CLI device flow, never request or print API tokens, verify the authenticated handle, and treat login approval as separate from publication approval.

Risk: A local validator result may differ from the ClawHub server dry-run or final server validation.

Mitigation: Compare the validator fingerprint with the CLI dry-run fingerprint and block publication until mismatches are explained.

Risk: An unclear publish response can make duplicate publication attempts likely.

Mitigation: Perform at most two non-mutating remote checks for that attempt, do not retry automatically, and require a corrected command plus fresh confirmation for any retry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geoffrey-xiao/skills/safe-clawhub-publisher)
- [Skill release](references/skill-release.md)
- [Plugin package release](references/plugin-release.md)
- [Release security checklist](references/security-checklist.md)
- [Version and changelog decisions](references/versioning.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub release report](assets/release-report.md)
- [ClawHub release checks workflow](assets/github-actions.yml)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands, JSON validator output, and release-report fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before authentication changes or publication; treats local validator output as evidence, not final server acceptance.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and changelog list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
