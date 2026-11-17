## Description:

Computer Use Agent (CUA) for macOS automation using TuriX. Use when you need to perform visual tasks on the desktop, such as opening apps, clicking buttons, or navigating UIs that don't have a CLI or API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongyu-yan](https://clawhub.ai/user/tongyu-yan)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to route GUI-only macOS tasks through TuriX, including opening applications, navigating web or desktop UIs, and resuming multi-step visual workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad macOS Screen Recording and Accessibility permissions for visual desktop control.

Mitigation: Use it only in a dedicated, low-sensitivity macOS session, grant the narrowest permissions, supervise sensitive workflows, and revoke permissions after use.

Risk: The skill relies on external TuriX-CUA code and dependencies that are not pinned by the artifact.

Mitigation: Pin and review the exact TuriX-CUA commit and dependency set before installation or execution.

Risk: GUI automation can interact with accounts, messages, financial pages, admin settings, or confidential data if tasked that way.

Mitigation: Avoid account sign-ups, OAuth, financial, messaging, admin, or confidential-data workflows unless each step is supervised.

## Reference(s):

- [TuriX-CUA setup repository](https://github.com/TurixAI/TuriX-CUA)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute macOS GUI automation after updating TuriX configuration.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
