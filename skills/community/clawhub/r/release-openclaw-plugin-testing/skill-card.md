## Description:

Plan and run pre-release OpenClaw plugin validation across bundled plugins, package artifacts, lifecycle commands, doctor/fix, config round-trip, gateway startup, SDK compatibility, Docker E2E, Package Acceptance, and Testbox proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to plan and run pre-release validation across plugin packages, lifecycle operations, configuration, gateway startup, SDK compatibility, and safe live-ish checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is partial because some referenced paths were missing from the bundle.

Mitigation: Review the missing paths or source bundle before relying on the clean scan verdict.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with shell command examples, a confidence matrix, and a release report template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The recommended checks depend on the release target and available credentials.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
