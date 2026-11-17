## Description:

Scrcpy Claw helps agents control Android devices through ADB and scrcpy, including touch input, keyboard input, system operations, screen analysis, AI-assisted automation, and action recording/playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[italks](https://clawhub.ai/user/italks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation teams use this skill to inspect and control authorized Android devices, automate UI workflows, and record or replay device actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue powerful Android device actions, including app control, clipboard changes, screenshots, screen recording, uninstall operations, data clearing, and replayed actions.

Mitigation: Use only on devices the operator owns or has explicit permission to control, prefer test devices, and require manual approval before destructive or privacy-sensitive actions.

Risk: The security review reports a text-input command-injection risk.

Mitigation: Avoid sensitive apps and passwords until the issue is fixed; review and sanitize text before sending it to device input commands.

Risk: Screen captures, UI dumps, clipboard operations, and recordings can expose private device content.

Mitigation: Keep Wi-Fi ADB disabled unless needed, avoid sensitive apps during automation, and handle saved screenshots, UI dumps, recordings, and action scripts as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/italks/skills/scrcpy-claw)
- [Publisher profile](https://clawhub.ai/user/italks)
- [Scrcpy Control Commands Reference](artifact/references/scrcpy-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with Python examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device-control commands or automation steps that should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact skill.json and README list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
