## Description:

Cloud browser automation CLI for AI agents powered by Scrapeless that can navigate pages, fill forms, click buttons, take screenshots, extract data, test web apps, and automate browser tasks with residential proxies and anti-detection features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapelesshq](https://clawhub.ai/user/scrapelesshq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to drive Scrapeless cloud browser sessions for website navigation, form interaction, screenshots, extraction, web app testing, and proxy-backed browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote browsing workflows may send browsing activity, extracted data, screenshots, cookies/storage data, live preview access, or session recordings through Scrapeless.

Mitigation: Use narrowly scoped API tokens, avoid sensitive accounts and secrets, and enable recording or live preview only when necessary.

Risk: Proxy and anti-detection features can be misused or conflict with website authorization or terms.

Mitigation: Confirm site authorization and acceptable-use requirements before using proxy or anti-detection options.

Risk: Unpinned package execution can run a changed version of the Scrapeless CLI.

Mitigation: Prefer a pinned and reviewed package version for production workflows.

Risk: Command-line credentials such as API tokens, real passwords, or proxy credentials can leak through shell history or process listings.

Mitigation: Use the supported config-file or environment-variable authentication paths and avoid passing sensitive credentials directly in commands.

## Reference(s):

- [Authentication](references/authentication.md)
- [Scrapeless Dashboard](https://app.scrapeless.com)
- [ClawHub Skill Page](https://clawhub.ai/scrapelesshq/skills/scrapeless-scraping-browser-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or retrieve session IDs, screenshots, page text, URLs, titles, cookies/storage data, and live preview links through Scrapeless CLI commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
