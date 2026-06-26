## Description: <br>
Controls a Windows desktop browser remotely so an agent can open pages, interact with Edge or Chrome, capture screenshots, package downloads, and return evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louisownopenclaw-netizen](https://clawhub.ai/user/louisownopenclaw-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to drive a Windows desktop browser session for navigation, UI interaction, screenshots, download packaging, and evidence return through a local or Discord-mediated workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can expose screenshots, downloads, logged-in sessions, and uploaded files. <br>
Mitigation: Use a dedicated Windows account and browser profile, keep unrelated sensitive accounts closed, and require explicit confirmation before screenshots, downloads, uploads, or form submissions. <br>
Risk: The workflow allows custom PowerShell and desktop automation that may act beyond the intended browser task. <br>
Mitigation: Review commands before execution, provide or audit the missing scripts yourself, and limit the Desktop node to the minimum privileges needed. <br>
Risk: Download packaging can include stale or unrelated files from the user's Downloads directory. <br>
Mitigation: Filter files by path and modification time before zipping, then summarize the included files and timestamp when returning evidence. <br>


## Reference(s): <br>
- [ClawHub Windows Browser Ops Release](https://clawhub.ai/louisownopenclaw-netizen/windows-browser-ops) <br>
- [Edge Automation Playbook](references/edge_playbook.md) <br>
- [Workflow Notes](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline PowerShell and shell command snippets plus guidance for screenshots, logs, and ZIP handoffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an approved Windows Desktop node, an unlocked graphical session, PowerShell script execution permission, and a browser profile suitable for the requested task.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
