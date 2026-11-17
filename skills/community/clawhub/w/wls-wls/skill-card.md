## Description:

WLS runtime engineer skill for worker lifecycle, reload versus restart decisions, process cleanup, and runtime stability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose and change WLS runtime process lifecycle behavior, including worker stability, dispatcher behavior, process cleanup, and reload versus restart decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime process changes can destabilize long-running WLS workers when reload, restart, or cleanup behavior is chosen incorrectly.

Mitigation: Trace the affected lifecycle path and choose reload or restart based on the affected runtime surface before changing process code.

Risk: Validation can interfere with existing WLS services or leave temporary test instances running.

Mitigation: Use a unique dedicated WLS test instance on port 9502 or higher and confirm that it is stopped after validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/wls-wls)
- [Publisher profile](https://clawhub.ai/user/aiweline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, shell commands, validation steps, and cleanup confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should report lifecycle impact, validation evidence from a dedicated WLS test instance, and confirmation that the instance was stopped.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
