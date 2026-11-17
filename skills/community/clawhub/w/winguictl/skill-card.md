## Description:

Windows desktop automation CLI for listing windows, inspecting UI structure, locating elements, and executing explicit mouse, keyboard, clipboard, screenshot, and control actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easyteacher](https://clawhub.ai/user/easyteacher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill on authorized Windows sessions to inspect desktop application state and perform explicit, reviewable GUI automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect private desktop or chat content and perform sensitive account actions.

Mitigation: Install only for authorized Windows sessions, keep sensitive applications closed, and require explicit confirmation before WeChat send, post, call, contact, delete, export, or logout actions.

Risk: Automation can target the wrong window or stale UI state, causing unintended clicks, typing, hotkeys, window closure, or data loss.

Mitigation: Use exact window IDs, focus and snapshot the target window, prefer HWND or UIA runtime IDs over coordinates, preview with --dry-run, and re-snapshot after each action.

Risk: Unattended automation can continue after desktop context changes.

Mitigation: Avoid unattended auto-reply workflows and add state checks, error handling, and human oversight for critical operations.

Risk: Dependency and provenance review is limited because no server-resolved GitHub import provenance is available.

Mitigation: Install dependencies in a virtual environment from trusted indexes, pin known-good versions, and review dependency provenance before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/easyteacher/skills/winguictl)
- [Security Guidelines](references/SECURITY.md)
- [Dependencies](references/dependencies.md)
- [Output Format](references/output-format.md)
- [Window Commands](references/window.md)
- [Snapshot Commands](references/snapshot.md)
- [Find Commands](references/find.md)
- [Action Commands](references/action.md)
- [Control Commands](references/control.md)
- [Screenshot Commands](references/screenshot.md)
- [Wait Commands](references/wait.md)
- [Clipboard Commands](references/clipboard.md)
- [WeChat Automation Guide](assets/wechat/wechat.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with PowerShell command examples; CLI execution results are JSON or boundary-marked text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Use exact window and element identifiers, dry-run previews, and refreshed snapshots before actions.]

## Skill Version(s):

0.6.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
