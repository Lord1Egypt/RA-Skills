## Description:

Set up and operate TeamPilot from zero on a clean machine. Use when cloning the TeamPilot repository, installing dependencies, starting the multi-agent runtime, driving missions in auto/manual mode, replaying runs in web UI, and troubleshooting first-run issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moolean](https://clawhub.ai/user/moolean)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to bootstrap TeamPilot, start its runtime, operate missions in auto or manual mode, inspect replay traces, and troubleshoot first-run issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow directs users to clone and run a TeamPilot repository, but the server evidence does not provide verified repository provenance.

Mitigation: Use only a known official TeamPilot repository and inspect package scripts and lockfiles before running setup commands.

Risk: Installing dependencies and starting the runtime may execute untrusted package scripts or local services.

Mitigation: Run the initial setup in an isolated environment without sensitive credentials or production access.

## Reference(s):

- [TeamPilot ClawHub skill page](https://clawhub.ai/moolean/skills/team-pilot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, runtime commands, mission operation guidance, replay workflow, API endpoint checklist, troubleshooting notes, and content quality guidance.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
