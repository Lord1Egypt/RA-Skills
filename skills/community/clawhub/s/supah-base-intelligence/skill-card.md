## Description:

Comprehensive token intelligence for Base blockchain, including risk scores, whale tracking, signal analysis, and safety checks for Base tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to request Base token risk assessments, safety scans, portfolio checks, whale movement monitoring, and trading signal summaries. It supports pre-trade research and portfolio monitoring, not automated trading decisions without separate review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid x402 API calls may execute automatically and incur USDC charges.

Mitigation: Require explicit user approval for paid calls and configure spending limits in the x402 client before use.

Risk: Token and wallet identifiers are sent to the configured API host.

Mitigation: Use the default SUPAH API endpoint unless an alternate SUPAH_API_BASE destination has been reviewed and trusted.

Risk: Trading signals and risk scores may be incomplete or misleading if used as the only basis for financial decisions.

Mitigation: Treat outputs as research inputs and require independent review before trading or portfolio actions.

Risk: Artifact pricing statements are inconsistent across files and commands.

Mitigation: Confirm expected per-call pricing in the x402 client before authorizing each paid request.

## Reference(s):

- [SUPAH Website](https://supah.ai)
- [SUPAH API Endpoint](https://api.supah.ai)
- [x402 Protocol](https://www.x402.org)
- [ClawHub Skill Page](https://clawhub.ai/supah-based/skills/supah-base-intelligence)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-style agent responses, CLI text, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include token scores, safety status, wallet or whale summaries, signal lists, recommendations, and per-call x402 USDC cost information.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
