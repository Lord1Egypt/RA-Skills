## Description:

Automate web browser interactions using natural language via CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to navigate websites, click page elements, fill forms, extract structured page data, capture screenshots, and manage browser sessions through a command-line browser tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interact with arbitrary websites and accounts through broad browser automation authority.

Mitigation: Use it only on sites and accounts you are authorized to access, review actions before execution, and verify state with screenshots or observations after important steps.

Risk: Remote AI processing may be used when SKILLBOSS_API_KEY is configured.

Mitigation: Avoid entering real passwords, secrets, private customer data, or internal site content through natural-language actions unless the external routing is approved.

Risk: The browser profile can preserve authenticated session cookies between runs.

Mitigation: Use an isolated browser profile for automation and clear stored sessions when work is complete.

Risk: The skill can create screenshots and automatic downloads on disk.

Mitigation: Review and clean files under ./agent/browser_screenshots/ and ./agent/downloads/ after each workflow.

Risk: Setup requires npm install and npm link even though server evidence flags incomplete install artifacts.

Mitigation: Verify the package source, dependency tree, and lockfile before installing or globally linking the browser command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-browser-automation)
- [Complete setup guide](https://skillboss.co/skill.md)
- [Browser Automation CLI Reference](artifact/REFERENCE.md)
- [Browser Automation Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash command examples; CLI commands return JSON and file paths for screenshots or downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are saved under ./agent/browser_screenshots/ and downloads under ./agent/downloads/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
