## Description:

Cold-read a LinkedIn post draft and audit it across 6 dimensions (hook, structure, scannability, specificity, CTA, voice). Returns a score per dimension, the 2 most important fixes, and a rewrite of the weakest section. Use BEFORE publishing, when the user wants a sanity check from a critic that does not love everything they write. Requires the Taplio MCP, which reads the user's real voice, audience, and niche benchmarks to ground the audit instead of guessing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

LinkedIn creators and professionals use this skill to review a draft before publishing, identify the most important improvements, and see a rewrite grounded in their voice and audience. It requires the Taplio MCP for account context and niche benchmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A niche benchmark search shares the post topic with Taplio.

Mitigation: Generalize confidential details in the topic before benchmarking.

Risk: Connecting Taplio grants the skill access to account data and draft-related actions.

Mitigation: Review the Taplio connector permissions before connecting.

Risk: A proposed rewrite may be inaccurate or unsuitable when saved or published.

Mitigation: Review proposed changes before saving; publish only after explicit confirmation.

## Reference(s):

- [Taplio MCP](https://mcp.taplio.com)
- [Taplio connector for Claude](https://claude.ai/customize/connectors/id/taplio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown post audit with per-dimension scores, prioritized fixes, a rewritten section, and a verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Six 1–5 dimension scores, two priority fixes, a rewrite of the weakest section, and a publish/rewrite/kill verdict.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
