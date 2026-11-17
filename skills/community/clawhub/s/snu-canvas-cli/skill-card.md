## Description:

LearningX CLI helps agents operate SNU's Canvas LMS through the lx-agent command-line bridge for configuration checks, course content, assignments, files, announcements, bot mode, serve mode, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guzus](https://clawhub.ai/user/guzus)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run lx-agent CLI workflows against SNU's Canvas LMS while keeping Canvas URL verification and token handling inside the configured CLI environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unverified local Go CLI for LMS operations.

Mitigation: Install only when the lx-agent repository path and revision are trusted, pinned, and reviewed.

Risk: Canvas API tokens may be mishandled if users share or print credentials during troubleshooting.

Mitigation: Keep tokens in server-side config.yaml or CANVAS_TOKEN, and do not request, print, log, or display token values.

Risk: Bot and serve modes may have undocumented network behavior or credential handling.

Mitigation: Avoid bot or serve modes until their network behavior and credential handling have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guzus/skills/snu-canvas-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise command-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid exposing Canvas token values and should keep LMS troubleshooting tied to the configured CLI and Canvas URL.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
