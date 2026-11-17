## Description:

Checks external factual claims against web evidence and cited sources before an agent relies on them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saver-si](https://clawhub.ai/user/saver-si)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to obtain a cited second check of factual claims in research, reports, or other tool outputs. It is not a wallet-security, transaction-simulation, or arithmetic tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Claims and optional context are sent to an external fact-checking service.

Mitigation: Do not send confidential, regulated, or secret material unless the service is approved for that data.

Risk: Verification costs 0.20 USDC per settled request, and uncertain responses could lead to duplicate charges.

Mitigation: Require explicit approval or a bounded wallet policy, verify payment terms, and use result recovery rather than automatically paying again after an uncertain outcome.

Risk: A cited verdict can still misinterpret sources or provide insufficient evidence.

Mitigation: Inspect cited source URLs, treat confidence as non-calibrated, and do not use verdicts to bypass execution policy.

## Reference(s):

- [SAVER Verifier ClawHub release](https://clawhub.ai/saver-si/skills/saver-verifier)
- [SAVER Verify homepage](https://saververify.com)
- [Agent tool specification](https://saververify.com/agent-tool.json)
- [Operator-funded report examples](https://saververify.com/examples.json)
- [API specification](https://api.saververify.com/openapi.json)
- [Payment requirements](https://api.saververify.com/.well-known/x402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [A cited factual assessment in agent-readable text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report insufficient evidence; confidence is not a calibrated probability.]

## Skill Version(s):

1.1.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
