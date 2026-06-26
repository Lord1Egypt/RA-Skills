## Description: <br>
Search the web and read page contents without API keys, with support for multi-engine search, page extraction, persistent browser interaction, screenshots, downloads, cookie banner dismissal, and JSON, markdown, or text output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiranUdi](https://clawhub.ai/user/LiranUdi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agent builders, and accessibility-focused users use this skill to search the web, extract readable page content, automate browser interactions, capture screenshots, and download files through local Playwright and HTTP scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a local browser session and interact with live websites, including logged-in or sensitive pages. <br>
Mitigation: Run it in an isolated environment, avoid sensitive sites unless each action is directly supervised, and close browser sessions when work is complete. <br>
Risk: The security summary flags broad download and persistent-browser controls that need careful review before use. <br>
Mitigation: Review generated actions before execution and avoid untrusted downloads until filename confinement and TLS verification behavior are fixed. <br>


## Reference(s): <br>
- [Web Pilot on ClawHub](https://clawhub.ai/LiranUdi/web-pilot) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON by default, with optional markdown or plain text output and generated files such as screenshots, PDFs, and downloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search returns result objects; page extraction returns readable content; browser session commands can preserve state until closed.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
