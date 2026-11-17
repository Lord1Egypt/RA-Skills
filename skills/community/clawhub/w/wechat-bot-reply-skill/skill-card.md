## Description:

Monitor WeChat for new messages from specific contacts and auto-reply on macOS with Peekaboo CLI or Windows with PeekabooWin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxdong-max](https://clawhub.ai/user/maxdong-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor a named WeChat contact, wait for a manual reply window, and generate or send an automated response if no manual reply is detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent monitoring can expose private WeChat message content through screenshots and pending files.

Mitigation: Use the skill only with non-sensitive chats and stop monitoring when the intended contact no longer needs auto-reply coverage.

Risk: Automated sending can reply to the wrong recipient when contact detection or window focus is incorrect.

Mitigation: Prefer review-before-send, verify the active contact immediately before sending, and enable auto-send only when wrong-recipient messages are acceptable.

Risk: Windows dependency resolution may fall back to npx, introducing avoidable dependency and execution risk.

Mitigation: Install PeekabooWin explicitly, set PEEKABOO_WIN_DIR, and avoid the npx fallback path.

Risk: Background monitoring and recurring automation may continue longer than intended.

Mitigation: Use a precise stop command that terminates the monitor process, deletes the pending file, and removes the recurring automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxdong-max/skills/wechat-bot-reply-skill)
- [Peekaboo / PeekabooWin guide](references/peekaboo-guide.md)
- [Peekaboo install documentation](https://peekaboo.sh/install.html)
- [PeekabooWin](https://github.com/FelixKruger/PeekabooWin)
- [Node.js](https://nodejs.org)
- [Python](https://python.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and PowerShell commands plus generated reply text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local pending files, screenshots, logs, and recurring automation prompts during use.]

## Skill Version(s):

5.0.0 (source: server release metadata; artifact docs identify v5 released 2026-05-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
