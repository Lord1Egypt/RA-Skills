## Description:

瑞玥餐饮API2 enables a restaurant customer-service agent to query live shop, menu, table, appointment, member, transaction, order, and payment-link data and perform booking or ordering actions through configured tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhimibuhui](https://clawhub.ai/user/zhimibuhui)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant customers and staff-facing agents use this skill to answer live dining questions and complete booking, ordering, cancellation, member, transaction, and payment-link workflows without relying on stale knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default backend connection is configured over HTTP.

Mitigation: Change the API base to an HTTPS endpoint before deployment in a controlled internal environment.

Risk: The skill can perform live booking, ordering, cancellation, and payment-link actions.

Mitigation: Require explicit user confirmation before invoking write or payment-link tools.

Risk: Tool arguments include identifiers such as memberId, reserveId, orderId, tenantId, and shopId.

Mitigation: Validate identifiers before placing them into URL paths or request bodies.

Risk: Broad trigger rules could route sensitive or high-impact dining operations too aggressively.

Mitigation: Tighten trigger rules and keep query, write, cancellation, and payment-link intents clearly separated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhimibuhui/skills/ry-drink2)
- [Publisher profile](https://clawhub.ai/user/zhimibuhui)
- [Tool manifest](artifact/tools.json)
- [Tool routing notes](artifact/tool-router.md)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Plain text responses backed by JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing responses should hide tool execution details and internal identifiers, except complete payment links when requested.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact skill.json reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
