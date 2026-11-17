## Description:

Drive web, mobile, desktop, and game interfaces with natural language using the Qirabot Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellof20](https://clawhub.ai/user/hellof20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to create Qirabot-driven UI automation, testing, scraping, visual verification, and RPA workflows across browsers, Android, iOS, desktop apps, and games.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can view and act on the target screen during UI automation.

Mitigation: Run it only for approved UI automation tasks, avoid privileged accounts, and require explicit approval before purchases, posts, deletes, account changes, or other irreversible actions.

Risk: Automation outcomes can be wrong or incomplete even when a run reports success.

Mitigation: Review generated reports and screenshots for human-facing results, and use independent verification checks when scripts must branch on the outcome.

Risk: Browser profiles, reports, screenshots, and recordings can contain sensitive account or screen data.

Mitigation: Keep persistent profiles scoped per site and task, protect report directories, and avoid exposing secrets or privileged sessions.

Risk: Unpinned dependencies or mismatched local environments can cause unreliable automation behavior.

Mitigation: Use a virtual environment, run the included preflight before writing automation, and pin package versions when repeatability matters.

## Reference(s):

- [Qirabot skill page](https://clawhub.ai/hellof20/skills/qirabot)
- [Publisher profile: hellof20](https://clawhub.ai/user/hellof20)
- [Qirabot API reference](references/REFERENCE.md)
- [Qirabot app](https://app.qirabot.com)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python template code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task-specific automation scripts and setup guidance; Qirabot runs may write HTML reports with screenshots and optional screen recordings.]

## Skill Version(s):

1.5.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
