## Description:

Yyqdata Stock Skill helps agents translate Chinese market-data questions into authenticated yyqdata OpenAPI requests for A-share, Hong Kong, U.S., fund, macro, derivative, bond, forex, research, and news data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kouyusanpi](https://clawhub.ai/user/kouyusanpi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and compatible agent users use this skill to answer Chinese stock and market-data questions by resolving securities, calling documented yyqdata REST endpoints, and summarizing results with traceable API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API token for yyqdata requests.

Mitigation: Store the token in a platform secret manager or protected environment variable, avoid pasting it into chat or URLs, and prefer Authorization headers over query parameters.

Risk: Network configuration can expose requests or credentials if an insecure base URL is used.

Mitigation: Use HTTPS-only yyqdata endpoints where available and avoid sending tokens through URLs that may be logged.

Risk: The package includes an update script that downloads and installs remote skill contents.

Mitigation: Review update.sh before running it, install only from the expected yyqdata manifest and zip URLs, and verify checksums when updating.

Risk: Administrative provisioning credentials could grant broader access than normal data-query use requires.

Mitigation: Do not provide admin.provision or other administrative credentials to the agent for routine market-data queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kouyusanpi/skills/yyqdata-stock-skill)
- [yyqdata release manifest](https://static.yyqyx.com/skill/yyqdata.manifest.json)
- [API quick reference](artifact/references/api-quick-reference.md)
- [API full specification](artifact/references/api-full-spec.md)
- [Data catalog](artifact/references/data-catalog.md)
- [Agent installation guide](artifact/INSTALL-AGENT.md)
- [yyqdata website](https://www.yyqyx.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and bash/curl commands; longer data pulls may include CSV file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a yyqdata token and outbound HTTP access to yyqdata OpenAPI endpoints.]

## Skill Version(s):

3.5.31 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
