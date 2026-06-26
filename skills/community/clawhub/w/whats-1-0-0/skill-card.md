## Description: <br>
Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to send WhatsApp messages to third parties, authenticate wacli, sync or backfill WhatsApp history, or search chats and messages on explicit request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WhatsApp messages or files to direct chats and groups. <br>
Mitigation: Require an explicit recipient and message or attachment, then confirm the recipient, group versus direct chat, message text, and attachment path before sending. <br>
Risk: Authentication and sync can retain WhatsApp history locally under ~/.wacli. <br>
Mitigation: Use sync or backfill only when needed, and review or remove ~/.wacli when local WhatsApp history should not be retained. <br>
Risk: The skill depends on the external wacli package source. <br>
Mitigation: Install only when the external wacli source is trusted and the user accepts QR-based WhatsApp account linking. <br>


## Reference(s): <br>
- [wacli homepage](https://wacli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/whats-1-0-0) <br>
- [Homebrew formula steipete/tap/wacli](steipete/tap/wacli) <br>
- [Go module github.com/steipete/wacli/cmd/wacli](github.com/steipete/wacli/cmd/wacli@latest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON output when the agent needs machine-readable wacli results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
