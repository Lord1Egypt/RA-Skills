## Description: <br>
SaaS (Screenshot As A Service) lets agents request cloud-rendered PNG or JPEG screenshots of web pages by URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kav-K](https://clawhub.ai/user/Kav-K) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add screenshot capture to agents and automations without running a browser locally. The skill supports URL screenshots with options for format, viewport, full-page capture, selectors, dark mode, cookies, headers, ad blocking, and device scale. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The screenshot provider can see submitted URLs and any cookies or headers included in requests. <br>
Mitigation: Do not send internal-only URLs, private account pages, session cookies, authorization headers, or regulated data unless the service is explicitly trusted and authorized for that use. <br>
Risk: API keys grant access to the screenshot service and cannot be recovered after registration. <br>
Mitigation: Store API keys securely and avoid exposing them in prompts, logs, screenshots, or committed files. <br>


## Reference(s): <br>
- [SnapService API](https://snap.llm.kaveenk.com) <br>
- [Register API key endpoint](https://snap.llm.kaveenk.com/api/register) <br>
- [Screenshot endpoint](https://snap.llm.kaveenk.com/api/screenshot) <br>
- [ClawHub skill page](https://clawhub.ai/Kav-K/snap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown with curl and Python examples; screenshot requests return PNG or JPEG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key; screenshot requests may include URL, format, viewport, full-page, selector, wait, scale, cookies, headers, dark mode, and ad-blocking options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
