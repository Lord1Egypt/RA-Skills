## Description:

Desktop automation via PyAutoGUI for mouse and keyboard actions, GUI testing, click and type sequences, screen-based workflows, and repetitive desktop tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangye230147961](https://clawhub.ai/user/yangye230147961)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to control desktop applications with PyAutoGUI for visual testing, repetitive UI tasks, screenshots, image-based clicking, keyboard shortcuts, and form filling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the active desktop through mouse and keyboard automation.

Mitigation: Run it only while watching the desktop and keep PyAutoGUI fail-safe enabled.

Risk: The typing helper prints the text it types, which can expose passwords, tokens, or other sensitive values.

Mitigation: Do not use scripts/type_sequence.py for secrets or sensitive text.

Risk: Full-screen screenshots can capture sensitive content visible on the desktop.

Mitigation: Avoid full-screen screenshots when sensitive apps or data are visible; prefer constrained screenshot regions.

Risk: Desktop automation dependencies and scripts may interact with sensitive local applications.

Mitigation: Review before installing and use a least-privileged virtual environment where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangye230147961/skills/pyautogui-skill)
- [Publisher profile](https://clawhub.ai/user/yangye230147961)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable Python helper scripts for screenshots, image clicking, mouse movement, keyboard shortcuts, and typing text.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
