## Description:

Professional-grade web research with multi-source verification and credibility scoring that cross-references multiple sources, scores reliability, and delivers verified intelligence for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run paid web research, fact verification, source credibility checks, and research report generation from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics, claims, and URLs are sent to a paid remote service.

Mitigation: Use the skill only for information that can be shared with the service provider, and avoid submitting sensitive or confidential material.

Risk: The SUPAH_API_BASE environment variable can redirect requests to a different endpoint.

Mitigation: Keep SUPAH_API_BASE unset for the default service, or set it only to a trusted HTTPS endpoint.

Risk: x402 micropayments can incur per-call spending.

Mitigation: Monitor payment activity and set agent-level spending limits before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supah-based/skills/supah-research-intelligence)
- [SUPAH API endpoint](https://api.supah.ai)
- [x402 documentation](https://www.x402.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Console text and markdown-style research summaries with citations, confidence scores, and source credibility fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid remote API calls via x402; outputs depend on the submitted topic, claim, or URL.]

## Skill Version(s):

1.3.0 (source: server release evidence; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
