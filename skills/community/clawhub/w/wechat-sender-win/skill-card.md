## Description:

Automates WeChat Desktop for Windows with pywinauto to search contacts and send single or batch messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloud44552731-arch](https://clawhub.ai/user/cloud44552731-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a Windows automation script that sends WeChat messages to a named contact or comma-separated contact list from a logged-in desktop session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send WeChat messages from a logged-in account with weak recipient and window verification.

Mitigation: Use only with contacts and message text that can be manually verified, avoid batch sending, and visibly confirm the WeChat window and recipient before execution.

Risk: Search selects the first visible result, which can send a message to the wrong contact if names are ambiguous or search timing is unreliable.

Mitigation: Prefer an implementation with exact recipient matching, preview or confirmation before send, and conservative search delays.

Risk: Unpinned dependencies and UI automation behavior can change across WeChat, Windows, or pywinauto versions.

Mitigation: Pin dependencies and test the workflow on the target Windows and WeChat Desktop versions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloud44552731-arch/skills/wechat-sender-win)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash command examples and Python script execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, WeChat Desktop logged in and visible, Python, and pywinauto.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
