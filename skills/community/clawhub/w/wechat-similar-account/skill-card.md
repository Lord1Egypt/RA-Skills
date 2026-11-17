## Description:

Recommends peer and aspirational WeChat Official Accounts using RedFox account data and a three-layer weighted matching method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat Official Account creators, content operators, MCN teams, and brand marketers use this skill to query an account by name, account ID, or category and receive comparable accounts, performance context, and recommendation reasons for growth planning or ad placement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's account query and REDFOX_API_KEY to redfox.hk.

Mitigation: Use a temporary, scoped, or managed RedFox secret; confirm the key source, scope, expiry, and revocation process before use.

Risk: The skill searches local shell or user profile locations for REDFOX_API_KEY and its documentation encourages persistent profile-based configuration.

Mitigation: Prefer session-scoped environment variables or a managed secret store, and avoid writing long-lived API keys to shell profiles.

Risk: Generated results may include vendor subscription or enterprise-sales messaging.

Mitigation: Review output before sharing it externally and separate account analysis from promotional sections when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/wechat-similar-account)
- [Core workflow reference](references/core_workflow.md)
- [RedFox data platform](https://redfox.hk/)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox enterprise services](https://redfox.hk/dashboard/enterprise)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-formatted account diagnostics, benchmark tables, recommendation reasons, and short command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY and sends account lookup requests to redfox.hk.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
