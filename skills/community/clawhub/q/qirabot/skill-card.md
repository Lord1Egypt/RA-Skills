## Description: <br>
Qirabot helps agents drive web, mobile, desktop, and game interfaces with natural-language actions through the Qirabot Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellof20](https://clawhub.ai/user/hellof20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and automation engineers use Qirabot to create UI automation scripts for browsers, mobile apps, desktop applications, and games when selectors are unavailable or visual validation is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Qirabot-driven automation can see and act on the target app, browser, or account session. <br>
Mitigation: Use dedicated test accounts or constrained sessions when possible, avoid screens with secrets or regulated data, and review generated reports before sharing them. <br>
Risk: Automation may perform irreversible or outward-facing actions such as purchases, posts, or deletions. <br>
Mitigation: Require explicit human confirmation before acting under a logged-in account or completing actions that change external state. <br>
Risk: Screenshots, HTML reports, and optional recordings can capture sensitive UI content. <br>
Mitigation: Keep recording disabled unless needed, limit report sharing, and remove sensitive artifacts before distribution. <br>
Risk: The agent loop can report success after interacting with the wrong UI element or screen. <br>
Mitigation: Inspect step screenshots or use an independent verification check before relying on automation results. <br>


## Reference(s): <br>
- [Qirabot API reference](references/REFERENCE.md) <br>
- [Qirabot service dashboard](https://app.qirabot.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces runnable Python automation templates and operational guidance; SDK runs may create HTML reports, screenshots, and optional recordings.] <br>

## Skill Version(s): <br>
1.5.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
