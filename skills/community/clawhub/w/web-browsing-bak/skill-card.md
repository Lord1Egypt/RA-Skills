## Description:

Browse and summarize websites, extract content from URLs, search the web for information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpneuma](https://clawhub.ai/user/xpneuma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to have an agent search the web, visit supplied URLs, summarize page content, and extract public webpage information for current-information tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled fetch helper can request arbitrary URLs from the agent environment without host or redirect restrictions.

Mitigation: Use only for public web browsing, block internal networks and metadata endpoints at runtime, and avoid private hostnames, localhost URLs, secrets, tokens, or sensitive search terms.

Risk: The skill may miss JavaScript-rendered pages, blocked sites, video or audio content, and login-required content.

Mitigation: Treat results as partial when a site requires dynamic rendering, media playback, automation blocking bypasses, or credentials, and verify important facts against accessible sources.

## Reference(s):

- [Web Browsing Usage Guide](references/usage-guide.md)
- [ClawHub skill page](https://clawhub.ai/xpneuma/skills/web-browsing-bak)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown prose with links, summaries, extracted webpage content, and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper-script fetches return page title, URL, status, and content truncated to 5000 characters.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
