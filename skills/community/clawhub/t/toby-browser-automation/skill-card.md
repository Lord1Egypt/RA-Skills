## Description: <br>
Automate web browser interactions using natural language via CLI commands for browsing websites, navigating pages, extracting data, taking screenshots, filling forms, clicking buttons, and interacting with web applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser navigation, page actions, structured extraction, element discovery, screenshots, and browser session control through local Chrome or SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a browser, interact with logged-in accounts, retain cookies, save screenshots and downloads, and access internal network sites. <br>
Mitigation: Use isolated browser profiles or test accounts, avoid sensitive financial or administrative workflows, and clear profile and download folders after use. <br>
Risk: Browser actions can submit forms, download files, make purchases, change accounts, or extract private page content. <br>
Mitigation: Require explicit user confirmation before submissions, downloads, purchases, account changes, or extracting private content. <br>
Risk: Remote mode can route AI browser actions or extraction through SkillBoss API Hub. <br>
Mitigation: Use remote mode only for data approved for third-party processing, and prefer local browser mode for sensitive pages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-browser-automation) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [Examples](EXAMPLES.md) <br>
- [CLI reference](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, CLI JSON responses, screenshots, and downloaded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Chrome when no SKILLBOSS_API_KEY is configured and SkillBoss API Hub remote mode when the key is present.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
