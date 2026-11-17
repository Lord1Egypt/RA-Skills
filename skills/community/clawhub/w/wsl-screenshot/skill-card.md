## Description:

Capture screenshots from WSL by calling Windows PowerShell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxuanyuan](https://clawhub.ai/user/wxuanyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents working inside WSL use this skill to capture the primary Windows screen and optionally share the saved screenshot for visual inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots can expose private information visible on the primary Windows screen.

Mitigation: Close or hide private windows before capture and review the saved image before sharing it when possible.

Risk: Captured image files remain in the configured Windows Pictures folder.

Mitigation: Delete screenshots that are no longer needed, especially after sharing or troubleshooting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxuanyuan/skills/wsl-screenshot)
- [Publisher profile](https://clawhub.ai/user/wxuanyuan)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash code blocks and PNG screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are saved to the configured Windows Pictures directory.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
