## Description:

SkillGuard scans ClawHub skills for prompt injection and malicious content using Lakera Guard before installation, either automatically during install requests or on demand by slug or search query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmerkle](https://clawhub.ai/user/0xmerkle)

### License/Terms of Use:


## Use Case:

Developers and agent operators use SkillGuard to scan ClawHub skills by slug or search query for prompt injection and malicious content before installation, then decide whether to proceed, block, or require explicit override.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes future ClawHub install behavior by persisting install policy in TOOLS.md.

Mitigation: Use an explicit, reversible setup flow and review the policy change before relying on automatic installation blocking.

Risk: The skill sends reusable API and webhook credentials through a third-party actor and webhook setup.

Mitigation: Use narrowly scoped or short-lived tokens and rotate credentials after testing or suspected exposure.

Risk: Webhook callbacks may expose an agent endpoint that can influence future agent behavior.

Mitigation: Use HTTPS-only callback exposure and a dedicated callback receiver that cannot directly submit general agent work.

## Reference(s):

- [ClawHub SkillGuard Skill Page](https://clawhub.ai/0xmerkle/skills/skill-guard-actor)
- [SkillGuard Apify Actor](https://apify.com/numerous_hierarchy/skill-guard-actor)
- [SkillGuard Integration Guide](artifact/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with scan verdicts, summary tables, JSON examples, and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN, LAKERA_API_KEY, OPENCLAW_WEBHOOK_URL, and OPENCLAW_HOOKS_TOKEN; scan results are returned asynchronously by webhook.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
