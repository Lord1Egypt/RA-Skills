## Description:

TinyFish helps agents search the web, fetch page content, produce source-backed research, extract data, and automate browser interactions through the TinyFish CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinyfish](https://clawhub.ai/user/tinyfish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current web information, inspect URLs, summarize pages, extract structured data, and automate browser-based workflows when static page fetching is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote browsing and form interaction can expose sensitive account content, private URLs, or credentials to a third-party service.

Mitigation: Avoid entering passwords, API keys, payment data, private URLs, or sensitive account content unless that exposure has been separately reviewed and accepted.

Risk: The documented global CLI installation can broaden local execution and update risk.

Mitigation: Prefer a pinned or isolated CLI installation and review the package before installing or upgrading.

Risk: Browser automation can submit forms, click controls, or perform actions on live websites.

Mitigation: Use narrowly scoped goals, review intended actions before execution where possible, and avoid destructive or account-changing workflows without explicit approval.

## Reference(s):

- [Tinyfish ClawHub skill page](https://clawhub.ai/tinyfish/skills/tinyfish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include URLs, citations, extracted page content, structured JSON, and TinyFish CLI commands.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
