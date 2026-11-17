## Description:

Generates a basic vercel.json configuration for Vercel deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to create a starter Vercel configuration file for web projects. Review the generated file before deploying because the release evidence says the script writes a fixed configuration rather than implementing all documented deployment modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can silently overwrite an existing vercel.json.

Mitigation: Run it in a clean directory or back up the existing vercel.json before execution.

Risk: The documentation advertises deployment modes and options that the release evidence says are not implemented.

Mitigation: Treat the output as a fixed starter configuration and manually adjust Vercel settings for framework, region, and deployment mode needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/vercel-config-generator)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [Text guidance with shell commands and JSON configuration content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite vercel.json in the current directory.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
