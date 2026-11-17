## Description:

Web Automation Suite helps agents prepare Playwright-based browser automation for Chrome CDP connections, page actions, screenshots, scraping, form filling, and scheduled monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to generate and adapt Playwright helper code, shell steps, and guidance for web scraping, form automation, batch posting, file upload, and scheduled data or content monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse logged-in browser sessions through Chrome CDP or browser-state.json.

Mitigation: Use an isolated browser profile or test account, and avoid saving personal or administrative login sessions in browser-state.json.

Risk: Form submission, file upload, batch posting, and scheduled task helpers can automatically submit or publish content.

Mitigation: Require explicit review before submissions, uploads, batch posts, or scheduled runs, and test selectors and payloads in a non-production environment.

Risk: Generated state files, screenshots, and monitoring logs may contain account, session, page, or scraped data.

Mitigation: Do not commit or share generated state files or logs; store outputs in a controlled location and remove them when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxie48892-jpg/skills/web-automation-suite)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable Playwright snippets and command examples that should be reviewed before use with logged-in browser sessions.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
