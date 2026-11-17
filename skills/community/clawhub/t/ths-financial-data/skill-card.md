## Description:

Provides stock market data access for real-time quotes, Chinese name lookup, keyboard abbreviation conversion, fund flow, daily K-line data, and Wencai natural-language queries through the thsdk library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bensema](https://clawhub.ai/user/bensema)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve and analyze A-share, Hong Kong, and U.S. stock market data, including quote lookup, K-line history, fund flow, depth data, and natural-language Wencai results. The skill helps agents resolve ambiguous stock identifiers and return user-facing market data tables or analysis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install or upgrade the third-party thsdk package during normal use.

Mitigation: Review the skill before installation, run it in an isolated environment, and prefer manually installing a pinned and reviewed thsdk version.

Risk: THS username, password, and MAC values may be needed for authenticated access.

Mitigation: Treat THS credentials as secrets and avoid running the skill with unrelated sensitive local credentials available.

## Reference(s):

- [thsdk API Reference](artifact/references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/bensema/skills/ths-financial-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, Python code snippets, shell commands, and structured Python return values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return candidate lists when a stock query is ambiguous; users should select a candidate before downstream data retrieval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
