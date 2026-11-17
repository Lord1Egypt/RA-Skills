## Description:

Windows Agent enables local Windows desktop automation through PowerShell scripts for screen observation, screenshots, window control, mouse and keyboard input, UI Automation, clipboard access, and process management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunsettide](https://clawhub.ai/user/sunsettide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and desktop automation users use this skill to let an agent inspect and operate a local Windows desktop, target UI elements, type or click, manage windows and processes, and verify outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over the local Windows desktop, including clicks, typing, window actions, clipboard changes, and process management.

Mitigation: Require manual confirmation before clicks, typing, submits, deletions, clipboard overwrites, window closing, or process termination, and verify the active target before acting.

Risk: Name-based process or window termination can affect unrelated applications and destroy unsaved work.

Mitigation: Prefer PID-based process actions, inspect process details before termination, and avoid name-based kill or close operations unless the target is unambiguous.

Risk: Screenshots and clipboard reads can expose sensitive local data.

Mitigation: Treat screenshots and clipboard contents as sensitive, keep generated files in intended local paths, and back up or restore clipboard contents when workflows require clipboard changes.

Risk: Using screenshot logical coordinates for input actions can cause incorrect clicks on DPI-scaled displays.

Mitigation: Use UI Automation physical coordinates for mouse actions and verify coordinates before destructive or high-impact operations.

## Reference(s):

- [Windows Agent on ClawHub](https://clawhub.ai/sunsettide/skills/windows-agent)
- [sunsettide ClawHub profile](https://clawhub.ai/user/sunsettide)
- [Prerequisites](PREREQUISITES.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with PowerShell command examples, textual command output, and local file paths for generated screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshot and screen-observation workflows can produce local image files for separate visual analysis.]

## Skill Version(s):

0.0.1 (source: server release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
