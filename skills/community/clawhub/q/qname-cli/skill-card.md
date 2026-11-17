## Description:

Use QName AI from the terminal for WHOIS, traffic, or Google Ads keyword research through the approved QName AI API, staying within the key's approved API types and quotas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibevibing](https://clawhub.ai/user/vibevibing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to run approved QName AI CLI workflows for WHOIS/domain availability, traffic lookup, and Google Ads keyword research while respecting configured API entitlements and quotas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A QName AI API key could be exposed through shell history, printed configuration, or overly broad local handling.

Mitigation: Use short-lived environment variables or an interactive secret flow, treat the key as a secret, and avoid printing secrets unless the user explicitly requests inspection.

Risk: Commands could exceed approved per-request or daily quotas, or use traffic and keyword APIs without the configured key being entitled for them.

Mitigation: Keep automation within approved quotas and use traffic or keyword commands only when the key is approved for the matching API type.

Risk: Keyword results may be scoped incorrectly if the default United States and English target IDs do not match the task.

Mitigation: Set country, language, and network options explicitly when the default targeting does not match the user's research need.

## Reference(s):

- [QName AI](https://qname.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance favors JSON output for agent parsing and includes quota, entitlement, and secret-handling constraints.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
