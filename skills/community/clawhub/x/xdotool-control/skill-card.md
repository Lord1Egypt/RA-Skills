## Description:

Mouse and keyboard automation using xdotool for clicking Chrome extension icons, typing into GUI apps, switching browser tabs, and running screenshot-verify-click loops when browser relay control is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremysommerfeld8910-cpu](https://clawhub.ai/user/jeremysommerfeld8910-cpu)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to control Linux desktop windows, Chrome UI, mouse clicks, keyboard input, screenshots, and tab navigation when browser protocol access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live GUI actions can affect real applications immediately.

Mitigation: Use a dedicated desktop or browser session and verify the target window before any click, type, tab, or close-tab action.

Risk: Screenshots may capture sensitive pages and remain in /tmp.

Mitigation: Keep sensitive pages hidden during use and remove generated screenshots after verification.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include command examples, script invocations, screenshot file paths, and verification guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
