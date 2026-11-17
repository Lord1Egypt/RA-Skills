## Description:

Advanced Windows desktop and browser automation via a local Python controller for screenshots, opening apps, navigating browsers, clicking, typing, and simple multi-step UI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzj520lyx](https://clawhub.ai/user/hzj520lyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when direct Windows desktop control is needed for local app launching, screenshots, typing, clicking, browser navigation, and short natural-language UI automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move the mouse, type, click, open applications, and control browser pages on the real Windows desktop.

Mitigation: Install and run it only when that level of local desktop control is intended, and supervise actions before allowing them on sensitive screens.

Risk: The documented wrapper uses an external hard-coded local entrypoint.

Mitigation: Review or fix the wrapper path before use so execution points to the expected local controller code.

Risk: Persistent runtime data and browser profiles may retain screenshots, failure data, browsing state, or local controller data.

Mitigation: Disable or isolate persistent browser profiles unless needed, and clean runtime/screenshots, runtime/failures, runtime/playwright_profile, and ~/.pyautogui-controller after testing.

Risk: Automated UI control can interact with passwords, account pages, legal consent dialogs, CAPTCHA flows, or confidential information.

Mitigation: Avoid using the skill on those workflows or screens; use lower-risk built-in browser or web tools where direct desktop control is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hzj520lyx/skills/pyautogui-controller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands with JSON controller results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; controller actions may return success, results, runtime, and warnings fields.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
