## Description:

Control Safari on macOS with AppleScript, safaridriver, screenshots, tab navigation, and real-browser read, click, and type workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to control Safari on macOS when work depends on a real Safari session, logged-in browser state, Safari-specific rendering, or an isolated safaridriver session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Safari control can expose open tabs, cookies, login state, clipboard, downloads, and visible page content.

Mitigation: Require confirmation before reading tabs, switching windows, capturing screenshots, clicking, typing, or writing local notes; prefer WebDriver or a dedicated Safari profile for risky work.

Risk: Blind clicks or keystrokes can affect the wrong page or application.

Mitigation: Run a read preflight and verify the title, URL, DOM text, focus, or screenshot before each meaningful action.

Risk: Local notes under ~/safari/ could retain sensitive browsing context if overused.

Mitigation: Store only durable permission state, approved recipes, snippets, and incident summaries; do not store secrets, raw history exports, or full browsing archives.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/safari)
- [Safari Browser Control Homepage](https://clawic.com/skills/safari)
- [AppleScript Control](artifact/applescript-control.md)
- [WebDriver and BiDi](artifact/webdriver-and-bidi.md)
- [Preflight and Permissions](artifact/preflight-and-permissions.md)
- [Screenshot and Visual Loop](artifact/screenshot-and-visual-loop.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, AppleScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Safari operating notes under ~/safari/ when the user approves persistent storage.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
