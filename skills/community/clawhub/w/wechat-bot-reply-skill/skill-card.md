## Description: <br>
Monitor WeChat for new messages from specific contacts and auto-reply. Supports macOS (Peekaboo CLI) and Windows (PeekabooWin). Requires Peekaboo CLI on macOS or PeekabooWin on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxdong-max](https://clawhub.ai/user/maxdong-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
End users and personal productivity agents use this skill to monitor a named WeChat contact, wait for manual replies, and send an automated reply only when the conversation still appears unanswered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill watches private WeChat conversations through screenshots. <br>
Mitigation: Grant screen-capture access only when needed, keep unrelated sensitive content off screen, and stop the monitor when finished. <br>
Risk: The skill can send WeChat replies as the user through input automation. <br>
Mitigation: Use it only for low-risk contacts, watch initial runs, and confirm the target contact and reply style before enabling recurring automation. <br>
Risk: On Windows, fallback execution through npx may fetch or run PeekabooWin indirectly. <br>
Mitigation: Install PeekabooWin at a verified path and set PEEKABOO_WIN_DIR instead of relying on the npx fallback. <br>


## Reference(s): <br>
- [Peekaboo and PeekabooWin guide](references/peekaboo-guide.md) <br>
- [PeekabooWin project](https://github.com/FelixKruger/PeekabooWin) <br>
- [Node.js](https://nodejs.org) <br>
- [Python](https://python.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and automation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide an agent to create local screenshots, monitor logs, and pending-message state files during execution.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
