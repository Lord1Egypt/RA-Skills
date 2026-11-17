## Description:

Query TDengine time-series database for futures market data using predefined schemas and tags like symbol and exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msincenselee](https://clawhub.ai/user/msincenselee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to connect to a TDengine database and query futures market K-line and tick data using documented supertables, concrete table naming rules, and symbol/exchange tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a hardcoded root TDengine database login.

Mitigation: Replace it with a dedicated read-only TDengine account and avoid passing passwords on the command line.

Risk: The skill includes Python dependency installation guidance.

Mitigation: Install dependencies in an isolated environment with pinned versions or a trusted package source.

## Reference(s):

- [TDengine Database skill instructions](artifact/SKILL.md)
- [TDengine schema reference](artifact/taos_schema.md)
- [ClawHub skill page](https://clawhub.ai/msincenselee/skills/taos)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown with shell and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes TDengine CLI and Python setup examples plus reusable SQL query templates.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
