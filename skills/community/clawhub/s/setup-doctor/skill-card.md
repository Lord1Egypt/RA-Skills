## Description:

Setup Doctor diagnoses OpenClaw setup issues by checking Node.js, npm, gateway status, configuration file presence, and workspace presence with quick and opt-in full modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to troubleshoot setup failures, gateway connectivity problems, missing configuration, and workspace readiness issues. It provides quick status checks, optional deeper diagnostics, and proposed fixes that require user confirmation before changes are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local diagnostics can expose environment status, local paths, tool versions, and OpenClaw file presence in the agent transcript.

Mitigation: Review diagnostic output before sharing it outside the working context, and avoid including sensitive local details in public reports.

Risk: Fix mode may propose local setup changes that could be incorrect for a user's environment.

Mitigation: Require explicit user confirmation, show exactly what will change, and re-run diagnostics after applying a confirmed fix.

Risk: The optional full-suite install suggestion installs additional skills beyond Setup Doctor.

Mitigation: Treat the suite install as optional and review each additional skill before installation.

## Reference(s):

- [Setup Doctor ClawHub skill page](https://clawhub.ai/tommot2/skills/setup-doctor)
- [Setup Doctor homepage](https://clawhub.ai/skills/setup-doctor)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style diagnostic reports with inline shell commands and JSON output from the bundled diagnostic script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quick mode targets about 10 seconds; full diagnostics are opt-in; fix mode requires user confirmation before applying changes.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
