## Description:

Windows Desktop browser remote-control guidance for using Edge or Chrome to open pages, interact with sites, capture screenshots, package downloads, and return evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louisownopenclaw-netizen](https://clawhub.ai/user/louisownopenclaw-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide remote Windows Desktop browser work such as navigation, UI interaction, screenshots, and download packaging for browser-based tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions in an authenticated desktop browser session with broad access to pages, accounts, screenshots, and downloads.

Mitigation: Use an isolated Desktop or browser profile, avoid unrelated logged-in accounts, and keep the remote session scoped to the requested task.

Risk: Screenshots and download archives may expose sensitive information or include files outside the intended task.

Mitigation: Capture only the target browser window when possible, archive only files produced for the current task, and review a manifest or preview before uploading evidence.

## Reference(s):

- [Workflow Notes](references/api_reference.md)
- [Edge Automation Playbook](references/edge_playbook.md)
- [Windows Browser Ops ClawHub Release](https://clawhub.ai/louisownopenclaw-netizen/skills/windows-browser-ops)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with PowerShell command snippets and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create screenshots, logs, or ZIP archives as task evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
