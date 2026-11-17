## Description:

This skill instructs an agent to require user-supplied six-digit verification before file, memory, tool, or other skill access, while allowing only ordinary Q&A before verification except during first-time binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to add an identity-check workflow around an agent so sensitive actions are refused until a user-provided code verifies the current conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to make identity verification a persistent, session-wide gate over files, memory, tools, and other skills.

Mitigation: Install only when that broad gate is intended; prefer scoped configuration that does not alter system prompts, AGENTS.md, long-term memory, or unrelated tools and skills.

Risk: Long-lived agent keys or conversation identifiers could weaken the gate if stored, exposed, or sent in URLs.

Mitigation: Store agent keys only in a dedicated secret store, never persist verification codes, conversation IDs, or release tokens, and prefer request-body parameters over URL query strings for sensitive values.

Risk: Verification service errors or network failures could leave the user's identity unresolved.

Mitigation: Keep the agent in an unverified state on network failures, HTTP 5xx responses, or unsuccessful verification responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-identity-cn)
- [Xinjianxue Identity API](https://chinaapi.xinjianxue.com)
- [Bind identity endpoint](https://chinaapi.xinjianxue.com/api/xinjianxue/identity/agent/bind)
- [Verify identity endpoint](https://chinaapi.xinjianxue.com/api/xinjianxue/identity/verify)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes identity binding, verification, release-query, and credential-handling instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
