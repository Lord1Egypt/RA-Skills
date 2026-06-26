## Description: <br>
yumweb lets agents operate a persistent, already logged-in Chromium browser to read pages, switch tabs, click, type, take screenshots, run JavaScript, and use authenticated websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumyumtum](https://clawhub.ai/user/yumyumtum) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use yumweb to give local AI agents controlled access to a persistent browser session for web reading, navigation, screenshots, form entry, and authenticated workflows such as X, Gmail, Outlook, Amazon, LinkedIn, Facebook, Instagram, and WeChat Web. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate inside logged-in browser sessions, including accounts that may contain personal or sensitive data. <br>
Mitigation: Use a separate low-sensitivity browser profile and treat the generated profile directory like credentials. <br>
Risk: The skill can post externally and submit forms through authenticated sites. <br>
Mitigation: Review every post, form submission, and account action before execution. <br>
Risk: The eval command runs arbitrary JavaScript in the active browser page. <br>
Mitigation: Only run trusted JavaScript strings and avoid untrusted or user-supplied eval payloads. <br>
Risk: The browser exposes a Chrome DevTools Protocol port for automation. <br>
Mitigation: Keep port 9333 bound to localhost and do not expose it to external networks. <br>


## Reference(s): <br>
- [ClawHub yumweb listing](https://clawhub.ai/yumyumtum/yumweb) <br>
- [README](README.md) <br>
- [Playwright Python documentation](https://playwright.dev/python/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [CLI stdout text or Markdown, JSON-serializable eval results, and PNG screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read, navigate, click, type, run JavaScript, manage tabs, fetch pages, and post to X when the browser profile is already authenticated.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata, RELEASE_NOTES_v0.1.0.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
