## Description:

Fetch US stock quotes, sentiment, analyst and company data, market activity, and screening results through the SentiSense CLI in plain text or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market researchers use the skill to retrieve US market data such as quotes, sentiment, news, earnings, insider activity, and screening results from an agent workflow or shell script. The data is informational and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes a low-probability version-pinning concern around npx, while its assessment disagreed with the finding.

Mitigation: Use the documented sentisense@0.78.1 commands and review the package before its first execution, as the skill instructs.

## Reference(s):

- [SentiSense website](https://sentisense.ai)
- [SentiSense API reference](https://sentisense.ai/skill.md)
- [ClawHub skill release](https://clawhub.ai/thesentitrader/skills/sentisense-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-text or JSON market data with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market data; no trading or write operations.]

## Skill Version(s):

0.4.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
