## Description:

web123 matches plain-language Web3 needs to AntalphaAI skill recommendations and install commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use web123 to browse Web3 skill categories or match tasks such as trading, wallet balance checks, technical analysis, safety scans, payment links, and beginner setup to recommended AntalphaAI skills with install commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill routes wallet and trading requests to unpinned installs for transaction-capable skills without enough risk disclosure.

Mitigation: Review each suggested downstream repository before installation and prefer pinned, reviewed revisions.

Risk: Recommended downstream skills may involve trades, exchange API keys, wallet connections, signatures, approvals, payment links, or leverage.

Mitigation: Treat web123 as navigation only; independently verify permissions, keys, transaction details, and financial risk before use.

## Reference(s):

- [Skill metadata catalog](references/skills.json)
- [web123 ClawHub release page](https://clawhub.ai/deanpeng-dotcom/skills/web123)
- [deanpeng-dotcom ClawHub publisher profile](https://clawhub.ai/user/deanpeng-dotcom)
- [AntalphaAI GitHub organization referenced by the artifact](https://github.com/AntalphaAI)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown recommendations with install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are selected from the bundled skill metadata catalog.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata; artifact frontmatter remains 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
