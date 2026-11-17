## Description:

Analyze social media post titles to discover what makes content perform well.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyobject](https://clawhub.ai/user/yyobject)

### License/Terms of Use:


## Use Case:

Content analysts, marketers, and social media operators use this skill to compare high- and low-performing post titles, identify recurring title features, verify those features against engagement metrics, and produce a concise HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports load Tailwind from a CDN when rendered.

Mitigation: Review generated HTML before sharing or opening it in sensitive environments, and allow external CDN loading only where that is acceptable.

Risk: Account identifiers can be sent to Tezign's API when using account-based data retrieval.

Mitigation: Prefer local file analysis for sensitive accounts or data, and confirm users are comfortable with the external API call before using account lookup.

Risk: The skill supports forwarding raw browser cookies through a command-line option.

Mitigation: Do not pass browser session cookies with --cookie; use unauthenticated or local-file workflows where possible.

Risk: The documented dependency installation uses --break-system-packages.

Mitigation: Install dependencies in an isolated virtual environment instead of modifying system Python packages.

Risk: Local run data and generated reports are retained under the workspace runs directory.

Mitigation: Delete run directories after review when they contain sensitive source data, account identifiers, or analysis outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyobject/skills/social-media-title-insight)
- [Tezign account-data API endpoint](https://vms-service-tx.tezign.com/datacenter/ai-insight/public/account-data?size=N)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands, JSON feature definitions, structured verification JSON, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis artifacts to a local runs directory, including cached data, feature JSON, verification JSON, auto-detection metadata, and report.html.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
