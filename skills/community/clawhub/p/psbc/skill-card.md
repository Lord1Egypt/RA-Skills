## Description:

Provides concise summaries of Postal Savings Bank of China public product pages, visible billing information, and service announcements without supporting login automation, funds movement, payments, or security bypass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to organize visible PSBC product, account-summary, and announcement information into concise summaries. It is intended for non-sensitive information review and explicitly excludes credential handling, automated login, payments, transfers, and security bypass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates in a banking context and may be asked to process authenticated bill data that could include sensitive personal or financial details.

Mitigation: Use it only on public PSBC product or announcement pages, or on authenticated pages deliberately provided for minimal aggregation; exclude full transaction details, account identifiers, credentials, and session-bearing URLs.

Risk: The security verdict is suspicious because the skill frames some online-banking bill processing as non-sensitive.

Mitigation: Review inputs before use and keep outputs limited to high-level summaries that would be acceptable in chat history or logs.

## Reference(s):

- [Postal Savings Bank of China Official Website](https://www.psbc.com/)
- [ClawHub Skill Page](https://clawhub.ai/mike47512/skills/psbc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should avoid credentials, account identifiers, full transaction details, session-bearing URLs, and sensitive personal data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
