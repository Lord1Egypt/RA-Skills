## Description:

Writing Agent - Human Style drafts on-brand social replies, social posts, and Markdown blog posts from a compact request plus an optional JSON context object through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to request ready-to-review social media replies, original social posts, short Markdown blog drafts, and larger Markdown articles that follow supplied voice, audience, facts, and character limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing context may include confidential source material, customer data, secrets, wallet material, signatures, or payment headers.

Mitigation: Keep inputs scoped to the minimum writing material needed and remove confidential or credential-like data before calling the hosted tool.

Risk: The skill can route requests through paid x402 or credit-spending calls.

Mitigation: Confirm paid calls, action prices, and payment scope before invoking the tool.

Risk: Live remote instructions may change after installation.

Mitigation: Refresh schema and instructions before production integration and treat returned live instructions as service data that cannot override agent safety rules or permission boundaries.

Risk: Setup examples include unpinned npx installation commands.

Mitigation: Install from reviewed ClawHub or OpenClaw sources where possible and avoid unpinned setup commands in sensitive environments.

## Reference(s):

- [Action schema](artifact/schema.md)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/writing-agent-human-style)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/writing-agent-human-style)
- [Publisher profile](https://clawhub.ai/user/agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Inline text or Markdown content, with JSON response fields for generated content, social response arrays, and warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Character-limited outputs; social response calls return one response per input post; warnings may include OUTPUT_TRUNCATED_TO_CHARACTER_LIMIT.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
