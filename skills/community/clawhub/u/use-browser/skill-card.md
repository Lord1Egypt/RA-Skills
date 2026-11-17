## Description:

Automates browser interactions for social media management across Instagram, LinkedIn, and X, including posting, DMs, connection requests, lead scraping, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mathiasthu](https://clawhub.ai/user/mathiasthu)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to let an agent navigate approved social media sites, manage authenticated sessions, publish content, send outreach, extract leads, and monitor activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act inside authenticated social media accounts, including public posts, outreach, engagement, scraping, and cookie handling.

Mitigation: Require explicit previews and confirmations for posts, DMs, connection requests, engagement, scraping or export jobs, and all cookie commands.

Risk: Exported cookies or active authenticated sessions could expose social media accounts if mishandled.

Mitigation: Avoid high-value accounts, store cookie exports only in protected locations, delete cookie export files after use, and close browser sessions after workflows finish.

## Reference(s):

- [Browser Use GitHub repository](https://github.com/browser-use/browser-use)
- [Browser Use skill CLI README](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md)
- [ClawHub skill page](https://clawhub.ai/mathiasthu/skills/use-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots, page-state summaries, extracted social media data, and action confirmations through the browser-use CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
