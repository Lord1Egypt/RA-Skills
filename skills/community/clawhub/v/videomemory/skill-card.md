## Description:

Start VideoMemory from OpenClaw and return the local UI link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clamepending](https://clawhub.ai/user/clamepending)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, start, relaunch, or check VideoMemory and retrieve the local UI link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party package installation can add OpenClaw bridge files and start a local VideoMemory service.

Mitigation: Install only if the @clamepending/videomemory package is trusted, review the --safe --explain onboarding plan before setup, and use a constrained environment when stronger supply-chain isolation is needed.

Risk: Onboarding or relaunch failures could leave the user without a reliable UI link.

Mitigation: Run the documented safe onboarding, relaunch, and health-check commands, and report actual stderr when a command fails.

## Reference(s):

- [VideoMemory ClawHub skill page](https://clawhub.ai/clamepending/skills/videomemory)
- [VideoMemory homepage](https://github.com/Clamepending/videomemory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with shell commands and a local UI link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful onboarding or relaunch returns the VideoMemory local UI link; failures should report the actual stderr.]

## Skill Version(s):

0.1.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
