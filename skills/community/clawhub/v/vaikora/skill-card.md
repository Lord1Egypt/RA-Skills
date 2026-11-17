## Description:

Route OpenClaw LLM calls through Vaikora for real-time AI agent security monitoring. Every action your agent takes gets scored for risk, anomaly-flagged, and pushed as a security signal to SentinelOne, CrowdStrike, or AWS Security Hub, without changing how your agent works.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data443](https://clawhub.ai/user/data443)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to route OpenClaw LLM traffic through Vaikora for agent action scoring, policy enforcement, anomaly detection, and forwarding high-risk security signals to supported SIEM or EDR connectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vaikora is in the LLM request path and can access full prompts, responses, and the forwarded upstream provider API key.

Mitigation: Evaluate with an isolated Vaikora account and a dedicated spend-limited provider key before routing production traffic.

Risk: Prompts or responses may contain regulated or sensitive data that would be visible to the proxy.

Mitigation: Do not route regulated or sensitive production data until retention, access controls, and vendor requirements have been reviewed.

Risk: The forwarded provider key is exposed to the proxy during use.

Mitigation: Use a test key for evaluation and rotate the upstream provider key after testing.

## Reference(s):

- [Vaikora homepage](https://vaikora.com)
- [Vaikora docs](https://vaikora.com/docs)
- [AWS Marketplace Security Hub connector](https://aws.amazon.com/marketplace/pp/prodview-dotgh5y3ox6rq)
- [AWS Marketplace SentinelOne connector](https://aws.amazon.com/marketplace/pp/prodview-tzxzdoajtk3bu)
- [AWS Marketplace CrowdStrike connector](https://aws.amazon.com/marketplace/pp/prodview-cs7idbycte7fm)
- [Data443](https://data443.com)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VAIKORA_API_KEY, VAIKORA_AGENT_ID, and LLM_PROVIDER_API_KEY environment variables.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
