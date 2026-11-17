## Description:

Rental Helper helps renters record listings, calculate rental budgets, compare options, track viewings, review rental pitfalls, and optionally parse listing pages or screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sosshuai](https://clawhub.ai/user/sosshuai)

### License/Terms of Use:

MIT-0

## Use Case:

Renters and housing-search assistants use this skill to collect rental listings, estimate affordability, compare tradeoffs, record viewing notes, and surface practical lease-checklist guidance. Agents can also use its helper scripts to import listings, parse user-provided pages or screenshots, and generate recommendations from locally stored listing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Listing, viewing, screenshot-derived, and contact details may be saved locally.

Mitigation: Use non-sensitive inputs where possible and confirm that local rental-data files are appropriate for the user's privacy expectations before saving.

Risk: URL parsing and scraping features may fetch broad or untrusted web content.

Mitigation: Limit parsing to trusted rental-site URLs and review URL validation and HTTPS handling before enabling automated fetching.

Risk: Scraping dependencies and browser automation can expand the runtime attack surface.

Mitigation: Pin and review dependencies, run scraping in a constrained environment, and require explicit user confirmation before interactive login or scraping flows.

Risk: Some built-in listing examples are described by server evidence as sample data rather than verified market data.

Mitigation: Label built-in examples as illustrative and require user-provided or independently verified listings for real rental decisions.

## Reference(s):

- [Rental Pitfall Guide](references/pitfall-guide.md)
- [Rental Helper ClawHub page](https://clawhub.ai/sosshuai/skills/rental-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Conversational guidance, Markdown comparison tables, shell command invocations, and local JSON listing or viewing records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores listing and viewing data locally under the OpenClaw rental-data workspace when helper scripts save records.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
