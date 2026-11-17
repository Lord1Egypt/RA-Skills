## Description:

SystemTemp monitors system temperature, CPU status, fan-related sensor data, temperature history, alerts, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofather](https://clawhub.ai/user/ofather)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and end users can use this skill to inspect local thermal sensor readings, track recent temperature history, configure threshold alerts, and generate simple temperature reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Node package install path may fetch unpinned code that is not clearly tied to the reviewed artifact files.

Mitigation: Prefer a reviewed local install or a pinned package version, and verify that the installed temp executable matches the reviewed temp.js before use.

Risk: The skill creates temperature logs, reports, and alert configuration under the user's openclaw_workspace.

Mitigation: Run it under the intended local user account and review generated files before sharing diagnostic output.

Risk: Copying the command into /usr/local/bin makes the tool available system-wide on shared or managed machines.

Mitigation: Avoid system-wide installation unless that exposure is intended and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofather/skills/systemtemp)
- [Skill homepage](https://clawhub.ai/skills/systemtemp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown-style status, history, alert, and report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local thermal sensor files and writes logs, alert configuration, and reports under the user's openclaw_workspace.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
