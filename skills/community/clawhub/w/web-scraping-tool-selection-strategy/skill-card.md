## Description:

Helps agents choose between opencli platform adapters and playwright-cli browser automation for web data collection across social media and e-commerce sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbozhao279-code](https://clawhub.ai/user/wenbozhao279-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to select an appropriate web data collection approach for platform-specific scraping, browser automation, logged-in page access, monitoring, and structured extraction tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer agents toward anti-bot circumvention or authenticated scraping.

Mitigation: Use it only for data you are legally authorized to access, and prefer official APIs or approved exports when available.

Risk: Browser-session reuse can expose private or account-restricted data.

Mitigation: Do not reuse logged-in sessions for third-party scraping unless the account owner has consented and the platform rules permit it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenbozhao279-code/skills/web-scraping-tool-selection-strategy)
- [Browser State Reuse Guide](references/browser-state-reuse-guide.md)
- [Data Extraction Patterns](references/data-extraction-patterns.md)
- [Platform Tool Mapping Reference](references/platform-tool-mapping-reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends tool selection, command patterns, prerequisites, and data quality checks for web scraping workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
