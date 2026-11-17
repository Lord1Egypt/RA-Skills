## Description:

Scans AISA for market rumor signals related to M&A, insider activity, analyst actions, social media, and regulatory events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and analysts use this skill to scan early market rumor signals and rank them by potential impact. Outputs should be independently verified before any investment or trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_BASE_URL can redirect the AISA API key and prompts to an arbitrary endpoint.

Mitigation: Remove or lock down AISA_BASE_URL and allow only the expected AISA endpoint before deployment.

Risk: The skill sends market-rumor scan requests and prompts to AISA.

Mitigation: Use a narrowly scoped, revocable AISA_API_KEY and avoid submitting confidential information.

Risk: The OpenAI SDK dependency is not pinned.

Mitigation: Pin and review the dependency version before installing in controlled environments.

Risk: Rumor outputs may be unconfirmed or misleading.

Mitigation: Independently verify signals against authoritative market, filing, and news sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/stock-rumors-zh)
- [ClawHub publisher profile](https://clawhub.ai/user/aisadocs)

## Skill Output:

**Output Type(s):** [text, markdown, json]

**Output Format:** [Markdown market-rumor report with an optional compact JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; sends scan requests to AISA.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
